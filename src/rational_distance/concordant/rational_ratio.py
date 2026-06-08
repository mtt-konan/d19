"""Rational fixed-ratio ``A / B = lambda`` identities.

This module is the proof-side analogue of :mod:`fixed_ratio_exact`.  It does
not generate integer candidates.  Instead it records exact ``Fraction``-level
identities that still make sense after replacing an integer ratio ``k`` by an
arbitrary positive rational ratio ``lambda``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

REL_SUM_AB = "sum=A+B"
REL_SUM_DIFF = "sum=|A-B|"
REL_DIFF_AB = "diff=A+B"
REL_DIFF_DIFF = "diff=|A-B|"


@dataclass(frozen=True, order=True)
class RationalRatioHit:
    """A ratio-level full-plane closure hit for rational ``A/B``."""

    r1: Fraction
    r2: Fraction
    relation: str
    centerline: bool


@dataclass(frozen=True)
class ProductIdentityTerms:
    """Terms in the ``p = rs`` product identity for a closure target."""

    lambda_ratio: Fraction
    target: Fraction
    product: Fraction
    a_term: Fraction
    b_term: Fraction
    b_minus_lambda_sq_a: Fraction


@dataclass(frozen=True)
class SquareRectangleTerms:
    """Four square-candidate corners after a closure linear relation."""

    lambda_ratio: Fraction
    target: Fraction
    mover: Fraction
    x: Fraction
    y: Fraction
    z: Fraction
    w: Fraction


@dataclass(frozen=True, order=True)
class ReciprocalClosureRoot:
    """A same-orbit closure root and whether it is a true ``R_lambda`` point."""

    r: Fraction
    relation: str
    true_member: bool


def _as_fraction(value: Fraction | int) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _validate_positive(name: str, value: Fraction) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _is_rational_square(value: Fraction) -> bool:
    if value < 0:
        return False
    num = isqrt(value.numerator)
    den = isqrt(value.denominator)
    return num * num == value.numerator and den * den == value.denominator


def _rational_sqrt(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    num = isqrt(value.numerator)
    den = isqrt(value.denominator)
    if num * num == value.numerator and den * den == value.denominator:
        return Fraction(num, den)
    return None


def is_rational_ratio_member(lambda_ratio: Fraction | int, r: Fraction | int) -> bool:
    """Return True iff ``r`` lies in ``R_lambda``.

    ``R_lambda`` is the set of positive rational ratios satisfying both:

        r^2 + 1        is a rational square
        r^2 + lambda^2 is a rational square
    """
    lam = _as_fraction(lambda_ratio)
    ratio = _as_fraction(r)
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", ratio)
    return _is_rational_square(ratio * ratio + 1) and _is_rational_square(
        ratio * ratio + lam * lam
    )


def reciprocal_ratio(lambda_ratio: Fraction | int, r: Fraction | int) -> Fraction:
    """Return the reciprocal-orbit mate ``lambda / r``."""
    lam = _as_fraction(lambda_ratio)
    ratio = _as_fraction(r)
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", ratio)
    return lam / ratio


def _targets(lambda_ratio: Fraction) -> tuple[tuple[Fraction, str], ...]:
    diff = abs(lambda_ratio - 1)
    targets: list[tuple[Fraction, str]] = [(lambda_ratio + 1, REL_SUM_AB)]
    if diff != 0:
        targets.append((diff, REL_SUM_DIFF))
    return tuple(targets)


def find_rational_ratio_hits(
    lambda_ratio: Fraction | int,
    ratios: tuple[Fraction, ...],
    *,
    include_centerline: bool = False,
) -> tuple[RationalRatioHit, ...]:
    """Check full-plane closure for an arbitrary rational ``A/B`` ratio."""
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    sorted_ratios = tuple(sorted(set(ratios)))
    hits: list[RationalRatioHit] = []

    sum_targets = _targets(lam)
    diff_targets: list[tuple[Fraction, str]] = [(lam + 1, REL_DIFF_AB)]
    diff = abs(lam - 1)
    if diff != 0:
        diff_targets.append((diff, REL_DIFF_DIFF))

    for i, r1 in enumerate(sorted_ratios):
        _validate_positive("r", r1)
        for j in range(i, len(sorted_ratios)):
            r2 = sorted_ratios[j]
            _validate_positive("r", r2)
            centerline = r1 == r2
            if centerline and not include_centerline:
                continue
            for target, relation in sum_targets:
                if r1 + r2 == target:
                    hits.append(RationalRatioHit(r1, r2, relation, centerline))
            if centerline:
                continue
            ratio_diff = abs(r2 - r1)
            for target, relation in diff_targets:
                if ratio_diff == target:
                    hits.append(RationalRatioHit(r1, r2, relation, False))
    return tuple(sorted(hits))


def reciprocal_sum_ab_roots(lambda_ratio: Fraction | int) -> tuple[Fraction, Fraction]:
    """Return roots forced by ``r + lambda/r = lambda + 1``.

    Algebraically the roots are always ``1`` and ``lambda``.  They need not be
    true ``R_lambda`` members; use :func:`true_reciprocal_sum_ab_roots` for that.
    """
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    return (Fraction(1), lam)


def true_reciprocal_sum_ab_roots(lambda_ratio: Fraction | int) -> tuple[Fraction, ...]:
    """Return the ``sum=A+B`` same-orbit roots that are true ``R_lambda`` points."""
    lam = _as_fraction(lambda_ratio)
    return tuple(r for r in reciprocal_sum_ab_roots(lam) if is_rational_ratio_member(lam, r))


def product_identity_terms(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    product: Fraction | int,
) -> ProductIdentityTerms:
    """Return the terms in the sum-closure product identity.

    For ``r+s=T`` and ``p=rs``:

        A_p = p^2 - 2p + T^2 + 1
        B_p = p^2 - 2lambda^2 p + lambda^2 T^2 + lambda^4

    and:

        B_p - lambda^2 A_p = (lambda^2 - 1)(lambda^2 - p^2)
    """
    lam = _as_fraction(lambda_ratio)
    t = _as_fraction(target)
    p = _as_fraction(product)
    _validate_positive("lambda_ratio", lam)
    if t <= 0:
        raise ValueError("target must be positive")

    lam_sq = lam * lam
    a_term = p * p - 2 * p + t * t + 1
    b_term = p * p - 2 * lam_sq * p + lam_sq * t * t + lam_sq * lam_sq
    return ProductIdentityTerms(
        lambda_ratio=lam,
        target=t,
        product=p,
        a_term=a_term,
        b_term=b_term,
        b_minus_lambda_sq_a=b_term - lam_sq * a_term,
    )


def closure_product_identity_terms(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    product: Fraction | int,
    relation: str,
) -> ProductIdentityTerms:
    """Return product-identity terms for a sum or difference closure relation."""
    lam = _as_fraction(lambda_ratio)
    t = _as_fraction(target)
    p = _as_fraction(product)
    _validate_positive("lambda_ratio", lam)
    if t <= 0:
        raise ValueError("target must be positive")

    if relation.startswith("sum="):
        sign = -1
    elif relation.startswith("diff="):
        sign = 1
    else:
        raise ValueError(f"unknown closure relation: {relation}")

    lam_sq = lam * lam
    a_term = p * p + sign * 2 * p + t * t + 1
    b_term = p * p + sign * 2 * lam_sq * p + lam_sq * t * t + lam_sq * lam_sq
    return ProductIdentityTerms(
        lambda_ratio=lam,
        target=t,
        product=p,
        a_term=a_term,
        b_term=b_term,
        b_minus_lambda_sq_a=b_term - lam_sq * a_term,
    )


def square_rectangle_terms(
    lambda_ratio: Fraction | int,
    target: Fraction | int,
    mover: Fraction | int,
) -> SquareRectangleTerms:
    """Return the four square-candidate corners from the wl113 rectangle model.

    The unified form is:

        (M-T)^2 + 4
        (M+T)^2 + 4
        (M-T)^2 + 4lambda^2
        (M+T)^2 + 4lambda^2

    For sum closure, ``M`` is ``q=s-r``.  For difference closure, ``M`` is
    ``L=r+s``.
    """
    lam = _as_fraction(lambda_ratio)
    t = _as_fraction(target)
    m = _as_fraction(mover)
    _validate_positive("lambda_ratio", lam)
    if t <= 0:
        raise ValueError("target must be positive")
    lam_sq = lam * lam
    left = m - t
    right = m + t
    return SquareRectangleTerms(
        lambda_ratio=lam,
        target=t,
        mover=m,
        x=left * left + 4,
        y=right * right + 4,
        z=left * left + 4 * lam_sq,
        w=right * right + 4 * lam_sq,
    )


def reciprocal_closure_roots(
    lambda_ratio: Fraction | int,
    relation: str,
) -> tuple[ReciprocalClosureRoot, ...]:
    """Return rational same-orbit roots for one closure relation.

    This intentionally separates "the quadratic has rational roots" from
    "those roots are true ``R_lambda`` points"; the distinction is the main
    pitfall when upgrading integer ``k`` proofs to rational ``lambda``.
    """
    lam = _as_fraction(lambda_ratio)
    _validate_positive("lambda_ratio", lam)
    roots: list[Fraction] = []
    if relation == REL_SUM_AB:
        roots = list(reciprocal_sum_ab_roots(lam))
    elif relation == REL_DIFF_DIFF:
        roots = [Fraction(1), lam]
    elif relation == REL_SUM_DIFF:
        target = abs(lam - 1)
        sqrt_disc = _rational_sqrt(target * target - 4 * lam)
        if sqrt_disc is not None:
            roots = [(target - sqrt_disc) / 2, (target + sqrt_disc) / 2]
    elif relation == REL_DIFF_AB:
        target = lam + 1
        sqrt_disc = _rational_sqrt(target * target + 4 * lam)
        if sqrt_disc is not None:
            roots = [(target - sqrt_disc) / 2, (target + sqrt_disc) / 2]
    else:
        raise ValueError(f"unknown relation: {relation}")

    out = [
        ReciprocalClosureRoot(
            r=root,
            relation=relation,
            true_member=is_rational_ratio_member(lam, root),
        )
        for root in sorted(set(roots))
        if root > 0
    ]
    return tuple(out)


__all__ = [
    "ProductIdentityTerms",
    "RationalRatioHit",
    "ReciprocalClosureRoot",
    "SquareRectangleTerms",
    "closure_product_identity_terms",
    "find_rational_ratio_hits",
    "is_rational_ratio_member",
    "product_identity_terms",
    "reciprocal_closure_roots",
    "reciprocal_ratio",
    "reciprocal_sum_ab_roots",
    "square_rectangle_terms",
    "true_reciprocal_sum_ab_roots",
]
