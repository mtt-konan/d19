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


def test_wl506_resolves_exactly_the_four_wl505_deferred_shell7_ledgers() -> None:
    audit = _wl506()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL506_resolve_shell7_deferred_ambient_C_d_global_solubility_ledgers"
    )
    assert audit["work_log"] == "wl506"
    assert audit["input_work_logs"] == ["wl491", "wl505"]
    assert audit["resolution_summary"] == {
        "wl505_deferred_entry_count": 4,
        "explicitly_classified_entry_count": 4,
        "ambient_globally_soluble_count": 2,
        "ambient_global_solubility_refuted_count": 2,
        "ambient_global_solubility_still_deferred_count": 0,
        "wl491_filter_applied_count": 2,
        "aa_bb_admissible_count": 0,
        "aa_bb_not_admissible_count": 2,
        "aa_bb_missing_pullback_data_count": 0,
        "aa_bb_filter_not_applied_count": 2,
    }
    assert [entry["candidate_id"] for entry in audit["resolved_deferred_entries"]] == [
        "AA_A4_B7_w_5_m_tail_shell7_candidate",
        "AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate",
        "BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate",
        "BB_A7_B4_w_5_m_tail_shell7_candidate",
    ]
    assert audit["shell7_globally_soluble_not_admissible_reopened_count"] == 0
    assert audit["shell7_processed_u3_exclusions_reopened_count"] == 0


def test_wl506_refutes_the_two_w5_deferred_ledgers_without_wl491() -> None:
    audit = _wl506()
    refuted = [
        entry
        for entry in audit["resolved_deferred_entries"]
        if entry["candidate_support"] == ["w_5"]
    ]

    assert [entry["candidate_id"] for entry in refuted] == [
        "AA_A4_B7_w_5_m_tail_shell7_candidate",
        "BB_A7_B4_w_5_m_tail_shell7_candidate",
    ]
    for entry in refuted:
        assert entry["complete_c_d_cover"]["d_vector"] == {
            "d_minus_p": 1,
            "d_pos_2sqrt_q": 5,
            "d_neg_2sqrt_q": 5,
        }
        assert entry["ambient_c_d_global_solubility"]["status"] == (
            "globally_not_soluble"
        )
        assert entry["ambient_c_d_global_solubility"]["certificate_type"] == (
            "targeted_mordell_weil_torsion_lift_refutation"
        )
        assert entry["ambient_c_d_global_solubility"]["rank_zero_certificate"] == {
            "rank": 0,
            "torsion_points": ["O", "(-370,0)", "(114,0)", "(370,0)"],
            "scope": "single instantiated curve E_{L=4,T=11}, not a family theorem",
        }
        assert entry["wl491_filter_result"]["output_class"] == "not_applied"
        assert entry["routing_state"]["ledger_route"] == (
            "ambient_c_d_global_solubility_refuted_ledger"
        )


def test_wl506_solves_the_two_u7_w37_ledgers_then_applies_wl491() -> None:
    audit = _wl506()
    soluble = [
        entry
        for entry in audit["resolved_deferred_entries"]
        if entry["candidate_support"] == ["u_7", "w_37"]
    ]

    assert [entry["candidate_id"] for entry in soluble] == [
        "AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate",
        "BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate",
    ]
    for entry in soluble:
        certificate = entry["ambient_c_d_global_solubility"]
        assert certificate["status"] == "globally_soluble"
        assert certificate["certificate_type"] == (
            "targeted_mordell_weil_cover_lift_certificate"
        )
        assert certificate["mordell_weil_point_source"] == {
            "curve_generator": "G=(-304,5376)",
            "torsion_translate": "T=(-592,0)",
            "point_expression": "-49*G + T",
            "curve_rank_scope": "single instantiated curve E_{L=7,T=10}, not a family theorem",
        }
        assert certificate["cover_lift_summary"] == {
            "cover_equation_count_checked": 3,
            "cover_equations_all_satisfied": True,
            "point_on_E_L_matches_cover_product": True,
        }
        assert len(certificate["point_on_cover"]["X"]) > 1000
        assert entry["wl491_filter_result"]["output_class"] == "not_admissible"
        assert entry["routing_state"]["ledger_route"] == (
            "globally_soluble_but_not_aa_bb_admissible_ledger"
        )


def test_wl506_stops_without_candidate_selection_or_forbidden_claims() -> None:
    audit = _wl506()

    assert audit["resolved_wl505_deferred_ledgers_here"] is True
    assert audit["all_wl505_deferred_entries_resolved_here"] is True
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
    assert audit["advance_to_wl507"] is False
    assert audit["stop_after_current_task"] is True


def test_wl506_cli_writes_result_json(tmp_path: Path) -> None:
    wl491 = tmp_path / "wl491.json"
    wl505 = tmp_path / "wl505.json"
    out = tmp_path / "wl506.json"
    wl491.write_text(json.dumps(_wl491_input()), encoding="utf-8")
    wl505.write_text(json.dumps(_wl505()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl491",
            str(wl491),
            "--wl505",
            str(wl505),
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
    assert "work_log=wl506" in result.stdout
    assert "ambient_globally_soluble_count=2" in result.stdout
    assert "ambient_global_solubility_refuted_count=2" in result.stdout
    assert "advance_to_wl507=False" in result.stdout
    assert payload["work_log"] == "wl506"
