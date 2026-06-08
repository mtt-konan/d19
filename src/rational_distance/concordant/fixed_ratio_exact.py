"""Exact fixed-ratio ``A = kB`` concordant-N analysis.

Unlike :mod:`fixed_ratio_sieve`, this module never treats arbitrary residues as
candidate ``N`` values. It calls the exact factor-decomposition concordant
search, then normalises every true integer ``N`` to the ratio ``N / B``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from rational_distance.concordant.factor_search import find_concordant_by_factorization

REL_SUM_AB = "sum=A+B"
REL_SUM_DIFF = "sum=|A-B|"
REL_DIFF_AB = "diff=A+B"
REL_DIFF_DIFF = "diff=|A-B|"


@dataclass(frozen=True, order=True)
class FixedRatioHit:
    """A ratio-level full-plane closure hit."""

    r1: Fraction
    r2: Fraction
    relation: str
    centerline: bool


@dataclass(frozen=True)
class FixedRatioRatioSummary:
    """Exact ratio summary for one fixed ``A = kB`` branch up to ``B <= max_b``."""

    k: int
    max_b: int
    ratios: tuple[Fraction, ...]
    ratio_count: int
    b_with_n_count: int
    total_n_count: int
    noncenter_hits: tuple[FixedRatioHit, ...]
    centerline_hits: tuple[FixedRatioHit, ...]


def _validate_inputs(k: int, b: int | None = None, max_b: int | None = None) -> None:
    if k < 1:
        raise ValueError("k must be a positive integer")
    if b is not None and b < 1:
        raise ValueError("b must be a positive integer")
    if max_b is not None and max_b < 1:
        raise ValueError("max_b must be a positive integer")


def fixed_ratio_concordant_n(k: int, b: int) -> list[int]:
    """Return every true concordant ``N`` for ``(B, A) = (b, kb)``."""
    _validate_inputs(k, b=b)
    if k == 1:
        return []
    return find_concordant_by_factorization(b, k * b)


def fixed_ratio_ratios_for_b(k: int, b: int) -> tuple[Fraction, ...]:
    """Return sorted distinct true ratios ``N / B`` for one ``B``."""
    return tuple(sorted({Fraction(n, b) for n in fixed_ratio_concordant_n(k, b)}))


def _targets_for_k(k: int) -> tuple[tuple[Fraction, str], ...]:
    targets: list[tuple[Fraction, str]] = [(Fraction(k + 1), REL_SUM_AB)]
    if k != 1:
        targets.append((Fraction(abs(k - 1)), REL_SUM_DIFF))
    return tuple(targets)


def find_fixed_ratio_ratio_hits(
    k: int,
    ratios: tuple[Fraction, ...],
    *,
    include_centerline: bool = False,
) -> tuple[FixedRatioHit, ...]:
    """Check full-plane closure after dividing all lengths by ``B``.

    For ``A = kB``, the four integer closure relations become:

        r1 + r2 = k + 1
        r1 + r2 = |k - 1|
        |r1-r2| = k + 1
        |r1-r2| = |k - 1|

    where ``r_i = N_i / B``.
    """
    _validate_inputs(k)
    sorted_ratios = tuple(sorted(set(ratios)))
    hits: list[FixedRatioHit] = []
    sum_targets = _targets_for_k(k)
    diff_targets: list[tuple[Fraction, str]] = [(Fraction(k + 1), REL_DIFF_AB)]
    if k != 1:
        diff_targets.append((Fraction(abs(k - 1)), REL_DIFF_DIFF))

    for i, r1 in enumerate(sorted_ratios):
        for j in range(i, len(sorted_ratios)):
            r2 = sorted_ratios[j]
            centerline = r1 == r2
            if centerline and not include_centerline:
                continue
            for target, relation in sum_targets:
                if r1 + r2 == target:
                    hits.append(FixedRatioHit(r1, r2, relation, centerline))
            if centerline:
                continue
            diff = abs(r2 - r1)
            for target, relation in diff_targets:
                if diff == target:
                    hits.append(FixedRatioHit(r1, r2, relation, False))
    return tuple(sorted(hits))


def collect_fixed_ratio_ratios(k: int, max_b: int) -> FixedRatioRatioSummary:
    """Collect exact ``N/B`` ratios for ``A = kB`` over ``1 <= B <= max_b``."""
    _validate_inputs(k, max_b=max_b)
    ratios: set[Fraction] = set()
    b_with_n = 0
    total_n = 0
    for b in range(1, max_b + 1):
        ns = fixed_ratio_concordant_n(k, b)
        if ns:
            b_with_n += 1
            total_n += len(ns)
            ratios.update(Fraction(n, b) for n in ns)

    ratio_tuple = tuple(sorted(ratios))
    return FixedRatioRatioSummary(
        k=k,
        max_b=max_b,
        ratios=ratio_tuple,
        ratio_count=len(ratio_tuple),
        b_with_n_count=b_with_n,
        total_n_count=total_n,
        noncenter_hits=find_fixed_ratio_ratio_hits(k, ratio_tuple),
        centerline_hits=find_fixed_ratio_ratio_hits(k, ratio_tuple, include_centerline=True),
    )


__all__ = [
    "FixedRatioHit",
    "FixedRatioRatioSummary",
    "collect_fixed_ratio_ratios",
    "find_fixed_ratio_ratio_hits",
    "fixed_ratio_concordant_n",
    "fixed_ratio_ratios_for_b",
]
