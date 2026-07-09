#!/usr/bin/env python3
"""Record the AA+BB D3 torsion baseline in complete d-coordinates."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only D3_torsion_baseline_in_d_coordinates for the AA+BB "
    "complete d-coordinate route. It records the rational E_L[2](Q) Kummer "
    "baseline in complete d-coordinates using D0-D2, but solves no local C_d "
    "rows, builds no D4 matrix or rank bound, proves no complete Sel_2(E) "
    "upper bound, makes no dim Sel_2(E)=2 claim, no rank zero, no Sha[2]=0, "
    "and no family exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

REPRESENTATIVE_ORDER = [
    "O",
    "T_minus_p",
    "T_pos_2sqrt_q",
    "T_neg_2sqrt_q",
]

ROOT_LABELS = {
    "T_minus_p": "e_minus=-p",
    "T_pos_2sqrt_q": "e_pos=2*sqrt_q",
    "T_neg_2sqrt_q": "e_neg=-2*sqrt_q",
}

EXCEPTIONAL_ROOT_RULE = (
    "At X=e_i, replace the vanishing d_i coordinate by the product "
    "of the two nonzero root differences."
)

PRODUCT_RELATION_CHECKS = {
    "relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in V",
    "checks": {
        "O": "1*1*1=1",
        "T_minus_p": (
            "((-p-2*sqrt_q)*(-p+2*sqrt_q))*(-p-2*sqrt_q)*"
            "(-p+2*sqrt_q)=((-p-2*sqrt_q)*(-p+2*sqrt_q))^2"
        ),
        "T_pos_2sqrt_q": (
            "(2*sqrt_q+p)*((2*sqrt_q+p)*(4*sqrt_q))*(4*sqrt_q)="
            "((2*sqrt_q+p)*(4*sqrt_q))^2"
        ),
        "T_neg_2sqrt_q": (
            "(-2*sqrt_q+p)*(-4*sqrt_q)*((-2*sqrt_q+p)*(-4*sqrt_q))="
            "((-2*sqrt_q+p)*(-4*sqrt_q))^2"
        ),
    },
    "all_verified_symbolically_mod_squares": True,
}

BASELINE_GROUP_LAW_CHECKS = {
    "generators": ["T_minus_p", "T_pos_2sqrt_q"],
    "generator_product": "T_minus_p*T_pos_2sqrt_q=T_neg_2sqrt_q in V^3",
    "self_products": {
        "T_minus_p*T_minus_p": "O",
        "T_pos_2sqrt_q*T_pos_2sqrt_q": "O",
        "T_neg_2sqrt_q*T_neg_2sqrt_q": "O",
    },
    "mixed_products": {
        "T_minus_p*T_pos_2sqrt_q": "T_neg_2sqrt_q",
        "T_minus_p*T_neg_2sqrt_q": "T_pos_2sqrt_q",
        "T_pos_2sqrt_q*T_neg_2sqrt_q": "T_minus_p",
    },
    "all_verified_coordinatewise_mod_squares": True,
}

SAFETY_BOUNDARIES = {
    "baseline_recorded_not_quotiented": True,
    "local_c_d_rows_solved_here": False,
    "local_c_d_rows_built_here": False,
    "d4_matrix_built_here": False,
    "selmer_upper_bound_proved_here": False,
}


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


def _has_d0_product_relation(d0_container: dict[str, Any]) -> bool:
    relation = str(
        d0_container.get("complete_d_container", {}).get("defining_relation", "")
    )
    return "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1" in relation


def _torsion_baseline_complete(d0_container: dict[str, Any]) -> bool:
    baseline = d0_container.get("torsion_kummer_baseline", {})
    representatives = baseline.get("representatives", {})
    return (
        baseline.get("same_quotient_as_container") is True
        and baseline.get("baseline_dimension") == 2
        and baseline.get("representative_order") == REPRESENTATIVE_ORDER
        and all(name in representatives for name in REPRESENTATIVE_ORDER)
        and baseline.get("baseline_generators") == ["T_minus_p", "T_pos_2sqrt_q"]
        and baseline.get("product_relation_verified_for_representatives") is True
        and baseline.get("baseline_not_quotiented_out") is True
    )


def _d1_support_ready_without_rows(d1_support: dict[str, Any]) -> bool:
    support = d1_support.get("candidate_support", {})
    return (
        d1_support.get("lemma_id") == "D1_relevant_place_support_confinement"
        and d1_support.get("d1_status") == "framed_and_proved_support_confinement"
        and support.get("equivalent_finite_set")
        == "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}"
        and d1_support.get("support_only_not_row_classification") is True
        and d1_support.get("local_c_d_rows_built") is False
    )


def _d2_rows_framed_without_solving(d2_rows: dict[str, Any]) -> bool:
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
    )


def _d2_row_ids(d2_rows: dict[str, Any]) -> list[str]:
    return [
        str(row.get("id"))
        for row in d2_rows.get("local_row_obligations", [])
        if row.get("id")
    ]


def _representatives_from_d0(d0_container: dict[str, Any]) -> dict[str, list[str]]:
    representatives = d0_container.get("torsion_kummer_baseline", {}).get(
        "representatives", {}
    )
    return {
        name: list(representatives[name])
        for name in REPRESENTATIVE_ORDER
        if name in representatives
    }


def _ambient_squareclass_quotient(d0_container: dict[str, Any]) -> str:
    return str(
        d0_container.get("complete_d_container", {}).get(
            "ambient_squareclass_quotient",
            "V = Q*/Q*2; triples are in V^3 and multiplied coordinatewise",
        )
    )


def _rational_two_torsion_baseline(
    d0_container: dict[str, Any],
) -> dict[str, Any]:
    return {
        "object_recorded": "rational E_L[2](Q) Kummer baseline",
        "ambient_squareclass_quotient": _ambient_squareclass_quotient(d0_container),
        "coordinate_order": COORDINATE_ORDER,
        "baseline_dimension": 2,
        "representative_order": REPRESENTATIVE_ORDER,
        "representatives": _representatives_from_d0(d0_container),
        "root_labels": ROOT_LABELS,
        "exceptional_root_rule": EXCEPTIONAL_ROOT_RULE,
        "same_quotient_as_container": True,
        "baseline_not_quotiented_out": True,
    }


def _baseline_comparison_contract(d2_rows: dict[str, Any]) -> dict[str, Any]:
    return {
        "comparison_target": "future solved local C_d rows from D2 obligations",
        "d2_row_ids_to_compare_against": _d2_row_ids(d2_rows),
        "comparison_status": "pending_until_local_c_d_rows_are_solved",
        "comparison_rule": (
            "Check each of O, T_minus_p, T_pos_2sqrt_q, and "
            "T_neg_2sqrt_q against each solved local row in the same "
            "complete d-coordinate order before any quotient or rank ledger."
        ),
        "quotient_baseline_here": False,
        "baseline_must_remain_visible_for_D4": True,
    }


def audit_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates(
    *,
    d0_container: dict[str, Any],
    d1_support: dict[str, Any],
    d2_rows: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(d0_container):
        violations.append("d0_container_not_ready")
    if not _has_complete_d_container(d0_container):
        violations.append("d0_complete_d_container_missing")
    if not _has_d0_product_relation(d0_container):
        violations.append("d0_product_relation_missing")
    if not _torsion_baseline_complete(d0_container):
        violations.append("d0_torsion_baseline_incomplete_or_quotiented")
    if not _ready(d1_support):
        violations.append("d1_support_not_ready")
    if not _d1_support_ready_without_rows(d1_support):
        if d1_support.get("local_c_d_rows_built") is True:
            violations.append("d1_already_built_local_rows")
        else:
            violations.append("d1_support_not_exact_S_D1")
    if not _ready(d2_rows):
        violations.append("d2_rows_not_ready")
    if not _d2_rows_framed_without_solving(d2_rows):
        if d2_rows.get("local_c_d_rows_solved") is True:
            violations.append("d2_already_solved_local_rows")
        if d2_rows.get("full_c_d_matrix_built") is True:
            violations.append("d2_already_built_full_matrix")
        if (
            d2_rows.get("local_c_d_rows_solved") is not True
            and d2_rows.get("full_c_d_matrix_built") is not True
        ):
            violations.append("d2_row_obligations_not_framed")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl471-wl473",
        "pattern": "AA+BB",
        "lemma_id": "D3_torsion_baseline_in_d_coordinates",
        "d3_status": "torsion_baseline_recorded_in_complete_d_coordinates",
        "d0_container_used": "D0_complete_d_prelocal_container",
        "d1_support_used": "S_D1={infinity,2} union {odd ell: ell | L*T*sqrt_q}",
        "d2_rows_used": "D2_local_C_d_row_characterization obligations only",
        "rational_two_torsion_baseline": _rational_two_torsion_baseline(
            d0_container
        ),
        "product_relation_checks": PRODUCT_RELATION_CHECKS,
        "baseline_group_law_checks": BASELINE_GROUP_LAW_CHECKS,
        "baseline_comparison_contract": _baseline_comparison_contract(d2_rows),
        "safety_boundaries": SAFETY_BOUNDARIES,
        "local_c_d_rows_solved": False,
        "local_c_d_rows_built": False,
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
        "next_lemma": "D2_local_C_d_row_solving",
        "do_not_proceed_to": ["D4_AA_BB_uniform_matrix_rank_bound"],
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--d0-container", type=Path, required=True)
    parser.add_argument("--d1-support", type=Path, required=True)
    parser.add_argument("--d2-rows", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates(
        d0_container=load_json(args.d0_container),
        d1_support=load_json(args.d1_support),
        d2_rows=load_json(args.d2_rows),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB D3 torsion-baseline audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"d3_status={audit['d3_status']}")
    print(
        "quotient_baseline_here="
        f"{audit['baseline_comparison_contract']['quotient_baseline_here']}"
    )
    print(f"full_c_d_matrix_built={audit['full_c_d_matrix_built']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
