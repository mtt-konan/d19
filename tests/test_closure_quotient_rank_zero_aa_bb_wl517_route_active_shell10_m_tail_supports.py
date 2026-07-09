from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl517_route_active_shell10_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter import (  # noqa: E501
    build_wl517_route_active_shell10_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter as build_wl517_route,  # noqa: E501
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl510_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
    _wl491_input,
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl516_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
    _wl516,
)


def _wl517() -> dict[str, object]:
    return build_wl517_route(wl491=_wl491_input(), wl516=_wl516())


def test_wl517_routes_exactly_the_ten_active_shell10_supports() -> None:
    audit = _wl517()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == (
        "WL517_route_active_shell10_M_tail_supports_through_ambient_C_d_solubility_then_wl491_filter"
    )
    assert audit["work_log"] == "wl517"
    assert audit["input_work_logs"] == ["wl491", "wl516"]
    assert audit["route_summary"] == {
        "active_shell10_support_entry_count": 10,
        "processed_exclusions_reopened_count": 0,
        "ambient_globally_soluble_count": 8,
        "ambient_global_solubility_refuted_count": 0,
        "ambient_global_solubility_deferred_count": 2,
        "wl491_filter_applied_count": 8,
        "aa_bb_admissible_count": 0,
        "aa_bb_not_admissible_count": 8,
        "aa_bb_missing_pullback_data_count": 0,
        "aa_bb_filter_deferred_count": 2,
    }
    assert [entry["candidate_id"] for entry in audit["routed_active_shell10_supports"]] == [
        "AA_A3_B10_u_3_plus_v_13_m_tail_shell10_candidate",
        "AA_A7_B10_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate",
        "AA_A10_B1_u_5_m_tail_shell10_candidate",
        "AA_A10_B7_v_17_plus_w_13_m_tail_shell10_candidate",
        "AA_A10_B9_u_5_m_tail_shell10_candidate",
        "BB_A1_B10_u_5_m_tail_shell10_candidate",
        "BB_A7_B10_v_17_plus_w_13_m_tail_shell10_candidate",
        "BB_A9_B10_u_5_m_tail_shell10_candidate",
        "BB_A10_B3_u_3_plus_v_13_m_tail_shell10_candidate",
        "BB_A10_B7_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate",
    ]
    assert audit["processed_exclusions_not_reopened"] == []


def test_wl517_applies_wl491_only_after_exact_integral_ambient_points() -> None:
    audit = _wl517()
    soluble = [
        entry
        for entry in audit["routed_active_shell10_supports"]
        if entry["ambient_c_d_global_solubility"]["status"] == "globally_soluble"
    ]

    assert [entry["candidate_id"] for entry in soluble] == [
        "AA_A3_B10_u_3_plus_v_13_m_tail_shell10_candidate",
        "AA_A7_B10_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate",
        "AA_A10_B1_u_5_m_tail_shell10_candidate",
        "AA_A10_B7_v_17_plus_w_13_m_tail_shell10_candidate",
        "BB_A1_B10_u_5_m_tail_shell10_candidate",
        "BB_A7_B10_v_17_plus_w_13_m_tail_shell10_candidate",
        "BB_A10_B3_u_3_plus_v_13_m_tail_shell10_candidate",
        "BB_A10_B7_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate",
    ]
    first = soluble[0]
    assert first["complete_c_d_cover"]["d_vector"] == {
        "d_minus_p": 39,
        "d_pos_2sqrt_q": 3,
        "d_neg_2sqrt_q": 13,
    }
    assert first["ambient_c_d_global_solubility"]["point_on_cover"] == {
        "X": 422,
        "u_minus_p": 2,
        "u_pos_2sqrt_q": 2,
        "u_neg_2sqrt_q": 8,
    }
    assert first["ambient_c_d_global_solubility"]["induced_point_on_E_L"] == {
        "X": 422,
        "Y": 1248,
    }
    assert first["wl491_filter_result"]["output_class"] == "not_admissible"
    assert first["routing_state"]["ledger_route"] == (
        "globally_soluble_but_not_aa_bb_admissible_ledger"
    )


def test_wl517_defers_unresolved_shell10_covers_without_filtering() -> None:
    audit = _wl517()
    deferred = [
        entry
        for entry in audit["routed_active_shell10_supports"]
        if entry["ambient_c_d_global_solubility"]["status"]
        == "global_solubility_deferred"
    ]

    assert [entry["candidate_id"] for entry in deferred] == [
        "AA_A10_B9_u_5_m_tail_shell10_candidate",
        "BB_A9_B10_u_5_m_tail_shell10_candidate",
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


def test_wl517_preserves_boundaries_and_stops_without_next_route() -> None:
    audit = _wl517()

    assert audit["route_audit_built_here"] is True
    assert audit["all_active_shell10_supports_classified_here"] is True
    assert audit["all_active_shell10_supports_fully_routed_here"] is False
    assert audit["shell11_executed_here"] is False
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
    assert audit["advance_to_wl518"] is False
    assert audit["stop_after_current_task"] is True


def test_wl517_cli_writes_result_json(tmp_path: Path) -> None:
    wl491 = tmp_path / "wl491.json"
    wl516 = tmp_path / "wl516.json"
    out = tmp_path / "wl517.json"
    wl491.write_text(json.dumps(_wl491_input()), encoding="utf-8")
    wl516.write_text(json.dumps(_wl516()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl517_route_active_shell10_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl491",
            str(wl491),
            "--wl516",
            str(wl516),
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
    assert "work_log=wl517" in result.stdout
    assert "ambient_globally_soluble_count=8" in result.stdout
    assert "ambient_global_solubility_deferred_count=2" in result.stdout
    assert "advance_to_wl518=False" in result.stdout
    assert payload["work_log"] == "wl517"
