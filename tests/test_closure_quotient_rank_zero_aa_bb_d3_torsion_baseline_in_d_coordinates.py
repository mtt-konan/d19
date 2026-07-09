from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates import (  # noqa: E501
    BOUNDARY,
    audit_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates,
)


def _representatives() -> dict[str, list[str]]:
    return {
        "O": ["1", "1", "1"],
        "T_minus_p": [
            "(-p-2*sqrt_q)*(-p+2*sqrt_q)",
            "-p-2*sqrt_q",
            "-p+2*sqrt_q",
        ],
        "T_pos_2sqrt_q": [
            "2*sqrt_q+p",
            "(2*sqrt_q+p)*(4*sqrt_q)",
            "4*sqrt_q",
        ],
        "T_neg_2sqrt_q": [
            "-2*sqrt_q+p",
            "-4*sqrt_q",
            "(-2*sqrt_q+p)*(-4*sqrt_q)",
        ],
    }


def _d0_container() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D0_complete_d_container_definition",
        "d0_status": "framed_definition",
        "complete_d_container": {
            "name": "D0_complete_d_prelocal_container",
            "ambient_squareclass_quotient": (
                "V = Q*/Q*2; triples are in V^3 and multiplied coordinatewise"
            ),
            "coordinate_tuple_order": [
                "d_minus_p",
                "d_pos_2sqrt_q",
                "d_neg_2sqrt_q",
            ],
            "defining_relation": (
                "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2"
            ),
            "local_c_d_rows_built": False,
            "package_x_coordinates_used": False,
        },
        "torsion_kummer_baseline": {
            "same_quotient_as_container": True,
            "baseline_dimension": 2,
            "representative_order": [
                "O",
                "T_minus_p",
                "T_pos_2sqrt_q",
                "T_neg_2sqrt_q",
            ],
            "representatives": _representatives(),
            "product_relation_verified_for_representatives": True,
            "baseline_generators": ["T_minus_p", "T_pos_2sqrt_q"],
            "generator_sum_relation": (
                "T_minus_p*T_pos_2sqrt_q=T_neg_2sqrt_q in V^3"
            ),
            "baseline_not_quotiented_out": True,
        },
        "local_c_d_rows_built": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d1_support() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D1_relevant_place_support_confinement",
        "d1_status": "framed_and_proved_support_confinement",
        "candidate_support": {
            "equivalent_finite_set": (
                "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}"
            ),
        },
        "support_only_not_row_classification": True,
        "local_c_d_rows_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d2_rows() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D2_local_C_d_row_characterization",
        "d2_status": "row_obligations_framed",
        "complete_d_coordinate_frame": {
            "coordinate_order": [
                "d_minus_p",
                "d_pos_2sqrt_q",
                "d_neg_2sqrt_q",
            ],
            "product_relation": (
                "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2"
            ),
            "package_x_coordinates_used": False,
        },
        "candidate_row_domain": {
            "places": "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}",
            "row_characterization_only": True,
        },
        "local_row_obligations": [
            {"id": "D2a_odd_L_collision_row", "place_type": "ell|L"},
            {"id": "D2b_odd_T_collision_row", "place_type": "ell|T"},
            {"id": "D2c_odd_sqrt_q_collision_row", "place_type": "ell|sqrt_q"},
            {"id": "D2d_dyadic_complete_row", "place_type": "ell=2"},
            {"id": "D2e_real_sign_row", "place_type": "infinity"},
        ],
        "row_obligations_framed": True,
        "local_c_d_rows_solved": False,
        "local_c_d_rows_built": False,
        "full_c_d_matrix_built": False,
        "old_package_x_coordinate_collapse_used": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def test_d3_records_all_four_torsion_representatives_in_complete_d_order() -> None:
    audit = audit_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
    )

    baseline = audit["rational_two_torsion_baseline"]
    assert audit["status"] == "ok"
    assert audit["lemma_id"] == "D3_torsion_baseline_in_d_coordinates"
    assert audit["d3_status"] == "torsion_baseline_recorded_in_complete_d_coordinates"
    assert baseline == {
        "object_recorded": "rational E_L[2](Q) Kummer baseline",
        "ambient_squareclass_quotient": (
            "V = Q*/Q*2; triples are in V^3 and multiplied coordinatewise"
        ),
        "coordinate_order": [
            "d_minus_p",
            "d_pos_2sqrt_q",
            "d_neg_2sqrt_q",
        ],
        "baseline_dimension": 2,
        "representative_order": [
            "O",
            "T_minus_p",
            "T_pos_2sqrt_q",
            "T_neg_2sqrt_q",
        ],
        "representatives": _representatives(),
        "root_labels": {
            "T_minus_p": "e_minus=-p",
            "T_pos_2sqrt_q": "e_pos=2*sqrt_q",
            "T_neg_2sqrt_q": "e_neg=-2*sqrt_q",
        },
        "exceptional_root_rule": (
            "At X=e_i, replace the vanishing d_i coordinate by the product "
            "of the two nonzero root differences."
        ),
        "same_quotient_as_container": True,
        "baseline_not_quotiented_out": True,
    }


def test_d3_audits_product_relation_and_generator_relations() -> None:
    audit = audit_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
    )

    assert audit["product_relation_checks"] == {
        "relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in V",
        "checks": {
            "O": "1*1*1=1",
            "T_minus_p": (
                "((-p-2*sqrt_q)*(-p+2*sqrt_q))*(-p-2*sqrt_q)*"
                "(-p+2*sqrt_q)=((-p-2*sqrt_q)*(-p+2*sqrt_q))^2"
            ),
            "T_pos_2sqrt_q": (
                "(2*sqrt_q+p)*((2*sqrt_q+p)*(4*sqrt_q))*(4*sqrt_q)="
                "((2*sqrt_q+p)*(4*sqrt_q))^2"
            ),
            "T_neg_2sqrt_q": (
                "(-2*sqrt_q+p)*(-4*sqrt_q)*((-2*sqrt_q+p)*(-4*sqrt_q))="
                "((-2*sqrt_q+p)*(-4*sqrt_q))^2"
            ),
        },
        "all_verified_symbolically_mod_squares": True,
    }
    assert audit["baseline_group_law_checks"] == {
        "generators": ["T_minus_p", "T_pos_2sqrt_q"],
        "generator_product": "T_minus_p*T_pos_2sqrt_q=T_neg_2sqrt_q in V^3",
        "self_products": {
            "T_minus_p*T_minus_p": "O",
            "T_pos_2sqrt_q*T_pos_2sqrt_q": "O",
            "T_neg_2sqrt_q*T_neg_2sqrt_q": "O",
        },
        "mixed_products": {
            "T_minus_p*T_pos_2sqrt_q": "T_neg_2sqrt_q",
            "T_minus_p*T_neg_2sqrt_q": "T_pos_2sqrt_q",
            "T_pos_2sqrt_q*T_neg_2sqrt_q": "T_minus_p",
        },
        "all_verified_coordinatewise_mod_squares": True,
    }


def test_d3_records_later_local_row_comparison_contract_without_quotienting() -> None:
    audit = audit_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
    )

    assert audit["baseline_comparison_contract"] == {
        "comparison_target": "future solved local C_d rows from D2 obligations",
        "d2_row_ids_to_compare_against": [
            "D2a_odd_L_collision_row",
            "D2b_odd_T_collision_row",
            "D2c_odd_sqrt_q_collision_row",
            "D2d_dyadic_complete_row",
            "D2e_real_sign_row",
        ],
        "comparison_status": "pending_until_local_c_d_rows_are_solved",
        "comparison_rule": (
            "Check each of O, T_minus_p, T_pos_2sqrt_q, and "
            "T_neg_2sqrt_q against each solved local row in the same "
            "complete d-coordinate order before any quotient or rank ledger."
        ),
        "quotient_baseline_here": False,
        "baseline_must_remain_visible_for_D4": True,
    }
    assert audit["local_c_d_rows_solved"] is False
    assert audit["full_c_d_matrix_built"] is False
    assert audit["d4_entered"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["next_lemma"] == "D2_local_C_d_row_solving"
    assert audit["do_not_proceed_to"] == ["D4_AA_BB_uniform_matrix_rank_bound"]
    assert audit["boundary"] == BOUNDARY


def test_d3_rejects_bad_or_overadvanced_inputs() -> None:
    d0 = _d0_container()
    d0["torsion_kummer_baseline"] = {"baseline_not_quotiented_out": False}
    d1 = _d1_support()
    d1["local_c_d_rows_built"] = True
    d2 = _d2_rows()
    d2["local_c_d_rows_solved"] = True
    d2["full_c_d_matrix_built"] = True

    audit = audit_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates(
        d0_container=d0,
        d1_support=d1,
        d2_rows=d2,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "d0_torsion_baseline_incomplete_or_quotiented",
        "d1_already_built_local_rows",
        "d2_already_solved_local_rows",
        "d2_already_built_full_matrix",
    ]
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_d3_cli_writes_scoped_result(tmp_path: Path) -> None:
    d0 = tmp_path / "d0.json"
    d1 = tmp_path / "d1.json"
    d2 = tmp_path / "d2.json"
    out = tmp_path / "d3.json"
    d0.write_text(json.dumps(_d0_container()), encoding="utf-8")
    d1.write_text(json.dumps(_d1_support()), encoding="utf-8")
    d2.write_text(json.dumps(_d2_rows()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_d3_torsion_baseline_in_d_coordinates.py",
            "--d0-container",
            str(d0),
            "--d1-support",
            str(d1),
            "--d2-rows",
            str(d2),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "d3_status=torsion_baseline_recorded_in_complete_d_coordinates" in result.stdout
    assert "quotient_baseline_here=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["rational_two_torsion_baseline"]["baseline_not_quotiented_out"] is True
    assert payload["d4_entered"] is False
