#!/usr/bin/env python3
"""Frame D2 local C_d row obligations for AA+BB complete d-covers."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only D2_local_C_d_row_characterization for the AA+BB "
    "complete d-coordinate route. It uses D0 and D1 to frame the minimal "
    "symbolic local C_d row obligations at S_D1, but solves no local rows, "
    "builds no full C_d matrix, proves no complete Sel_2(E) upper bound, "
    "makes no dim Sel_2(E)=2 claim, no rank zero, no Sha[2]=0, and no "
    "family exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

COMPLETE_D_COORDINATE_FRAME = {
    "curve": "E_L: Y^2=(X+p)*(X^2-4*q)",
    "coordinate_order": COORDINATE_ORDER,
    "product_relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2",
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
    "package_x_coordinates_used": False,
}

CANDIDATE_ROW_DOMAIN = {
    "source": "D1_relevant_place_support_confinement",
    "places": "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}",
    "odd_place_types": ["ell|L", "ell|T", "ell|sqrt_q"],
    "row_characterization_only": True,
}

LOCAL_ROW_OBLIGATIONS = [
    {
        "id": "D2a_odd_L_collision_row",
        "place_type": "ell|L",
        "prime_condition": "ell odd and ell | L",
        "colliding_roots": ["e_minus=-p", "e_pos=2*sqrt_q"],
        "vanishing_root_difference": "e_pos-e_minus = 16*L^2",
        "unit_root_difference_obligations": [
            (
                "check whether e_minus-e_neg=4*T^2 is an ell-adic unit in "
                "the active parameter stratum"
            ),
            (
                "check whether e_pos-e_neg=4*sqrt_q is an ell-adic unit in "
                "the active parameter stratum"
            ),
        ],
        "local_equation_to_characterize": (
            "d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = 16*L^2"
        ),
        "minimal_output_needed": (
            "allowed squareclass pairs for (d_minus_p,d_pos_2sqrt_q), then "
            "d_neg_2sqrt_q from the product relation"
        ),
        "status": "obligation_framed_not_solved",
    },
    {
        "id": "D2b_odd_T_collision_row",
        "place_type": "ell|T",
        "prime_condition": "ell odd and ell | T",
        "colliding_roots": ["e_minus=-p", "e_neg=-2*sqrt_q"],
        "vanishing_root_difference": "e_minus-e_neg = 4*T^2",
        "unit_root_difference_obligations": [
            (
                "check whether e_pos-e_minus=16*L^2 is an ell-adic unit in "
                "the active parameter stratum"
            ),
            (
                "check whether e_pos-e_neg=4*sqrt_q is an ell-adic unit in "
                "the active parameter stratum"
            ),
        ],
        "local_equation_to_characterize": (
            "d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*T^2"
        ),
        "minimal_output_needed": (
            "allowed squareclass pairs for (d_minus_p,d_neg_2sqrt_q), then "
            "d_pos_2sqrt_q from the product relation"
        ),
        "status": "obligation_framed_not_solved",
    },
    {
        "id": "D2c_odd_sqrt_q_collision_row",
        "place_type": "ell|sqrt_q",
        "prime_condition": "ell odd and ell | sqrt_q",
        "colliding_roots": ["e_pos=2*sqrt_q", "e_neg=-2*sqrt_q"],
        "vanishing_root_difference": "e_pos-e_neg = 4*sqrt_q",
        "unit_root_difference_obligations": [
            (
                "check whether e_pos-e_minus=16*L^2 is an ell-adic unit in "
                "the active parameter stratum"
            ),
            (
                "check whether e_minus-e_neg=4*T^2 is an ell-adic unit in "
                "the active parameter stratum"
            ),
        ],
        "local_equation_to_characterize": (
            "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 "
            "= -4*sqrt_q"
        ),
        "minimal_output_needed": (
            "allowed squareclass pairs for (d_pos_2sqrt_q,d_neg_2sqrt_q), "
            "then d_minus_p from the product relation"
        ),
        "status": "obligation_framed_not_solved",
    },
    {
        "id": "D2d_dyadic_complete_row",
        "place_type": "ell=2",
        "prime_condition": "v=2",
        "reason_2_is_relevant": (
            "all three root differences contain a factor 4 or 16, so odd-prime "
            "unit collision rows do not determine the dyadic local image"
        ),
        "local_equations_to_characterize": [
            "d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2 = 16*L^2",
            "d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*T^2",
            "d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2 = -4*sqrt_q",
        ],
        "minimal_output_needed": (
            "a Q_2 squareclass row for the complete d-triple, separated by the "
            "needed parity/residue strata of L,T,sqrt_q"
        ),
        "old_dyadic_package_rows_reused": False,
        "status": "obligation_framed_not_solved",
    },
    {
        "id": "D2e_real_sign_row",
        "place_type": "infinity",
        "root_order": [
            "e_neg=-2*sqrt_q",
            "e_minus=-p",
            "e_pos=2*sqrt_q",
        ],
        "allowed_sign_classes": [["+", "+", "+"], ["-", "-", "+"]],
        "forbidden_sign_classes": [["+", "-", "-"], ["-", "+", "-"]],
        "minimal_output_needed": (
            "record the real sign row only; do not combine it with finite rows "
            "into a rank bound"
        ),
        "status": "symbolically_characterized",
    },
]

ROW_AUDIT_BOUNDARIES = {
    "odd_rows_are_collision_obligations_not_allowed_subspaces": True,
    "dyadic_row_is_not_imported_from_old_package_x_coordinates": True,
    "real_row_is_recorded_without_selmer_bound_claim": True,
    "D3_torsion_baseline_not_entered": True,
    "D4_uniform_matrix_rank_bound_not_entered": True,
}


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _has_complete_d_container(d0_container: dict[str, Any]) -> bool:
    container = d0_container.get("complete_d_container", {})
    return (
        d0_container.get("lemma_id") == "D0_complete_d_container_definition"
        and container.get("name") == "D0_complete_d_prelocal_container"
        and container.get("coordinate_tuple_order") == COORDINATE_ORDER
    )


def _has_d0_product_relation(d0_container: dict[str, Any]) -> bool:
    relation = str(
        d0_container.get("complete_d_container", {}).get("defining_relation", "")
    )
    return "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1" in relation


def _uses_package_x_coordinates(d0_container: dict[str, Any]) -> bool:
    return (
        d0_container.get("complete_d_container", {}).get("package_x_coordinates_used")
        is True
    )


def _d1_is_exact_support(d1_support: dict[str, Any]) -> bool:
    support = d1_support.get("candidate_support", {})
    return (
        d1_support.get("lemma_id") == "D1_relevant_place_support_confinement"
        and d1_support.get("d1_status") == "framed_and_proved_support_confinement"
        and support.get("equivalent_finite_set")
        == "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}"
        and d1_support.get("support_only_not_row_classification") is True
    )


def audit_rank_zero_aa_bb_d2_local_c_d_row_characterization(
    *,
    d0_container: dict[str, Any],
    d1_support: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(d0_container):
        violations.append("d0_container_not_ready")
    if not _has_complete_d_container(d0_container):
        violations.append("d0_complete_d_container_missing")
    if not _has_d0_product_relation(d0_container):
        violations.append("d0_product_relation_missing")
    if _uses_package_x_coordinates(d0_container):
        violations.append("d0_uses_package_x_coordinates")
    if not _ready(d1_support):
        violations.append("d1_support_not_ready")
    if not _d1_is_exact_support(d1_support):
        violations.append("d1_support_not_exact_S_D1")
    if d1_support.get("local_c_d_rows_built") is True:
        violations.append("d1_already_built_local_rows")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl471-wl472",
        "pattern": "AA+BB",
        "lemma_id": "D2_local_C_d_row_characterization",
        "d2_status": "row_obligations_framed",
        "complete_d_coordinate_frame": COMPLETE_D_COORDINATE_FRAME,
        "candidate_row_domain": CANDIDATE_ROW_DOMAIN,
        "local_row_obligations": LOCAL_ROW_OBLIGATIONS,
        "row_audit_boundaries": ROW_AUDIT_BOUNDARIES,
        "d0_container_used": "D0_complete_d_prelocal_container",
        "d1_support_used": "S_D1={infinity,2} union {odd ell: ell | L*T*sqrt_q}",
        "row_obligations_framed": True,
        "local_c_d_rows_solved": False,
        "local_c_d_rows_built": False,
        "full_c_d_matrix_built": False,
        "d3_entered": False,
        "d4_entered": False,
        "old_package_x_coordinate_collapse_used": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "family_exclusion_proved_count": 0,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "search_count_used_as_progress": False,
        "next_lemma": "D3_torsion_baseline_in_d_coordinates",
        "do_not_proceed_to": [
            "D3_torsion_baseline_in_d_coordinates",
            "D4_AA_BB_uniform_matrix_rank_bound",
        ],
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--d0-container", type=Path, required=True)
    parser.add_argument("--d1-support", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_d2_local_c_d_row_characterization(
        d0_container=load_json(args.d0_container),
        d1_support=load_json(args.d1_support),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB D2 local C_d row-characterization audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"d2_status={audit['d2_status']}")
    print(f"local_c_d_rows_solved={audit['local_c_d_rows_solved']}")
    print(f"full_c_d_matrix_built={audit['full_c_d_matrix_built']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
