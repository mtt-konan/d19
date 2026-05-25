"""Helpers for analyzing half-points of concordant-N points."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import isqrt


@dataclass(frozen=True)
class HalfPointAnalysis:
    x: int
    y: int
    signature: tuple[int, int, int]


def _square_root_or_raise(value: int) -> int:
    root = isqrt(value)
    if root * root != value:
        raise ValueError(f"{value} is not a square")
    return root


def squarefree_part(n: int) -> int:
    sign = -1 if n < 0 else 1
    remainder = abs(n)
    out = 1
    factor = 2
    while factor * factor <= remainder:
        exponent = 0
        while remainder % factor == 0:
            remainder //= factor
            exponent += 1
        if exponent % 2 == 1:
            out *= factor
        factor += 1 if factor == 2 else 2
    if remainder > 1:
        out *= remainder
    return sign * out


def _double_point(A: int, B: int, x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    a2 = A * A + B * B
    a4 = A * A * B * B
    slope = Fraction(3 * x * x + 2 * a2 * x + a4, 2 * y)
    x2 = slope * slope - a2 - 2 * x
    y2 = -y + slope * (x - x2)
    return x2, y2


def enumerate_half_points_for_concordant_N(A: int, B: int, N: int) -> list[HalfPointAnalysis]:
    r1 = N
    r2 = _square_root_or_raise(N * N + A * A)
    r3 = _square_root_or_raise(N * N + B * B)
    target = (Fraction(N * N), Fraction(N * r2 * r3))

    halves: dict[tuple[int, int], HalfPointAnalysis] = {}
    for s1, s2, s3 in product((1, -1), repeat=3):
        u1, u2, u3 = s1 * r1, s2 * r2, s3 * r3
        x = r1 * r1 + u1 * u2 + u1 * u3 + u2 * u3
        y = (u1 + u2) * (u1 + u3) * (u2 + u3)
        doubled = _double_point(A, B, Fraction(x), Fraction(y))
        if doubled == target or doubled == (target[0], -target[1]):
            halves[(x, y)] = HalfPointAnalysis(
                x=x,
                y=y,
                signature=(
                    squarefree_part(x),
                    squarefree_part(x + A * A),
                    squarefree_part(x + B * B),
                ),
            )
    return sorted(halves.values(), key=lambda item: (abs(item.x), abs(item.y), item.x, item.y))
