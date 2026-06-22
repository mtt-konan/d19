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


def test_closure_member_product_square_ledger_separates_weak_and_true_squares() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        closure_member_product_square_ledger,
    )

    weak = closure_member_product_square_ledger(
        Fraction(535, 161),
        Fraction(696, 161),
        Fraction(364, 161),
        REL_SUM_AB,
    )

    assert weak.roots == (Fraction(14, 23), Fraction(26, 7))
    assert weak.unit_values == (Fraction(725, 529), Fraction(725, 49))
    assert weak.lambda_values == (
        Fraction(295829, 25921),
        Fraction(643829, 25921),
    )
    assert weak.unit_product == weak.identity_terms.a_term
    assert weak.lambda_product == weak.identity_terms.b_term
    assert weak.unit_product_is_square
    assert weak.lambda_product_is_square
    assert weak.member_squareclasses == (29, 29, 29, 29)
    assert weak.member_squareclass_pair == (29, 29)
    assert not weak.member_squareclasses_all_trivial
    assert not weak.true_member_pair
    assert weak.identity_terms.b_minus_lambda_sq_a == (
        (weak.lambda_ratio * weak.lambda_ratio - 1)
        * (weak.lambda_ratio * weak.lambda_ratio - weak.product * weak.product)
    )

    true = closure_member_product_square_ledger(
        Fraction(1),
        Fraction(25, 12),
        Fraction(1),
        REL_SUM_AB,
    )

    assert true.roots == (Fraction(3, 4), Fraction(4, 3))
    assert true.member_squareclasses == (1, 1, 1, 1)
    assert true.member_squareclass_pair == (1, 1)
    assert true.member_squareclasses_all_trivial
    assert true.true_member_pair


def test_closure_member_prime_valuation_ledger_tracks_squareclass_escape() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        closure_member_prime_valuation_ledger,
    )

    weak = closure_member_prime_valuation_ledger(
        Fraction(535, 161),
        Fraction(696, 161),
        Fraction(364, 161),
        REL_SUM_AB,
    )

    assert weak.member_squareclass_primes == (29,)
    assert weak.three_mod_four_member_squareclass_primes == ()
    assert weak.rows_by_prime[29].member_valuations == (1, 1, 1, 1)
    assert weak.rows_by_prime[29].identity_valuations == (2, 2, 2, 1, 1)
    assert weak.rows_by_prime[29].all_member_valuations_even is False
    assert weak.rows_by_prime[29].product_valuations_even
    assert weak.three_mod_four_primes == (3, 7, 11, 19, 23, 31)
    assert all(row.all_member_valuations_even for row in weak.three_mod_four_rows)

    true = closure_member_prime_valuation_ledger(
        Fraction(1),
        Fraction(25, 12),
        Fraction(1),
        REL_SUM_AB,
    )

    assert true.member_squareclass_primes == ()
    assert true.three_mod_four_primes == (3,)
    assert true.rows_by_prime[3].member_valuations == (0, -2, 0, -2)
    assert true.rows_by_prime[3].identity_valuations == (-2, -2, None, None, None)
    assert true.rows_by_prime[3].all_member_valuations_even


def test_one_mod_four_squareclass_absorption_turns_guard_roots_into_leg_slopes() -> None:
    from rational_distance.concordant.rational_ratio import (
        squareclass_two_square_absorption,
    )

    first = squareclass_two_square_absorption(Fraction(14, 23), 29)

    assert first.squareclass == 29
    assert first.two_square_decomposition == (5, 2)
    assert first.absorbed_plus == Fraction(4, 3)
    assert first.absorbed_plus_value == Fraction(25, 9)
    assert first.absorbed_plus_is_member
    assert first.absorbed_minus == Fraction(24, 143)
    assert first.absorbed_minus_is_member

    second = squareclass_two_square_absorption(Fraction(26, 7), 29)

    assert second.absorbed_minus == Fraction(4, 3)
    assert second.absorbed_minus_is_member
    assert second.absorbed_plus == Fraction(-144, 17)


def test_residual_gaussian_absorption_ledger_detects_centerline_shadow() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        closure_product_square_conditions,
        residual_gaussian_absorption_ledger,
    )

    condition = closure_product_square_conditions(
        Fraction(535, 161),
        Fraction(696, 161),
        Fraction(364, 161),
        REL_SUM_AB,
    )

    ledger = residual_gaussian_absorption_ledger(condition)

    assert ledger.squareclass == 29
    assert ledger.r_absorption.absorbed_plus == Fraction(4, 3)
    assert ledger.s_absorption.absorbed_minus == Fraction(4, 3)
    assert ledger.common_absorbed_members == (Fraction(4, 3),)
    assert ledger.centerline_shadow


def test_inverse_gaussian_absorption_pair_reconstructs_guard_residual() -> None:
    from rational_distance.concordant.rational_ratio import (
        inverse_gaussian_absorption_pair,
    )

    pair = inverse_gaussian_absorption_pair(
        absorbed=Fraction(4, 3),
        squareclass=29,
        r_branch="plus",
        s_branch="minus",
    )

    assert pair.two_square_decomposition == (5, 2)
    assert pair.r == Fraction(14, 23)
    assert pair.s == Fraction(26, 7)
    assert pair.lambda_ratio == Fraction(535, 161)
    assert pair.product == Fraction(52, 23)
    assert pair.condition.product_square_bucket == "residual"
    assert pair.condition.member_squareclass_pair == (29, 29)


def test_inverse_gaussian_absorption_pair_terms_factor_guard_identity() -> None:
    from rational_distance.concordant.rational_ratio import (
        inverse_gaussian_absorption_pair_terms,
    )

    terms = inverse_gaussian_absorption_pair_terms(
        absorbed=Fraction(4, 3),
        squareclass=29,
        r_branch="plus",
        s_branch="minus",
    )

    assert terms.pair.lambda_ratio == Fraction(535, 161)
    assert terms.pair.product == Fraction(52, 23)
    assert terms.denominator_product == Fraction(161, 9)
    assert terms.lambda_numerator == Fraction(535, 9)
    assert terms.product_numerator == Fraction(364, 9)
    assert terms.lambda_minus_product_left_factor == Fraction(3)
    assert terms.lambda_minus_product_right_factor == Fraction(19, 3)
    assert terms.lambda_minus_product_factorized == (
        terms.pair.lambda_ratio - terms.pair.product
    )
    assert terms.lambda_plus_product_z_factor == Fraction(31, 9)
    assert terms.lambda_plus_product_factorized == (
        terms.pair.lambda_ratio + terms.pair.product
    )
    assert terms.lambda_squared_minus_product_squared_factorized == (
        terms.pair.lambda_ratio**2 - terms.pair.product**2
    )
    assert terms.lambda_squared_minus_one_extra_factor == Fraction(187, 9)
    assert terms.lambda_squared_minus_one_factorized == (
        terms.pair.lambda_ratio**2 - 1
    )
    assert terms.a_term_factorized == terms.identity_terms.a_term
    assert terms.b_term_minus_factor == Fraction(10201, 81)
    assert terms.b_term_plus_factor == Fraction(22201, 81)
    assert terms.b_term_factorized == terms.identity_terms.b_term
    assert terms.b_minus_lambda_sq_a_factorized == (
        terms.identity_terms.b_minus_lambda_sq_a
    )
    assert terms.factorization_holds


def test_inverse_gaussian_absorption_pair_terms_factor_member_squares() -> None:
    from rational_distance.concordant.rational_ratio import (
        inverse_gaussian_absorption_pair_terms,
    )

    terms = inverse_gaussian_absorption_pair_terms(
        absorbed=Fraction(4, 3),
        squareclass=29,
        r_branch="plus",
        s_branch="minus",
    )

    assert terms.r_unit_value_factorized == terms.pair.r**2 + 1
    assert terms.s_unit_value_factorized == terms.pair.s**2 + 1
    assert terms.r_lambda_value_factorized == (
        terms.pair.r**2 + terms.pair.lambda_ratio**2
    )
    assert terms.s_lambda_value_factorized == (
        terms.pair.s**2 + terms.pair.lambda_ratio**2
    )
    assert terms.r_unit_value_factorized == Fraction(725, 529)
    assert terms.s_unit_value_factorized == Fraction(725, 49)
    assert terms.r_lambda_value_factorized == Fraction(295829, 25921)
    assert terms.s_lambda_value_factorized == Fraction(643829, 25921)
    assert (
        terms.r_unit_value_factorized * terms.s_unit_value_factorized
        == terms.identity_terms.a_term
    )
    assert (
        terms.r_lambda_value_factorized * terms.s_lambda_value_factorized
        == terms.identity_terms.b_term
    )
    assert terms.member_factorization_holds


def test_inverse_gaussian_centerline_shadow_obstruction_blocks_unit_terms() -> None:
    from rational_distance.concordant.rational_ratio import (
        inverse_gaussian_centerline_shadow_obstruction,
    )

    obstruction = inverse_gaussian_centerline_shadow_obstruction(
        absorbed=Fraction(4, 3),
        squareclass=29,
        r_branch="plus",
        s_branch="minus",
    )

    assert obstruction.absorbed_unit_value == Fraction(25, 9)
    assert obstruction.absorbed_unit_value_is_square
    assert obstruction.squareclass_is_trivial is False
    assert obstruction.r_unit_squareclass == 29
    assert obstruction.s_unit_squareclass == 29
    assert obstruction.unit_squareclass_obstruction
    assert obstruction.true_member_pair_blocked
    assert obstruction.obstruction_reason == "nontrivial-squareclass-on-unit-terms"


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


def test_sum_ab_root_grid_residual_prime_class_summary_tracks_1_mod_4_escape() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_root_grid_residual_prime_class_summary,
    )

    summary = sum_ab_root_grid_residual_prime_class_summary(
        max_numerator=26,
        max_denominator=23,
    )

    assert summary.total_residuals == 1
    assert summary.bucket_counts == {
        "only_1_mod_4_squareclass": 1,
    }
    assert summary.squareclass_prime_counts == {
        (29,): 1,
    }
    assert summary.three_mod_four_squareclass_prime_counts == {
        (): 1,
    }
    assert summary.examples_by_bucket[
        "only_1_mod_4_squareclass"
    ].member_squareclass_pair == (29, 29)
    assert summary.examples_by_bucket[
        "only_1_mod_4_squareclass"
    ].lambda_ratio == Fraction(535, 161)


def test_sum_ab_root_grid_gaussian_shadow_summary_counts_centerline_shadows() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_root_grid_gaussian_shadow_summary,
    )

    summary = sum_ab_root_grid_gaussian_shadow_summary(
        max_numerator=26,
        max_denominator=23,
    )

    assert summary.total_residuals == 1
    assert summary.centerline_shadow_count == 1
    assert summary.nonshadow_count == 0
    assert summary.common_absorbed_member_counts == {
        (Fraction(4, 3),): 1,
    }
    assert summary.examples_by_bucket["centerline_shadow"].lambda_ratio == Fraction(
        535,
        161,
    )


def test_sum_ab_root_grid_gaussian_shadow_obstruction_summary_counts_blocked_shadows() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_root_grid_gaussian_shadow_obstruction_summary,
    )

    summary = sum_ab_root_grid_gaussian_shadow_obstruction_summary(
        max_numerator=26,
        max_denominator=23,
    )

    assert summary.total_residuals == 1
    assert summary.centerline_shadow_count == 1
    assert summary.unit_obstructed_count == 1
    assert summary.nonobstructed_count == 0
    assert summary.obstruction_reason_counts == {
        "nontrivial-squareclass-on-unit-terms": 1,
    }
    assert summary.examples_by_bucket["unit_obstructed"].lambda_ratio == Fraction(
        535,
        161,
    )
    assert summary.examples_by_bucket["unit_obstructed"].member_squareclass_pair == (
        29,
        29,
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


def test_sum_ab_same_orientation_denominator_factorization_exposes_shared_leg_offsets() -> None:
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

    assert factorization.shared_numerator == 105
    assert factorization.shared_minus_other_denominator == -255
    assert factorization.shared_minus_failed_denominator == -315
    assert factorization.shared_minus_other_factorization == (15, -17)
    assert factorization.shared_minus_failed_factorization == (45, -7)

    even_factorization = sum_ab_same_orientation_denominator_factorization(
        slope_m=4,
        slope_n=1,
        scaled_term_m=7,
        scaled_term_n=2,
        orientation="even",
    )

    assert even_factorization.shared_numerator == 556
    assert even_factorization.shared_minus_other_denominator == 136
    assert even_factorization.shared_minus_failed_denominator == 196
    assert even_factorization.shared_minus_other_factorization == (8, 17)
    assert even_factorization.shared_minus_failed_factorization == (28, 7)


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


def test_sum_ab_four_slope_squareclass_summary_separates_centerline_artifacts() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_four_slope_squareclass_summary,
    )

    summary = sum_ab_four_slope_squareclass_summary(max_m=8)

    assert summary.max_m == 8
    assert summary.slope_count == 30
    assert summary.equal_unit_squareclass_pairs == 21
    assert summary.centerline_equal_unit_squareclass_pairs == 21
    assert summary.noncenter_equal_unit_squareclass_pairs == 0
    assert summary.true_four_pass_pairs == 0
    assert summary.centerline_squareclasses[13] == 1
    assert summary.centerline_squareclasses[65] == 1


def test_sum_ab_four_slope_squareclass_witnesses_record_equal_squareclass_pairs() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_four_slope_squareclass_witnesses,
    )

    witnesses = sum_ab_four_slope_squareclass_witnesses(max_m=8, limit=3)

    assert len(witnesses) == 3
    assert all(witness.centerline for witness in witnesses)
    assert all(not witness.true_four_pass for witness in witnesses)
    assert witnesses[0].slope1 == witnesses[0].slope2
    assert witnesses[0].r == witnesses[0].s
    assert witnesses[0].unit_squareclass == 13
    assert witnesses[0].lambda_ratio == Fraction(2)

    noncenter = sum_ab_four_slope_squareclass_witnesses(
        max_m=8,
        include_centerline=False,
    )

    assert noncenter == ()


def test_sum_ab_squareclass_ratio_z_reduction_matches_direct_terms() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_squareclass_ratio_z_reduction,
    )

    reduction = sum_ab_squareclass_ratio_z_reduction(Fraction(1, 4), Fraction(2, 7))

    assert reduction.t == Fraction(1, 4)
    assert reduction.u == Fraction(2, 7)
    assert reduction.z == Fraction(-45, 14)
    assert reduction.direct_ratio == reduction.reduced_ratio
    assert reduction.direct_ratio == Fraction(30346, 27421)
    assert not reduction.ratio_is_square
    assert reduction.u_recovery_square == reduction.z * reduction.z + 4

    centerline = sum_ab_squareclass_ratio_z_reduction(Fraction(1, 4), Fraction(1, 4))

    assert centerline.z == Fraction(-15, 4)
    assert centerline.direct_ratio == 1
    assert centerline.ratio_is_square


def test_sum_ab_squareclass_ratio_z_parameterization_is_self_similar() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_squareclass_ratio_z_parameterization,
        sum_ab_squareclass_ratio_z_reduction,
    )

    parametrized = sum_ab_squareclass_ratio_z_parameterization(
        Fraction(1, 4),
        Fraction(2, 7),
    )
    direct = sum_ab_squareclass_ratio_z_reduction(Fraction(1, 4), Fraction(2, 7))

    assert parametrized.z == direct.z
    assert parametrized.reduced_ratio == direct.reduced_ratio
    assert parametrized.self_similar_ratio == direct.direct_ratio
    assert parametrized.centerline_factor != 0
    assert not parametrized.ratio_is_square

    centerline = sum_ab_squareclass_ratio_z_parameterization(
        Fraction(1, 4),
        Fraction(1, 4),
    )

    assert centerline.centerline_factor == 0
    assert centerline.reduced_ratio == centerline.self_similar_ratio
    assert centerline.self_similar_ratio == 1
    assert centerline.ratio_is_square


def test_sum_ab_squareclass_ratio_tu_quotient_model_tracks_recovery_conditions() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_squareclass_ratio_tu_quotient_model,
        sum_ab_squareclass_ratio_z_reduction,
    )

    model = sum_ab_squareclass_ratio_tu_quotient_model(
        Fraction(-15, 4),
        Fraction(-45, 14),
    )
    direct = sum_ab_squareclass_ratio_z_reduction(Fraction(1, 4), Fraction(2, 7))

    assert model.ratio == direct.direct_ratio
    assert model.t_recovery_square
    assert model.u_recovery_square
    assert not model.ratio_is_square
    assert model.numerator_quadratic - model.denominator_quadratic == (
        model.t_quotient - model.u_quotient
    ) * (model.t_quotient + model.u_quotient)

    fake = sum_ab_squareclass_ratio_tu_quotient_model(Fraction(-7), Fraction(-35, 17))

    assert fake.ratio == Fraction(28561, 15625)
    assert fake.ratio_is_square
    assert not fake.t_recovery_square
    assert not fake.u_recovery_square


def test_sum_ab_squareclass_ratio_slope_quadratic_model_matches_quotient_model() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_squareclass_ratio_slope_quadratic_model,
        sum_ab_squareclass_ratio_tu_quotient_model,
    )

    model = sum_ab_squareclass_ratio_slope_quadratic_model(
        Fraction(15, 8),
        Fraction(45, 28),
    )
    quotient = sum_ab_squareclass_ratio_tu_quotient_model(
        Fraction(-15, 4),
        Fraction(-45, 14),
    )

    assert model.ratio == quotient.ratio
    assert model.ratio == Fraction(30346, 27421)
    assert model.x_recovery_square
    assert model.y_recovery_square
    assert model.numerator_quadratic - model.denominator_quadratic == (
        model.slope_x - model.slope_y
    ) * (model.slope_x + model.slope_y)

    fake = sum_ab_squareclass_ratio_slope_quadratic_model(
        Fraction(7, 2),
        Fraction(35, 34),
    )

    assert fake.ratio == Fraction(28561, 15625)
    assert fake.ratio_is_square
    assert not fake.x_recovery_square
    assert not fake.y_recovery_square


def test_sum_ab_squareclass_ratio_slope_model_tracks_individual_squares() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_squareclass_ratio_slope_quadratic_model,
    )

    model = sum_ab_squareclass_ratio_slope_quadratic_model(
        Fraction(15, 8),
        Fraction(45, 28),
    )

    assert model.numerator_quadratic == Fraction(15173, 1568)
    assert model.denominator_quadratic == Fraction(27421, 3136)
    assert not model.numerator_is_square
    assert not model.denominator_is_square
    assert not model.individual_unit_terms_are_squares

    fake = sum_ab_squareclass_ratio_slope_quadratic_model(
        Fraction(7, 2),
        Fraction(35, 34),
    )

    assert fake.ratio_is_square
    assert fake.numerator_is_square
    assert fake.denominator_is_square
    assert fake.individual_unit_terms_are_squares
    assert not fake.x_recovery_square
    assert not fake.y_recovery_square


def test_sum_ab_four_square_dual_slope_model_records_both_pythagorean_halves() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_four_square_dual_slope_model,
    )

    original = sum_ab_four_square_dual_slope_model(
        Fraction(15, 8),
        Fraction(45, 28),
    )

    assert original.common_leg == Fraction(139, 56)
    assert original.dual_slope_x == Fraction(139, 105)
    assert original.dual_slope_y == Fraction(139, 90)
    assert original.x_is_pythagorean
    assert original.y_is_pythagorean
    assert not original.dual_x_is_pythagorean
    assert not original.dual_y_is_pythagorean
    assert not original.all_four_slopes_are_pythagorean
    assert original.self_dual_identity_holds

    fake = sum_ab_four_square_dual_slope_model(
        Fraction(7, 2),
        Fraction(35, 34),
    )

    assert fake.common_leg == Fraction(60, 17)
    assert fake.dual_slope_x == Fraction(120, 119)
    assert fake.dual_slope_y == Fraction(24, 7)
    assert not fake.x_is_pythagorean
    assert not fake.y_is_pythagorean
    assert fake.dual_x_is_pythagorean
    assert fake.dual_y_is_pythagorean
    assert not fake.all_four_slopes_are_pythagorean
    assert fake.reconstructed_x == fake.slope_x
    assert fake.reconstructed_y == fake.slope_y
    assert fake.reconstructed_common_leg == fake.common_leg
    assert fake.self_dual_identity_holds


def test_sum_ab_dual_slope_parameterization_exposes_centerline_factor() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_parameterization,
    )

    model = sum_ab_dual_slope_parameterization(Fraction(1, 4), Fraction(2, 7))

    assert model.dual_slope_x == Fraction(15, 8)
    assert model.dual_slope_y == Fraction(45, 28)
    assert model.generated_x == Fraction(24, 7)
    assert model.generated_y == Fraction(4)
    assert model.common_leg == Fraction(45, 7)
    assert model.generated_x_recovery_value == Fraction(625, 49)
    assert model.generated_y_recovery_value == Fraction(17)
    assert model.generated_x_is_pythagorean
    assert not model.generated_y_is_pythagorean
    assert model.generated_x_minus_y == Fraction(-4, 7)
    assert model.generated_x_minus_y_factorized == model.generated_x_minus_y
    assert model.recovery_value_difference_factorized == (
        model.generated_x_recovery_value - model.generated_y_recovery_value
    )
    assert model.centerline_factor != 0
    assert not model.centerline_factor_zero

    centerline = sum_ab_dual_slope_parameterization(Fraction(1, 4), Fraction(1, 4))

    assert centerline.generated_x == centerline.generated_y
    assert centerline.centerline_factor == 0
    assert centerline.centerline_factor_zero
    assert centerline.centerline_recovery_quartic == Fraction(65, 256)
    assert centerline.generated_x_recovery_value == Fraction(65)


def test_sum_ab_dual_slope_valuation_ledger_tracks_3_mod_4_boundary() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_valuation_ledger,
    )

    ledger = sum_ab_dual_slope_valuation_ledger(Fraction(1, 4), Fraction(2, 7))

    assert ledger.recovery_squareclasses == (1, 17)
    assert ledger.recovery_squareclass_primes == (17,)
    assert ledger.three_mod_four_recovery_squareclass_primes == ()
    assert ledger.three_mod_four_primes == (3, 7)
    assert ledger.rows_by_prime[7].recovery_valuations == (-2, 0)
    assert ledger.rows_by_prime[7].recovery_difference_valuation == -2
    assert ledger.rows_by_prime[7].centerline_factor_valuation == -4
    assert ledger.rows_by_prime[7].all_recovery_valuations_even
    assert ledger.rows_by_prime[17].recovery_valuations == (0, 1)
    assert not ledger.rows_by_prime[17].all_recovery_valuations_even


def test_sum_ab_dual_slope_qadic_norm_ledger_tracks_shadow_squareclasses() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_qadic_norm_ledger,
    )

    ledger = sum_ab_dual_slope_qadic_norm_ledger(
        Fraction(61, 77),
        Fraction(5, 77),
        prime=31,
    )

    assert ledger.q_norm_values == (-Fraction(41888068, 35153041), Fraction(43356476, 35153041))
    assert ledger.q_norm_valuations == (2, 2)
    assert ledger.recovery_squareclasses == (545050311562, 211590847301)
    assert ledger.recovery_valuations_at_prime == (0, 0)
    assert ledger.shadow_prime_balanced_in_recovery_squareclasses
    assert ledger.q_norm_squareclasses == (10897, 11279)
    assert ledger.odd_q_norm_squareclass_primes == ((17, 641), (11279,))
    assert 31 not in ledger.recovery_squareclass_primes[0]
    assert 31 not in ledger.recovery_squareclass_primes[1]


def test_sum_ab_dual_slope_qadic_norm_summary_counts_recovery_prime_patterns() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_qadic_norm_summary,
    )

    summary = sum_ab_dual_slope_qadic_norm_summary(
        (
            (Fraction(61, 77), Fraction(5, 77)),
            (Fraction(20, 41), Fraction(5, 77)),
        ),
        prime=31,
    )

    assert summary.sample_count == 2
    assert summary.shadow_prime_balanced_count == 2
    assert summary.recovery_contains_shadow_prime_count == 0
    assert summary.recovery_has_three_mod_four_prime_count == 0
    assert summary.recovery_has_only_two_or_one_mod_four_primes_count == 2
    assert summary.q_norm_valuation_pair_counts == {(2, 2): 2}
    assert summary.examples_by_bucket["only_two_or_one_mod_four"].parameter_pairs == (
        Fraction(61, 77),
        Fraction(5, 77),
    )


def test_sum_ab_dual_slope_qadic_norm_generated_summary_expands_shadow_samples() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_qadic_norm_generated_summary,
    )

    generated = sum_ab_dual_slope_qadic_norm_generated_summary(
        prime=31,
        exponent=2,
        representative_bound=80,
        sample_limit=4,
    )

    assert generated.prime == 31
    assert generated.modulus == 31 * 31
    assert generated.root_count_mod_prime == 8
    assert generated.lift_count == 8
    assert generated.summary.sample_count == 4
    assert generated.summary.shadow_prime_balanced_count == 4
    assert generated.summary.recovery_contains_shadow_prime_count == 0
    assert generated.summary.recovery_has_three_mod_four_prime_count == 0
    assert generated.summary.recovery_has_only_two_or_one_mod_four_primes_count == 4
    assert set(generated.summary.q_norm_valuation_pair_counts) == {(2, 2)}
    assert generated.summary.recovery_prime_mod4_counts == {1: 16, 2: 4}
    assert generated.summary.recovery_prime_mod8_counts == {1: 8, 2: 4, 5: 8}
    assert generated.summary.recovery_prime_mod16_counts == {
        1: 3,
        2: 4,
        5: 5,
        9: 5,
        13: 3,
    }
    assert all(t > 0 and u > 0 for t, u in generated.parameter_pairs)


def test_sum_ab_dual_slope_qadic_norm_generated_summary_tries_multiple_representatives() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_qadic_norm_generated_summary,
    )

    generated = sum_ab_dual_slope_qadic_norm_generated_summary(
        prime=47,
        exponent=2,
        representative_bound=220,
        sample_limit=4,
    )

    assert generated.root_count_mod_prime == 8
    assert generated.lift_count == 8
    assert generated.summary.sample_count == 4
    assert set(generated.summary.q_norm_valuation_pair_counts) == {(2, 2)}
    assert generated.summary.recovery_contains_shadow_prime_count == 0
    assert generated.summary.recovery_prime_mod4_counts == {1: 20, 2: 4}
    assert generated.summary.recovery_prime_mod8_counts == {1: 11, 2: 4, 5: 9}
    assert all(t > 0 and u > 0 for t, u in generated.parameter_pairs)


def test_sum_ab_dual_slope_qadic_norm_bridge_summary_rewrites_recovery_as_bridges() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_qadic_norm_bridge_summary,
    )

    bridge_summary = sum_ab_dual_slope_qadic_norm_bridge_summary(
        prime=31,
        exponent=2,
        representative_bound=80,
        sample_limit=4,
    )

    assert bridge_summary.sample_count == 4
    assert bridge_summary.recovery_matches_bridge_squareclass_count == 4
    assert bridge_summary.generated_flags_match_bridge_flags_count == 4
    assert bridge_summary.all_cross_bridges_pythagorean_count == 0
    assert bridge_summary.first_ledger.norm_ledger.recovery_squareclasses == (
        113231540023993,
        54204260682434,
    )
    assert bridge_summary.first_ledger.bridge_cycle.bridge_squareclasses == (
        113231540023993,
        54204260682434,
    )


def test_sum_ab_dual_slope_qadic_bridge_valuation_summary_tracks_e_near_tube() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_qadic_bridge_valuation_summary,
    )

    valuation_summary = sum_ab_dual_slope_qadic_bridge_valuation_summary(
        prime=31,
        exponent=2,
        representative_bound=80,
        sample_limit=8,
    )

    assert valuation_summary.sample_count == 8
    assert valuation_summary.centerline_factor_valuation_counts == {
        (0, 0, 0, 0): 8
    }
    assert valuation_summary.extra_factor_valuation_counts == {2: 8}
    assert valuation_summary.bridge_difference_valuation_counts == {2: 8}
    assert valuation_summary.bridge_value_valuation_pair_counts == {(0, 0): 8}
    assert valuation_summary.bridge_value_2adic_pair_counts == {
        (0, 1): 4,
        (1, 0): 4,
    }
    assert valuation_summary.first_row.extra_factor_valuation == 2
    assert valuation_summary.first_row.centerline_factor_valuations == (0, 0, 0, 0)


def test_sum_ab_dual_slope_qadic_bridge_2adic_summary_separates_parity_survivors() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_qadic_bridge_2adic_summary,
    )

    killed = sum_ab_dual_slope_qadic_bridge_2adic_summary(
        prime=31,
        exponent=2,
        representative_bound=80,
        sample_limit=8,
    )
    survivor = sum_ab_dual_slope_qadic_bridge_2adic_summary(
        prime=47,
        exponent=2,
        representative_bound=220,
        sample_limit=8,
    )

    assert killed.sample_count == 8
    assert killed.parity_killed_count == 8
    assert killed.two_adic_local_square_count == 0
    assert killed.bridge_value_2adic_pair_counts == {(0, 1): 4, (1, 0): 4}
    assert survivor.sample_count == 8
    assert survivor.parity_killed_count == 6
    assert survivor.two_adic_local_square_count == 2
    assert survivor.bridge_value_2adic_pair_counts == {
        (-6, -6): 2,
        (0, 1): 3,
        (1, 0): 3,
    }
    assert survivor.local_square_unit_mod8_pair_counts == {(1, 1): 2}


def test_sum_ab_dual_slope_qadic_bridge_local_square_summary_keeps_survivors() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_qadic_bridge_local_square_summary,
    )

    q47 = sum_ab_dual_slope_qadic_bridge_local_square_summary(
        prime=47,
        exponent=2,
        representative_bound=220,
        sample_limit=8,
    )
    q79 = sum_ab_dual_slope_qadic_bridge_local_square_summary(
        prime=79,
        exponent=2,
        representative_bound=260,
        sample_limit=8,
    )

    assert q47.sample_count == 8
    assert q47.two_adic_local_square_count == 2
    assert q47.q_adic_local_square_count == 8
    assert q47.combined_q_and_2_adic_local_square_count == 2
    assert q47.q_adic_local_square_flag_pair_counts == {(True, True): 8}
    assert q79.sample_count == 8
    assert q79.two_adic_local_square_count == 4
    assert q79.q_adic_local_square_count == 8
    assert q79.combined_q_and_2_adic_local_square_count == 4
    assert q79.combined_survivor_parameter_pairs[0] == (Fraction(151, 176), Fraction(49, 108))


def test_sum_ab_dual_slope_gaussian_absorption_returns_failure_to_dual_slope() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_gaussian_absorption,
    )

    absorption = sum_ab_dual_slope_gaussian_absorption(
        Fraction(1, 4),
        Fraction(2, 7),
        failed_side="y",
    )

    assert absorption.failed_slope == Fraction(4)
    assert absorption.failed_squareclass == 17
    assert absorption.two_square_decomposition == (4, 1)
    assert absorption.absorbed_plus is None
    assert absorption.absorbed_minus == Fraction(15, 8)
    assert absorption.matching_absorptions == (("minus", "dual_x", Fraction(15, 8)),)
    assert absorption.absorbs_to_existing_dual_slope


def test_sum_ab_dual_slope_gaussian_bridge_recovers_target_squareclass() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_gaussian_bridge,
    )

    bridge = sum_ab_dual_slope_gaussian_bridge(
        Fraction(1, 4),
        Fraction(2, 7),
        failed_side="y",
        target_side="dual_x",
    )

    assert bridge.failed_slope == Fraction(4)
    assert bridge.target_slope == Fraction(15, 8)
    assert bridge.bridge_ratio == Fraction(1, 4)
    assert bridge.bridge_value == Fraction(17, 16)
    assert bridge.bridge_squareclass == 17
    assert bridge.failed_squareclass == 17
    assert bridge.squareclass_matches_failure
    assert bridge.recovered_target == bridge.target_slope
    assert bridge.recovery_identity_holds


def test_sum_ab_dual_slope_gaussian_bridge_cycle_reduces_squares_to_bridges() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_gaussian_bridge_cycle,
    )

    cycle = sum_ab_dual_slope_gaussian_bridge_cycle(Fraction(1, 4), Fraction(2, 7))

    assert cycle.generated_slopes == (Fraction(24, 7), Fraction(4))
    assert cycle.dual_slopes == (Fraction(15, 8), Fraction(45, 28))
    assert cycle.x_to_dual_y.bridge_ratio == Fraction(357, 1276)
    assert cycle.y_to_dual_x.bridge_ratio == Fraction(1, 4)
    assert cycle.bridge_ratios == (Fraction(357, 1276), Fraction(1, 4))
    assert cycle.generated_squareclasses == (1, 17)
    assert cycle.bridge_squareclasses == (1, 17)
    assert cycle.generated_pythagorean_flags == (True, False)
    assert cycle.bridge_pythagorean_flags == (True, False)
    assert cycle.generated_flags_match_bridge_flags
    assert not cycle.all_generated_slopes_are_pythagorean
    assert not cycle.all_cross_bridges_are_pythagorean


def test_sum_ab_dual_slope_bridge_difference_factors_through_new_curve() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_bridge_difference_factorization,
    )

    factorization = sum_ab_dual_slope_bridge_difference_factorization(
        Fraction(1, 4),
        Fraction(2, 7),
    )

    assert factorization.bridge_value_difference == Fraction(3211, 203522)
    assert factorization.centerline_factor == Fraction(2925, 153664)
    assert factorization.extra_equal_bridge_factor == Fraction(285, 784)
    assert factorization.bridge_difference_factorized == (
        factorization.bridge_value_difference
    )
    assert factorization.factorization_holds
    assert factorization.extra_factor_u_quadratic_coefficients == (
        Fraction(-11, 16),
        Fraction(-15, 16),
        Fraction(11, 16),
    )
    assert factorization.extra_factor_u_discriminant == Fraction(709, 256)
    assert factorization.new_curve_value_t == Fraction(709, 256)
    assert factorization.extra_factor_discriminant_matches_new_curve


def test_sum_ab_bridge_extra_factor_reduces_to_z_lemma_centerline() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_bridge_extra_factor_z_lemma_reduction,
    )

    reduction = sum_ab_bridge_extra_factor_z_lemma_reduction(Fraction(1, 4))

    assert reduction.parameter_t == Fraction(1, 4)
    assert reduction.z_value == -Fraction(15, 4)
    assert reduction.z_parameter_m == -Fraction(3, 5)
    assert reduction.new_curve_value_t == Fraction(709, 256)
    assert reduction.scaled_new_curve_value == Fraction(709, 16)
    assert reduction.z_recovery_square == Fraction(289, 16)
    assert reduction.z_lemma_new_curve_square == Fraction(709, 16)
    assert reduction.z_reduction_identity_holds
    assert reduction.centerline_bridge.centerline_parameter == Fraction(3, 5)
    assert reduction.centerline_bridge.centerline_quartic == Fraction(2836, 625)
    assert reduction.centerline_bridge_identity_holds
    assert reduction.extra_factor_reduces_to_centerline


def test_sum_ab_dual_slope_bridge_residue_summary_routes_mod5_11_to_extra_factor() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_bridge_projective_residue_summary,
    )

    mod5 = sum_ab_dual_slope_bridge_projective_residue_summary(5)

    assert mod5.projective_class_count == 36
    assert mod5.both_bridge_square_classes == 15
    assert mod5.centerline_square_classes == 11
    assert mod5.noncenter_square_classes == 4
    assert mod5.noncenter_extra_factor_zero_classes == 4
    assert mod5.noncenter_extra_factor_nonzero_classes == 0
    assert mod5.noncenter_extra_factor_nonzero_examples == ()

    mod11 = sum_ab_dual_slope_bridge_projective_residue_summary(11)

    assert mod11.projective_class_count == 144
    assert mod11.both_bridge_square_classes == 36
    assert mod11.centerline_square_classes == 28
    assert mod11.noncenter_square_classes == 8
    assert mod11.noncenter_extra_factor_zero_classes == 8
    assert mod11.noncenter_extra_factor_nonzero_classes == 0

    mod7 = sum_ab_dual_slope_bridge_projective_residue_summary(7)

    assert mod7.noncenter_extra_factor_nonzero_classes == 32


def test_sum_ab_dual_slope_bridge_prime_power_lift_tracks_centerline_extra_factor() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_bridge_prime_power_lift_summary,
    )

    mod25 = sum_ab_dual_slope_bridge_prime_power_lift_summary(5, 2)

    assert mod25.modulus == 25
    assert mod25.projective_class_count == 900
    assert mod25.both_bridge_square_classes == 295
    assert mod25.valuation_pair_counts == {
        (0, 2): 20,
        (2, 0): 175,
        (2, 1): 80,
        (2, 2): 20,
    }
    assert mod25.centerline_unit_extra_unit_classes == 0
    assert mod25.centerline_unit_classes == 20
    assert mod25.centerline_unit_min_extra_valuation == 2

    mod121 = sum_ab_dual_slope_bridge_prime_power_lift_summary(11, 2)

    assert mod121.modulus == 121
    assert mod121.projective_class_count == 17424
    assert mod121.both_bridge_square_classes == 4356
    assert mod121.centerline_unit_extra_unit_classes == 0
    assert mod121.centerline_unit_classes == 968
    assert mod121.centerline_unit_min_extra_valuation == 1


def test_sum_ab_dual_slope_bridge_centerline_factor_lift_splits_centerline_tubes() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_bridge_centerline_factor_lift_summary,
    )

    mod25 = sum_ab_dual_slope_bridge_centerline_factor_lift_summary(5, 2)

    assert mod25.modulus == 25
    assert mod25.projective_class_count == 900
    assert mod25.both_bridge_square_classes == 295
    assert mod25.max_centerline_factor_extra_valuation_counts == {
        (0, 2): 20,
        (1, 0): 112,
        (1, 1): 64,
        (2, 0): 63,
        (2, 1): 16,
        (2, 2): 20,
    }
    assert mod25.factor_extra_valuation_counts[(0, 0, 0, 0, 2)] == 20
    assert mod25.factor_extra_valuation_counts[(2, 2, 0, 0, 0)] == 2
    assert mod25.factor_extra_valuation_counts[(0, 0, 2, 2, 0)] == 2
    assert mod25.factor_extra_valuation_counts[(0, 2, 0, 2, 2)] == 2

    mod121 = sum_ab_dual_slope_bridge_centerline_factor_lift_summary(11, 2)

    assert mod121.modulus == 121
    assert mod121.projective_class_count == 17424
    assert mod121.both_bridge_square_classes == 4356
    assert mod121.max_centerline_factor_extra_valuation_counts == {
        (0, 1): 880,
        (0, 2): 88,
        (1, 0): 2600,
        (1, 1): 400,
        (2, 0): 304,
        (2, 1): 40,
        (2, 2): 44,
    }
    assert mod121.factor_extra_valuation_counts[(0, 0, 0, 0, 1)] == 880
    assert mod121.factor_extra_valuation_counts[(0, 0, 1, 0, 0)] == 880
    assert mod121.factor_extra_valuation_counts[(2, 2, 0, 0, 0)] == 2
    assert mod121.factor_extra_valuation_counts[(0, 0, 2, 2, 0)] == 2


def test_sum_ab_bridge_branch_restrictions_split_quartic_from_square() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_bridge_centerline_branch_restrictions,
    )

    restrictions = sum_ab_dual_slope_bridge_centerline_branch_restrictions(
        Fraction(1, 4)
    )
    by_branch = {restriction.branch: restriction for restriction in restrictions}

    assert tuple(by_branch) == ("t-u", "t+u", "tu-1", "tu+1")
    assert all(restriction.bridge_numerators_equal for restriction in restrictions)
    assert all(restriction.common_identity_holds for restriction in restrictions)
    assert all(restriction.extra_identity_holds for restriction in restrictions)

    assert by_branch["t-u"].parameter_u == Fraction(1, 4)
    assert by_branch["t-u"].restriction_kind == "centerline-quartic"
    assert by_branch["t-u"].common_bridge_numerator == Fraction(14625, 65536)
    assert by_branch["t-u"].extra_factor == Fraction(105, 256)

    assert by_branch["t+u"].parameter_u == -Fraction(1, 4)
    assert by_branch["t+u"].restriction_kind == "trivial-square"
    assert by_branch["t+u"].common_bridge_numerator == Fraction(65025, 65536)
    assert by_branch["t+u"].extra_factor == Fraction(225, 256)

    assert by_branch["tu-1"].parameter_u == Fraction(4)
    assert by_branch["tu-1"].restriction_kind == "trivial-square"
    assert by_branch["tu-1"].common_bridge_numerator == Fraction(65025, 256)
    assert by_branch["tu-1"].extra_factor == -Fraction(225, 16)

    assert by_branch["tu+1"].parameter_u == -Fraction(4)
    assert by_branch["tu+1"].restriction_kind == "centerline-quartic"
    assert by_branch["tu+1"].common_bridge_numerator == Fraction(14625, 256)
    assert by_branch["tu+1"].extra_factor == -Fraction(105, 16)


def test_sum_ab_bridge_trivial_tube_expansions_have_square_base() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_bridge_trivial_tube_expansions,
    )

    expansions = sum_ab_dual_slope_bridge_trivial_tube_expansions(Fraction(1, 4))
    by_branch = {expansion.branch: expansion for expansion in expansions}

    assert tuple(by_branch) == ("t+u", "tu-1")
    assert all(expansion.bridge_constants_equal for expansion in expansions)
    assert all(expansion.common_constant_is_square for expansion in expansions)
    assert all(expansion.nonzero_square_constant for expansion in expansions)

    plus = by_branch["t+u"]
    assert plus.base_u == -Fraction(1, 4)
    assert plus.common_constant_square_root == Fraction(255, 256)
    assert plus.x_coefficients == (
        Fraction(65025, 65536),
        -Fraction(10965, 4096),
        Fraction(3211, 2048),
        Fraction(307, 256),
        Fraction(113, 256),
    )
    assert plus.y_coefficients == (
        Fraction(65025, 65536),
        -Fraction(19125, 4096),
        Fraction(11243, 2048),
        Fraction(371, 256),
        Fraction(49, 256),
    )
    assert plus.difference_coefficients == (
        Fraction(0),
        Fraction(255, 128),
        -Fraction(251, 64),
        -Fraction(1, 4),
        Fraction(1, 4),
    )
    assert plus.extra_coefficients == (
        Fraction(225, 256),
        -Fraction(19, 32),
        -Fraction(11, 16),
    )

    inverse = by_branch["tu-1"]
    assert inverse.base_u == Fraction(4)
    assert inverse.common_constant_square_root == Fraction(255, 16)
    assert inverse.x_coefficients == (
        Fraction(65025, 256),
        Fraction(13515, 64),
        Fraction(8281, 128),
        Fraction(557, 64),
        Fraction(113, 256),
    )
    assert inverse.y_coefficients == (
        Fraction(65025, 256),
        Fraction(11475, 64),
        Fraction(5723, 128),
        Fraction(301, 64),
        Fraction(49, 256),
    )
    assert inverse.difference_coefficients == (
        Fraction(0),
        Fraction(255, 8),
        Fraction(1279, 64),
        Fraction(4),
        Fraction(1, 4),
    )
    assert inverse.extra_coefficients == (
        -Fraction(225, 16),
        -Fraction(103, 16),
        -Fraction(11, 16),
    )


def test_sum_ab_centerline_factor_exact_branches_separate_positive_domain() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_centerline_factor_positive_domain,
    )

    positive = sum_ab_dual_slope_centerline_factor_positive_domain(Fraction(1, 4))
    by_branch = {row.branch: row for row in positive}

    assert tuple(by_branch) == ("t-u", "t+u", "tu-1", "tu+1")
    assert by_branch["t-u"].parameter_u == Fraction(1, 4)
    assert by_branch["t-u"].parameter_u_in_unit_interval
    assert by_branch["t-u"].dual_slope_y_positive
    assert by_branch["t-u"].dual_denominator_positive
    assert by_branch["t-u"].admissible_positive_parameterization
    assert by_branch["t-u"].restriction_kind == "centerline-quartic"

    assert by_branch["t+u"].parameter_u == -Fraction(1, 4)
    assert not by_branch["t+u"].parameter_u_in_unit_interval
    assert not by_branch["t+u"].admissible_positive_parameterization
    assert by_branch["t+u"].restriction_kind == "trivial-square"

    assert by_branch["tu-1"].parameter_u == Fraction(4)
    assert not by_branch["tu-1"].parameter_u_in_unit_interval
    assert not by_branch["tu-1"].dual_slope_y_positive
    assert not by_branch["tu-1"].admissible_positive_parameterization
    assert by_branch["tu-1"].restriction_kind == "trivial-square"

    assert by_branch["tu+1"].parameter_u == -Fraction(4)
    assert not by_branch["tu+1"].parameter_u_in_unit_interval
    assert not by_branch["tu+1"].admissible_positive_parameterization
    assert by_branch["tu+1"].restriction_kind == "centerline-quartic"

    small = sum_ab_dual_slope_centerline_factor_positive_domain(Fraction(1, 5))
    small_by_branch = {row.branch: row for row in small}

    assert small_by_branch["t-u"].parameter_u_in_unit_interval
    assert small_by_branch["t-u"].dual_slope_y_positive
    assert not small_by_branch["t-u"].dual_denominator_positive
    assert not any(row.admissible_positive_parameterization for row in small)


def test_sum_ab_positive_trivial_tube_local_witnesses_show_5adic_gap() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_positive_trivial_tube_local_witnesses,
    )

    witnesses = sum_ab_dual_slope_positive_trivial_tube_local_witnesses()
    by_branch = {witness.branch: witness for witness in witnesses}

    assert tuple(by_branch) == ("t+u", "tu-1")
    assert all(witness.prime == 5 for witness in witnesses)
    assert all(witness.admissible_positive_parameterization for witness in witnesses)
    assert all(witness.tube_valuation == 2 for witness in witnesses)
    assert all(witness.recovery_values_are_local_squares for witness in witnesses)
    assert not any(witness.recovery_values_are_rational_squares for witness in witnesses)

    plus = by_branch["t+u"]
    assert plus.parameter_t == Fraction(1, 4)
    assert plus.parameter_u == Fraction(19, 24)
    assert plus.tube_value == Fraction(25, 24)
    assert plus.dual_denominator == Fraction(12175, 7296)
    assert plus.generated_slopes == (Fraction(344, 2435), Fraction(2736, 2435))
    assert plus.recovery_values == (
        Fraction(6047561, 5929225),
        Fraction(13414921, 5929225),
    )
    assert plus.local_square_flags == (True, True)
    assert plus.rational_square_flags == (False, False)

    inverse = by_branch["tu-1"]
    assert inverse.parameter_t == Fraction(1, 4)
    assert inverse.parameter_u == Fraction(7, 8)
    assert inverse.tube_value == -Fraction(25, 32)
    assert inverse.dual_denominator == Fraction(225, 128)
    assert inverse.generated_slopes == (Fraction(8, 105), Fraction(16, 15))
    assert inverse.recovery_values == (
        Fraction(11089, 11025),
        Fraction(481, 225),
    )
    assert inverse.local_square_flags == (True, True)
    assert inverse.rational_square_flags == (False, False)


def test_sum_ab_positive_trivial_tube_squareclass_ledgers_are_one_mod_four() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_positive_trivial_tube_squareclass_ledgers,
    )

    ledgers = sum_ab_dual_slope_positive_trivial_tube_squareclass_ledgers()
    by_branch = {ledger.witness.branch: ledger for ledger in ledgers}

    assert tuple(by_branch) == ("t+u", "tu-1")
    assert all(ledger.three_mod_four_squareclass_primes == () for ledger in ledgers)
    assert all(ledger.all_squareclass_primes_are_one_mod_four for ledger in ledgers)
    assert all(not ledger.witness.recovery_values_are_rational_squares for ledger in ledgers)

    plus = by_branch["t+u"]
    assert plus.recovery_squareclasses == (6047561, 13414921)
    assert plus.recovery_squareclass_primes == (
        (13, 173, 2689),
        (13, 17, 101, 601),
    )
    assert plus.one_mod_four_squareclass_primes == (
        13,
        17,
        101,
        173,
        601,
        2689,
    )

    inverse = by_branch["tu-1"]
    assert inverse.recovery_squareclasses == (11089, 481)
    assert inverse.recovery_squareclass_primes == ((13, 853), (13, 37))
    assert inverse.one_mod_four_squareclass_primes == (13, 37, 853)


def test_sum_ab_positive_trivial_tube_member_ledgers_fail_only_lambda_terms() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_dual_slope_positive_trivial_tube_member_ledgers,
    )

    ledgers = sum_ab_dual_slope_positive_trivial_tube_member_ledgers()
    by_branch = {ledger.witness.branch: ledger for ledger in ledgers}

    assert tuple(by_branch) == ("t+u", "tu-1")
    assert all(ledger.closes_sum_ab for ledger in ledgers)
    assert all(ledger.unit_terms_are_squares for ledger in ledgers)
    assert not any(ledger.lambda_terms_are_squares for ledger in ledgers)
    assert not any(ledger.true_member_pair for ledger in ledgers)
    assert all(ledger.three_mod_four_member_squareclass_primes == () for ledger in ledgers)

    plus = by_branch["t+u"]
    assert plus.lambda_ratio == Fraction(487, 129)
    assert plus.ratios == (Fraction(8, 15), Fraction(912, 215))
    assert plus.product == Fraction(2432, 1075)
    assert plus.member_squareclasses == (1, 1, 6047561, 13414921)
    assert plus.member_squareclass_primes == (
        (),
        (),
        (13, 173, 2689),
        (13, 17, 101, 601),
    )

    inverse = by_branch["tu-1"]
    assert inverse.lambda_ratio == Fraction(7)
    assert inverse.ratios == (Fraction(8, 15), Fraction(112, 15))
    assert inverse.product == Fraction(896, 225)
    assert inverse.member_squareclasses == (1, 1, 11089, 481)
    assert inverse.member_squareclass_primes == (
        (),
        (),
        (13, 853),
        (13, 37),
    )


def test_closure_identity_three_mod_four_balance_tracks_shared_compensation() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        closure_identity_three_mod_four_balance_ledger,
    )

    plus = closure_identity_three_mod_four_balance_ledger(
        Fraction(487, 129),
        Fraction(616, 129),
        Fraction(2432, 1075),
        REL_SUM_AB,
    )

    assert plus.odd_lambda_squared_minus_product_squared_primes == (7, 19471)
    assert plus.shared_odd_lambda_squared_minus_one_primes == (7,)
    assert plus.unshared_odd_lambda_squared_minus_product_squared_primes == (19471,)
    assert plus.odd_identity_difference_primes == (11, 179, 19471)
    assert plus.rows_by_prime[7].identity_valuations == (0, 0, 2, 1, 1)
    assert plus.rows_by_prime[7].lambda_squared_minus_one_odd
    assert plus.rows_by_prime[7].lambda_squared_minus_product_squared_odd
    assert plus.rows_by_prime[7].shared_odd_compensation
    assert plus.rows_by_prime[19471].identity_valuations == (0, 0, 1, 0, 1)
    assert not plus.rows_by_prime[19471].shared_odd_compensation

    inverse = closure_identity_three_mod_four_balance_ledger(
        Fraction(7),
        Fraction(8),
        Fraction(896, 225),
        REL_SUM_AB,
    )

    assert inverse.odd_lambda_squared_minus_product_squared_primes == ()
    assert inverse.shared_odd_lambda_squared_minus_one_primes == ()
    assert inverse.unshared_odd_lambda_squared_minus_product_squared_primes == ()
    assert inverse.odd_identity_difference_primes == (3,)


def test_closure_identity_shared_gcd_ledger_tracks_discriminant_boundary() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        closure_identity_shared_gcd_ledger,
    )

    ledger = closure_identity_shared_gcd_ledger(
        Fraction(487, 129),
        Fraction(616, 129),
        Fraction(2432, 1075),
        REL_SUM_AB,
    )

    assert ledger.shared_odd_compensation_primes == (7,)
    assert ledger.unshared_odd_lambda_squared_minus_product_squared_primes == (19471,)
    assert ledger.rows_by_prime[7].lambda_squared_minus_one_valuation == 1
    assert ledger.rows_by_prime[7].lambda_squared_minus_product_squared_valuation == 1
    assert ledger.rows_by_prime[7].p_squared_minus_one_valuation == 1
    assert ledger.rows_by_prime[7].closure_discriminant_valuation == 0
    assert ledger.rows_by_prime[7].p_squared_minus_one_carries_shared_factor
    assert ledger.rows_by_prime[7].closure_discriminant_valuation_even
    assert ledger.rows_by_prime[7].shared_odd_compensation

    assert ledger.rows_by_prime[19471].lambda_squared_minus_one_valuation == 0
    assert ledger.rows_by_prime[19471].lambda_squared_minus_product_squared_valuation == 1
    assert ledger.rows_by_prime[19471].p_squared_minus_one_valuation == 0
    assert ledger.rows_by_prime[19471].closure_discriminant_valuation == 0
    assert not ledger.rows_by_prime[19471].shared_odd_compensation
    assert not ledger.rows_by_prime[19471].p_squared_minus_one_carries_shared_factor


def test_sum_ab_shared_odd_prime_residue_summary_splits_sign_cases() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_shared_odd_prime_residue_summary,
    )

    killed = sum_ab_shared_odd_prime_residue_summary(3)

    assert killed.prime_mod_8 == 3
    assert killed.case_keys == ()
    assert killed.all_cases_killed

    seven = sum_ab_shared_odd_prime_residue_summary(7)

    assert seven.prime_mod_8 == 7
    assert seven.prime_mod_16 == 7
    assert seven.case_keys == ((1, 1), (-1, -1))
    assert seven.cases[0].root_residues == ((1, 1),)
    assert seven.cases[1].root_residues == ((1, 6), (6, 1))

    thirty_one = sum_ab_shared_odd_prime_residue_summary(31)

    assert thirty_one.prime_mod_16 == 15
    assert thirty_one.case_keys == ((1, 1), (1, -1), (-1, -1))
    assert thirty_one.cases[1].root_residues == ((9, 24), (24, 9))


def test_sum_ab_shared_odd_prime_power_lift_summary_tracks_p_shadow() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_shared_odd_prime_power_lift_summary,
    )

    seven = sum_ab_shared_odd_prime_power_lift_summary(7, 2)

    assert seven.modulus == 49
    assert seven.total_lifts == 72
    assert seven.pattern_counts == {
        (-1, -1, 1, 0, (0, 0, 0, 0)): 72,
    }
    assert seven.p_minus_lambda_shadow_count == 72
    assert seven.p_plus_lambda_shadow_count == 0

    thirty_one = sum_ab_shared_odd_prime_power_lift_summary(31, 2)

    assert thirty_one.modulus == 961
    assert thirty_one.total_lifts == 3600
    assert thirty_one.pattern_counts == {
        (-1, -1, 1, 0, (0, 0, 0, 0)): 1800,
        (1, -1, 0, 1, (0, 0, 0, 0)): 1800,
    }
    assert thirty_one.p_minus_lambda_shadow_count == 1800
    assert thirty_one.p_plus_lambda_shadow_count == 1800


def test_sum_ab_slope_ratio_y_discriminant_ledger_records_new_curve_factor() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_slope_ratio_y_discriminant_ledger,
    )

    ledger = sum_ab_slope_ratio_y_discriminant_ledger(Fraction(3, 4), Fraction(5, 7))

    assert ledger.slope_x == Fraction(3, 4)
    assert ledger.square_ratio == Fraction(5, 7)
    assert ledger.quadratic_coefficients == (
        Fraction(-3, 7),
        Fraction(-1, 7),
        Fraction(65, 112),
    )
    assert ledger.y_discriminant == Fraction(199, 196)
    assert ledger.y_discriminant_inner == Fraction(-199, 784)
    assert ledger.inner_as_quadratic_in_square_ratio == Fraction(-199, 784)
    assert ledger.inner_square_ratio_discriminant == Fraction(325, 256)
    assert ledger.pythagorean_recovery_square == Fraction(25, 16)
    assert ledger.new_curve_factor == Fraction(13, 16)
    assert ledger.slope_x_is_pythagorean
    assert not ledger.new_curve_factor_is_square


def test_sum_ab_new_curve_mod3_residue_summary_only_leaves_boundary_classes() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_new_curve_residue_summary,
    )

    summary = sum_ab_new_curve_residue_summary(3)

    assert summary.modulus == 3
    assert summary.primitive_classes == 8
    assert summary.square_classes == 4
    assert summary.boundary_square_classes == 4
    assert summary.nonboundary_square_classes == 0
    assert summary.boundary_examples == ((1, 1, 1), (1, 2, 1), (2, 1, 1))
    assert summary.nonboundary_examples == ()


def test_sum_ab_new_curve_z_reduction_tracks_two_square_conditions() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_new_curve_z_reduction,
    )

    reduction = sum_ab_new_curve_z_reduction(Fraction(3, 2))

    assert reduction.parameter_t == Fraction(3, 2)
    assert reduction.z_value == Fraction(5, 6)
    assert reduction.original_quartic_value == Fraction(509, 16)
    assert reduction.scaled_quartic_value == Fraction(509, 36)
    assert reduction.z_recovery_square == Fraction(169, 36)
    assert reduction.new_curve_square == Fraction(509, 36)
    assert reduction.identity_holds
    assert reduction.z_recovery_is_square
    assert not reduction.new_curve_is_square

    boundary = sum_ab_new_curve_z_reduction(Fraction(1))

    assert boundary.z_value == 0
    assert boundary.z_recovery_square == 4
    assert boundary.new_curve_square == 4
    assert boundary.z_recovery_is_square
    assert boundary.new_curve_is_square


def test_sum_ab_z_lemma_centerline_bridge_matches_quartic() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_z_lemma_centerline_bridge,
    )

    bridge = sum_ab_z_lemma_centerline_bridge(Fraction(3, 5))

    assert bridge.parameter == Fraction(3, 5)
    assert bridge.z_value == Fraction(15, 4)
    assert bridge.denominator_square == Fraction(256, 625)
    assert bridge.remaining_quartic == Fraction(6676, 625)
    assert bridge.centerline_parameter == Fraction(-3, 5)
    assert bridge.centerline_quartic == bridge.remaining_quartic
    assert bridge.scaled_second_square == Fraction(1669, 16)
    assert bridge.identity_holds
    assert not bridge.remaining_quartic_is_square

    boundary = sum_ab_z_lemma_centerline_bridge(Fraction(0))

    assert boundary.z_value == 0
    assert boundary.remaining_quartic == 1
    assert boundary.centerline_quartic == 1
    assert boundary.remaining_quartic_is_square


def test_sum_ab_k_discriminant_quartic_completion_links_centerline() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_k_discriminant_quartic_completion,
    )

    completion = sum_ab_k_discriminant_quartic_completion(
        Fraction(3, 5),
        Fraction(4, 9),
    )

    assert completion.parameter == Fraction(3, 5)
    assert completion.square_ratio == Fraction(4, 9)
    assert completion.centerline_quartic == Fraction(2836, 625)
    assert completion.remaining_quartic == Fraction(20176, 50625)
    assert completion.linear_square_term == Fraction(512, 5625)
    assert completion.positive_square_term == Fraction(336, 125)
    assert completion.left_side == completion.right_side
    assert completion.identity_holds
    assert completion.positive_remainder == Fraction(112896, 15625)


def test_sum_ab_k_square_candidate_y_discriminant_separates_layers() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_k_square_candidate_y_discriminant,
    )

    candidate = sum_ab_k_square_candidate_y_discriminant(
        Fraction(1, 2),
        Fraction(36, 25),
    )

    assert candidate.parameter == Fraction(1, 2)
    assert candidate.slope_x == Fraction(3, 4)
    assert candidate.square_ratio == Fraction(36, 25)
    assert candidate.square_ratio_is_square
    assert candidate.remaining_quartic == Fraction(9409, 2500)
    assert candidate.remaining_quartic_is_square
    assert candidate.y_discriminant == Fraction(10179, 2500)
    assert not candidate.y_discriminant_is_square


def test_sum_ab_k_square_y_discriminant_factorization_splits_layer3() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_k_square_y_discriminant_factorization,
    )

    factorization = sum_ab_k_square_y_discriminant_factorization(
        Fraction(1, 2),
        Fraction(6, 5),
    )

    assert factorization.parameter == Fraction(1, 2)
    assert factorization.slope_x == Fraction(3, 4)
    assert factorization.square_ratio_root == Fraction(6, 5)
    assert factorization.square_ratio == Fraction(36, 25)
    assert factorization.minus_factor == Fraction(-39, 100)
    assert factorization.plus_factor == Fraction(261, 100)
    assert factorization.y_discriminant == Fraction(10179, 2500)
    assert factorization.factorization_holds
    assert factorization.shared_factor_discriminant == Fraction(13, 16)
    assert not factorization.shared_factor_discriminant_is_square

    centerline = sum_ab_k_square_y_discriminant_factorization(
        Fraction(3, 5),
        Fraction(1),
    )

    assert centerline.minus_factor == -Fraction(4, 25)
    assert centerline.plus_factor == Fraction(64, 25)
    assert centerline.y_discriminant == Fraction(256, 225)
    assert centerline.factorization_holds


def test_sum_ab_same_orientation_both_pass_residue_summary_tracks_mod3_boundary() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_same_orientation_both_pass_residue_summary,
    )

    mod3 = sum_ab_same_orientation_both_pass_residue_summary(3)

    assert mod3.modulus == 3
    assert mod3.noncenter_survivor_count_by_orientation == {"odd": 0, "even": 0}
    assert mod3.p_equals_q_count_by_orientation == {"odd": 32, "even": 32}
    assert mod3.noncenter_examples_by_orientation == {"odd": (), "even": ()}

    mod9 = sum_ab_same_orientation_both_pass_residue_summary(9)

    assert mod9.noncenter_survivor_count_by_orientation == {
        "odd": 1728,
        "even": 1728,
    }
    assert mod9.noncenter_examples_by_orientation["odd"][:2] == (
        (0, 1, 1, 3, 4, 0, 3),
        (0, 1, 1, 6, 7, 0, 6),
    )


def test_sum_ab_same_orientation_both_pass_lift_summary_tracks_3adic_survivors() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_same_orientation_both_pass_lift_summary,
    )

    odd_lift = sum_ab_same_orientation_both_pass_lift_summary(
        modulus=9,
        orientation="odd",
        residue=(0, 1, 1, 3),
        prime=3,
    )

    assert odd_lift.next_modulus == 27
    assert odd_lift.lift_count == 81
    assert odd_lift.diff_valuation_counts == {1: 81}
    assert odd_lift.examples[:2] == (
        (0, 1, 1, 3, 13, 0, 21),
        (0, 1, 1, 12, 22, 0, 3),
    )

    even_lift = sum_ab_same_orientation_both_pass_lift_summary(
        modulus=9,
        orientation="even",
        residue=(1, 1, 1, 2),
        prime=3,
    )

    assert even_lift.next_modulus == 27
    assert even_lift.lift_count == 81
    assert even_lift.diff_valuation_counts == {1: 81}
    assert even_lift.examples[0] == (1, 1, 1, 2, 13, 0, 21)


def test_sum_ab_same_orientation_difference_factor_valuation_summary_splits_branches() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_same_orientation_difference_factor_valuation_summary,
    )

    odd_summary = sum_ab_same_orientation_difference_factor_valuation_summary(
        modulus=27,
        orientation="odd",
        prime=3,
    )

    assert odd_summary.total_survivors == 124416
    assert odd_summary.pattern_counts == {
        (0, 1, 1): 46656,
        (0, 2, 2): 15552,
        (1, 0, 1): 46656,
        (2, 0, 2): 15552,
    }
    assert odd_summary.examples[(1, 0, 1)] == (
        0,
        1,
        1,
        3,
        13,
        0,
        21,
        3,
        1,
    )

    even_summary = sum_ab_same_orientation_difference_factor_valuation_summary(
        modulus=27,
        orientation="even",
        prime=3,
    )

    assert even_summary.pattern_counts == odd_summary.pattern_counts
    assert even_summary.examples[(0, 1, 1)] == (
        1,
        1,
        1,
        4,
        8,
        0,
        24,
        5,
        -3,
    )


def test_sum_ab_same_orientation_combined_valuation_summary_shows_many_local_patterns() -> None:
    from rational_distance.concordant.rational_ratio import (
        sum_ab_same_orientation_combined_valuation_summary,
    )

    odd_summary = sum_ab_same_orientation_combined_valuation_summary(
        modulus=27,
        orientation="odd",
        prime=3,
    )

    assert odd_summary.total_survivors == 124416
    assert odd_summary.pattern_count == 49
    assert odd_summary.top_patterns[:2] == (
        ((1, 0, 1, 0, 0, 0, 1, 1), 23328),
        ((0, 1, 0, 1, 0, 0, 1, 1), 23328),
    )

    even_summary = sum_ab_same_orientation_combined_valuation_summary(
        modulus=27,
        orientation="even",
        prime=3,
    )

    assert even_summary.total_survivors == 124416
    assert even_summary.pattern_count == 45
    assert even_summary.top_patterns[:2] == (
        ((1, 0, 0, 1, 0, 0, 1, 1), 23328),
        ((0, 1, 1, 0, 0, 0, 1, 1), 23328),
    )
    assert even_summary.zero_offset_pattern_count == 4


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

    assert ledger.lambda_numerator == 6
    assert ledger.lambda_denominator == 1
    assert ledger.target == Fraction(5)
    assert ledger.discriminant == Fraction(1)
    assert ledger.discriminant_numerator == 1
    assert ledger.discriminant_denominator == 1
    assert ledger.discriminant_is_square
    assert ledger.discriminant_squareclass == 1
    assert ledger.discriminant_integer_squareclass == 1
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

    assert ledger.lambda_numerator == 3
    assert ledger.lambda_denominator == 2
    assert ledger.target == Fraction(5, 2)
    assert ledger.discriminant == Fraction(49, 4)
    assert ledger.discriminant_numerator == 49
    assert ledger.discriminant_denominator == 4
    assert ledger.discriminant_is_square
    assert ledger.discriminant_squareclass == 1
    assert ledger.discriminant_integer_squareclass == 1
    assert [(row.r, row.unit_squareclass, row.lambda_squareclass) for row in ledger.roots] == [
        (Fraction(3), 10, 5),
    ]
    assert ledger.true_roots == ()
    assert ledger.branch_closed
