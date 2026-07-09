#!/usr/bin/env python3
"""Choose the post-wl502 empty-shell AA+BB route without executing it."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl503 / post_wl502_empty_shell_route_choice_audit. It "
    "uses wl502 as input, observes that shell 6 produced no active M_tail "
    "kernel supports and no duplicate or processed support outputs, evaluates "
    "the next route options, chooses the next narrow gate as executing the "
    "next finite M_tail shell from the existing wl498 plan, and stops before "
    "executing shell 7, testing ambient C_d solubility, applying wl491, "
    "selecting a final obstruction candidate, proving local rows, running "
    "broad rank or Selmer diagnostics, advancing to wl504, using the old "
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

REQUIRED_EMPTY_SHELL6_SUMMARY = {
    "sample_count": 8,
    "full_rank_sample_count": 8,
    "kernel_sample_count": 0,
    "kernel_support_entry_count": 0,
    "active_new_support_entry_count": 0,
    "excluded_duplicate_or_processed_support_entry_count": 0,
    "unique_active_supports": [],
}

REQUIRED_CLOSED_LEDGER_EXCLUSIONS = [
    "u_3_processed_or_deprioritized_after_wl493_wl491",
    "bounded_v_5_entries_disposed_by_wl495_wl496",
    "shell5_u_5_entries_refuted_by_wl500",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl502_ready(wl502: dict[str, Any]) -> bool:
    scope = wl502.get("declared_extension_scope", {})
    return (
        wl502.get("status") == "ok"
        and wl502.get("ready") is True
        and wl502.get("lemma_id")
        == "WL502_execute_next_finite_M_tail_shell_from_wl498_plan"
        and wl502.get("work_log") == "wl502"
        and wl502.get("input_work_logs") == ["wl480", "wl501"]
        and scope.get("extension_unit") == "finite_primitive_shell"
        and scope.get("shell_axis") == "max(A,B)"
        and scope.get("shell_bound") == 6
        and scope.get("sides") == ["AA", "BB"]
        and scope.get("primitive_condition") == "gcd(A,B)=1"
        and scope.get("uses_wl498_duplicate_support_guard") is True
        and scope.get("uses_wl501_closed_ledger_exclusions") is True
        and wl502.get("closed_ledger_exclusions_applied")
        == REQUIRED_CLOSED_LEDGER_EXCLUSIONS
        and wl502.get("sample_summary") == REQUIRED_EMPTY_SHELL6_SUMMARY
        and wl502.get("active_new_kernel_supports") == []
        and wl502.get("excluded_duplicate_or_processed_supports") == []
        and wl502.get("m_tail_diagnostics_extended_here") is True
        and wl502.get("new_supports_computed_here") is True
        and wl502.get("candidate_selected_here") is False
        and wl502.get("new_m_tail_row_proved_here") is False
        and wl502.get("new_local_row_proved_here") is False
        and wl502.get("new_c_d_solubility_tested_here") is False
        and wl502.get("wl491_filter_applied_here") is False
        and wl502.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl502.get("family_rank_or_selmer_diagnostics_run") is False
        and wl502.get("single_curve_diagnostics_run") is False
        and wl502.get("old_package_x_coordinate_collapse_used") is False
        and wl502.get("package_x_s_tilde_bridge_used") is False
        and wl502.get("advance_to_wl503") is False
        and not _claims_forbidden_bound(wl502)
    )


def _completed_shell_bound(wl502: dict[str, Any]) -> int:
    return int(wl502.get("declared_extension_scope", {}).get("shell_bound", 0))


def _post_wl502_empty_shell_state_summary(wl502: dict[str, Any]) -> dict[str, int]:
    summary = wl502["sample_summary"]
    return {
        "completed_finite_shell_bound_after_wl502": _completed_shell_bound(wl502),
        "shell6_sample_count_from_wl502": summary["sample_count"],
        "shell6_full_rank_sample_count_from_wl502": summary[
            "full_rank_sample_count"
        ],
        "shell6_kernel_sample_count_from_wl502": summary["kernel_sample_count"],
        "shell6_active_new_support_entry_count_from_wl502": summary[
            "active_new_support_entry_count"
        ],
        "shell6_excluded_duplicate_or_processed_support_entry_count_from_wl502": (
            summary["excluded_duplicate_or_processed_support_entry_count"]
        ),
        "active_candidate_count_after_wl502": 0,
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "execute_next_finite_M_tail_shell_from_wl498_plan": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl502 leaves no active M_tail support to route and no "
                "duplicate or processed support to close. The remaining "
                "controllable diagnostic route is still the finite primitive "
                "shell axis already structured by wl498, so the next gate is "
                "to execute the next shell later while preserving the same "
                "duplicate-support guard."
            ),
        },
        "invent_shell6_ambient_C_d_solubility_task": {
            "decision": "reject",
            "reason": (
                "Shell 6 produced no kernel support, so there is no ambient "
                "C_d class to test and no wl491 filter input to construct."
            ),
        },
        "claim_uniform_M_tail_full_rank_from_shell6": {
            "decision": "reject",
            "reason": (
                "The eight full-rank shell-6 samples are diagnostic output "
                "for one finite shell only; they do not prove uniform M_tail "
                "full rank."
            ),
        },
        "select_final_obstruction_candidate": {
            "decision": "reject",
            "reason": (
                "No active support, ambient global point, or AA+BB-admissible "
                "point remains after wl502, so there is no final obstruction "
                "candidate to select here."
            ),
        },
        "return_to_theorem_level_local_row_work": {
            "decision": "defer_until_a_specific_row_gap_is_identified",
            "reason": (
                "Theorem-level local row work remains part of the larger "
                "Selmer route, but wl502 did not identify a new row gap. "
                "Entering that work here would be broader than this gate."
            ),
        },
    }


def _selected_next_gate(wl502: dict[str, Any]) -> dict[str, Any]:
    completed_shell = _completed_shell_bound(wl502)
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


def build_wl503_post_wl502_empty_shell_route_choice_audit(
    *,
    wl502: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl502_ready(wl502):
        violations.append("wl502_input_not_ready_empty_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl502 empty shell-6 M_tail diagnostic output",
        "pattern": "AA+BB",
        "lemma_id": "WL503_post_wl502_empty_shell_route_choice_audit",
        "work_log": "wl503",
        "input_work_log": "wl502",
        "post_wl502_empty_shell_state_summary": (
            _post_wl502_empty_shell_state_summary(wl502) if status == "ok" else {}
        ),
        "closed_ledger_do_not_reopen": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "route_options": _route_options(),
        "selected_next_gate": (
            _selected_next_gate(wl502)
            if status == "ok"
            else {"gate": "not_selected_input_issues", "entered_here": False}
        ),
        "post_wl502_route_choice_made_here": status == "ok",
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
        "advance_to_wl504": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Execute the next finite M_tail shell from the wl498 plan. wl503 "
            "selects that gate only; it does not run shell 7, test ambient "
            "C_d solubility, apply wl491, prove a local row, or claim uniform "
            "M_tail full rank."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl502", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl503_post_wl502_empty_shell_route_choice_audit(
        wl502=load_json(args.wl502)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl503 post-wl502 empty-shell route-choice audit to {args.out}")
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
