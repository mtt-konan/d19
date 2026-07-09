#!/usr/bin/env python3
"""Audit the AA+BB rank-zero reduction to a 2-primary Selmer gap."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits the conditional AA+BB reduction from an odd-prime Selmer gap "
    "to a 2-primary Selmer gap. It does not prove that Selmer candidates come "
    "from common source points, does not prove a Selmer rank bound, does not "
    "prove rank zero, and does not prove any lambda-family exclusion."
)

POINT_LEVEL_COLLAPSE = {
    "source": "wl460-wl463",
    "scope": "genuine AA+BB common-source rational points",
    "remaining_triples": [
        {
            "x_minus_p": "1",
            "x_pos_2sqrt_q": "1",
            "x_neg_2sqrt_q": "1",
        }
    ],
    "nontrivial_triple_count": 0,
    "selmer_lift_proved": False,
}


def _aa_bb_group(family_obligations: dict[str, Any]) -> dict[str, Any] | None:
    for group in family_obligations.get("groups", []):
        if str(group.get("pattern", "")) == "AA+BB":
            return dict(group)
    return None


def audit_rank_zero_aa_bb_two_primary_reduction(
    *,
    family_obligations: dict[str, Any],
    product_relation: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []

    if family_obligations.get("status") != "ok" or family_obligations.get("ready") is not True:
        violations.append("family_obligations_not_ready")
    if product_relation.get("status") != "ok" or product_relation.get("ready") is not True:
        violations.append("product_relation_not_ready")

    aa_bb = _aa_bb_group(family_obligations)
    if aa_bb is None:
        violations.append("aa_bb_group_missing")
        aa_bb = {
            "candidate_class_count": 0,
            "model_count": 0,
            "model_counts_by_curve": {},
            "pattern": "AA+BB",
        }

    relation = str(product_relation.get("common_source_relation", ""))
    if "x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q" not in relation:
        violations.append("common_source_relation_missing")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "pattern": "AA+BB",
        "candidate_class_count": int(aa_bb.get("candidate_class_count", 0) or 0),
        "model_count": int(aa_bb.get("model_count", 0) or 0),
        "model_counts_by_curve": dict(aa_bb.get("model_counts_by_curve", {})),
        "common_source_product_relation_available": status == "ok",
        "odd_prime_support_for_actual_points_trivial": status == "ok",
        "remaining_gap_kind": "Selmer-layer lift of point-level collapse",
        "remaining_gap_components": [
            "lift common-source compatibility to the Selmer layer",
            "dyadic local condition",
            "unit/sign classes",
        ],
        "point_level_two_primary_collapse": POINT_LEVEL_COLLAPSE,
        "next_theorem_target": (
            "Prove the AA+BB Selmer-layer lift: every relevant Selmer candidate "
            "satisfies the common-source two-primary compatibility whose "
            "point-level collapse leaves only (1,1,1)."
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family-obligations", type=Path, required=True)
    parser.add_argument("--product-relation", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_two_primary_reduction(
        family_obligations=load_json(args.family_obligations),
        product_relation=load_json(args.product_relation),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero AA+BB two-primary reduction to {args.out}")
    print(f"status={audit['status']}")
    print(f"candidate_class_count={audit['candidate_class_count']}")
    print(
        "odd_prime_support_for_actual_points_trivial="
        f"{audit['odd_prime_support_for_actual_points_trivial']}"
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
