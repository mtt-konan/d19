from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice_audit import (  # noqa: E501
    build_wl524_post_wl523_route_choice_audit,
)


def _wl523() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / "results/"
            "closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate.json"
        ).read_text(encoding="utf-8")
    )


def _wl524() -> dict[str, object]:
    return build_wl524_post_wl523_route_choice_audit(wl523=_wl523())


def test_wl524_summarizes_post_wl523_route_state() -> None:
    audit = _wl524()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL524_post_wl523_route_choice_audit"
    assert audit["work_log"] == "wl524"
    assert audit["input_work_log"] == "wl523"
    assert audit["routing_audit_only"] is True
    assert audit["post_wl523_route_state_summary"] == {
        "point_level_square_obstruction_status": (
            "provable_from_existing_wl491_machinery"
        ),
        "uniform_cover_family_squareclass_theorem_status": (
            "needs_new_uniform_squareclass_lemma"
        ),
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": 15,
        "globally_soluble_but_not_aa_bb_admissible_entry_count": 29,
        "opposite_side_squareclass_failure_entry_count": 29,
        "genuinely_deferred_cover_family_count": 0,
        "aa_bb_admissible_cover_family_count": 0,
        "active_final_obstruction_candidate_count": 0,
    }


def test_wl524_compares_required_route_options() -> None:
    audit = _wl524()

    options = audit["route_options"]
    assert set(options) == {
        "attempt_new_uniform_cover_family_squareclass_obstruction_lemma",
        "return_later_to_finite_shell11_m_tail_diagnostics",
        "proof_level_local_or_hilbert_row_work",
        "final_obstruction_candidate_selection",
    }
    assert (
        options["attempt_new_uniform_cover_family_squareclass_obstruction_lemma"][
            "decision"
        ]
        == "selected_next_narrow_gate"
    )
    assert (
        options["return_later_to_finite_shell11_m_tail_diagnostics"]["decision"]
        == "defer"
    )
    assert (
        options["proof_level_local_or_hilbert_row_work"]["decision"]
        == "defer_until_named_selmer_row_gap"
    )
    assert options["final_obstruction_candidate_selection"]["decision"] == "reject"


def test_wl524_selects_uniform_cover_family_lemma_but_does_not_enter_it() -> None:
    audit = _wl524()

    selected = audit["selected_next_gate"]
    assert selected["gate"] == "attempt_uniform_cover_family_squareclass_obstruction_lemma"
    assert selected["entered_here"] is False
    assert selected["input_work_log_to_use_later"] == "wl523"
    assert selected["object_layer"] == "cover_family_statement_layer"
    assert selected["not_a_selmer_upper_bound"] is True
    assert selected["not_a_finite_taxonomy_count_claim"] is True
    assert selected["uniform_cover_family_lemma_proved_here"] is False
    assert selected["shell11_executed_here"] is False
    assert selected["m_tail_diagnostics_extended_here"] is False
    assert selected["new_supports_computed_here"] is False
    assert selected["new_c_d_solubility_tested_here"] is False
    assert selected["wl491_filter_applied_here"] is False
    assert selected["candidate_selected_here"] is False


def test_wl524_stops_without_forbidden_work_or_claims() -> None:
    audit = _wl524()

    assert audit["post_wl523_route_choice_made_here"] is True
    assert audit["selected_route_entered_here"] is False
    assert audit["uniform_cover_family_lemma_proved_here"] is False
    assert audit["shell11_executed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["wl491_filter_applied_to_new_point_here"] is False
    assert audit["final_obstruction_candidate_selected_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_selected_next_gate"] is False
    assert audit["advance_to_wl525"] is False
    assert audit["stop_after_current_task"] is True


def test_wl524_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl524.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice_audit.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl523",
            str(
                ROOT
                / "results/"
                "closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate.json"
            ),
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
    assert "work_log=wl524" in result.stdout
    assert (
        "selected_gate=attempt_uniform_cover_family_squareclass_obstruction_lemma"
        in result.stdout
    )
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl524"
    assert payload["selected_next_gate"]["entered_here"] is False
