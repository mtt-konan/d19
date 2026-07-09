#!/usr/bin/env python3
"""Audit the AA+BB D4 uniform matrix rank bound from solved C_d rows."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl480 / D4_AA_BB_uniform_matrix_rank_bound_audit for "
    "the AA+BB complete d-coordinate route. It combines the solved D2 local "
    "row ledger, the real sign row, the D0 product relation, and the D3 "
    "torsion baseline into a symbolic F2 dimension ledger. It does not prove "
    "a complete Sel_2(E) upper bound, does not claim dim Sel_2(E)=2, rank "
    "zero, Sha[2]=0, or any family exclusion. The outcome is a rank-condition "
    "obstruction, not a theorem-strength Selmer bound."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

ROW_GENERATOR_LEDGER = [
    {
        "source": "real sign row",
        "generator_family": "tau_minus",
        "coordinate_pattern": "(-1,-1,+1)",
        "role": "one rational 2-torsion baseline generator",
    },
    {
        "source": "pure odd ell|L rows",
        "generator_family": "u_ell for ell|L",
        "coordinate_pattern": "(ell,ell,1)",
        "free_count_symbol": "omega_L",
    },
    {
        "source": "pure odd ell|T rows",
        "generator_family": "v_ell for ell|T",
        "coordinate_pattern": "(ell,1,ell)",
        "free_count_symbol": "omega_T",
    },
    {
        "source": "pure odd ell|sqrt_q rows",
        "generator_family": "w_ell for ell|sqrt_q",
        "coordinate_pattern": "(1,ell,ell)",
        "free_count_symbol": "omega_sqrt_q",
    },
    {
        "source": "dyadic row",
        "generator_family": "w_2",
        "coordinate_pattern": "(1,2,2)",
        "free_count_symbol": "epsilon_balanced_2",
        "ordinary_even_sqrt_q_value": 0,
        "balanced_odd_sqrt_q_value": 1,
    },
]

BASELINE_QUOTIENT_LEDGER = {
    "baseline_dimension": 2,
    "baseline_generators": [
        "tau_minus=(-1,-1,+1)",
        (
            "tau_sqrt_q=product_{ell|sqrt_q} w_ell times w_2 when "
            "v2(sqrt_q) is odd"
        ),
    ],
    "baseline_contained_in_row_ledger": True,
    "baseline_quotiented_for_tail_formula": True,
}

SOLVED_ROW_IDS = [
    "D2a_odd_L_collision_row",
    "D2b_odd_T_collision_row",
    "D2c_odd_sqrt_q_collision_row",
    "D2d_dyadic_complete_row",
    "D2_multi_collision_overlaps",
    "D2e_real_sign_row_from_wl473",
]

LOCAL_CHARACTER_MATRIX_DESCRIPTION = {
    "id": "M_tail",
    "object": (
        "parameter-dependent F2 matrix of residual local characters left by "
        "the solved complete d-coordinate rows after D0 and D3"
    ),
    "rows": [
        "odd ell|L unit equalities: local class(d_minus_p)=local class(d_pos_2sqrt_q)",
        "odd ell|T unit equalities: local class(d_minus_p)=local class(d_neg_2sqrt_q)",
        "odd ell|sqrt_q unit equalities: local class(d_pos_2sqrt_q)=local class(d_neg_2sqrt_q)",
        "Q_2 dyadic aggregate class constraints from wl478 stratum",
    ],
    "entries": (
        "Legendre/Hilbert character values of the other selected support "
        "generators at the active local row, plus the dyadic residue characters"
    ),
    "not_uniformly_ranked_by_wl480_inputs": True,
}

SURVIVING_OBSTRUCTION = {
    "id": "M_tail_uniform_full_rank_missing",
    "description": (
        "The solved rows identify the exact tail matrix whose kernel would be "
        "the non-torsion part of the complete d-coordinate container, but the "
        "current ledger does not prove that this parameter-dependent matrix "
        "has full tail rank for every primitive AA+BB input."
    ),
    "tail_dimension_formula": (
        "dim(tail)=omega_L+omega_T+omega_sqrt_q+epsilon_balanced_2-1-rank(M_tail)"
    ),
    "uniform_bound_obstruction": (
        "Need a uniform lower bound rank(M_tail) >= "
        "omega_L+omega_T+omega_sqrt_q+epsilon_balanced_2-1."
    ),
}

PROOF_SUMMARY = [
    (
        "The D0 product relation reduces each global squareclass support "
        "generator to a two-coordinate pattern. The solved pure odd rows give "
        "(ell,ell,1), (ell,1,ell), and (1,ell,ell) for the L, T, and sqrt_q "
        "support classes respectively."
    ),
    (
        "The real row contributes exactly the sign pattern (-1,-1,+1), which "
        "is one D3 torsion generator. The dyadic row contributes no separate "
        "prime-2 generator in the ordinary stratum and contributes the "
        "(1,2,2) generator in the balanced stratum."
    ),
    (
        "The second D3 torsion generator is the total sqrt_q squareclass, i.e. "
        "the product of all sqrt_q-prime generators and the balanced 2-generator "
        "when v2(sqrt_q) is odd. Quotienting the visible torsion baseline leaves "
        "the symbolic tail dimension formula."
    ),
    (
        "The remaining odd unit and dyadic aggregate conditions are exactly a "
        "parameter-dependent F2 character matrix M_tail. wl480 does not contain "
        "a uniform full-rank theorem for that matrix, so the ledger does not "
        "force a complete Selmer upper bound of dimension 2."
    ),
]


def f2_rank(rows: list[list[int]]) -> int:
    """Return the row rank over F2."""
    vectors = [
        sum((entry & 1) << index for index, entry in enumerate(row))
        for row in rows
    ]
    rank = 0
    while vectors:
        pivot = max(vectors)
        if pivot == 0:
            break
        rank += 1
        pivot_bit = pivot.bit_length() - 1
        next_vectors: list[int] = []
        for vector in vectors:
            if vector == pivot:
                continue
            if (vector >> pivot_bit) & 1:
                vector ^= pivot
            if vector:
                next_vectors.append(vector)
        vectors = next_vectors
    return rank


def tail_dimension_formula(
    *,
    omega_L: int,
    omega_T: int,
    omega_sqrt_q: int,
    epsilon_balanced_2: int,
    tail_matrix_rank: int,
) -> dict[str, object]:
    rank_needed = omega_L + omega_T + omega_sqrt_q + epsilon_balanced_2 - 1
    ambient = 1 + omega_L + omega_T + omega_sqrt_q + epsilon_balanced_2
    tail = rank_needed - tail_matrix_rank
    return {
        "ambient_row_ledger_dimension_formula": (
            "1 + omega_L + omega_T + omega_sqrt_q + epsilon_balanced_2 - "
            "rank(M_tail)"
        ),
        "torsion_baseline_dimension": 2,
        "tail_dimension_formula": (
            "omega_L + omega_T + omega_sqrt_q + epsilon_balanced_2 - 1 - "
            "rank(M_tail)"
        ),
        "numeric_ambient_row_ledger_dimension": ambient - tail_matrix_rank,
        "numeric_tail_dimension_after_torsion": tail,
        "rank_needed_for_uniform_dim2_bound": rank_needed,
        "provided_tail_matrix_rank": tail_matrix_rank,
        "uniform_dim2_bound_for_these_counts": tail == 0,
    }


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        payload.get("complete_selmer_upper_bound_proved") is True
        or payload.get("dim_sel2_eq_2_claimed") is True
        or payload.get("rank_zero_claimed") is True
        or payload.get("sha2_trivial_claimed") is True
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _d3_baseline_ready(d3_baseline: dict[str, Any]) -> bool:
    baseline = d3_baseline.get("rational_two_torsion_baseline", {})
    contract = d3_baseline.get("baseline_comparison_contract", {})
    return (
        d3_baseline.get("lemma_id") == "D3_torsion_baseline_in_d_coordinates"
        and d3_baseline.get("d3_status")
        == "torsion_baseline_recorded_in_complete_d_coordinates"
        and baseline.get("baseline_dimension") == 2
        and baseline.get("baseline_not_quotiented_out") is True
        and contract.get("quotient_baseline_here") is False
    )


def _prior_row_ok(
    row: dict[str, Any], *, lemma_id: str, status_key: str, status_value: str
) -> bool:
    return (
        row.get("lemma_id") == lemma_id
        and row.get(status_key) == status_value
        and row.get("full_c_d_matrix_built") is False
        and not _claims_forbidden_bound(row)
    )


def _multi_row_ok(row: dict[str, Any]) -> bool:
    return (
        row.get("lemma_id") == "D2_multi_collision_overlaps"
        and row.get("d2_multi_status")
        == "odd_multi_collision_overlaps_impossible_under_primitive_normalization"
        and row.get("local_c_d_rows_solved") is True
        and row.get("remaining_d2_obligations") == []
        and row.get("multi_collision_overlaps_possible_under_aa_bb_inputs") is False
        and row.get("complete_local_c_d_row_for_overlaps") == "vacuous_empty_row"
        and not _claims_forbidden_bound(row)
    )


def audit_rank_zero_aa_bb_d4_uniform_matrix_rank_bound(
    *,
    d3_baseline: dict[str, Any],
    d2a_row: dict[str, Any],
    d2b_row: dict[str, Any],
    d2c_row: dict[str, Any],
    d2d_row: dict[str, Any],
    d2_multi_row: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(d3_baseline):
        violations.append("d3_baseline_not_ready")
    if not _d3_baseline_ready(d3_baseline):
        violations.append("d3_torsion_baseline_not_available_for_d4")

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
        if not _prior_row_ok(
            row,
            lemma_id=lemma_id,
            status_key=status_key,
            status_value=status_value,
        ):
            violations.append(f"{prefix}_row_not_scoped_solved_row")

    if not _ready(d2_multi_row):
        violations.append("d2_multi_row_not_ready")
    if not _multi_row_ok(d2_multi_row):
        violations.append("d2_multi_row_not_completed_or_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl473-wl479",
        "pattern": "AA+BB",
        "lemma_id": "D4_AA_BB_uniform_matrix_rank_bound_audit",
        "work_log": "wl480",
        "d4_status": "uniform_dim2_bound_not_forced_by_solved_rows",
        "complete_d_coordinate_order": COORDINATE_ORDER,
        "d0_product_relation_used": (
            "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2"
        ),
        "d3_torsion_baseline_used": True,
        "d3_torsion_baseline_dimension": 2,
        "solved_row_ids": SOLVED_ROW_IDS,
        "global_f2_dimension_ledger_built": True,
        "row_generator_ledger": ROW_GENERATOR_LEDGER,
        "baseline_quotient_ledger": BASELINE_QUOTIENT_LEDGER,
        "local_character_matrix": LOCAL_CHARACTER_MATRIX_DESCRIPTION,
        "dimension_ledger": {
            "omega_symbols": [
                "omega_L=#odd primes dividing L",
                "omega_T=#odd primes dividing T",
                "omega_sqrt_q=#odd primes dividing sqrt_q",
            ],
            "epsilon_balanced_2": (
                "1 when v2(T)=v2(L)+1, equivalently v2(sqrt_q) is odd; "
                "0 in the ordinary dyadic stratum"
            ),
            "pre_character_matrix_dimension": (
                "1+omega_L+omega_T+omega_sqrt_q+epsilon_balanced_2"
            ),
            "after_torsion_tail_dimension": (
                "omega_L+omega_T+omega_sqrt_q+epsilon_balanced_2-1-rank(M_tail)"
            ),
            "rank_needed_for_dim2_bound": (
                "omega_L+omega_T+omega_sqrt_q+epsilon_balanced_2-1"
            ),
        },
        "uniform_bound_decision": {
            "complete_selmer_upper_bound_dimension_2_forced": False,
            "reason": (
                "The solved rows reduce D4 to a parameter-dependent F2 character "
                "matrix M_tail, but the ledger contains no uniform proof that "
                "M_tail has the required full rank."
            ),
            "rank_condition_needed": (
                "rank(M_tail)=omega_L+omega_T+omega_sqrt_q+"
                "epsilon_balanced_2-1"
            ),
        },
        "surviving_obstruction": SURVIVING_OBSTRUCTION,
        "proof_summary": PROOF_SUMMARY,
        "full_parameter_specialized_matrix_built": False,
        "full_c_d_matrix_built": False,
        "d4_entered": True,
        "old_package_x_coordinate_collapse_used": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "family_exclusion_proved_count": 0,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "search_count_used_as_progress": False,
        "next_lemma": "prove_uniform_full_rank_for_M_tail_or_find_kernel_obstruction",
        "do_not_proceed_to": [
            "rank_zero_claim",
            "dim_Sel_2_E_eq_2_claim",
            "Sha_2_trivial_claim",
            "family_exclusion_claim",
        ],
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--d3-baseline", type=Path, required=True)
    parser.add_argument("--d2a-row", type=Path, required=True)
    parser.add_argument("--d2b-row", type=Path, required=True)
    parser.add_argument("--d2c-row", type=Path, required=True)
    parser.add_argument("--d2d-row", type=Path, required=True)
    parser.add_argument("--d2-multi-row", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_d4_uniform_matrix_rank_bound(
        d3_baseline=load_json(args.d3_baseline),
        d2a_row=load_json(args.d2a_row),
        d2b_row=load_json(args.d2b_row),
        d2c_row=load_json(args.d2c_row),
        d2d_row=load_json(args.d2d_row),
        d2_multi_row=load_json(args.d2_multi_row),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB D4 uniform matrix-rank audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"d4_status={audit['d4_status']}")
    print(
        "complete_selmer_upper_bound_proved="
        f"{audit['complete_selmer_upper_bound_proved']}"
    )
    print(f"surviving_obstruction={audit['surviving_obstruction']['id']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
