"""Focused tests for the Berry C_1 B2 rank and saturation boundary."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def _result():
    from scripts.theory.berry_sextic_b2_rank_boundary import verify_b2

    return verify_b2()


def test_global_branch_algebra_proves_no_rational_two_torsion() -> None:
    result = _result()
    branch = result["global_branch_algebra"]

    assert result["status"] == "ok"
    assert branch["checks"] == {
        "i_square_root": True,
        "q2_gcd_is_one": True,
        "q3_gcd_is_one": True,
        "q6_frobenius_remainder_is_x": True,
    }
    assert result["rank"]["j2_dimension_over_K"] == 0


def test_structural_point_relations_are_exactly_div_t() -> None:
    result = _result()
    points = result["points_and_relations"]

    assert points["principal_divisor"] == "div(t)=A_plus+A_minus-P_plus-P_minus"
    assert points["class_relation"] == "E_plus+E_minus+D_inf=0"
    assert points["all_relation_vectors"] == (
        "Z*(1,1,1) in the ordered basis (E_plus,E_minus,D_inf)"
    )


def test_good_reduction_certifies_rank_two_independence() -> None:
    result = _result()
    reduction = result["reduction"]

    assert reduction["prime_ideal"] == "(269, i-82)"
    assert reduction["curve_counts"] == {"C(F_269)": 282, "C(F_269^2)": 72430}
    assert reduction["jacobian_order"] == 75708
    assert reduction["jacobian_group_invariants"] == [3, 25236]
    assert reduction["mod_3_coordinates"] == {
        "E_plus": [2, 1],
        "D_inf": [0, 1],
    }
    assert reduction["mod_3_determinant"] == 2
    assert reduction["no_global_point_search"] is True
    assert result["rank"]["rank_lower_bound"] == 2


def test_selmer_bound_keeps_sha_and_saturation_distinct() -> None:
    result = _result()

    assert result["rank"]["selmer_dimension"] == 3
    assert result["rank"]["certified_rank_interval"] == [2, 3]
    assert result["rank"]["sha_2_dimension_formula"] == ("dim Sha(J/K)[2] = 3-rank J(K)")
    assert result["saturation"]["H_rank"] == 2
    assert result["saturation"]["H_is_2_saturated"] is False
    assert result["saturation"]["kummer_image_of_H_dimension"] == 1
    assert result["t0_fake_squareclass"]["finite_evaluation_at_t0"] == "-theta"
    assert result["t0_fake_squareclass"]["beta_squared"] == "-i*theta"
    assert result["t0_fake_squareclass"]["exact_polynomial_remainder_zero"] is True
    assert result["proof_boundary"]["full_mordell_weil_basis"] is False
    assert result["proof_boundary"]["rational_t_claimed"] is False


def test_exact_sage_certificate_is_proof_enabled_and_narrow() -> None:
    source = (ROOT / "scripts/theory/berry_sextic_b2_rank_boundary.sage").read_text(
        encoding="utf-8"
    )

    assert "proof.all(True)" in source
    assert "TwoSelmerGroup" not in source
    assert "rational_points" not in source
    assert "269, i-82" in source
