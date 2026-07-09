#!/usr/bin/env python3
"""Select the next complete d-coordinate route after the wl487 u_3 point."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl488 / select_next_complete_d_coordinate_route_after_"
    "u3_global_point for the AA+BB complete d-coordinate route. It takes wl487 "
    "as input, records what the globally soluble non-baseline u_3 point changes, "
    "and selects the next narrow route gate. It does not enter that gate, does "
    "not run broad rank or Selmer diagnostics, does not use the old package-x "
    "S~ bridge, does not run single-curve diagnostics, does not prove a complete "
    "Sel_2(E) upper bound, and does not claim dim Sel_2(E)=2, rank zero, "
    "Sha[2]=0, full Mordell-Weil torsion, or any family exclusion."
)

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


def _wl487_ready(wl487: dict[str, Any]) -> bool:
    route_impact = wl487.get("route_impact", {})
    next_gate = wl487.get("next_narrow_gate", {})
    refutation_scope = wl487.get("refutation_scope", {})
    point = wl487.get("global_point_classification", {})
    point_d = point.get("complete_d_squareclass", {}).get("representative", {})
    torsion_compare = point.get("visible_two_torsion_baseline_comparison", {})
    return (
        wl487.get("status") == "ok"
        and wl487.get("ready") is True
        and wl487.get("lemma_id") == "WL487_route_impact_of_global_point"
        and wl487.get("work_log") == "wl487"
        and wl487.get("input_work_log") == "wl486"
        and refutation_scope.get("candidate_id")
        == "AA_A3_B1_u_3_complete_d_candidate"
        and refutation_scope.get("refuted_interpretation")
        == "this_specific_u3_as_locally_soluble_globally_pointless_obstruction"
        and refutation_scope.get("refuted_here") is True
        and point.get("classification")
        == "non_torsion_candidate_not_visible_two_torsion_baseline"
        and point_d == {"d_minus_p": 3, "d_pos_2sqrt_q": 3, "d_neg_2sqrt_q": 1}
        and torsion_compare.get("matches_visible_two_torsion_baseline") is False
        and route_impact.get("m_tail_status_after_global_point")
        == "u3_no_longer_available_as_global_obstruction_candidate"
        and route_impact.get("m_tail_full_rank_rescue_reopened_here") is False
        and route_impact.get("new_local_or_hilbert_row_found_here") is False
        and next_gate.get("gate")
        == "select_next_complete_d_coordinate_route_after_u3_global_point"
        and next_gate.get("entered_here") is False
        and wl487.get("old_package_x_coordinate_collapse_used") is False
        and wl487.get("broad_rank_or_selmer_diagnostics_run") is False
        and not _claims_forbidden_bound(wl487)
    )


def _u3_global_point_impact(wl487: dict[str, Any]) -> dict[str, Any]:
    refutation_scope = wl487["refutation_scope"]
    point = wl487["global_point_classification"]
    return {
        "candidate_id": refutation_scope["candidate_id"],
        "d_vector": dict(refutation_scope["d_vector"]),
        "point_classification": point["classification"],
        "changes": [
            "remove_u3_from_current_global_obstruction_candidate_ledger",
            "record_u3_as_globally_soluble_complete_d_coordinate_class_for_this_sample",
            "promote_the_next_question_from_local_obstruction_to_AA_BB_admissibility",
        ],
        "does_not_change": [
            "M_tail_uniform_full_rank_missing_remains_unproved",
            "no_new_local_or_hilbert_row_is_added",
            "visible_torsion_baseline_is_not_enlarged_here",
            "no_complete_selmer_upper_bound_or_rank_zero_conclusion_is_proved",
        ],
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "inspect_AA_BB_closure_pullback_common_source_constraints": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "The failed u3 obstruction attempt produced a global "
                "non-baseline C_d point, so the next controllable question is "
                "whether such a point is admissible for the AA+BB common source "
                "and closure/pullback constraints."
            ),
        },
        "pick_another_M_tail_or_kernel_candidate": {
            "decision": "defer",
            "reason": (
                "wl487 did not reopen the M_tail full-rank rescue path or add a "
                "new row; moving to another kernel candidate would not explain "
                "what the global u3 point means."
            ),
        },
        "run_another_minimal_complete_C_d_obstruction_test": {
            "decision": "defer",
            "reason": (
                "Another obstruction test is allowed later, but first the route "
                "must separate globally soluble C_d classes that are AA+BB "
                "admissible from classes that only live on the ambient E_L."
            ),
        },
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "AA_BB_closure_pullback_common_source_constraints_for_global_C_d_point",
        "entered_here": False,
        "input_to_later_gate": [
            "wl487_u3_global_point_classification",
            "complete_d_coordinate_class_(3,3,1)",
            "AA_A3_B1_common_source_and_closure_equations",
        ],
        "minimum_later_question": (
            "Does the wl486/wl487 global point pull back to the AA+BB common "
            "source/closure constraints, or is it only an ambient E_L point?"
        ),
    }


def build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point(
    *, wl487: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl487_ready(wl487):
        violations.append("wl487_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl487 route impact of the global u_3 C_d point",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL488_select_next_complete_d_coordinate_route_after_u3_global_point"
        ),
        "work_log": "wl488",
        "input_work_log": "wl487",
        "u3_global_point_impact": (
            _u3_global_point_impact(wl487) if status == "ok" else {}
        ),
        "route_options": _route_options(),
        "selected_next_gate": _selected_next_gate(),
        "routing_audit_only": True,
        "m_tail_full_rank_rescue_reopened_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_complete_c_d_obstruction_test_selected_here": False,
        "closure_pullback_common_source_gate_selected_here": status == "ok",
        "broad_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "search_count_used_as_progress": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl487", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl488_select_next_complete_d_coordinate_route_after_u3_global_point(
        wl487=load_json(args.wl487)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl488 next-route audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(
        "broad_rank_or_selmer_diagnostics_run="
        f"{audit['broad_rank_or_selmer_diagnostics_run']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
