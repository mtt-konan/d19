#!/usr/bin/env python3
"""Audit the AA+BB route pivot after H2 coordinate equivalence fails."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only the route pivot after H2_coordinate_equivalence fails. "
    "It selects the next proof route and records reusable evidence, but proves "
    "no complete Sel_2(E) upper bound, rank zero, Sha[2]=0, or family exclusion."
)

ROUTE_DECISION = {
    "selected_route": "build_minimal_C_d_local_solubility_matrix",
    "why": (
        "H2 refutes the package x-triple as complete coordinate data, so the "
        "only bridge route still aimed at a Sel_2 upper bound must work in "
        "complete d-coordinates and test local solubility of C_d directly."
    ),
    "redefine_d_container_only": "necessary_as_setup_but_not_sufficient",
    "pivot_to_other_obstruction_route": (
        "defer_until_C_d_matrix_fails_or_exhibits_surviving_classes"
    ),
    "stop_after_route_pivot_audit": True,
}

MATRIX_SCOPE = {
    "builds_matrix_now": False,
    "minimal_matrix_target": (
        "local rows for C_d in complete d-coordinates over the relation "
        "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1"
    ),
    "why_minimal": (
        "The old S~ ledger killed tails only after collapsing to package "
        "x-coordinates. H2 shows those coordinates lose complete d-data, so "
        "the next proof object must be a d-coordinate local-solubility ledger."
    ),
    "places_to_prioritize_next": [
        "odd primes ell | T with ell == 1 mod 4",
        "the dyadic place",
        "real place only as already checked sign sanity",
    ],
}

NEXT_LEMMAS = [
    {
        "id": "D0_complete_d_container_definition",
        "status": "next_to_prove",
        "claim_status": "not_proved_here",
        "statement": (
            "Define the replacement container directly in complete "
            "d-coordinates, with product relation and torsion Kummer baseline "
            "inside the same quotient."
        ),
    },
    {
        "id": "D1_relevant_place_support_confinement",
        "status": "next_to_prove",
        "claim_status": "not_proved_here",
        "statement": (
            "Identify the finite set of places where C_d local solubility can "
            "cut the d-coordinate container."
        ),
    },
    {
        "id": "D2_local_C_d_row_characterization",
        "status": "next_to_prove",
        "claim_status": "not_proved_here",
        "statement": (
            "Write the minimal local solubility rows for C_d at the remaining "
            "places instead of using package x-coordinate rows."
        ),
    },
    {
        "id": "D3_torsion_baseline_in_d_coordinates",
        "status": "next_to_prove",
        "claim_status": "not_proved_here",
        "statement": (
            "Verify the two-dimensional torsion baseline in complete "
            "d-coordinates, including exceptional root representatives."
        ),
    },
    {
        "id": "D4_AA_BB_uniform_matrix_rank_bound",
        "status": "blocked_on_D0_D3",
        "claim_status": "not_proved_here",
        "statement": (
            "Only after D0-D3, prove or refute a uniform rank bound for the "
            "replacement d-coordinate matrix."
        ),
    },
]

OLD_S_TILDE_EVIDENCE_REUSE = {
    "reusable_as_boundary_evidence": [
        "wl465 object consistency: S~ is a pseudo-container, not Sel_2(E_L/Q)",
        "wl468 theorem bridge audit: Sel_2(E_L/Q) subset S~ is not proved",
        "wl469 H2 audit: package x-triple cannot replace complete d-data",
    ],
    "reusable_inside_old_container_only": [
        "wl466 sign-tail kill inside S~",
        "wl467 T-tail kill inside S~",
        "dim_F2 S~ <= 2 as a pseudo-container statement",
    ],
    "reusable_as_d_matrix_templates_only": [
        "wl457-wl459 odd-prime support rows, after re-proving them as C_d local rows",
        "wl460-wl462 dyadic local computations, after rewriting them in d-coordinates",
        "wl463 point-level collapse, only as a sanity check on rational-point images",
    ],
    "not_reusable_as_selmer_bridge": [
        "package x-coordinate equivalence",
        "direct transfer of mixed AA+BB common-source rows to all complete Selmer classes",
        "single-curve sample Selmer diagnostics as proof of a family bound",
    ],
}


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _h2_refuted(payload: dict[str, Any]) -> bool:
    verdict = payload.get("h2_verdict", {})
    return (
        verdict.get("status") == "refuted"
        and verdict.get("coordinate_equivalence_refuted") is True
        and verdict.get("coordinate_equivalence_proved") is False
    )


def audit_rank_zero_aa_bb_route_pivot(
    *,
    complete_two_descent_recast: dict[str, Any],
    theorem_bridge: dict[str, Any],
    h2_coordinate_equivalence: dict[str, Any],
    pseudo_selmer_container: dict[str, Any],
    t_tail_audit: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(complete_two_descent_recast):
        violations.append("complete_two_descent_recast_not_ready")
    if not _ready(theorem_bridge):
        violations.append("theorem_bridge_not_ready")
    if not _ready(h2_coordinate_equivalence):
        violations.append("h2_coordinate_equivalence_not_ready")
    if not _h2_refuted(h2_coordinate_equivalence):
        violations.append("h2_coordinate_equivalence_not_refuted")
    if not _ready(pseudo_selmer_container):
        violations.append("pseudo_selmer_container_not_ready")
    if not _ready(t_tail_audit):
        violations.append("t_tail_audit_not_ready")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl464-wl469",
        "pattern": "AA+BB",
        "route_decision": ROUTE_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "next_lemmas": NEXT_LEMMAS,
        "old_s_tilde_evidence_reuse": OLD_S_TILDE_EVIDENCE_REUSE,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "search_count_used_as_progress": False,
        "full_c_d_matrix_built": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complete-two-descent-recast", type=Path, required=True)
    parser.add_argument("--theorem-bridge", type=Path, required=True)
    parser.add_argument("--h2-coordinate-equivalence", type=Path, required=True)
    parser.add_argument("--pseudo-selmer-container", type=Path, required=True)
    parser.add_argument("--t-tail-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_route_pivot(
        complete_two_descent_recast=load_json(args.complete_two_descent_recast),
        theorem_bridge=load_json(args.theorem_bridge),
        h2_coordinate_equivalence=load_json(args.h2_coordinate_equivalence),
        pseudo_selmer_container=load_json(args.pseudo_selmer_container),
        t_tail_audit=load_json(args.t_tail_audit),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB route-pivot audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"selected_route={audit['route_decision']['selected_route']}")
    print(
        "complete_selmer_upper_bound_proved="
        f"{audit['complete_selmer_upper_bound_proved']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
