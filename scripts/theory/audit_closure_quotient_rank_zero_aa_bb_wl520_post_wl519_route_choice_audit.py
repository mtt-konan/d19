#!/usr/bin/env python3
"""Choose the post-wl519 AA+BB route without entering the chosen gate."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl520 / post_wl519_route_choice_audit. It uses wl519 "
    "as input, observes that the only wl518 genuinely deferred shell-10 u_5 "
    "ambient C_d cover has now been classified as globally soluble but not "
    "AA+BB-admissible after wl491, compares the next route options, chooses "
    "support-family / cover-family synthesis after wl519 as the next narrow "
    "gate, and stops before entering that synthesis, executing shell 11, "
    "re-opening wl519 not-admissible ledgers, shell-9 ledgers, or previous "
    "refuted covers, pivoting to proof-level generalization, selecting a "
    "final obstruction candidate, running broad rank or Selmer diagnostics, "
    "using the old package-x S~ bridge, or claiming a complete Sel_2(E) upper "
    "bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform M_tail full rank, or "
    "any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

REQUIRED_WL519_SUMMARY = {
    "wl518_remaining_deferred_candidate_count": 2,
    "shared_cover_count_resolved_here": 1,
    "classified_candidate_entry_count": 2,
    "ambient_globally_soluble_count": 2,
    "ambient_global_solubility_refuted_count": 0,
    "exact_ambient_point_certificate_count": 1,
    "wl491_filter_applied_count": 2,
    "aa_bb_admissible_count": 0,
    "aa_bb_not_admissible_count": 2,
}

REQUIRED_WL519_RESOLVED_IDS = [
    "AA_A10_B9_u_5_m_tail_shell10_candidate",
    "BB_A9_B10_u_5_m_tail_shell10_candidate",
]

REQUIRED_WL519_SHARED_COVER = {
    "L": 10,
    "T": 19,
    "d_vector": {
        "d_minus_p": 5,
        "d_pos_2sqrt_q": 5,
        "d_neg_2sqrt_q": 1,
    },
    "elliptic_curve_model": "V^2 = (X + 78)*(X - 1522)*(X + 1522)",
}

REQUIRED_WL519_CLOSED_LEDGER_EXCLUSIONS = [
    "wl491_wl517_globally_soluble_not_admissible_ledgers",
    "wl500_shell5_u5_refuted_cover",
    "wl517_shell10_L10_T11_u5_not_admissible_cover",
    "wl514_shell9_u7_refuted_cover",
]

REQUIRED_CLOSED_LEDGER_EXCLUSIONS = [
    "u_3_processed_or_deprioritized_after_wl493_wl491",
    "bounded_v_5_entries_disposed_by_wl495_wl496",
    "shell5_u_5_entries_refuted_by_wl500",
    "shell6_empty_diagnostic_output_from_wl502",
    "shell7_entries_disposed_by_wl505_wl506",
    "shell8_pure_u_3_processed_exclusions_from_wl508",
    "shell9_entries_disposed_by_wl511_wl512_wl514",
    "shell10_globally_soluble_not_admissible_ledgers_from_wl517",
    "shell10_u_5_mirror_ledgers_not_admissible_from_wl519",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl519_ready(wl519: dict[str, Any]) -> bool:
    return (
        wl519.get("status") == "ok"
        and wl519.get("ready") is True
        and wl519.get("lemma_id")
        == "WL519_resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover"
        and wl519.get("work_log") == "wl519"
        and wl519.get("input_work_logs") == ["wl491", "wl518"]
        and wl519.get("resolved_shell10_deferred_covers_here") is True
        and wl519.get("resolution_summary") == REQUIRED_WL519_SUMMARY
        and wl519.get("resolved_candidate_ids") == REQUIRED_WL519_RESOLVED_IDS
        and wl519.get("resolved_shared_cover") == REQUIRED_WL519_SHARED_COVER
        and wl519.get("closed_ledger_do_not_reopen")
        == REQUIRED_WL519_CLOSED_LEDGER_EXCLUSIONS
        and wl519.get("closed_ledgers_reopened_count") == 0
        and wl519.get("shell10_not_admissible_ledgers_reopened_count") == 0
        and wl519.get("shell10_refuted_ledgers_reopened_count") == 0
        and wl519.get("wl491_filter_applied_to_new_point_here") is True
        and wl519.get("candidate_selected_here") is False
        and wl519.get("post_wl519_route_choice_made_here") is False
        and wl519.get("new_m_tail_or_kernel_candidate_selected_here") is False
        and wl519.get("new_m_tail_row_proved_here") is False
        and wl519.get("new_local_row_proved_here") is False
        and wl519.get("new_shell_or_grid_refreshed_here") is False
        and wl519.get("m_tail_diagnostics_extended_here") is False
        and wl519.get("new_supports_computed_here") is False
        and wl519.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl519.get("family_rank_or_selmer_diagnostics_run") is False
        and wl519.get("single_curve_diagnostics_run") is False
        and wl519.get("old_package_x_coordinate_collapse_used") is False
        and wl519.get("package_x_s_tilde_bridge_used") is False
        and wl519.get("shell11_executed_here") is False
        and wl519.get("advance_to_wl520") is False
        and not _claims_forbidden_bound(wl519)
    )


def _post_wl519_route_state_summary() -> dict[str, int]:
    return {
        "wl518_deferred_cover_families_classified_after_wl519": 1,
        "wl519_globally_soluble_not_admissible_count": 2,
        "shell10_remaining_deferred_count_after_wl519": 0,
        "shell10_aa_bb_admissible_count_after_wl519": 0,
        "active_final_candidate_count_after_wl519": 0,
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "support_family_cover_family_synthesis_toward_reusable_theorem_candidate_patterns": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl519 classifies the only wl518 deferred cover, so the "
                "narrowest controllable next step is to resynthesize the "
                "wl491-wl519 ledgers by support and cover family. This can "
                "preserve reusable theorem-candidate patterns without "
                "claiming any theorem or widening the finite shell search."
            ),
        },
        "execute_shell11_from_existing_wl498_plan": {
            "decision": "defer",
            "reason": (
                "Shell 11 is a legitimate later finite M_tail diagnostic "
                "extension only after the post-wl519 classified shell-10 "
                "ledger state is synthesized. Running it now would widen the "
                "search before extracting the reusable pattern information "
                "from the fully classified shell-10 route."
            ),
        },
        "proof_level_generalization_or_local_row_work": {
            "decision": "defer_without_named_theorem_gap",
            "reason": (
                "wl519 produces a globally soluble but not AA+BB-admissible "
                "classification, not a named local-row or Selmer-layer gap. "
                "Proof-level work should wait until synthesis identifies a "
                "specific reusable theorem-candidate pattern or obstruction "
                "shape to formalize."
            ),
        },
        "final_candidate_selection": {
            "decision": "reject",
            "reason": (
                "No AA+BB-admissible ambient C_d point or unresolved final "
                "obstruction candidate remains after wl519. The two mirror "
                "u_5 entries are not-admissible ledgers, not candidates."
            ),
        },
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "synthesize_support_and_cover_families_after_wl519",
        "entered_here": False,
        "input_work_logs_to_use_later": [f"wl{index}" for index in range(491, 520)],
        "purpose": "derive_reusable_theorem_candidate_patterns",
        "not_a_theorem_claim": True,
        "must_preserve_closed_ledgers": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "compare_axes": [
            "support_family",
            "cover_family",
            "classification",
            "wl491_admissibility_status",
        ],
        "new_shell_or_grid_refreshed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_here": False,
        "candidate_selected_here": False,
        "minimum_later_question": (
            "Aggregate wl491-wl519 ledgers by support and cover family after "
            "the shared shell-10 u_5 cover has been classified, then decide "
            "whether the reusable pattern suggests a named proof gap or only "
            "a later finite shell extension."
        ),
    }


def build_wl520_post_wl519_route_choice_audit(
    *,
    wl519: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl519_ready(wl519):
        violations.append("wl519_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl519 closed shared shell-10 u_5 ambient C_d route state",
        "pattern": "AA+BB",
        "lemma_id": "WL520_post_wl519_route_choice_audit",
        "work_log": "wl520",
        "input_work_log": "wl519",
        "post_wl519_route_state_summary": (
            _post_wl519_route_state_summary() if status == "ok" else {}
        ),
        "closed_ledger_do_not_reopen": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "route_options": _route_options(),
        "selected_next_gate": (
            _selected_next_gate()
            if status == "ok"
            else {"gate": "not_selected_input_issues", "entered_here": False}
        ),
        "post_wl519_route_choice_made_here": status == "ok",
        "routing_audit_only": True,
        "support_family_synthesis_built_here": False,
        "wl519_not_admissible_ledgers_reopened_count": 0,
        "shell9_ledgers_reopened_count": 0,
        "previous_refuted_covers_reopened_count": 0,
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
        "shell11_executed_here": False,
        "advance_to_selected_next_gate": False,
        "advance_to_wl521": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Synthesize support and cover families after wl519. wl520 selects "
            "that gate only; it does not build the synthesis, execute shell "
            "11, run broad Selmer diagnostics, select a final candidate, or "
            "claim theorem progress."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl519", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl520_post_wl519_route_choice_audit(wl519=load_json(args.wl519))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl520 post-wl519 route-choice audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(f"shell11_executed_here={audit['shell11_executed_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
