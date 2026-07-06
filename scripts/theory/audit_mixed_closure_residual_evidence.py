#!/usr/bin/env python3
"""Audit mixed-closure AA/BB residual evidence across stored result files."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

Key = tuple[int, int, str]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _row_key(row: dict[str, Any]) -> Key:
    return int(row["A"]), int(row["B"]), str(row["curve"])


def _index_rows(rows: list[dict[str, Any]]) -> dict[Key, dict[str, Any]]:
    return {_row_key(row): row for row in rows}


def _counter_dict(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def _alignment(ok: bool) -> str:
    return "match" if ok else "mismatch"


def _violation(row: dict[str, Any], kind: str, **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "A": int(row["A"]),
        "B": int(row["B"]),
        "curve": str(row["curve"]),
        "kind": kind,
    }
    payload.update(extra)
    return payload


def _target_rows(
    rank_summary: dict[str, Any],
    curves: set[str],
) -> list[dict[str, Any]]:
    rows = [
        row
        for row in rank_summary.get("uncertain_rank_rows", [])
        if str(row.get("curve")) in curves
    ]
    return sorted(rows, key=lambda row: (int(row["A"]), int(row["B"]), str(row["curve"])))


def _no_point_cover_indices(cover_row: dict[str, Any] | None) -> list[int]:
    if cover_row is None:
        return []
    indices: list[int] = []
    for cover in cover_row.get("covers", []):
        if cover.get("point_count") == 0:
            indices.append(int(cover["index"]))
    return indices


def _status_counts_for_targets(
    rows_by_key: dict[Key, dict[str, Any]],
    target_rows: list[dict[str, Any]],
) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in target_rows:
        stored = rows_by_key.get(_row_key(row))
        counts[str(stored.get("status", "missing")) if stored is not None else "missing"] += 1
    return counts


def audit_residual_evidence(
    *,
    rank_summary: dict[str, Any],
    diagnostic_rows: list[dict[str, Any]],
    cover_rows: list[dict[str, Any]],
    bsd_rows: list[dict[str, Any]],
    curves: set[str],
) -> dict[str, Any]:
    targets = _target_rows(rank_summary, curves)
    diagnostics_by_key = _index_rows(diagnostic_rows)
    covers_by_key = _index_rows(cover_rows)
    bsd_by_key = _index_rows(bsd_rows)

    selmer_backend_alignment_counts: Counter[str] = Counter()
    rank_plus_sha2_alignment_counts: Counter[str] = Counter()
    cover_count_selmer_alignment_counts: Counter[str] = Counter()
    no_point_selmer_gap_alignment_counts: Counter[str] = Counter()
    residual_rows: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    candidate_cover_total = 0
    candidate_rows = 0
    bsd_conditional_rank0_rows = 0

    for row in targets:
        key = _row_key(row)
        diagnostic = diagnostics_by_key.get(key)
        cover = covers_by_key.get(key)
        bsd = bsd_by_key.get(key)

        if diagnostic is None:
            violations.append(_violation(row, "missing-diagnostic-row"))
        if cover is None:
            violations.append(_violation(row, "missing-cover-row"))
        if bsd is None:
            violations.append(_violation(row, "missing-bsd-row"))

        selmer_rank_pari: int | None = None
        selmer_rank_mwrank: int | None = None
        torsion_two_dimension: int | None = None
        selmer_gap: int | None = None

        if diagnostic is not None:
            if diagnostic.get("status") != "ok":
                violations.append(
                    _violation(
                        row,
                        "diagnostic-status-not-ok",
                        status=str(diagnostic.get("status", "missing")),
                    )
                )
            selmer_rank_pari = int(diagnostic["selmer_rank_pari"])
            selmer_rank_mwrank = int(diagnostic["selmer_rank_mwrank"])
            torsion_two_dimension = int(diagnostic["torsion_two_dimension"])
            selmer_gap = selmer_rank_pari - torsion_two_dimension

            selmer_match = selmer_rank_pari == selmer_rank_mwrank
            selmer_backend_alignment_counts[_alignment(selmer_match)] += 1
            if not selmer_match:
                violations.append(
                    _violation(
                        row,
                        "selmer-backend-mismatch",
                        selmer_rank_pari=selmer_rank_pari,
                        selmer_rank_mwrank=selmer_rank_mwrank,
                    )
                )

            actual_rank_plus_sha2 = int(diagnostic["rank_plus_sha2_dimension"])
            rank_plus_match = actual_rank_plus_sha2 == selmer_gap
            rank_plus_sha2_alignment_counts[_alignment(rank_plus_match)] += 1
            if not rank_plus_match:
                violations.append(
                    _violation(
                        row,
                        "rank-plus-sha2-mismatch",
                        expected=selmer_gap,
                        actual=actual_rank_plus_sha2,
                    )
                )

        cover_count: int | None = None
        covers_without_points: int | None = None
        no_point_cover_indices = _no_point_cover_indices(cover)
        if cover is not None:
            if cover.get("status") != "ok":
                violations.append(
                    _violation(
                        row,
                        "cover-status-not-ok",
                        status=str(cover.get("status", "missing")),
                    )
                )
            cover_count = int(cover["cover_count"])
            covers_without_points = int(cover["covers_without_points"])
            candidate_cover_total += covers_without_points
            if covers_without_points > 0:
                candidate_rows += 1

            if selmer_rank_pari is not None:
                cover_count_match = cover_count == selmer_rank_pari
                cover_count_selmer_alignment_counts[_alignment(cover_count_match)] += 1
                if not cover_count_match:
                    violations.append(
                        _violation(
                            row,
                            "cover-count-selmer-mismatch",
                            expected=selmer_rank_pari,
                            actual=cover_count,
                        )
                    )

            if selmer_gap is not None:
                no_point_match = covers_without_points == selmer_gap
                no_point_selmer_gap_alignment_counts[_alignment(no_point_match)] += 1
                if not no_point_match:
                    violations.append(
                        _violation(
                            row,
                            "no-point-selmer-gap-mismatch",
                            expected=selmer_gap,
                            actual=covers_without_points,
                        )
                    )

        bsd_status = str(bsd.get("status", "missing")) if bsd is not None else "missing"
        bsd_analytic_rank = None
        if bsd is not None and bsd.get("status") == "ok":
            bsd_analytic_rank = int(bsd["analytic_rank"])
            if bsd_analytic_rank == 0:
                bsd_conditional_rank0_rows += 1

        residual_rows.append(
            {
                "A": int(row["A"]),
                "B": int(row["B"]),
                "curve": str(row["curve"]),
                "input_rank": str(row["rank"]),
                "selmer_rank_pari": selmer_rank_pari,
                "selmer_rank_mwrank": selmer_rank_mwrank,
                "torsion_two_dimension": torsion_two_dimension,
                "selmer_gap": selmer_gap,
                "cover_count": cover_count,
                "covers_without_points": covers_without_points,
                "no_point_cover_indices": no_point_cover_indices,
                "bsd_status": bsd_status,
                "bsd_analytic_rank": bsd_analytic_rank,
                "evidence_level": "explicit-sha2-candidate"
                if covers_without_points and covers_without_points > 0
                else "no-candidate-cover",
                "proof_status": "candidate-not-proof",
            }
        )

    return {
        "target_curves": sorted(curves),
        "target_rows": len(targets),
        "diagnostic_rows": len(diagnostic_rows),
        "cover_rows": len(cover_rows),
        "bsd_rows": len(bsd_rows),
        "diagnostic_status_counts": _counter_dict(
            _status_counts_for_targets(diagnostics_by_key, targets)
        ),
        "cover_status_counts": _counter_dict(_status_counts_for_targets(covers_by_key, targets)),
        "bsd_status_counts": _counter_dict(_status_counts_for_targets(bsd_by_key, targets)),
        "selmer_backend_alignment_counts": _counter_dict(selmer_backend_alignment_counts),
        "rank_plus_sha2_alignment_counts": _counter_dict(rank_plus_sha2_alignment_counts),
        "cover_count_selmer_alignment_counts": _counter_dict(
            cover_count_selmer_alignment_counts
        ),
        "no_point_selmer_gap_alignment_counts": _counter_dict(
            no_point_selmer_gap_alignment_counts
        ),
        "candidate_cover_total": candidate_cover_total,
        "candidate_rows": candidate_rows,
        "bsd_conditional_rank0_rows": bsd_conditional_rank0_rows,
        "violations": violations,
        "residual_rows": residual_rows,
        "boundary": (
            "This audit aligns stored residual evidence across rank summary, Sage "
            "Selmer diagnostics, PARI ell2cover probes, and BSD diagnostics. "
            "Every no-point cover remains a bounded-search Sha[2] candidate, not "
            "a proof that the cover has no rational point."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank-summary", type=Path, required=True)
    parser.add_argument("--diagnostics", type=Path, required=True)
    parser.add_argument("--covers", type=Path, required=True)
    parser.add_argument("--bsd", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--curve",
        action="append",
        choices=["AA", "AB", "BA", "BB"],
        default=[],
        help="Residual curve to audit. Defaults to AA and BB.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    curves = set(args.curve or ["AA", "BB"])
    audit = audit_residual_evidence(
        rank_summary=load_json(args.rank_summary),
        diagnostic_rows=load_jsonl(args.diagnostics),
        cover_rows=load_jsonl(args.covers),
        bsd_rows=load_jsonl(args.bsd),
        curves=curves,
    )
    write_json(args.out, audit)
    violation_count = len(audit["violations"])
    print(f"wrote mixed closure residual evidence audit to {args.out}")
    print(f"target_rows={audit['target_rows']}")
    print(f"candidate_cover_total={audit['candidate_cover_total']}")
    print(f"violations={violation_count}")
    if args.strict and violation_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
