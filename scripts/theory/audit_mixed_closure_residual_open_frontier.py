#!/usr/bin/env python3
"""Audit the remaining open frontier for mixed-closure residual covers."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This is an open-frontier ledger. It sorts remaining residual covers "
    "by the next missing proof ingredient; it does not prove no-pointness."
)

NEXT_STEPS = {
    "bsd-conditional-no-point": (
        "conditional evidence only; do not count as strict proof"
    ),
    "rank-zero-needs-rank-proof": (
        "prove rank zero; torsion-preimage audit can then rule out points"
    ),
    "rank1-needs-visible-generator-or-descent": (
        "separate the rank-one part from the residual Sha[2] class"
    ),
    "even-rank-gap4-needs-deeper-descent": (
        "run a deeper descent or independent Sha[2] obstruction"
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _cover_key(row: dict[str, Any]) -> tuple[int, int, str, int]:
    return (
        int(row["A"]),
        int(row["B"]),
        str(row["curve"]),
        int(row["cover_index"]),
    )


def _bsd_conditional_keys(
    bsd_conditional_no_point_audit: dict[str, Any],
) -> set[tuple[int, int, str, int]]:
    return {
        _cover_key(row)
        for row in bsd_conditional_no_point_audit.get("rows", [])
        if row.get("conditional_no_point_status") == "bsd-conditional-no-point"
    }


def _frontier_type(
    *,
    gap_type: str,
    is_bsd_conditional_no_point: bool,
) -> str:
    if is_bsd_conditional_no_point:
        return "bsd-conditional-no-point"
    if gap_type == "rank0-sha2-gap2":
        return "rank-zero-needs-rank-proof"
    if gap_type == "rank1-sha2-gap2-open":
        return "rank1-needs-visible-generator-or-descent"
    if gap_type == "even-rank-sha2-gap4-open":
        return "even-rank-gap4-needs-deeper-descent"
    return "unclassified-open"


def audit_residual_open_frontier(
    *,
    selmer_gap_ledger: dict[str, Any],
    bsd_conditional_no_point_audit: dict[str, Any],
) -> dict[str, Any]:
    bsd_conditional_keys = _bsd_conditional_keys(bsd_conditional_no_point_audit)
    rows: list[dict[str, Any]] = []

    for ledger_row in selmer_gap_ledger.get("rows", []):
        gap_type = str(ledger_row["gap_type"])
        frontier_type = _frontier_type(
            gap_type=gap_type,
            is_bsd_conditional_no_point=_cover_key(ledger_row)
            in bsd_conditional_keys,
        )
        rows.append(
            {
                "priority": int(ledger_row["priority"]),
                "A": int(ledger_row["A"]),
                "B": int(ledger_row["B"]),
                "curve": str(ledger_row["curve"]),
                "cover_index": int(ledger_row["cover_index"]),
                "gap_type": gap_type,
                "frontier_type": frontier_type,
                "next_step": NEXT_STEPS.get(
                    frontier_type, "classify this residual cover before claiming more"
                ),
                "candidate_not_proof": True,
            }
        )

    frontier_type_counts = dict(
        sorted(Counter(row["frontier_type"] for row in rows).items())
    )
    open_frontier_type_counts = {
        key: value
        for key, value in frontier_type_counts.items()
        if key != "bsd-conditional-no-point"
    }

    return {
        "status": "ok",
        "candidate_cover_total": len(rows),
        "conditional_no_point_cover_count": frontier_type_counts.get(
            "bsd-conditional-no-point", 0
        ),
        "strict_no_point_cover_count": 0,
        "open_frontier_cover_count": sum(open_frontier_type_counts.values()),
        "frontier_type_counts": frontier_type_counts,
        "open_frontier_type_counts": open_frontier_type_counts,
        "rows": rows,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selmer-gap-ledger", type=Path, required=True)
    parser.add_argument("--bsd-conditional-no-point-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_residual_open_frontier(
        selmer_gap_ledger=load_json(args.selmer_gap_ledger),
        bsd_conditional_no_point_audit=load_json(
            args.bsd_conditional_no_point_audit
        ),
    )
    write_json(args.out, audit)
    print(f"wrote residual open-frontier audit to {args.out}")
    print(f"candidate_cover_total={audit['candidate_cover_total']}")
    print(f"open_frontier_cover_count={audit['open_frontier_cover_count']}")
    print(f"strict_no_point_cover_count={audit['strict_no_point_cover_count']}")
    if args.strict and audit["strict_no_point_cover_count"] != 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
