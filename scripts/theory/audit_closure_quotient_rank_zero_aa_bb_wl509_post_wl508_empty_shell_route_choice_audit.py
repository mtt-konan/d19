#!/usr/bin/env python3
"""Choose the post-wl508 empty-active-shell AA+BB route without executing it."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl509 / post_wl508_empty_shell_route_choice_audit. It "
    "uses wl508 as input, observes that shell 8 produced no active M_tail "
    "kernel supports after the two pure u_3 processed exclusions, evaluates "
    "the next route options, chooses the next narrow gate as executing the "
    "next finite M_tail shell from the existing wl498 plan, and stops before "
    "executing shell 9, testing ambient C_d solubility, applying wl491, "
    "selecting a final obstruction candidate, proving local rows, running "
    "broad rank or Selmer diagnostics, advancing to wl510, using the old "
    "package-x S~ bridge, or claiming a complete Sel_2(E) upper bound, dim "
    "Sel_2(E)=2, rank zero, Sha[2]=0, uniform M_tail full rank, or any "
    "family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

REQUIRED_EMPTY_ACTIVE_SHELL8_SUMMARY = {
    "sample_count": 16,
    "full_rank_sample_count": 14,
    "kernel_sample_count": 2,
    "kernel_support_entry_count": 2,
    "active_new_support_entry_count": 0,
    "excluded_duplicate_or_processed_support_entry_count": 2,
    "unique_active_supports": [],
}

REQUIRED_WL508_CLOSED_LEDGER_EXCLUSIONS = [
    "u_3_processed_or_deprioritized_after_wl493_wl491",
    "bounded_v_5_entries_disposed_by_wl495_wl496",
    "shell5_u_5_entries_refuted_by_wl500",
    "shell6_empty_diagnostic_output_from_wl502",
    "shell7_active_not_admissible_ledgers_from_wl505",
    "shell7_processed_u3_exclusions_from_wl505",
    "shell7_w5_deferred_ledgers_refuted_by_wl506",
    "shell7_u7_w37_deferred_ledgers_not_admissible_by_wl506",
]

REQUIRED_CLOSED_LEDGER_EXCLUSIONS = [
    *REQUIRED_WL508_CLOSED_LEDGER_EXCLUSIONS,
    "shell8_empty_active_diagnostic_output_from_wl508",
    "shell8_processed_u3_exclusions_from_wl508",
]

REQUIRED_SHELL8_PROCESSED_CANDIDATE_IDS = [
    "AA_A3_B8_u_3_m_tail_shell8_candidate",
    "BB_A8_B3_u_3_m_tail_shell8_candidate",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl508_ready(wl508: dict[str, Any]) -> bool:
    scope = wl508.get("declared_extension_scope", {})
    excluded_ids = [
        entry.get("candidate_id")
        for entry in wl508.get("excluded_duplicate_or_processed_supports", [])
    ]
    return (
        wl508.get("status") == "ok"
        and wl508.get("ready") is True
        and wl508.get("lemma_id")
        == "WL508_execute_next_finite_M_tail_shell_from_wl498_plan"
        and wl508.get("work_log") == "wl508"
        and wl508.get("input_work_logs") == ["wl480", "wl507"]
        and scope.get("extension_unit") == "finite_primitive_shell"
        and scope.get("shell_axis") == "max(A,B)"
        and scope.get("shell_bound") == 8
        and scope.get("sides") == ["AA", "BB"]
        and scope.get("primitive_condition") == "gcd(A,B)=1"
        and scope.get("uses_wl498_duplicate_support_guard") is True
        and scope.get("uses_wl507_closed_ledger_exclusions") is True
        and wl508.get("closed_ledger_exclusions_applied")
        == REQUIRED_WL508_CLOSED_LEDGER_EXCLUSIONS
        and wl508.get("sample_summary") == REQUIRED_EMPTY_ACTIVE_SHELL8_SUMMARY
        and wl508.get("active_new_kernel_supports") == []
        and excluded_ids == REQUIRED_SHELL8_PROCESSED_CANDIDATE_IDS
        and wl508.get("m_tail_diagnostics_extended_here") is True
        and wl508.get("new_supports_computed_here") is True
        and wl508.get("candidate_selected_here") is False
        and wl508.get("new_m_tail_or_kernel_candidate_selected_here") is False
        and wl508.get("new_m_tail_row_proved_here") is False
        and wl508.get("new_local_row_proved_here") is False
        and wl508.get("new_c_d_solubility_tested_here") is False
        and wl508.get("wl491_filter_applied_here") is False
        and wl508.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl508.get("family_rank_or_selmer_diagnostics_run") is False
        and wl508.get("single_curve_diagnostics_run") is False
        and wl508.get("old_package_x_coordinate_collapse_used") is False
        and wl508.get("package_x_s_tilde_bridge_used") is False
        and wl508.get("advance_to_wl509") is False
        and not _claims_forbidden_bound(wl508)
    )


def _completed_shell_bound(wl508: dict[str, Any]) -> int:
    return int(wl508.get("declared_extension_scope", {}).get("shell_bound", 0))


def _post_wl508_empty_shell_state_summary(wl508: dict[str, Any]) -> dict[str, int]:
    summary = wl508["sample_summary"]
    return {
        "completed_finite_shell_bound_after_wl508": _completed_shell_bound(wl508),
        "shell8_sample_count_from_wl508": summary["sample_count"],
        "shell8_full_rank_sample_count_from_wl508": summary[
            "full_rank_sample_count"
        ],
        "shell8_kernel_sample_count_from_wl508": summary["kernel_sample_count"],
        "shell8_kernel_support_entry_count_from_wl508": summary[
            "kernel_support_entry_count"
        ],
        "shell8_active_new_support_entry_count_from_wl508": summary[
            "active_new_support_entry_count"
        ],
        "shell8_excluded_duplicate_or_processed_support_entry_count_from_wl508": (
            summary["excluded_duplicate_or_processed_support_entry_count"]
        ),
        "active_candidate_count_after_wl508": 0,
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "execute_next_finite_M_tail_shell_from_wl498_plan": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl508 leaves no active M_tail support to route after the two "
                "pure u_3 processed exclusions. The remaining controllable "
                "diagnostic route is still the finite primitive shell axis "
                "already structured by wl498, so the next gate is to execute "
                "the next shell later while preserving all closed-ledger "
                "exclusions through wl508."
            ),
        },
        "invent_shell8_ambient_C_d_solubility_task": {
            "decision": "reject",
            "reason": (
                "Shell 8 has no active M_tail support. The two kernel outputs "
                "are processed pure u_3 repeats, so there is no new ambient "
                "C_d class to test and no new wl491 filter input."
            ),
        },
        "reopen_shell8_processed_u3_exclusions": {
            "decision": "reject",
            "reason": (
                "The shell-8 kernel outputs are exactly the already processed "
                "u_3 support family. Re-opening them would duplicate the "
                "wl493/wl491 u_3 ledger rather than shrink a theorem gap."
            ),
        },
        "claim_uniform_M_tail_full_rank_from_shell8": {
            "decision": "reject",
            "reason": (
                "The 14 full-rank shell-8 samples and empty active queue are "
                "finite diagnostic output only; they do not prove uniform "
                "M_tail full rank."
            ),
        },
        "select_final_obstruction_candidate": {
            "decision": "reject",
            "reason": (
                "No active support, ambient global point, or AA+BB-admissible "
                "point remains after wl508, so there is no final obstruction "
                "candidate to select here."
            ),
        },
        "return_to_theorem_level_local_row_work": {
            "decision": "defer_until_a_specific_row_gap_is_identified",
            "reason": (
                "Theorem-level local row work remains part of the larger "
                "Selmer route, but wl508 did not identify a new row gap. "
                "Entering that work here would be broader than this gate."
            ),
        },
    }


def _selected_next_gate(wl508: dict[str, Any]) -> dict[str, Any]:
    completed_shell = _completed_shell_bound(wl508)
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


def build_wl509_post_wl508_empty_shell_route_choice_audit(
    *,
    wl508: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl508_ready(wl508):
        violations.append("wl508_input_not_ready_empty_active_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl508 empty-active shell-8 M_tail diagnostic output",
        "pattern": "AA+BB",
        "lemma_id": "WL509_post_wl508_empty_shell_route_choice_audit",
        "work_log": "wl509",
        "input_work_log": "wl508",
        "post_wl508_empty_shell_state_summary": (
            _post_wl508_empty_shell_state_summary(wl508) if status == "ok" else {}
        ),
        "closed_ledger_do_not_reopen": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "route_options": _route_options(),
        "selected_next_gate": (
            _selected_next_gate(wl508)
            if status == "ok"
            else {"gate": "not_selected_input_issues", "entered_here": False}
        ),
        "post_wl508_route_choice_made_here": status == "ok",
        "routing_audit_only": True,
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_shell_or_grid_refreshed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
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
        "advance_to_selected_next_gate": False,
        "advance_to_wl510": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Execute the next finite M_tail shell from the wl498 plan. wl509 "
            "selects that gate only; it does not run shell 9, test ambient "
            "C_d solubility, apply wl491, prove a local row, re-open shell-8 "
            "processed u_3 exclusions, or claim uniform M_tail full rank."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl508", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl509_post_wl508_empty_shell_route_choice_audit(
        wl508=load_json(args.wl508)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl509 post-wl508 route-choice audit to {args.out}")
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
