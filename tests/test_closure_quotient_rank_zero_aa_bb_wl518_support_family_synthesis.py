from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517 import (  # noqa: E501
    build_wl518_support_family_synthesis_after_wl517,
)

WL491_TO_WL517_RESULT_FILES = [
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
]


def _ledger_payloads() -> list[dict[str, object]]:
    return [
        json.loads((ROOT / "results" / file_name).read_text(encoding="utf-8"))
        for file_name in WL491_TO_WL517_RESULT_FILES
    ]


def _wl518() -> dict[str, object]:
    return build_wl518_support_family_synthesis_after_wl517(
        ledger_payloads=_ledger_payloads()
    )


def test_wl518_aggregates_final_ledgers_by_support_and_cover_family() -> None:
    audit = _wl518()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL518_support_family_synthesis_after_wl517"
    assert audit["work_log"] == "wl518"
    assert audit["input_work_log"] == "wl517"
    assert audit["input_work_logs"] == [f"wl{index}" for index in range(491, 518)]
    assert audit["ledger_summary"] == {
        "final_candidate_ledger_entry_count": 43,
        "support_family_count": 13,
        "cover_family_count": 22,
        "refuted_entry_count": 10,
        "globally_soluble_but_not_aa_bb_admissible_entry_count": 27,
        "genuinely_deferred_entry_count": 2,
        "already_closed_entry_count": 4,
        "aa_bb_admissible_entry_count": 0,
    }

    support_families = {
        family["support_family"]: family for family in audit["support_family_synthesis"]
    }
    assert support_families["u_5"]["classification"] == "genuinely_deferred"
    assert support_families["u_5"]["status_counts"] == {
        "already_closed": 0,
        "genuinely_deferred": 2,
        "globally_soluble_but_not_aa_bb_admissible": 2,
        "refuted": 2,
    }
    assert support_families["u_3"]["classification"] == "already_closed"
    assert support_families["u_3"]["status_counts"] == {
        "already_closed": 4,
        "genuinely_deferred": 0,
        "globally_soluble_but_not_aa_bb_admissible": 1,
        "refuted": 0,
    }


def test_wl518_identifies_the_current_deferred_cover_family_and_candidate_pattern() -> None:
    audit = _wl518()

    assert audit["genuinely_deferred_cover_families"] == [
        {
            "cover_family": "support=u_5|L=10|T=19|d=(5,5,1)",
            "support_family": "u_5",
            "classification": "genuinely_deferred",
            "candidate_ids": [
                "AA_A10_B9_u_5_m_tail_shell10_candidate",
                "BB_A9_B10_u_5_m_tail_shell10_candidate",
            ],
            "entry_count": 2,
            "work_logs": ["wl517"],
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
    ]
    assert audit["theorem_candidate_patterns"] == [
        {
            "pattern_id": "u5_mirror_deferred_cover_after_mixed_u5_history",
            "support_family": "u_5",
            "current_cover_family": "support=u_5|L=10|T=19|d=(5,5,1)",
            "candidate_ids": [
                "AA_A10_B9_u_5_m_tail_shell10_candidate",
                "BB_A9_B10_u_5_m_tail_shell10_candidate",
            ],
            "status": "candidate_pattern_not_theorem",
            "why_interesting": (
                "The same u_5 d-vector family already has a refuted shell-5 "
                "cover and a shell-10 globally soluble but not AA+BB-admissible "
                "mirror cover; the only remaining open instance is the shared "
                "L=10,T=19 cover."
            ),
        }
    ]


def test_wl518_selects_targeted_shell10_u5_cover_resolution_but_does_not_enter_it() -> None:
    audit = _wl518()

    selected = audit["selected_next_gate"]
    assert selected["gate"] == "resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover"
    assert selected["entered_here"] is False
    assert selected["candidate_ids"] == [
        "AA_A10_B9_u_5_m_tail_shell10_candidate",
        "BB_A9_B10_u_5_m_tail_shell10_candidate",
    ]
    assert selected["shared_cover"] == "L=10,T=19,d=(5,5,1)"
    assert selected["allowed_future_certificates"] == [
        "exact_ambient_C_d_global_point",
        "exhaustive_no_lift_certificate",
    ]
    assert audit["route_options"][
        "resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover"
    ]["decision"] == "selected_next_narrow_gate"
    assert audit["route_options"]["proof_level_generalization_task"][
        "decision"
    ] == "defer_until_current_deferred_cover_is_classified"


def test_wl518_stops_without_forbidden_work_or_wl519_advance() -> None:
    audit = _wl518()

    assert audit["support_family_synthesis_built_here"] is True
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["shell11_executed_here"] is False
    assert audit["resolved_shell10_deferred_covers_here"] is False
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
    assert audit["advance_to_wl519"] is False
    assert audit["stop_after_current_task"] is True


def test_wl518_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl518.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517.py"
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
    assert "work_log=wl518" in result.stdout
    assert (
        "selected_gate=resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover"
        in result.stdout
    )
    assert "genuinely_deferred_cover_family_count=1" in result.stdout
    assert payload["work_log"] == "wl518"
    assert payload["selected_next_gate"]["entered_here"] is False
