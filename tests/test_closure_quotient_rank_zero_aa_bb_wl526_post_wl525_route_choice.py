from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit import (  # noqa: E501
    build_wl526_post_wl525_route_choice_audit,
)


def _wl525() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / "results/"
            "closure_quotient_rank_zero_aa_bb_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma.json"
        ).read_text(encoding="utf-8")
    )


def _wl526() -> dict[str, object]:
    return build_wl526_post_wl525_route_choice_audit(wl525=_wl525())


def test_wl526_summarizes_post_wl525_failed_uniform_attempt_state() -> None:
    audit = _wl526()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL526_post_wl525_route_choice_audit"
    assert audit["work_log"] == "wl526"
    assert audit["input_work_log"] == "wl525"
    assert audit["routing_audit_only"] is True
    assert audit["post_wl525_route_state_summary"] == {
        "uniform_cover_family_lemma_status": "not_proved_from_wl523_wl524_inputs",
        "finite_taxonomy_promotion_status": "refuted",
        "mathematical_uniform_lemma_refuted": False,
        "failure_point": "missing_function_field_squareclass_certificate",
        "precise_failure_point": "finite_taxonomy_has_no_uniform_squareclass_certificate",
        "finite_taxonomy_is_theorem_proof": False,
        "uniform_cover_family_lemma_proved_here": False,
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": 15,
        "globally_soluble_but_not_aa_bb_admissible_entry_count": 29,
    }


def test_wl526_compares_exact_post_wl525_route_families() -> None:
    audit = _wl526()

    route_families = audit["route_families"]
    assert list(route_families) == [
        "gather_minimal_function_field_squareclass_proof_data_for_named_cover_families",
        "return_to_finite_shell_m_tail_diagnostics",
        "name_theorem_level_complete_selmer_local_hilbert_row_obligation",
        "abandon_this_obstruction_line_and_select_different_candidate",
    ]
    assert (
        route_families[
            "gather_minimal_function_field_squareclass_proof_data_for_named_cover_families"
        ]["decision"]
        == "selected_next_narrow_gate"
    )
    assert (
        route_families["return_to_finite_shell_m_tail_diagnostics"]["decision"]
        == "defer"
    )
    assert (
        route_families[
            "name_theorem_level_complete_selmer_local_hilbert_row_obligation"
        ]["decision"]
        == "defer_until_cover_family_obstruction_line_is_scoped_or_refuted"
    )
    assert (
        route_families[
            "abandon_this_obstruction_line_and_select_different_candidate"
        ]["decision"]
        == "reject_for_now"
    )


def test_wl526_selects_minimal_function_field_data_scoping_but_does_not_enter_it() -> None:
    audit = _wl526()

    selected = audit["selected_next_gate"]
    assert (
        selected["gate"]
        == "gather_minimal_function_field_squareclass_proof_data_for_named_cover_families"
    )
    assert selected["entered_here"] is False
    assert selected["input_work_log_to_use_later"] == "wl525"
    assert selected["object_layer"] == "cover_family_function_field_proof_data_scoping"
    assert selected["not_a_selmer_upper_bound"] is True
    assert selected["not_a_finite_taxonomy_count_claim"] is True
    assert selected["builds_function_field_models_here"] is False
    assert selected["proves_uniform_lemma_here"] is False
    assert selected["minimum_later_data_to_scope"] == [
        "named cover-family model inventory",
        "rational source-side map inventory",
        "N and M as candidate function-field elements",
        "opposite-side product squareclass or divisor-parity certificate target",
        "exceptional specialization and positivity-separation checklist",
    ]


def test_wl526_stops_without_forbidden_work_or_claims() -> None:
    audit = _wl526()

    assert audit["post_wl525_route_choice_made_here"] is True
    assert audit["selected_route_entered_here"] is False
    assert audit["function_field_models_built_here"] is False
    assert audit["function_field_squareclass_certificate_proved_here"] is False
    assert audit["uniform_cover_family_lemma_proved_here"] is False
    assert audit["complete_selmer_local_hilbert_row_obligation_named_here"] is False
    assert audit["abandoned_obstruction_line_here"] is False
    assert audit["different_candidate_selected_here"] is False
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
    assert audit["advance_to_wl527"] is False
    assert audit["stop_after_current_task"] is True


def test_wl526_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl526.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl525",
            str(
                ROOT
                / "results/"
                "closure_quotient_rank_zero_aa_bb_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma.json"
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
    assert "work_log=wl526" in result.stdout
    assert (
        "selected_gate=gather_minimal_function_field_squareclass_proof_data_for_named_cover_families"
        in result.stdout
    )
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl526"
    assert payload["selected_next_gate"]["entered_here"] is False
