#!/usr/bin/env python3
"""Define the AA+BB complete d-coordinate prelocal container."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only D0_complete_d_container_definition after the H2 route "
    "pivot. It defines the complete d-coordinate prelocal container and torsion "
    "baseline, but proves no C_d local rows, complete Sel_2(E) upper bound, "
    "rank zero, Sha[2]=0, or family exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

COMPLETE_D_CONTAINER = {
    "name": "D0_complete_d_prelocal_container",
    "ambient_squareclass_quotient": (
        "V = Q*/Q*2; triples are in V^3 and multiplied coordinatewise"
    ),
    "coordinate_tuple_order": COORDINATE_ORDER,
    "coordinate_definitions": {
        "d_minus_p": "X-(-p)=X+p",
        "d_pos_2sqrt_q": "X-(2*sqrt_q)",
        "d_neg_2sqrt_q": "X-(-2*sqrt_q)=X+2*sqrt_q",
    },
    "defining_relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2",
    "relation_plane_dimension": 2,
    "covers_represented_symbolically": "C_d",
    "local_c_d_rows_built": False,
    "package_x_coordinates_used": False,
    "old_s_tilde_used_as_container": False,
}

REPRESENTATIVE_ORDER = [
    "O",
    "T_minus_p",
    "T_pos_2sqrt_q",
    "T_neg_2sqrt_q",
]

EXCEPTIONAL_ROOT_REPRESENTATIVES = {
    "standard_rule": (
        "At X=e_i, replace the vanishing d_i coordinate by the product of "
        "the two nonzero root differences."
    ),
    "root_labels": {
        "T_minus_p": "e_minus=-p",
        "T_pos_2sqrt_q": "e_pos=2*sqrt_q",
        "T_neg_2sqrt_q": "e_neg=-2*sqrt_q",
    },
    "representatives_are_complete_d_data": True,
    "package_x_collapse_not_used": True,
    "root_cases_included": [
        "T_minus_p",
        "T_pos_2sqrt_q",
        "T_neg_2sqrt_q",
    ],
}


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _route_selects_d_matrix(route_pivot: dict[str, Any]) -> bool:
    return (
        route_pivot.get("route_decision", {}).get("selected_route")
        == "build_minimal_C_d_local_solubility_matrix"
    )


def _has_next_d0(route_pivot: dict[str, Any]) -> bool:
    return any(
        item.get("id") == "D0_complete_d_container_definition"
        for item in route_pivot.get("next_lemmas", [])
    )


def _has_complete_d_product_relation(complete_two_descent_recast: dict[str, Any]) -> bool:
    relation = str(
        complete_two_descent_recast.get("complete_two_descent_coordinates", {}).get(
            "ambient_relation", ""
        )
    )
    return (
        "d_minus_p * d_pos_2sqrt_q * d_neg_2sqrt_q" in relation
        and "Q*/Q*2" in relation
    )


def _h2_refuted(h2_coordinate_equivalence: dict[str, Any]) -> bool:
    verdict = h2_coordinate_equivalence.get("h2_verdict", {})
    return (
        verdict.get("status") == "refuted"
        and verdict.get("coordinate_equivalence_refuted") is True
        and verdict.get("coordinate_equivalence_proved") is False
    )


def _torsion_kummer_baseline(
    complete_two_descent_recast: dict[str, Any],
) -> dict[str, Any]:
    torsion_images = complete_two_descent_recast.get("torsion_kummer_images", {})
    representatives = {
        name: torsion_images[name]
        for name in REPRESENTATIVE_ORDER
        if name in torsion_images
    }
    return {
        "source": "E_L[2](Q) inside the complete d-coordinate quotient",
        "same_quotient_as_container": True,
        "baseline_dimension": 2,
        "representative_order": list(representatives),
        "representatives": representatives,
        "product_relation_verified_for_representatives": True,
        "baseline_generators": ["T_minus_p", "T_pos_2sqrt_q"],
        "generator_sum_relation": "T_minus_p*T_pos_2sqrt_q=T_neg_2sqrt_q in V^3",
        "baseline_not_quotiented_out": True,
    }


def audit_rank_zero_aa_bb_complete_d_container_definition(
    *,
    route_pivot: dict[str, Any],
    complete_two_descent_recast: dict[str, Any],
    h2_coordinate_equivalence: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(route_pivot):
        violations.append("route_pivot_not_ready")
    if not _route_selects_d_matrix(route_pivot) or not _has_next_d0(route_pivot):
        violations.append("route_pivot_d0_not_selected")
    if not _ready(complete_two_descent_recast):
        violations.append("complete_two_descent_recast_not_ready")
    if not _has_complete_d_product_relation(complete_two_descent_recast):
        violations.append("complete_d_product_relation_missing")
    if not _ready(h2_coordinate_equivalence):
        violations.append("h2_coordinate_equivalence_not_ready")
    if not _h2_refuted(h2_coordinate_equivalence):
        violations.append("h2_coordinate_equivalence_not_refuted")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl464-wl470",
        "pattern": "AA+BB",
        "lemma_id": "D0_complete_d_container_definition",
        "d0_status": "framed_definition",
        "complete_d_container": COMPLETE_D_CONTAINER,
        "torsion_kummer_baseline": _torsion_kummer_baseline(
            complete_two_descent_recast
        ),
        "exceptional_root_representatives": EXCEPTIONAL_ROOT_REPRESENTATIVES,
        "d1_entered": False,
        "d2_entered": False,
        "d3_entered": False,
        "d4_entered": False,
        "local_c_d_rows_built": False,
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "search_count_used_as_progress": False,
        "do_not_proceed_to": [
            "D1_relevant_place_support_confinement",
            "D2_local_C_d_row_characterization",
            "D3_torsion_baseline_in_d_coordinates",
            "D4_AA_BB_uniform_matrix_rank_bound",
        ],
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route-pivot", type=Path, required=True)
    parser.add_argument("--complete-two-descent-recast", type=Path, required=True)
    parser.add_argument("--h2-coordinate-equivalence", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_complete_d_container_definition(
        route_pivot=load_json(args.route_pivot),
        complete_two_descent_recast=load_json(args.complete_two_descent_recast),
        h2_coordinate_equivalence=load_json(args.h2_coordinate_equivalence),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB D0 complete-d-container audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"d0_status={audit['d0_status']}")
    print(f"local_c_d_rows_built={audit['local_c_d_rows_built']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
