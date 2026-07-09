#!/usr/bin/env python3
"""Choose the post-wl514 AA+BB route without entering the chosen gate."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl515 / post_wl514_route_choice_audit. It uses wl514 "
    "as input, observes that all shell-9 ambient C_d deferred ledgers have "
    "now been classified, preserves the four wl511 globally soluble but not "
    "AA+BB-admissible shell-9 ledgers, the two wl512 v_13 refutations, and "
    "the two wl514 u_7 refutations, evaluates the next route options, "
    "chooses the next narrow gate as executing the next finite M_tail shell "
    "from the existing wl498 plan, and stops before executing shell 10, "
    "testing ambient C_d solubility, applying wl491, re-opening any closed "
    "shell-9 ledger, selecting a final obstruction candidate, pivoting to a "
    "proof-level gate without a specific proof gap, running broad rank or "
    "Selmer diagnostics, advancing to wl516, using the old package-x S~ "
    "bridge, or claiming a complete Sel_2(E) upper bound, dim Sel_2(E)=2, "
    "rank zero, Sha[2]=0, uniform M_tail full rank, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

REQUIRED_WL514_SUMMARY = {
    "wl513_remaining_deferred_candidate_count": 2,
    "shared_cover_count_resolved_here": 1,
    "classified_candidate_entry_count": 2,
    "ambient_globally_soluble_count": 0,
    "ambient_global_solubility_refuted_count": 2,
    "exhaustive_no_lift_certificate_count": 1,
    "wl491_filter_applied_count": 0,
    "aa_bb_admissible_count": 0,
    "aa_bb_filter_not_applied_count": 2,
}

REQUIRED_WL514_RESOLVED_IDS = [
    "AA_A7_B9_u_7_m_tail_shell9_candidate",
    "BB_A9_B7_u_7_m_tail_shell9_candidate",
]

REQUIRED_WL514_SHARED_COVER = {
    "L": 7,
    "T": 16,
    "d_vector": {
        "d_minus_p": 7,
        "d_pos_2sqrt_q": 7,
        "d_neg_2sqrt_q": 1,
    },
    "elliptic_curve_model": "V^2 = (X + 120)*(X - 904)*(X + 904)",
}

REQUIRED_WL514_CLOSED_LEDGER_EXCLUSIONS = [
    "u_3_processed_or_deprioritized_after_wl493_wl491",
    "bounded_v_5_entries_disposed_by_wl495_wl496",
    "shell5_u_5_entries_refuted_by_wl500",
    "shell6_empty_diagnostic_output_from_wl502",
    "shell7_entries_disposed_by_wl505_wl506",
    "shell8_pure_u_3_processed_exclusions_from_wl508",
    "shell9_globally_soluble_not_admissible_ledgers_from_wl511",
    "shell9_v_13_deferred_ledgers_refuted_by_wl512",
]

REQUIRED_CLOSED_LEDGER_EXCLUSIONS = [
    *REQUIRED_WL514_CLOSED_LEDGER_EXCLUSIONS,
    "shell9_u_7_deferred_ledgers_refuted_by_wl514",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl514_ready(wl514: dict[str, Any]) -> bool:
    return (
        wl514.get("status") == "ok"
        and wl514.get("ready") is True
        and wl514.get("lemma_id")
        == "WL514_resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledger"
        and wl514.get("work_log") == "wl514"
        and wl514.get("input_work_log") == "wl513"
        and wl514.get("resolved_remaining_shell9_u7_ledger_here") is True
        and wl514.get("resolution_summary") == REQUIRED_WL514_SUMMARY
        and wl514.get("resolved_candidate_ids") == REQUIRED_WL514_RESOLVED_IDS
        and wl514.get("resolved_shared_cover") == REQUIRED_WL514_SHARED_COVER
        and wl514.get("closed_ledger_do_not_reopen")
        == REQUIRED_WL514_CLOSED_LEDGER_EXCLUSIONS
        and wl514.get("shell9_not_admissible_ledgers_reopened_count") == 0
        and wl514.get("shell9_v13_refuted_ledgers_reopened_count") == 0
        and wl514.get("closed_ledgers_reopened_count") == 0
        and wl514.get("wl491_filter_applied_to_new_point_here") is False
        and wl514.get("candidate_selected_here") is False
        and wl514.get("post_wl514_route_choice_made_here") is False
        and wl514.get("new_m_tail_or_kernel_candidate_selected_here") is False
        and wl514.get("new_m_tail_row_proved_here") is False
        and wl514.get("new_local_row_proved_here") is False
        and wl514.get("new_shell_or_grid_refreshed_here") is False
        and wl514.get("m_tail_diagnostics_extended_here") is False
        and wl514.get("new_supports_computed_here") is False
        and wl514.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl514.get("family_rank_or_selmer_diagnostics_run") is False
        and wl514.get("single_curve_diagnostics_run") is False
        and wl514.get("old_package_x_coordinate_collapse_used") is False
        and wl514.get("package_x_s_tilde_bridge_used") is False
        and wl514.get("shell10_executed_here") is False
        and wl514.get("advance_to_wl515") is False
        and not _claims_forbidden_bound(wl514)
    )


def _post_wl514_route_state_summary() -> dict[str, int]:
    return {
        "wl511_globally_soluble_not_admissible_count": 4,
        "wl512_v13_refuted_count": 2,
        "wl514_u7_refuted_count": 2,
        "shell9_remaining_deferred_count_after_wl514": 0,
        "shell9_aa_bb_admissible_count_after_wl514": 0,
        "active_candidate_count_after_wl514": 0,
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "execute_next_finite_M_tail_shell_from_wl498_plan": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl514 closes the last shell-9 deferred ambient C_d ledger, "
                "and shell 9 leaves no AA+BB-admissible or deferred active "
                "candidate. The existing controllable diagnostic route is "
                "therefore to continue the finite primitive shell axis "
                "already structured by wl498, preserving all closed-ledger "
                "exclusions and stopping the future shell execution before "
                "ambient C_d solubility."
            ),
        },
        "pivot_to_proof_level_route_choice_now": {
            "decision": "reject_without_specific_proof_gap",
            "reason": (
                "A proof-level pivot would need a named local-row, Selmer, "
                "or descent-object gap. wl514 only closes the remaining "
                "shell-9 ambient deferred ledgers; it does not identify a "
                "new theorem-level row obligation or prove a Selmer upper "
                "bound. Entering proof-level work here would be broader than "
                "the next narrow gate."
            ),
        },
        "reopen_closed_shell9_ledgers": {
            "decision": "reject",
            "reason": (
                "The four wl511 globally soluble but not AA+BB-admissible "
                "shell-9 ledgers, the two wl512 v_13 refutations, and the two "
                "wl514 u_7 refutations are closed for the current route."
            ),
        },
        "select_final_obstruction_candidate": {
            "decision": "reject",
            "reason": (
                "After wl514, shell 9 has no remaining deferred ledger and "
                "no AA+BB-admissible ambient point. There is no final "
                "obstruction candidate to select."
            ),
        },
        "apply_wl491_to_refuted_or_not_admissible_ledgers": {
            "decision": "reject",
            "reason": (
                "wl491 is only for established ambient C_d global points. It "
                "must not be applied to the wl512 or wl514 refuted covers, "
                "and the wl511 globally soluble points already failed the "
                "filter."
            ),
        },
        "claim_uniform_M_tail_full_rank_from_shell9": {
            "decision": "reject",
            "reason": (
                "The shell-9 classifications are finite diagnostic ledger "
                "output. They do not prove uniform M_tail full rank or any "
                "complete Selmer upper bound."
            ),
        },
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "execute_next_finite_M_tail_shell_from_wl498_plan",
        "entered_here": False,
        "uses_existing_wl498_plan": True,
        "shell_bound_to_execute_later": 10,
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
            "max(A,B)=10, while preserving every closed ledger through wl515 "
            "and stopping before ambient C_d solubility."
        ),
    }


def build_wl515_post_wl514_route_choice_audit(
    *,
    wl514: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl514_ready(wl514):
        violations.append("wl514_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl514 closed shell-9 deferred ambient C_d ledger state",
        "pattern": "AA+BB",
        "lemma_id": "WL515_post_wl514_route_choice_audit",
        "work_log": "wl515",
        "input_work_log": "wl514",
        "post_wl514_route_state_summary": (
            _post_wl514_route_state_summary() if status == "ok" else {}
        ),
        "closed_ledger_do_not_reopen": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "route_options": _route_options(),
        "selected_next_gate": (
            _selected_next_gate()
            if status == "ok"
            else {"gate": "not_selected_input_issues", "entered_here": False}
        ),
        "post_wl514_route_choice_made_here": status == "ok",
        "routing_audit_only": True,
        "shell9_not_admissible_ledgers_reopened_count": 0,
        "shell9_v13_refuted_ledgers_reopened_count": 0,
        "shell9_u7_refuted_ledgers_reopened_count": 0,
        "closed_ledgers_reopened_count": 0,
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
        "shell10_executed_here": False,
        "advance_to_selected_next_gate": False,
        "advance_to_wl516": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Execute the next finite M_tail shell from the wl498 plan. wl515 "
            "selects that gate only; it does not run shell 10, test ambient "
            "C_d solubility, apply wl491, re-open shell-9 ledgers, select a "
            "final candidate, pivot to proof-level work, or claim Selmer "
            "progress."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl514", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl515_post_wl514_route_choice_audit(wl514=load_json(args.wl514))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl515 post-wl514 route-choice audit to {args.out}")
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
