from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl513_post_wl512_route_choice_audit import (  # noqa: E501
    build_wl513_post_wl512_route_choice_audit,
)
from tests.test_closure_quotient_rank_zero_aa_bb_wl512_resolve_shell9_deferred_ambient_c_d import (
    _wl512,
)


def _wl513() -> dict[str, object]:
    return build_wl513_post_wl512_route_choice_audit(wl512=_wl512())


def test_wl513_summarizes_remaining_u7_gap_without_reopening_closed_ledgers() -> None:
    audit = _wl513()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL513_post_wl512_route_choice_audit"
    assert audit["work_log"] == "wl513"
    assert audit["input_work_log"] == "wl512"
    assert audit["post_wl512_route_state_summary"] == {
        "wl512_deferred_entry_count": 4,
        "wl512_explicitly_classified_entry_count": 4,
        "shell9_v13_refuted_count_from_wl512": 2,
        "shell9_u7_still_deferred_count_after_wl512": 2,
        "shell9_wl491_filter_applied_count_from_wl512": 0,
        "aa_bb_admissible_count_after_wl512": 0,
        "active_candidate_count_after_wl512": 0,
    }
    assert audit["remaining_deferred_candidate_ids"] == [
        "AA_A7_B9_u_7_m_tail_shell9_candidate",
        "BB_A9_B7_u_7_m_tail_shell9_candidate",
    ]
    assert audit["remaining_deferred_shared_cover"] == {
        "L": 7,
        "T": 16,
        "d_vector": {
            "d_minus_p": 7,
            "d_pos_2sqrt_q": 7,
            "d_neg_2sqrt_q": 1,
        },
        "elliptic_curve_model": (
            "V^2 = (X + 120)*(X - 904)*(X + 904)"
        ),
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
    ]
    assert audit["shell9_not_admissible_ledgers_reopened_count"] == 0
    assert audit["shell9_v13_refuted_ledgers_reopened_count"] == 0
    assert audit["closed_ledgers_reopened_count"] == 0


def test_wl513_selects_targeted_u7_cover_resolution_but_does_not_enter_it() -> None:
    audit = _wl513()

    selected = audit["selected_next_gate"]
    assert selected["gate"] == (
        "resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers"
    )
    assert selected["entered_here"] is False
    assert selected["candidate_ids"] == [
        "AA_A7_B9_u_7_m_tail_shell9_candidate",
        "BB_A9_B7_u_7_m_tail_shell9_candidate",
    ]
    assert selected["shared_cover"] == "L=7,T=16,d=(7,7,1)"
    assert selected["minimum_later_question"] == (
        "Resolve the shared shell-9 u_7 ambient C_d cover at "
        "L=7,T=16,d=(7,7,1) by either an exact ambient point or an "
        "exhaustive no-lift certificate; only after global solubility is "
        "established may wl491 be applied."
    )
    assert selected["shell10_executed_here"] is False
    assert selected["new_local_row_proved_here"] is False
    assert selected["broad_rank_or_selmer_diagnostics_run"] is False
    assert selected["candidate_selected_here"] is False
    assert audit["route_options"][
        "resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers"
    ]["decision"] == "selected_next_narrow_gate"
    assert audit["route_options"]["execute_shell10_from_wl498_plan"]["decision"] == (
        "reject"
    )
    assert audit["route_options"]["reopen_shell9_v13_or_not_admissible_ledgers"][
        "decision"
    ] == "reject"
    assert audit["route_options"]["prove_local_or_hilbert_rows_now"]["decision"] == (
        "future_gate_only"
    )


def test_wl513_stops_without_forbidden_work_or_wl514_advance() -> None:
    audit = _wl513()

    assert audit["post_wl512_route_choice_made_here"] is True
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
    assert audit["advance_to_wl514"] is False
    assert audit["stop_after_current_task"] is True


def test_wl513_cli_writes_result_json(tmp_path: Path) -> None:
    wl512_path = tmp_path / "wl512.json"
    out = tmp_path / "wl513.json"
    wl512_path.write_text(json.dumps(_wl512()), encoding="utf-8")
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl513_post_wl512_route_choice_audit.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl512",
            str(wl512_path),
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
    assert "work_log=wl513" in result.stdout
    assert (
        "selected_gate=resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers"
        in result.stdout
    )
    assert "remaining_deferred_count=2" in result.stdout
    assert payload["work_log"] == "wl513"
    assert payload["selected_next_gate"]["entered_here"] is False
