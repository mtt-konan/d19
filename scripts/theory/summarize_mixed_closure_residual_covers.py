#!/usr/bin/env python3
"""Summarize explicit 2-cover probes for mixed-closure residual rows."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


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


def _row_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return int(row["A"]), int(row["B"]), str(row["curve"])


def _diagnostic_index(
    diagnostic_rows: list[dict[str, Any]] | None,
) -> dict[tuple[int, int, str], dict[str, Any]]:
    if not diagnostic_rows:
        return {}
    return {_row_key(row): row for row in diagnostic_rows}


def _selmer_gap(row: dict[str, Any] | None) -> int | None:
    if row is None or row.get("status") != "ok":
        return None
    if "selmer_rank_pari" not in row or "torsion_two_dimension" not in row:
        return None
    return int(row["selmer_rank_pari"]) - int(row["torsion_two_dimension"])


def _alignment(covers_without_points: int, selmer_gap: int | None) -> str:
    if selmer_gap is None:
        return "missing-diagnostic"
    if covers_without_points == selmer_gap:
        return "match"
    return "mismatch"


def _evidence_level(row: dict[str, Any], covers_without_points: int) -> str:
    if row.get("status") != "ok":
        return "no-cover-data"
    if covers_without_points > 0:
        return "bounded-search-no-point-candidate"
    return "bounded-search-found-points-on-all-covers"


def _point_count_pattern(row: dict[str, Any]) -> str:
    return json.dumps([cover.get("point_count") for cover in row.get("covers", [])])


def _no_point_cover_indices(row: dict[str, Any]) -> list[int]:
    indices: list[int] = []
    for cover in row.get("covers", []):
        if cover.get("point_count") == 0:
            indices.append(int(cover["index"]))
    return indices


def _counter_dict(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def summarize_cover_rows(
    cover_rows: list[dict[str, Any]],
    *,
    diagnostic_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    diagnostics = _diagnostic_index(diagnostic_rows)
    status_counts: Counter[str] = Counter()
    cover_count_counts: Counter[str] = Counter()
    covers_without_points_counts: Counter[str] = Counter()
    point_count_patterns: Counter[str] = Counter()
    selmer_gap_alignment_counts: Counter[str] = Counter()
    evidence_level_counts: Counter[str] = Counter()
    rows_by_curve: dict[str, dict[str, Counter[str]]] = defaultdict(
        lambda: {
            "status_counts": Counter(),
            "cover_count_counts": Counter(),
            "covers_without_points_counts": Counter(),
            "point_count_patterns": Counter(),
            "selmer_gap_alignment_counts": Counter(),
            "evidence_level_counts": Counter(),
        }
    )
    no_point_cover_rows: list[dict[str, Any]] = []

    for row in cover_rows:
        curve = str(row["curve"])
        status = str(row.get("status", "missing"))
        cover_count = int(row.get("cover_count", 0))
        covers_without_points = int(row.get("covers_without_points", 0))
        selmer_gap = _selmer_gap(diagnostics.get(_row_key(row)))
        alignment = _alignment(covers_without_points, selmer_gap)
        evidence_level = _evidence_level(row, covers_without_points)
        pattern = _point_count_pattern(row)

        status_counts[status] += 1
        cover_count_counts[str(cover_count)] += 1
        covers_without_points_counts[str(covers_without_points)] += 1
        point_count_patterns[pattern] += 1
        selmer_gap_alignment_counts[alignment] += 1
        evidence_level_counts[evidence_level] += 1

        curve_bucket = rows_by_curve[curve]
        curve_bucket["status_counts"][status] += 1
        curve_bucket["cover_count_counts"][str(cover_count)] += 1
        curve_bucket["covers_without_points_counts"][str(covers_without_points)] += 1
        curve_bucket["point_count_patterns"][pattern] += 1
        curve_bucket["selmer_gap_alignment_counts"][alignment] += 1
        curve_bucket["evidence_level_counts"][evidence_level] += 1

        if covers_without_points > 0:
            no_point_cover_rows.append(
                {
                    "A": int(row["A"]),
                    "B": int(row["B"]),
                    "curve": curve,
                    "cover_count": cover_count,
                    "covers_without_points": covers_without_points,
                    "no_point_cover_indices": _no_point_cover_indices(row),
                    "selmer_gap": selmer_gap,
                    "selmer_gap_alignment": alignment,
                    "evidence_level": evidence_level,
                }
            )

    return {
        "rows": len(cover_rows),
        "status_counts": _counter_dict(status_counts),
        "cover_count_counts": _counter_dict(cover_count_counts),
        "covers_without_points_counts": _counter_dict(covers_without_points_counts),
        "point_count_patterns": _counter_dict(point_count_patterns),
        "selmer_gap_alignment_counts": _counter_dict(selmer_gap_alignment_counts),
        "evidence_level_counts": _counter_dict(evidence_level_counts),
        "rows_by_curve": {
            curve: {name: _counter_dict(counter) for name, counter in buckets.items()}
            for curve, buckets in sorted(rows_by_curve.items())
        },
        "no_point_cover_rows": no_point_cover_rows,
        "boundary": (
            "A no-point cover here means hyperellratpoints found no point up to "
            "the chosen height. It is an explicit Sha[2] candidate, not a proof "
            "that the cover has no rational point."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--covers", type=Path, required=True, help="ell2cover JSONL input.")
    parser.add_argument(
        "--diagnostics",
        type=Path,
        default=None,
        help="Optional Sage Selmer diagnostic JSONL input.",
    )
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cover_rows = load_jsonl(args.covers)
    diagnostic_rows = load_jsonl(args.diagnostics) if args.diagnostics else None
    summary = summarize_cover_rows(cover_rows, diagnostic_rows=diagnostic_rows)
    write_json(args.out, summary)
    print(f"wrote residual cover summary for {summary['rows']} rows to {args.out}")
    print(f"status_counts={summary['status_counts']}")
    print(f"covers_without_points_counts={summary['covers_without_points_counts']}")
    print(f"selmer_gap_alignment_counts={summary['selmer_gap_alignment_counts']}")
    print(f"evidence_level_counts={summary['evidence_level_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
