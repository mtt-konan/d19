#!/usr/bin/env python3
"""Choose the post-wl496 AA+BB route without executing the next gate."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl497 / post_wl496_route_choice_audit. It uses the "
    "wl493-wl496 route state to observe that u_3 and the bounded refreshed "
    "v_5 supports have all been disposed in the current route ledger, chooses "
    "the next narrow gate as a structured M_tail diagnostic extension, and "
    "stops before refreshing a new grid, proving local rows, testing new "
    "ambient C_d solubility, selecting a final obstruction candidate, running "
    "broad rank or Selmer diagnostics, advancing to wl498, using the old "
    "package-x S~ bridge, or claiming a complete Sel_2(E) upper bound, "
    "dim Sel_2(E)=2, rank zero, Sha[2]=0, or any family exclusion."
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


def _base_ready(payload: dict[str, Any], *, work_log: str, lemma_id: str) -> bool:
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == work_log
        and payload.get("lemma_id") == lemma_id
        and payload.get("old_package_x_coordinate_collapse_used") is False
        and payload.get("package_x_s_tilde_bridge_used") is False
        and payload.get("broad_rank_or_selmer_diagnostics_run") is False
        and payload.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(payload)
    )


def _wl493_ready(wl493: dict[str, Any]) -> bool:
    summary = wl493.get("queue_summary", {})
    return (
        _base_ready(
            wl493,
            work_log="wl493",
            lemma_id="WL493_candidate_queue_from_existing_M_tail_diagnostics",
        )
        and wl493.get("candidate_queue_built_here") is True
        and summary.get("active_unprocessed_candidate_count") == 0
        and summary.get("deprioritized_or_excluded_candidate_count") == 1
        and wl493.get("candidate_selected_here") is False
        and wl493.get("new_m_tail_row_proved_here") is False
        and wl493.get("ambient_c_d_solubility_proved_for_new_candidate_here")
        is False
    )


def _wl494_ready(wl494: dict[str, Any]) -> bool:
    summary = wl494.get("sample_summary", {})
    return (
        _base_ready(
            wl494,
            work_log="wl494",
            lemma_id="WL494_extend_or_refresh_M_tail_diagnostics",
        )
        and wl494.get("diagnostic_refresh_built_here") is True
        and summary.get("active_new_support_entry_count") == 6
        and summary.get("processed_or_excluded_u3_entry_count") == 2
        and summary.get("unique_active_supports") == ["v_5"]
        and wl494.get("candidate_selected_here") is False
        and wl494.get("new_m_tail_row_proved_here") is False
        and wl494.get("ambient_c_d_solubility_proved_for_new_candidate_here")
        is False
        and wl494.get("aa_bb_admissibility_proved_for_new_candidate_here")
        is False
    )


def _wl495_ready(wl495: dict[str, Any]) -> bool:
    summary = wl495.get("route_summary", {})
    return (
        _base_ready(
            wl495,
            work_log="wl495",
            lemma_id=(
                "WL495_route_refreshed_support_through_ambient_C_d_"
                "solubility_then_wl491_filter"
            ),
        )
        and wl495.get("route_audit_built_here") is True
        and summary.get("active_refreshed_support_entry_count") == 6
        and summary.get("ambient_globally_soluble_count") == 4
        and summary.get("ambient_global_solubility_deferred_count") == 2
        and summary.get("wl491_filter_applied_count") == 4
        and summary.get("aa_bb_admissible_count") == 0
        and summary.get("aa_bb_not_admissible_count") == 4
        and wl495.get("candidate_selected_here") is False
        and wl495.get("new_m_tail_row_proved_here") is False
        and wl495.get("new_local_row_proved_here") is False
    )


def _wl496_ready(wl496: dict[str, Any]) -> bool:
    summary = wl496.get("resolution_summary", {})
    return (
        _base_ready(
            wl496,
            work_log="wl496",
            lemma_id=(
                "WL496_resolve_wl495_deferred_v5_ambient_C_d_global_"
                "solubility_ledgers"
            ),
        )
        and wl496.get("resolved_wl495_deferred_ledgers_here") is True
        and wl496.get("all_wl495_deferred_entries_resolved_here") is True
        and summary.get("wl495_deferred_entry_count") == 2
        and summary.get("ambient_global_solubility_refuted_count") == 2
        and summary.get("ambient_global_solubility_still_deferred_count") == 0
        and summary.get("wl491_filter_applied_count") == 0
        and summary.get("aa_bb_admissible_count") == 0
        and wl496.get("candidate_selected_here") is False
        and wl496.get("new_m_tail_row_proved_here") is False
        and wl496.get("new_local_row_proved_here") is False
        and wl496.get("advance_to_wl497") is False
    )


def _post_wl496_route_state_summary(
    *,
    wl493: dict[str, Any],
    wl494: dict[str, Any],
    wl495: dict[str, Any],
    wl496: dict[str, Any],
) -> dict[str, int]:
    wl493_summary = wl493["queue_summary"]
    wl494_summary = wl494["sample_summary"]
    wl495_summary = wl495["route_summary"]
    wl496_summary = wl496["resolution_summary"]
    aa_bb_admissible_count = (
        wl495_summary["aa_bb_admissible_count"]
        + wl496_summary["aa_bb_admissible_count"]
    )
    return {
        "u3_active_unprocessed_candidate_count_after_wl493": wl493_summary[
            "active_unprocessed_candidate_count"
        ],
        "u3_processed_or_deprioritized_count_after_wl493": wl493_summary[
            "deprioritized_or_excluded_candidate_count"
        ],
        "bounded_v5_active_support_entry_count_from_wl494": wl494_summary[
            "active_new_support_entry_count"
        ],
        "bounded_v5_routed_not_admissible_count_from_wl495": wl495_summary[
            "aa_bb_not_admissible_count"
        ],
        "bounded_v5_refuted_ambient_count_from_wl496": wl496_summary[
            "ambient_global_solubility_refuted_count"
        ],
        "bounded_v5_still_deferred_count_after_wl496": wl496_summary[
            "ambient_global_solubility_still_deferred_count"
        ],
        "aa_bb_admissible_count_after_wl496": aa_bb_admissible_count,
        "active_candidate_count_after_wl496": 0,
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "summarize_current_route_impact": {
            "decision": "defer_as_documentation_only",
            "reason": (
                "A route-impact summary is useful as context, but by itself "
                "would only restate that u_3 and bounded v_5 were disposed; it "
                "does not produce a new controllable support or shrink the "
                "Selmer upper-bound gap."
            ),
        },
        "return_to_theorem_level_local_row_work": {
            "decision": (
                "defer_until_a_structured_M_tail_gap_or_candidate_requires_it"
            ),
            "reason": (
                "The current finite route has no active admissible or "
                "unresolved support. Broad theorem-level local row work would "
                "be unscoped unless a structured M_tail diagnostic extension "
                "identifies which row or support is actually needed."
            ),
        },
        "structure_or_extend_M_tail_diagnostics": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "The complete d-coordinate route remains blocked at the "
                "parameter-dependent M_tail layer after u_3 and the bounded "
                "v_5 supports are disposed. The next controllable action is to "
                "structure the next M_tail diagnostic extension, explicitly "
                "excluding disposed supports and preserving the ambient C_d "
                "then wl491 route for any genuinely new support."
            ),
        },
        "select_final_obstruction_candidate": {
            "decision": "reject",
            "reason": (
                "No AA+BB-admissible point or unresolved active candidate "
                "exists after wl496, so there is no final obstruction "
                "candidate to select here."
            ),
        },
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "structure_next_M_tail_diagnostic_extension",
        "entered_here": False,
        "new_grid_refreshed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "candidate_selected_here": False,
        "required_exclusions": [
            "do_not_reenter_u_3",
            "do_not_reopen_bounded_v_5_entries_from_wl494_wl496",
        ],
        "required_route_for_future_new_support": [
            "M_tail_support",
            "ambient_C_d_global_solubility",
            "wl491_AA_BB_admissibility_filter",
            "admissible_or_not_admissible_or_refuted_ledger",
        ],
        "minimum_later_question": (
            "What structured, non-duplicating M_tail diagnostic extension can "
            "produce a genuinely new support or a precise row gap, while "
            "carrying forward the disposed u_3/v_5 ledger state?"
        ),
    }


def build_wl497_post_wl496_route_choice_audit(
    *,
    wl493: dict[str, Any],
    wl494: dict[str, Any],
    wl495: dict[str, Any],
    wl496: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl493_ready(wl493):
        violations.append("wl493_input_not_ready_or_not_scoped")
    if not _wl494_ready(wl494):
        violations.append("wl494_input_not_ready_or_not_scoped")
    if not _wl495_ready(wl495):
        violations.append("wl495_input_not_ready_or_not_scoped")
    if not _wl496_ready(wl496):
        violations.append("wl496_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl493-wl496 route state after disposed u_3 and bounded v_5",
        "pattern": "AA+BB",
        "lemma_id": "WL497_post_wl496_route_choice_audit",
        "work_log": "wl497",
        "input_work_logs": ["wl493", "wl494", "wl495", "wl496"],
        "post_wl496_route_state_summary": (
            _post_wl496_route_state_summary(
                wl493=wl493,
                wl494=wl494,
                wl495=wl495,
                wl496=wl496,
            )
            if status == "ok"
            else {}
        ),
        "route_options": _route_options(),
        "selected_next_gate": _selected_next_gate(),
        "post_wl496_route_choice_made_here": status == "ok",
        "routing_audit_only": True,
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_grid_refreshed_here": False,
        "new_c_d_solubility_tested_here": False,
        "aa_bb_admissibility_proved_for_new_candidate_here": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "family_rank_or_selmer_diagnostics_run": False,
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
        "advance_to_wl498": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Structure the next M_tail diagnostic extension without reusing "
            "the disposed u_3 or bounded v_5 ledgers; any future new support "
            "must still pass ambient C_d solubility before the wl491 filter."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl493", type=Path, required=True)
    parser.add_argument("--wl494", type=Path, required=True)
    parser.add_argument("--wl495", type=Path, required=True)
    parser.add_argument("--wl496", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl497_post_wl496_route_choice_audit(
        wl493=load_json(args.wl493),
        wl494=load_json(args.wl494),
        wl495=load_json(args.wl495),
        wl496=load_json(args.wl496),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl497 post-wl496 route-choice audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(f"advance_to_wl498={audit['advance_to_wl498']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
