#!/usr/bin/env python3
"""Solve the AA+BB D2c pure odd-sqrt_q collision row in complete d-coordinates."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl477 / D2c_odd_sqrt_q_collision_row for the AA+BB "
    "complete d-coordinate route. It solves the pure odd ell|sqrt_q local "
    "C_d row where ell does not divide L*T, records overlaps with ell|L or "
    "ell|T as unsolved multi-collision obligations, references wl475 and "
    "wl476 only as the prior solved pure odd rows, and does not solve dyadic "
    "rows or overlaps, build a D4 matrix, prove a complete Sel_2(E) upper "
    "bound, claim dim Sel_2(E)=2, rank zero, Sha[2]=0, or any family "
    "exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

PURE_SQRT_Q_COLLISION_STRATUM = {
    "prime_condition": "ell odd and ell | sqrt_q",
    "excluded_overlaps": ["ell | L", "ell | T"],
    "root_difference_squareclasses": {
        "e_pos-e_neg": (
            "4*sqrt_q has positive ell-adic valuation m=v_ell(sqrt_q); "
            "m is not assumed even"
        ),
        "e_pos-e_minus": "16*L^2 is an ell-adic square unit",
        "e_minus-e_neg": "4*T^2 is an ell-adic square unit",
    },
    "pure_stratum_residue_constraint": (
        "sqrt_q=T^2+4*L^2 and ell does not divide L*T force -1 to be "
        "a square modulo ell"
    ),
    "normal_form": (
        "after translating by e_minus and scaling by a square unit, the "
        "third root is 0 and the two colliding roots are 1 and "
        "1+epsilon with v_ell(epsilon)=m>0"
    ),
}

SOLVED_LOCAL_ROW = {
    "id": "D2c_odd_sqrt_q_collision_row",
    "place_type": "ell|sqrt_q",
    "stratum": "pure_sqrt_q_collision",
    "applies_when": "ell odd, ell | sqrt_q, ell does not divide L*T",
    "coordinate_pair": ["d_pos_2sqrt_q", "d_neg_2sqrt_q"],
    "allowed_pair_rule": (
        "(d_pos_2sqrt_q,d_neg_2sqrt_q)=(lambda,lambda) for "
        "lambda in Q_ell*/Q_ell*2"
    ),
    "allowed_valuation_rule": (
        "v_ell(d_pos_2sqrt_q) == v_ell(d_neg_2sqrt_q) mod 2"
    ),
    "allowed_unit_squareclass_rule": (
        "unit(d_pos_2sqrt_q) == unit(d_neg_2sqrt_q) in F_ell*/F_ell*2"
    ),
    "allowed_pair_squareclasses": [
        "(1,1)",
        "(nu,nu)",
        "(ell,ell)",
        "(nu*ell,nu*ell)",
    ],
    "nu": "any fixed nonsquare unit in Q_ell",
    "d_minus_p_from_product_relation": "1 in Q_ell*/Q_ell*2",
    "row_dimension_over_F2_local_only": 2,
    "local_c_d_row_solved": True,
}

SQRT_Q_VALUATION_CASE_ANALYSIS = [
    {
        "case": "unit squareclasses",
        "realization": (
            "choose the node parameter z with v_ell(z)=0; then "
            "z and z-epsilon have the same prescribed unit squareclass"
        ),
    },
    {
        "case": "ramified squareclasses when m>=2",
        "realization": (
            "choose z with v_ell(z)=1<m; then z and z-epsilon have "
            "the same prescribed ramified squareclass"
        ),
    },
    {
        "case": "ramified squareclasses when m=1",
        "realization": (
            "the class of epsilon is realized by v_ell(z)>1, and the "
            "opposite ramified class is realized using a residue b with "
            "chi(b)=chi(b-1)=-1; such b exists because ell is odd and "
            "-1 is a square in the pure stratum"
        ),
    },
]

PROOF_SUMMARY = [
    (
        "In the pure stratum, both distances from e_minus to the two "
        "colliding roots are square units, so every integral node-local "
        "point has d_minus_p=1."
    ),
    (
        "After normalizing the third root to 0 and the colliding roots to "
        "1 and 1+epsilon, with v_ell(epsilon)=m>0, the reduction is the "
        "split nodal curve y^2=x*(x-1)^2."
    ),
    (
        "The local equation near the node is z*(z-epsilon) square. This "
        "forces d_pos_2sqrt_q and d_neg_2sqrt_q to have the same "
        "squareclass, hence d_minus_p=1 by the product relation."
    ),
    (
        "All four diagonal squareclasses are realized. Unit classes use "
        "v_ell(z)=0; ramified classes use v_ell(z)=1 when m>=2, while "
        "the m=1 case uses the pure-stratum fact that -1 is a residue to "
        "realize both ramified unit residues."
    ),
]

MULTI_COLLISION_OBLIGATIONS = [
    {
        "condition": "ell | sqrt_q and ell | L",
        "reason": "e_pos-e_minus=16*L^2 is no longer an ell-adic unit",
        "status": "multi_collision_obligation_not_solved_here",
    },
    {
        "condition": "ell | sqrt_q and ell | T",
        "reason": "e_minus-e_neg=4*T^2 is no longer an ell-adic unit",
        "status": "multi_collision_obligation_not_solved_here",
    },
]

REMAINING_D2_OBLIGATIONS = [
    "D2d_dyadic_complete_row",
    "D2_multi_collision_overlaps",
]


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _has_complete_d_container(d0_container: dict[str, Any]) -> bool:
    container = d0_container.get("complete_d_container", {})
    return (
        d0_container.get("lemma_id") == "D0_complete_d_container_definition"
        and d0_container.get("d0_status") == "framed_definition"
        and container.get("name") == "D0_complete_d_prelocal_container"
        and container.get("coordinate_tuple_order") == COORDINATE_ORDER
        and container.get("local_c_d_rows_built") is False
        and container.get("package_x_coordinates_used") is False
    )


def _has_product_relation(payload: dict[str, Any]) -> bool:
    container_relation = str(
        payload.get("complete_d_container", {}).get("defining_relation", "")
    )
    frame_relation = str(
        payload.get("complete_d_coordinate_frame", {}).get("product_relation", "")
    )
    return (
        "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1" in container_relation
        or "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1" in frame_relation
    )


def _d1_is_exact_support(d1_support: dict[str, Any]) -> bool:
    support = d1_support.get("candidate_support", {})
    return (
        d1_support.get("lemma_id") == "D1_relevant_place_support_confinement"
        and d1_support.get("d1_status") == "framed_and_proved_support_confinement"
        and support.get("equivalent_finite_set")
        == "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}"
        and d1_support.get("support_only_not_row_classification") is True
        and d1_support.get("local_c_d_rows_built") is False
    )


def _d2_rows_framed(d2_rows: dict[str, Any]) -> bool:
    frame = d2_rows.get("complete_d_coordinate_frame", {})
    return (
        d2_rows.get("lemma_id") == "D2_local_C_d_row_characterization"
        and d2_rows.get("d2_status") == "row_obligations_framed"
        and d2_rows.get("row_obligations_framed") is True
        and d2_rows.get("local_c_d_rows_solved") is False
        and d2_rows.get("local_c_d_rows_built") is False
        and d2_rows.get("full_c_d_matrix_built") is False
        and frame.get("coordinate_order") == COORDINATE_ORDER
        and frame.get("package_x_coordinates_used") is False
        and _has_product_relation(d2_rows)
    )


def _has_d2c_obligation(d2_rows: dict[str, Any]) -> bool:
    return any(
        row.get("id") == "D2c_odd_sqrt_q_collision_row"
        and row.get("place_type") == "ell|sqrt_q"
        for row in d2_rows.get("local_row_obligations", [])
    )


def _d3_baseline_recorded_without_matrix(d3_baseline: dict[str, Any]) -> bool:
    contract = d3_baseline.get("baseline_comparison_contract", {})
    return (
        d3_baseline.get("lemma_id") == "D3_torsion_baseline_in_d_coordinates"
        and d3_baseline.get("d3_status")
        == "torsion_baseline_recorded_in_complete_d_coordinates"
        and d3_baseline.get("local_c_d_rows_solved") is False
        and d3_baseline.get("local_c_d_rows_built") is False
        and d3_baseline.get("full_c_d_matrix_built") is False
        and contract.get("comparison_status")
        == "pending_until_local_c_d_rows_are_solved"
        and contract.get("quotient_baseline_here") is False
    )


def _d2a_solved_without_advancing(d2a_row: dict[str, Any]) -> bool:
    return (
        d2a_row.get("lemma_id") == "D2a_odd_L_collision_row"
        and d2a_row.get("d2a_status") == "pure_L_collision_row_solved"
        and d2a_row.get("local_c_d_rows_partially_solved") is True
        and d2a_row.get("local_c_d_rows_solved") is False
        and d2a_row.get("full_c_d_matrix_built") is False
        and d2a_row.get("complete_selmer_upper_bound_proved") is False
        and d2a_row.get("dim_sel2_eq_2_claimed") is False
        and d2a_row.get("rank_zero_claimed") is False
        and d2a_row.get("sha2_trivial_claimed") is False
        and d2a_row.get("family_exclusion_proved_count") == 0
    )


def _d2b_solved_without_advancing(d2b_row: dict[str, Any]) -> bool:
    return (
        d2b_row.get("lemma_id") == "D2b_odd_T_collision_row"
        and d2b_row.get("d2b_status") == "pure_T_collision_row_solved"
        and d2b_row.get("local_c_d_rows_partially_solved") is True
        and d2b_row.get("local_c_d_rows_solved") is False
        and d2b_row.get("full_c_d_matrix_built") is False
        and d2b_row.get("complete_selmer_upper_bound_proved") is False
        and d2b_row.get("dim_sel2_eq_2_claimed") is False
        and d2b_row.get("rank_zero_claimed") is False
        and d2b_row.get("sha2_trivial_claimed") is False
        and d2b_row.get("family_exclusion_proved_count") == 0
    )


def audit_rank_zero_aa_bb_d2c_odd_sqrt_q_collision_row(
    *,
    d0_container: dict[str, Any],
    d1_support: dict[str, Any],
    d2_rows: dict[str, Any],
    d3_baseline: dict[str, Any],
    d2a_row: dict[str, Any],
    d2b_row: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(d0_container):
        violations.append("d0_container_not_ready")
    if not _has_complete_d_container(d0_container):
        violations.append("d0_complete_d_container_missing")
    if not _has_product_relation(d0_container):
        violations.append("d0_product_relation_missing")
    if not _ready(d1_support):
        violations.append("d1_support_not_ready")
    if not _d1_is_exact_support(d1_support):
        if d1_support.get("local_c_d_rows_built") is True:
            violations.append("d1_already_built_local_rows")
        else:
            violations.append("d1_support_not_exact_S_D1")
    if not _ready(d2_rows):
        violations.append("d2_rows_not_ready")
    if not _d2_rows_framed(d2_rows):
        if d2_rows.get("local_c_d_rows_solved") is True:
            violations.append("d2_already_solved_all_local_rows")
        if d2_rows.get("full_c_d_matrix_built") is True:
            violations.append("d2_already_built_full_matrix")
        if (
            d2_rows.get("local_c_d_rows_solved") is not True
            and d2_rows.get("full_c_d_matrix_built") is not True
        ):
            violations.append("d2_rows_not_framed")
    if not _has_d2c_obligation(d2_rows):
        violations.append("d2c_obligation_missing")
    if not _ready(d3_baseline):
        violations.append("d3_baseline_not_ready")
    if not _d3_baseline_recorded_without_matrix(d3_baseline):
        if d3_baseline.get("full_c_d_matrix_built") is True:
            violations.append("d3_already_built_full_matrix")
        else:
            violations.append("d3_baseline_not_recorded_without_matrix")
    if not _ready(d2a_row):
        violations.append("d2a_row_not_ready")
    if not _d2a_solved_without_advancing(d2a_row):
        if d2a_row.get("full_c_d_matrix_built") is True:
            violations.append("d2a_already_built_full_matrix")
        elif d2a_row.get("complete_selmer_upper_bound_proved") is True:
            violations.append("d2a_already_claims_selmer_bound")
        else:
            violations.append("d2a_row_not_scoped_pure_L_solution")
    if not _ready(d2b_row):
        violations.append("d2b_row_not_ready")
    if not _d2b_solved_without_advancing(d2b_row):
        if d2b_row.get("full_c_d_matrix_built") is True:
            violations.append("d2b_already_built_full_matrix")
        elif d2b_row.get("complete_selmer_upper_bound_proved") is True:
            violations.append("d2b_already_claims_selmer_bound")
        else:
            violations.append("d2b_row_not_scoped_pure_T_solution")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl471-wl476",
        "pattern": "AA+BB",
        "lemma_id": "D2c_odd_sqrt_q_collision_row",
        "d2c_status": "pure_sqrt_q_collision_row_solved",
        "complete_d_coordinate_order": COORDINATE_ORDER,
        "d0_container_used": "D0_complete_d_prelocal_container",
        "d1_support_used": "S_D1={infinity,2} union {odd ell: ell | L*T*sqrt_q}",
        "d2_obligation_used": "D2c_odd_sqrt_q_collision_row",
        "d3_baseline_used_as_boundary_only": True,
        "wl475_referenced_only": True,
        "wl476_referenced_only": True,
        "pure_sqrt_q_collision_stratum": PURE_SQRT_Q_COLLISION_STRATUM,
        "solved_local_row": SOLVED_LOCAL_ROW,
        "sqrt_q_valuation_case_analysis": SQRT_Q_VALUATION_CASE_ANALYSIS,
        "proof_summary": PROOF_SUMMARY,
        "multi_collision_obligations": MULTI_COLLISION_OBLIGATIONS,
        "row_depends_on_v_ell_sqrt_q_parity": False,
        "row_depends_on_sqrt_q_unit_residue": False,
        "row_obstruction_remaining": False,
        "overlap_cases_solved_here": False,
        "local_c_d_rows_partially_solved": True,
        "local_c_d_rows_solved": False,
        "solved_row_ids": [
            "D2a_odd_L_collision_row",
            "D2b_odd_T_collision_row",
            "D2c_odd_sqrt_q_collision_row",
        ],
        "remaining_d2_obligations": REMAINING_D2_OBLIGATIONS,
        "full_c_d_matrix_built": False,
        "d4_entered": False,
        "old_package_x_coordinate_collapse_used": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "family_exclusion_proved_count": 0,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "search_count_used_as_progress": False,
        "next_lemma": "remaining_D2_local_C_d_rows_not_started_here",
        "do_not_proceed_to": [
            "D4_AA_BB_uniform_matrix_rank_bound",
            "complete_selmer_upper_bound_claim",
        ],
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--d0-container", type=Path, required=True)
    parser.add_argument("--d1-support", type=Path, required=True)
    parser.add_argument("--d2-rows", type=Path, required=True)
    parser.add_argument("--d3-baseline", type=Path, required=True)
    parser.add_argument("--d2a-row", type=Path, required=True)
    parser.add_argument("--d2b-row", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_d2c_odd_sqrt_q_collision_row(
        d0_container=load_json(args.d0_container),
        d1_support=load_json(args.d1_support),
        d2_rows=load_json(args.d2_rows),
        d3_baseline=load_json(args.d3_baseline),
        d2a_row=load_json(args.d2a_row),
        d2b_row=load_json(args.d2b_row),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB D2c odd-sqrt_q collision-row audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"d2c_status={audit['d2c_status']}")
    print(f"local_c_d_rows_solved={audit['local_c_d_rows_solved']}")
    print(f"full_c_d_matrix_built={audit['full_c_d_matrix_built']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
