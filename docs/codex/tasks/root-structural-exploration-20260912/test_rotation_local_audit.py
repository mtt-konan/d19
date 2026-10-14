"""Exact certificates for the task-local full-lift 5-adic criterion."""

from fractions import Fraction
from itertools import product

import pytest
import sympy as sp

A, B, W, C, S, T = sp.symbols("a b w C S t")
DC = C * A - S * B
DD = S * A + C * B
NORM = A**2 + B**2
Q = A**2 - B**2
R = DC**2 - DD**2
FULL = sp.expand(Q**2 + R**2 - 4 * NORM * W**2 + 4 * W**4)
INTEGER_MODEL = sp.Poly(
    sp.expand(FULL.subs({C: sp.Rational(3, 5), S: sp.Rational(4, 5)}) * 625 / 2),
    A,
    B,
    W,
    domain=sp.ZZ,
)


def valuation(n, p):
    """Finite valuation, with zero excluded from these fixed certificates."""
    assert n != 0
    result = 0
    while n % p == 0:
        n //= p
        result += 1
    return result


def unit_residue(value, p):
    v = valuation(value.numerator, p) - valuation(value.denominator, p)
    unit = value / Fraction(p) ** v
    return v, unit.numerator * pow(unit.denominator, -1, p) % p


@pytest.mark.parametrize(("i", "j", "distance"), [(0, 0, A), (1, 1, B), (0, 1, DC), (1, 0, DD)])
def test_each_original_distance_lifts(i, j, distance):
    x = sp.Rational(1, 2) + (Q + R) / (4 * W**2)
    y = sp.Rational(1, 2) + (Q - R) / (4 * W**2)
    residual = sp.expand(8 * W**4 * ((x - i) ** 2 + (y - j) ** 2 - distance**2 / W**2) - FULL)
    expected = 0 if (i, j) in ((0, 0), (1, 1)) else -4 * W**2 * NORM * (C**2 + S**2 - 1)
    assert sp.expand(residual - expected) == 0


def test_integer_model_has_correct_scale_coefficient():
    numerator = (3 * A - 4 * B) ** 2 - (4 * A + 3 * B) ** 2
    correct = 625 * Q**2 + numerator**2 - 2500 * NORM * W**2 + 2500 * W**4
    assert sp.expand(2 * INTEGER_MODEL.as_expr() - correct) == 0
    assert INTEGER_MODEL.coeff_monomial(A**2 * W**2) == -1250
    assert INTEGER_MODEL.coeff_monomial(B**2 * W**2) == -1250
    assert INTEGER_MODEL.coeff_monomial(W**4) == 1250


def test_five_adic_change_and_fermat_reduction():
    new_b = 2 * A + 5 * T
    new_c = -A - 4 * T
    new_d = 2 * A + 3 * T
    assert sp.expand(A**2 + new_b**2 - new_c**2 - new_d**2) == 0
    assert sp.expand((3 * A - 4 * new_b) / 5 - new_c) == 0
    assert sp.expand((4 * A + 3 * new_b) / 5 - new_d) == 0
    assert sp.Matrix([[1, 0, 0], [2, 5, 0], [0, 0, 1]]).det() == 5
    new_model = sp.Poly(
        sp.expand(INTEGER_MODEL.as_expr().subs(B, new_b) / 625), A, T, W, domain=sp.ZZ
    )
    fermat = 2 * (A**4 + (A - T) ** 4 + W**4)
    assert sp.Poly(new_model.as_expr() - fermat, A, T, W, modulus=5).is_zero
    residues = [
        (a, t, w)
        for a, t, w in product(range(5), repeat=3)
        if (a**4 + (a - t) ** 4 + w**4) % 5 == 0
    ]
    assert residues == [(0, 0, 0)]


def test_primitive_full_model_always_has_unit_norm_mod_five():
    count = 0
    for a, b, c, d, w in product(range(5), repeat=5):
        if not any((a, b, c, d, w)):
            continue
        norm = a * a + b * b
        if (norm - c * c - d * d) % 5:
            continue
        closure = (a * a - b * b) ** 2 + (c * c - d * d) ** 2
        if (closure - 4 * norm * w * w + 4 * w**4) % 5:
            continue
        count += 1
        assert norm % 5 != 0
    assert count == 96


def test_rotation_recovery_uses_only_the_unit_norm():
    assert sp.expand(A * DC + B * DD - C * NORM) == 0
    assert sp.expand(A * DD - B * DC - S * NORM) == 0
    assert sp.expand(DC**2 + DD**2 - NORM * (C**2 + S**2)) == 0


def test_all_integral_rotation_residues_have_simple_hensel_seed():
    rotations = [(c, s) for c, s in product(range(5), repeat=2) if (c * c + s * s) % 5 == 1]
    assert rotations == [(0, 1), (0, 4), (1, 0), (4, 0)]
    for c, s in rotations:
        model = FULL.subs({C: c, S: s, W: 1})
        reduced = 2 * (A**2 - B**2) ** 2 - 4 * (A**2 + B**2) + 4
        assert sp.Poly(model - reduced, A, B, modulus=5).is_zero
        assert int(model.subs({A: 0, B: 2})) % 5 == 0
        assert int(sp.diff(model, B).subs({A: 0, B: 2})) % 5 == 3


@pytest.mark.parametrize(("denominator", "residue"), [(1819808, 2), (5269842, 3)])
def test_prior_scale_witness_fails_over_q_five(denominator, residue):
    scale = Fraction(6375625, denominator)
    assert unit_residue(scale, 5) == (4, residue)
    assert residue not in {x * x % 5 for x in range(1, 5)}


def test_prior_projection_witness_is_preserved():
    m = Fraction(-169, 505)
    c, s = Fraction(3, 5), Fraction(4, 5)
    rho = (c - m * s) ** 2 - (s + m * c) ** 2
    g = (1 - m * m) ** 2 + rho * rho
    h = Fraction(3450034, 6375625)
    assert (1 + m * m) ** 2 - g == h * h
    assert {2 * (1 + m * m + sign * h) / g for sign in (1, -1)} == {
        Fraction(6375625, 1819808),
        Fraction(6375625, 5269842),
    }


def test_correct_model_has_nonzero_side_q_two_hensel_lift():
    polynomial = sp.Poly(INTEGER_MODEL.as_expr().subs({A: 1, B: 3}), W, domain=sp.ZZ)
    value = int(polynomial.eval(12))
    derivative = int(polynomial.diff().eval(12))
    assert value == 24143872
    assert derivative == 8340000
    v_value, v_derivative = valuation(value, 2), valuation(derivative, 2)
    assert (v_value, v_derivative) == (11, 5)
    assert v_value > 2 * v_derivative
    assert v_value - v_derivative > valuation(12, 2)


def test_obstruction_is_not_all_rotations_or_all_denominator_primes():
    c, s = Fraction(5, 13), Fraction(12, 13)
    assert c * c + s * s == 1
    assert c.denominator % 5 != 0 and s.denominator % 5 != 0
    model = FULL.subs({C: sp.Rational(5, 13), S: sp.Rational(12, 13), A: 25, W: 1})
    value = Fraction(model.subs(B, 2))
    derivative = Fraction(sp.diff(model, B).subs(B, 2))
    assert unit_residue(value, 5)[0] >= 1
    assert unit_residue(derivative, 5)[0] == 0
    assert (1**4 + 2**4 + 4**4) % 13 == 0
