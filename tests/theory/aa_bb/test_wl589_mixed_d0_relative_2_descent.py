from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.wl589_mixed_d0_relative_2_descent import (
    build_wl589_mixed_d0_relative_2_descent,
)


def test_wl589_builds_a_complete_mixed_d0_certificate() -> None:
    audit = build_wl589_mixed_d0_relative_2_descent()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl589"
    assert audit["scope"] == ("support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85), R^2=P_op only")
    assert audit["verification"]["violations"] == []
    assert audit["proof_boundary"]["D0_certificate_proved_here"] is True
    assert audit["proof_boundary"]["advance_to_D1"] is False


def test_wl589_source_maps_and_divisors_are_complete() -> None:
    audit = build_wl589_mixed_d0_relative_2_descent()
    source = audit["source_cover"]
    divisors = audit["divisors_and_branch_cover"]
    picard = audit["picard_and_twists"]

    assert all(source["identity_checks"].values())
    assert source["parameters"]["p"] == -128
    assert source["parameters"]["sqrt_q"] == 136
    assert source["parameters"]["q"] == 18496
    assert source["parameters"]["d_vector"] == {
        "d_minus_p": 15,
        "d_pos_2sqrt_q": 51,
        "d_neg_2sqrt_q": 85,
    }
    assert source["function_field"]["affine_equation"] == (
        "W^2 = 289*r^4 - 408*r^3 + 274*r^2 - 120*r + 25"
    )
    assert all(source["map_coverage_checks"].values())
    assert source["map_coverage_checks"]["tangent_r"] == "10/17"
    assert source["map_coverage_checks"]["infinity_branch_count"] == 2
    assert all(divisors["reduced_and_disjoint_checks"].values())
    assert divisors["factor_divisors"]["branch_degree"] == 32
    assert divisors["factor_divisors"]["pole_degree"] == 8
    assert divisors["fixed_square_locus"]["smooth_normalization_genus"] == 17
    assert divisors["square_locus_affine_model"]["source_open_condition"] == ("D(r)*A(r) != 0")
    assert all(divisors["denominator_chart_checks"].values())
    assert picard["jacobian_model"]["factorization"] == ("(u-516)*(u-192)*(u+708)")
    assert all(picard["jacobian_model"]["polynomial_checks"].values())
    assert picard["factor_twist_set"]["all_Q_S_twists"]["count"] == 256


def test_wl589_handles_real_q2_and_odd_bad_fiber_inputs() -> None:
    audit = build_wl589_mixed_d0_relative_2_descent()
    local = audit["local_exception_and_bad_fiber_data"]
    branches = local["exceptional_and_denominator_branches"]

    assert local["real_analysis"]["positivity"] == ("N>0 and M>0 iff -10<t<10")
    assert all(local["real_analysis"]["structural_checks"].values())
    q2 = local["two_adic_source_analysis"]
    assert q2["factor_squareclass"] == "[F_plus]=[F_minus]=[5] in Q2*/Q2*2"
    assert q2["positive_twist_residue_mod_8"] == 5
    assert all(q2["structural_checks"].values())
    for name in [
        "r=0",
        "r=infinity",
        "u0=0",
        "D=0 denominator",
        "u_plus=0",
        "W=0",
        "F_plus=0",
        "F_minus=0",
        "R=0",
    ]:
        assert name in branches
    assert set(local["bad_fiber_set"]["odd_bad_fiber_inputs"]) == {
        "3",
        "5",
        "7",
        "17",
        "29",
        "37",
    }
    assert all(
        row["status"] == "unevaluated_D0_input"
        for row in local["bad_fiber_set"]["odd_bad_fiber_inputs"].values()
    )
    assert local["bad_fiber_set"]["odd_bad_fibers_resolved"] is False


def test_wl589_keeps_exact_aa_bb_lift_conditions() -> None:
    audit = build_wl589_mixed_d0_relative_2_descent()
    lift = audit["aa_bb_lift"]

    assert lift["orientation_table"] == [
        {"quotient": "AA", "A": 3, "B": 7, "L": 3, "source_leg": 3, "opposite_leg": 7},
        {"quotient": "BB", "A": 7, "B": 3, "L": 3, "source_leg": 3, "opposite_leg": 7},
    ]
    assert all(lift["orientation_checks"].values())
    assert lift["definitions"]["source_leg"] == 3
    assert lift["definitions"]["opposite_leg"] == 7
    assert len(lift["exact_conditions"]) == 4
    assert lift["sample_non_square_specialization"]["P_op_is_square"] is False
    assert all(lift["structural_checks"].values())


def test_wl589_factor_twists_are_bidirectionally_complete() -> None:
    audit = build_wl589_mixed_d0_relative_2_descent()
    completeness = audit["factor_twist_completeness"]

    assert completeness["rational_square_locus_bidirectional_completeness"] == {
        "forward_factor_cover_to_fixed_cover": True,
        "reverse_fixed_square_locus_to_factor_cover": True,
        "rational_zero_pole_branches_closed": True,
        "listed_exceptional_branch_set_is_complete": True,
    }
    assert completeness["factor_cover_S_sufficiency"]["all_factor_branch_checks_pass"] is True
    assert completeness["factor_cover_S_sufficiency"]["factor_specific_S_support_check"] is True
    assert completeness["factor_value_squareclass_lemma"]["universal_parity_check"] is True
    assert completeness["factor_twist_candidates"]["Q_S_mod_squares_count"] == 256
    assert completeness["factor_twist_candidates"]["real_and_Q2_filtered_count"] == 16
    assert completeness["factor_twist_candidates"]["odd_bad_fiber_filter_applied"] is False
    assert completeness["factor_twist_candidates"]["real_Q2_survivors"] == [
        5,
        21,
        29,
        37,
        85,
        357,
        493,
        629,
        3045,
        3885,
        5365,
        22533,
        51765,
        66045,
        91205,
        383061,
    ]
