#!/usr/bin/env python3
"""Discharge AA+BB D2 odd multi-collision overlaps in complete d-coordinates."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl479 / D2_multi_collision_overlaps for the AA+BB "
    "complete d-coordinate route. It proves that odd primes dividing at "
    "least two of L, T, and sqrt_q are impossible under the primitive "
    "A:B normalization, using only sqrt_q=T^2+4*L^2 and the odd-prime "
    "hypothesis. The overlap row is therefore vacuous. This completes the "
    "scoped D2 row-obligation ledger but does not build D4, combine rows "
    "into a complete Sel_2(E) upper bound, claim dim Sel_2(E)=2, rank zero, "
    "Sha[2]=0, or any family exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

OVERLAP_GCD_LEMMA = {
    "id": "odd_overlap_equivalence_to_gcd_L_T",
    "statement": (
        "For odd ell and sqrt_q=T^2+4*L^2, ell divides at least two of "
        "{L,T,sqrt_q} if and only if ell divides gcd(L,T); in that case "
        "ell divides all three."
    ),
    "pair_implications": [
        "ell|L and ell|T imply ell|sqrt_q",
        "ell|L and ell|sqrt_q imply ell|T",
        "ell|T and ell|sqrt_q imply ell|L",
    ],
}

PRIMITIVE_NORMALIZATION_INPUTS_NEEDED = [
    "A:B is primitive, so gcd(A,B)=1",
    "T=A+B",
    "L=A on the AA side or L=B on the BB side",
    "therefore gcd(L,T)=1",
    "ell is odd; ell=2 is handled only by wl478",
]

OVERLAP_CASES = [
    {
        "case": "ell | L and ell | T",
        "deduction": "sqrt_q=T^2+4*L^2 is also divisible by ell",
        "primitive_status": "impossible because ell would divide gcd(L,T)",
    },
    {
        "case": "ell | L and ell | sqrt_q",
        "deduction": "T^2=sqrt_q-4*L^2 is divisible by ell, hence ell | T",
        "primitive_status": "impossible because ell would divide gcd(L,T)",
    },
    {
        "case": "ell | T and ell | sqrt_q",
        "deduction": "4*L^2=sqrt_q-T^2 is divisible by ell, hence ell | L",
        "primitive_status": "impossible because ell is odd and would divide gcd(L,T)",
    },
]

PROOF_SUMMARY = [
    (
        "The only identity needed for overlaps is sqrt_q=T^2+4*L^2. For an "
        "odd ell, the factor 4 is a unit, so divisibility by two of "
        "L, T, sqrt_q forces divisibility by the third."
    ),
    (
        "Thus any odd multi-collision is exactly an odd prime divisor of "
        "gcd(L,T). In the AA+BB primitive normalization, T=A+B and "
        "L is A on the AA side or B on the BB side, so gcd(L,T)=gcd(A,B)=1."
    ),
    (
        "Consequently no odd overlap local C_d row exists in the normalized "
        "AA+BB route. The pure odd rows wl475-wl477 and the dyadic row wl478 "
        "exhaust the D2 finite row obligations; this statement is only a "
        "local-row ledger result, not a Selmer upper-bound theorem."
    ),
]


def overlap_support_for_odd_prime(ell: int, *, L: int, T: int) -> dict[str, object]:
    if ell % 2 == 0 or ell <= 1:
        raise ValueError("ell must be an odd prime for this audit helper")
    sqrt_q = T * T + 4 * L * L
    divides_l = L % ell == 0
    divides_t = T % ell == 0
    divides_sqrt_q = sqrt_q % ell == 0
    hit_count = sum([divides_l, divides_t, divides_sqrt_q])
    return {
        "ell": ell,
        "sqrt_q": sqrt_q,
        "divides_L": divides_l,
        "divides_T": divides_t,
        "divides_sqrt_q": divides_sqrt_q,
        "divides_at_least_two": hit_count >= 2,
        "divides_gcd_L_T": math.gcd(L, T) % ell == 0,
        "divides_all_three": hit_count == 3,
    }


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


def _prior_row_is_scoped(
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


def audit_rank_zero_aa_bb_d2_multi_collision_overlaps(
    *,
    d0_container: dict[str, Any],
    d1_support: dict[str, Any],
    d2_rows: dict[str, Any],
    d3_baseline: dict[str, Any],
    d2a_row: dict[str, Any],
    d2b_row: dict[str, Any],
    d2c_row: dict[str, Any],
    d2d_row: dict[str, Any],
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
        (
            d2d_row,
            "D2d_dyadic_complete_row",
            "d2d_status",
            "dyadic_complete_row_solved",
            "d2d",
        ),
    ]
    for row, lemma_id, status_key, status_value, prefix in prior_specs:
        if not _ready(row):
            violations.append(f"{prefix}_row_not_ready")
        if not _prior_row_is_scoped(
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
                violations.append(f"{prefix}_row_not_scoped_prior_solution")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl471-wl478",
        "pattern": "AA+BB",
        "lemma_id": "D2_multi_collision_overlaps",
        "work_log": "wl479",
        "d2_multi_status": (
            "odd_multi_collision_overlaps_impossible_under_primitive_normalization"
        ),
        "complete_d_coordinate_order": COORDINATE_ORDER,
        "d0_container_used": "D0_complete_d_prelocal_container",
        "d1_support_used": "S_D1={infinity,2} union {odd ell: ell | L*T*sqrt_q}",
        "d2_obligation_used": "D2_multi_collision_overlaps",
        "d3_baseline_used_as_boundary_only": True,
        "wl475_referenced_only": True,
        "wl476_referenced_only": True,
        "wl477_referenced_only": True,
        "wl478_referenced_only": True,
        "identity_used": "sqrt_q=T^2+4*L^2",
        "odd_prime_hypothesis_used": True,
        "overlap_gcd_lemma": OVERLAP_GCD_LEMMA,
        "primitive_normalization_inputs_needed": PRIMITIVE_NORMALIZATION_INPUTS_NEEDED,
        "overlap_cases": OVERLAP_CASES,
        "proof_summary": PROOF_SUMMARY,
        "multi_collision_overlaps_possible_under_aa_bb_inputs": False,
        "complete_local_c_d_row_for_overlaps": "vacuous_empty_row",
        "row_obstruction_remaining": False,
        "local_c_d_rows_partially_solved": True,
        "local_c_d_rows_solved": True,
        "local_c_d_rows_solved_scope": (
            "D2 symbolic local row obligations only; no D4 matrix or Selmer "
            "upper-bound combination is built here"
        ),
        "solved_row_ids": [
            "D2a_odd_L_collision_row",
            "D2b_odd_T_collision_row",
            "D2c_odd_sqrt_q_collision_row",
            "D2d_dyadic_complete_row",
            "D2_multi_collision_overlaps",
        ],
        "remaining_d2_obligations": [],
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
        "next_lemma": "D4_not_started_here",
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
    parser.add_argument("--d2d-row", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_d2_multi_collision_overlaps(
        d0_container=load_json(args.d0_container),
        d1_support=load_json(args.d1_support),
        d2_rows=load_json(args.d2_rows),
        d3_baseline=load_json(args.d3_baseline),
        d2a_row=load_json(args.d2a_row),
        d2b_row=load_json(args.d2b_row),
        d2c_row=load_json(args.d2c_row),
        d2d_row=load_json(args.d2d_row),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB D2 multi-collision overlap audit to {args.out}")
    print(f"status={audit['status']}")
    print("d2_multi_status=odd_multi_collision_overlaps_impossible")
    print(f"local_c_d_rows_solved={audit['local_c_d_rows_solved']}")
    print(f"full_c_d_matrix_built={audit['full_c_d_matrix_built']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
