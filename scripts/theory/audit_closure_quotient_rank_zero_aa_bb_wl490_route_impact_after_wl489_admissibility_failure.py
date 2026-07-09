#!/usr/bin/env python3
"""Record wl490 route impact after the wl489 admissibility failure."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl490 / route_impact_after_wl489_admissibility_failure "
    "for the explicit AA A=3,B=1 u_3 global C_d point. It uses wl489 as input, "
    "removes that point from the current obstruction-candidate ledger and from "
    "the admissible-point ledger, records it only as globally soluble but not "
    "AA+BB-admissible for this sample, and selects the next narrow route. It "
    "does not define the next filter, does not choose another M_tail/kernel "
    "candidate, does not run broad rank or Selmer diagnostics, does not use the "
    "old package-x S~ bridge, does not run single-curve diagnostics, does not "
    "prove a complete Sel_2(E) upper bound, and does not claim dim Sel_2(E)=2, "
    "rank zero, Sha[2]=0, full Mordell-Weil torsion, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

TARGET_CANDIDATE_ID = "AA_A3_B1_u_3_complete_d_candidate"
TARGET_D_VECTOR = {
    "d_minus_p": 3,
    "d_pos_2sqrt_q": 3,
    "d_neg_2sqrt_q": 1,
}


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl489_ready(wl489: dict[str, Any]) -> bool:
    point = wl489.get("explicit_global_point", {})
    verdict = wl489.get("wl489_verdict", {})
    common_source = wl489.get("common_source_constraint_audit", {})
    return (
        wl489.get("status") == "ok"
        and wl489.get("ready") is True
        and wl489.get("lemma_id")
        == "WL489_closure_pullback_common_source_constraints_for_global_C_d_point"
        and wl489.get("work_log") == "wl489"
        and wl489.get("input_work_log") == "wl488"
        and point.get("candidate_id") == TARGET_CANDIDATE_ID
        and point.get("complete_d_squareclass") == TARGET_D_VECTOR
        and verdict.get("status") == "proved_fails_for_this_explicit_point"
        and verdict.get("proved_satisfies_AA_BB_constraints") is False
        and verdict.get("proved_fails_AA_BB_constraints") is True
        and verdict.get("missing_pullback_data_gate_triggered") is False
        and common_source.get("bb_side", {}).get("product_is_square") is False
        and wl489.get("point_level_admissibility_decided_here") is True
        and wl489.get("old_package_x_coordinate_collapse_used") is False
        and wl489.get("package_x_s_tilde_bridge_used") is False
        and wl489.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl489.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl489)
    )


def _candidate_summary(wl489: dict[str, Any]) -> dict[str, Any]:
    point = wl489["explicit_global_point"]
    return {
        "candidate_id": point["candidate_id"],
        "d_vector": dict(point["complete_d_squareclass"]),
    }


def _ledger_update(wl489: dict[str, Any]) -> dict[str, Any]:
    candidate = _candidate_summary(wl489)
    return {
        "killed_candidate": {
            **candidate,
            "reason": (
                "wl489 proves this ambient global C_d point fails AA+BB "
                "common-source constraints."
            ),
        },
        "remove_from_current_obstruction_candidate_ledger": True,
        "remove_from_admissible_point_ledger": True,
        "current_obstruction_candidate_ledger_after_wl490": [],
        "admissible_point_ledger_after_wl490": [],
        "globally_soluble_but_not_aa_bb_admissible_ledger": [
            {
                **candidate,
                "wl489_status": wl489["wl489_verdict"]["status"],
            }
        ],
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "define_reusable_ambient_C_d_to_AA_BB_admissibility_filter": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl489 killed the first ambient global C_d point by "
                "AA+BB common-source constraints, so the next controllable "
                "unit is a reusable filter that every later ambient C_d point "
                "must pass before it enters the admissible ledger."
            ),
        },
        "return_to_M_tail_kernel_classification_for_another_candidate": {
            "decision": "defer",
            "reason": (
                "Allowed later, but choosing another candidate before a "
                "reusable admissibility filter would repeat the wl489 "
                "point-specific check and blur ambient solubility with "
                "AA+BB admissibility."
            ),
        },
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "define_reusable_ambient_C_d_to_AA_BB_admissibility_filter",
        "entered_here": False,
        "input_to_later_gate": [
            "wl489_pullback_values_N_4_M_0",
            "wl489_common_source_failure_on_BB_side",
            "complete_d_coordinate_class_(3,3,1)",
            "AA_BB_common_source_closure_equations",
        ],
        "minimum_later_question": (
            "Given an ambient global C_d point, decide whether its pullback "
            "satisfies the AA+BB common-source closure constraints before "
            "recording it as admissible."
        ),
    }


def build_wl490_route_impact_after_wl489_admissibility_failure(
    *, wl489: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl489_ready(wl489):
        violations.append("wl489_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl489 explicit u_3 AA+BB admissibility failure",
        "pattern": "AA+BB",
        "lemma_id": "WL490_route_impact_after_wl489_admissibility_failure",
        "work_log": "wl490",
        "input_work_log": "wl489",
        "ledger_update": _ledger_update(wl489) if status == "ok" else {},
        "route_options": _route_options(),
        "selected_next_gate": _selected_next_gate(),
        "routing_audit_only": True,
        "point_level_admissibility_decided_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "admissibility_filter_defined_here": False,
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
        "advance_to_wl491": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl489", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl490_route_impact_after_wl489_admissibility_failure(
        wl489=load_json(args.wl489)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl490 route-impact audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(f"advance_to_wl491={audit['advance_to_wl491']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
