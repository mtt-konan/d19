from __future__ import annotations

import sys
from fractions import Fraction
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def _is_rational_square(value: Fraction) -> bool:
    num = isqrt(value.numerator)
    den = isqrt(value.denominator)
    return num * num == value.numerator and den * den == value.denominator


def test_rational_ratio_membership_uses_both_square_conditions() -> None:
    from rational_distance.concordant.rational_ratio import is_rational_ratio_member

    assert is_rational_ratio_member(Fraction(7), Fraction(12, 5))
    assert is_rational_ratio_member(Fraction(7), Fraction(35, 12))
    assert not is_rational_ratio_member(Fraction(7), Fraction(1))
    assert not is_rational_ratio_member(Fraction(3, 4), Fraction(3, 4))


def test_reciprocal_ratio_preserves_membership_for_rational_lambda() -> None:
    from rational_distance.concordant.rational_ratio import reciprocal_ratio

    lam = Fraction(7)
    r = Fraction(12, 5)

    assert reciprocal_ratio(lam, r) == Fraction(35, 12)


def test_rational_ratio_hits_check_full_plane_targets() -> None:
    from rational_distance.concordant.rational_ratio import find_rational_ratio_hits

    ratios = (Fraction(2), Fraction(6), Fraction(10))
    hits = find_rational_ratio_hits(Fraction(7), ratios)

    assert [(hit.r1, hit.r2, hit.relation, hit.centerline) for hit in hits] == [
        (Fraction(2), Fraction(6), "sum=A+B", False),
        (Fraction(2), Fraction(10), "diff=A+B", False),
    ]


def test_rational_ratio_hit_product_diagnostics_identify_reciprocal_pair() -> None:
    from rational_distance.concordant.rational_ratio import (
        rational_ratio_hit_product_diagnostics,
    )

    diagnostics = rational_ratio_hit_product_diagnostics(
        Fraction(6),
        (Fraction(2), Fraction(3)),
    )

    assert len(diagnostics) == 1
    diagnostic = diagnostics[0]
    assert diagnostic.r1 == Fraction(2)
    assert diagnostic.r2 == Fraction(3)
    assert diagnostic.relation == "sum=|A-B|"
    assert diagnostic.product == Fraction(6)
    assert diagnostic.product_equals_lambda
    assert diagnostic.reciprocal_pair
    assert not diagnostic.true_member_pair


def test_reciprocal_orbit_sum_ab_roots_are_not_true_members_for_rational_lambda() -> None:
    from rational_distance.concordant.rational_ratio import (
        full_plane_reciprocal_obstruction,
        reciprocal_sum_ab_roots,
        sum_ab_reciprocal_obstruction,
        true_reciprocal_sum_ab_roots,
    )

    lam = Fraction(3, 4)

    assert reciprocal_sum_ab_roots(lam) == (Fraction(1), Fraction(3, 4))
    assert true_reciprocal_sum_ab_roots(lam) == ()

    obstruction = sum_ab_reciprocal_obstruction(lam)

    assert obstruction.lambda_ratio == lam
    assert obstruction.roots == (Fraction(1), lam)
    assert obstruction.forced_unit_root == Fraction(1)
    assert obstruction.unit_leg_value == Fraction(2)
    assert not obstruction.unit_leg_is_square
    assert obstruction.true_roots == ()
    assert obstruction.branch_closed

    full_plane = full_plane_reciprocal_obstruction(lam)

    assert full_plane.lambda_ratio == lam
    assert full_plane.all_branches_closed
    assert full_plane.by_relation["sum=A+B"].roots == (lam, Fraction(1))
    assert full_plane.by_relation["sum=A+B"].true_roots == ()


def test_product_identity_holds_for_rational_lambda() -> None:
    from rational_distance.concordant.rational_ratio import product_identity_terms

    lam = Fraction(7, 3)
    target = lam + 1
    product = Fraction(5, 2)

    terms = product_identity_terms(lam, target, product)

    assert terms.b_minus_lambda_sq_a == (lam * lam - 1) * (lam * lam - product * product)


def test_closure_product_identity_uses_difference_sign() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_DIFF_AB,
        REL_SUM_AB,
        closure_product_identity_terms,
        closure_product_square_conditions,
    )

    lam = Fraction(7, 3)
    target = Fraction(5)
    product = Fraction(2)

    sum_terms = closure_product_identity_terms(lam, target, product, REL_SUM_AB)
    diff_terms = closure_product_identity_terms(lam, target, product, REL_DIFF_AB)

    assert sum_terms.a_term == product * product - 2 * product + target * target + 1
    assert diff_terms.a_term == product * product + 2 * product + target * target + 1
    assert diff_terms.b_term == (
        product * product
        + 2 * lam * lam * product
        + lam * lam * target * target
        + lam**4
    )
    assert diff_terms.b_minus_lambda_sq_a == (
        (lam * lam - 1) * (lam * lam - product * product)
    )

    diff_conditions = closure_product_square_conditions(lam, target, product, REL_DIFF_AB)

    assert diff_conditions.discriminant == target * target + 4 * product
    assert diff_conditions.roots == ()

    diff_product_with_roots = Fraction(16, 9)
    diff_conditions = closure_product_square_conditions(
        lam,
        target,
        diff_product_with_roots,
        REL_DIFF_AB,
    )

    assert diff_conditions.roots == (Fraction(1, 3), Fraction(16, 3))
    assert not diff_conditions.true_member_pair


def test_sum_ab_product_square_conditions_do_not_imply_membership() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        closure_product_identity_terms,
        closure_product_square_conditions,
        is_rational_ratio_member,
    )

    lam = Fraction(535, 161)
    r = Fraction(14, 23)
    s = Fraction(26, 7)
    product = r * s
    target = lam + 1

    terms = closure_product_identity_terms(lam, target, product, REL_SUM_AB)
    discriminant = target * target - 4 * product

    assert r + s == target
    assert product != lam
    assert terms.a_term == Fraction(525625, 25921)
    assert terms.b_term == Fraction(190463289241, 671898241)
    assert discriminant == Fraction(250000, 25921)
    assert _is_rational_square(terms.a_term)
    assert _is_rational_square(terms.b_term)
    assert _is_rational_square(discriminant)
    assert not is_rational_ratio_member(lam, r)
    assert not is_rational_ratio_member(lam, s)

    conditions = closure_product_square_conditions(lam, target, product, REL_SUM_AB)

    assert conditions.discriminant == discriminant
    assert conditions.roots == (r, s)
    assert not conditions.centerline
    assert not conditions.reciprocal_pair
    assert conditions.product_square_bucket == "residual"
    assert conditions.product_terms_are_squares
    assert not conditions.true_member_pair
    assert conditions.member_square_flags == (False, False, False, False)
    assert conditions.member_squareclasses == (29, 29, 29, 29)
    assert conditions.member_squareclass_pair == (29, 29)
    assert len(set(conditions.member_squareclasses)) == 1
    assert conditions.member_squareclasses_pairwise_equal
    assert conditions.product_square_explained_by_pairwise_squareclasses
    assert conditions.member_squareclasses_all_equal
    assert not conditions.member_squareclasses_all_trivial

    mixed_conditions = closure_product_square_conditions(
        Fraction(2),
        Fraction(3),
        Fraction(9, 4),
        REL_SUM_AB,
    )

    assert mixed_conditions.product_terms_are_squares
    assert mixed_conditions.centerline
    assert not mixed_conditions.reciprocal_pair
    assert mixed_conditions.product_square_bucket == "centerline"
    assert mixed_conditions.member_squareclasses == (13, 13, 1, 1)
    assert mixed_conditions.member_squareclass_pair == (13, 1)
    assert mixed_conditions.member_squareclasses_pairwise_equal
    assert mixed_conditions.product_square_explained_by_pairwise_squareclasses
    assert not mixed_conditions.member_squareclasses_all_equal

    true_conditions = closure_product_square_conditions(
        Fraction(1),
        Fraction(25, 12),
        Fraction(1),
        REL_SUM_AB,
    )

    assert true_conditions.true_member_pair
    assert true_conditions.roots == (Fraction(3, 4), Fraction(4, 3))
    assert true_conditions.member_squareclass_pair == (1, 1)
    assert true_conditions.member_squareclasses_pairwise_equal
    assert true_conditions.product_square_explained_by_pairwise_squareclasses
    assert true_conditions.member_squareclasses_all_equal
    assert true_conditions.member_squareclasses_all_trivial

    reciprocal_conditions = closure_product_square_conditions(
        Fraction(7),
        Fraction(8),
        Fraction(7),
        REL_SUM_AB,
    )

    assert reciprocal_conditions.roots == (Fraction(1), Fraction(7))
    assert not reciprocal_conditions.centerline
    assert reciprocal_conditions.reciprocal_pair
    assert reciprocal_conditions.product_square_bucket == "reciprocal"
    assert reciprocal_conditions.member_squareclass_pair == (2, 2)
    assert not reciprocal_conditions.true_member_pair


def test_sum_ab_slope_pair_translates_to_rational_ratio_membership() -> None:
    from rational_distance.concordant.rational_ratio import (
        is_pythagorean_leg_ratio,
        sum_ab_point_from_slopes,
        sum_ab_product_square_condition_from_slopes,
    )

    point = sum_ab_point_from_slopes(Fraction(3, 4), Fraction(4, 3))

    assert point is not None
    assert point.lambda_ratio == Fraction(12, 13)
    assert point.r1 == Fraction(9, 13)
    assert point.r2 == Fraction(16, 13)
    assert point.closes_sum_ab
    assert is_pythagorean_leg_ratio(point.slope1)
    assert is_pythagorean_leg_ratio(point.slope2)
    assert not point.true_member_pair

    residual_condition = sum_ab_product_square_condition_from_slopes(
        Fraction(14, 23) / Fraction(535, 161),
        Fraction(26, 7) / Fraction(535, 161),
    )

    assert residual_condition is not None
    assert residual_condition.lambda_ratio == Fraction(535, 161)
    assert residual_condition.roots == (Fraction(14, 23), Fraction(26, 7))
    assert residual_condition.product_square_bucket == "residual"
    assert residual_condition.member_squareclass_pair == (29, 29)


def test_sum_ab_centerline_squareclass_conditions_explain_midpoint_hits() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        sum_ab_centerline_squareclass_conditions,
    )

    conditions = sum_ab_centerline_squareclass_conditions(Fraction(3))

    assert conditions.relation == REL_SUM_AB
    assert conditions.roots == (Fraction(2), Fraction(2))
    assert conditions.centerline
    assert conditions.product == Fraction(4)
    assert conditions.product_terms_are_squares
    assert conditions.member_squareclasses == (5, 5, 13, 13)
    assert conditions.member_squareclass_pair == (5, 13)
    assert conditions.member_squareclasses_pairwise_equal
    assert not conditions.true_member_pair
    assert conditions.centerline_obstruction == "both-legs"

    unit_conditions = sum_ab_centerline_squareclass_conditions(Fraction(1))

    assert unit_conditions.roots == (Fraction(1), Fraction(1))
    assert unit_conditions.member_squareclass_pair == (2, 2)
    assert not unit_conditions.true_member_pair
    assert unit_conditions.centerline_obstruction == "both-legs"

    lambda_leg_conditions = sum_ab_centerline_squareclass_conditions(Fraction(15))

    assert lambda_leg_conditions.member_squareclass_pair == (65, 1)
    assert lambda_leg_conditions.centerline_obstruction == "unit-leg"


def test_sum_ab_centerline_equations_expose_two_square_conditions() -> None:
    from rational_distance.concordant.rational_ratio import sum_ab_centerline_equations

    equations = sum_ab_centerline_equations(Fraction(3))

    assert equations.lambda_ratio == Fraction(3)
    assert equations.center == Fraction(2)
    assert equations.unit_value == Fraction(5)
    assert equations.lambda_value == Fraction(13)
    assert not equations.unit_is_square
    assert not equations.lambda_is_square
    assert equations.unit_squareclass == 5
    assert equations.lambda_squareclass == 13
    assert not equations.true_member
    assert equations.obstruction == "both-legs"

    lambda_leg = sum_ab_centerline_equations(Fraction(15))

    assert lambda_leg.center == Fraction(8)
    assert lambda_leg.unit_value == Fraction(65)
    assert lambda_leg.lambda_value == Fraction(289)
    assert not lambda_leg.unit_is_square
    assert lambda_leg.lambda_is_square
    assert lambda_leg.unit_squareclass == 65
    assert lambda_leg.lambda_squareclass == 1
    assert not lambda_leg.true_member
    assert lambda_leg.obstruction == "unit-leg"


def test_sum_ab_centerline_unit_leg_param_reduces_to_lambda_leg_check() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_centerline_from_unit_leg_param,
    )

    model = sum_ab_centerline_from_unit_leg_param(Fraction(3, 5))

    assert model.parameter == Fraction(3, 5)
    assert model.center == Fraction(15, 8)
    assert model.lambda_ratio == Fraction(11, 4)
    assert model.unit_hypotenuse == Fraction(17, 8)
    assert model.equations.unit_is_square
    assert model.equations.unit_value == Fraction(289, 64)
    assert not model.equations.lambda_is_square
    assert model.equations.lambda_value == Fraction(709, 64)
    assert model.remaining_squareclass == 709
    assert not model.true_member


def test_sum_ab_centerline_remaining_quartic_matches_lambda_leg_value() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_centerline_quartic_negative_reciprocal_quotient,
        sum_ab_centerline_quartic_pari_diagnostics,
        sum_ab_centerline_quartic_self_similarity,
        sum_ab_centerline_quotient_w_parameterization,
        sum_ab_centerline_remaining_quartic,
    )

    quartic = sum_ab_centerline_remaining_quartic(Fraction(3, 5))

    assert quartic.parameter == Fraction(3, 5)
    assert quartic.coefficients == (1, 8, 18, -8, 1)
    assert quartic.quartic_value == Fraction(2836, 625)
    assert quartic.denominator_square == Fraction(256, 625)
    assert quartic.lambda_value == Fraction(709, 64)
    assert quartic.lambda_value == quartic.quartic_value / quartic.denominator_square
    assert quartic.squareclass == 709
    assert not quartic.is_square

    self_similarity = sum_ab_centerline_quartic_self_similarity(Fraction(3, 5))

    assert self_similarity.parameter == Fraction(3, 5)
    assert self_similarity.quartic_value == Fraction(2836, 625)
    assert self_similarity.first_square_term == Fraction(44, 25)
    assert self_similarity.second_square_term == Fraction(6, 5)
    assert (
        self_similarity.quartic_value
        == self_similarity.first_square_term**2
        + self_similarity.second_square_term**2
    )
    assert self_similarity.quadratic_coefficients == (
        Fraction(3, 5),
        Fraction(44, 25),
        Fraction(-3, 5),
    )
    assert self_similarity.quadratic_root_sum == Fraction(-44, 15)
    assert self_similarity.quadratic_root_product == Fraction(-1)
    assert self_similarity.roots_are_negative_reciprocals
    assert self_similarity.direct_positive_descent_warning == "negative-reciprocal-roots"
    assert self_similarity.quadratic_discriminant == self_similarity.quartic_value
    assert not self_similarity.has_rational_lift

    base = sum_ab_centerline_quartic_self_similarity(Fraction(0))

    assert base.quartic_value == 1
    assert base.quadratic_root_sum is None
    assert base.quadratic_root_product is None
    assert not base.roots_are_negative_reciprocals
    assert base.direct_positive_descent_warning == "degenerate-linear-root"
    assert base.has_rational_lift
    assert base.lift_roots == (Fraction(0),)

    quotient = sum_ab_centerline_quartic_negative_reciprocal_quotient(
        Fraction(3, 5)
    )

    assert quotient.parameter == Fraction(3, 5)
    assert quotient.negative_reciprocal == Fraction(-5, 3)
    assert quotient.quotient_variable == Fraction(-16, 15)
    assert quotient.quartic_value == Fraction(2836, 625)
    assert quotient.negative_reciprocal_quartic_value == Fraction(2836, 81)
    assert (
        quotient.negative_reciprocal_quartic_value
        == quotient.quartic_value / quotient.parameter**4
    )
    assert quotient.negative_reciprocal_symmetry_holds
    assert quotient.scaled_quartic_value == Fraction(2836, 225)
    assert quotient.quotient_quadratic_value == Fraction(2836, 225)
    assert quotient.reconstructing_quadratic_coefficients == (
        Fraction(1),
        Fraction(16, 15),
        Fraction(-1),
    )
    assert quotient.reconstruction_discriminant == Fraction(1156, 225)
    assert quotient.reconstruction_discriminant_is_square
    assert quotient.reconstruction_roots == (Fraction(-5, 3), Fraction(3, 5))

    quotient_base = sum_ab_centerline_quartic_negative_reciprocal_quotient(
        Fraction(1)
    )

    assert quotient_base.quotient_variable == 0
    assert quotient_base.reconstruction_discriminant == 4
    assert quotient_base.reconstruction_roots == (Fraction(-1), Fraction(1))

    w_param = sum_ab_centerline_quotient_w_parameterization(Fraction(3, 5))

    assert w_param.parameter == Fraction(3, 5)
    assert w_param.quotient_variable == Fraction(15, 4)
    assert w_param.w_value == Fraction(17, 4)
    assert w_param.w_condition_holds
    assert w_param.remaining_quartic_value == Fraction(164, 25)
    assert w_param.z_square_value == Fraction(1025, 16)
    assert not w_param.z_square_value_is_square
    assert w_param.negative_reciprocal_parameter == Fraction(-5, 3)
    assert w_param.negative_reciprocal_remaining_quartic_value == Fraction(4100, 81)
    assert w_param.negative_reciprocal_symmetry_holds
    assert w_param.second_quotient_variable == Fraction(-16, 15)
    assert w_param.second_quotient_quadratic_value == Fraction(164, 9)
    assert w_param.remaining_quartic_over_parameter_square == Fraction(164, 9)

    pari_diagnostics = sum_ab_centerline_quartic_pari_diagnostics()

    if pari_diagnostics.available:
        assert pari_diagnostics.centerline_model == (0, 18, 0, -68, 56)
        assert pari_diagnostics.centerline_rank_bounds == (0, 0)
        assert pari_diagnostics.centerline_sha2_lower == 0
        assert pari_diagnostics.centerline_torsion_order == 4
        assert pari_diagnostics.centerline_generators == ()
        assert pari_diagnostics.centerline_small_points == (
            (-2, -16),
            (-2, 16),
            (2, 0),
        )
        assert pari_diagnostics.w_parameterized_model == (0, -6, 0, -164, 1240)
        assert pari_diagnostics.w_parameterized_rank_bounds == (0, 0)
        assert pari_diagnostics.w_parameterized_sha2_lower == 0
        assert pari_diagnostics.w_parameterized_torsion_order == 4
        assert pari_diagnostics.w_parameterized_generators == ()
        assert pari_diagnostics.w_parameterized_small_points == (
            (6, -16),
            (6, 16),
            (10, 0),
        )
        assert pari_diagnostics.proof_status == "needs-birational-pullback"


def test_sum_ab_centerline_quartic_integer_equation_tracks_residues() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_centerline_quartic_crt_live_residue_summary,
        sum_ab_centerline_quartic_integer_equation,
        sum_ab_centerline_quartic_live_residue_classes,
        sum_ab_centerline_quartic_primitive_residue_summary,
        sum_ab_centerline_quartic_residue_summary,
    )

    equation = sum_ab_centerline_quartic_integer_equation(3, 5)

    assert equation.u == 3
    assert equation.v == 5
    assert equation.value == 2836
    assert equation.denominator_square == 256
    assert equation.reduced_lambda_value == Fraction(709, 64)
    assert equation.squareclass == 709
    assert not equation.is_square
    assert equation.residue(5) == 1
    assert equation.residue_is_square(5)

    summary = sum_ab_centerline_quartic_residue_summary(5)

    assert summary.modulus == 5
    assert summary.total_classes == 25
    assert summary.square_residue_classes == 21
    assert summary.non_square_residue_classes == 4
    assert summary.zero_residue_classes == 9
    assert summary.square_residues == (0, 1, 4)

    primitive_summary = sum_ab_centerline_quartic_primitive_residue_summary(5)

    assert primitive_summary.modulus == 5
    assert primitive_summary.primitive_classes == 24
    assert primitive_summary.degenerate_denominator_classes == 8
    assert primitive_summary.total_classes == 16
    assert primitive_summary.square_residue_classes == 12
    assert primitive_summary.non_square_residue_classes == 4
    assert primitive_summary.zero_residue_classes == 0
    assert primitive_summary.square_residues == (0, 1, 4)

    composite_summary = sum_ab_centerline_quartic_primitive_residue_summary(143)

    assert composite_summary.modulus == 143
    assert composite_summary.primitive_classes == 20160
    assert composite_summary.degenerate_denominator_classes == 480
    assert composite_summary.total_classes == 19680
    assert composite_summary.square_residue_classes == 3600
    assert composite_summary.non_square_residue_classes == 16080
    assert composite_summary.zero_residue_classes == 0

    live_classes = sum_ab_centerline_quartic_live_residue_classes(5)

    assert [(item.u, item.v, item.residue) for item in live_classes] == [
        (0, 1, 1),
        (0, 2, 1),
        (0, 3, 1),
        (0, 4, 1),
        (1, 0, 1),
        (1, 2, 1),
        (2, 0, 1),
        (2, 4, 1),
        (3, 0, 1),
        (3, 1, 1),
        (4, 0, 1),
        (4, 3, 1),
    ]

    crt_summary = sum_ab_centerline_quartic_crt_live_residue_summary(5, 7)

    assert crt_summary.combined_modulus == 35
    assert crt_summary.left_square_primitive_classes == 20
    assert crt_summary.right_square_primitive_classes == 24
    assert crt_summary.left_live_classes == 12
    assert crt_summary.right_live_classes == 24
    assert crt_summary.left_degenerate_square_classes == 8
    assert crt_summary.right_degenerate_square_classes == 0
    assert crt_summary.live_live_pairs == 288
    assert crt_summary.one_sided_degenerate_pairs == 192
    assert crt_summary.both_degenerate_pairs == 0
    assert crt_summary.merged_live_classes == 480
    assert crt_summary.direct_live_classes == 480
    assert crt_summary.matches_direct

    crt_143_summary = sum_ab_centerline_quartic_crt_live_residue_summary(11, 13)

    assert crt_143_summary.combined_modulus == 143
    assert crt_143_summary.live_live_pairs == 2400
    assert crt_143_summary.one_sided_degenerate_pairs == 1200
    assert crt_143_summary.merged_live_classes == 3600
    assert crt_143_summary.direct_live_classes == 3600
    assert crt_143_summary.matches_direct


def test_sum_ab_product_square_bucket_summary_keeps_residual_guard() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        closure_product_square_conditions,
        sum_ab_product_square_bucket_summary,
        sum_ab_product_square_residuals_from_grid,
    )

    residual_guard = closure_product_square_conditions(
        Fraction(535, 161),
        Fraction(696, 161),
        Fraction(364, 161),
        REL_SUM_AB,
    )
    summary = sum_ab_product_square_bucket_summary(
        lambda_ratios=tuple(Fraction(value) for value in range(1, 16)),
        max_denominator=20,
        extra_conditions=(residual_guard,),
    )

    assert summary.bucket_counts == {
        "centerline": 230,
        "reciprocal": 40,
        "residual": 1,
    }
    assert summary.true_member_counts == {}
    assert summary.examples_by_bucket["residual"] == residual_guard
    assert summary.squareclass_pair_counts_by_bucket["centerline"][(2, 2)] == 20
    assert summary.squareclass_pair_counts_by_bucket["reciprocal"][(2, 2)] == 40
    assert summary.squareclass_pair_counts_by_bucket["residual"][(29, 29)] == 1

    residuals = sum_ab_product_square_residuals_from_grid(
        lambda_ratios=(Fraction(535, 161),),
        max_denominator=23,
    )

    assert residual_guard in residuals
    assert all(condition.product_square_bucket == "residual" for condition in residuals)


def test_sum_ab_product_square_residuals_from_root_grid_finds_known_residual() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_product_square_residuals_from_root_grid,
    )

    residuals = sum_ab_product_square_residuals_from_root_grid(
        max_numerator=26,
        max_denominator=23,
    )

    known = [
        condition
        for condition in residuals
        if condition.lambda_ratio == Fraction(535, 161)
        and condition.roots == (Fraction(14, 23), Fraction(26, 7))
    ]

    assert len(known) == 1
    assert known[0].product_square_bucket == "residual"
    assert known[0].member_squareclass_pair == (29, 29)
    assert not known[0].true_member_pair
    assert all(condition.product_square_bucket == "residual" for condition in residuals)


def test_sum_ab_root_grid_residual_summary_counts_squareclass_pairs() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_root_grid_residual_summary,
    )

    summary = sum_ab_root_grid_residual_summary(
        max_numerator=26,
        max_denominator=23,
    )

    assert summary.bucket_counts == {"residual": 1}
    assert summary.true_member_counts == {}
    assert summary.squareclass_pair_counts_by_bucket == {"residual": {(29, 29): 1}}
    assert summary.examples_by_bucket["residual"].lambda_ratio == Fraction(535, 161)
    assert summary.examples_by_bucket["residual"].roots == (
        Fraction(14, 23),
        Fraction(26, 7),
    )


def test_sum_ab_root_grid_residual_watchlist_flags_true_or_trivial_pairs() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        closure_product_square_conditions,
        sum_ab_root_grid_residual_watchlist,
    )

    assert (
        sum_ab_root_grid_residual_watchlist(
            max_numerator=26,
            max_denominator=23,
        )
        == ()
    )

    true_condition = closure_product_square_conditions(
        Fraction(1),
        Fraction(25, 12),
        Fraction(1),
        REL_SUM_AB,
    )

    assert sum_ab_root_grid_residual_watchlist(
        max_numerator=1,
        max_denominator=1,
        extra_conditions=(true_condition,),
    ) == (true_condition,)


def test_sum_ab_residual_squareclass_equations_explain_product_square() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_residual_squareclass_equations,
    )

    equations = sum_ab_residual_squareclass_equations(
        lambda_ratio=Fraction(535, 161),
        r=Fraction(14, 23),
        s=Fraction(26, 7),
    )

    assert equations.closes_sum_ab
    assert not equations.reciprocal_pair
    assert equations.unit_values == (
        Fraction(725, 529),
        Fraction(725, 49),
    )
    assert equations.lambda_values == (
        Fraction(295829, 25921),
        Fraction(643829, 25921),
    )
    assert equations.unit_squareclasses == (29, 29)
    assert equations.lambda_squareclasses == (29, 29)
    assert equations.unit_product_is_square
    assert equations.lambda_product_is_square
    assert not equations.all_terms_are_squares
    assert not equations.squareclasses_all_trivial

    true_equations = sum_ab_residual_squareclass_equations(
        lambda_ratio=Fraction(1),
        r=Fraction(3, 4),
        s=Fraction(4, 3),
    )

    assert true_equations.reciprocal_pair
    assert true_equations.unit_squareclasses == (1, 1)
    assert true_equations.lambda_squareclasses == (1, 1)
    assert true_equations.all_terms_are_squares
    assert true_equations.squareclasses_all_trivial


def test_sum_ab_true_closure_relation_classifies_proof_branches() -> None:
    from rational_distance.concordant.rational_ratio import sum_ab_true_closure_relation

    reciprocal = sum_ab_true_closure_relation(
        lambda_ratio=Fraction(7),
        r=Fraction(1),
        s=Fraction(7),
    )

    assert reciprocal.closes_sum_ab
    assert not reciprocal.both_true_members
    assert reciprocal.reciprocal_pair
    assert not reciprocal.centerline
    assert reciprocal.branch == "false-reciprocal"

    true_nonclosure = sum_ab_true_closure_relation(
        lambda_ratio=Fraction(1),
        r=Fraction(3, 4),
        s=Fraction(4, 3),
    )

    assert not true_nonclosure.closes_sum_ab
    assert true_nonclosure.both_true_members
    assert true_nonclosure.reciprocal_pair
    assert true_nonclosure.branch == "not-sum-ab"

    residual = sum_ab_true_closure_relation(
        lambda_ratio=Fraction(535, 161),
        r=Fraction(14, 23),
        s=Fraction(26, 7),
    )

    assert residual.closes_sum_ab
    assert not residual.both_true_members
    assert not residual.reciprocal_pair
    assert residual.branch == "false-residual"

    centerline = sum_ab_true_closure_relation(
        lambda_ratio=Fraction(3),
        r=Fraction(2),
        s=Fraction(2),
    )

    assert centerline.closes_sum_ab
    assert centerline.centerline
    assert not centerline.both_true_members
    assert centerline.branch == "false-centerline"


def test_scan_sum_ab_true_closure_relations_monitors_nonreciprocal_branch() -> None:
    from rational_distance.concordant.rational_ratio import (
        scan_sum_ab_true_closure_relations,
    )

    relations = scan_sum_ab_true_closure_relations(
        lambda_ratios=(Fraction(7),),
        max_numerator=7,
        max_denominator=1,
    )

    assert [(item.r, item.s, item.branch) for item in relations] == [
        (Fraction(4), Fraction(4), "false-centerline"),
        (Fraction(1), Fraction(7), "false-reciprocal"),
        (Fraction(2), Fraction(6), "false-residual"),
        (Fraction(3), Fraction(5), "false-residual"),
    ]
    assert not any(item.branch == "true-nonreciprocal" for item in relations)

    true_only = scan_sum_ab_true_closure_relations(
        lambda_ratios=(Fraction(1),),
        max_numerator=4,
        max_denominator=4,
        branches=("true-nonreciprocal",),
    )

    assert true_only == ()


def test_full_plane_true_closure_relation_handles_difference_branch() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_DIFF_AB,
        full_plane_true_closure_relation,
    )

    relation = full_plane_true_closure_relation(
        lambda_ratio=Fraction(7),
        r=Fraction(2),
        s=Fraction(10),
        relation=REL_DIFF_AB,
    )

    assert relation.target == Fraction(8)
    assert relation.closes_relation
    assert not relation.closes_sum_ab
    assert not relation.both_true_members
    assert not relation.reciprocal_pair
    assert relation.branch == "false-residual"


def test_scan_full_plane_true_closure_relations_is_not_sum_only() -> None:
    from rational_distance.concordant.rational_ratio import (
        scan_full_plane_true_closure_relations,
    )

    relations = scan_full_plane_true_closure_relations(
        lambda_ratios=(Fraction(7),),
        max_numerator=10,
        max_denominator=1,
        include_centerline=False,
    )

    assert ("sum=A+B", Fraction(2), Fraction(6), "false-residual") in {
        (item.relation, item.r, item.s, item.branch) for item in relations
    }
    assert ("diff=A+B", Fraction(2), Fraction(10), "false-residual") in {
        (item.relation, item.r, item.s, item.branch) for item in relations
    }
    assert not any(item.branch == "true-nonreciprocal" for item in relations)


def test_scan_full_plane_true_closure_relations_covers_abs_difference_targets() -> None:
    from rational_distance.concordant.rational_ratio import (
        scan_full_plane_true_closure_relations,
    )

    relations = scan_full_plane_true_closure_relations(
        lambda_ratios=(Fraction(6),),
        max_numerator=6,
        max_denominator=1,
        include_centerline=False,
    )

    relation_keys = {
        (item.relation, item.r, item.s, item.branch) for item in relations
    }

    assert ("sum=|A-B|", Fraction(2), Fraction(3), "false-reciprocal") in relation_keys
    assert ("diff=|A-B|", Fraction(1), Fraction(6), "false-reciprocal") in relation_keys


def test_scan_full_plane_true_closure_relations_can_focus_on_danger_branch() -> None:
    from rational_distance.concordant.rational_ratio import (
        scan_full_plane_true_closure_relations,
    )

    relations = scan_full_plane_true_closure_relations(
        lambda_ratios=(Fraction(1), Fraction(7)),
        max_numerator=10,
        max_denominator=10,
        branches=("true-nonreciprocal",),
    )

    assert relations == ()


def test_full_plane_closure_product_ledger_links_classification_to_product_terms() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_DIFF_AB,
        full_plane_closure_product_ledger,
    )

    ledger = full_plane_closure_product_ledger(
        lambda_ratio=Fraction(7),
        r=Fraction(2),
        s=Fraction(10),
        relation=REL_DIFF_AB,
    )

    assert ledger.classification.closes_relation
    assert ledger.target == Fraction(8)
    assert ledger.product == Fraction(20)
    assert ledger.product_equals_lambda is False
    assert ledger.danger_branch is False
    assert ledger.conditions.discriminant == Fraction(144)
    assert ledger.conditions.roots == (Fraction(2), Fraction(10))
    assert ledger.conditions.true_member_pair is False


def test_full_plane_closure_product_ledger_rejects_nonclosure_pairs() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        full_plane_closure_product_ledger,
    )

    try:
        full_plane_closure_product_ledger(
            lambda_ratio=Fraction(1),
            r=Fraction(3, 4),
            s=Fraction(4, 3),
            relation=REL_SUM_AB,
        )
    except ValueError as error:
        assert "requires a pair that does close" in str(error)
    else:
        raise AssertionError("expected nonclosure pair to be rejected")


def test_full_plane_closure_product_summary_counts_relation_and_bucket() -> None:
    from rational_distance.concordant.rational_ratio import (
        full_plane_closure_product_summary,
    )

    summary = full_plane_closure_product_summary(
        lambda_ratios=(Fraction(7),),
        max_numerator=10,
        max_denominator=1,
        include_centerline=False,
    )

    assert summary.total_relations == 11
    assert summary.branch_counts == {"false-reciprocal": 2, "false-residual": 9}
    assert summary.relation_branch_counts[("sum=A+B", "false-residual")] == 2
    assert summary.relation_branch_counts[("diff=A+B", "false-residual")] == 2
    assert summary.product_bucket_counts[("sum=A+B", "reciprocal")] == 1
    assert summary.product_bucket_counts[("sum=|A-B|", "none")] == 2
    assert summary.danger_count == 0


def test_scan_sum_ab_slope_pairs_finds_no_small_true_hits() -> None:
    from rational_distance.concordant.rational_ratio import scan_sum_ab_slope_pairs

    slopes = (Fraction(3, 4), Fraction(4, 3), Fraction(5, 12), Fraction(12, 5))

    assert scan_sum_ab_slope_pairs(slopes, include_false_members=False) == ()


def test_pythagorean_leg_ratios_generate_bounded_slope_pool() -> None:
    from rational_distance.concordant.rational_ratio import (
        positive_rational_ratios,
        pythagorean_leg_ratios,
    )

    assert positive_rational_ratios(3, 3) == (
        Fraction(1, 3),
        Fraction(1, 2),
        Fraction(2, 3),
        Fraction(1),
        Fraction(3, 2),
        Fraction(2),
        Fraction(3),
    )

    assert pythagorean_leg_ratios(3) == (
        Fraction(3, 4),
        Fraction(4, 3),
        Fraction(5, 12),
        Fraction(12, 5),
    )


def test_leg_ratio_squareclass_explains_pythagorean_failure() -> None:
    from rational_distance.concordant.rational_ratio import leg_ratio_squareclass

    passing = leg_ratio_squareclass(Fraction(3, 4))
    failing = leg_ratio_squareclass(Fraction(9, 13))

    assert passing.is_square
    assert passing.squarefree_part == 1
    assert passing.squareclass_primes == ()

    assert not failing.is_square
    assert failing.value == Fraction(250, 169)
    assert failing.squarefree_part == 10
    assert failing.squareclass_primes == (2, 5)
    assert failing.three_mod_four_primes == ()


def test_sum_ab_slope_obstruction_identifies_scaled_leg_failures() -> None:
    from rational_distance.concordant.rational_ratio import sum_ab_slope_obstruction

    obstruction = sum_ab_slope_obstruction(Fraction(3, 4), Fraction(4, 3))

    assert obstruction is not None
    assert obstruction.lambda_ratio == Fraction(12, 13)
    assert obstruction.failed_terms == ("r1", "r2")
    assert obstruction.term_squareclasses == (
        ("slope1", 1),
        ("slope2", 1),
        ("r1", 10),
        ("r2", 17),
    )


def test_sum_ab_slope_obstruction_counts_three_pass_near_miss() -> None:
    from rational_distance.concordant.rational_ratio import sum_ab_slope_obstruction

    obstruction = sum_ab_slope_obstruction(Fraction(15, 8), Fraction(7, 24))

    assert obstruction is not None
    assert obstruction.lambda_ratio == Fraction(6, 7)
    assert obstruction.r1 == Fraction(45, 28)
    assert obstruction.r2 == Fraction(1, 4)
    assert obstruction.failed_terms == ("r2",)
    assert obstruction.passed_terms == ("slope1", "slope2", "r1")
    assert obstruction.pass_count == 3
    assert obstruction.failure_count == 1
    assert obstruction.three_pass_near_miss


def test_scan_sum_ab_slope_obstructions_filters_three_pass_near_misses() -> None:
    from rational_distance.concordant.rational_ratio import scan_sum_ab_slope_obstructions

    slopes = (Fraction(3, 4), Fraction(4, 3), Fraction(15, 8), Fraction(7, 24))

    near_misses = scan_sum_ab_slope_obstructions(slopes, pass_count=3)

    assert len(near_misses) == 1
    assert near_misses[0].slope1 == Fraction(7, 24)
    assert near_misses[0].slope2 == Fraction(15, 8)
    assert near_misses[0].failed_terms == ("r1",)
    assert near_misses[0].passed_terms == ("slope1", "slope2", "r2")


def test_sum_ab_three_pass_mobius_model_reconstructs_missing_term() -> None:
    from rational_distance.concordant.rational_ratio import sum_ab_three_pass_mobius_model

    model = sum_ab_three_pass_mobius_model(
        slope=Fraction(15, 8),
        scaled_term=Fraction(45, 28),
    )

    assert model.lambda_ratio == Fraction(6, 7)
    assert model.slope == Fraction(15, 8)
    assert model.other_slope == Fraction(7, 24)
    assert model.scaled_term == Fraction(45, 28)
    assert model.failed_scaled_term == Fraction(1, 4)
    assert model.closes_sum_ab
    assert model.three_terms_are_pythagorean
    assert not model.failed_term_is_pythagorean
    assert model.failed_squareclass == 17


def test_sum_ab_mobius_model_from_euclid_params_exposes_square_equations() -> None:
    from rational_distance.concordant.rational_ratio import (
        PythagoreanLegParam,
        sum_ab_three_pass_mobius_model_from_params,
    )

    model = sum_ab_three_pass_mobius_model_from_params(
        slope=PythagoreanLegParam(m=4, n=1, orientation="odd"),
        scaled_term=PythagoreanLegParam(m=7, n=2, orientation="odd"),
    )

    assert model.mobius.slope == Fraction(15, 8)
    assert model.mobius.scaled_term == Fraction(45, 28)
    assert model.mobius.other_slope == Fraction(7, 24)
    assert model.mobius.failed_scaled_term == Fraction(1, 4)
    assert model.other_slope_square_equation == (
        Fraction(7, 24) * Fraction(7, 24) + 1,
        Fraction(25, 24) * Fraction(25, 24),
    )
    assert model.failed_square_equation == (
        Fraction(1, 4) * Fraction(1, 4) + 1,
        None,
    )
    assert model.other_slope_integer_equation == (7, 24, 25)
    assert model.failed_integer_equation == (1, 4, None)
    assert model.other_slope_polynomial_terms == (105, 360)
    assert model.failed_polynomial_terms == (105, 420)
    assert model.other_slope_polynomial_equation == (105, 360, 375)
    assert model.failed_polynomial_equation == (105, 420, None)
    assert model.failed_squareclass == 17


def test_sum_ab_euclid_orientation_equations_expand_four_cases() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_euclid_orientation_equations,
    )

    cases = sum_ab_euclid_orientation_equations(
        slope_m=4,
        slope_n=1,
        scaled_term_m=7,
        scaled_term_n=2,
    )

    assert [
        (
            case.slope_orientation,
            case.scaled_term_orientation,
            case.slope_terms,
            case.scaled_term_terms,
            case.other_slope_polynomial_equation,
            case.failed_polynomial_equation,
        )
        for case in cases
    ] == [
        ("odd", "odd", (15, 8), (45, 28), (105, 360, 375), (105, 420, None)),
        ("odd", "even", (15, 8), (28, 45), (479, 224, None), (479, 675, None)),
        ("even", "odd", (8, 15), (45, 28), (539, 675, None), (539, 224, None)),
        ("even", "even", (8, 15), (28, 45), (556, 420, None), (556, 360, None)),
    ]


def test_sum_ab_euclid_residue_summaries_count_square_residue_obstructions() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_euclid_residue_summaries,
    )

    summaries = sum_ab_euclid_residue_summaries(modulus=8)

    assert [
        (
            summary.slope_orientation,
            summary.scaled_term_orientation,
            summary.total_classes,
            summary.other_square_classes,
            summary.failed_square_classes,
            summary.both_square_classes,
            summary.other_only_classes,
            summary.failed_only_classes,
            summary.neither_square_classes,
            summary.other_square_forces_failed_square,
        )
        for summary in summaries
    ] == [
        ("odd", "odd", 4096, 4096, 4096, 4096, 0, 0, 0, True),
        ("odd", "even", 4096, 4096, 3072, 3072, 1024, 0, 0, False),
        ("even", "odd", 4096, 3072, 4096, 3072, 0, 1024, 0, True),
        ("even", "even", 4096, 4096, 4096, 4096, 0, 0, 0, True),
    ]


def test_sum_ab_euclid_conditional_residue_summaries_apply_primitive_filters() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_euclid_conditional_residue_summaries,
    )

    summaries = sum_ab_euclid_conditional_residue_summaries(modulus=24)

    assert [
        (
            summary.slope_orientation,
            summary.scaled_term_orientation,
            summary.total_classes,
            summary.other_square_classes,
            summary.failed_square_classes,
            summary.both_square_classes,
            summary.other_only_classes,
            summary.failed_only_classes,
            summary.neither_square_classes,
        )
        for summary in summaries
    ] == [
        ("odd", "odd", 24576, 16384, 16384, 8192, 8192, 8192, 0),
        ("odd", "even", 16384, 0, 0, 0, 0, 0, 16384),
        ("even", "odd", 16384, 0, 0, 0, 0, 0, 16384),
        ("even", "even", 24576, 16384, 16384, 8192, 8192, 8192, 0),
    ]


def test_sum_ab_same_orientation_shared_leg_terms_expose_square_difference() -> None:
    from rational_distance.concordant.rational_ratio import (
        PythagoreanLegParam,
        sum_ab_same_orientation_shared_leg_terms,
    )

    terms = sum_ab_same_orientation_shared_leg_terms(
        slope=PythagoreanLegParam(m=4, n=1, orientation="odd"),
        scaled_term=PythagoreanLegParam(m=7, n=2, orientation="odd"),
    )

    assert terms.orientation == "odd"
    assert terms.slope_terms == (15, 8)
    assert terms.scaled_term_terms == (45, 28)
    assert terms.shared_numerator == 105
    assert terms.other_denominator == 360
    assert terms.failed_denominator == 420
    assert terms.other_square_equation == (105, 360, 375)
    assert terms.failed_square_equation == (105, 420, None)
    assert terms.square_difference == 105 * 105 + 360 * 360 - (105 * 105 + 420 * 420)
    assert terms.denominator_square_difference == 360 * 360 - 420 * 420
    assert terms.other_hypotenuse_factor_pair == (15, 735)
    assert terms.failed_hypotenuse_factor_pair is None
    assert terms.other_factor_pair_gcd == 15
    assert terms.other_reduced_factor_pair == (1, 49)
    assert terms.other_reduced_factor_pair_gcd == 1
    assert terms.other_reduced_factor_pair_square_roots == (1, 7)
    assert terms.other_reduced_factor_pair_is_square_pair
    assert terms.other_factor_pair_parameterization == (15, 1, 7)
    assert terms.other_parameterized_shared_numerator == 105
    assert terms.other_parameterized_denominator == 360
    assert terms.other_parameterized_hypotenuse == 375
    assert terms.failed_factor_pair_gcd is None
    assert terms.failed_reduced_factor_pair is None
    assert terms.failed_reduced_factor_pair_gcd is None
    assert terms.failed_reduced_factor_pair_square_roots is None
    assert not terms.failed_reduced_factor_pair_is_square_pair
    assert terms.failed_factor_pair_parameterization is None


def test_sum_ab_same_orientation_shared_leg_terms_reject_mixed_orientation() -> None:
    import pytest

    from rational_distance.concordant.rational_ratio import (
        PythagoreanLegParam,
        sum_ab_same_orientation_shared_leg_terms,
    )

    with pytest.raises(ValueError, match="matching orientations"):
        sum_ab_same_orientation_shared_leg_terms(
            slope=PythagoreanLegParam(m=4, n=1, orientation="odd"),
            scaled_term=PythagoreanLegParam(m=7, n=2, orientation="even"),
        )


def test_sum_ab_same_orientation_denominator_factorization_exposes_nu_minus_mv() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_same_orientation_denominator_factorization,
    )

    factorization = sum_ab_same_orientation_denominator_factorization(
        slope_m=4,
        slope_n=1,
        scaled_term_m=7,
        scaled_term_n=2,
        orientation="odd",
    )

    assert factorization.other_denominator == 360
    assert factorization.failed_denominator == 420
    assert factorization.denominator_difference == -60
    assert factorization.denominator_sum == 780
    assert factorization.nu_minus_mv == -1
    assert factorization.difference_factorization == (2, 30, -1)
    assert factorization.sum_factorization == (2, 26, 15)

    even_factorization = sum_ab_same_orientation_denominator_factorization(
        slope_m=4,
        slope_n=1,
        scaled_term_m=7,
        scaled_term_n=2,
        orientation="even",
    )

    assert even_factorization.other_denominator == 420
    assert even_factorization.failed_denominator == 360
    assert even_factorization.denominator_difference == 60
    assert even_factorization.nu_minus_mv == -1
    assert even_factorization.difference_factorization == (-2, 30, -1)
    assert even_factorization.sum_factorization == (2, 26, 15)


def test_sum_ab_same_orientation_cross_gcd_terms_expose_denominator_source() -> None:
    from fractions import Fraction

    from rational_distance.concordant.rational_ratio import (
        PythagoreanLegParam,
        sum_ab_same_orientation_cross_gcd_terms,
    )

    terms = sum_ab_same_orientation_cross_gcd_terms(
        slope=PythagoreanLegParam(m=4, n=1, orientation="odd"),
        scaled_term=PythagoreanLegParam(m=7, n=2, orientation="odd"),
    )

    assert terms.orientation == "odd"
    assert terms.slope_terms == (15, 8)
    assert terms.scaled_term_terms == (45, 28)
    assert terms.other_denominator == 360
    assert terms.failed_denominator == 420
    assert terms.gcd_a_b == 1
    assert terms.gcd_c_d == 1
    assert terms.gcd_a_c == 15
    assert terms.gcd_a_d == 1
    assert terms.gcd_b_c == 1
    assert terms.gcd_b_d == 4
    assert terms.gcd_p_q == 60
    assert terms.primitive_cross_gcd_product == 60
    assert terms.primitive_cross_gcd_identity_holds
    assert terms.denominator_difference == -60
    assert terms.denominator_sum == 780
    assert terms.denominator_difference_over_gcd == -1
    assert terms.denominator_sum_over_gcd == 13
    assert terms.normalized_denominator_pair == (6, 7)
    assert terms.difference_factorization_over_gcd == (
        Fraction(1, 30),
        30,
        -1,
    )
    assert terms.sum_factorization_over_gcd == (Fraction(1, 30), 26, 15)

    even_terms = sum_ab_same_orientation_cross_gcd_terms(
        slope=PythagoreanLegParam(m=4, n=1, orientation="even"),
        scaled_term=PythagoreanLegParam(m=7, n=2, orientation="even"),
    )

    assert even_terms.other_denominator == 420
    assert even_terms.failed_denominator == 360
    assert even_terms.gcd_a_c == 4
    assert even_terms.gcd_b_d == 15
    assert even_terms.gcd_p_q == 60
    assert even_terms.primitive_cross_gcd_product == 60
    assert even_terms.denominator_difference_over_gcd == 1
    assert even_terms.denominator_sum_over_gcd == 13
    assert even_terms.normalized_denominator_pair == (7, 6)
    assert even_terms.difference_factorization_over_gcd == (
        Fraction(-1, 30),
        30,
        -1,
    )
    assert even_terms.sum_factorization_over_gcd == (Fraction(1, 30), 26, 15)


def test_sum_ab_same_orientation_normalized_near_miss_summary_counts_patterns() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_same_orientation_normalized_near_miss_summary,
    )

    summary = sum_ab_same_orientation_normalized_near_miss_summary(max_m=8)

    assert summary.max_m == 8
    assert summary.total_near_misses == 6
    assert summary.abs_difference_over_gcd_counts[1] == 2
    assert summary.abs_difference_over_gcd_counts[17] == 2
    assert summary.abs_difference_over_gcd_counts[38] == 2
    assert summary.failing_squareclass_counts[17] == 4
    assert summary.failing_squareclass_counts[24634] == 2
    assert summary.normalized_pair_counts[((6, 7), "odd")] == 1
    assert summary.normalized_pair_counts[((7, 6), "odd")] == 1
    assert len(summary.examples_by_failing_squareclass[17]) == 4
    assert {
        example.denominator_difference_over_gcd
        for example in summary.examples_by_failing_squareclass[17]
    } == {-38, -1, 1, 38}
    assert summary.canonical_triples_by_failing_squareclass[17] == (
        (7, 24, 28),
        (28, 7, 45),
    )
    assert summary.family_edges_by_failing_squareclass[17][0].source == (7, 24, 28)
    assert summary.family_edges_by_failing_squareclass[17][0].target == (28, 7, 45)
    assert summary.family_edges_by_failing_squareclass[17][
        0
    ].target_uses_source_failed_leg
    assert summary.family_edges_by_failing_squareclass[17][0].target_uses_source_shared_leg
    assert summary.family_edges_by_failing_squareclass[17][0].source_max == 28
    assert summary.family_edges_by_failing_squareclass[17][0].target_max == 45
    assert summary.family_edges_by_failing_squareclass[17][0].target_max_delta == 17
    assert summary.family_edges_by_failing_squareclass[17][0].target_n_delta == 21
    assert not summary.family_edges_by_failing_squareclass[17][0].decreases_n
    assert not summary.family_edges_by_failing_squareclass[17][0].decreases_max
    assert summary.family_edges_by_failing_squareclass[17][1].target_max_delta == -17
    assert summary.family_edges_by_failing_squareclass[17][1].target_n_delta == -21
    assert summary.family_edges_by_failing_squareclass[17][1].decreases_n
    assert summary.family_edges_by_failing_squareclass[17][1].decreases_max
    assert summary.n_descending_edge_count == 1
    assert summary.n_descending_continuation_count == 0
    assert summary.examples_by_abs_difference[1][0].slope_params == (4, 1)
    assert summary.examples_by_abs_difference[1][0].scaled_term_params == (7, 2)
    assert summary.examples_by_abs_difference[1][0].orientation == "odd"
    assert summary.examples_by_abs_difference[1][0].shared_numerator == 105
    assert summary.examples_by_abs_difference[1][0].other_denominator == 360
    assert summary.examples_by_abs_difference[1][0].failed_denominator == 420
    assert summary.examples_by_abs_difference[1][0].gcd_n_p_q == 15
    assert summary.examples_by_abs_difference[1][0].normalized_shared_leg_triple == (
        7,
        24,
        28,
    )
    assert summary.examples_by_abs_difference[1][0].normalized_other_squareclass == 1
    assert summary.examples_by_abs_difference[1][0].normalized_failed_squareclass == 17
    assert summary.examples_by_abs_difference[1][0].normalized_denominator_pair == (
        6,
        7,
    )
    assert summary.examples_by_abs_difference[1][0].other_square_passes
    assert not summary.examples_by_abs_difference[1][0].failed_square_passes
    assert summary.examples_by_abs_difference[1][1].normalized_denominator_pair == (
        7,
        6,
    )
    assert summary.examples_by_abs_difference[1][1].normalized_shared_leg_triple == (
        7,
        28,
        24,
    )
    assert summary.examples_by_abs_difference[1][1].normalized_other_squareclass == 17
    assert summary.examples_by_abs_difference[1][1].normalized_failed_squareclass == 1
    assert not summary.examples_by_abs_difference[1][1].other_square_passes
    assert summary.examples_by_abs_difference[1][1].failed_square_passes


def test_scan_sum_ab_slope_obstructions_reuses_squareclass_diagnostics(monkeypatch) -> None:
    import rational_distance.concordant.rational_ratio as rr

    calls: dict[Fraction, int] = {}
    original = rr.leg_ratio_squareclass

    def tracking_squareclass(ratio: Fraction):
        calls[ratio] = calls.get(ratio, 0) + 1
        return original(ratio)

    monkeypatch.setattr(rr, "leg_ratio_squareclass", tracking_squareclass)

    slopes = (Fraction(3, 4), Fraction(4, 3), Fraction(5, 12), Fraction(12, 5))

    obstructions = rr.scan_sum_ab_slope_obstructions(slopes)

    assert len(obstructions) == 9
    assert calls
    assert max(calls.values()) == 1


def test_sum_ab_ratio_shadow_key_identifies_reciprocal_near_misses() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_ratio_shadow_key,
        sum_ab_slope_obstruction,
    )

    first = sum_ab_slope_obstruction(Fraction(7, 24), Fraction(15, 8))
    reciprocal_shadow = sum_ab_slope_obstruction(Fraction(8, 15), Fraction(28, 45))

    assert first is not None
    assert reciprocal_shadow is not None
    assert first.three_pass_near_miss
    assert reciprocal_shadow.three_pass_near_miss
    assert sum_ab_ratio_shadow_key(first) == sum_ab_ratio_shadow_key(reciprocal_shadow)


def test_group_sum_ab_ratio_shadow_orbits_merges_reciprocal_pair() -> None:
    from rational_distance.concordant.rational_ratio import (
        group_sum_ab_ratio_shadow_orbits,
        sum_ab_slope_obstruction,
    )

    first = sum_ab_slope_obstruction(Fraction(7, 24), Fraction(15, 8))
    reciprocal_shadow = sum_ab_slope_obstruction(Fraction(8, 15), Fraction(28, 45))
    unrelated = sum_ab_slope_obstruction(Fraction(3, 4), Fraction(4, 3))

    assert first is not None
    assert reciprocal_shadow is not None
    assert unrelated is not None

    orbits = group_sum_ab_ratio_shadow_orbits((first, reciprocal_shadow, unrelated))

    assert [orbit.member_count for orbit in orbits] == [1, 2]
    assert [orbit.failed_squareclasses for orbit in orbits] == [(10, 17), (17,)]


def test_square_rectangle_terms_match_sum_branch_distances() -> None:
    from rational_distance.concordant.rational_ratio import square_rectangle_terms

    terms = square_rectangle_terms(lambda_ratio=Fraction(7), target=Fraction(8), mover=Fraction(1))

    assert (terms.x, terms.y, terms.z, terms.w) == (
        Fraction(53),
        Fraction(85),
        Fraction(245),
        Fraction(277),
    )
    assert terms.y - terms.x == Fraction(32)
    assert terms.w - terms.z == Fraction(32)
    assert terms.z - terms.x == Fraction(192)
    assert terms.w - terms.y == Fraction(192)
    assert terms.x + terms.w == terms.y + terms.z


def test_reciprocal_orbit_dangerous_discriminant_roots_are_not_members() -> None:
    from rational_distance.concordant.rational_ratio import (
        full_plane_reciprocal_obstruction,
        reciprocal_closure_roots,
    )

    sum_diff_roots = reciprocal_closure_roots(Fraction(6), "sum=|A-B|")
    diff_ab_roots = reciprocal_closure_roots(Fraction(3, 2), "diff=A+B")

    assert [(root.r, root.true_member) for root in sum_diff_roots] == [
        (Fraction(2), False),
        (Fraction(3), False),
    ]
    assert [(root.r, root.true_member) for root in diff_ab_roots] == [
        (Fraction(3), False),
    ]

    summary = full_plane_reciprocal_obstruction(Fraction(6))

    assert summary.all_branches_closed
    assert summary.by_relation["sum=A+B"].roots == (Fraction(1), Fraction(6))
    assert summary.by_relation["sum=|A-B|"].roots == (Fraction(2), Fraction(3))
    assert summary.by_relation["diff=A+B"].roots == ()
    assert summary.by_relation["diff=|A-B|"].roots == (Fraction(1), Fraction(6))
    assert all(row.true_roots == () for row in summary.by_relation.values())


def test_reciprocal_closure_squareclass_ledger_explains_failed_roots() -> None:
    from rational_distance.concordant.rational_ratio import (
        reciprocal_closure_squareclass_ledger,
    )

    ledger = reciprocal_closure_squareclass_ledger(Fraction(6), "sum=|A-B|")

    assert [(row.r, row.unit_squareclass, row.lambda_squareclass) for row in ledger] == [
        (Fraction(2), 5, 10),
        (Fraction(3), 10, 5),
    ]
    assert all(not row.true_member for row in ledger)


def test_reciprocal_closure_discriminant_ledger_explains_failed_roots() -> None:
    from rational_distance.concordant.rational_ratio import (
        reciprocal_closure_discriminant_ledger,
    )

    ledger = reciprocal_closure_discriminant_ledger(Fraction(6), "sum=|A-B|")

    assert ledger.target == Fraction(5)
    assert ledger.discriminant == Fraction(1)
    assert ledger.discriminant_is_square
    assert ledger.discriminant_squareclass == 1
    assert [(row.r, row.unit_squareclass, row.lambda_squareclass) for row in ledger.roots] == [
        (Fraction(2), 5, 10),
        (Fraction(3), 10, 5),
    ]
    assert ledger.true_roots == ()
    assert ledger.branch_closed


def test_reciprocal_closure_discriminant_ledger_handles_single_positive_root() -> None:
    from rational_distance.concordant.rational_ratio import (
        reciprocal_closure_discriminant_ledger,
    )

    ledger = reciprocal_closure_discriminant_ledger(Fraction(3, 2), "diff=A+B")

    assert ledger.target == Fraction(5, 2)
    assert ledger.discriminant == Fraction(49, 4)
    assert ledger.discriminant_is_square
    assert ledger.discriminant_squareclass == 1
    assert [(row.r, row.unit_squareclass, row.lambda_squareclass) for row in ledger.roots] == [
        (Fraction(3), 10, 5),
    ]
    assert ledger.true_roots == ()
    assert ledger.branch_closed
