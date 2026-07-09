#!/usr/bin/env python3
"""Audit the next singleton dyadic target for AA+BB rank-zero closure."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This chooses a minimal AA+BB dyadic theorem target from the "
    "trivial-retaining support shapes. The target is singleton only after "
    "intersecting the dyadic image with the rational 2-primary subgroup "
    "{1,-1,2,-2}; it does not claim a full Q2*/Q2*2 singleton image. It does "
    "not prove any dyadic local image, Selmer lift, Selmer rank bound, rank "
    "zero, or lambda-family exclusion."
)

KERNEL_ORDER = ("x_minus_p", "x_neg_2sqrt_q", "x_pos_2sqrt_q")
ODD_SUPPORT_STATUS = {
    "x_minus_p": "empty after AA+BB odd-support collapse",
    "x_neg_2sqrt_q": "empty after AA+BB odd-support collapse",
    "x_pos_2sqrt_q": "possible tail at odd primes ell | T, ell == 1 mod 4",
}
KERNEL_TO_PACKAGE = {
    "x_minus_p": "rank-zero-selmer-AA-BB-kernel-minus-p",
    "x_neg_2sqrt_q": "rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q",
    "x_pos_2sqrt_q": "rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q",
}


def _singleton_count(shape: dict[str, Any]) -> int:
    return sum(
        1
        for support in shape.get("unordered_allowed_supports", [])
        if list(support) == ["1"]
    )


def _has_singleton(shape: dict[str, Any]) -> bool:
    return _singleton_count(shape) > 0


def audit_rank_zero_aa_bb_dyadic_singleton_target(
    pair_profiles: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if (
        pair_profiles.get("status") != "ok"
        or pair_profiles.get("ready") is not True
        or pair_profiles.get("trivial_pattern_retained") is not True
    ):
        violations.append("pair_profiles_not_ready")

    shapes = list(pair_profiles.get("trivial_retaining_support_shape_rows", []))
    if int(pair_profiles.get("trivial_retaining_support_shape_count", 0) or 0) != 4:
        violations.append("trivial_retaining_support_shape_count_not_four")
    if not shapes or not all(_has_singleton(shape) for shape in shapes):
        violations.append("not_every_shape_forces_singleton_kernel")

    singleton_shape_count = sum(1 for shape in shapes if _has_singleton(shape))
    two_singleton_shape_count = sum(
        1 for shape in shapes if _singleton_count(shape) >= 2
    )
    odd_collapsed_kernels = [
        kernel for kernel in KERNEL_ORDER if ODD_SUPPORT_STATUS[kernel].startswith("empty")
    ]
    primary_target_kernel = odd_collapsed_kernels[0]
    alternate_target_kernels = odd_collapsed_kernels[1:]

    target_rows = [
        {
            "kernel": kernel,
            "package_id": KERNEL_TO_PACKAGE[kernel],
            "odd_support_status": ODD_SUPPORT_STATUS[kernel],
            "priority": (
                "primary"
                if kernel == primary_target_kernel
                else "alternate"
                if kernel in alternate_target_kernels
                else "defer"
            ),
        }
        for kernel in KERNEL_ORDER
    ]

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "trivial_pattern_retained": pair_profiles.get("trivial_pattern_retained") is True,
        "nontrivial_pattern_count": int(pair_profiles.get("nontrivial_pattern_count", 0) or 0),
        "support_shape_count": len(shapes),
        "support_shape_forcing_singleton_count": singleton_shape_count,
        "support_shape_with_two_singletons_count": two_singleton_shape_count,
        "odd_collapsed_singleton_candidate_count": len(odd_collapsed_kernels),
        "primary_target_kernel": primary_target_kernel,
        "primary_target_package": KERNEL_TO_PACKAGE[primary_target_kernel],
        "alternate_target_kernels": alternate_target_kernels,
        "deferred_kernel": "x_pos_2sqrt_q",
        "relevant_squareclass_subgroup": ["1", "-1", "2", "-2"],
        "target_is_full_q2_singleton_claim": False,
        "target_intersection_squareclasses": ["1"],
        "target_rows": target_rows,
        "next_theorem_target": (
            "Prove a dyadic local-image theorem showing that the AA+BB "
            "x_minus_p image intersects the rational 2-primary subgroup "
            "{1,-1,2,-2} only in {1}; then use the remaining support-shape "
            "and common-source/Selmer compatibility analysis to attack the "
            "15 nontrivial 2-primary patterns."
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair-profiles", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_dyadic_singleton_target(
        load_json(args.pair_profiles)
    )
    write_json(args.out, audit)
    print(
        "wrote closure quotient rank-zero AA+BB dyadic singleton target to "
        f"{args.out}"
    )
    print(f"status={audit['status']}")
    print(f"primary_target_kernel={audit['primary_target_kernel']}")
    print(f"support_shape_forcing_singleton_count={audit['support_shape_forcing_singleton_count']}")
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
