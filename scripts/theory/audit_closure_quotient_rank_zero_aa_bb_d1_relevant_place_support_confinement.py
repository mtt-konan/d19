#!/usr/bin/env python3
"""Frame D1 relevant-place support confinement for AA+BB complete d-covers."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only D1_relevant_place_support_confinement for the AA+BB "
    "complete d-coordinate route. It confines candidate d-coordinate support "
    "to the finite bad-place set before D2, but proves no local C_d rows, no "
    "complete Sel_2(E) upper bound, no dim Sel_2(E)=2 claim, no rank zero, "
    "no Sha[2]=0, and no family exclusion."
)

CANDIDATE_SUPPORT = {
    "name": "S_D1_relevant_places",
    "places": {
        "archimedean": ["infinity"],
        "dyadic": ["2"],
        "odd_bad_primes_general": (
            "odd ell dividing (e_minus-e_pos)*(e_minus-e_neg)*(e_pos-e_neg)"
        ),
        "odd_bad_primes_in_parameters": (
            "odd ell dividing (p+2*sqrt_q)*(p-2*sqrt_q)*(4*sqrt_q)"
        ),
        "odd_bad_primes_AA_BB_simplified": "odd ell dividing L*T*sqrt_q",
    },
    "parameter_identities": {
        "p+2*sqrt_q": "16*L^2",
        "p-2*sqrt_q": "-4*T^2",
        "4*sqrt_q": "4*(T^2+4*L^2)",
    },
    "equivalent_finite_set": "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}",
}

OUTSIDE_SUPPORT_CONFINEMENT = {
    "claim": (
        "For odd ell not in S_D1, C_d(Q_ell) forces each d-coordinate "
        "to have even ell-adic valuation."
    ),
    "reason": (
        "At good odd primes with distinct integral roots and unit root "
        "differences, the Kummer image for full rational 2-torsion is the "
        "unramified subgroup; ramified squareclasses cannot occur."
    ),
    "consequence": (
        "Global d-coordinate candidates may be represented by "
        "S_D1-supported squareclasses before D2 writes any local C_d rows."
    ),
}

SUPPORT_PROOF_OBLIGATIONS = [
    {
        "id": "D1a_good_odd_prime_unramified_image",
        "claim": (
            "If ell is odd, the three roots are ell-integral, and all root "
            "differences are ell-units, then every local Kummer d-coordinate "
            "has even ell-adic valuation."
        ),
        "status": "framed_as_standard_good_reduction_lemma",
    },
    {
        "id": "D1b_AA_BB_root_difference_support",
        "claim": (
            "For e_minus=-p, e_pos=2*sqrt_q, e_neg=-2*sqrt_q, the odd "
            "root-difference support is contained in primes dividing "
            "L*T*sqrt_q."
        ),
        "status": "proved_by_parameter_identities",
    },
    {
        "id": "D1c_no_local_row_written",
        "claim": (
            "D1 only restricts the global squareclass support; it does not "
            "classify the allowed local valuation rows at primes in S_D1."
        ),
        "status": "boundary_condition",
    },
]


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _d0_framed_without_rows(d0_container: dict[str, Any]) -> bool:
    return (
        d0_container.get("lemma_id") == "D0_complete_d_container_definition"
        and d0_container.get("d0_status") == "framed_definition"
        and d0_container.get("local_c_d_rows_built") is False
        and d0_container.get("complete_d_container", {}).get("local_c_d_rows_built")
        is False
    )


def _has_d0_relation(d0_container: dict[str, Any]) -> bool:
    relation = str(
        d0_container.get("complete_d_container", {}).get("defining_relation", "")
    )
    return "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1" in relation


def _has_complete_d_difference_equations(
    complete_two_descent_recast: dict[str, Any],
) -> bool:
    equations = complete_two_descent_recast.get(
        "complete_two_descent_coordinates", {}
    ).get("difference_equations", [])
    if not isinstance(equations, list):
        return False
    joined = "\n".join(str(item) for item in equations)
    return all(
        token in joined
        for token in ["p+2*sqrt_q", "p-2*sqrt_q", "-4*sqrt_q"]
    )


def audit_rank_zero_aa_bb_d1_relevant_place_support_confinement(
    *,
    d0_container: dict[str, Any],
    complete_two_descent_recast: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(d0_container):
        violations.append("d0_container_not_ready")
    if d0_container.get("local_c_d_rows_built") is True:
        violations.append("d0_already_built_local_rows")
    if (
        not _d0_framed_without_rows(d0_container)
        and "d0_already_built_local_rows" not in violations
    ):
        violations.append("d0_not_framed_without_local_rows")
    if not _has_d0_relation(d0_container):
        violations.append("d0_product_relation_missing")
    if not _ready(complete_two_descent_recast):
        violations.append("complete_two_descent_recast_not_ready")
    if not _has_complete_d_difference_equations(complete_two_descent_recast):
        violations.append("complete_d_difference_equations_missing")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl464-wl471",
        "pattern": "AA+BB",
        "lemma_id": "D1_relevant_place_support_confinement",
        "d1_status": "framed_and_proved_support_confinement",
        "candidate_support": CANDIDATE_SUPPORT,
        "outside_support_confinement": OUTSIDE_SUPPORT_CONFINEMENT,
        "support_proof_obligations": SUPPORT_PROOF_OBLIGATIONS,
        "d0_container_used": "D0_complete_d_prelocal_container",
        "support_only_not_row_classification": True,
        "d2_entered": False,
        "d3_entered": False,
        "d4_entered": False,
        "local_c_d_rows_built": False,
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "family_exclusion_proved_count": 0,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "search_count_used_as_progress": False,
        "next_lemma": "D2_local_C_d_row_characterization",
        "do_not_proceed_to": [
            "D2_local_C_d_row_characterization",
            "D3_torsion_baseline_in_d_coordinates",
            "D4_AA_BB_uniform_matrix_rank_bound",
        ],
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--d0-container", type=Path, required=True)
    parser.add_argument("--complete-two-descent-recast", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_d1_relevant_place_support_confinement(
        d0_container=load_json(args.d0_container),
        complete_two_descent_recast=load_json(args.complete_two_descent_recast),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB D1 relevant-place support audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"d1_status={audit['d1_status']}")
    print(f"local_c_d_rows_built={audit['local_c_d_rows_built']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
