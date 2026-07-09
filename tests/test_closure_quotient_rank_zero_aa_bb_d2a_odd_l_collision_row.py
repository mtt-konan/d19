from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_d2a_odd_l_collision_row import (
    BOUNDARY,
    audit_rank_zero_aa_bb_d2a_odd_l_collision_row,
)


def _d0_container() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D0_complete_d_container_definition",
        "d0_status": "framed_definition",
        "complete_d_container": {
            "name": "D0_complete_d_prelocal_container",
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


def _d3_baseline() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D3_torsion_baseline_in_d_coordinates",
        "d3_status": "torsion_baseline_recorded_in_complete_d_coordinates",
        "baseline_comparison_contract": {
            "comparison_status": "pending_until_local_c_d_rows_are_solved",
            "quotient_baseline_here": False,
        },
        "local_c_d_rows_solved": False,
        "local_c_d_rows_built": False,
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def test_d2a_solves_pure_l_collision_row_in_complete_d_coordinates() -> None:
    audit = audit_rank_zero_aa_bb_d2a_odd_l_collision_row(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
        d3_baseline=_d3_baseline(),
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "D2a_odd_L_collision_row"
    assert audit["d2a_status"] == "pure_L_collision_row_solved"
    assert audit["solved_local_row"] == {
        "id": "D2a_odd_L_collision_row",
        "place_type": "ell|L",
        "stratum": "pure_L_collision",
        "applies_when": "ell odd, ell | L, ell does not divide T*sqrt_q",
        "coordinate_pair": ["d_minus_p", "d_pos_2sqrt_q"],
        "allowed_pair_rule": (
            "(d_minus_p,d_pos_2sqrt_q)=(lambda,lambda) for "
            "lambda in Q_ell*/Q_ell*2"
        ),
        "allowed_valuation_rule": (
            "v_ell(d_minus_p) == v_ell(d_pos_2sqrt_q) mod 2"
        ),
        "allowed_unit_squareclass_rule": (
            "unit(d_minus_p) == unit(d_pos_2sqrt_q) in F_ell*/F_ell*2"
        ),
        "allowed_pair_squareclasses": [
            "(1,1)",
            "(nu,nu)",
            "(ell,ell)",
            "(nu*ell,nu*ell)",
        ],
        "nu": "any fixed nonsquare unit in Q_ell",
        "d_neg_2sqrt_q_from_product_relation": "1 in Q_ell*/Q_ell*2",
        "row_dimension_over_F2_local_only": 2,
        "local_c_d_row_solved": True,
    }


def test_d2a_records_pure_stratum_derivation_and_multicollision_boundaries() -> None:
    audit = audit_rank_zero_aa_bb_d2a_odd_l_collision_row(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
        d3_baseline=_d3_baseline(),
    )

    assert audit["pure_L_collision_stratum"] == {
        "prime_condition": "ell odd and ell | L",
        "excluded_overlaps": ["ell | T", "ell | sqrt_q"],
        "root_difference_squareclasses": {
            "e_pos-e_minus": (
                "16*L^2 has positive even ell-adic valuation and squareclass 1"
            ),
            "e_minus-e_neg": "4*T^2 is an ell-adic square unit",
            "e_pos-e_neg": (
                "4*sqrt_q=(2*T)^2*(1+4*L^2/T^2) is an ell-adic square unit"
            ),
        },
        "normal_form": (
            "after translating by e_neg and scaling by the square unit "
            "e_minus-e_neg, the reduction is y^2=x*(x-1)^2"
        ),
    }
    assert audit["proof_summary"] == [
        (
            "In the pure stratum, the two non-colliding differences to "
            "e_neg are square units, so every local point has "
            "d_neg_2sqrt_q=1."
        ),
        (
            "The reduced odd-prime model is the split nodal curve "
            "y^2=x*(x-1)^2; away from the node, local solubility forces "
            "x to be a square, hence the two colliding d-coordinates have "
            "the same squareclass."
        ),
        (
            "Conversely each lambda in Q_ell*/Q_ell*2 is realized: smooth "
            "points on the split nodal reduction realize both unit classes, "
            "and points with v_ell(X-e_minus)=1 realize the ramified classes."
        ),
        (
            "The product relation then determines "
            "d_neg_2sqrt_q=(d_minus_p*d_pos_2sqrt_q)^-1=1."
        ),
    ]
    assert audit["multi_collision_obligations"] == [
        {
            "condition": "ell | L and ell | T",
            "reason": "e_minus-e_neg=4*T^2 is no longer an ell-adic unit",
            "status": "multi_collision_obligation_not_solved_here",
        },
        {
            "condition": "ell | L and ell | sqrt_q",
            "reason": "e_pos-e_neg=4*sqrt_q is no longer an ell-adic unit",
            "status": "multi_collision_obligation_not_solved_here",
        },
    ]
    assert audit["row_obstruction_remaining"] is False
    assert audit["overlap_cases_solved_here"] is False


def test_d2a_keeps_scope_below_matrix_and_selmer_claims() -> None:
    audit = audit_rank_zero_aa_bb_d2a_odd_l_collision_row(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
        d3_baseline=_d3_baseline(),
    )

    assert audit["local_c_d_rows_partially_solved"] is True
    assert audit["local_c_d_rows_solved"] is False
    assert audit["solved_row_ids"] == ["D2a_odd_L_collision_row"]
    assert audit["remaining_d2_obligations"] == [
        "D2b_odd_T_collision_row",
        "D2c_odd_sqrt_q_collision_row",
        "D2d_dyadic_complete_row",
        "D2a_multi_collision_overlaps",
    ]
    assert audit["full_c_d_matrix_built"] is False
    assert audit["d4_entered"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY


def test_d2a_rejects_inputs_without_the_d2a_obligation_or_overadvanced_d3() -> None:
    d2 = _d2_rows()
    d2["local_row_obligations"] = [
        {"id": "D2b_odd_T_collision_row", "place_type": "ell|T"},
    ]
    d3 = _d3_baseline()
    d3["full_c_d_matrix_built"] = True

    audit = audit_rank_zero_aa_bb_d2a_odd_l_collision_row(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=d2,
        d3_baseline=d3,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "d2a_obligation_missing",
        "d3_already_built_full_matrix",
    ]
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_d2a_cli_writes_scoped_result(tmp_path: Path) -> None:
    d0 = tmp_path / "d0.json"
    d1 = tmp_path / "d1.json"
    d2 = tmp_path / "d2.json"
    d3 = tmp_path / "d3.json"
    out = tmp_path / "d2a.json"
    d0.write_text(json.dumps(_d0_container()), encoding="utf-8")
    d1.write_text(json.dumps(_d1_support()), encoding="utf-8")
    d2.write_text(json.dumps(_d2_rows()), encoding="utf-8")
    d3.write_text(json.dumps(_d3_baseline()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_d2a_odd_l_collision_row.py",
            "--d0-container",
            str(d0),
            "--d1-support",
            str(d1),
            "--d2-rows",
            str(d2),
            "--d3-baseline",
            str(d3),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "d2a_status=pure_L_collision_row_solved" in result.stdout
    assert "full_c_d_matrix_built=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["solved_local_row"]["allowed_pair_rule"].startswith(
        "(d_minus_p,d_pos_2sqrt_q)=(lambda,lambda)"
    )
    assert payload["complete_selmer_upper_bound_proved"] is False
