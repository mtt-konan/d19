from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma import (  # noqa: E501
    build_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma,
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
    return json.loads(
        (
            ROOT
            / "results/"
            "closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice_audit.json"
        ).read_text(encoding="utf-8")
    )


def _wl525() -> dict[str, object]:
    return build_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma(
        wl523=_wl523(),
        wl524=_wl524(),
    )


def test_wl525_enters_selected_uniform_cover_family_statement_gate() -> None:
    audit = _wl525()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert (
        audit["lemma_id"]
        == "WL525_attempt_uniform_cover_family_squareclass_obstruction_lemma"
    )
    assert audit["work_log"] == "wl525"
    assert audit["input_work_logs"] == ["wl523", "wl524"]
    assert audit["object_layer"] == "cover_family_statement_layer"
    assert audit["selected_gate_entered_here"] is True
    assert audit["attempted_uniform_cover_family_lemma_here"] is True


def test_wl525_records_precise_uniform_lemma_target_and_required_proof_obligations() -> None:
    audit = _wl525()

    target = audit["uniform_lemma_target"]
    assert target["scope"] == "cover_family_statement"
    assert target["covered_cover_family_count"] == 15
    assert target["covered_entry_count"] == 29
    assert target["claim_to_prove"] == (
        "For every rational ambient C_d point on each named wl522 globally "
        "soluble but not AA+BB-admissible cover family that has a certified "
        "wl491 centered-even pullback, the opposite-side common-source product "
        "is non-square in Q*/Q*2."
    )
    assert target["would_imply_only"] == (
        "a cover-family AA+BB non-admissibility obstruction, not a Selmer "
        "upper bound, rank-zero theorem, Sha[2] statement, or family exclusion"
    )

    obligations = audit["uniform_proof_obligations"]
    assert obligations == [
        "Give a cover-family model and rational source-side map for each named cover family.",
        "Express N and M as rational functions on the cover-family function field.",
        "Express the opposite-side product as a rational function on that function field.",
        (
            "Prove that rational function is not a square in the relevant function field, "
            "or prove an equivalent squareclass obstruction that survives specialization "
            "to every rational point under consideration."
        ),
        (
            "Control exceptional divisors, poles, zeroes, and positivity or "
            "nondegeneracy failures separately from squareclass failure."
        ),
        (
            "Show the proof is uniform for all rational points on the family, "
            "not just for the finite wl522 ledger entries."
        ),
    ]


def test_wl525_refutes_finite_taxonomy_promotion_but_not_the_mathematical_lemma() -> None:
    audit = _wl525()

    decision = audit["attempt_decision"]
    assert decision == {
        "uniform_cover_family_lemma_status": "not_proved_from_wl523_wl524_inputs",
        "finite_taxonomy_promotion_status": "refuted",
        "mathematical_uniform_lemma_refuted": False,
        "failure_point": "missing_function_field_squareclass_certificate",
        "reason": (
            "wl523 supplies a point-level wl491 obstruction and wl524 selects "
            "this proof attempt, but neither input supplies cover-family "
            "function-field squareclass data, divisor parity data, or a "
            "specialization argument. The 15 cover-family / 29 entry taxonomy "
            "therefore cannot be promoted to a uniform theorem."
        ),
    }

    assert audit["finite_taxonomy_is_theorem_proof"] is False
    assert audit["uniform_cover_family_lemma_proved_here"] is False
    assert (
        audit["precise_failure_point"]
        == "finite_taxonomy_has_no_uniform_squareclass_certificate"
    )


def test_wl525_keeps_wl522_counts_as_audit_snapshot_only() -> None:
    audit = _wl525()

    finite = audit["finite_input_snapshot"]
    assert finite["globally_soluble_but_not_aa_bb_admissible_cover_family_count"] == 15
    assert finite["globally_soluble_but_not_aa_bb_admissible_entry_count"] == 29
    assert finite["opposite_side_squareclass_failure_entry_count"] == 29
    assert finite["genuinely_deferred_cover_family_count"] == 0
    assert finite["aa_bb_admissible_cover_family_count"] == 0
    assert finite["used_as_uniform_proof"] is False
    assert finite["audit_snapshot_only"] is True


def test_wl525_stops_without_forbidden_work_or_claims() -> None:
    audit = _wl525()

    assert audit["stop_after_current_task"] is True
    assert audit["advance_to_next_roadmap_step"] is False
    assert audit["shell11_executed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["wl491_filter_applied_to_new_point_here"] is False
    assert audit["final_obstruction_candidate_selected_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0


def test_wl525_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl525.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl525_attempt_uniform_cover_family_squareclass_obstruction_lemma.py"
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
            "--wl524",
            str(
                ROOT
                / "results/"
                "closure_quotient_rank_zero_aa_bb_wl524_post_wl523_route_choice_audit.json"
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
    assert "work_log=wl525" in result.stdout
    assert (
        "uniform_cover_family_lemma_status=not_proved_from_wl523_wl524_inputs"
        in result.stdout
    )
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl525"
    assert payload["attempt_decision"]["finite_taxonomy_promotion_status"] == "refuted"
