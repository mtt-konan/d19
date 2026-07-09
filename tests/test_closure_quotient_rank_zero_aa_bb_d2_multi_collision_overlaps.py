from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_d2_multi_collision_overlaps import (
    BOUNDARY,
    audit_rank_zero_aa_bb_d2_multi_collision_overlaps,
    overlap_support_for_odd_prime,
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


def _prior_row(lemma_id: str, status_key: str, status_value: str) -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "lemma_id": lemma_id,
        status_key: status_value,
        "local_c_d_rows_partially_solved": True,
        "local_c_d_rows_solved": False,
        "full_c_d_matrix_built": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _d2a_row() -> dict[str, object]:
    return _prior_row(
        "D2a_odd_L_collision_row",
        "d2a_status",
        "pure_L_collision_row_solved",
    )


def _d2b_row() -> dict[str, object]:
    return _prior_row(
        "D2b_odd_T_collision_row",
        "d2b_status",
        "pure_T_collision_row_solved",
    )


def _d2c_row() -> dict[str, object]:
    return _prior_row(
        "D2c_odd_sqrt_q_collision_row",
        "d2c_status",
        "pure_sqrt_q_collision_row_solved",
    )


def _d2d_row() -> dict[str, object]:
    return _prior_row(
        "D2d_dyadic_complete_row",
        "d2d_status",
        "dyadic_complete_row_solved",
    )


def _audit() -> dict[str, object]:
    return audit_rank_zero_aa_bb_d2_multi_collision_overlaps(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
        d3_baseline=_d3_baseline(),
        d2a_row=_d2a_row(),
        d2b_row=_d2b_row(),
        d2c_row=_d2c_row(),
        d2d_row=_d2d_row(),
    )


def test_overlap_support_equivalence_for_odd_primes() -> None:
    assert overlap_support_for_odd_prime(3, L=3, T=5) == {
        "ell": 3,
        "sqrt_q": 61,
        "divides_L": True,
        "divides_T": False,
        "divides_sqrt_q": False,
        "divides_at_least_two": False,
        "divides_gcd_L_T": False,
        "divides_all_three": False,
    }
    assert overlap_support_for_odd_prime(5, L=2, T=5) == {
        "ell": 5,
        "sqrt_q": 41,
        "divides_L": False,
        "divides_T": True,
        "divides_sqrt_q": False,
        "divides_at_least_two": False,
        "divides_gcd_L_T": False,
        "divides_all_three": False,
    }
    assert overlap_support_for_odd_prime(3, L=3, T=6) == {
        "ell": 3,
        "sqrt_q": 72,
        "divides_L": True,
        "divides_T": True,
        "divides_sqrt_q": True,
        "divides_at_least_two": True,
        "divides_gcd_L_T": True,
        "divides_all_three": True,
    }


def test_d2_multi_collision_overlaps_are_impossible_under_primitive_normalization() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["lemma_id"] == "D2_multi_collision_overlaps"
    assert audit["d2_multi_status"] == (
        "odd_multi_collision_overlaps_impossible_under_primitive_normalization"
    )
    assert audit["multi_collision_overlaps_possible_under_aa_bb_inputs"] is False
    assert audit["overlap_gcd_lemma"] == {
        "id": "odd_overlap_equivalence_to_gcd_L_T",
        "statement": (
            "For odd ell and sqrt_q=T^2+4*L^2, ell divides at least two of "
            "{L,T,sqrt_q} if and only if ell divides gcd(L,T); in that case "
            "ell divides all three."
        ),
        "pair_implications": [
            "ell|L and ell|T imply ell|sqrt_q",
            "ell|L and ell|sqrt_q imply ell|T",
            "ell|T and ell|sqrt_q imply ell|L",
        ],
    }
    assert audit["primitive_normalization_inputs_needed"] == [
        "A:B is primitive, so gcd(A,B)=1",
        "T=A+B",
        "L=A on the AA side or L=B on the BB side",
        "therefore gcd(L,T)=1",
        "ell is odd; ell=2 is handled only by wl478",
    ]
    assert audit["complete_local_c_d_row_for_overlaps"] == "vacuous_empty_row"


def test_d2_multi_collision_marks_d2_rows_complete_but_no_selmer_bound() -> None:
    audit = _audit()

    assert audit["solved_row_ids"] == [
        "D2a_odd_L_collision_row",
        "D2b_odd_T_collision_row",
        "D2c_odd_sqrt_q_collision_row",
        "D2d_dyadic_complete_row",
        "D2_multi_collision_overlaps",
    ]
    assert audit["remaining_d2_obligations"] == []
    assert audit["local_c_d_rows_solved"] is True
    assert audit["full_c_d_matrix_built"] is False
    assert audit["d4_entered"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["boundary"] == BOUNDARY


def test_d2_multi_collision_rejects_overadvanced_prior_row() -> None:
    d2d = _d2d_row()
    d2d["complete_selmer_upper_bound_proved"] = True

    audit = audit_rank_zero_aa_bb_d2_multi_collision_overlaps(
        d0_container=_d0_container(),
        d1_support=_d1_support(),
        d2_rows=_d2_rows(),
        d3_baseline=_d3_baseline(),
        d2a_row=_d2a_row(),
        d2b_row=_d2b_row(),
        d2c_row=_d2c_row(),
        d2d_row=d2d,
    )

    assert audit["status"] == "issues"
    assert audit["violations"] == ["d2d_already_claims_selmer_bound"]
    assert audit["complete_selmer_upper_bound_proved"] is False


def test_d2_multi_collision_cli_writes_scoped_result(tmp_path: Path) -> None:
    d0 = tmp_path / "d0.json"
    d1 = tmp_path / "d1.json"
    d2 = tmp_path / "d2.json"
    d3 = tmp_path / "d3.json"
    d2a = tmp_path / "d2a.json"
    d2b = tmp_path / "d2b.json"
    d2c = tmp_path / "d2c.json"
    d2d = tmp_path / "d2d.json"
    out = tmp_path / "d2_multi.json"
    d0.write_text(json.dumps(_d0_container()), encoding="utf-8")
    d1.write_text(json.dumps(_d1_support()), encoding="utf-8")
    d2.write_text(json.dumps(_d2_rows()), encoding="utf-8")
    d3.write_text(json.dumps(_d3_baseline()), encoding="utf-8")
    d2a.write_text(json.dumps(_d2a_row()), encoding="utf-8")
    d2b.write_text(json.dumps(_d2b_row()), encoding="utf-8")
    d2c.write_text(json.dumps(_d2c_row()), encoding="utf-8")
    d2d.write_text(json.dumps(_d2d_row()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_d2_multi_collision_overlaps.py",
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
            "--d2c-row",
            str(d2c),
            "--d2d-row",
            str(d2d),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "d2_multi_status=odd_multi_collision_overlaps_impossible" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["complete_local_c_d_row_for_overlaps"] == "vacuous_empty_row"
    assert payload["complete_selmer_upper_bound_proved"] is False
