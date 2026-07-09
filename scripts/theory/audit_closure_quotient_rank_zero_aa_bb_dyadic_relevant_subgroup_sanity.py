#!/usr/bin/env python3
"""Finite sanity check for the AA+BB x_minus_p dyadic subgroup target."""

from __future__ import annotations

import argparse
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json

BOUNDARY = (
    "This is a finite 2-adic sanity check for the AA+BB x_minus_p target. "
    "It is not a proof of the dyadic local image, a Selmer lift, a Selmer "
    "rank bound, rank zero, or any lambda-family exclusion."
)

RELEVANT_SUBGROUP = ["1", "-1", "2", "-2"]
FULL_Q2_COUNTEREXAMPLE_MESSAGE = (
    "full Q2 local image can contain a class outside {1,-1,2,-2}; the theorem "
    "target must stay subgroup-relative"
)


def _v2_int(value: int) -> int:
    if value == 0:
        raise ValueError("v2 is undefined at zero")
    value = abs(value)
    exponent = 0
    while value % 2 == 0:
        exponent += 1
        value //= 2
    return exponent


def _v2(value: Fraction) -> int:
    return _v2_int(value.numerator) - _v2_int(value.denominator)


def _odd_unit_mod8(value: Fraction) -> int:
    exponent = _v2(value)
    numerator = value.numerator
    denominator = value.denominator
    if exponent >= 0:
        numerator //= 2**exponent
    else:
        denominator //= 2 ** (-exponent)
    return (numerator % 8) * pow(denominator % 8, -1, 8) % 8


def q2_squareclass(value: int | Fraction) -> str:
    value = Fraction(value)
    if value == 0:
        return "0"
    parity = _v2(value) % 2
    unit = _odd_unit_mod8(value)
    if parity == 0:
        return {1: "1", 3: "3", 5: "5", 7: "-1"}[unit]
    return {1: "2", 3: "6", 5: "10", 7: "-2"}[unit]


def _is_q2_square(value: Fraction) -> bool:
    if value == 0:
        return True
    return _v2(value) % 2 == 0 and _odd_unit_mod8(value) == 1


def _x_minus_p_rhs(x: Fraction, *, l_value: int, t_value: int) -> Fraction:
    return (
        x**3
        + (32 * l_value * l_value - 8 * t_value * t_value) * x * x
        + 16 * (t_value * t_value + 4 * l_value * l_value) ** 2 * x
    )


def _local_classes(
    *,
    a_value: int,
    b_value: int,
    l_value: int,
    numerator_bound: int,
    denominator_exp_bound: int,
) -> set[str]:
    t_value = a_value + b_value
    classes: set[str] = set()
    for numerator in range(-numerator_bound, numerator_bound + 1):
        if numerator == 0:
            continue
        for denominator_exp in range(denominator_exp_bound + 1):
            x_value = Fraction(numerator, 2**denominator_exp)
            if _is_q2_square(
                _x_minus_p_rhs(x_value, l_value=l_value, t_value=t_value)
            ):
                classes.add(q2_squareclass(x_value))
    return classes


def _parse_pair(raw: str) -> tuple[int, int]:
    left, right = raw.split(":", maxsplit=1)
    pair = (int(left), int(right))
    if pair[0] <= 0 or pair[1] <= 0 or gcd(*pair) != 1:
        raise argparse.ArgumentTypeError("sample pairs must be positive primitive A:B")
    return pair


def audit_rank_zero_aa_bb_dyadic_relevant_subgroup_sanity(
    *,
    sample_pairs: list[tuple[int, int]],
    numerator_bound: int,
    denominator_exp_bound: int,
) -> dict[str, Any]:
    observed: dict[str, list[str]] = {}
    full_counterexample: dict[str, str] | None = None
    relevant = set(RELEVANT_SUBGROUP)
    for a_value, b_value in sample_pairs:
        aa_classes = _local_classes(
            a_value=a_value,
            b_value=b_value,
            l_value=a_value,
            numerator_bound=numerator_bound,
            denominator_exp_bound=denominator_exp_bound,
        )
        bb_classes = _local_classes(
            a_value=a_value,
            b_value=b_value,
            l_value=b_value,
            numerator_bound=numerator_bound,
            denominator_exp_bound=denominator_exp_bound,
        )
        intersection = aa_classes & bb_classes
        relevant_intersection = sorted(intersection & relevant, key=RELEVANT_SUBGROUP.index)
        pair_id = f"{a_value}:{b_value}"
        observed[pair_id] = relevant_intersection
        if full_counterexample is None:
            outside_relevant = sorted(intersection - relevant)
            if outside_relevant:
                full_counterexample = {
                    "pair": pair_id,
                    "class": outside_relevant[0],
                    "meaning": FULL_Q2_COUNTEREXAMPLE_MESSAGE,
                }

    target_intersection = sorted(
        set.intersection(*(set(classes) for classes in observed.values())),
        key=RELEVANT_SUBGROUP.index,
    )
    violations: list[str] = []
    if target_intersection != ["1"]:
        violations.append("observed_relevant_intersection_not_singleton")
    if full_counterexample is None:
        violations.append("full_q2_boundary_counterexample_missing")
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "sample_pair_count": len(sample_pairs),
        "numerator_bound": numerator_bound,
        "denominator_exp_bound": denominator_exp_bound,
        "relevant_squareclass_subgroup": RELEVANT_SUBGROUP,
        "observed_relevant_intersection_by_pair": observed,
        "target_intersection_squareclasses": target_intersection,
        "full_q2_singleton_counterexample": full_counterexample,
        "finite_sanity_check_not_proof": True,
        "dyadic_local_image_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sample-pair",
        action="append",
        type=_parse_pair,
        default=[],
        help="primitive A:B pair to use for the finite sanity check",
    )
    parser.add_argument("--numerator-bound", type=int, default=64)
    parser.add_argument("--denominator-exp-bound", type=int, default=6)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sample_pairs = args.sample_pair or [(1, 2), (1, 4), (3, 5), (5, 7)]
    audit = audit_rank_zero_aa_bb_dyadic_relevant_subgroup_sanity(
        sample_pairs=sample_pairs,
        numerator_bound=args.numerator_bound,
        denominator_exp_bound=args.denominator_exp_bound,
    )
    write_json(args.out, audit)
    print(
        "wrote closure quotient rank-zero AA+BB dyadic relevant subgroup "
        f"sanity audit to {args.out}"
    )
    print(f"status={audit['status']}")
    print(f"target_intersection_squareclasses={audit['target_intersection_squareclasses']}")
    print(f"dyadic_local_image_proved_count={audit['dyadic_local_image_proved_count']}")
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
