#!/usr/bin/env python3
"""Synthesize wl491-wl519 AA+BB ledgers after the shared u_5 cover is closed."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517 import (  # noqa: E501
        _claims_forbidden_bound,
        _cover_family_synthesis,
        _final_candidate_ledgers,
        _genuinely_deferred_cover_families,
        _ledger_summary,
        _support_family_synthesis,
    )
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from audit_closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517 import (
        _claims_forbidden_bound,
        _cover_family_synthesis,
        _final_candidate_ledgers,
        _genuinely_deferred_cover_families,
        _ledger_summary,
        _support_family_synthesis,
    )
    from json_io import load_json, write_json

EXPECTED_INPUT_WORK_LOGS = [f"wl{index}" for index in range(491, 521)]

BOUNDARY = (
    "This audits only wl521 / support_family_synthesis_after_wl519. It uses "
    "wl520 as the immediate route-choice input and aggregates existing "
    "wl491-wl519 ledger outputs by support family and cover family after the "
    "shared shell-10 u_5 cover has been classified. It preserves all closed "
    "ledgers through wl520, does not execute shell 11, does not compute new "
    "M_tail supports, does not test new ambient C_d solubility, does not "
    "apply wl491 to a new point, does not run broad rank or Selmer "
    "diagnostics, does not select a final obstruction candidate, does not "
    "use the old package-x S~ bridge, and does not claim a complete "
    "Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform "
    "M_tail full rank, or any family exclusion."
)

REQUIRED_WL520_SELECTED_GATE = {
    "gate": "synthesize_support_and_cover_families_after_wl519",
    "entered_here": False,
}

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


def _payloads_ready(payloads: list[dict[str, Any]]) -> bool:
    by_work_log = {payload.get("work_log"): payload for payload in payloads}
    if sorted(by_work_log) != EXPECTED_INPUT_WORK_LOGS:
        return False

    wl519 = by_work_log.get("wl519", {})
    wl520 = by_work_log.get("wl520", {})
    selected_gate = wl520.get("selected_next_gate", {})
    return (
        all(payload.get("status") == "ok" for payload in payloads)
        and all(payload.get("ready") is True for payload in payloads)
        and all(not _claims_forbidden_bound(payload) for payload in payloads)
        and wl519.get("lemma_id")
        == "WL519_resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover"
        and wl519.get("resolved_shell10_deferred_covers_here") is True
        and wl519.get("resolution_summary", {}).get("aa_bb_not_admissible_count") == 2
        and wl519.get("resolution_summary", {}).get("aa_bb_admissible_count") == 0
        and wl519.get("post_wl519_route_choice_made_here") is False
        and wl520.get("lemma_id") == "WL520_post_wl519_route_choice_audit"
        and wl520.get("post_wl519_route_choice_made_here") is True
        and selected_gate.get("gate") == REQUIRED_WL520_SELECTED_GATE["gate"]
        and selected_gate.get("entered_here") is REQUIRED_WL520_SELECTED_GATE["entered_here"]
        and wl520.get("support_family_synthesis_built_here") is False
        and wl520.get("closed_ledger_do_not_reopen") == REQUIRED_CLOSED_LEDGER_EXCLUSIONS
        and wl520.get("advance_to_wl521") is False
        and wl520.get("shell11_executed_here") is False
        and wl520.get("candidate_selected_here") is False
        and wl520.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl520.get("old_package_x_coordinate_collapse_used") is False
        and wl520.get("package_x_s_tilde_bridge_used") is False
    )


def _aa_bb_admissible_cover_families(
    cover_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        row
        for row in cover_rows
        if row["classification"] == "aa_bb_admissible"
    ]


def _cover_family_by_id(
    cover_rows: list[dict[str, Any]],
    cover_family: str,
) -> dict[str, Any]:
    for row in cover_rows:
        if row["cover_family"] == cover_family:
            return row
    return {}


def _theorem_candidate_patterns(
    *,
    support_rows: list[dict[str, Any]],
    cover_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    support_by_id = {row["support_family"]: row for row in support_rows}
    u5 = support_by_id.get("u_5", {})
    counts = u5.get("status_counts", {})
    expected_u5_covers = [
        "support=u_5|L=5|T=8|d=(5,5,1)",
        "support=u_5|L=10|T=11|d=(5,5,1)",
        "support=u_5|L=10|T=19|d=(5,5,1)",
    ]
    cover_by_id = {row["cover_family"]: row for row in cover_rows}
    if not all(cover in cover_by_id for cover in expected_u5_covers):
        return []
    if counts != {
        "already_closed": 0,
        "genuinely_deferred": 0,
        "globally_soluble_but_not_aa_bb_admissible": 4,
        "refuted": 2,
    }:
        return []
    return [
        {
            "pattern_id": "u5_classified_mirror_cover_after_mixed_u5_history",
            "support_family": "u_5",
            "status": "candidate_pattern_not_theorem",
            "cover_families": expected_u5_covers,
            "classification_counts": counts,
            "why_interesting": (
                "The d=(5,5,1) u_5 cover history is now fully classified: "
                "one mirror cover is ambient globally not soluble and two "
                "mirror covers are globally soluble but fail wl491."
            ),
        }
    ]


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "named_proof_gap_generalization_task": {
            "decision": "defer_no_named_gap_isolated",
            "reason": (
                "The post-wl519 synthesis preserves a reusable u_5 "
                "theorem-candidate pattern, but it is still only finite "
                "refuted/not-admissible cover history. It does not isolate a "
                "specific local row, Hilbert row, or Selmer-layer gap to "
                "generalize."
            ),
        },
        "execute_shell11_from_existing_wl498_plan": {
            "decision": "selected_later_next_gate_not_entered",
            "reason": (
                "After wl519 there are no genuinely deferred cover families, "
                "no AA+BB-admissible ambient C_d points, and no final "
                "obstruction candidate. The next route should only be the "
                "later finite M_tail shell extension from the existing wl498 "
                "plan, not a proof-level claim."
            ),
        },
        "select_final_obstruction_candidate": {
            "decision": "reject",
            "reason": (
                "The classified ledgers contain no AA+BB-admissible ambient "
                "C_d point and no unresolved final obstruction candidate."
            ),
        },
    }


def _proof_gap_or_shell_extension_decision() -> dict[str, Any]:
    return {
        "selected_route": "later_finite_shell_extension",
        "named_proof_gap_isolated_here": False,
        "next_gate": "execute_next_finite_M_tail_shell_from_wl498_plan",
        "next_shell": "max(A,B)=11",
        "entered_here": False,
        "reason": (
            "The only reusable pattern isolated here is diagnostic finite "
            "u_5 cover history. It is not a theorem-level proof gap, so the "
            "route should continue later with the next finite shell rather "
            "than a named generalization task."
        ),
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "execute_next_finite_M_tail_shell_from_wl498_plan",
        "entered_here": False,
        "selected_shell": "max(A,B)=11",
        "from_existing_plan": "wl498",
        "shell11_executed_here": False,
        "new_shell_or_grid_refreshed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_here": False,
        "candidate_selected_here": False,
        "minimum_later_question": (
            "Execute the next finite M_tail shell from the existing wl498 "
            "plan at max(A,B)=11, preserving all closed ledgers and stopping "
            "before any ambient C_d / wl491 route unless that later gate "
            "explicitly selects it."
        ),
    }


def build_wl521_support_family_synthesis_after_wl519(
    *,
    ledger_payloads: list[dict[str, Any]],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _payloads_ready(ledger_payloads):
        violations.append("wl491_to_wl520_inputs_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    entries = _final_candidate_ledgers(ledger_payloads) if status == "ok" else []
    support_rows = _support_family_synthesis(entries)
    cover_rows = _cover_family_synthesis(entries)
    deferred_cover_rows = _genuinely_deferred_cover_families(cover_rows)
    admissible_cover_rows = _aa_bb_admissible_cover_families(cover_rows)
    patterns = _theorem_candidate_patterns(
        support_rows=support_rows,
        cover_rows=cover_rows,
    )

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl491-wl519 ledger outputs with wl520 as immediate input",
        "pattern": "AA+BB",
        "lemma_id": "WL521_support_family_synthesis_after_wl519",
        "work_log": "wl521",
        "input_work_log": "wl520",
        "input_work_logs": list(EXPECTED_INPUT_WORK_LOGS),
        "support_family_synthesis_built_here": status == "ok",
        "aggregation_axis": [
            "support_family",
            "cover_family",
        ],
        "ledger_summary": _ledger_summary(
            entries=entries,
            support_rows=support_rows,
            cover_rows=cover_rows,
        ),
        "final_candidate_ledgers": entries,
        "support_family_synthesis": support_rows,
        "cover_family_synthesis": cover_rows,
        "genuinely_deferred_cover_families": deferred_cover_rows,
        "aa_bb_admissible_cover_families": admissible_cover_rows,
        "post_wl519_classified_cover_family": _cover_family_by_id(
            cover_rows,
            "support=u_5|L=10|T=19|d=(5,5,1)",
        ),
        "theorem_candidate_patterns": patterns,
        "proof_gap_or_shell_extension_decision": _proof_gap_or_shell_extension_decision(),
        "route_options": _route_options(),
        "selected_next_gate": _selected_next_gate(),
        "closed_ledger_do_not_reopen": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
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
        "advance_to_wl522": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "wl521 selects only a later finite shell extension from the "
            "existing wl498 plan at max(A,B)=11. It does not execute shell "
            "11, compute supports, test ambient C_d solubility, apply wl491, "
            "or claim theorem progress."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def load_wl491_to_wl520_payloads(ledger_dir: Path) -> list[dict[str, Any]]:
    payloads = []
    for work_log in EXPECTED_INPUT_WORK_LOGS:
        matches = sorted(
            ledger_dir.glob(f"closure_quotient_rank_zero_aa_bb_{work_log}_*.json")
        )
        if len(matches) != 1:
            raise FileNotFoundError(
                f"expected exactly one result JSON for {work_log} in {ledger_dir}"
            )
        payloads.append(load_json(matches[0]))
    return payloads


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl521_support_family_synthesis_after_wl519(
        ledger_payloads=load_wl491_to_wl520_payloads(args.ledger_dir)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl521 support-family synthesis to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_route={audit['proof_gap_or_shell_extension_decision']['selected_route']}")
    print(f"shell11_executed_here={audit['shell11_executed_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
