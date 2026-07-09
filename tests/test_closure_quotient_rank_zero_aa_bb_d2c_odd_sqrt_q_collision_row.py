from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_d2c_odd_sqrt_q_collision_row import (
    BOUNDARY,
    audit_rank_zero_aa_bb_d2c_odd_sqrt_q_collision_row,
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
            "defining_relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2",
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
            "equivalent_finite_set": "{infinity, 2} union {odd ell: ell | L*T*sqrt_q}",
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
            "product_relation": "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2",
            "package_x_coordinates_used": False,
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


def _d2a_row() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D2a_odd_L_collision_row",
        "d2a_status": "pure_L_collision_row_solved",
        "local_c_d_rows_partially_solved": True,
        "local_c_d_rows_solved": False,
        "solved_row_ids": ["D2a_odd_L_collision_row"],
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d2b_row() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": "D2b_odd_T_collision_row",
        "d2b_status": "pure_T_collision_row_solved",
        "local_c_d_rows_partially_solved": True,
        "local_c_d_rows_solved": False,
        "solved_row_ids": [
            "D2a_odd_L_collision_row",
            "D2b_odd_T_collision_row",
        ],
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _audit() -> dict[str, object]:
    return audit_rank_zero_aa_bb_d2c_odd_sqrt_q_collision_row(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
        d3_baseline=_d3_baseline(),
        d2a_row=_d2a_row(),
        d2b_row=_d2b_row(),
    )


def test_d2c_solves_pure_sqrt_q_collision_row_in_complete_d_coordinates() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "D2c_odd_sqrt_q_collision_row"
    assert audit["d2c_status"] == "pure_sqrt_q_collision_row_solved"
    assert audit["solved_local_row"] == {
        "id": "D2c_odd_sqrt_q_collision_row",
        "place_type": "ell|sqrt_q",
        "stratum": "pure_sqrt_q_collision",
        "applies_when": "ell odd, ell | sqrt_q, ell does not divide L*T",
        "coordinate_pair": ["d_pos_2sqrt_q", "d_neg_2sqrt_q"],
        "allowed_pair_rule": (
            "(d_pos_2sqrt_q,d_neg_2sqrt_q)=(lambda,lambda) for "
            "lambda in Q_ell*/Q_ell*2"
        ),
        "allowed_valuation_rule": "v_ell(d_pos_2sqrt_q) == v_ell(d_neg_2sqrt_q) mod 2",
        "allowed_unit_squareclass_rule": (
            "unit(d_pos_2sqrt_q) == unit(d_neg_2sqrt_q) in F_ell*/F_ell*2"
        ),
        "allowed_pair_squareclasses": [
            "(1,1)",
            "(nu,nu)",
            "(ell,ell)",
            "(nu*ell,nu*ell)",
        ],
        "nu": "any fixed nonsquare unit in Q_ell",
        "d_minus_p_from_product_relation": "1 in Q_ell*/Q_ell*2",
        "row_dimension_over_F2_local_only": 2,
        "local_c_d_row_solved": True,
    }


def test_d2c_records_sqrt_q_valuation_cases_without_adding_residue_obstruction() -> None:
    audit = _audit()

    assert audit["pure_sqrt_q_collision_stratum"] == {
        "prime_condition": "ell odd and ell | sqrt_q",
        "excluded_overlaps": ["ell | L", "ell | T"],
        "root_difference_squareclasses": {
            "e_pos-e_neg": (
                "4*sqrt_q has positive ell-adic valuation m=v_ell(sqrt_q); "
                "m is not assumed even"
            ),
            "e_pos-e_minus": "16*L^2 is an ell-adic square unit",
            "e_minus-e_neg": "4*T^2 is an ell-adic square unit",
        },
        "pure_stratum_residue_constraint": (
            "sqrt_q=T^2+4*L^2 and ell does not divide L*T force -1 to be "
            "a square modulo ell"
        ),
        "normal_form": (
            "after translating by e_minus and scaling by a square unit, the "
            "third root is 0 and the two colliding roots are 1 and "
            "1+epsilon with v_ell(epsilon)=m>0"
        ),
    }
    assert audit["sqrt_q_valuation_case_analysis"] == [
        {
            "case": "unit squareclasses",
            "realization": (
                "choose the node parameter z with v_ell(z)=0; then "
                "z and z-epsilon have the same prescribed unit squareclass"
            ),
        },
        {
            "case": "ramified squareclasses when m>=2",
            "realization": (
                "choose z with v_ell(z)=1<m; then z and z-epsilon have "
                "the same prescribed ramified squareclass"
            ),
        },
        {
            "case": "ramified squareclasses when m=1",
            "realization": (
                "the class of epsilon is realized by v_ell(z)>1, and the "
                "opposite ramified class is realized using a residue b with "
                "chi(b)=chi(b-1)=-1; such b exists because ell is odd and "
                "-1 is a square in the pure stratum"
            ),
        },
    ]
    assert audit["row_depends_on_v_ell_sqrt_q_parity"] is False
    assert audit["row_depends_on_sqrt_q_unit_residue"] is False
    assert audit["row_obstruction_remaining"] is False


def test_d2c_keeps_scope_below_matrix_and_marks_overlaps() -> None:
    audit = _audit()

    assert audit["wl475_referenced_only"] is True
    assert audit["wl476_referenced_only"] is True
    assert audit["local_c_d_rows_partially_solved"] is True
    assert audit["local_c_d_rows_solved"] is False
    assert audit["solved_row_ids"] == [
        "D2a_odd_L_collision_row",
        "D2b_odd_T_collision_row",
        "D2c_odd_sqrt_q_collision_row",
    ]
    assert audit["remaining_d2_obligations"] == [
        "D2d_dyadic_complete_row",
        "D2_multi_collision_overlaps",
    ]
    assert audit["multi_collision_obligations"] == [
        {
            "condition": "ell | sqrt_q and ell | L",
            "reason": "e_pos-e_minus=16*L^2 is no longer an ell-adic unit",
            "status": "multi_collision_obligation_not_solved_here",
        },
        {
            "condition": "ell | sqrt_q and ell | T",
            "reason": "e_minus-e_neg=4*T^2 is no longer an ell-adic unit",
            "status": "multi_collision_obligation_not_solved_here",
        },
    ]
    assert audit["overlap_cases_solved_here"] is False
    assert audit["full_c_d_matrix_built"] is False
    assert audit["d4_entered"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY


def test_d2c_rejects_missing_d2c_obligation_or_overadvanced_prior_row() -> None:
    d2 = _d2_rows()
    d2["local_row_obligations"] = [
        {"id": "D2a_odd_L_collision_row", "place_type": "ell|L"},
        {"id": "D2b_odd_T_collision_row", "place_type": "ell|T"},
    ]
    d2b = _d2b_row()
    d2b["complete_selmer_upper_bound_proved"] = True

    audit = audit_rank_zero_aa_bb_d2c_odd_sqrt_q_collision_row(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=d2,
        d3_baseline=_d3_baseline(),
        d2a_row=_d2a_row(),
        d2b_row=d2b,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == [
        "d2c_obligation_missing",
        "d2b_already_claims_selmer_bound",
    ]
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_d2c_cli_writes_scoped_result(tmp_path: Path) -> None:
    d0 = tmp_path / "d0.json"
    d1 = tmp_path / "d1.json"
    d2 = tmp_path / "d2.json"
    d3 = tmp_path / "d3.json"
    d2a = tmp_path / "d2a.json"
    d2b = tmp_path / "d2b.json"
    out = tmp_path / "d2c.json"
    d0.write_text(json.dumps(_d0_container()), encoding="utf-8")
    d1.write_text(json.dumps(_d1_support()), encoding="utf-8")
    d2.write_text(json.dumps(_d2_rows()), encoding="utf-8")
    d3.write_text(json.dumps(_d3_baseline()), encoding="utf-8")
    d2a.write_text(json.dumps(_d2a_row()), encoding="utf-8")
    d2b.write_text(json.dumps(_d2b_row()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_d2c_odd_sqrt_q_collision_row.py",
            "--d0-container",
            str(d0),
            "--d1-support",
            str(d1),
            "--d2-rows",
            str(d2),
            "--d3-baseline",
            str(d3),
            "--d2a-row",
            str(d2a),
            "--d2b-row",
            str(d2b),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "d2c_status=pure_sqrt_q_collision_row_solved" in result.stdout
    assert "full_c_d_matrix_built=False" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["solved_local_row"]["allowed_pair_rule"].startswith(
        "(d_pos_2sqrt_q,d_neg_2sqrt_q)=(lambda,lambda)"
    )
    assert payload["row_depends_on_v_ell_sqrt_q_parity"] is False
    assert payload["complete_selmer_upper_bound_proved"] is False
