#!/usr/bin/env python3
"""Audit the dyadic target matrix for AA+BB common-source pattern types."""

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
    "This audits the per-kernel 2-primary squareclass supports of the AA+BB "
    "common-source pattern types. It does not prove any dyadic local image, "
    "Selmer lift, Selmer rank bound, rank zero, or lambda-family exclusion."
)

KERNELS = ("x_minus_p", "x_pos_2sqrt_q", "x_neg_2sqrt_q")


def audit_rank_zero_aa_bb_dyadic_target_matrix(
    pattern_types: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if (
        pattern_types.get("status") != "ok"
        or pattern_types.get("ready") is not True
        or int(pattern_types.get("pattern_type_count", 0) or 0) != 5
    ):
        violations.append("pattern_types_not_ready")

    type_rows = list(pattern_types.get("type_rows", []))
    matrix_rows: list[dict[str, Any]] = []
    all_support_signatures: dict[str, int] = defaultdict(int)

    for row in type_rows:
        rep = dict(row.get("representative", {}))
        type_id = str(row.get("type_id", ""))
        supports = {}
        for kernel in KERNELS:
            support = sorted({str(rep.get(kernel, ""))})
            if type_id == "minus_one_pair":
                support = ["-1", "1"]
            elif type_id == "two_pair":
                support = ["1", "2"]
            elif type_id == "minus_two_pair":
                support = ["-2", "1"]
            elif type_id == "fully_mixed_nontrivial":
                support = ["-1", "-2", "2"]
            supports[kernel] = support
            all_support_signatures[f"{kernel}:{','.join(support)}"] += 1
        matrix_rows.append(
            {
                "type_id": type_id,
                "pattern_count": int(row.get("pattern_count", 0) or 0),
                "kernel_supports": supports,
                "dyadic_filter_hint": {
                    "all_trivial": (
                        "To kill this type, some kernel must exclude class 1."
                    ),
                    "minus_one_pair": (
                        "To kill this type by one kernel alone, that kernel must "
                        "exclude both 1 and -1 from its dyadic image."
                    ),
                    "two_pair": (
                        "To kill this type by one kernel alone, that kernel must "
                        "exclude both 1 and 2 from its dyadic image."
                    ),
                    "minus_two_pair": (
                        "To kill this type by one kernel alone, that kernel must "
                        "exclude both 1 and -2 from its dyadic image."
                    ),
                    "fully_mixed_nontrivial": (
                        "To kill this type by one kernel alone, that kernel must "
                        "exclude all three classes {-1,2,-2}, or else use "
                        "cross-kernel compatibility."
                    ),
                }[type_id],
            }
        )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "pattern_type_count": len(matrix_rows),
        "kernel_count": len(KERNELS),
        "dyadic_target_matrix_rows": matrix_rows,
        "next_target": (
            "Prove kernel-specific dyadic image restrictions strong enough to cut "
            "the listed support sets, or combine weaker dyadic images with "
            "cross-kernel/Selmer compatibility."
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern-types", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_dyadic_target_matrix(load_json(args.pattern_types))
    write_json(args.out, audit)
    print(
        "wrote closure quotient rank-zero AA+BB dyadic target matrix to "
        f"{args.out}"
    )
    print(f"status={audit['status']}")
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
