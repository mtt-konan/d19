from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl502_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
    build_wl502_execute_next_finite_m_tail_shell_from_wl498_plan,
)


def _wl480_input() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D4_AA_BB_uniform_matrix_rank_bound_audit",
        "work_log": "wl480",
        "d4_status": "uniform_dim2_bound_not_forced_by_solved_rows",
        "complete_d_coordinate_order": [
            "d_minus_p",
            "d_pos_2sqrt_q",
            "d_neg_2sqrt_q",
        ],
        "local_character_matrix": {"id": "M_tail"},
        "surviving_obstruction": {"id": "M_tail_uniform_full_rank_missing"},
        "old_package_x_coordinate_collapse_used": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _wl501_input() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "WL501_post_wl500_route_choice_audit",
        "work_log": "wl501",
        "input_work_log": "wl500",
        "post_wl500_route_choice_made_here": True,
        "post_wl500_route_state_summary": {
            "shell5_active_u5_support_entry_count_from_wl500": 2,
            "shell5_ambient_global_solubility_refuted_count_from_wl500": 2,
            "shell5_ambient_global_solubility_still_deferred_count_after_wl500": 0,
            "shell5_wl491_filter_applied_count_from_wl500": 0,
            "aa_bb_admissible_count_after_wl500": 0,
            "active_candidate_count_after_wl500": 0,
            "completed_finite_shell_bound_after_wl500": 5,
        },
        "closed_ledger_do_not_reopen": [
            "u_3_processed_or_deprioritized_after_wl493_wl491",
            "bounded_v_5_entries_disposed_by_wl495_wl496",
            "shell5_u_5_entries_refuted_by_wl500",
        ],
        "selected_next_gate": {
            "gate": "execute_next_finite_M_tail_shell_from_wl498_plan",
            "entered_here": False,
            "uses_existing_wl498_plan": True,
            "shell_bound_to_execute_later": 6,
            "new_shell_or_grid_refreshed_here": False,
            "m_tail_diagnostics_extended_here": False,
            "new_supports_computed_here": False,
            "new_c_d_solubility_tested_here": False,
            "wl491_filter_applied_here": False,
        },
        "candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_c_d_solubility_tested_here": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "family_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "advance_to_wl502": False,
    }


def _wl502() -> dict[str, object]:
    return build_wl502_execute_next_finite_m_tail_shell_from_wl498_plan(
        wl480=_wl480_input(),
        wl501=_wl501_input(),
        shell_bound=6,
    )


def test_wl502_executes_exactly_shell6_from_wl501_gate() -> None:
    audit = _wl502()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL502_execute_next_finite_M_tail_shell_from_wl498_plan"
    assert audit["work_log"] == "wl502"
    assert audit["input_work_logs"] == ["wl480", "wl501"]
    assert audit["declared_extension_scope"] == {
        "extension_unit": "finite_primitive_shell",
        "shell_bound": 6,
        "shell_axis": "max(A,B)",
        "sides": ["AA", "BB"],
        "primitive_condition": "gcd(A,B)=1",
        "sample_order": "side, then A ascending, then B ascending",
        "sample_count": 8,
        "uses_existing_wl481_matrix_builder": True,
        "uses_wl498_duplicate_support_guard": True,
        "uses_wl501_closed_ledger_exclusions": True,
    }
    assert audit["sample_summary"] == {
        "sample_count": 8,
        "full_rank_sample_count": 8,
        "kernel_sample_count": 0,
        "kernel_support_entry_count": 0,
        "active_new_support_entry_count": 0,
        "excluded_duplicate_or_processed_support_entry_count": 0,
        "unique_active_supports": [],
    }


def test_wl502_outputs_only_m_tail_diagnostic_queues_and_applies_exclusions() -> None:
    audit = _wl502()

    assert audit["active_new_kernel_supports"] == []
    assert audit["excluded_duplicate_or_processed_supports"] == []
    assert audit["duplicate_support_guard_summary"] == {
        "route_key_fields": [
            "source_quotient",
            "A",
            "B",
            "L",
            "T",
            "candidate_support",
        ],
        "processed_support_family_exclusion_count": 1,
        "bounded_route_key_exclusion_count": 6,
        "shell5_closed_route_key_exclusion_count": 2,
        "candidate_id_collision_exclusion_count": 8,
        "active_new_support_entry_count": 0,
        "excluded_duplicate_or_processed_support_entry_count": 0,
    }
    assert audit["closed_ledger_exclusions_applied"] == [
        "u_3_processed_or_deprioritized_after_wl493_wl491",
        "bounded_v_5_entries_disposed_by_wl495_wl496",
        "shell5_u_5_entries_refuted_by_wl500",
    ]


def test_wl502_stops_before_c_d_wl491_final_candidate_or_wl503() -> None:
    audit = _wl502()

    assert audit["m_tail_diagnostics_extended_here"] is True
    assert audit["new_supports_computed_here"] is True
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_or_kernel_candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["new_local_row_proved_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["ambient_c_d_solubility_proved_for_new_candidate_here"] is False
    assert audit["wl491_filter_applied_here"] is False
    assert audit["aa_bb_admissibility_proved_for_new_candidate_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["family_rank_or_selmer_diagnostics_run"] is False
    assert audit["single_curve_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_wl503"] is False
    assert audit["stop_after_current_task"] is True


def test_wl502_cli_writes_result_json(tmp_path: Path) -> None:
    wl480 = tmp_path / "wl480.json"
    wl501 = tmp_path / "wl501.json"
    out = tmp_path / "wl502.json"
    wl480.write_text(json.dumps(_wl480_input()), encoding="utf-8")
    wl501.write_text(json.dumps(_wl501_input()), encoding="utf-8")

    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl502_execute_next_finite_m_tail_shell_from_wl498_plan.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl480",
            str(wl480),
            "--wl501",
            str(wl501),
            "--shell-bound",
            "6",
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
    assert "work_log=wl502" in result.stdout
    assert "active_new_support_entry_count=0" in result.stdout
    assert "excluded_duplicate_or_processed_support_entry_count=0" in result.stdout
    assert payload["work_log"] == "wl502"
    assert payload["active_new_kernel_supports"] == []
