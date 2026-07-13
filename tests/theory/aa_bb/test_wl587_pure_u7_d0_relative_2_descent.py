from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.wl587_pure_u7_d0_relative_2_descent import (
    build_wl587_pure_u7_d0_relative_2_descent,
)


def test_wl587_builds_a_complete_pure_u7_d0_certificate() -> None:
    audit = build_wl587_pure_u7_d0_relative_2_descent()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl587"
    assert audit["scope"] == "support=u_7|L=7|T=9|d=(7,7,1), R^2=P_op only"
    assert audit["verification"]["violations"] == []
    assert audit["proof_boundary"]["D0_certificate_proved_here"] is True
    assert audit["proof_boundary"]["advance_to_D1"] is False


def test_wl587_source_maps_and_squareclass_data_are_complete() -> None:
    audit = build_wl587_pure_u7_d0_relative_2_descent()
    source = audit["source_cover"]
    divisors = audit["divisors_and_branch_cover"]
    picard = audit["picard_and_twists"]

    assert source["identity_checks"]
    assert all(source["identity_checks"].values())
    assert divisors["factor_divisors"]["branch_divisor_mod_2"].startswith("B=")
    assert all(divisors["reduced_and_disjoint_checks"].values())
    assert divisors["genus_certificate"]["smooth_normalization_genus"] == 17
    assert divisors["factor_cover_reduction_checks"]
    assert all(divisors["factor_cover_reduction_checks"].values())
    assert (
        picard["picard_square_root_data"]["factor_plus"]["square_root_line_bundle"]
        == "L_plus=O_C(D_t)"
    )
    assert (
        picard["picard_square_root_data"]["factor_minus"]["square_root_line_bundle"]
        == "L_minus=O_C(D_t)"
    )
    assert picard["picard_square_root_data"]["factor_plus"]["Pic0_class"] == ("[D_t-8*O]")
    assert picard["picard_square_root_data"]["factor_minus"]["Pic0_class"] == ("[D_t-8*O]")
    assert picard["picard_square_root_data"]["four_square_roots_of_O_B"]["set"] == [
        "L0",
        "L0 tensor [W1-W2]",
        "L0 tensor [W1-W3]",
        "L0 tensor [W1-W4]",
    ]
    assert picard["picard_square_root_data"]["four_square_roots_of_O_B"]["role"].endswith(
        "not the constant factor-twist set"
    )
    assert picard["jacobian_model"]["factorization"] == ("(x-22704)*(x+5520)*(x+17184)")
    assert picard["factor_twist_set"]["positive_2adic_survivor_count"] == 16
    assert picard["factor_twist_set"]["all_Q_S_twists"] == {
        "count": 256,
        "all_squarefree_signed_representatives": True,
    }
    assert audit["verification"]["checks"]["factor_cover_role_separation"] is True
    assert divisors["fixed_square_locus"]["generic_function_field_degree"] == 2
    assert divisors["fixed_square_locus"]["factor_cover_generic_function_field_degree"] == 4


def test_wl587_handles_local_and_exceptional_branches() -> None:
    audit = build_wl587_pure_u7_d0_relative_2_descent()
    local = audit["local_exception_and_bad_fiber_data"]
    branches = local["exceptional_and_denominator_branches"]

    assert local["two_adic_source_analysis"]["conclusion"].startswith(
        "F_plus, F_minus, and P_op are Q2 squares at every finite Q2 source point"
    )
    assert all(local["two_adic_source_analysis"]["structural_checks"].values())
    assert audit["verification"]["checks"]["two_adic_analysis"] is True
    assert local["real_analysis"]["positivity"] == "N>0 and M>0 iff -9<t<9"
    assert all(local["real_analysis"]["structural_checks"].values())
    for name in [
        "r=0",
        "r=infinity",
        "u0=0",
        "u_plus=0",
        "W=0",
        "F_plus=0",
        "F_minus=0",
        "R=0",
    ]:
        assert name in branches
    assert len(local["bad_fiber_set"]["reduction_summary"]) == 7
    assert local["bad_fiber_set"]["odd_bad_fibers_resolved"] is False
    assert set(local["bad_fiber_set"]["odd_bad_fiber_inputs"]) == {
        "3",
        "5",
        "7",
        "53",
        "97",
        "277",
    }
    assert all(
        row["status"] == "unevaluated_D0_input"
        for row in local["bad_fiber_set"]["odd_bad_fiber_inputs"].values()
    )


def test_wl587_keeps_exact_aa_bb_lift_conditions() -> None:
    audit = build_wl587_pure_u7_d0_relative_2_descent()
    lift = audit["aa_bb_lift"]

    assert lift["definitions"]["AA_source_leg"] == 7
    assert lift["definitions"]["BB_source_leg"] == 7
    assert lift["definitions"]["opposite_leg"] == 2
    assert len(lift["exact_conditions"]) == 4
    assert lift["sample_non_square_specialization"]["P_op_is_square"] is False
    assert audit["proof_boundary"]["rational_point_classification"] is False


def test_wl587_factor_twists_are_bidirectionally_complete() -> None:
    audit = build_wl587_pure_u7_d0_relative_2_descent()
    completeness = audit["factor_twist_completeness"]

    assert (
        completeness["rational_square_locus_bidirectional_completeness"][
            "forward_factor_cover_to_fixed_cover"
        ]
        is True
    )
    assert (
        completeness["rational_square_locus_bidirectional_completeness"][
            "reverse_fixed_square_locus_to_factor_cover"
        ]
        is True
    )
    assert (
        completeness["rational_square_locus_bidirectional_completeness"][
            "rational_zero_pole_branches_closed"
        ]
        is True
    )
    assert completeness["factor_cover_S_sufficiency"]["all_factor_branch_checks_pass"] is True
    assert completeness["factor_cover_S_sufficiency"]["factor_specific_S_support_check"] is True
    assert completeness["factor_value_squareclass_lemma"]["universal_parity_check"] is True
    assert (
        completeness["rational_square_locus_bidirectional_completeness"][
            "listed_exceptional_branch_set_is_complete"
        ]
        is True
    )
    assert completeness["factor_twist_candidates"] == {
        "Q_S_mod_squares_count": 256,
        "real_and_Q2_filtered_count": 16,
        "odd_bad_fiber_filter_applied": False,
    }
