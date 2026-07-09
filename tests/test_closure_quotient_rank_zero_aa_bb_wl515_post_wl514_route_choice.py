from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl515_post_wl514_route_choice_audit import (  # noqa: E501
    build_wl515_post_wl514_route_choice_audit,
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl514_resolve_remaining_shell9_u7_ambient_c_d import (  # noqa: E501
    _wl514,
)


def _wl515() -> dict[str, object]:
    return build_wl515_post_wl514_route_choice_audit(wl514=_wl514())


def test_wl515_summarizes_closed_shell9_state_without_reopening_ledgers() -> None:
    audit = _wl515()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL515_post_wl514_route_choice_audit"
    assert audit["work_log"] == "wl515"
    assert audit["input_work_log"] == "wl514"
    assert audit["post_wl514_route_state_summary"] == {
        "wl511_globally_soluble_not_admissible_count": 4,
        "wl512_v13_refuted_count": 2,
        "wl514_u7_refuted_count": 2,
        "shell9_remaining_deferred_count_after_wl514": 0,
        "shell9_aa_bb_admissible_count_after_wl514": 0,
        "active_candidate_count_after_wl514": 0,
    }
    assert audit["closed_ledger_do_not_reopen"] == [
        "u_3_processed_or_deprioritized_after_wl493_wl491",
        "bounded_v_5_entries_disposed_by_wl495_wl496",
        "shell5_u_5_entries_refuted_by_wl500",
        "shell6_empty_diagnostic_output_from_wl502",
        "shell7_entries_disposed_by_wl505_wl506",
        "shell8_pure_u_3_processed_exclusions_from_wl508",
        "shell9_globally_soluble_not_admissible_ledgers_from_wl511",
        "shell9_v_13_deferred_ledgers_refuted_by_wl512",
        "shell9_u_7_deferred_ledgers_refuted_by_wl514",
    ]
    assert audit["shell9_not_admissible_ledgers_reopened_count"] == 0
    assert audit["shell9_v13_refuted_ledgers_reopened_count"] == 0
    assert audit["shell9_u7_refuted_ledgers_reopened_count"] == 0
    assert audit["closed_ledgers_reopened_count"] == 0


def test_wl515_selects_shell10_gate_but_does_not_execute_it() -> None:
    audit = _wl515()

    selected = audit["selected_next_gate"]
    assert selected["gate"] == "execute_next_finite_M_tail_shell_from_wl498_plan"
    assert selected["entered_here"] is False
    assert selected["uses_existing_wl498_plan"] is True
    assert selected["shell_bound_to_execute_later"] == 10
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
    assert audit["route_options"]["pivot_to_proof_level_route_choice_now"][
        "decision"
    ] == "reject_without_specific_proof_gap"
    assert audit["route_options"]["reopen_closed_shell9_ledgers"]["decision"] == (
        "reject"
    )
    assert audit["route_options"]["select_final_obstruction_candidate"][
        "decision"
    ] == "reject"


def test_wl515_stops_without_forbidden_work_or_selected_gate_advance() -> None:
    audit = _wl515()

    assert audit["post_wl514_route_choice_made_here"] is True
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
    assert audit["search_count_used_as_progress"] is False
    assert audit["shell10_executed_here"] is False
    assert audit["advance_to_selected_next_gate"] is False
    assert audit["advance_to_wl516"] is False
    assert audit["stop_after_current_task"] is True


def test_wl515_cli_writes_result_json(tmp_path: Path) -> None:
    wl514_path = tmp_path / "wl514.json"
    out = tmp_path / "wl515.json"
    wl514_path.write_text(json.dumps(_wl514()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl515_post_wl514_route_choice_audit.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl514",
            str(wl514_path),
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
    assert "work_log=wl515" in result.stdout
    assert "selected_gate=execute_next_finite_M_tail_shell_from_wl498_plan" in result.stdout
    assert "shell_bound_to_execute_later=10" in result.stdout
    assert payload["work_log"] == "wl515"
    assert payload["selected_next_gate"]["shell_bound_to_execute_later"] == 10
