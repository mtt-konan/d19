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


def _wl504() -> dict[str, object]:
    wl502 = build_wl502_execute_next_finite_m_tail_shell_from_wl498_plan(
        wl480=_wl480_input(),
        wl501=_wl501_input(),
        shell_bound=6,
    )
    wl503 = build_wl503_post_wl502_empty_shell_route_choice_audit(wl502=wl502)
    return build_wl504_execute_next_finite_m_tail_shell_from_wl498_plan(
        wl480=_wl480_input(),
        wl503=wl503,
        shell_bound=7,
    )


def _wl505() -> dict[str, object]:
    return build_wl505_route(
        wl491=_wl491_input(),
        wl504=_wl504(),
    )


def _wl506() -> dict[str, object]:
    return build_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers(
        wl491=_wl491_input(),
        wl505=_wl505(),
    )


def _wl507() -> dict[str, object]:
    return build_wl507_post_wl506_route_choice_audit(wl506=_wl506())


def test_wl507_summarizes_disposed_shell7_route_without_reopening_ledgers() -> None:
    audit = _wl507()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL507_post_wl506_route_choice_audit"
    assert audit["work_log"] == "wl507"
    assert audit["input_work_log"] == "wl506"
    assert audit["post_wl506_route_state_summary"] == {
        "completed_finite_shell_bound_after_wl506": 7,
        "shell7_deferred_entry_count_from_wl506": 4,
        "shell7_deferred_entries_resolved_by_wl506": 4,
        "shell7_ambient_global_solubility_refuted_count_from_wl506": 2,
        "shell7_globally_soluble_not_admissible_count_from_wl506": 2,
        "shell7_ambient_global_solubility_still_deferred_count_after_wl506": 0,
        "shell7_wl491_filter_applied_count_from_wl506": 2,
        "aa_bb_admissible_count_after_wl506": 0,
        "active_candidate_count_after_wl506": 0,
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
    ]


def test_wl507_selects_shell8_gate_but_does_not_execute_it() -> None:
    audit = _wl507()

    selected = audit["selected_next_gate"]
    assert selected["gate"] == "execute_next_finite_M_tail_shell_from_wl498_plan"
    assert selected["entered_here"] is False
    assert selected["uses_existing_wl498_plan"] is True
    assert selected["shell_bound_to_execute_later"] == 8
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
    assert audit["route_options"]["reopen_shell7_ambient_ledgers"]["decision"] == "reject"
    assert audit["route_options"]["select_final_obstruction_candidate"]["decision"] == "reject"


def test_wl507_stops_without_forbidden_work_or_wl508_advance() -> None:
    audit = _wl507()

    assert audit["post_wl506_route_choice_made_here"] is True
    assert audit["routing_audit_only"] is True
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_or_kernel_candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["new_local_row_proved_here"] is False
    assert audit["new_shell_or_grid_refreshed_here"] is False
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
    assert audit["advance_to_wl508"] is False
    assert audit["stop_after_current_task"] is True


def test_wl507_cli_writes_result_json(tmp_path: Path) -> None:
    wl506_path = tmp_path / "wl506.json"
    out = tmp_path / "wl507.json"
    wl506_path.write_text(json.dumps(_wl506()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl507_post_wl506_route_choice_audit.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl506",
            str(wl506_path),
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
    assert "work_log=wl507" in result.stdout
    assert "selected_gate=execute_next_finite_M_tail_shell_from_wl498_plan" in result.stdout
    assert "shell_bound_to_execute_later=8" in result.stdout
    assert payload["work_log"] == "wl507"
    assert payload["selected_next_gate"]["shell_bound_to_execute_later"] == 8
