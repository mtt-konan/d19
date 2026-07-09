#!/usr/bin/env python3
"""Solve the AA+BB D2d dyadic complete row in complete d-coordinates."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl478 / D2d_dyadic_complete_row for the AA+BB "
    "complete d-coordinate route. It solves the Q_2 local C_d row from the "
    "three complete difference equations, separated by the necessary "
    "valuation strata of L,T,sqrt_q, records odd multi-collision overlaps as "
    "unsolved D2 obligations, references wl475-wl477 only as prior solved "
    "pure odd rows, and does not build a D4 matrix, prove a complete "
    "Sel_2(E) upper bound, claim dim Sel_2(E)=2, rank zero, Sha[2]=0, or "
    "any family exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

DYADIC_SQUARECLASS_LABELS = ["1", "-1", "2", "-2", "5", "-5", "10", "-10"]

DYADIC_STRATA = [
    {
        "id": "ordinary_even_sqrt_q_stratum",
        "condition": "v2(T) != v2(L)+1, equivalently v2(sqrt_q) is even",
        "subcases": [
            "v2(T) < v2(L)+1 gives v2(sqrt_q)=2*v2(T)",
            "v2(T) > v2(L)+1 gives v2(sqrt_q)=2*v2(L)+2",
        ],
        "odd_unit_residue_dependence": False,
    },
    {
        "id": "balanced_odd_sqrt_q_stratum",
        "condition": "v2(T) == v2(L)+1, equivalently v2(sqrt_q)=2*v2(T)+1",
        "subcases": [
            "write L=2^a*l and T=2^(a+1)*t with l,t odd",
            "then sqrt_q=2^(2*a+2)*(l^2+t^2) has odd valuation 2*a+3",
        ],
        "odd_unit_residue_dependence": False,
    },
]

SOLVED_LOCAL_ROWS = [
    {
        "stratum_id": "ordinary_even_sqrt_q_stratum",
        "allowed_triple_rule": (
            "d_minus_p in {1,-1,5,-5}, d_neg_2sqrt_q in {1,5}, "
            "and d_pos_2sqrt_q=d_minus_p*d_neg_2sqrt_q"
        ),
        "allowed_triples": [
            ["1", "1", "1"],
            ["1", "5", "5"],
            ["-1", "-1", "1"],
            ["-1", "-5", "5"],
            ["5", "5", "1"],
            ["5", "1", "5"],
            ["-5", "-5", "1"],
            ["-5", "-1", "5"],
        ],
        "row_dimension_over_F2_local_only": 3,
    },
    {
        "stratum_id": "balanced_odd_sqrt_q_stratum",
        "allowed_triple_rule": (
            "d_minus_p in {1,-1}, d_neg_2sqrt_q in {1,2,5,10}, "
            "and d_pos_2sqrt_q=d_minus_p*d_neg_2sqrt_q"
        ),
        "allowed_triples": [
            ["1", "1", "1"],
            ["1", "2", "2"],
            ["1", "5", "5"],
            ["1", "10", "10"],
            ["-1", "-1", "1"],
            ["-1", "-2", "2"],
            ["-1", "-5", "5"],
            ["-1", "-10", "10"],
        ],
        "row_dimension_over_F2_local_only": 3,
    },
]

COMPLETE_D_EQUATIONS = {
    "coordinate_order": COORDINATE_ORDER,
    "covering_equations": [
        "d_minus_p*u_minus_p^2 = X+p",
        "d_pos_2sqrt_q*u_pos_2sqrt_q^2 = X-2*sqrt_q",
        "d_neg_2sqrt_q*u_neg_2sqrt_q^2 = X+2*sqrt_q",
    ],
    "difference_equations": [
        "d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = 16*L^2",
        "d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*T^2",
        "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q",
    ],
    "one_parameter_form": (
        "with A=X+p, the three represented quantities are "
        "A, A-16*L^2, A+4*T^2"
    ),
    "product_relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q_2*/Q_2*2",
    "old_package_x_coordinates_used": False,
}

PROOF_SUMMARY = [
    (
        "Write L=2^a*l and T=2^b*t with l,t odd. In the complete "
        "d-coordinate equations, X is replaced by A=X+p, so the row is "
        "controlled by the Q_2 squareclasses of A, A-16*L^2, and A+4*T^2."
    ),
    (
        "If b is not a+1, the two dyadic root separations 16*L^2 and "
        "4*T^2 have distinct even valuations. A valuation partition for A "
        "then rules out every ramified coordinate and leaves exactly the "
        "ordinary row listed above."
    ),
    (
        "If b=a+1, divide the three equations by the square 2^(2*a+4). "
        "The normalized row is z, z-l^2, z+t^2 with l,t odd; the two "
        "nonzero finite roots are congruent to 1 and -1 modulo 8, and their "
        "separation has odd valuation. This is the only dyadic stratum where "
        "ramified classes occur."
    ),
    (
        "In both strata the listed triples include the exceptional root "
        "representatives from the complete 2-descent convention, and direct "
        "Hensel lifting of the residue classes gives the converse "
        "realization for every listed triple."
    ),
]

REMAINING_D2_OBLIGATIONS = ["D2_multi_collision_overlaps"]

MULTI_COLLISION_BOUNDARY = [
    {
        "condition": "odd ell divides at least two of L, T, sqrt_q",
        "status": "multi_collision_overlap_not_solved_here",
    }
]


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


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


def _has_d2d_obligation(d2_rows: dict[str, Any]) -> bool:
    return any(
        row.get("id") == "D2d_dyadic_complete_row"
        and row.get("place_type") == "ell=2"
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


def _prior_odd_row_is_scoped(
    row: dict[str, Any], *, lemma_id: str, status_key: str, status_value: str
) -> bool:
    return (
        row.get("lemma_id") == lemma_id
        and row.get(status_key) == status_value
        and row.get("local_c_d_rows_partially_solved") is True
        and row.get("local_c_d_rows_solved") is False
        and row.get("full_c_d_matrix_built") is False
        and row.get("complete_selmer_upper_bound_proved") is False
        and row.get("dim_sel2_eq_2_claimed") is False
        and row.get("rank_zero_claimed") is False
        and row.get("sha2_trivial_claimed") is False
        and row.get("family_exclusion_proved_count") == 0
    )


def audit_rank_zero_aa_bb_d2d_dyadic_complete_row(
    *,
    d0_container: dict[str, Any],
    d1_support: dict[str, Any],
    d2_rows: dict[str, Any],
    d3_baseline: dict[str, Any],
    d2a_row: dict[str, Any],
    d2b_row: dict[str, Any],
    d2c_row: dict[str, Any],
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
    if not _has_d2d_obligation(d2_rows):
        violations.append("d2d_obligation_missing")
    if not _ready(d3_baseline):
        violations.append("d3_baseline_not_ready")
    if not _d3_baseline_recorded_without_matrix(d3_baseline):
        if d3_baseline.get("full_c_d_matrix_built") is True:
            violations.append("d3_already_built_full_matrix")
        else:
            violations.append("d3_baseline_not_recorded_without_matrix")

    prior_specs = [
        (
            d2a_row,
            "D2a_odd_L_collision_row",
            "d2a_status",
            "pure_L_collision_row_solved",
            "d2a",
        ),
        (
            d2b_row,
            "D2b_odd_T_collision_row",
            "d2b_status",
            "pure_T_collision_row_solved",
            "d2b",
        ),
        (
            d2c_row,
            "D2c_odd_sqrt_q_collision_row",
            "d2c_status",
            "pure_sqrt_q_collision_row_solved",
            "d2c",
        ),
    ]
    for row, lemma_id, status_key, status_value, prefix in prior_specs:
        if not _ready(row):
            violations.append(f"{prefix}_row_not_ready")
        if not _prior_odd_row_is_scoped(
            row,
            lemma_id=lemma_id,
            status_key=status_key,
            status_value=status_value,
        ):
            if row.get("full_c_d_matrix_built") is True:
                violations.append(f"{prefix}_already_built_full_matrix")
            elif row.get("complete_selmer_upper_bound_proved") is True:
                violations.append(f"{prefix}_already_claims_selmer_bound")
            else:
                violations.append(f"{prefix}_row_not_scoped_pure_solution")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl471-wl477",
        "pattern": "AA+BB",
        "lemma_id": "D2d_dyadic_complete_row",
        "d2d_status": "dyadic_complete_row_solved",
        "complete_d_coordinate_order": COORDINATE_ORDER,
        "q2_squareclass_labels": DYADIC_SQUARECLASS_LABELS,
        "d0_container_used": "D0_complete_d_prelocal_container",
        "d1_support_used": "S_D1={infinity,2} union {odd ell: ell | L*T*sqrt_q}",
        "d2_obligation_used": "D2d_dyadic_complete_row",
        "d3_baseline_used_as_boundary_only": True,
        "wl475_referenced_only": True,
        "wl476_referenced_only": True,
        "wl477_referenced_only": True,
        "complete_d_equations": COMPLETE_D_EQUATIONS,
        "dyadic_strata": DYADIC_STRATA,
        "solved_local_rows": SOLVED_LOCAL_ROWS,
        "proof_summary": PROOF_SUMMARY,
        "row_depends_on_odd_unit_residues_of_L_or_T": False,
        "row_obstruction_remaining": False,
        "local_c_d_rows_partially_solved": True,
        "local_c_d_rows_solved": False,
        "solved_row_ids": [
            "D2a_odd_L_collision_row",
            "D2b_odd_T_collision_row",
            "D2c_odd_sqrt_q_collision_row",
            "D2d_dyadic_complete_row",
        ],
        "remaining_d2_obligations": REMAINING_D2_OBLIGATIONS,
        "multi_collision_overlaps_solved_here": False,
        "multi_collision_boundary": MULTI_COLLISION_BOUNDARY,
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
        "next_lemma": "D2_multi_collision_overlaps_not_started_here",
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
    parser.add_argument("--d2c-row", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_d2d_dyadic_complete_row(
        d0_container=load_json(args.d0_container),
        d1_support=load_json(args.d1_support),
        d2_rows=load_json(args.d2_rows),
        d3_baseline=load_json(args.d3_baseline),
        d2a_row=load_json(args.d2a_row),
        d2b_row=load_json(args.d2b_row),
        d2c_row=load_json(args.d2c_row),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB D2d dyadic complete-row audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"d2d_status={audit['d2d_status']}")
    print(f"local_c_d_rows_solved={audit['local_c_d_rows_solved']}")
    print(f"full_c_d_matrix_built={audit['full_c_d_matrix_built']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
