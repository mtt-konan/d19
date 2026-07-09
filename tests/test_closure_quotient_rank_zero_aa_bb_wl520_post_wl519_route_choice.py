from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl520_post_wl519_route_choice_audit import (  # noqa: E501
    build_wl520_post_wl519_route_choice_audit,
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl519_resolve_shared_shell10_u5 import (
    _wl519,
)


def _wl520() -> dict[str, object]:
    return build_wl520_post_wl519_route_choice_audit(wl519=_wl519())


def test_wl520_summarizes_post_wl519_closed_state_without_reopening_ledgers() -> None:
    audit = _wl520()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL520_post_wl519_route_choice_audit"
    assert audit["work_log"] == "wl520"
    assert audit["input_work_log"] == "wl519"
    assert audit["post_wl519_route_state_summary"] == {
        "wl518_deferred_cover_families_classified_after_wl519": 1,
        "wl519_globally_soluble_not_admissible_count": 2,
        "shell10_remaining_deferred_count_after_wl519": 0,
        "shell10_aa_bb_admissible_count_after_wl519": 0,
        "active_final_candidate_count_after_wl519": 0,
    }
    assert audit["closed_ledger_do_not_reopen"] == [
        "u_3_processed_or_deprioritized_after_wl493_wl491",
        "bounded_v_5_entries_disposed_by_wl495_wl496",
        "shell5_u_5_entries_refuted_by_wl500",
        "shell6_empty_diagnostic_output_from_wl502",
        "shell7_entries_disposed_by_wl505_wl506",
        "shell8_pure_u_3_processed_exclusions_from_wl508",
        "shell9_entries_disposed_by_wl511_wl512_wl514",
        "shell10_globally_soluble_not_admissible_ledgers_from_wl517",
        "shell10_u_5_mirror_ledgers_not_admissible_from_wl519",
    ]
    assert audit["wl519_not_admissible_ledgers_reopened_count"] == 0
    assert audit["shell9_ledgers_reopened_count"] == 0
    assert audit["previous_refuted_covers_reopened_count"] == 0
    assert audit["closed_ledgers_reopened_count"] == 0


def test_wl520_selects_post_classification_family_synthesis_but_does_not_enter_it() -> None:
    audit = _wl520()

    selected = audit["selected_next_gate"]
    assert selected["gate"] == "synthesize_support_and_cover_families_after_wl519"
    assert selected["entered_here"] is False
    assert selected["input_work_logs_to_use_later"] == [f"wl{index}" for index in range(491, 520)]
    assert selected["purpose"] == "derive_reusable_theorem_candidate_patterns"
    assert selected["not_a_theorem_claim"] is True
    assert selected["new_shell_or_grid_refreshed_here"] is False
    assert selected["m_tail_diagnostics_extended_here"] is False
    assert selected["new_supports_computed_here"] is False
    assert selected["new_c_d_solubility_tested_here"] is False
    assert selected["wl491_filter_applied_here"] is False
    assert selected["candidate_selected_here"] is False
    assert audit["route_options"][
        "support_family_cover_family_synthesis_toward_reusable_theorem_candidate_patterns"
    ]["decision"] == "selected_next_narrow_gate"
    assert audit["route_options"]["execute_shell11_from_existing_wl498_plan"][
        "decision"
    ] == "defer"
    assert audit["route_options"]["proof_level_generalization_or_local_row_work"][
        "decision"
    ] == "defer_without_named_theorem_gap"
    assert audit["route_options"]["final_candidate_selection"]["decision"] == "reject"


def test_wl520_stops_without_forbidden_work_or_selected_gate_advance() -> None:
    audit = _wl520()

    assert audit["post_wl519_route_choice_made_here"] is True
    assert audit["routing_audit_only"] is True
    assert audit["support_family_synthesis_built_here"] is False
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
    assert audit["shell11_executed_here"] is False
    assert audit["advance_to_selected_next_gate"] is False
    assert audit["advance_to_wl521"] is False
    assert audit["stop_after_current_task"] is True


def test_wl520_cli_writes_result_json(tmp_path: Path) -> None:
    wl519_path = tmp_path / "wl519.json"
    out = tmp_path / "wl520.json"
    wl519_path.write_text(json.dumps(_wl519()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl520_post_wl519_route_choice_audit.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl519",
            str(wl519_path),
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
    assert "work_log=wl520" in result.stdout
    assert "selected_gate=synthesize_support_and_cover_families_after_wl519" in result.stdout
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl520"
    assert payload["selected_next_gate"]["entered_here"] is False
