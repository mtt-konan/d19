from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope import (  # noqa: E501
    build_wl527_function_field_squareclass_proof_data_scope,
)


def _wl522() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / "results/"
            "closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint.json"
        ).read_text(encoding="utf-8")
    )


def _wl526() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / "results/"
            "closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit.json"
        ).read_text(encoding="utf-8")
    )


def _wl527() -> dict[str, object]:
    return build_wl527_function_field_squareclass_proof_data_scope(
        wl522=_wl522(),
        wl526=_wl526(),
    )


def test_wl527_enters_wl526_selected_function_field_scoping_gate() -> None:
    audit = _wl527()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert (
        audit["lemma_id"]
        == "WL527_function_field_squareclass_proof_data_scope"
    )
    assert audit["work_log"] == "wl527"
    assert audit["input_work_logs"] == ["wl526", "wl522"]
    assert audit["immediate_input_work_log"] == "wl526"
    assert audit["selected_gate_entered_here"] is True
    assert audit["object_layer"] == "cover_family_function_field_proof_data_scoping"
    assert audit["function_field_proof_data_scoped_here"] is True
    assert audit["uniform_cover_family_lemma_proved_here"] is False


def test_wl527_inventories_the_named_wl522_not_admissible_cover_families() -> None:
    audit = _wl527()

    summary = audit["scope_summary"]
    assert summary["named_cover_family_count"] == 15
    assert summary["named_entry_count"] == 29
    assert summary["ready_for_later_uniform_squareclass_proof_attempt"] is False
    assert summary["ready_cover_family_count"] == 0
    assert summary["not_ready_cover_family_count"] == 15
    assert summary["cover_families_with_label_and_l_t_d_data_count"] == 14
    assert summary["cover_families_missing_explicit_d_vector_count"] == 1
    assert summary["exact_missing_data_class"] == (
        "uniform_function_field_model_maps_and_squareclass_certificate"
    )

    inventory = audit["cover_family_proof_data_inventory"]
    assert len(inventory) == 15
    assert [row["classification"] for row in inventory] == [
        "globally_soluble_but_not_aa_bb_admissible"
    ] * 15
    assert inventory[0]["cover_family"] == "support=u_3|L=3|T=4|d=(?,?,?)"
    assert inventory[0]["cover_family_model_availability"]["status"] == (
        "cover_label_only_missing_explicit_d_vector_and_equation"
    )
    assert inventory[1]["cover_family_model_availability"]["status"] == (
        "label_and_l_t_d_vector_only_no_explicit_function_field_model"
    )


def test_wl527_scopes_minimum_data_obligations_without_proving_them() -> None:
    audit = _wl527()

    row = audit["cover_family_proof_data_inventory"][1]
    assert row["rational_source_side_maps"]["status"] == "missing_uniform_maps"
    assert row["candidate_function_field_elements"]["status"] == (
        "missing_N_M_as_function_field_elements"
    )
    assert row["opposite_side_target"] == {
        "status": "formula_target_only_not_a_certificate",
        "AA_source_target": "(N^2 + B^2)(M^2 + B^2)",
        "BB_source_target": "(N^2 + A^2)(M^2 + A^2)",
        "certificate_needed": (
            "non-square in the cover-family function field, or equivalent "
            "divisor-parity squareclass obstruction surviving specialization"
        ),
    }
    assert row["exceptional_specialization_positivity_checklist"] == [
        "separate poles and zeroes of N, M, and the opposite-side product",
        "separate exceptional divisors where the source-side pullback is undefined",
        "separate specializations where centered-even or rationality hypotheses fail",
        "separate N_not_positive and M_not_positive from squareclass failure",
        "separate degeneracy of A, B, N, M, or source-side products from squareclass failure",
        "record positivity domain before any later uniform proof attempt",
    ]
    assert row["readiness"] == "not_ready_for_later_uniform_squareclass_proof_attempt"
    assert row["missing_data_classes"] == [
        "explicit_cover_family_function_field_model",
        "rational_source_side_maps_on_family",
        "N_M_as_function_field_elements",
        "opposite_side_product_squareclass_or_divisor_parity_certificate",
        "exceptional_specialization_and_positivity_separation",
    ]

    counts = audit["missing_data_class_counts"]
    assert counts["explicit_cover_family_function_field_model"] == 15
    assert counts["rational_source_side_maps_on_family"] == 15
    assert counts["N_M_as_function_field_elements"] == 15
    assert (
        counts["opposite_side_product_squareclass_or_divisor_parity_certificate"]
        == 15
    )
    assert counts["exceptional_specialization_and_positivity_separation"] == 15
    assert counts["explicit_d_vector_for_family_label"] == 1


def test_wl527_stops_without_forbidden_work_or_claims() -> None:
    audit = _wl527()

    assert audit["function_field_models_built_here"] is False
    assert audit["function_field_engine_built_here"] is False
    assert audit["function_field_squareclass_certificate_proved_here"] is False
    assert audit["uniform_cover_family_lemma_proved_here"] is False
    assert audit["complete_selmer_local_hilbert_row_obligation_named_here"] is False
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
    assert audit["advance_to_next_roadmap_step"] is False
    assert audit["stop_after_current_task"] is True


def test_wl527_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl527.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.py"
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
            "--wl526",
            str(
                ROOT
                / "results/"
                "closure_quotient_rank_zero_aa_bb_wl526_post_wl525_route_choice_audit.json"
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
    assert "work_log=wl527" in result.stdout
    assert "named_cover_family_count=15" in result.stdout
    assert "ready_for_later_uniform_squareclass_proof_attempt=False" in result.stdout
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl527"
    assert payload["scope_summary"]["not_ready_cover_family_count"] == 15
