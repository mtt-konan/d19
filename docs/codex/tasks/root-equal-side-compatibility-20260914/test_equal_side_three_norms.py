"""Exact tests for the equal-side three-norm reformulation."""

from math import isqrt

import sympy as sp

a, b, c, d, R, q, r, h, V, w, e, f = sp.symbols("a b c d R q r h V w e f")


def test_square_side_quadratic_and_discriminant_factors():
    root_polynomial = sp.expand((4 * V**2 - 4 * R * V + q**2 + r**2).subs(V, (R + h) / 2))
    assert sp.expand(root_polynomial.subs(h**2, R**2 - q**2 - r**2)) == 0
    discriminant = R**2 - q**2 - r**2
    assert sp.expand((h**2 - discriminant).subs(h**2, discriminant)) == 0
    first = (2 * a * b) ** 2 - r**2 - (R**2 - q**2 - r**2)
    assert sp.expand(first.subs({R: a**2 + b**2, q: a**2 - b**2})) == 0
    second = (2 * c * d) ** 2 - q**2 - (R**2 - q**2 - r**2)
    assert sp.expand(second.subs({R: c**2 + d**2, r: c**2 - d**2})) == 0


def test_three_square_system_is_reversible():
    a2 = ((w + e) ** 2 + f**2) / 2
    b2 = ((w - e) ** 2 + f**2) / 2
    c2 = ((w + f) ** 2 + e**2) / 2
    d2 = ((w - f) ** 2 + e**2) / 2
    r_value = w**2 + e**2 + f**2
    assert sp.expand(a2 + b2 - r_value) == 0
    assert sp.expand(c2 + d2 - r_value) == 0
    assert sp.expand(a2 - b2 - 2 * w * e) == 0
    assert sp.expand(c2 - d2 - 2 * w * f) == 0
    assert sp.expand((2 * w * e) ** 2 + (2 * w * f) ** 2 - 4 * w**2 * (r_value - w**2)) == 0


def test_quadratic_roots_are_the_square_side_and_complementary_norm():
    polynomial = 4 * V**2 - 4 * (w**2 + e**2 + f**2) * V + 4 * w**2 * (e**2 + f**2)
    assert sp.factor(polynomial - 4 * (V - w**2) * (V - e**2 - f**2)) == 0


def test_primitive_parity_makes_the_other_root_a_2_adic_nonsquare():
    for e in range(1, 16, 2):
        for f in range(1, 16, 2):
            complement = e * e + f * f
            assert complement % 8 == 2


def test_nontrivial_discriminant_lift_can_fail_side_square():
    rv = 23426
    qv, rvv, hv = -20976, -3024, 9982
    assert 35**2 + 149**2 == 101**2 + 115**2 == rv
    assert qv == 35**2 - 149**2 and rvv == 101**2 - 115**2
    assert hv**2 == rv**2 - qv**2 - rvv**2
    candidates = ((rv + hv) // 2, (rv - hv) // 2)
    assert candidates == (16704, 6722)
    assert all(isqrt(candidate) ** 2 != candidate for candidate in candidates)


def test_rectangle_tuple_fails_first_equal_side_lift():
    rv, qv, rvv = 625, 175, -175
    discriminant = rv**2 - qv**2 - rvv**2
    assert discriminant == 625 * 527
    assert isqrt(discriminant) ** 2 != discriminant
    assert 527 == 17 * 31
