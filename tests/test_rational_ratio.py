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


def test_reciprocal_orbit_sum_ab_roots_are_not_true_members_for_rational_lambda() -> None:
    from rational_distance.concordant.rational_ratio import (
        reciprocal_sum_ab_roots,
        true_reciprocal_sum_ab_roots,
    )

    lam = Fraction(3, 4)

    assert reciprocal_sum_ab_roots(lam) == (Fraction(1), Fraction(3, 4))
    assert true_reciprocal_sum_ab_roots(lam) == ()


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


def test_sum_ab_product_square_conditions_do_not_imply_membership() -> None:
    from rational_distance.concordant.rational_ratio import (
        REL_SUM_AB,
        closure_product_identity_terms,
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


def test_sum_ab_slope_pair_translates_to_rational_ratio_membership() -> None:
    from rational_distance.concordant.rational_ratio import (
        is_pythagorean_leg_ratio,
        sum_ab_point_from_slopes,
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


def test_scan_sum_ab_slope_pairs_finds_no_small_true_hits() -> None:
    from rational_distance.concordant.rational_ratio import scan_sum_ab_slope_pairs

    slopes = (Fraction(3, 4), Fraction(4, 3), Fraction(5, 12), Fraction(12, 5))

    assert scan_sum_ab_slope_pairs(slopes, include_false_members=False) == ()


def test_pythagorean_leg_ratios_generate_bounded_slope_pool() -> None:
    from rational_distance.concordant.rational_ratio import pythagorean_leg_ratios

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
    from rational_distance.concordant.rational_ratio import reciprocal_closure_roots

    sum_diff_roots = reciprocal_closure_roots(Fraction(6), "sum=|A-B|")
    diff_ab_roots = reciprocal_closure_roots(Fraction(3, 2), "diff=A+B")

    assert [(root.r, root.true_member) for root in sum_diff_roots] == [
        (Fraction(2), False),
        (Fraction(3), False),
    ]
    assert [(root.r, root.true_member) for root in diff_ab_roots] == [
        (Fraction(3), False),
    ]
