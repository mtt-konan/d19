from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl521_support_family_synthesis_after_wl519 import (  # noqa: E501
    build_wl521_support_family_synthesis_after_wl519,
)

WL491_TO_WL520_RESULT_FILES = [
    "closure_quotient_rank_zero_aa_bb_wl491_ambient_c_d_to_aa_bb_admissibility_filter.json",
    "closure_quotient_rank_zero_aa_bb_wl492_route_selection_after_admissibility_filter.json",
    "closure_quotient_rank_zero_aa_bb_wl493_candidate_queue_from_existing_m_tail_diagnostics.json",
    "closure_quotient_rank_zero_aa_bb_wl494_extend_or_refresh_m_tail_diagnostics.json",
    "closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json",
    "closure_quotient_rank_zero_aa_bb_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers.json",
    "closure_quotient_rank_zero_aa_bb_wl497_post_wl496_route_choice_audit.json",
    "closure_quotient_rank_zero_aa_bb_wl498_structure_next_m_tail_diagnostic_extension_plan.json",
    "closure_quotient_rank_zero_aa_bb_wl499_execute_finite_m_tail_diagnostic_extension_from_wl498_plan.json",
    "closure_quotient_rank_zero_aa_bb_wl500_route_active_u5_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.json",
    "closure_quotient_rank_zero_aa_bb_wl501_post_wl500_route_choice_audit.json",
    "closure_quotient_rank_zero_aa_bb_wl502_execute_next_finite_m_tail_shell_from_wl498_plan.json",
    "closure_quotient_rank_zero_aa_bb_wl503_post_wl502_empty_shell_route_choice_audit.json",
    "closure_quotient_rank_zero_aa_bb_wl504_execute_next_finite_m_tail_shell_from_wl498_plan.json",
    "closure_quotient_rank_zero_aa_bb_wl505_route_active_shell7_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.json",
    "closure_quotient_rank_zero_aa_bb_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers.json",
    "closure_quotient_rank_zero_aa_bb_wl507_post_wl506_route_choice_audit.json",
    "closure_quotient_rank_zero_aa_bb_wl508_execute_next_finite_m_tail_shell_from_wl498_plan.json",
    "closure_quotient_rank_zero_aa_bb_wl509_post_wl508_empty_shell_route_choice_audit.json",
    "closure_quotient_rank_zero_aa_bb_wl510_execute_next_finite_m_tail_shell_from_wl498_plan.json",
    "closure_quotient_rank_zero_aa_bb_wl511_route_active_shell9_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.json",
    "closure_quotient_rank_zero_aa_bb_wl512_resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers.json",
    "closure_quotient_rank_zero_aa_bb_wl513_post_wl512_route_choice_audit.json",
    "closure_quotient_rank_zero_aa_bb_wl514_resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger.json",
    "closure_quotient_rank_zero_aa_bb_wl515_post_wl514_route_choice_audit.json",
    "closure_quotient_rank_zero_aa_bb_wl516_execute_next_finite_m_tail_shell_from_wl498_plan.json",
    "closure_quotient_rank_zero_aa_bb_wl517_route_active_shell10_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.json",
    "closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517.json",
    "closure_quotient_rank_zero_aa_bb_wl519_resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover.json",
    "closure_quotient_rank_zero_aa_bb_wl520_post_wl519_route_choice_audit.json",
]


def _ledger_payloads() -> list[dict[str, object]]:
    return [
        json.loads((ROOT / "results" / file_name).read_text(encoding="utf-8"))
        for file_name in WL491_TO_WL520_RESULT_FILES
    ]


def _wl521() -> dict[str, object]:
    return build_wl521_support_family_synthesis_after_wl519(
        ledger_payloads=_ledger_payloads()
    )


def test_wl521_reaggregates_wl491_wl519_after_the_shared_u5_cover_is_classified() -> None:
    audit = _wl521()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL521_support_family_synthesis_after_wl519"
    assert audit["work_log"] == "wl521"
    assert audit["input_work_log"] == "wl520"
    assert audit["input_work_logs"] == [f"wl{index}" for index in range(491, 521)]
    assert audit["ledger_summary"] == {
        "final_candidate_ledger_entry_count": 43,
        "support_family_count": 13,
        "cover_family_count": 22,
        "refuted_entry_count": 10,
        "globally_soluble_but_not_aa_bb_admissible_entry_count": 29,
        "genuinely_deferred_entry_count": 0,
        "already_closed_entry_count": 4,
        "aa_bb_admissible_entry_count": 0,
    }
    assert audit["genuinely_deferred_cover_families"] == []
    assert audit["aa_bb_admissible_cover_families"] == []

    support_families = {
        family["support_family"]: family for family in audit["support_family_synthesis"]
    }
    assert support_families["u_5"]["classification"] == (
        "globally_soluble_but_not_aa_bb_admissible"
    )
    assert support_families["u_5"]["status_counts"] == {
        "already_closed": 0,
        "genuinely_deferred": 0,
        "globally_soluble_but_not_aa_bb_admissible": 4,
        "refuted": 2,
    }


def test_wl521_preserves_post_wl519_u5_pattern_without_turning_it_into_a_theorem() -> None:
    audit = _wl521()

    assert audit["post_wl519_classified_cover_family"] == {
        "cover_family": "support=u_5|L=10|T=19|d=(5,5,1)",
        "support_family": "u_5",
        "classification": "globally_soluble_but_not_aa_bb_admissible",
        "candidate_ids": [
            "AA_A10_B9_u_5_m_tail_shell10_candidate",
            "BB_A9_B10_u_5_m_tail_shell10_candidate",
        ],
        "entry_count": 2,
        "work_logs": ["wl519"],
        "cover_summary": {
            "L": 10,
            "T": 19,
            "d_vector": {
                "d_minus_p": 5,
                "d_pos_2sqrt_q": 5,
                "d_neg_2sqrt_q": 1,
            },
        },
    }
    assert audit["theorem_candidate_patterns"] == [
        {
            "pattern_id": "u5_classified_mirror_cover_after_mixed_u5_history",
            "support_family": "u_5",
            "status": "candidate_pattern_not_theorem",
            "cover_families": [
                "support=u_5|L=5|T=8|d=(5,5,1)",
                "support=u_5|L=10|T=11|d=(5,5,1)",
                "support=u_5|L=10|T=19|d=(5,5,1)",
            ],
            "classification_counts": {
                "already_closed": 0,
                "genuinely_deferred": 0,
                "globally_soluble_but_not_aa_bb_admissible": 4,
                "refuted": 2,
            },
            "why_interesting": (
                "The d=(5,5,1) u_5 cover history is now fully classified: "
                "one mirror cover is ambient globally not soluble and two "
                "mirror covers are globally soluble but fail wl491."
            ),
        }
    ]


def test_wl521_selects_later_finite_shell_extension_not_a_named_proof_gap() -> None:
    audit = _wl521()

    decision = audit["proof_gap_or_shell_extension_decision"]
    assert decision["selected_route"] == "later_finite_shell_extension"
    assert decision["named_proof_gap_isolated_here"] is False
    assert decision["next_gate"] == "execute_next_finite_M_tail_shell_from_wl498_plan"
    assert decision["next_shell"] == "max(A,B)=11"
    assert decision["entered_here"] is False
    assert audit["selected_next_gate"]["gate"] == "execute_next_finite_M_tail_shell_from_wl498_plan"
    assert audit["selected_next_gate"]["entered_here"] is False
    assert audit["route_options"]["named_proof_gap_generalization_task"][
        "decision"
    ] == "defer_no_named_gap_isolated"
    assert audit["route_options"]["execute_shell11_from_existing_wl498_plan"][
        "decision"
    ] == "selected_later_next_gate_not_entered"


def test_wl521_stops_without_forbidden_work_or_wl522_advance() -> None:
    audit = _wl521()

    assert audit["support_family_synthesis_built_here"] is True
    assert audit["wl519_not_admissible_ledgers_reopened_count"] == 0
    assert audit["shell9_ledgers_reopened_count"] == 0
    assert audit["previous_refuted_covers_reopened_count"] == 0
    assert audit["closed_ledgers_reopened_count"] == 0
    assert audit["new_shell_or_grid_refreshed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["wl491_filter_applied_to_new_point_here"] is False
    assert audit["shell11_executed_here"] is False
    assert audit["candidate_selected_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["family_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_selected_next_gate"] is False
    assert audit["advance_to_wl522"] is False
    assert audit["stop_after_current_task"] is True


def test_wl521_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl521.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl521_support_family_synthesis_after_wl519.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--ledger-dir",
            str(ROOT / "results"),
            "--out",
            str(out),
            "--strict",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "work_log=wl521" in result.stdout
    assert "selected_route=later_finite_shell_extension" in result.stdout
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl521"
    assert payload["selected_next_gate"]["entered_here"] is False
