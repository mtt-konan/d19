#!/usr/bin/env python3
"""Compress AA+BB common-source 2-primary patterns into multiplicative types."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits multiplicative type compression of the 16 AA+BB common-source "
    "2-primary squareclass patterns. It does not prove any dyadic local "
    "condition, Selmer lift, Selmer rank bound, rank zero, or lambda-family "
    "exclusion."
)


def _type_id(row: dict[str, Any]) -> str:
    triple = sorted(
        [
            str(row.get("x_minus_p", "")),
            str(row.get("x_pos_2sqrt_q", "")),
            str(row.get("x_neg_2sqrt_q", "")),
        ]
    )
    if triple == ["1", "1", "1"]:
        return "all_trivial"
    if triple == ["-1", "-1", "1"]:
        return "minus_one_pair"
    if triple == ["1", "2", "2"]:
        return "two_pair"
    if triple == ["-2", "-2", "1"]:
        return "minus_two_pair"
    if triple == ["-1", "-2", "2"]:
        return "fully_mixed_nontrivial"
    return "unexpected"


def audit_rank_zero_aa_bb_common_source_pattern_types(
    common_source_patterns: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if (
        common_source_patterns.get("status") != "ok"
        or common_source_patterns.get("ready") is not True
        or int(common_source_patterns.get("common_source_kernel_triple_pattern_count", 0) or 0)
        != 16
    ):
        violations.append("common_source_patterns_not_ready")

    rows = list(common_source_patterns.get("common_source_pattern_rows", []))
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[_type_id(row)].append(dict(row))

    if "unexpected" in grouped:
        violations.append("unexpected_pattern_type")

    expected_sizes = {
        "all_trivial": 1,
        "minus_one_pair": 3,
        "two_pair": 3,
        "minus_two_pair": 3,
        "fully_mixed_nontrivial": 6,
    }
    for type_id, expected_size in expected_sizes.items():
        if len(grouped.get(type_id, [])) != expected_size:
            violations.append(f"type_size_mismatch={type_id}")

    status = "ok" if not violations else "issues"
    type_rows = [
        {
            "type_id": type_id,
            "pattern_count": len(grouped[type_id]),
            "representative": grouped[type_id][0],
            "description": {
                "all_trivial": "all three kernel classes trivial",
                "minus_one_pair": "one trivial class and two -1 classes",
                "two_pair": "one trivial class and two 2 classes",
                "minus_two_pair": "one trivial class and two -2 classes",
                "fully_mixed_nontrivial": "the three distinct nontrivial classes {-1,2,-2}",
            }[type_id],
        }
        for type_id in [
            "all_trivial",
            "minus_one_pair",
            "two_pair",
            "minus_two_pair",
            "fully_mixed_nontrivial",
        ]
    ]
    return {
        "status": status,
        "ready": status == "ok",
        "pattern": "AA+BB",
        "raw_pattern_count": len(rows),
        "pattern_type_count": len(type_rows),
        "type_rows": type_rows,
        "next_target": (
            "Check dyadic local-image and Selmer-lift compatibility by pattern type "
            "before descending to the 16 raw assignments."
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--common-source-patterns", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_common_source_pattern_types(
        load_json(args.common_source_patterns)
    )
    write_json(args.out, audit)
    print(
        "wrote closure quotient rank-zero AA+BB common-source pattern types to "
        f"{args.out}"
    )
    print(f"status={audit['status']}")
    print(f"raw_pattern_count={audit['raw_pattern_count']}")
    print(f"pattern_type_count={audit['pattern_type_count']}")
    print(
        "selmer_rank_upper_bound_proved_count="
        f"{audit['selmer_rank_upper_bound_proved_count']}"
    )
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
