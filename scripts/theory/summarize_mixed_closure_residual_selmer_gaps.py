#!/usr/bin/env python3
"""Summarize residual mixed-closure Selmer/Sha[2] gap diagnostics."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


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


def _row_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return int(row["A"]), int(row["B"]), str(row["curve"])


def _diagnostic_index(
    diagnostics: list[dict[str, Any]],
) -> dict[tuple[int, int, str], dict[str, Any]]:
    return {_row_key(row): row for row in diagnostics}


def _int_value(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0) or 0)


def _rank_bounds(diagnostic: dict[str, Any]) -> list[int]:
    return [int(value) for value in diagnostic.get("rank_bounds", [])]


def _selmer_rank(diagnostic: dict[str, Any]) -> int:
    return _int_value(diagnostic, "selmer_rank_mwrank") or _int_value(
        diagnostic, "selmer_rank_pari"
    )


def _gap_type(
    *,
    diagnostic_status: str,
    rank_bounds: list[int],
    priority_selmer_gap: int,
    rank_plus_sha2_dimension: int,
) -> str:
    if diagnostic_status != "ok":
        return "diagnostic-open"
    if (
        rank_bounds == [0, 2]
        and priority_selmer_gap == 2
        and rank_plus_sha2_dimension == 2
    ):
        return "rank0-sha2-gap2"
    return "residual-gap-open"


def build_selmer_gap_ledger(
    *,
    priorities: dict[str, Any],
    diagnostics: list[dict[str, Any]],
) -> dict[str, Any]:
    diagnostics_by_key = _diagnostic_index(diagnostics)
    rows: list[dict[str, Any]] = []
    diagnostic_status_counts: Counter[str] = Counter()
    missing_diagnostic_rows = 0
    all_rows_candidate_not_proof = True

    for priority_row in priorities.get("rows", []):
        diagnostic = diagnostics_by_key.get(_row_key(priority_row), {})
        diagnostic_status = str(diagnostic.get("status", "missing"))
        diagnostic_status_counts.update([diagnostic_status])
        if not diagnostic:
            missing_diagnostic_rows += 1
        proof_status = str(priority_row.get("proof_status", "candidate-not-proof"))
        all_rows_candidate_not_proof = (
            all_rows_candidate_not_proof and proof_status == "candidate-not-proof"
        )
        rank_bounds = _rank_bounds(diagnostic)
        priority_selmer_gap = _int_value(priority_row, "selmer_gap")
        rank_plus_sha2_dimension = _int_value(diagnostic, "rank_plus_sha2_dimension")
        rows.append(
            {
                "priority": int(priority_row["priority"]),
                "A": int(priority_row["A"]),
                "B": int(priority_row["B"]),
                "curve": str(priority_row["curve"]),
                "cover_index": int(priority_row["cover_index"]),
                "priority_selmer_gap": priority_selmer_gap,
                "diagnostic_status": diagnostic_status,
                "rank_bounds": rank_bounds,
                "selmer_rank": _selmer_rank(diagnostic),
                "torsion_two_dimension": _int_value(
                    diagnostic, "torsion_two_dimension"
                ),
                "rank_plus_sha2_dimension": rank_plus_sha2_dimension,
                "root_number": _int_value(diagnostic, "root_number"),
                "conductor": _int_value(diagnostic, "conductor"),
                "has_bsd_conditional_rank0": bool(
                    priority_row.get("has_bsd_conditional_rank0", False)
                ),
                "proof_status": proof_status,
                "gap_type": _gap_type(
                    diagnostic_status=diagnostic_status,
                    rank_bounds=rank_bounds,
                    priority_selmer_gap=priority_selmer_gap,
                    rank_plus_sha2_dimension=rank_plus_sha2_dimension,
                ),
            }
        )

    return {
        "candidate_cover_total": len(rows),
        "diagnostic_status_counts": dict(sorted(diagnostic_status_counts.items())),
        "rows_with_ok_diagnostics": int(diagnostic_status_counts.get("ok", 0)),
        "missing_diagnostic_rows": missing_diagnostic_rows,
        "rank0_sha2_gap2_cover_total": sum(
            1 for row in rows if row["gap_type"] == "rank0-sha2-gap2"
        ),
        "gap_type_counts": dict(sorted(Counter(row["gap_type"] for row in rows).items())),
        "all_rows_candidate_not_proof": all_rows_candidate_not_proof,
        "rows": rows,
        "boundary": (
            "This ledger organizes residual Selmer/Sha[2] gaps. It does not "
            "prove that any residual cover has no rational point."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--priorities", type=Path, required=True)
    parser.add_argument("--diagnostics", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ledger = build_selmer_gap_ledger(
        priorities=load_json(args.priorities),
        diagnostics=load_jsonl(args.diagnostics),
    )
    write_json(args.out, ledger)
    print(f"wrote residual Selmer gap ledger to {args.out}")
    print(f"candidate_cover_total={ledger['candidate_cover_total']}")
    print(f"rank0_sha2_gap2_cover_total={ledger['rank0_sha2_gap2_cover_total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
