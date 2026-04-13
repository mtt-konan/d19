"""Rational arithmetic helpers."""

from __future__ import annotations

from fractions import Fraction
from math import gcd, isqrt


def rational_sqrt(f: Fraction) -> Fraction | None:
    """Return √f as a Fraction if f is a perfect rational square, else None.

    Strategy: write f = p/q in lowest terms.
    √(p/q) ∈ ℚ  ⟺  both p and q are perfect integer squares.
    """
    if f < 0:
        return None
    if f == 0:
        return Fraction(0)
    p, q = f.numerator, f.denominator
    sp, sq = isqrt(p), isqrt(q)
    if sp * sp == p and sq * sq == q:
        return Fraction(sp, sq)
    return None


def is_rational_sqrt(f: Fraction) -> bool:
    return rational_sqrt(f) is not None


def primitive_pythagorean_triples(max_m: int) -> list[tuple[int, int, int]]:
    """Yield primitive Pythagorean triples (a, b, c) with a²+b²=c², a<b<c.

    Uses the standard parametrization:
        m > n > 0, gcd(m,n)=1, m−n odd
        a = m²−n²,  b = 2mn,  c = m²+n²
    Includes both (a,b,c) and (b,a,c) so callers get all orientations.
    """
    triples: list[tuple[int, int, int]] = []
    for m in range(2, max_m + 1):
        for n in range(1, m):
            if (m - n) % 2 == 0:
                continue
            if gcd(m, n) != 1:
                continue
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            triples.append((a, b, c))
            triples.append((b, a, c))  # swapped orientation
    return triples


def scale_triple(a: int, b: int, c: int, k: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    """Scale a primitive triple by rational k: (ka, kb, kc)."""
    return Fraction(k * a), Fraction(k * b), Fraction(k * c)
