#!/usr/bin/env python3
"""Audit the bridge from S~ <= 2 to a complete Selmer upper bound."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only the theorem-candidate bridge from the AA+BB pseudo-container "
    "S~ to a complete 2-Selmer upper-bound statement. It proves no full "
    "Sel_2(E) upper bound, rank zero, Sha[2]=0, or family exclusion."
)

BRIDGE_SUMMARY = {
    "cheap_container_result": "dim_F2 S_tilde_AA_BB <= 2",
    "relevant_complete_selmer_object": (
        "Sel_2(E_L/Q) for the complete full-rational-2-torsion curve "
        "E_L: Y^2=(X+p)*(X^2-4*q), with L=A on AA and L=B on BB"
    ),
    "s_tilde_is_valid_upper_bound_for_complete_selmer": False,
    "complete_selmer_upper_bound_proved": False,
    "theorem_candidate_promotable": False,
    "reason": (
        "The killed ledger bounds only the AA+BB common-source pseudo-container; "
        "it has not been proved to contain every class of the complete "
        "2-Selmer group Sel_2(E_L/Q)."
    ),
}

REQUIRED_HYPOTHESES = [
    {
        "id": "H1_complete_selmer_object",
        "needed": True,
        "status": "framed_not_proved",
        "statement": (
            "Fix the theorem object as Sel_2(E_L/Q) for each AA or BB side, "
            "not the AA+BB common-source pseudo-container and not sampled "
            "single-curve diagnostics."
        ),
    },
    {
        "id": "H2_coordinate_equivalence",
        "needed": True,
        "status": "partially_framed",
        "statement": (
            "Prove the complete-descent d-coordinates and the three package "
            "x-coordinates define equivalent squareclass data for every "
            "Selmer class, including torsion representatives and exceptional "
            "root cases."
        ),
    },
    {
        "id": "H3_uniform_local_containment",
        "needed": True,
        "status": "missing",
        "statement": (
            "For every place v and every complete 2-cover C_d locally soluble "
            "over Q_v, prove its translated x-data satisfies the constraints "
            "used to define S_tilde_AA_BB."
        ),
    },
    {
        "id": "H4_mixed_rows_upgrade",
        "needed": True,
        "status": "missing",
        "statement": (
            "Upgrade wl457-wl459 from AA+BB mixed common-source support rows "
            "to valid constraints on all complete Selmer classes, or prove a "
            "separate theorem that every relevant Selmer class is represented "
            "by such a common-source class."
        ),
    },
    {
        "id": "H5_dimension_and_torsion_identification",
        "needed": True,
        "status": "missing",
        "statement": (
            "After Sel_2(E_L/Q) subset S_tilde_AA_BB is proved, identify the "
            "two-dimensional torsion baseline inside the same ambient quotient "
            "and verify dim_F2 S_tilde_AA_BB <= 2 in that quotient."
        ),
    },
]

FORMAL_GAPS = [
    "No proved inclusion Sel_2(E_L/Q) subset S_tilde_AA_BB.",
    (
        "The support-killing rows wl457-wl459 are still mixed AA+BB common-source "
        "rows, not complete local matrix rows."
    ),
    (
        "The full C_d local-solubility matrix has not been built or shown "
        "redundant for all Selmer classes."
    ),
    "The killed T-tail and sign-tail remove symbolic tails only inside S_tilde_AA_BB.",
    (
        "Therefore dim_F2 S_tilde_AA_BB <= 2 is not yet a rigorous upper bound "
        "for dim_F2 Sel_2(E_L/Q)."
    ),
]

OBJECT_BOUNDARY = {
    "s_tilde_object": "AA+BB common-source pseudo-Selmer upper-bound container",
    "complete_selmer_object": "Sel_2(E_L/Q) for the individual complete 2-descent curve",
    "sample_diagnostic_object": "single_curve_full_2_selmer diagnostics only",
    "valid_implication_currently_proved": (
        "AA+BB common-source Selmer-candidate ledger classes are contained in S~"
    ),
    "invalid_implication_not_proved": "Sel_2(E_L/Q) subset S~",
}


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def audit_rank_zero_aa_bb_theorem_bridge(
    *,
    pseudo_selmer_container: dict[str, Any],
    t_tail_audit: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(pseudo_selmer_container):
        violations.append("pseudo_selmer_container_not_ready")
    if not _ready(t_tail_audit):
        violations.append("t_tail_audit_not_ready")
    if t_tail_audit.get("dimension_bound_update", {}).get("upper_bound") != "dim_F2 S~ <= 2":
        violations.append("s_tilde_bound_not_dim_le_2")
    if t_tail_audit.get("dimension_bound_update", {}).get("complete_selmer_bound_proved"):
        violations.append("input_overclaims_complete_selmer_bound")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl465-wl467",
        "pattern": "AA+BB",
        "bridge_summary": BRIDGE_SUMMARY,
        "object_boundary": OBJECT_BOUNDARY,
        "required_hypotheses": REQUIRED_HYPOTHESES,
        "formal_gaps": FORMAL_GAPS,
        "next_action": "stop_after_bridge_audit",
        "do_not_proceed_to": [
            "finite-ledger coverage",
            "all-lambda coverage",
            "family exclusion theorem",
        ],
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pseudo-selmer-container", type=Path, required=True)
    parser.add_argument("--t-tail-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_theorem_bridge(
        pseudo_selmer_container=load_json(args.pseudo_selmer_container),
        t_tail_audit=load_json(args.t_tail_audit),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB theorem bridge audit to {args.out}")
    print(f"status={audit['status']}")
    print(
        "s_tilde_is_valid_upper_bound_for_complete_selmer="
        f"{audit['bridge_summary']['s_tilde_is_valid_upper_bound_for_complete_selmer']}"
    )
    print(
        "complete_selmer_upper_bound_proved="
        f"{audit['bridge_summary']['complete_selmer_upper_bound_proved']}"
    )
    print(
        "theorem_candidate_promotable="
        f"{audit['bridge_summary']['theorem_candidate_promotable']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
