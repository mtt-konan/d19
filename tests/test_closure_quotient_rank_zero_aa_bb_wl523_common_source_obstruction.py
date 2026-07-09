from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate import (  # noqa: E501
    build_wl523_try_common_source_square_obstruction_lemma_candidate,
)


def _wl522() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / "results/"
            "closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.json"
        ).read_text(encoding="utf-8")
    )


def _wl523() -> dict[str, object]:
    return build_wl523_try_common_source_square_obstruction_lemma_candidate(wl522=_wl522())


def test_wl523_states_precise_point_level_common_source_square_obstruction() -> None:
    audit = _wl523()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "WL523_try_common_source_square_obstruction_lemma_candidate"
    assert audit["work_log"] == "wl523"
    assert audit["input_work_log"] == "wl522"
    assert audit["proof_statement_layer_only"] is True

    statement = audit["lemma_statement"]
    assert statement["lemma_id"] == (
        "common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families"
    )
    assert statement["scope"] == "point_level_aa_bb_admissibility_obstruction"
    assert statement["source_side_product"] == {
        "AA": "(N^2 + A^2)(M^2 + A^2)",
        "BB": "(N^2 + B^2)(M^2 + B^2)",
    }
    assert statement["opposite_side_product"] == {
        "AA_source": "(N^2 + B^2)(M^2 + B^2)",
        "BB_source": "(N^2 + A^2)(M^2 + A^2)",
    }
    assert statement["conclusion"] == (
        "If the opposite-side product is not a rational square, the ambient "
        "C_d point is not AA+BB-admissible and must stay in the globally "
        "soluble but not AA+BB-admissible ledger."
    )


def test_wl523_separates_squareclass_failure_from_sign_failure() -> None:
    audit = _wl523()

    separation = audit["failure_separation"]
    assert separation["squareclass_failure_reasons"] == [
        "AA_common_source_product_not_square",
        "BB_common_source_product_not_square",
    ]
    assert separation["positivity_or_nondegeneracy_reasons"] == [
        "A_not_positive",
        "B_not_positive",
        "N_not_positive",
        "M_not_positive",
    ]
    assert separation["M_not_positive_is_squareclass_failure"] is False
    assert separation["squareclass_failure_alone_blocks_admissibility"] is True
    assert separation["positivity_failure_alone_is_same_lemma"] is False


def test_wl523_decides_existing_wl491_proves_point_lemma_but_not_uniform_cover_theorem() -> None:
    audit = _wl523()

    decision = audit["proof_decision"]
    assert decision == {
        "point_level_lemma_status": "provable_from_existing_wl491_machinery",
        "new_point_level_lemma_needed": False,
        "cover_family_uniform_theorem_status": "needs_new_uniform_squareclass_lemma",
        "finite_taxonomy_count_is_proof": False,
        "too_finite_if_read_as_family_theorem": True,
        "false_as_stated_for_all_future_ambient_points": "not_decided_here",
        "reason": (
            "wl491 already proves the point-level obstruction after a certified "
            "centered-even pullback. The wl522 taxonomy only shows that the "
            "recorded globally soluble not-admissible ledger entries fail this "
            "check; it does not prove a uniform statement for every rational "
            "point on those cover families."
        ),
    }


def test_wl523_uses_wl522_taxonomy_without_new_route_work_or_forbidden_claims() -> None:
    audit = _wl523()

    taxonomy = audit["wl522_taxonomy_application"]
    assert taxonomy["globally_soluble_but_not_aa_bb_admissible_cover_family_count"] == 15
    assert taxonomy["globally_soluble_but_not_aa_bb_admissible_entry_count"] == 29
    assert taxonomy["opposite_side_squareclass_failure_entry_count"] == 29
    assert taxonomy["positivity_failure_entry_count"] == 13
    assert taxonomy["genuinely_deferred_cover_family_count"] == 0
    assert taxonomy["aa_bb_admissible_cover_family_count"] == 0

    assert audit["shell11_executed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["wl491_filter_applied_to_new_point_here"] is False
    assert audit["final_obstruction_candidate_selected_here"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["advance_to_wl524"] is False
    assert audit["stop_after_current_task"] is True


def test_wl523_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl523.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl523_try_common_source_square_obstruction_lemma_candidate.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl522",
            str(
                ROOT
                / "results/"
                "closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.json"
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
    assert "work_log=wl523" in result.stdout
    assert "point_level_lemma_status=provable_from_existing_wl491_machinery" in result.stdout
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl523"
    assert payload["proof_decision"]["new_point_level_lemma_needed"] is False
