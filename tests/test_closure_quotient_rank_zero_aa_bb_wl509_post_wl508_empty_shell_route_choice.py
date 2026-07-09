from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl509_post_wl508_empty_shell_route_choice_audit import (  # noqa: E501
    build_wl509_post_wl508_empty_shell_route_choice_audit,
)


def _wl508() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "WL508_execute_next_finite_M_tail_shell_from_wl498_plan",
        "work_log": "wl508",
        "input_work_logs": ["wl480", "wl507"],
        "declared_extension_scope": {
            "extension_unit": "finite_primitive_shell",
            "shell_bound": 8,
            "shell_axis": "max(A,B)",
            "sides": ["AA", "BB"],
            "primitive_condition": "gcd(A,B)=1",
            "sample_order": "side, then A ascending, then B ascending",
            "sample_count": 16,
            "uses_existing_wl481_matrix_builder": True,
            "uses_wl498_duplicate_support_guard": True,
            "uses_wl507_closed_ledger_exclusions": True,
        },
        "closed_ledger_exclusions_applied": [
            "u_3_processed_or_deprioritized_after_wl493_wl491",
            "bounded_v_5_entries_disposed_by_wl495_wl496",
            "shell5_u_5_entries_refuted_by_wl500",
            "shell6_empty_diagnostic_output_from_wl502",
            "shell7_active_not_admissible_ledgers_from_wl505",
            "shell7_processed_u3_exclusions_from_wl505",
            "shell7_w5_deferred_ledgers_refuted_by_wl506",
            "shell7_u7_w37_deferred_ledgers_not_admissible_by_wl506",
        ],
        "sample_summary": {
            "sample_count": 16,
            "full_rank_sample_count": 14,
            "kernel_sample_count": 2,
            "kernel_support_entry_count": 2,
            "active_new_support_entry_count": 0,
            "excluded_duplicate_or_processed_support_entry_count": 2,
            "unique_active_supports": [],
        },
        "active_new_kernel_supports": [],
        "excluded_duplicate_or_processed_supports": [
            {"candidate_id": "AA_A3_B8_u_3_m_tail_shell8_candidate"},
            {"candidate_id": "BB_A8_B3_u_3_m_tail_shell8_candidate"},
        ],
        "m_tail_diagnostics_extended_here": True,
        "new_supports_computed_here": True,
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_c_d_solubility_tested_here": False,
        "ambient_c_d_solubility_proved_for_new_candidate_here": False,
        "wl491_filter_applied_here": False,
        "aa_bb_admissibility_proved_for_new_candidate_here": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "family_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "uniform_m_tail_full_rank_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "advance_to_wl509": False,
    }


def _wl509() -> dict[str, object]:
    return build_wl509_post_wl508_empty_shell_route_choice_audit(wl508=_wl508())


def test_wl509_summarizes_empty_active_shell8_without_reopening_ledgers() -> None:
    audit = _wl509()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL509_post_wl508_empty_shell_route_choice_audit"
    assert audit["work_log"] == "wl509"
    assert audit["input_work_log"] == "wl508"
    assert audit["post_wl508_empty_shell_state_summary"] == {
        "completed_finite_shell_bound_after_wl508": 8,
        "shell8_sample_count_from_wl508": 16,
        "shell8_full_rank_sample_count_from_wl508": 14,
        "shell8_kernel_sample_count_from_wl508": 2,
        "shell8_kernel_support_entry_count_from_wl508": 2,
        "shell8_active_new_support_entry_count_from_wl508": 0,
        "shell8_excluded_duplicate_or_processed_support_entry_count_from_wl508": 2,
        "active_candidate_count_after_wl508": 0,
    }
    assert audit["closed_ledger_do_not_reopen"] == [
        "u_3_processed_or_deprioritized_after_wl493_wl491",
        "bounded_v_5_entries_disposed_by_wl495_wl496",
        "shell5_u_5_entries_refuted_by_wl500",
        "shell6_empty_diagnostic_output_from_wl502",
        "shell7_active_not_admissible_ledgers_from_wl505",
        "shell7_processed_u3_exclusions_from_wl505",
        "shell7_w5_deferred_ledgers_refuted_by_wl506",
        "shell7_u7_w37_deferred_ledgers_not_admissible_by_wl506",
        "shell8_empty_active_diagnostic_output_from_wl508",
        "shell8_processed_u3_exclusions_from_wl508",
    ]


def test_wl509_selects_shell9_gate_but_does_not_execute_it() -> None:
    audit = _wl509()

    selected = audit["selected_next_gate"]
    assert selected["gate"] == "execute_next_finite_M_tail_shell_from_wl498_plan"
    assert selected["entered_here"] is False
    assert selected["uses_existing_wl498_plan"] is True
    assert selected["shell_bound_to_execute_later"] == 9
    assert selected["preserve_wl498_duplicate_support_guard"] is True
    assert selected["new_shell_or_grid_refreshed_here"] is False
    assert selected["m_tail_diagnostics_extended_here"] is False
    assert selected["new_supports_computed_here"] is False
    assert selected["new_c_d_solubility_tested_here"] is False
    assert selected["wl491_filter_applied_here"] is False
    assert selected["candidate_selected_here"] is False
    assert selected["required_route_for_future_new_support"] == [
        "M_tail_support",
        "ambient_C_d_global_solubility",
        "wl491_AA_BB_admissibility_filter",
        "admissible_or_not_admissible_or_refuted_ledger",
    ]
    assert audit["route_options"]["execute_next_finite_M_tail_shell_from_wl498_plan"][
        "decision"
    ] == "selected_next_narrow_gate"
    assert audit["route_options"]["invent_shell8_ambient_C_d_solubility_task"][
        "decision"
    ] == "reject"
    assert audit["route_options"]["reopen_shell8_processed_u3_exclusions"][
        "decision"
    ] == "reject"
    assert audit["route_options"]["claim_uniform_M_tail_full_rank_from_shell8"][
        "decision"
    ] == "reject"


def test_wl509_stops_without_forbidden_work_or_selected_gate_advance() -> None:
    audit = _wl509()

    assert audit["post_wl508_route_choice_made_here"] is True
    assert audit["routing_audit_only"] is True
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_or_kernel_candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["new_local_row_proved_here"] is False
    assert audit["new_shell_or_grid_refreshed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["wl491_filter_applied_to_new_point_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["family_rank_or_selmer_diagnostics_run"] is False
    assert audit["single_curve_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_selected_next_gate"] is False
    assert audit["advance_to_wl510"] is False
    assert audit["stop_after_current_task"] is True


def test_wl509_cli_writes_result_json(tmp_path: Path) -> None:
    wl508_path = tmp_path / "wl508.json"
    out = tmp_path / "wl509.json"
    wl508_path.write_text(json.dumps(_wl508()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl509_post_wl508_empty_shell_route_choice_audit.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl508",
            str(wl508_path),
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
    assert "work_log=wl509" in result.stdout
    assert "selected_gate=execute_next_finite_M_tail_shell_from_wl498_plan" in result.stdout
    assert "shell_bound_to_execute_later=9" in result.stdout
    assert payload["work_log"] == "wl509"
    assert payload["selected_next_gate"]["shell_bound_to_execute_later"] == 9
