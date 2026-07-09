from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl516_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
    build_wl516_execute_next_finite_m_tail_shell_from_wl498_plan,
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl510_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
    _wl480_input,
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl515_post_wl514_route_choice import (
    _wl515,
)


def _wl516() -> dict[str, object]:
    return build_wl516_execute_next_finite_m_tail_shell_from_wl498_plan(
        wl480=_wl480_input(),
        wl515=_wl515(),
        shell_bound=10,
    )


def test_wl516_executes_exactly_shell10_from_wl515_gate() -> None:
    audit = _wl516()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL516_execute_next_finite_M_tail_shell_from_wl498_plan"
    assert audit["work_log"] == "wl516"
    assert audit["input_work_logs"] == ["wl480", "wl515"]
    assert audit["declared_extension_scope"] == {
        "extension_unit": "finite_primitive_shell",
        "shell_bound": 10,
        "shell_axis": "max(A,B)",
        "sides": ["AA", "BB"],
        "primitive_condition": "gcd(A,B)=1",
        "sample_order": "side, then A ascending, then B ascending",
        "sample_count": 16,
        "uses_existing_wl481_matrix_builder": True,
        "uses_wl498_duplicate_support_guard": True,
        "uses_wl515_closed_ledger_exclusions": True,
    }
    assert audit["sample_summary"] == {
        "sample_count": 16,
        "full_rank_sample_count": 6,
        "kernel_sample_count": 10,
        "kernel_support_entry_count": 10,
        "active_new_support_entry_count": 10,
        "excluded_duplicate_or_processed_support_entry_count": 0,
        "unique_active_supports": [
            "u_3",
            "u_5",
            "u_7",
            "v_13",
            "v_17",
            "w_13",
            "w_5",
        ],
    }


def test_wl516_records_shell10_active_and_excluded_m_tail_queues() -> None:
    audit = _wl516()

    assert [
        entry["candidate_id"] for entry in audit["active_new_kernel_supports"]
    ] == [
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
    assert audit["excluded_duplicate_or_processed_supports"] == []
    assert audit["closed_ledger_exclusions_applied"] == [
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
        "shell9_closed_route_key_exclusion_count": 8,
        "candidate_id_collision_exclusion_count": 32,
        "active_new_support_entry_count": 10,
        "excluded_duplicate_or_processed_support_entry_count": 0,
    }


def test_wl516_stops_before_c_d_wl491_final_candidate_or_next_route() -> None:
    audit = _wl516()

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
    assert audit["advance_to_wl517"] is False
    assert audit["stop_after_current_task"] is True


def test_wl516_cli_writes_result_json(tmp_path: Path) -> None:
    wl480 = tmp_path / "wl480.json"
    wl515 = tmp_path / "wl515.json"
    out = tmp_path / "wl516.json"
    wl480.write_text(json.dumps(_wl480_input()), encoding="utf-8")
    wl515.write_text(json.dumps(_wl515()), encoding="utf-8")

    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl516_execute_next_finite_m_tail_shell_from_wl498_plan.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl480",
            str(wl480),
            "--wl515",
            str(wl515),
            "--shell-bound",
            "10",
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
    assert "work_log=wl516" in result.stdout
    assert "active_new_support_entry_count=10" in result.stdout
    assert "excluded_duplicate_or_processed_support_entry_count=0" in result.stdout
    assert payload["work_log"] == "wl516"
    assert len(payload["active_new_kernel_supports"]) == 10
