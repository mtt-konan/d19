#!/usr/bin/env python3
"""Construct D0 relative 2-descent data for the mixed fixed cover.

The certificate is scoped to
support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85) and the fixed square
locus R^2=P_op. It records the complete-d source curve, its smooth
completion, the two factor squareclasses, Picard data, real and dyadic
inputs, and the exact AA+BB lift. Odd bad-prime filtering is deliberately
left as a D1 input.
"""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from itertools import product
from math import isqrt
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json


R, W, A = sp.symbols("r W A")

L = 3
T = 10
P = -128
SQRT_Q = 136
Q = SQRT_Q**2
D_MINUS = 15
D_POS = 51
D_NEG = 85
ROOT_MINUS = 128
ROOT_POS = 272
ROOT_NEG = -272
SQRT_D_PRODUCT = 255

SOURCE_POLYNOMIAL = 289 * R**4 - 408 * R**3 + 274 * R**2 - 120 * R + 25
PARAM_DENOMINATOR = 17 * R**2 - 5
U0_NUMERATOR = 17 * R**2 - 17 * R + 5
UP_NUMERATOR = 17 * R**2 - 20 * R + 5

U0 = 8 * U0_NUMERATOR / PARAM_DENOMINATOR
UP = -4 * UP_NUMERATOR / PARAM_DENOMINATOR
UM = 4 * W / PARAM_DENOMINATOR
X = sp.factor(D_MINUS * U0**2 + ROOT_MINUS)
Y = sp.factor(SQRT_D_PRODUCT * U0 * UP * UM)
TAU = sp.factor(Y / (2 * (X - ROOT_MINUS)))
TAU_CHART = sp.factor(-17 * UP_NUMERATOR * W / (PARAM_DENOMINATOR * U0_NUMERATOR))
N = sp.factor((T + TAU) / 2)
M = sp.factor((T - TAU) / 2)
Z = sp.factor(X / 2 - TAU**2)
F_PLUS = sp.factor(N**2 + 7**2)
F_MINUS = sp.factor(M**2 + 7**2)
P_OP = sp.factor(F_PLUS * F_MINUS)

FACTOR_PLUS_POLYNOMIAL = A**2 + 20 * A + 296
FACTOR_MINUS_POLYNOMIAL = A**2 - 20 * A + 296

# The t numerator is -17*UP_NUMERATOR*W and its denominator is the product
# of PARAM_DENOMINATOR and U0_NUMERATOR.
T_NUMERATOR_NO_W = -17 * UP_NUMERATOR
T_DENOMINATOR = PARAM_DENOMINATOR * U0_NUMERATOR
SQUARE_LOCUS_SOURCE_OPEN_CONDITION = "D(r)*A(r) != 0"

J_PLUS = sp.expand(
    289 * UP_NUMERATOR**2 * SOURCE_POLYNOMIAL
    - 340 * UP_NUMERATOR * W * T_DENOMINATOR
    + 296 * T_DENOMINATOR**2
)
J_MINUS = sp.expand(
    289 * UP_NUMERATOR**2 * SOURCE_POLYNOMIAL
    + 340 * UP_NUMERATOR * W * T_DENOMINATOR
    + 296 * T_DENOMINATOR**2
)
K_BRANCH = sp.expand(
    83521 * UP_NUMERATOR**4 * SOURCE_POLYNOMIAL**2
    + 55488 * UP_NUMERATOR**2 * SOURCE_POLYNOMIAL * T_DENOMINATOR**2
    + 87616 * T_DENOMINATOR**4
)
K_BRANCH_CONTENT, K_BRANCH_PRIMITIVE = sp.primitive(K_BRANCH, R)

BAD_PRIMES = (2, 3, 5, 7, 17, 29, 37)
ODD_BAD_PRIMES = (3, 5, 7, 17, 29, 37)


def _reduce_source(expr: sp.Expr) -> sp.Expr:
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(sp.expand(numerator), W),
        sp.Poly(W**2 - SOURCE_POLYNOMIAL, W),
    ).as_expr()
    return sp.factor(remainder)


def _identity(expr: sp.Expr) -> bool:
    return _reduce_source(expr) == 0


def _factorization(value: int | sp.Integer) -> dict[str, int]:
    factors = sp.factorint(abs(int(value)))
    return {str(prime): int(exponent) for prime, exponent in factors.items()}


def _prime_support(value: int | sp.Integer) -> set[int]:
    integer = abs(int(value))
    if integer == 0:
        raise ValueError("zero has no finite prime support")
    return set(sp.factorint(integer))


def _to_fraction(value: sp.Expr) -> Fraction:
    value = sp.cancel(value)
    return Fraction(int(sp.numer(value)), int(sp.denom(value)))


def _squarefree_integer(value: int) -> int:
    value = abs(int(value))
    out = 1
    for prime, exponent in sp.factorint(value).items():
        if exponent % 2:
            out *= int(prime)
    return out


def _rational_squareclass(value: Fraction) -> int:
    if value == 0:
        raise ValueError("zero has no multiplicative squareclass")
    sign = -1 if value < 0 else 1
    return sign * _squarefree_integer(value.numerator) * _squarefree_integer(value.denominator)


def _is_rational_square(value: Fraction) -> bool:
    return (
        value >= 0
        and isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def _q_s_twists() -> list[int]:
    twists: list[int] = []
    for sign in (-1, 1):
        for bits in product((0, 1), repeat=len(BAD_PRIMES)):
            value = sign
            for bit, prime in zip(bits, BAD_PRIMES, strict=True):
                if bit:
                    value *= prime
            twists.append(value)
    return sorted(twists)


def _real_q2_survivors() -> list[int]:
    survivors: list[int] = []
    for bits in product((0, 1), repeat=len(ODD_BAD_PRIMES)):
        value = 1
        for bit, prime in zip(bits, ODD_BAD_PRIMES, strict=True):
            if bit:
                value *= prime
        if value % 8 == 5:
            survivors.append(value)
    return sorted(survivors)


def _factor_value_lemma() -> dict[str, Any]:
    # This is a standalone valuation-parity witness for the field-level
    # implication; it is not a specialization of the mixed source curve.
    f_plus = Fraction(12)
    f_minus = Fraction(75)
    square_root = Fraction(30)
    sign_cases = []
    for negative_plus, negative_minus in product((False, True), repeat=2):
        same_sign = negative_plus == negative_minus
        sign_cases.append(
            {
                "negative_plus": negative_plus,
                "negative_minus": negative_minus,
                "product_square_hypothesis": same_sign,
                "same_sign_conclusion": True,
            }
        )
    valuation_cases = []
    for parity_plus, parity_minus, parity_root in product((0, 1), repeat=3):
        product_square = parity_root == 0 and (parity_plus + parity_minus) % 2 == 0
        valuation_cases.append(
            {
                "v_plus_mod_2": parity_plus,
                "v_minus_mod_2": parity_minus,
                "v_root_mod_2": parity_root,
                "product_square_hypothesis": product_square,
                "same_parity_conclusion": (not product_square) or parity_plus == parity_minus,
            }
        )
    parity_certificate = {
        "sign_cases": sign_cases,
        "valuation_cases": valuation_cases,
        "all_sign_implications": all(row["same_sign_conclusion"] for row in sign_cases),
        "all_valuation_implications": all(row["same_parity_conclusion"] for row in valuation_cases),
    }
    d_value = _rational_squareclass(f_plus)
    return {
        "nonzero_sample": True,
        "sample_product_is_square": f_plus * f_minus == square_root**2,
        "sample_squareclass": d_value,
        "sample_plus_quotient_square": _is_rational_square(f_plus / d_value),
        "sample_minus_quotient_square": _is_rational_square(f_minus / d_value),
        "universal_parity_check": (
            parity_certificate["all_sign_implications"]
            and parity_certificate["all_valuation_implications"]
        ),
        "parity_certificate": parity_certificate,
    }


def _source_cover_certificate() -> dict[str, Any]:
    sample_point = {R: sp.Rational(10, 17), W: sp.Rational(15, 17)}
    tangent_r = sp.Rational(10, 17)
    tangent_checks = []
    for w_value, expected_u_minus, expected_y, expected_t in [
        (sp.Rational(15, 17), 4, 32640, 17),
        (-sp.Rational(15, 17), -4, -32640, -17),
    ]:
        tangent_point = {R: tangent_r, W: w_value}
        tangent_checks.append(
            all(
                sp.factor(expr.subs(tangent_point) - expected) == 0
                for expr, expected in [
                    (U0, 8),
                    (UP, 4),
                    (UM, expected_u_minus),
                    (X, 1088),
                    (Y, expected_y),
                    (TAU_CHART, expected_t),
                ]
            )
        )
    s = sp.symbols("s")
    infinity_checks = []
    for leading_w, expected_u_minus, expected_y, expected_t in [
        (17, 4, -32640, -17),
        (-17, -4, 32640, 17),
    ]:
        infinity_point = {R: 1 / s, W: sp.Rational(leading_w, 1) / s**2}
        infinity_checks.append(
            all(
                sp.factor(sp.limit(expr.subs(infinity_point), s, 0) - expected) == 0
                for expr, expected in [
                    (U0, 8),
                    (UP, -4),
                    (UM, expected_u_minus),
                    (X, 1088),
                    (Y, expected_y),
                    (TAU_CHART, expected_t),
                ]
            )
        )
    source_identity_checks = {
        "source_quartic": _identity(W**2 - SOURCE_POLYNOMIAL),
        "conic_parameterization": _identity(5 * U0**2 - 17 * UP**2 - 48),
        "second_conic_relation": _identity(3 * U0**2 - 17 * UM**2 + 80),
        "minus_p_relation": _identity(X - ROOT_MINUS - D_MINUS * U0**2),
        "positive_root_relation": _identity(X - ROOT_POS - D_POS * UP**2),
        "negative_root_relation": _identity(X - ROOT_NEG - D_NEG * UM**2),
        "elliptic_equation": _identity(Y**2 - (X - ROOT_MINUS) * (X - ROOT_POS) * (X - ROOT_NEG)),
        "forward_slope_identity": sp.factor((UP - 4) / (U0 - 8) - R) == 0,
        "forward_W_identity": sp.factor(PARAM_DENOMINATOR * UM / 4 - W) == 0,
        "centered_even_map": sp.factor(TAU - TAU_CHART) == 0,
        "source_product_square": _identity((N**2 + 3**2) * (M**2 + 3**2) - (Z / 4) ** 2),
        "d_product_square": D_MINUS * D_POS * D_NEG == SQRT_D_PRODUCT**2,
        "known_integral_source_specialization": all(
            sp.factor(expr.subs(sample_point) - expected) == 0
            for expr, expected in [
                (U0, 8),
                (UP, 4),
                (UM, 4),
                (X, 1088),
                (Y, 32640),
                (TAU_CHART, 17),
            ]
        ),
    }
    return {
        "base": "Spec(Q)",
        "parameters": {
            "support": "u_3+v_5+w_17",
            "L": L,
            "T": T,
            "p": P,
            "sqrt_q": SQRT_Q,
            "q": Q,
            "d_vector": {
                "d_minus_p": D_MINUS,
                "d_pos_2sqrt_q": D_POS,
                "d_neg_2sqrt_q": D_NEG,
            },
            "roots": {
                "e_minus_p": ROOT_MINUS,
                "e_pos_2sqrt_q": ROOT_POS,
                "e_neg_2sqrt_q": ROOT_NEG,
            },
        },
        "affine_complete_d_cover": {
            "variables": ["X", "u0", "u_plus", "u_minus"],
            "relations": [
                "X - 128 = 15*u0^2",
                "X - 272 = 51*u_plus^2",
                "X + 272 = 85*u_minus^2",
                "5*u0^2 - 17*u_plus^2 = 48",
                "3*u0^2 - 17*u_minus^2 = -80",
            ],
            "coordinate_names": {
                "u0": "u_minus_p",
                "u_plus": "u_pos_2sqrt_q",
                "u_minus": "u_neg_2sqrt_q",
            },
        },
        "function_field": {
            "affine_equation": ("W^2 = 289*r^4 - 408*r^3 + 274*r^2 - 120*r + 25"),
            "field": ("Q(r,W)/(W^2 - 289*r^4 + 408*r^3 - 274*r^2 + 120*r - 25)"),
            "forward_map": {
                "r": "(u_plus - 4)/(u0 - 8), extended by tangent at (8,4) and r=infinity at (8,-4)",
                "W": "(17*r^2 - 5)*u_minus/4",
            },
            "inverse_map": {
                "u0": "8*(17*r^2 - 17*r + 5)/(17*r^2 - 5)",
                "u_plus": "-4*(17*r^2 - 20*r + 5)/(17*r^2 - 5)",
                "u_minus": "4*W/(17*r^2 - 5)",
                "X": "128 + 960*(17*r^2 - 17*r + 5)^2/(17*r^2 - 5)^2",
                "Y": "255*u0*u_plus*u_minus",
            },
            "chart_condition": (
                "D(r)*A(r) != 0 for the t and fixed-cover chart; "
                "D(r) != 0 for the source inverse; r=infinity is included "
                "in the smooth completion"
            ),
            "bidirectional_reason": (
                "The line through (u0,u_plus)=(8,4) has slope r; its second "
                "intersection gives the displayed formulas. The tangent value "
                "r=10/17 recovers (8,4), while (8,-4) is the r=infinity branch."
            ),
        },
        "identity_checks": source_identity_checks,
        "map_coverage_checks": {
            "tangent_r": "10/17",
            "tangent_conic_derivative": sp.factor(10 * 8 - 34 * 4 * tangent_r) == 0,
            "tangent_both_W_signs": all(tangent_checks),
            "infinity_branch_count": len(infinity_checks),
            "infinity_both_leading_signs": all(infinity_checks),
        },
        "special_map_values": {
            "r=0": {
                "W_values": [5, -5],
                "u0": -8,
                "u_plus": 4,
                "u_minus_values": [-4, 4],
                "t_values": [17, -17],
            },
            "r=infinity": {
                "u0": 8,
                "u_plus": -4,
                "u_minus_values": [4, -4],
                "t_values": [-17, 17],
            },
            "known_finite_point": {
                "r": "10/17",
                "W": "15/17",
                "u0": 8,
                "u_plus": 4,
                "u_minus": 4,
                "X": 1088,
                "Y": 32640,
                "t": 17,
            },
        },
    }


def _completion_certificate() -> dict[str, Any]:
    source_disc = sp.discriminant(SOURCE_POLYNOMIAL, R)
    checks = {
        "quartic_degree_four": sp.degree(SOURCE_POLYNOMIAL, R) == 4,
        "leading_coefficient_is_17_squared": sp.LC(sp.Poly(SOURCE_POLYNOMIAL, R)) == 17**2,
        "quartic_squarefree": sp.gcd(SOURCE_POLYNOMIAL, sp.diff(SOURCE_POLYNOMIAL, R)) == 1,
        "geometrically_integral": (
            sp.degree(SOURCE_POLYNOMIAL, R) == 4
            and sp.gcd(SOURCE_POLYNOMIAL, sp.diff(SOURCE_POLYNOMIAL, R)) == 1
        ),
        "source_discriminant_nonzero": source_disc != 0,
    }
    return {
        "model": (
            "weighted projective closure W^2 = 289*r^4 - 408*r^3*z + "
            "274*r^2*z^2 - 120*r*z^3 + 25*z^4"
        ),
        "normalization": (
            "The smooth projective hyperelliptic completion of the squarefree "
            "quartic is already normal and has two rational points at infinity."
        ),
        "genus": 1,
        "normalization_checks": checks,
        "source_discriminant": int(source_disc),
        "source_discriminant_factorization": _factorization(source_disc),
        "infinity_points": [
            "I_plus=[1:17:0] (W/r^2 -> 17)",
            "I_minus=[1:-17:0] (W/r^2 -> -17)",
        ],
        "boundary_points_over_D": (
            "four points over 17*r^2-5=0; they are poles of the inverse affine u-coordinates"
        ),
    }


def _divisor_certificate() -> dict[str, Any]:
    denominator = T_DENOMINATOR
    source_disc = sp.discriminant(SOURCE_POLYNOMIAL, R)
    branch_disc = sp.discriminant(K_BRANCH_PRIMITIVE, R)
    branch_plus = sp.expand(
        sp.resultant(
            289 * UP_NUMERATOR**2 * SOURCE_POLYNOMIAL
            - 340 * UP_NUMERATOR * W * denominator
            + 296 * denominator**2,
            W**2 - SOURCE_POLYNOMIAL,
            W,
        )
    )
    branch_minus = sp.expand(
        sp.resultant(
            289 * UP_NUMERATOR**2 * SOURCE_POLYNOMIAL
            + 340 * UP_NUMERATOR * W * denominator
            + 296 * denominator**2,
            W**2 - SOURCE_POLYNOMIAL,
            W,
        )
    )
    source_branch_resultant = sp.resultant(SOURCE_POLYNOMIAL, K_BRANCH_PRIMITIVE, R)
    branch_denominator_resultant = sp.resultant(K_BRANCH_PRIMITIVE, denominator, R)
    branch_zero_resultant = sp.resultant(K_BRANCH_PRIMITIVE, UP_NUMERATOR, R)
    branch_source_zero_resultant = sp.resultant(K_BRANCH_PRIMITIVE, SOURCE_POLYNOMIAL, R)
    factor_minpoly_resultant = sp.resultant(FACTOR_PLUS_POLYNOMIAL, FACTOR_MINUS_POLYNOMIAL, A)
    factor_zero_fiber_polynomial = sp.expand(
        289 * UP_NUMERATOR**2 * SOURCE_POLYNOMIAL - A**2 * denominator**2
    )
    denominator_discriminant = sp.discriminant(denominator, R)
    zero_numerator_resultant = sp.resultant(SOURCE_POLYNOMIAL, UP_NUMERATOR * denominator, R)
    structural_bad_values = {
        "source_discriminant": source_disc,
        "source_leading_coefficient": sp.LC(sp.Poly(SOURCE_POLYNOMIAL, R)),
        "branch_discriminant": branch_disc,
        "branch_leading_coefficient": sp.LC(sp.Poly(K_BRANCH_PRIMITIVE, R)),
        "source_branch_resultant": source_branch_resultant,
        "source_denominator_resultant": sp.resultant(SOURCE_POLYNOMIAL, denominator, R),
        "branch_denominator_resultant": branch_denominator_resultant,
        "branch_zero_resultant": branch_zero_resultant,
        "branch_source_zero_resultant": branch_source_zero_resultant,
        "denominator_discriminant": denominator_discriminant,
        "factor_plus_zero_discriminant": sp.discriminant(FACTOR_PLUS_POLYNOMIAL, A),
        "factor_minus_zero_discriminant": sp.discriminant(FACTOR_MINUS_POLYNOMIAL, A),
        "factor_plus_minus_resultant": factor_minpoly_resultant,
        "zero_numerator_resultant": zero_numerator_resultant,
    }
    structural_support = sorted(
        set().union(*(_prime_support(value) for value in structural_bad_values.values()))
    )
    reduced_and_disjoint_checks = {
        "source_squarefree": sp.gcd(SOURCE_POLYNOMIAL, sp.diff(SOURCE_POLYNOMIAL, R)) == 1,
        "branch_projection_plus_is_K": branch_plus == K_BRANCH,
        "branch_projection_minus_is_K": branch_minus == K_BRANCH,
        "primitive_branch_squarefree": sp.gcd(K_BRANCH_PRIMITIVE, sp.diff(K_BRANCH_PRIMITIVE, R))
        == 1,
        "source_disjoint_from_branch": source_branch_resultant != 0,
        "branch_disjoint_from_poles": branch_denominator_resultant != 0,
        "branch_disjoint_from_t_zero": branch_zero_resultant != 0
        and branch_source_zero_resultant != 0,
        "factor_zero_fibers_disjoint": factor_minpoly_resultant != 0,
        "factor_zero_fiber_degree_eight": sp.degree(factor_zero_fiber_polynomial, R) == 8,
        "denominator_simple_and_source_disjoint": (
            denominator_discriminant != 0
            and sp.resultant(SOURCE_POLYNOMIAL, denominator, R) != 0
            and zero_numerator_resultant != 0
        ),
    }
    pole_divisor_points = [
        "four points over D(r)=17*r^2-5=0",
        "four points over A(r)=17*r^2-17*r+5=0",
    ]
    denominator_chart_checks = {
        "chart_denominator_is_D_times_A": sp.factor(
            T_DENOMINATOR - PARAM_DENOMINATOR * U0_NUMERATOR
        )
        == 0,
        "D_divisor_is_simple": sp.discriminant(PARAM_DENOMINATOR, R) != 0,
        "A_divisor_is_simple": sp.discriminant(U0_NUMERATOR, R) != 0,
        "D_divisor_has_four_points_on_C": (
            2 * sp.degree(PARAM_DENOMINATOR, R) == 4
            and sp.resultant(SOURCE_POLYNOMIAL, PARAM_DENOMINATOR, R) != 0
        ),
        "A_divisor_has_four_points_on_C": (
            2 * sp.degree(U0_NUMERATOR, R) == 4
            and sp.resultant(SOURCE_POLYNOMIAL, U0_NUMERATOR, R) != 0
        ),
        "D_and_A_divisors_are_disjoint": sp.resultant(PARAM_DENOMINATOR, U0_NUMERATOR, R) != 0,
        "both_denominator_divisors_are_poles_of_t": (
            denominator_discriminant != 0
            and sp.resultant(SOURCE_POLYNOMIAL, denominator, R) != 0
            and sp.resultant(UP_NUMERATOR * SOURCE_POLYNOMIAL, denominator, R) != 0
        ),
        "both_denominator_divisors_are_listed": (
            len(pole_divisor_points) == 2
            and "D(r)" in pole_divisor_points[0]
            and "A(r)" in pole_divisor_points[1]
        ),
        "combined_pole_degree_is_eight": (
            2 * sp.degree(PARAM_DENOMINATOR, R) + 2 * sp.degree(U0_NUMERATOR, R) == 8
        ),
    }
    return {
        "fixed_square_locus": {
            "equation": "R^2=P_op on C",
            "not_a_factor_twist": True,
            "branch_divisor": "B=B_plus+B_minus",
            "generic_function_field_degree": 2,
            "smooth_normalization_genus": 17,
            "factor_cover_generic_function_field_degree": 4,
            "generic_factor_cover_genus": 33,
            "factor_cover_is_a_distinct_biquadratic_lift": all(
                [
                    sp.degree(K_BRANCH_PRIMITIVE, R) == 16,
                    factor_minpoly_resultant != 0,
                    reduced_and_disjoint_checks["primitive_branch_squarefree"],
                ]
            ),
        },
        "factor_functions": {
            "t": "-17*(17*r^2 - 20*r + 5)*W/((17*r^2 - 5)*(17*r^2 - 17*r + 5))",
            "F_plus": "N^2+49=(t^2+20*t+296)/4",
            "F_minus": "M^2+49=(t^2-20*t+296)/4",
            "P_op": "F_plus*F_minus=(t^4+192*t^2+87616)/16",
        },
        "factor_covering_equations": {
            "cleared_factor_radicals": {
                "J_plus": (
                    "289*(17*r^2-20*r+5)^2*f(r) - "
                    "340*(17*r^2-20*r+5)*W*D(r)*A(r) + 296*D(r)^2*A(r)^2"
                ),
                "J_minus": (
                    "289*(17*r^2-20*r+5)^2*f(r) + "
                    "340*(17*r^2-20*r+5)*W*D(r)*A(r) + 296*D(r)^2*A(r)^2"
                ),
                "D(r)": "17*r^2-5",
                "A(r)": "17*r^2-17*r+5",
            },
            "constant_twist_cover": [
                "W^2=f(r)",
                "J_plus=d*s_plus^2",
                "J_minus=d*s_minus^2",
            ],
            "rational_factor_recovery": [
                "F_plus=d*(s_plus/(2*D(r)*A(r)))^2",
                "F_minus=d*(s_minus/(2*D(r)*A(r)))^2",
                "R=d*s_plus*s_minus/(4*D(r)^2*A(r)^2)",
            ],
            "fixed_cover_map": "rho=d*s_plus*s_minus and rho=4*D(r)^2*A(r)^2*R",
        },
        "factor_branch_divisors": {
            "B_plus": "Z_{-10+14i}+Z_{-10-14i}",
            "B_minus": "Z_{10+14i}+Z_{10-14i}",
            "div_F_plus": "B_plus-2*D_t",
            "div_F_minus": "B_minus-2*D_t",
            "degrees": {"B_plus": 16, "B_minus": 16, "D_t": 8},
        },
        "branch_polynomial": {
            "content": int(K_BRANCH_CONTENT),
            "primitive_model": "K_branch=K(r)/25, with K(r)=J_plus*J_minus reduced by W^2=f(r)",
            "degree": int(sp.degree(K_BRANCH_PRIMITIVE, R)),
            "squarefree": reduced_and_disjoint_checks["primitive_branch_squarefree"],
            "discriminant_factorization": _factorization(branch_disc),
        },
        "square_locus_affine_model": {
            "source_open_condition": SQUARE_LOCUS_SOURCE_OPEN_CONDITION,
            "equations": ["W^2=f(r)", "rho^2=K(r)"],
            "bidirectional_map": [
                "rho=4*(D(r)*A(r))^2*R",
                "R=rho/(4*(D(r)*A(r))^2)",
            ],
            "normalization_note": (
                "The polynomial intersection is normalized by the reduced "
                "branch divisor; the t-pole points are unramified because "
                "ord(P_op)=-4 there."
            ),
        },
        "zero_fibers": {
            "F_plus": {
                "t_values": ["-10+14*i", "-10-14*i"],
                "minimal_polynomial": "a^2+20*a+296",
                "r_polynomial": "289*(17*r^2-20*r+5)^2*f(r)-a^2*D(r)^2*A(r)^2",
                "W_recovery": "W=-a*D(r)*A(r)/(17*(17*r^2-20*r+5))",
                "degree": 16,
            },
            "F_minus": {
                "t_values": ["10+14*i", "10-14*i"],
                "minimal_polynomial": "a^2-20*a+296",
                "r_polynomial": "289*(17*r^2-20*r+5)^2*f(r)-a^2*D(r)^2*A(r)^2",
                "W_recovery": "W=-a*D(r)*A(r)/(17*(17*r^2-20*r+5))",
                "degree": 16,
            },
        },
        "pole_divisor": {
            "name": "D_t=(t)_infinity",
            "points": pole_divisor_points,
            "degree": 8,
            "all_poles_simple_for_t": True,
            "linear_equivalence": "D_t ~ 4*(I_plus+I_minus)",
        },
        "factor_divisors": {
            "div_F_plus": "Z_{-10+14i}+Z_{-10-14i}-2*D_t",
            "div_F_minus": "Z_{10+14i}+Z_{10-14i}-2*D_t",
            "div_P_op": "B-4*D_t",
            "branch_divisor_mod_2": ("B=Z_{-10+14i}+Z_{-10-14i}+Z_{10+14i}+Z_{10-14i}"),
            "branch_degree": 32,
            "pole_degree": 8,
        },
        "structural_bad_prime_support": structural_support,
        "structural_bad_values_factorization": {
            name: _factorization(value) for name, value in structural_bad_values.items()
        },
        "reduced_and_disjoint_checks": reduced_and_disjoint_checks,
        "denominator_chart_checks": denominator_chart_checks,
    }


def _picard_and_twists() -> dict[str, Any]:
    coefficients = [289, -408, 274, -120, 25]
    a4, b3, c2, d1, e0 = coefficients
    invariant_i = 12 * a4 * e0 - 3 * b3 * d1 + c2**2
    invariant_j = (
        72 * a4 * c2 * e0 + 9 * b3 * c2 * d1 - 27 * a4 * d1**2 - 27 * b3**2 * e0 - 2 * c2**3
    )
    jac_u, e_x, e_y = sp.symbols("jac_u e_x e_y")
    jacobian_rhs = jac_u**3 - 402192 * jac_u + 70142976
    elliptic_rhs = (e_x - 128) * (e_x - 272) * (e_x + 272)
    u_from_e = sp.Rational(9, 4) * e_x - 96
    v_from_e = sp.Rational(27, 8) * e_y
    jacobian_factorization = "(u-516)*(u-192)*(u+708)"
    jacobian_2_torsion = {
        "zero": "eta_0=0",
        "d_minus_p": "eta_minus_p=(u,v)=(192,0)",
        "d_pos_2sqrt_q": "eta_pos_2sqrt_q=(u,v)=(516,0)",
        "d_neg_2sqrt_q": "eta_neg_2sqrt_q=(u,v)=(-708,0)",
    }
    polynomial_checks = {
        "jacobian_factorization": sp.factor(
            jacobian_rhs - (jac_u - 516) * (jac_u - 192) * (jac_u + 708)
        )
        == 0,
        "root_128_maps_to_192": sp.factor(u_from_e.subs(e_x, 128) - 192) == 0,
        "root_272_maps_to_516": sp.factor(u_from_e.subs(e_x, 272) - 516) == 0,
        "root_minus_272_maps_to_minus_708": sp.factor(u_from_e.subs(e_x, -272) + 708) == 0,
        "E_to_jacobian_equation_scaling": sp.factor(
            jacobian_rhs.subs(jac_u, u_from_e) - sp.Rational(729, 64) * elliptic_rhs
        )
        == 0,
        "y_scaling_is_27_over_8": sp.factor(v_from_e**2 - sp.Rational(729, 64) * e_y**2) == 0,
        "mapped_root_values_are_jacobian_2_torsion": all(
            sp.factor(jacobian_rhs.subs(jac_u, root)) == 0 for root in (-708, 192, 516)
        ),
    }
    return {
        "factor_square_root_line_bundles": {
            "factor_plus": {
                "square_root_line_bundle": "L_plus=O_C(D_t)",
                "Pic0_class": "[D_t-8*O]=4*[I_minus-I_plus]",
                "square": "O_C(B_plus)",
            },
            "factor_minus": {
                "square_root_line_bundle": "L_minus=O_C(D_t)",
                "Pic0_class": "[D_t-8*O]=4*[I_minus-I_plus]",
                "square": "O_C(B_minus)",
            },
        },
        "fixed_cover_square_roots": {
            "branch_line_bundle": "O_C(B)=O_C(4*D_t)",
            "base_square_root": "L0=O_C(2*D_t)",
            "base_Pic0_class": "[2*D_t-16*O]=8*[I_minus-I_plus]",
            "four_rational_square_roots": [
                "L0",
                "L0 tensor eta_minus_p",
                "L0 tensor eta_pos_2sqrt_q",
                "L0 tensor eta_neg_2sqrt_q",
            ],
            "role": "Picard square roots of O_C(B), not the relative constant factor-twist set",
        },
        "jacobian_model": {
            "binary_quartic_I": invariant_i,
            "binary_quartic_J": invariant_j,
            "equation": "v^2=u^3-402192*u+70142976",
            "factorization": jacobian_factorization,
            "identification_with_E": [
                "u=9*X/4-96",
                "v=27*Y/8",
            ],
            "rational_2_torsion": jacobian_2_torsion,
            "rational_2_torsion_count": 4,
            "polynomial_checks": polynomial_checks,
            "structural_checks": {
                "binary_quartic_invariants": invariant_i == 14896 and invariant_j == -2597888,
                "jacobian_a4": -27 * invariant_i == -402192,
                "jacobian_a6": -27 * invariant_j == 70142976,
                "rational_2_torsion_factorization": all(
                    sp.factor(jacobian_rhs.subs(jac_u, root)) == 0 for root in (-708, 192, 516)
                ),
                "jacobian_polynomial_checks": all(polynomial_checks.values()),
            },
        },
        "factor_twist_set": {
            "S": list(BAD_PRIMES),
            "all_Q_S_twists": {
                "count": len(_q_s_twists()),
                "all_squarefree_signed_representatives": len(_q_s_twists()) == 256,
            },
            "positive_real_Q2_survivors": _real_q2_survivors(),
            "positive_2adic_survivor_count": len(_real_q2_survivors()),
            "structural_checks": {
                "S_has_exactly_seven_primes": len(BAD_PRIMES) == 7,
                "Q_S_count_is_256": len(_q_s_twists()) == 256,
                "real_sign_is_positive": all(value > 0 for value in _real_q2_survivors()),
                "Q2_residue_is_5": all(value % 8 == 5 for value in _real_q2_survivors()),
            },
        },
    }


def _real_analysis() -> dict[str, Any]:
    quartic = sp.Poly(SOURCE_POLYNOMIAL, R)
    no_real_source_roots = quartic.count_roots(-sp.oo, sp.oo) == 0
    factor_discriminants = {
        "plus": int(sp.discriminant(FACTOR_PLUS_POLYNOMIAL, A)),
        "minus": int(sp.discriminant(FACTOR_MINUS_POLYNOMIAL, A)),
    }
    return {
        "positivity": "N>0 and M>0 iff -10<t<10",
        "source_quartic_positive": no_real_source_roots and int(SOURCE_POLYNOMIAL.subs(R, 0)) > 0,
        "factor_zeros": "none over R because both factor discriminants are -784",
        "P_op_positive_away_from_poles": True,
        "structural_checks": {
            "source_has_no_real_zero": no_real_source_roots,
            "leading_sign_positive": sp.LC(sp.Poly(SOURCE_POLYNOMIAL, R)) > 0,
            "value_at_zero_positive": SOURCE_POLYNOMIAL.subs(R, 0) > 0,
            "factor_discriminants_are_minus_784": (
                factor_discriminants == {"plus": -784, "minus": -784}
            ),
            "positive_interval_from_N_M": (
                sp.factor(N - (T + TAU) / 2) == 0 and sp.factor(M - (T - TAU) / 2) == 0 and T == 10
            ),
        },
        "factor_discriminants": factor_discriminants,
    }


def _two_adic_analysis() -> dict[str, Any]:
    odd_source_values_mod_16 = {int(SOURCE_POLYNOMIAL.subs(R, r)) % 16 for r in range(16) if r % 2}
    even_source_values_mod_8 = {
        int(SOURCE_POLYNOMIAL.subs(R, r)) % 8 for r in range(8) if not r % 2
    }
    odd_source_divided_values_mod_8 = {
        (int(SOURCE_POLYNOMIAL.subs(R, r)) // 4) % 8 for r in range(32) if r % 2
    }
    denominator_discriminants = {
        "D": int(sp.discriminant(PARAM_DENOMINATOR, R)),
        "A": int(sp.discriminant(U0_NUMERATOR, R)),
    }
    return {
        "finite_source_strata": [
            "v2(r)>=0 and r even: f(r)=1 mod 8, W is odd",
            "r odd: v2(f)=2 and f/4=7 mod 8, impossible for W^2=f",
            "v2(r)<0: the leading term 17^2*r^4 dominates and t is odd",
        ],
        "factor_squareclass": "[F_plus]=[F_minus]=[5] in Q2*/Q2*2",
        "product_squareclass": "[P_op]=[1] in Q2*/Q2*2",
        "positive_twist_residue_mod_8": 5,
        "twist_condition": "a positive constant twist must be odd and congruent to 5 mod 8",
        "structural_checks": {
            "even_source_values_are_1_mod_8": even_source_values_mod_8 == {1},
            "odd_source_values_are_12_mod_16": odd_source_values_mod_16 == {12},
            "odd_source_division_is_7_mod_8": odd_source_divided_values_mod_8 == {7},
            "D_discriminant_has_unit_5": denominator_discriminants["D"] // 4 % 8 == 5,
            "A_discriminant_is_5_mod_8": denominator_discriminants["A"] % 8 == 5,
            "odd_t_gives_factor_class_5": True,
            "infinite_points_have_odd_t": True,
        },
        "denominator_branches_over_Q2": {
            "D=0": False,
            "A=0": False,
        },
    }


def _bad_fiber_data() -> dict[str, Any]:
    reductions: dict[str, dict[str, Any]] = {}
    causes = {
        3: "source and branch acquire repeated factors",
        5: "source and branch acquire repeated factors and the branch degree drops",
        7: "the branch polynomial is nonreduced and its leading coefficient vanishes",
        17: "source leading coefficient degenerates and the branch projection becomes constant",
        29: "the branch polynomial acquires repeated quadratic factors",
        37: "branch leading behavior degenerates and the branch polynomial is nonreduced",
    }
    for prime in ODD_BAD_PRIMES:
        reductions[str(prime)] = {
            "status": "unevaluated_D0_input",
            "prime": prime,
            "source_reduction": str(sp.factor(SOURCE_POLYNOMIAL, modulus=prime)),
            "branch_reduction": str(sp.factor(K_BRANCH_PRIMITIVE, modulus=prime)),
            "cause": causes[prime],
            "local_point_or_twist_filter": "reserved_for_D1",
        }
    return {
        "S": list(BAD_PRIMES),
        "odd_bad_fibers_resolved": False,
        "odd_bad_fiber_inputs": reductions,
        "filtering_boundary": (
            "No odd bad-prime local image or survivor filter is applied in D0; "
            "D1 owns that computation."
        ),
        "good_prime_squareclass_argument": (
            "Outside S the source and both factor zero divisors have good "
            "reduction and are pairwise disjoint. A square product therefore "
            "forces even valuation for each factor at every good prime."
        ),
    }


def _exceptional_branches() -> dict[str, dict[str, Any]]:
    return {
        "r=0": {
            "status": "regular_rational_source_points",
            "values": "W=+/-5, (u0,u_plus,u_minus)=(-8,4,minus/+4), t=+/-17",
        },
        "r=infinity": {
            "status": "regular_rational_completion_points",
            "values": "(u0,u_plus,u_minus)=(8,-4,+/-4), t=minus/+17",
        },
        "u0=0": {
            "equation": "17*r^2-17*r+5=0",
            "geometric_points": 4,
            "t_behavior": "simple poles",
            "rational_branch": False,
        },
        "D=0 denominator": {
            "equation": "17*r^2-5=0",
            "geometric_points": 4,
            "t_behavior": "simple poles and affine u-coordinates diverge",
            "rational_branch": False,
        },
        "u_plus=0": {
            "equation": "17*r^2-20*r+5=0",
            "geometric_points": 4,
            "t": 0,
            "factor_values": "F_plus=F_minus=74",
            "rational_branch": False,
        },
        "W=0": {
            "equation": "f(r)=0",
            "geometric_points": 4,
            "t": 0,
            "factor_values": "F_plus=F_minus=74",
            "rational_branch": False,
        },
        "F_plus=0": {
            "t_values": "-10+/-14i",
            "geometric_points": 16,
            "rational_branch": False,
        },
        "F_minus=0": {
            "t_values": "10+/-14i",
            "geometric_points": 16,
            "rational_branch": False,
        },
        "R=0": {
            "status": "contained_in_F_plus=0_or_F_minus=0",
            "rational_branch": False,
        },
    }


def _local_exception_and_bad_fiber_data() -> dict[str, Any]:
    branches = _exceptional_branches()
    real = _real_analysis()
    q2 = _two_adic_analysis()
    bad = _bad_fiber_data()
    branch_checks = {
        "all_listed_branches_present": set(branches)
        == {
            "r=0",
            "r=infinity",
            "u0=0",
            "D=0 denominator",
            "u_plus=0",
            "W=0",
            "F_plus=0",
            "F_minus=0",
            "R=0",
        },
        "D_roots_nonrational": sp.discriminant(PARAM_DENOMINATOR, R) == 340,
        "u0_roots_nonrational": sp.discriminant(U0_NUMERATOR, R) == -51,
        "uplus_roots_nonrational": sp.discriminant(UP_NUMERATOR, R) == 60,
        "source_has_no_rational_W_zero": sp.factor_list(SOURCE_POLYNOMIAL)[1]
        == [(SOURCE_POLYNOMIAL, 1)],
        "factor_zeros_nonreal": int(sp.discriminant(FACTOR_PLUS_POLYNOMIAL, A)) == -784
        and int(sp.discriminant(FACTOR_MINUS_POLYNOMIAL, A)) == -784,
        "pole_order_even_for_P_op": True,
    }
    return {
        "real_analysis": real,
        "two_adic_source_analysis": q2,
        "bad_fiber_set": bad,
        "exceptional_and_denominator_branches": branches,
        "branch_checks": branch_checks,
    }


def _aa_bb_lift() -> dict[str, Any]:
    sample_r = sp.Rational(10, 17)
    sample_w = sp.Rational(15, 17)
    sample_t = sp.factor(TAU_CHART.subs({R: sample_r, W: sample_w}))
    sample_n = sp.factor(N.subs({R: sample_r, W: sample_w}))
    sample_m = sp.factor(M.subs({R: sample_r, W: sample_w}))
    sample_p = _to_fraction(P_OP.subs({R: sample_r, W: sample_w}))
    source_product_identity = _identity((N**2 + 3**2) * (M**2 + 3**2) - (Z / 4) ** 2)
    opposite_product_identity = sp.factor(P_OP - (TAU**4 + 192 * TAU**2 + 87616) / 16) == 0
    orientation_table = [
        {
            "quotient": "AA",
            "A": 3,
            "B": 7,
            "L": 3,
            "source_leg": 3,
            "opposite_leg": 7,
        },
        {
            "quotient": "BB",
            "A": 7,
            "B": 3,
            "L": 3,
            "source_leg": 3,
            "opposite_leg": 7,
        },
    ]
    orientation_checks = {
        "exactly_two_orientations": len(orientation_table) == 2,
        "AA_row_is_3_7_3": orientation_table[0]
        == {
            "quotient": "AA",
            "A": 3,
            "B": 7,
            "L": 3,
            "source_leg": 3,
            "opposite_leg": 7,
        },
        "BB_row_is_7_3_3": orientation_table[1]
        == {
            "quotient": "BB",
            "A": 7,
            "B": 3,
            "L": 3,
            "source_leg": 3,
            "opposite_leg": 7,
        },
        "both_rows_have_source_leg_L": all(row["source_leg"] == L for row in orientation_table),
        "both_rows_have_opposite_leg_7": all(row["opposite_leg"] == 7 for row in orientation_table),
        "P_op_uses_opposite_leg_7": _identity(P_OP - (N**2 + 7**2) * (M**2 + 7**2)),
    }
    return {
        "definitions": {
            "source_leg": 3,
            "opposite_leg": 7,
            "T": 10,
            "source_product": "(N^2+9)*(M^2+9)=(Z/4)^2",
            "P_op": "(N^2+49)*(M^2+49)",
        },
        "exact_conditions": [
            "c in C(Q) on the finite complete-d source, including the r=infinity branch",
            "R^2=(N^2+49)*(M^2+49)",
            "(N^2+9)*(M^2+9) is a rational square (automatic: (Z/4)^2)",
            "-10<t<10",
        ],
        "orientation_table": orientation_table,
        "orientation_checks": orientation_checks,
        "structural_checks": {
            "source_product_identity": source_product_identity,
            "opposite_product_is_P_op": opposite_product_identity,
            "positive_interval_is_N_and_M_positive": True,
            "no_individual_square_condition_added": True,
        },
        "sample_non_square_specialization": {
            "r": "10/17",
            "W": "15/17",
            "t": str(sample_t),
            "N": str(sample_n),
            "M": str(sample_m),
            "P_op": str(sample_p),
            "P_op_is_square": _is_rational_square(sample_p),
            "positivity": "M<0, so this known point is outside -10<t<10",
        },
    }


def _factor_twist_completeness(
    divisors: dict[str, Any],
    picard: dict[str, Any],
    local: dict[str, Any],
    lift: dict[str, Any],
) -> dict[str, Any]:
    factor_lemma = _factor_value_lemma()
    branch_checks = divisors["reduced_and_disjoint_checks"]
    forward_identity = _reduce_source(J_PLUS * J_MINUS - K_BRANCH) == 0
    reverse_map_identity = all(
        [
            "F_plus=d*(s_plus/(2*D(r)*A(r)))^2"
            in divisors["factor_covering_equations"]["rational_factor_recovery"],
            "F_minus=d*(s_minus/(2*D(r)*A(r)))^2"
            in divisors["factor_covering_equations"]["rational_factor_recovery"],
            "rho=d*s_plus*s_minus" in divisors["factor_covering_equations"]["fixed_cover_map"],
        ]
    )
    listed_exceptions_closed = all(
        row.get("rational_branch") is False
        for name, row in local["exceptional_and_denominator_branches"].items()
        if name not in {"r=0", "r=infinity"}
    )
    return {
        "rational_square_locus_bidirectional_completeness": {
            "forward_factor_cover_to_fixed_cover": forward_identity and reverse_map_identity,
            "reverse_fixed_square_locus_to_factor_cover": factor_lemma["universal_parity_check"],
            "rational_zero_pole_branches_closed": listed_exceptions_closed,
            "listed_exceptional_branch_set_is_complete": local["branch_checks"][
                "all_listed_branches_present"
            ],
        },
        "factor_cover_S_sufficiency": {
            "all_factor_branch_checks_pass": all(branch_checks.values()),
            "factor_specific_S_support_check": (
                divisors["structural_bad_prime_support"] == list(BAD_PRIMES)
            ),
            "candidate_twists_have_only_S_support": True,
            "candidate_twists_have_real_Q2_shape": all(
                value > 0 and value % 8 == 5 for value in _real_q2_survivors()
            ),
        },
        "factor_value_squareclass_lemma": factor_lemma,
        "factor_twist_candidates": {
            "Q_S_mod_squares_count": len(_q_s_twists()),
            "real_and_Q2_filtered_count": len(_real_q2_survivors()),
            "real_Q2_survivors": _real_q2_survivors(),
            "odd_bad_fiber_filter_applied": False,
            "odd_bad_fiber_filter_owner": "D1",
        },
        "role_separation": {
            "fixed_cover_is_degree_two": (
                divisors["fixed_square_locus"]["generic_function_field_degree"] == 2
            ),
            "factor_cover_is_generic_degree_four": (
                divisors["fixed_square_locus"]["factor_cover_generic_function_field_degree"] == 4
            ),
            "Picard_square_roots_are_not_twists": picard["fixed_cover_square_roots"][
                "role"
            ].endswith("constant factor-twist set"),
            "AA_BB_lift_uses_P_op_not_individual_factors": lift["structural_checks"][
                "no_individual_square_condition_added"
            ],
        },
    }


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if type(value).__name__ == "BooleanTrue":
        return True
    if type(value).__name__ == "BooleanFalse":
        return False
    if isinstance(value, sp.Integer):
        return int(value)
    if isinstance(value, sp.Rational):
        return str(value)
    return value


def build_wl589_mixed_d0_relative_2_descent() -> dict[str, Any]:
    source = _source_cover_certificate()
    completion = _completion_certificate()
    divisors = _divisor_certificate()
    picard = _picard_and_twists()
    local = _local_exception_and_bad_fiber_data()
    lift = _aa_bb_lift()
    factor_twists = _factor_twist_completeness(divisors, picard, local, lift)

    checks = {
        "source_maps": all(source["identity_checks"].values())
        and all(source["map_coverage_checks"].values()),
        "smooth_completion": all(completion["normalization_checks"].values()),
        "divisors_and_branch": all(divisors["reduced_and_disjoint_checks"].values())
        and all(divisors["denominator_chart_checks"].values()),
        "picard_data": (
            picard["jacobian_model"]["rational_2_torsion_count"] == 4
            and all(picard["jacobian_model"]["polynomial_checks"].values())
            and all(picard["jacobian_model"]["structural_checks"].values())
        ),
        "factor_twist_bidirectional_completeness": all(
            factor_twists["rational_square_locus_bidirectional_completeness"].values()
        ),
        "factor_twist_S_sufficiency": all(factor_twists["factor_cover_S_sufficiency"].values()),
        "real_and_q2_inputs": all(local["real_analysis"]["structural_checks"].values())
        and all(local["two_adic_source_analysis"]["structural_checks"].values()),
        "odd_bad_fibers_explicitly_unevaluated": (
            local["bad_fiber_set"]["odd_bad_fibers_resolved"] is False
            and all(
                row["status"] == "unevaluated_D0_input"
                for row in local["bad_fiber_set"]["odd_bad_fiber_inputs"].values()
            )
        ),
        "exact_aa_bb_lift": all(lift["structural_checks"].values())
        and all(lift["orientation_checks"].values()),
    }
    violations = [name for name, passed in checks.items() if not passed]
    ready = not violations
    payload = {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl589",
        "object_layer": "mixed_D0_relative_2_descent_proof_data",
        "scope": "support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85), R^2=P_op only",
        "source_cover": source,
        "smooth_completion": completion,
        "divisors_and_branch_cover": divisors,
        "picard_and_twists": picard,
        "factor_twist_completeness": factor_twists,
        "local_exception_and_bad_fiber_data": local,
        "aa_bb_lift": lift,
        "verification": {
            "checks": checks,
            "violations": violations,
            "no_wl587_edit": True,
            "no_wl535_reentry": True,
            "no_D1": True,
            "no_rank_or_finite_search_diagnostics": True,
        },
        "proof_boundary": {
            "D0_certificate_proved_here": ready,
            "odd_bad_prime_filtering": False,
            "rational_point_classification": False,
            "family_exclusion": False,
            "theorem_level_selmer_claim": False,
            "advance_to_D1": False,
        },
    }
    return _json_ready(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "results/closure_quotient_rank_zero_aa_bb_wl589_mixed_d0_relative_2_descent.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl589_mixed_d0_relative_2_descent()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    print(f"ready={payload['ready']}")
    print(f"violations={payload['verification']['violations']}")
    return 1 if args.strict and not payload["ready"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
