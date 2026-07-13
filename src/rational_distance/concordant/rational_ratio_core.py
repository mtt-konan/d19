"""Small relation-level core for the partner-edge reciprocal audit.

The larger fixed-ratio research implementation lives in
``concordant.archive.rational_ratio``.  This module keeps the runtime audit
independent of that experimental diagnostic surface and of SymPy.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

REL_SUM_AB = "sum=A+B"
REL_SUM_DIFF = "sum=|A-B|"
REL_DIFF_AB = "diff=A+B"
REL_DIFF_DIFF = "diff=|A-B|"


@dataclass(frozen=True)
class FullPlaneTrueClosureRelation:
    """Classify one full-plane relation and its true ``R_lambda`` branch."""

    lambda_ratio: Fraction
    relation: str
    target: Fraction
    r: Fraction
    s: Fraction
    closure_value: Fraction
    closes_relation: bool
    closes_sum_ab: bool
    closes_sum_diff: bool
    closes_diff_ab: bool
    closes_diff_diff: bool
    r_true_member: bool
    s_true_member: bool
    both_true_members: bool
    reciprocal_pair: bool
    centerline: bool
    branch: str


def _as_fraction(value: Fraction | int) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _validate_positive(name: str, value: Fraction) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _rational_sqrt(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator == value.numerator and denominator * denominator == value.denominator:
        return Fraction(numerator, denominator)
    return None


def is_rational_ratio_member(lambda_ratio: Fraction | int, r: Fraction | int) -> bool:
    """Return whether ``r`` satisfies both defining ``R_lambda`` squares."""
    lam = _as_fraction(lambda_ratio)
    ratio = _as_fraction(r)
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", ratio)
    return _rational_sqrt(ratio * ratio + 1) is not None and _rational_sqrt(
        ratio * ratio + lam * lam
    ) is not None


def reciprocal_ratio(lambda_ratio: Fraction | int, r: Fraction | int) -> Fraction:
    """Return the reciprocal-orbit mate ``lambda / r``."""
    lam = _as_fraction(lambda_ratio)
    ratio = _as_fraction(r)
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", ratio)
    return lam / ratio


def _full_plane_relation_target(lambda_ratio: Fraction, relation: str) -> Fraction:
    if relation in (REL_SUM_AB, REL_DIFF_AB):
        return lambda_ratio + 1
    if relation in (REL_SUM_DIFF, REL_DIFF_DIFF):
        target = abs(lambda_ratio - 1)
        if target == 0:
            raise ValueError("|A-B| target is zero when lambda_ratio = 1")
        return target
    raise ValueError(f"unknown relation: {relation}")


def full_plane_true_closure_relation(
    *,
    lambda_ratio: Fraction | int,
    r: Fraction | int,
    s: Fraction | int,
    relation: str,
) -> FullPlaneTrueClosureRelation:
    """Classify one full-plane closure pair for the reciprocal audit."""
    lam = _as_fraction(lambda_ratio)
    root1, root2 = sorted((_as_fraction(r), _as_fraction(s)))
    _validate_positive("lambda_ratio", lam)
    _validate_positive("r", root1)
    _validate_positive("s", root2)

    target = _full_plane_relation_target(lam, relation)
    sum_value = root1 + root2
    diff_value = abs(root2 - root1)
    closure_value = sum_value if relation.startswith("sum=") else diff_value
    diff_target = abs(lam - 1)
    closes_sum_ab = sum_value == lam + 1
    closes_sum_diff = diff_target != 0 and sum_value == diff_target
    closes_diff_ab = diff_value == lam + 1
    closes_diff_diff = diff_target != 0 and diff_value == diff_target
    closes_relation = closure_value == target

    r_true = is_rational_ratio_member(lam, root1)
    s_true = is_rational_ratio_member(lam, root2)
    both_true = r_true and s_true
    reciprocal_pair = root1 * root2 == lam
    centerline = root1 == root2
    if not closes_relation:
        branch = "not-closure"
    elif centerline and not both_true:
        branch = "false-centerline"
    elif centerline:
        branch = "true-centerline"
    elif reciprocal_pair and both_true:
        branch = "true-reciprocal"
    elif reciprocal_pair:
        branch = "false-reciprocal"
    elif both_true:
        branch = "true-nonreciprocal"
    else:
        branch = "false-residual"

    return FullPlaneTrueClosureRelation(
        lambda_ratio=lam,
        relation=relation,
        target=target,
        r=root1,
        s=root2,
        closure_value=closure_value,
        closes_relation=closes_relation,
        closes_sum_ab=closes_sum_ab,
        closes_sum_diff=closes_sum_diff,
        closes_diff_ab=closes_diff_ab,
        closes_diff_diff=closes_diff_diff,
        r_true_member=r_true,
        s_true_member=s_true,
        both_true_members=both_true,
        reciprocal_pair=reciprocal_pair,
        centerline=centerline,
        branch=branch,
    )


__all__ = [
    "REL_DIFF_AB",
    "REL_DIFF_DIFF",
    "REL_SUM_AB",
    "REL_SUM_DIFF",
    "FullPlaneTrueClosureRelation",
    "full_plane_true_closure_relation",
    "is_rational_ratio_member",
    "reciprocal_ratio",
]
