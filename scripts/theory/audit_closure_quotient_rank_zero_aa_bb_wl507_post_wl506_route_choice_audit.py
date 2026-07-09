#!/usr/bin/env python3
"""Choose the post-wl506 AA+BB route without executing shell 8."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl507 / post_wl506_route_choice_audit. It uses wl506 "
    "as input, observes that the shell-7 active/deferred ambient C_d ledgers "
    "are fully disposed, evaluates the next route options, chooses the next "
    "narrow gate as executing the next finite M_tail shell from the existing "
    "wl498 plan, and stops before executing shell 8, testing new ambient C_d "
    "solubility, applying wl491 to any new point, re-opening shell-7 routed "
    "or refuted ledgers, selecting a final obstruction candidate, proving "
    "local rows, running broad rank or Selmer diagnostics, advancing to "
    "wl508, using the old package-x S~ bridge, or claiming a complete "
    "Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform "
    "M_tail full rank, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

REQUIRED_WL506_SUMMARY = {
    "wl505_deferred_entry_count": 4,
    "explicitly_classified_entry_count": 4,
    "ambient_globally_soluble_count": 2,
    "ambient_global_solubility_refuted_count": 2,
    "ambient_global_solubility_still_deferred_count": 0,
    "wl491_filter_applied_count": 2,
    "aa_bb_admissible_count": 0,
    "aa_bb_not_admissible_count": 2,
    "aa_bb_missing_pullback_data_count": 0,
    "aa_bb_filter_not_applied_count": 2,
}

REQUIRED_CLOSED_LEDGER_EXCLUSIONS = [
    "u_3_processed_or_deprioritized_after_wl493_wl491",
    "bounded_v_5_entries_disposed_by_wl495_wl496",
    "shell5_u_5_entries_refuted_by_wl500",
    "shell6_empty_diagnostic_output_from_wl502",
    "shell7_active_not_admissible_ledgers_from_wl505",
    "shell7_processed_u3_exclusions_from_wl505",
    "shell7_w5_deferred_ledgers_refuted_by_wl506",
    "shell7_u7_w37_deferred_ledgers_not_admissible_by_wl506",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl506_ready(wl506: dict[str, Any]) -> bool:
    return (
        wl506.get("status") == "ok"
        and wl506.get("ready") is True
        and wl506.get("lemma_id")
        == "WL506_resolve_shell7_deferred_ambient_C_d_global_solubility_ledgers"
        and wl506.get("work_log") == "wl506"
        and wl506.get("input_work_logs") == ["wl491", "wl505"]
        and wl506.get("resolution_summary") == REQUIRED_WL506_SUMMARY
        and wl506.get("resolved_wl505_deferred_ledgers_here") is True
        and wl506.get("all_wl505_deferred_entries_resolved_here") is True
        and wl506.get("shell7_globally_soluble_not_admissible_reopened_count") == 0
        and wl506.get("shell7_processed_u3_exclusions_reopened_count") == 0
        and wl506.get("candidate_selected_here") is False
        and wl506.get("new_m_tail_row_proved_here") is False
        and wl506.get("new_local_row_proved_here") is False
        and wl506.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl506.get("family_rank_or_selmer_diagnostics_run") is False
        and wl506.get("single_curve_diagnostics_run") is False
        and wl506.get("old_package_x_coordinate_collapse_used") is False
        and wl506.get("package_x_s_tilde_bridge_used") is False
        and wl506.get("advance_to_wl507") is False
        and not _claims_forbidden_bound(wl506)
    )


def _completed_shell_bound(wl506: dict[str, Any]) -> int:
    samples = [
        entry.get("sample", {})
        for entry in wl506.get("resolved_deferred_entries", [])
    ]
    bounds = [
        max(int(sample["A"]), int(sample["B"]))
        for sample in samples
        if "A" in sample and "B" in sample
    ]
    return max(bounds) if bounds else 0


def _post_wl506_route_state_summary(wl506: dict[str, Any]) -> dict[str, int]:
    summary = wl506["resolution_summary"]
    return {
        "completed_finite_shell_bound_after_wl506": _completed_shell_bound(wl506),
        "shell7_deferred_entry_count_from_wl506": summary[
            "wl505_deferred_entry_count"
        ],
        "shell7_deferred_entries_resolved_by_wl506": summary[
            "explicitly_classified_entry_count"
        ],
        "shell7_ambient_global_solubility_refuted_count_from_wl506": summary[
            "ambient_global_solubility_refuted_count"
        ],
        "shell7_globally_soluble_not_admissible_count_from_wl506": summary[
            "aa_bb_not_admissible_count"
        ],
        "shell7_ambient_global_solubility_still_deferred_count_after_wl506": summary[
            "ambient_global_solubility_still_deferred_count"
        ],
        "shell7_wl491_filter_applied_count_from_wl506": summary[
            "wl491_filter_applied_count"
        ],
        "aa_bb_admissible_count_after_wl506": summary["aa_bb_admissible_count"],
        "active_candidate_count_after_wl506": 0,
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "execute_next_finite_M_tail_shell_from_wl498_plan": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl506 leaves no unresolved shell-7 ambient-solubility "
                "ledger, no AA+BB-admissible point, and no final obstruction "
                "candidate. The remaining controllable diagnostic route is "
                "still the finite primitive shell axis already structured by "
                "wl498, so the next narrow executable gate should be the next "
                "finite shell under that plan."
            ),
        },
        "reopen_shell7_ambient_ledgers": {
            "decision": "reject",
            "reason": (
                "The shell-7 active/deferred ledgers are already routed: "
                "eight are globally soluble but not AA+BB-admissible from "
                "wl505, two pure u_3 entries are processed exclusions, two "
                "w_5 deferred entries are refuted by wl506, and two u_7+w_37 "
                "entries are globally soluble but not AA+BB-admissible by "
                "wl506."
            ),
        },
        "select_final_obstruction_candidate": {
            "decision": "reject",
            "reason": (
                "No shell-7 entry is AA+BB-admissible and no unresolved "
                "ambient C_d ledger remains, so there is no final obstruction "
                "candidate to select here."
            ),
        },
        "return_to_theorem_level_local_row_work": {
            "decision": "defer_until_a_new_M_tail_gap_or_support_requires_it",
            "reason": (
                "Theorem-level local row work remains part of the larger "
                "Selmer route, but wl506 did not identify a new row gap. "
                "Entering that work here would be broader than this gate."
            ),
        },
    }


def _selected_next_gate(wl506: dict[str, Any]) -> dict[str, Any]:
    completed_shell = _completed_shell_bound(wl506)
    return {
        "gate": "execute_next_finite_M_tail_shell_from_wl498_plan",
        "entered_here": False,
        "uses_existing_wl498_plan": True,
        "shell_bound_to_execute_later": completed_shell + 1,
        "preserve_wl498_duplicate_support_guard": True,
        "new_shell_or_grid_refreshed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_here": False,
        "candidate_selected_here": False,
        "required_exclusions": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
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


def build_wl507_post_wl506_route_choice_audit(
    *,
    wl506: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl506_ready(wl506):
        violations.append("wl506_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl506 closed shell-7 ambient C_d route state",
        "pattern": "AA+BB",
        "lemma_id": "WL507_post_wl506_route_choice_audit",
        "work_log": "wl507",
        "input_work_log": "wl506",
        "post_wl506_route_state_summary": (
            _post_wl506_route_state_summary(wl506) if status == "ok" else {}
        ),
        "closed_ledger_do_not_reopen": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "route_options": _route_options(),
        "selected_next_gate": (
            _selected_next_gate(wl506)
            if status == "ok"
            else {"gate": "not_selected_input_issues", "entered_here": False}
        ),
        "post_wl506_route_choice_made_here": status == "ok",
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
        "uniform_m_tail_full_rank_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "search_count_used_as_progress": False,
        "advance_to_wl508": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Execute the next finite M_tail shell from the wl498 plan. wl507 "
            "selects that gate only; it does not run shell 8, test a new "
            "ambient C_d cover, apply wl491 to a new point, re-open shell-7 "
            "ledgers, or advance to wl508."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl506", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl507_post_wl506_route_choice_audit(wl506=load_json(args.wl506))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl507 post-wl506 route-choice audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(
        "shell_bound_to_execute_later="
        f"{audit['selected_next_gate'].get('shell_bound_to_execute_later')}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
