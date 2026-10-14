"""Exact structural certificates for the square/rectangle comparison."""

from fractions import Fraction
from itertools import product
from math import isqrt

import pytest
import sympy as sp

A, B, C, D, L, M, W, T = sp.symbols("a b c d L M w t")
NORM = A**2 + B**2
Q, R = A**2 - B**2, C**2 - D**2
FLAG = A**2 + B**2 - C**2 - D**2
RECTANGLE = (
    M**2 * (Q + R) ** 2
    + L**2 * (Q - R) ** 2
    - 8 * L**2 * M**2 * NORM
    + 4 * L**2 * M**2 * (L**2 + M**2)
)
RATIO = T**2 * (Q + R) ** 2 + (Q - R) ** 2 - 8 * T**2 * NORM * W**2 + 4 * T**2 * (1 + T**2) * W**4
SQUARE = Q**2 + R**2 - 4 * NORM * W**2 + 4 * W**4


@pytest.mark.parametrize(("i", "j", "distance"), [(0, 0, A), (1, 1, B), (0, 1, C), (1, 0, D)])
def test_each_rectangle_distance_has_exact_reverse_lift(i, j, distance):
    x = L / 2 + (Q + R) / (4 * L)
    y = M / 2 + (Q - R) / (4 * M)
    residual = 16 * L**2 * M**2 * ((x - i * L) ** 2 + (y - j * M) ** 2 - distance**2)
    correction = 0 if (i, j) in ((0, 0), (1, 1)) else 8 * L**2 * M**2 * FLAG
    assert sp.expand(residual - RECTANGLE - correction) == 0


def test_shape_mixed_term_and_individual_side_lifts():
    expanded = (
        (L**2 + M**2) * (Q**2 + R**2)
        + 2 * (M**2 - L**2) * Q * R
        - 8 * L**2 * M**2 * NORM
        + 4 * L**2 * M**2 * (L**2 + M**2)
    )
    assert sp.expand(RECTANGLE - expanded) == 0
    mean = (L**2 + M**2) / 2
    epsilon = (L**2 - M**2) / (L**2 + M**2)
    shape = Q**2 + R**2 - 2 * epsilon * Q * R
    shape -= 4 * mean * (1 - epsilon**2) * (NORM - mean)
    assert sp.factor(RECTANGLE - (L**2 + M**2) * shape) == 0
    assert sp.factor(mean * (1 + epsilon) - L**2) == 0
    assert sp.factor(mean * (1 - epsilon) - M**2) == 0
    assert sp.factor(1 - epsilon**2 - (2 * L * M / (L**2 + M**2)) ** 2) == 0


def test_saturation_removes_only_the_extraneous_side_factor():
    assert sp.expand(RECTANGLE.subs({L: W, M: T * W}) - W**2 * RATIO) == 0
    boundary = T**2 * (Q + R) ** 2 + (Q - R) ** 2
    assert sp.expand(RATIO.subs(W, 0) - boundary) == 0
    assert boundary != 0


def test_exact_deformation_identity():
    correction = (T**2 - 1) * (4 * T**2 * W**4 - (Q - R) ** 2)
    assert sp.expand(RATIO - 2 * T**2 * SQUARE - correction) == 0


@pytest.mark.parametrize("tau", [1, 4])
def test_entire_residue_class_has_square_model_and_unit_norm(tau):
    assert sp.Poly(RATIO.subs(T, tau) - 2 * SQUARE, A, B, C, D, W, modulus=5).is_zero
    count = 0
    for a, b, c, d, w in product(range(5), repeat=5):
        if not any((a, b, c, d, w)):
            continue
        norm = a * a + b * b
        if (norm - c * c - d * d) % 5:
            continue
        q, r = a * a - b * b, c * c - d * d
        f = tau * tau * (q + r) ** 2 + (q - r) ** 2
        f -= 8 * tau * tau * norm * w * w
        f += 4 * tau * tau * (1 + tau * tau) * w**4
        if f % 5:
            continue
        count += 1
        assert norm % 5 != 0
    assert count == 96


@pytest.mark.parametrize("tau", [1, 4])
@pytest.mark.parametrize(("c", "s"), [(0, 1), (0, 4), (1, 0), (4, 0)])
def test_every_integral_shape_rotation_residue_has_hensel_seed(tau, c, s):
    rotated = RATIO.subs({T: tau, C: c * A - s * B, D: s * A + c * B, W: 1})
    assert int(rotated.subs({A: 0, B: 2})) % 5 == 0
    assert int(sp.diff(rotated, B).subs({A: 0, B: 2})) % 5 == 1


def test_other_unit_shape_has_different_zero_norm_congruence():
    zero_norm_relations = sp.groebner([A**2 + B**2, C**2 + D**2], B, D, A, C, W, modulus=5)
    _, remainder = zero_norm_relations.reduce(sp.expand(RATIO.subs(T, 2) - 4 * A**2 * C**2))
    assert remainder == 0


@pytest.mark.parametrize("height", [7, 25])
def test_strict_rational_rectangles_with_nonintegral_rotation(height):
    width, x, y = 24, 12, 16
    distances = (20, 15, 15, 20)
    vertices = ((0, 0), (width, height), (0, height), (width, 0))
    for (i, j), distance in zip(vertices, distances, strict=True):
        assert (x - i) ** 2 + (y - j) ** 2 == distance**2
    a, b, c, d = map(Fraction, distances)
    norm = a * a + b * b
    assert norm == c * c + d * d == 625
    rc, rs = (a * c + b * d) / norm, (a * d - b * c) / norm
    assert (rc, rs) == (Fraction(24, 25), Fraction(7, 25))
    assert rc * rc + rs * rs == 1
    assert rc * a - rs * b == c
    assert rs * a + rc * b == d
    assert rc.denominator % 5 == rs.denominator % 5 == 0
    point = {A: a, B: b, C: c, D: d, L: width, M: height}
    assert RECTANGLE.subs(point) == 0
    assert RATIO.subs({**point, T: sp.Rational(height, width), W: width}) == 0
    ratio = Fraction(height, width)
    assert ratio.numerator * pow(ratio.denominator, -1, 5) % 5 == (3 if height == 7 else 0)
    assert Fraction(x, width) == Fraction(1, 2)
    assert Fraction(y, width) == Fraction(2, 3)
    assert (0 < y < height) == (height == 25)


def test_fixed_distance_tuple_requires_irrational_square_side():
    norm, q, r = 625, 175, -175
    discriminant = norm**2 - q**2 - r**2
    assert discriminant == 25**2 * 527
    assert 527 == 17 * 31
    assert isqrt(discriminant) ** 2 != discriminant
    assert 0 < discriminant < norm**2
    v = sp.symbols("V")
    polynomial = v**2 - norm * v + sp.Rational(q**2 + r**2, 4)
    for sign in (-1, 1):
        root = (625 + sign * 25 * sp.sqrt(527)) / 2
        assert sp.simplify(polynomial.subs(v, root)) == 0
