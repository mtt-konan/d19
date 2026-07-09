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
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl503_post_wl502_empty_shell_route_choice_audit import (  # noqa: E501
    build_wl503_post_wl502_empty_shell_route_choice_audit,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl504_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
    build_wl504_execute_next_finite_m_tail_shell_from_wl498_plan,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl505_route_active_shell7_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter import (  # noqa: E501
    build_wl505_route_active_shell7_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter as build_wl505_route,  # noqa: E501
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers import (  # noqa: E501
    build_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl507_post_wl506_route_choice_audit import (  # noqa: E501
    build_wl507_post_wl506_route_choice_audit,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl508_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
    build_wl508_execute_next_finite_m_tail_shell_from_wl498_plan,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl509_post_wl508_empty_shell_route_choice_audit import (  # noqa: E501
    build_wl509_post_wl508_empty_shell_route_choice_audit,
)
from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl510_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
    build_wl510_execute_next_finite_m_tail_shell_from_wl498_plan,
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


def _wl491_input() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "WL491_reusable_ambient_C_d_to_AA_BB_admissibility_filter",
        "work_log": "wl491",
        "admissibility_filter_defined_here": True,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
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


def _wl509() -> dict[str, object]:
    wl502 = build_wl502_execute_next_finite_m_tail_shell_from_wl498_plan(
        wl480=_wl480_input(),
        wl501=_wl501_input(),
        shell_bound=6,
    )
    wl503 = build_wl503_post_wl502_empty_shell_route_choice_audit(wl502=wl502)
    wl504 = build_wl504_execute_next_finite_m_tail_shell_from_wl498_plan(
        wl480=_wl480_input(),
        wl503=wl503,
        shell_bound=7,
    )
    wl505 = build_wl505_route(wl491=_wl491_input(), wl504=wl504)
    wl506 = build_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers(
        wl491=_wl491_input(),
        wl505=wl505,
    )
    wl507 = build_wl507_post_wl506_route_choice_audit(wl506=wl506)
    wl508 = build_wl508_execute_next_finite_m_tail_shell_from_wl498_plan(
        wl480=_wl480_input(),
        wl507=wl507,
        shell_bound=8,
    )
    return build_wl509_post_wl508_empty_shell_route_choice_audit(wl508=wl508)


def _wl510() -> dict[str, object]:
    return build_wl510_execute_next_finite_m_tail_shell_from_wl498_plan(
        wl480=_wl480_input(),
        wl509=_wl509(),
        shell_bound=9,
    )


def test_wl510_executes_exactly_shell9_from_wl509_gate() -> None:
    audit = _wl510()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL510_execute_next_finite_M_tail_shell_from_wl498_plan"
    assert audit["work_log"] == "wl510"
    assert audit["input_work_logs"] == ["wl480", "wl509"]
    assert audit["declared_extension_scope"] == {
        "extension_unit": "finite_primitive_shell",
        "shell_bound": 9,
        "shell_axis": "max(A,B)",
        "sides": ["AA", "BB"],
        "primitive_condition": "gcd(A,B)=1",
        "sample_order": "side, then A ascending, then B ascending",
        "sample_count": 24,
        "uses_existing_wl481_matrix_builder": True,
        "uses_wl498_duplicate_support_guard": True,
        "uses_wl509_closed_ledger_exclusions": True,
    }
    assert audit["sample_summary"] == {
        "sample_count": 24,
        "full_rank_sample_count": 16,
        "kernel_sample_count": 8,
        "kernel_support_entry_count": 8,
        "active_new_support_entry_count": 8,
        "excluded_duplicate_or_processed_support_entry_count": 0,
        "unique_active_supports": ["u_3", "u_7", "v_13", "v_5", "w_53"],
    }


def test_wl510_records_only_active_and_excluded_m_tail_queues() -> None:
    audit = _wl510()

    assert [
        entry["candidate_id"] for entry in audit["active_new_kernel_supports"]
    ] == [
        "AA_A4_B9_v_13_m_tail_shell9_candidate",
        "AA_A7_B9_u_7_m_tail_shell9_candidate",
        "AA_A9_B1_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate",
        "AA_A9_B4_v_13_m_tail_shell9_candidate",
        "BB_A1_B9_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate",
        "BB_A4_B9_v_13_m_tail_shell9_candidate",
        "BB_A9_B4_v_13_m_tail_shell9_candidate",
        "BB_A9_B7_u_7_m_tail_shell9_candidate",
    ]
    assert audit["excluded_duplicate_or_processed_supports"] == []
    assert audit["closed_ledger_exclusions_applied"] == [
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
        "shell6_closed_route_key_exclusion_count": 0,
        "shell7_closed_route_key_exclusion_count": 14,
        "shell8_closed_route_key_exclusion_count": 2,
        "candidate_id_collision_exclusion_count": 24,
        "active_new_support_entry_count": 8,
        "excluded_duplicate_or_processed_support_entry_count": 0,
    }


def test_wl510_stops_before_c_d_wl491_final_candidate_or_wl511() -> None:
    audit = _wl510()

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
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_wl511"] is False
    assert audit["stop_after_current_task"] is True


def test_wl510_cli_writes_result_json(tmp_path: Path) -> None:
    wl480 = tmp_path / "wl480.json"
    wl509 = tmp_path / "wl509.json"
    out = tmp_path / "wl510.json"
    wl480.write_text(json.dumps(_wl480_input()), encoding="utf-8")
    wl509.write_text(json.dumps(_wl509()), encoding="utf-8")

    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl510_execute_next_finite_m_tail_shell_from_wl498_plan.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl480",
            str(wl480),
            "--wl509",
            str(wl509),
            "--shell-bound",
            "9",
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
    assert "work_log=wl510" in result.stdout
    assert "active_new_support_entry_count=8" in result.stdout
    assert "excluded_duplicate_or_processed_support_entry_count=0" in result.stdout
    assert payload["work_log"] == "wl510"
    assert len(payload["active_new_kernel_supports"]) == 8
