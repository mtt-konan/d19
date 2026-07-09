#!/usr/bin/env python3
"""Audit finite 2-primary squareclass patterns for AA+BB common-source points."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits the finite 2-primary squareclass patterns forced for AA+BB "
    "common-source rational points. It does not prove a Selmer lift, a dyadic "
    "local condition, a Selmer rank bound, rank zero, or any lambda-family "
    "exclusion."
)

CLASS_TO_BITS = {
    "1": (0, 0),
    "-1": (1, 0),
    "2": (0, 1),
    "-2": (1, 1),
}

BITS_TO_CLASS = {bits: label for label, bits in CLASS_TO_BITS.items()}


def _multiply_classes(left: str, right: str) -> str:
    a0, a1 = CLASS_TO_BITS[left]
    b0, b1 = CLASS_TO_BITS[right]
    return BITS_TO_CLASS[((a0 + b0) % 2, (a1 + b1) % 2)]


def _pattern_rows() -> list[dict[str, str]]:
    labels = ["1", "-1", "2", "-2"]
    rows: list[dict[str, str]] = []
    for minus_p in labels:
        for pos in labels:
            neg = _multiply_classes(minus_p, pos)
            rows.append(
                {
                    "x_minus_p": minus_p,
                    "x_pos_2sqrt_q": pos,
                    "x_neg_2sqrt_q": neg,
                    "product_squareclass": "1",
                }
            )
    return rows


def audit_rank_zero_aa_bb_common_source_2primary_patterns(
    *,
    two_primary_reduction: dict[str, Any],
    product_relation: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []

    if (
        two_primary_reduction.get("status") != "ok"
        or two_primary_reduction.get("ready") is not True
        or two_primary_reduction.get("odd_prime_support_for_actual_points_trivial")
        is not True
    ):
        violations.append("two_primary_reduction_not_ready")

    if (
        product_relation.get("status") != "ok"
        or product_relation.get("ready") is not True
        or "x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q"
        not in str(product_relation.get("common_source_relation", ""))
    ):
        violations.append("product_relation_not_ready")

    status = "ok" if not violations else "issues"
    pattern_rows = _pattern_rows()
    return {
        "status": status,
        "ready": status == "ok",
        "pattern": "AA+BB",
        "candidate_class_count": int(
            two_primary_reduction.get("candidate_class_count", 0) or 0
        ),
        "q2_squareclass_universe_size": 8,
        "naive_q2_kernel_triple_pattern_count": 512,
        "common_source_squareclass_subgroup_generators": ["-1", "2"],
        "common_source_squareclass_subgroup_size": 4,
        "common_source_kernel_triple_pattern_count": len(pattern_rows),
        "common_source_pattern_rows": pattern_rows,
        "pattern_reduction_factor_vs_naive_q2_box": 32,
        "product_square_relation_retained": status == "ok",
        "pattern_description": (
            "Each kernel coordinate lies in the rational squareclass subgroup "
            "<-1,2> = {1,-1,2,-2}, and the product of the three classes is trivial."
        ),
        "remaining_filter_layer": "dyadic local image and Selmer-lift compatibility",
        "next_target": (
            "Rule out the finite 2-primary common-source patterns at the Selmer "
            "level for AA+BB."
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--two-primary-reduction", type=Path, required=True)
    parser.add_argument("--product-relation", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_common_source_2primary_patterns(
        two_primary_reduction=load_json(args.two_primary_reduction),
        product_relation=load_json(args.product_relation),
    )
    write_json(args.out, audit)
    print(
        "wrote closure quotient rank-zero AA+BB common-source 2-primary patterns "
        f"to {args.out}"
    )
    print(f"status={audit['status']}")
    print(f"candidate_class_count={audit['candidate_class_count']}")
    print(
        "common_source_kernel_triple_pattern_count="
        f"{audit['common_source_kernel_triple_pattern_count']}"
    )
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
