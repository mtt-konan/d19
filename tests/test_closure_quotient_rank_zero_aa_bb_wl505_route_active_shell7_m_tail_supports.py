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


def test_wl505_routes_exactly_the_twelve_active_shell7_supports() -> None:
    audit = _wl505()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL505_route_active_shell7_M_tail_supports_through_ambient_C_d_solubility_then_wl491_filter"
    )
    assert audit["work_log"] == "wl505"
    assert audit["input_work_logs"] == ["wl491", "wl504"]
    assert audit["route_summary"] == {
        "active_shell7_support_entry_count": 12,
        "processed_exclusions_reopened_count": 0,
        "ambient_globally_soluble_count": 8,
        "ambient_global_solubility_refuted_count": 0,
        "ambient_global_solubility_deferred_count": 4,
        "wl491_filter_applied_count": 8,
        "aa_bb_admissible_count": 0,
        "aa_bb_not_admissible_count": 8,
        "aa_bb_missing_pullback_data_count": 0,
        "aa_bb_filter_deferred_count": 4,
    }
    assert [entry["candidate_id"] for entry in audit["routed_active_shell7_supports"]] == [
        "AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate",
        "AA_A4_B7_w_5_m_tail_shell7_candidate",
        "AA_A6_B7_v_13_m_tail_shell7_candidate",
        "AA_A7_B2_u_7_m_tail_shell7_candidate",
        "AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate",
        "AA_A7_B6_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate",
        "BB_A2_B7_u_7_m_tail_shell7_candidate",
        "BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate",
        "BB_A6_B7_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate",
        "BB_A7_B3_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate",
        "BB_A7_B4_w_5_m_tail_shell7_candidate",
        "BB_A7_B6_v_13_m_tail_shell7_candidate",
    ]
    assert audit["processed_exclusions_not_reopened"] == [
        "AA_A6_B7_u_3_m_tail_shell7_candidate",
        "BB_A7_B6_u_3_m_tail_shell7_candidate",
    ]


def test_wl505_applies_wl491_only_after_exact_integral_ambient_points() -> None:
    audit = _wl505()
    soluble = [
        entry
        for entry in audit["routed_active_shell7_supports"]
        if entry["ambient_c_d_global_solubility"]["status"] == "globally_soluble"
    ]

    assert len(soluble) == 8
    first = soluble[0]
    assert first["candidate_id"] == (
        "AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate"
    )
    assert first["complete_c_d_cover"]["d_vector"] == {
        "d_minus_p": 15,
        "d_pos_2sqrt_q": 51,
        "d_neg_2sqrt_q": 85,
    }
    assert first["ambient_c_d_global_solubility"]["point_on_cover"] == {
        "X": 1088,
        "u_minus_p": 8,
        "u_pos_2sqrt_q": 4,
        "u_neg_2sqrt_q": 4,
    }
    assert first["ambient_c_d_global_solubility"]["induced_point_on_E_L"] == {
        "X": 1088,
        "Y": 32640,
    }
    assert first["wl491_filter_result"]["output_class"] == "not_admissible"
    assert first["routing_state"]["ledger_route"] == (
        "globally_soluble_but_not_aa_bb_admissible_ledger"
    )


def test_wl505_defers_unresolved_shell7_covers_without_filtering() -> None:
    audit = _wl505()
    deferred = [
        entry
        for entry in audit["routed_active_shell7_supports"]
        if entry["ambient_c_d_global_solubility"]["status"]
        == "global_solubility_deferred"
    ]

    assert [entry["candidate_id"] for entry in deferred] == [
        "AA_A4_B7_w_5_m_tail_shell7_candidate",
        "AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate",
        "BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate",
        "BB_A7_B4_w_5_m_tail_shell7_candidate",
    ]
    for entry in deferred:
        assert entry["wl491_filter_input"] == {}
        assert entry["wl491_filter_result"] == {
            "output_class": "not_applied",
            "reason": "ambient_global_C_d_solubility_not_established",
            "blocking_reasons": ["ambient_C_d_global_point_not_established"],
        }
        assert entry["routing_state"] == {
            "ambient_c_d_global_solubility_status": "global_solubility_deferred",
            "aa_bb_admissibility_status": "not_applied_ambient_global_solubility_unproved",
            "ledger_route": "ambient_c_d_solubility_deferred_ledger",
            "blocking_reasons": ["ambient_C_d_global_point_not_established"],
        }


def test_wl505_stops_without_candidate_selection_or_forbidden_claims() -> None:
    audit = _wl505()

    assert audit["route_audit_built_here"] is True
    assert audit["all_active_shell7_supports_classified_here"] is True
    assert audit["candidate_selected_here"] is False
    assert audit["new_m_tail_row_proved_here"] is False
    assert audit["new_local_row_proved_here"] is False
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
    assert audit["advance_to_wl506"] is False
    assert audit["stop_after_current_task"] is True


def test_wl505_cli_writes_result_json(tmp_path: Path) -> None:
    wl491 = tmp_path / "wl491.json"
    wl504 = tmp_path / "wl504.json"
    out = tmp_path / "wl505.json"
    wl491.write_text(json.dumps(_wl491_input()), encoding="utf-8")
    wl504.write_text(json.dumps(_wl504()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl505_route_active_shell7_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl491",
            str(wl491),
            "--wl504",
            str(wl504),
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
    assert "work_log=wl505" in result.stdout
    assert "ambient_globally_soluble_count=8" in result.stdout
    assert "ambient_global_solubility_deferred_count=4" in result.stdout
    assert "advance_to_wl506=False" in result.stdout
    assert payload["work_log"] == "wl505"
