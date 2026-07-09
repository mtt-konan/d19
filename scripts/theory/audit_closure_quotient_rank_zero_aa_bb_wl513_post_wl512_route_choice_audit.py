#!/usr/bin/env python3
"""Choose the post-wl512 AA+BB route without entering the chosen gate."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl513 / post_wl512_route_choice_audit. It uses wl512 "
    "as input, observes that the two shell-9 v_13 deferred covers have been "
    "refuted and exactly two shell-9 u_7 ambient C_d global-solubility "
    "ledgers remain deferred for the shared L=7,T=16,d=(7,7,1) cover, "
    "evaluates the next route options, chooses the next narrow gate as "
    "targeted resolution of that remaining u_7 cover, and stops before "
    "entering that gate, executing shell 10, re-opening shell-9 v_13 "
    "refuted ledgers, re-opening shell-9 globally soluble but not "
    "AA+BB-admissible ledgers, selecting a final obstruction candidate, "
    "proving local rows, running broad rank or Selmer diagnostics, advancing "
    "to wl514, using the old package-x S~ bridge, or claiming a complete "
    "Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform "
    "M_tail full rank, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

REQUIRED_WL512_SUMMARY = {
    "wl511_deferred_entry_count": 4,
    "explicitly_classified_entry_count": 4,
    "ambient_globally_soluble_count": 0,
    "ambient_global_solubility_refuted_count": 2,
    "ambient_global_solubility_still_deferred_count": 2,
    "wl491_filter_applied_count": 0,
    "aa_bb_admissible_count": 0,
    "aa_bb_not_admissible_count": 0,
    "aa_bb_missing_pullback_data_count": 0,
    "aa_bb_filter_not_applied_count": 4,
}

REFUTED_V13_IDS = [
    "AA_A4_B9_v_13_m_tail_shell9_candidate",
    "BB_A9_B4_v_13_m_tail_shell9_candidate",
]

DEFERRED_U7_IDS = [
    "AA_A7_B9_u_7_m_tail_shell9_candidate",
    "BB_A9_B7_u_7_m_tail_shell9_candidate",
]

EXPECTED_U7_D_VECTOR = {
    "d_minus_p": 7,
    "d_pos_2sqrt_q": 7,
    "d_neg_2sqrt_q": 1,
}

REQUIRED_CLOSED_LEDGER_EXCLUSIONS = [
    "u_3_processed_or_deprioritized_after_wl493_wl491",
    "bounded_v_5_entries_disposed_by_wl495_wl496",
    "shell5_u_5_entries_refuted_by_wl500",
    "shell6_empty_diagnostic_output_from_wl502",
    "shell7_entries_disposed_by_wl505_wl506",
    "shell8_pure_u_3_processed_exclusions_from_wl508",
    "shell9_globally_soluble_not_admissible_ledgers_from_wl511",
    "shell9_v_13_deferred_ledgers_refuted_by_wl512",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl512_ready(wl512: dict[str, Any]) -> bool:
    return (
        wl512.get("status") == "ok"
        and wl512.get("ready") is True
        and wl512.get("lemma_id")
        == "WL512_resolve_shell9_deferred_ambient_C_d_global_solubility_ledgers"
        and wl512.get("work_log") == "wl512"
        and wl512.get("input_work_logs") == ["wl491", "wl511"]
        and wl512.get("resolution_summary") == REQUIRED_WL512_SUMMARY
        and wl512.get("classified_wl511_deferred_ledgers_here") is True
        and wl512.get("all_wl511_deferred_entries_resolved_here") is False
        and wl512.get("shell9_globally_soluble_not_admissible_reopened_count") == 0
        and wl512.get("closed_ledgers_reopened_count") == 0
        and wl512.get("candidate_selected_here") is False
        and wl512.get("new_m_tail_row_proved_here") is False
        and wl512.get("new_local_row_proved_here") is False
        and wl512.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl512.get("family_rank_or_selmer_diagnostics_run") is False
        and wl512.get("single_curve_diagnostics_run") is False
        and wl512.get("old_package_x_coordinate_collapse_used") is False
        and wl512.get("package_x_s_tilde_bridge_used") is False
        and wl512.get("shell10_executed_here") is False
        and wl512.get("advance_to_wl513") is False
        and not _claims_forbidden_bound(wl512)
    )


def _classified_entries(wl512: dict[str, Any]) -> list[dict[str, Any]]:
    return list(wl512.get("classified_deferred_entries", []))


def _deferred_u7_entries(wl512: dict[str, Any]) -> list[dict[str, Any]]:
    entries = [
        entry
        for entry in _classified_entries(wl512)
        if entry.get("candidate_id") in DEFERRED_U7_IDS
    ]
    return sorted(entries, key=lambda entry: DEFERRED_U7_IDS.index(entry["candidate_id"]))


def _refuted_v13_entries(wl512: dict[str, Any]) -> list[dict[str, Any]]:
    entries = [
        entry
        for entry in _classified_entries(wl512)
        if entry.get("candidate_id") in REFUTED_V13_IDS
    ]
    return sorted(entries, key=lambda entry: REFUTED_V13_IDS.index(entry["candidate_id"]))


def _is_refuted_v13_entry(entry: dict[str, Any]) -> bool:
    return (
        entry.get("candidate_support") == ["v_13"]
        and entry.get("ambient_c_d_global_solubility", {}).get("status")
        == "globally_not_soluble"
        and entry.get("routing_state", {}).get("ledger_route")
        == "ambient_c_d_global_solubility_refuted_ledger"
        and entry.get("wl491_filter_result", {}).get("output_class") == "not_applied"
    )


def _is_deferred_u7_entry(entry: dict[str, Any]) -> bool:
    sample = entry.get("sample", {})
    cover = entry.get("complete_c_d_cover", {})
    return (
        entry.get("candidate_support") == ["u_7"]
        and sample.get("L") == 7
        and sample.get("T") == 16
        and cover.get("d_vector") == EXPECTED_U7_D_VECTOR
        and entry.get("ambient_c_d_global_solubility", {}).get("status")
        == "global_solubility_deferred"
        and entry.get("routing_state", {}).get("ledger_route")
        == "ambient_c_d_solubility_deferred_ledger"
        and entry.get("wl491_filter_result", {}).get("output_class") == "not_applied"
    )


def _u7_shared_cover_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    if not entries:
        return {}
    sample = entries[0].get("sample", {})
    return {
        "L": sample.get("L"),
        "T": sample.get("T"),
        "d_vector": dict(EXPECTED_U7_D_VECTOR),
        "elliptic_curve_model": "V^2 = (X + 120)*(X - 904)*(X + 904)",
    }


def _post_wl512_route_state_summary(wl512: dict[str, Any]) -> dict[str, int]:
    summary = wl512["resolution_summary"]
    return {
        "wl512_deferred_entry_count": summary["wl511_deferred_entry_count"],
        "wl512_explicitly_classified_entry_count": summary[
            "explicitly_classified_entry_count"
        ],
        "shell9_v13_refuted_count_from_wl512": summary[
            "ambient_global_solubility_refuted_count"
        ],
        "shell9_u7_still_deferred_count_after_wl512": summary[
            "ambient_global_solubility_still_deferred_count"
        ],
        "shell9_wl491_filter_applied_count_from_wl512": summary[
            "wl491_filter_applied_count"
        ],
        "aa_bb_admissible_count_after_wl512": summary["aa_bb_admissible_count"],
        "active_candidate_count_after_wl512": 0,
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "wl512 leaves exactly two unresolved ledgers, and they are "
                "the same shell-9 u_7 ambient C_d cover with "
                "L=7,T=16,d=(7,7,1). The narrowest route is therefore to "
                "resolve that one shared cover by an exact ambient point or "
                "an exhaustive no-lift certificate before any wl491 filter "
                "or candidate selection can occur."
            ),
        },
        "execute_shell10_from_wl498_plan": {
            "decision": "reject",
            "reason": (
                "There is still an unresolved shell-9 ambient C_d "
                "global-solubility ledger. Advancing to shell 10 would widen "
                "the diagnostic search before the current explicit gap is "
                "resolved."
            ),
        },
        "reopen_shell9_v13_or_not_admissible_ledgers": {
            "decision": "reject",
            "reason": (
                "The two v_13 deferred ledgers were refuted by wl512, and "
                "the four globally soluble but not AA+BB-admissible shell-9 "
                "ledgers were already routed by wl511. Re-opening them would "
                "duplicate closed ledger work."
            ),
        },
        "select_final_obstruction_candidate": {
            "decision": "reject",
            "reason": (
                "The remaining u_7 cover has neither an exact ambient point "
                "nor an exhaustive no-lift certificate, and no shell-9 entry "
                "is AA+BB-admissible. There is no final candidate to select."
            ),
        },
        "prove_local_or_hilbert_rows_now": {
            "decision": "future_gate_only",
            "reason": (
                "Local/Hilbert row work is not entered by this route-choice "
                "audit. It may be selected later only as a specific future "
                "gate, not proved here."
            ),
        },
    }


def _selected_next_gate(entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "gate": "resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers",
        "entered_here": False,
        "candidate_ids": list(DEFERRED_U7_IDS),
        "shared_cover": "L=7,T=16,d=(7,7,1)",
        "shared_cover_summary": _u7_shared_cover_summary(entries),
        "allowed_future_certificates": [
            "exact_ambient_C_d_global_point",
            "exhaustive_no_lift_certificate",
        ],
        "wl491_filter_allowed_only_after_global_solubility": True,
        "shell10_executed_here": False,
        "new_local_row_proved_here": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "candidate_selected_here": False,
        "minimum_later_question": (
            "Resolve the shared shell-9 u_7 ambient C_d cover at "
            "L=7,T=16,d=(7,7,1) by either an exact ambient point or an "
            "exhaustive no-lift certificate; only after global solubility is "
            "established may wl491 be applied."
        ),
    }


def build_wl513_post_wl512_route_choice_audit(
    *,
    wl512: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl512_ready(wl512):
        violations.append("wl512_input_not_ready_or_not_scoped")

    u7_entries = _deferred_u7_entries(wl512)
    v13_entries = _refuted_v13_entries(wl512)
    if [entry.get("candidate_id") for entry in u7_entries] != DEFERRED_U7_IDS:
        violations.append("wl512_remaining_u7_deferred_entries_missing_or_out_of_order")
    if [entry.get("candidate_id") for entry in v13_entries] != REFUTED_V13_IDS:
        violations.append("wl512_refuted_v13_entries_missing_or_out_of_order")
    if any(not _is_deferred_u7_entry(entry) for entry in u7_entries):
        violations.append("wl512_u7_entries_not_matching_expected_deferred_cover")
    if any(not _is_refuted_v13_entry(entry) for entry in v13_entries):
        violations.append("wl512_v13_entries_not_matching_expected_refuted_state")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl512 post-classification shell-9 deferred-ledger state",
        "pattern": "AA+BB",
        "lemma_id": "WL513_post_wl512_route_choice_audit",
        "work_log": "wl513",
        "input_work_log": "wl512",
        "post_wl512_route_state_summary": (
            _post_wl512_route_state_summary(wl512) if status == "ok" else {}
        ),
        "remaining_deferred_candidate_ids": (
            [entry["candidate_id"] for entry in u7_entries] if status == "ok" else []
        ),
        "remaining_deferred_shared_cover": (
            _u7_shared_cover_summary(u7_entries) if status == "ok" else {}
        ),
        "closed_ledger_do_not_reopen": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "route_options": _route_options(),
        "selected_next_gate": (
            _selected_next_gate(u7_entries)
            if status == "ok"
            else {"gate": "not_selected_input_issues", "entered_here": False}
        ),
        "post_wl512_route_choice_made_here": status == "ok",
        "routing_audit_only": True,
        "shell9_not_admissible_ledgers_reopened_count": 0,
        "shell9_v13_refuted_ledgers_reopened_count": 0,
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
        "advance_to_wl514": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Resolve the remaining shared shell-9 u_7 ambient C_d "
            "global-solubility cover. wl513 selects that gate only; it does "
            "not prove local rows, test solubility, apply wl491, execute "
            "shell 10, select a final candidate, or claim Selmer progress."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl512", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl513_post_wl512_route_choice_audit(wl512=load_json(args.wl512))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl513 post-wl512 route-choice audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(f"remaining_deferred_count={len(audit['remaining_deferred_candidate_ids'])}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
