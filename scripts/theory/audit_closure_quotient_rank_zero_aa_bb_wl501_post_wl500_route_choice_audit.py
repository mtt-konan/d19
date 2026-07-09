#!/usr/bin/env python3
"""Choose the post-wl500 AA+BB route without executing the next gate."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl501 / post_wl500_route_choice_audit. It uses wl500 "
    "as input, observes that the two shell-5 u_5 M_tail supports have both "
    "been closed as ambient globally not soluble, evaluates the next route "
    "options, chooses the next narrow gate as executing the next finite "
    "M_tail shell from the existing wl498 plan, and stops before refreshing "
    "or executing that shell, testing new C_d solubility, applying wl491 to "
    "any new point, selecting a final obstruction candidate, running broad "
    "rank or Selmer diagnostics, advancing to wl502, using the old package-x "
    "S~ bridge, or claiming a complete Sel_2(E) upper bound, dim Sel_2(E)=2, "
    "rank zero, Sha[2]=0, or any family exclusion."
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


def _wl500_ready(wl500: dict[str, Any]) -> bool:
    summary = wl500.get("route_summary", {})
    return (
        wl500.get("status") == "ok"
        and wl500.get("ready") is True
        and wl500.get("lemma_id")
        == (
            "WL500_route_active_u5_M_tail_supports_through_ambient_C_d_"
            "solubility_then_wl491_filter"
        )
        and wl500.get("work_log") == "wl500"
        and wl500.get("input_work_logs") == ["wl491", "wl499"]
        and wl500.get("route_audit_built_here") is True
        and wl500.get("all_active_u5_entries_classified_here") is True
        and summary.get("active_u5_support_entry_count") == 2
        and summary.get("ambient_global_solubility_refuted_count") == 2
        and summary.get("ambient_global_solubility_still_deferred_count") == 0
        and summary.get("wl491_filter_applied_count") == 0
        and summary.get("aa_bb_admissible_count") == 0
        and wl500.get("candidate_selected_here") is False
        and wl500.get("new_m_tail_row_proved_here") is False
        and wl500.get("new_local_row_proved_here") is False
        and wl500.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl500.get("family_rank_or_selmer_diagnostics_run") is False
        and wl500.get("single_curve_diagnostics_run") is False
        and wl500.get("old_package_x_coordinate_collapse_used") is False
        and wl500.get("package_x_s_tilde_bridge_used") is False
        and wl500.get("advance_to_wl501") is False
        and not _claims_forbidden_bound(wl500)
    )


def _completed_shell_bound(wl500: dict[str, Any]) -> int:
    samples = [
        entry.get("sample", {})
        for entry in wl500.get("routed_active_u5_supports", [])
    ]
    bounds = [
        max(int(sample["A"]), int(sample["B"]))
        for sample in samples
        if "A" in sample and "B" in sample
    ]
    return max(bounds) if bounds else 0


def _post_wl500_route_state_summary(wl500: dict[str, Any]) -> dict[str, int]:
    summary = wl500["route_summary"]
    return {
        "shell5_active_u5_support_entry_count_from_wl500": summary[
            "active_u5_support_entry_count"
        ],
        "shell5_ambient_global_solubility_refuted_count_from_wl500": summary[
            "ambient_global_solubility_refuted_count"
        ],
        "shell5_ambient_global_solubility_still_deferred_count_after_wl500": summary[
            "ambient_global_solubility_still_deferred_count"
        ],
        "shell5_wl491_filter_applied_count_from_wl500": summary[
            "wl491_filter_applied_count"
        ],
        "aa_bb_admissible_count_after_wl500": summary["aa_bb_admissible_count"],
        "active_candidate_count_after_wl500": 0,
        "completed_finite_shell_bound_after_wl500": _completed_shell_bound(wl500),
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "execute_next_finite_M_tail_shell_from_wl498_plan": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl500 leaves no active shell-5 u_5 ambient-solubility gap, "
                "no AA+BB-admissible point, and no final obstruction "
                "candidate. The remaining controllable gap is still the "
                "parameter-dependent M_tail layer already structured by "
                "wl498, so the next narrow executable gate should be the next "
                "finite primitive shell under that plan."
            ),
        },
        "summarize_current_route_impact": {
            "decision": "defer_as_documentation_only",
            "reason": (
                "The current audit already records the route impact: u_3, "
                "bounded v_5, and shell-5 u_5 supports are disposed for this "
                "route. A standalone summary would not create a new support, "
                "prove a local row, or tighten a Selmer upper bound."
            ),
        },
        "return_to_theorem_level_local_row_work": {
            "decision": "defer_until_a_new_M_tail_gap_or_support_requires_it",
            "reason": (
                "Theorem-level local row work is still necessary eventually, "
                "but returning to it now would be broad and unanchored: there "
                "is no active admissible point, unresolved ambient cover, or "
                "identified row gap produced by wl500."
            ),
        },
        "select_final_obstruction_candidate": {
            "decision": "reject",
            "reason": (
                "All shell-5 u_5 ambient covers were refuted and no AA+BB-"
                "admissible point exists, so there is no final obstruction "
                "candidate to select here."
            ),
        },
    }


def _closed_ledger_do_not_reopen() -> list[str]:
    return [
        "u_3_processed_or_deprioritized_after_wl493_wl491",
        "bounded_v_5_entries_disposed_by_wl495_wl496",
        "shell5_u_5_entries_refuted_by_wl500",
    ]


def _selected_next_gate(wl500: dict[str, Any]) -> dict[str, Any]:
    completed_shell = _completed_shell_bound(wl500)
    return {
        "gate": "execute_next_finite_M_tail_shell_from_wl498_plan",
        "entered_here": False,
        "uses_existing_wl498_plan": True,
        "shell_bound_to_execute_later": completed_shell + 1,
        "new_shell_or_grid_refreshed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_here": False,
        "candidate_selected_here": False,
        "required_exclusions": _closed_ledger_do_not_reopen(),
        "required_route_for_future_new_support": [
            "M_tail_support",
            "ambient_C_d_global_solubility",
            "wl491_AA_BB_admissibility_filter",
            "admissible_or_not_admissible_or_refuted_ledger",
        ],
        "minimum_later_question": (
            "Execute the next finite primitive shell from wl498, with "
            f"max(A,B)={completed_shell + 1}, while preserving the duplicate "
            "support guard and stopping before ambient C_d solubility."
        ),
    }


def build_wl501_post_wl500_route_choice_audit(
    *,
    wl500: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl500_ready(wl500):
        violations.append("wl500_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl500 route state after shell-5 u_5 ambient refutations",
        "pattern": "AA+BB",
        "lemma_id": "WL501_post_wl500_route_choice_audit",
        "work_log": "wl501",
        "input_work_log": "wl500",
        "post_wl500_route_state_summary": (
            _post_wl500_route_state_summary(wl500) if status == "ok" else {}
        ),
        "closed_ledger_do_not_reopen": _closed_ledger_do_not_reopen(),
        "route_options": _route_options(),
        "selected_next_gate": (
            _selected_next_gate(wl500)
            if status == "ok"
            else {"gate": "not_selected_input_issues", "entered_here": False}
        ),
        "post_wl500_route_choice_made_here": status == "ok",
        "routing_audit_only": True,
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_shell_or_grid_refreshed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_to_new_point_here": False,
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
        "advance_to_wl502": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Execute the next finite M_tail shell from the wl498 plan. wl501 "
            "selects that gate only; it does not run a new shell, test a new "
            "ambient C_d cover, apply wl491 to a new point, or advance to "
            "wl502."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl500", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl501_post_wl500_route_choice_audit(wl500=load_json(args.wl500))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl501 post-wl500 route-choice audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(f"advance_to_wl502={audit['advance_to_wl502']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
