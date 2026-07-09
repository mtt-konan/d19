#!/usr/bin/env python3
"""Route the wl483 u_3 tail candidate into an obstruction workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl484 / u3_obstruction_route_entry_audit for the AA+BB "
    "complete d-coordinate route. It takes wl483 as input, records the explicit "
    "AA A=3, B=1 u_3 candidate datum d=(3,3,1), closes the current M_tail "
    "full-rank row-rescue path for now, and chooses the next obstruction "
    "workflow gate. It does not run broad rank or Selmer diagnostics, does not "
    "prove local or global solubility of C_d, does not prove an obstruction, "
    "does not prove a complete Sel_2(E) upper bound, and does not claim dim "
    "Sel_2(E)=2, rank zero, Sha[2]=0, or any family exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]
TARGET_SUPPORT = ["u_3"]
RELEVANT_PLACES = ["infinity", "2", "3", "13"]
FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl483_ready(wl483: dict[str, Any]) -> bool:
    decision = wl483.get("decision", {})
    return (
        wl483.get("status") == "ok"
        and wl483.get("ready") is True
        and wl483.get("lemma_id") == "WL483_local_Hilbert_row_decision_gate"
        and wl483.get("work_log") == "wl483"
        and wl483.get("input_work_log") == "wl482"
        and wl483.get("target_kernel", {}).get("support") == TARGET_SUPPORT
        and wl483.get("relevant_places") == RELEVANT_PLACES
        and decision.get("decision")
        == "no_justified_additional_local_hilbert_character_row_available"
        and decision.get("additional_local_hilbert_row_available") is False
        and decision.get("route_must_pivot_to_obstruction_handling") is True
        and wl483.get("old_package_x_coordinate_collapse_used") is False
        and not _claims_forbidden_bound(wl483)
    )


def _sample_with_curve_parameters(wl483: dict[str, Any]) -> dict[str, Any]:
    sample = dict(wl483.get("target_kernel", {}).get("sample", {}))
    L = int(sample["L"])
    T = int(sample["T"])
    sqrt_q = int(sample["sqrt_q"])
    sample["p"] = 8 * L * L - 2 * T * T
    sample["q"] = sqrt_q * sqrt_q
    return sample


def _obstruction_candidate_datum(wl483: dict[str, Any]) -> dict[str, Any]:
    sample = _sample_with_curve_parameters(wl483)
    return {
        "id": "AA_A3_B1_u_3_complete_d_candidate",
        "curve_model": "E_L: Y^2=(X+p)*(X^2-4*q)",
        "sample": sample,
        "coordinate_order": COORDINATE_ORDER,
        "support": list(TARGET_SUPPORT),
        "generator_family": "u_ell=(ell,ell,1) for odd ell | L",
        "active_prime": 3,
        "d_vector": {
            "d_minus_p": 3,
            "d_pos_2sqrt_q": 3,
            "d_neg_2sqrt_q": 1,
        },
        "d_vector_pattern": "(3,3,1)",
        "relevant_places": list(RELEVANT_PLACES),
        "source_work_logs": ["wl481", "wl482", "wl483"],
        "local_row_status_from_wl483": (
            "no justified additional local/Hilbert row currently kills u_3"
        ),
    }


def _m_tail_full_rank_rescue_status(wl483: dict[str, Any]) -> dict[str, Any]:
    change = wl483.get("wl481_wl482_change", {})
    return {
        "decision": "M_tail_full_rank_rescue_closed_for_now",
        "wl483_decision": wl483.get("decision", {}).get("decision"),
        "wl481_matrix_changed": change.get("wl481_matrix_changed"),
        "wl482_classification_changed": change.get("wl482_classification_changed"),
        "reason": (
            "wl483 found no currently justified additional local/Hilbert row "
            "at infinity, 2, 3, or 13 that kills u_3, so wl484 enters the "
            "obstruction workflow instead of trying another M_tail row rescue."
        ),
    }


def _next_obstruction_workflow_gate() -> dict[str, Any]:
    return {
        "available_gates": [
            "explicit_C_d_cover_local_global_solubility",
            "Cassels_Tate_or_second_descent",
            "L_value_or_analytic_rank_route",
        ],
        "selected_gate": "explicit_C_d_cover_local_global_solubility",
        "why_selected": (
            "The u_3 datum is already explicit in complete d-coordinates and wl483 "
            "closed the row-rescue path. The next narrow controllable question is "
            "whether the concrete C_d cover for d=(3,3,1) is locally soluble at the "
            "recorded places and globally soluble or obstructed."
        ),
        "entry_questions_for_next_workflow": [
            "Write the explicit C_d equations for d=(3,3,1) over AA A=3, B=1.",
            "Check local solubility only at the recorded relevant places first.",
            (
                "If locally soluble everywhere in scope, decide global solubility "
                "or record the precise remaining certificate gap."
            ),
        ],
        "deferred_gates": [
            {
                "gate": "Cassels_Tate_or_second_descent",
                "reason": (
                    "Defer until the explicit C_d cover is certified as the relevant "
                    "locally soluble Selmer-class representative or obstruction."
                ),
            },
            {
                "gate": "L_value_or_analytic_rank_route",
                "reason": (
                    "Defer because analytic-rank evidence would not by itself be the "
                    "minimal certificate for this concrete d-cover routing question."
                ),
            },
        ],
        "proof_started_here": False,
    }


def build_wl484_u3_obstruction_route_entry_audit(
    *, wl483: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl483_ready(wl483):
        violations.append("wl483_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl483 local/Hilbert row decision gate",
        "pattern": "AA+BB",
        "lemma_id": "WL484_u3_obstruction_route_entry_audit",
        "work_log": "wl484",
        "input_work_log": "wl483",
        "obstruction_candidate_datum": (
            _obstruction_candidate_datum(wl483) if status == "ok" else {}
        ),
        "m_tail_full_rank_rescue_status": (
            _m_tail_full_rank_rescue_status(wl483) if status == "ok" else {}
        ),
        "next_obstruction_workflow_gate": _next_obstruction_workflow_gate(),
        "routing_audit_only": True,
        "obstruction_proved_here": False,
        "explicit_c_d_cover_solved_here": False,
        "symbolic_rank_status": "M_tail_full_rank_rescue_closed_for_now",
        "computed_rank_status": "finite_sample_candidate_routed_only",
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl483", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl484_u3_obstruction_route_entry_audit(wl483=load_json(args.wl483))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl484 u_3 obstruction route entry audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['next_obstruction_workflow_gate']['selected_gate']}")
    print(
        "obstruction_proved_here="
        f"{audit['obstruction_proved_here']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
