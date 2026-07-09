#!/usr/bin/env python3
"""Finite residue-class sanity check for the AA+BB x_minus_p dyadic target."""

from __future__ import annotations

import argparse
import sys
from math import gcd
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_dyadic_relevant_subgroup_sanity import (  # noqa: E402
    FULL_Q2_COUNTEREXAMPLE_MESSAGE,
    RELEVANT_SUBGROUP,
    _local_classes,
)

BOUNDARY = (
    "This is a finite residue-class sanity check for the AA+BB x_minus_p "
    "subgroup target. It is not a proof of the dyadic local image, a Selmer "
    "lift, a Selmer rank bound, rank zero, or any lambda-family exclusion."
)


def _parity_bucket(a_value: int, b_value: int) -> str:
    a_parity = "odd" if a_value % 2 else "even"
    b_parity = "odd" if b_value % 2 else "even"
    return f"{a_parity}-{b_parity}"


def _canonical_representative(
    a_residue: int,
    b_residue: int,
    *,
    modulus: int,
    search_bound: int,
) -> tuple[int, int]:
    for a_value in range(1, search_bound + 1):
        if a_value % modulus != a_residue:
            continue
        for b_value in range(1, search_bound + 1):
            if b_value % modulus != b_residue:
                continue
            if gcd(a_value, b_value) == 1:
                return a_value, b_value
    raise ValueError(
        f"no primitive representative found for residues {(a_residue, b_residue)}"
    )


def audit_rank_zero_aa_bb_dyadic_residue_class_sanity(
    *,
    modulus: int,
    numerator_bound: int,
    denominator_exp_bound: int,
    representative_search_bound: int,
) -> dict[str, Any]:
    relevant = set(RELEVANT_SUBGROUP)
    rows: list[dict[str, Any]] = []
    parity_bucket_counts = {"odd-even": 0, "even-odd": 0, "odd-odd": 0}
    target_intersection: set[str] | None = None
    full_q2_counterexample_residue_class_count = 0
    nontrivial_relevant_residue_class_count = 0
    nontrivial_relevant_by_bucket = {"odd-even": 0, "even-odd": 0, "odd-odd": 0}

    for a_residue in range(modulus):
        for b_residue in range(modulus):
            if a_residue % 2 == 0 and b_residue % 2 == 0:
                continue
            a_value, b_value = _canonical_representative(
                a_residue,
                b_residue,
                modulus=modulus,
                search_bound=representative_search_bound,
            )
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
            relevant_intersection = [
                cls for cls in RELEVANT_SUBGROUP if cls in intersection
            ]
            if target_intersection is None:
                target_intersection = set(relevant_intersection)
            else:
                target_intersection &= set(relevant_intersection)
            outside_relevant = sorted(intersection - relevant)
            bucket = _parity_bucket(a_residue, b_residue)
            if outside_relevant:
                full_q2_counterexample_residue_class_count += 1
            if set(relevant_intersection) != {"1"}:
                nontrivial_relevant_residue_class_count += 1
                nontrivial_relevant_by_bucket[bucket] += 1
            parity_bucket_counts[bucket] += 1
            rows.append(
                {
                    "residue_class": f"{a_residue}:{b_residue} mod {modulus}",
                    "representative_pair": f"{a_value}:{b_value}",
                    "parity_bucket": bucket,
                    "observed_relevant_intersection": relevant_intersection,
                    "observed_full_q2_classes_outside_relevant_subgroup": outside_relevant,
                }
            )

    rows.sort(key=lambda row: row["residue_class"])
    target_intersection_list = [
        cls for cls in RELEVANT_SUBGROUP if cls in (target_intersection or set())
    ]
    violations: list[str] = []
    if target_intersection_list != ["1"]:
        violations.append("residue_class_target_intersection_not_singleton")
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "residue_modulus": modulus,
        "primitive_residue_class_count": len(rows),
        "representative_search_bound": representative_search_bound,
        "numerator_bound": numerator_bound,
        "denominator_exp_bound": denominator_exp_bound,
        "relevant_squareclass_subgroup": RELEVANT_SUBGROUP,
        "target_intersection_squareclasses": target_intersection_list,
        "nontrivial_relevant_residue_class_count": nontrivial_relevant_residue_class_count,
        "nontrivial_relevant_by_bucket": nontrivial_relevant_by_bucket,
        "full_q2_counterexample_residue_class_count": (
            full_q2_counterexample_residue_class_count
        ),
        "full_q2_counterexample_meaning": FULL_Q2_COUNTEREXAMPLE_MESSAGE,
        "parity_bucket_counts": parity_bucket_counts,
        "sample_rows": rows,
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
    parser.add_argument("--modulus", type=int, default=8)
    parser.add_argument("--numerator-bound", type=int, default=32)
    parser.add_argument("--denominator-exp-bound", type=int, default=5)
    parser.add_argument("--representative-search-bound", type=int, default=64)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_dyadic_residue_class_sanity(
        modulus=args.modulus,
        numerator_bound=args.numerator_bound,
        denominator_exp_bound=args.denominator_exp_bound,
        representative_search_bound=args.representative_search_bound,
    )
    write_json(args.out, audit)
    print(
        "wrote closure quotient rank-zero AA+BB dyadic residue-class sanity "
        f"audit to {args.out}"
    )
    print(f"status={audit['status']}")
    print(f"primitive_residue_class_count={audit['primitive_residue_class_count']}")
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
