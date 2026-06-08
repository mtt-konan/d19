from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


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
