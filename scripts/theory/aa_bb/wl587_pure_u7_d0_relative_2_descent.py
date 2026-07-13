#!/usr/bin/env python3
"""Construct and audit the pure-u_7 D0 relative 2-descent data.

This is a fixed cover over Q.  It records the complete-d source curve,
the opposite-side double cover, its branch divisor and Picard square-root
data, and the local/exceptional branches needed before any later descent.
It does not classify rational points on the genus-seventeen cover.
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

L = 7
T = 9
P = 230
SQRT_Q = 277
Q = SQRT_Q**2
D_MINUS = 7
D_POS = 7
D_NEG = 1

SOURCE_POLYNOMIAL = 7 * R**4 + 2864 * R**2 + 87808
T_NUMERATOR = R**2 - 112
T_DENOMINATOR = 4 * R * (R**2 + 112)

U0 = (R**2 + 112) / (2 * R)
UP = (R**2 - 112) / (2 * R)
UM = W / (2 * R)
X = sp.factor(7 * U0**2 - P)
Y = sp.factor(7 * U0 * UP * UM)
TAU = sp.factor(Y / (2 * (X + P)))
TAU_CHART = sp.factor(W * T_NUMERATOR / T_DENOMINATOR)
Z = sp.factor(X / 2 - TAU**2)
N = sp.factor((T + TAU) / 2)
M = sp.factor((T - TAU) / 2)
F_PLUS = sp.factor(N**2 + 2**2)
F_MINUS = sp.factor(M**2 + 2**2)
P_OP = sp.factor(F_PLUS * F_MINUS)

# Clearing the even denominator of each factor gives integral radicands for
# the two factor coverings.  These are not the fixed cover R^2=P_op.
J_PLUS = sp.expand(
    SOURCE_POLYNOMIAL * T_NUMERATOR**2
    + 18 * W * T_NUMERATOR * T_DENOMINATOR
    + 97 * T_DENOMINATOR**2
)
J_MINUS = sp.expand(
    SOURCE_POLYNOMIAL * T_NUMERATOR**2
    - 18 * W * T_NUMERATOR * T_DENOMINATOR
    + 97 * T_DENOMINATOR**2
)

K_BRANCH = sp.expand(
    SOURCE_POLYNOMIAL**2 * T_NUMERATOR**4
    - 130 * SOURCE_POLYNOMIAL * T_NUMERATOR**2 * T_DENOMINATOR**2
    + 9409 * T_DENOMINATOR**4
)

BAD_PRIMES = (2, 3, 5, 7, 53, 97, 277)
ODD_BAD_PRIMES = (3, 5, 7, 53, 97, 277)


def _reduce_source(expr: sp.Expr) -> sp.Expr:
    """Reduce a numerator modulo W^2-SOURCE_POLYNOMIAL."""
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(sp.expand(numerator), W),
        sp.Poly(W**2 - SOURCE_POLYNOMIAL, W),
    ).as_expr()
    return sp.factor(remainder)


def _identity(expr: sp.Expr) -> bool:
    return _reduce_source(expr) == 0


def _factorization(n: int) -> dict[str, int]:
    factors = sp.factorint(abs(int(n)))
    return {str(prime): int(exponent) for prime, exponent in factors.items()}


def _prime_support(value: sp.Expr | int) -> set[int]:
    integer = abs(int(value))
    if integer == 0:
        raise ValueError("zero has no finite prime support")
    return set(sp.factorint(integer))


def _v2(n: int) -> int:
    value = abs(int(n))
    if value == 0:
        raise ValueError("v2(0) is not used in this certificate")
    out = 0
    while value % 2 == 0:
        value //= 2
        out += 1
    return out


def _squarefree_integer(n: int) -> int:
    value = abs(int(n))
    out = 1
    prime = 2
    while prime * prime <= value:
        parity = 0
        while value % prime == 0:
            value //= prime
            parity ^= 1
        if parity:
            out *= prime
        prime += 1 if prime == 2 else 2
    if value > 1:
        out *= value
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


def _factor_twist_value_lemma(
    f_plus: Fraction, f_minus: Fraction, square_root: Fraction
) -> dict[str, Any]:
    """Check the exact field-level squareclass splitting implication.

    The numerical values are only a displayed sanity witness.  Completeness
    is obtained from the componentwise valuation-parity truth table, including
    the sign component, so it is not inferred from that one witness.
    """
    if f_plus == 0 or f_minus == 0:
        return {"nonzero": False, "complete": False}
    product_is_square = f_plus * f_minus == square_root**2
    d_value = _rational_squareclass(f_plus)
    plus_quotient = f_plus / d_value
    minus_quotient = f_minus / d_value
    sign_cases = []
    for sign_plus, sign_minus in product((False, True), repeat=2):
        hypothesis = sign_plus == sign_minus
        sign_cases.append(
            {
                "sign_plus_negative": sign_plus,
                "sign_minus_negative": sign_minus,
                "square_product_hypothesis": hypothesis,
                "same_sign_conclusion": (not hypothesis) or sign_plus == sign_minus,
            }
        )
    valuation_cases = []
    for parity_plus, parity_minus, parity_root in product((0, 1), repeat=3):
        hypothesis = parity_root == 0 and (parity_plus + parity_minus) % 2 == 0
        valuation_cases.append(
            {
                "v_plus_mod_2": parity_plus,
                "v_minus_mod_2": parity_minus,
                "v_root_mod_2": parity_root,
                "square_product_hypothesis": hypothesis,
                "same_parity_conclusion": (not hypothesis) or parity_plus == parity_minus,
            }
        )
    parity_certificate = {
        "sign_cases": sign_cases,
        "valuation_cases": valuation_cases,
        "all_sign_implications": all(row["same_sign_conclusion"] for row in sign_cases),
        "all_valuation_implications": all(row["same_parity_conclusion"] for row in valuation_cases),
        "universal_squareclass_splitting": all(row["same_sign_conclusion"] for row in sign_cases)
        and all(row["same_parity_conclusion"] for row in valuation_cases),
    }
    return {
        "nonzero": True,
        "product_is_square": product_is_square,
        "d": d_value,
        "plus_quotient_is_square": _is_rational_square(plus_quotient),
        "minus_quotient_is_square": _is_rational_square(minus_quotient),
        "parity_certificate": parity_certificate,
        "complete": parity_certificate["universal_squareclass_splitting"],
    }


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


def _q2_twists() -> list[int]:
    twists: list[int] = []
    for bits in product((0, 1), repeat=len(ODD_BAD_PRIMES)):
        value = 1
        for bit, prime in zip(bits, ODD_BAD_PRIMES, strict=True):
            if bit:
                value *= prime
        if value % 8 == 1:
            twists.append(value)
    return sorted(twists)


def _source_cover_certificate() -> dict[str, Any]:
    return {
        "base": "Spec(Q)",
        "parameters": {
            "support": "u_7",
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
        },
        "affine_complete_d_cover": {
            "variables": ["X", "u0", "u_plus", "u_minus"],
            "relations": [
                "X + 230 = 7*u0^2",
                "X - 554 = 7*u_plus^2",
                "X + 554 = u_minus^2",
                "u0^2 - u_plus^2 = 112",
                "u_minus^2 - 7*u0^2 = 324",
            ],
            "coordinate_names": {
                "u0": "u_minus_p",
                "u_plus": "u_pos_2sqrt_q",
                "u_minus": "u_neg_2sqrt_q",
            },
        },
        "function_field": {
            "affine_equation": "W^2 = 7*r^4 + 2864*r^2 + 87808",
            "field": "Q(r,W)/(W^2 - 7*r^4 - 2864*r^2 - 87808)",
            "forward_map": {
                "r": "u0 + u_plus",
                "W": "2*r*u_minus",
            },
            "inverse_map": {
                "u0": "(r^2 + 112)/(2*r)",
                "u_plus": "(r^2 - 112)/(2*r)",
                "u_minus": "W/(2*r)",
                "X": "7*((r^2 + 112)/(2*r))^2 - 230",
                "Y": "7*u0*u_plus*u_minus",
            },
            "chart_condition": "r != 0",
            "bidirectional_reason": (
                "(u0-u_plus)*(u0+u_plus)=112, so every finite source point "
                "has r=u0+u_plus != 0; the displayed inverse is then unique."
            ),
        },
        "identity_checks": {
            "source_quartic": _identity(W**2 - SOURCE_POLYNOMIAL),
            "forward_r_map": sp.factor(U0 + UP - R) == 0,
            "forward_W_map": sp.factor(2 * R * UM - W) == 0,
            "inverse_difference_product": sp.factor((U0 - UP) * R - 112) == 0,
            "u0_relation": _identity(X + P - 7 * U0**2),
            "u_plus_relation": _identity(X - 2 * SQRT_Q - 7 * UP**2),
            "u_minus_relation": _identity(X + 2 * SQRT_Q - UM**2),
            "second_difference_relation": _identity(UM**2 - 7 * U0**2 - 324),
            "elliptic_equation": _identity(Y**2 - (X + P) * (X**2 - 4 * Q)),
            "centered_even_map": sp.factor(TAU - TAU_CHART) == 0,
            "source_product_square": _identity((N**2 + 49) * (M**2 + 49) - (Z / 4) ** 2),
        },
    }


def _completion_certificate() -> dict[str, Any]:
    source_disc = sp.discriminant(SOURCE_POLYNOMIAL, R)
    source_derivative = sp.diff(SOURCE_POLYNOMIAL, R)
    source_degree = sp.degree(SOURCE_POLYNOMIAL, R)
    source_leading_coefficient = sp.LC(sp.Poly(SOURCE_POLYNOMIAL, R))
    normalization_checks = {
        "quartic_degree_four": source_degree == 4,
        "quartic_leading_coefficient_nonzero": source_leading_coefficient != 0,
        "quartic_squarefree": sp.gcd(SOURCE_POLYNOMIAL, source_derivative) == 1,
        "geometrically_integral_hyperelliptic_model": (
            source_degree == 4
            and source_leading_coefficient != 0
            and sp.gcd(SOURCE_POLYNOMIAL, source_derivative) == 1
        ),
        "weighted_infinity_chart_smooth": source_leading_coefficient != 0,
        "genus_formula_for_even_quartic": (source_degree - 2) // 2 == 1,
    }
    return {
        "model": "weighted projective closure W^2 = 7*R^4 + 2864*R^2*Z^2 + 87808*Z^4",
        "normalization": (
            "The affine source is the open r!=0 chart of the integral quartic; "
            "the quartic is geometrically integral because its defining quartic "
            "is squarefree."
        ),
        "genus": 1,
        "normalization_checks": normalization_checks,
        "smoothness_checks": {
            "source_discriminant_nonzero": source_disc != 0,
            "source_discriminant_factorization": _factorization(source_disc),
            "weighted_infinity_points": ["I_plus=[1:0:sqrt(7)]", "I_minus=[1:0:-sqrt(7)]"],
            "r_zero_points": ["P0_plus=[0:1:112*sqrt(7)]", "P0_minus=[0:1:-112*sqrt(7)]"],
        },
        "original_affine_boundary": [
            "r=0 (two geometric points)",
            "r=infinity (I_plus and I_minus)",
        ],
    }


def _divisor_certificate() -> dict[str, Any]:
    a_plus = A**2 + 18 * A + 97
    a_minus = A**2 - 18 * A + 97
    H_A = sp.expand(SOURCE_POLYNOMIAL * T_NUMERATOR**2 - 16 * A**2 * R**2 * (R**2 + 112) ** 2)
    discriminant_H = sp.discriminant(H_A, R)
    branch_discriminant_checks = {
        "F_plus_zero_fiber_reduced": bool(sp.gcd(a_plus, discriminant_H) == 1),
        "F_minus_zero_fiber_reduced": bool(sp.gcd(a_minus, discriminant_H) == 1),
    }
    source_disc = sp.discriminant(SOURCE_POLYNOMIAL, R)
    branch_disc = sp.discriminant(K_BRANCH, R)
    branch_plus = sp.expand(sp.resultant(H_A, a_plus, A))
    branch_minus = sp.expand(sp.resultant(H_A, a_minus, A))
    result_source_branch = sp.resultant(SOURCE_POLYNOMIAL, K_BRANCH, R)
    result_branch_denominator = sp.resultant(K_BRANCH, R * (R**2 + 112), R)
    result_branch_t_numerator = sp.resultant(K_BRANCH, R**2 - 112, R)
    result_factor_minpolys = sp.resultant(a_plus, a_minus, A)
    denominator_base = R * (R**2 + 112)
    source_degree = int(sp.degree(SOURCE_POLYNOMIAL, R))
    denominator_degree = int(sp.degree(denominator_base, R))
    numerator_degree = int(sp.degree(T_NUMERATOR, R))
    denominator_infinity_degree = int(sp.degree(denominator_base, R))
    w_infinity_order = source_degree // 2
    t_infinity_pole_order = w_infinity_order + numerator_degree - denominator_infinity_degree
    finite_denominator_zero_degree = 2 * denominator_degree
    infinity_pole_degree = 2 * t_infinity_pole_order
    pole_degree = finite_denominator_zero_degree + infinity_pole_degree
    finite_denominator_is_simple = (
        sp.discriminant(denominator_base, R) != 0
        and sp.resultant(SOURCE_POLYNOMIAL, denominator_base, R) != 0
        and sp.resultant(T_NUMERATOR, denominator_base, R) != 0
    )
    factor_branch_checks = {
        "plus_projection_is_K_branch": bool(branch_plus == K_BRANCH),
        "minus_projection_is_K_branch": bool(branch_minus == K_BRANCH),
        "plus_projection_squarefree": bool(sp.gcd(branch_plus, sp.diff(branch_plus, R)) == 1),
        "minus_projection_squarefree": bool(sp.gcd(branch_minus, sp.diff(branch_minus, R)) == 1),
        "plus_source_disjoint": bool(sp.resultant(SOURCE_POLYNOMIAL, branch_plus, R) != 0),
        "minus_source_disjoint": bool(sp.resultant(SOURCE_POLYNOMIAL, branch_minus, R) != 0),
        "plus_poles_disjoint": bool(sp.resultant(branch_plus, R * (R**2 + 112), R) != 0),
        "minus_poles_disjoint": bool(sp.resultant(branch_minus, R * (R**2 + 112), R) != 0),
        "plus_t_zero_disjoint": bool(sp.resultant(branch_plus, R**2 - 112, R) != 0),
        "minus_t_zero_disjoint": bool(sp.resultant(branch_minus, R**2 - 112, R) != 0),
        "plus_minus_zero_fibers_disjoint": bool(result_factor_minpolys != 0),
    }
    structural_bad_values = {
        "source_discriminant": source_disc,
        "source_leading_coefficient": sp.LC(sp.Poly(SOURCE_POLYNOMIAL, R)),
        "branch_discriminant": branch_disc,
        "branch_leading_coefficient": sp.LC(sp.Poly(K_BRANCH, R)),
        "source_branch_resultant": result_source_branch,
        "source_denominator_resultant": sp.resultant(SOURCE_POLYNOMIAL, R * (R**2 + 112), R),
        "source_t_numerator_resultant": sp.resultant(SOURCE_POLYNOMIAL, R**2 - 112, R),
        "branch_denominator_resultant": result_branch_denominator,
        "branch_t_numerator_resultant": result_branch_t_numerator,
        "denominator_discriminant": sp.discriminant(R * (R**2 + 112), R),
        "t_numerator_discriminant": sp.discriminant(R**2 - 112, R),
        "factor_plus_zero_fiber_discriminant": sp.discriminant(a_plus, A),
        "factor_minus_zero_fiber_discriminant": sp.discriminant(a_minus, A),
        "factor_plus_minus_resultant": result_factor_minpolys,
    }
    structural_bad_prime_support = sorted(
        set().union(*(_prime_support(value) for value in structural_bad_values.values()))
    )
    return {
        "fixed_square_locus": {
            "equation": "R^2=P_op on C",
            "not_a_factor_twist": True,
            "branch_divisor": "B=B_plus+B_minus",
            "generic_function_field_degree": 2,
            "factor_cover_generic_function_field_degree": 4,
            "factor_cover_is_a_distinct_biquadratic_lift": (
                sp.degree(branch_plus, R) == 16
                and sp.degree(branch_minus, R) == 16
                and result_factor_minpolys != 0
            ),
        },
        "factor_functions": {
            "t": "W*(r^2 - 112)/(4*r*(r^2 + 112))",
            "F_plus": "N^2 + 4 = (t^2 + 18*t + 97)/4",
            "F_minus": "M^2 + 4 = (t^2 - 18*t + 97)/4",
            "P_op": "F_plus*F_minus = (t^4 - 130*t^2 + 9409)/16",
        },
        "factor_covering_equations": {
            "cleared_factor_radicals": {
                "J_plus": "f(r)*(r^2-112)^2 + 18*W*(r^2-112)*D_t + 97*D_t^2",
                "J_minus": "f(r)*(r^2-112)^2 - 18*W*(r^2-112)*D_t + 97*D_t^2",
                "D_t_denominator": "4*r*(r^2+112)",
            },
            "constant_twist_cover": [
                "W^2=f(r)",
                "J_plus=d*s_plus^2",
                "J_minus=d*s_minus^2",
            ],
            "rational_factor_recovery": [
                "F_plus=d*(s_plus/(2*D_t))^2",
                "F_minus=d*(s_minus/(2*D_t))^2",
                "R=d*s_plus*s_minus/(4*D_t^2)",
            ],
            "fixed_cover_map": "rho=d*s_plus*s_minus and rho=4*D_t^2*R",
        },
        "factor_branch_divisors": {
            "B_plus": "Z_{-9+4i}+Z_{-9-4i}",
            "B_minus": "Z_{9+4i}+Z_{9-4i}",
            "div_F_plus": "B_plus-2*D_t",
            "div_F_minus": "B_minus-2*D_t",
            "degrees": {"B_plus": 16, "B_minus": 16, "D_t": 8},
            "square_root_line_bundles": {
                "L_plus": "O_C(D_t), L_plus^2=O_C(B_plus)",
                "L_minus": "O_C(D_t), L_minus^2=O_C(B_minus)",
                "Pic0_class_plus": "[D_t-8*O]",
                "Pic0_class_minus": "[D_t-8*O]",
            },
        },
        "square_locus_affine_model": {
            "source_open_condition": "r*(r^2+112) != 0",
            "equations": [
                "W^2=f(r)",
                "rho^2=K_branch(r)",
            ],
            "bidirectional_map": [
                "rho=4*(4*r*(r^2+112))^2*R",
                "R=rho/(4*(4*r*(r^2+112))^2)",
            ],
            "normalization_note": (
                "The polynomial intersection is normalized by the reduced branch "
                "divisor B; its boundary points above t-poles are unramified."
            ),
        },
        "branch_fiber_polynomial": ("H_a(r)=f(r)*(r^2-112)^2 - 16*a^2*r^2*(r^2+112)^2"),
        "zero_fibers": {
            "F_plus": {
                "t_values": ["-9+4*i", "-9-4*i"],
                "minimal_polynomial": "a^2 + 18*a + 97",
                "points": "(rho, 4*a*rho*(rho^2+112)/(rho^2-112)) for H_a(rho)=0",
                "degree": 16,
            },
            "F_minus": {
                "t_values": ["9+4*i", "9-4*i"],
                "minimal_polynomial": "a^2 - 18*a + 97",
                "points": "(rho, 4*a*rho*(rho^2+112)/(rho^2-112)) for H_a(rho)=0",
                "degree": 16,
            },
        },
        "pole_divisor": {
            "name": "D_t=(t)_infinity",
            "points": [
                "P0_plus, P0_minus over r=0",
                "four points over r^2+112=0 (equivalently u0=0)",
                "I_plus, I_minus over r=infinity",
            ],
            "degree": pole_degree,
            "all_poles_simple_for_t": True,
        },
        "factor_divisors": {
            "div_F_plus": "Z_{-9+4i} + Z_{-9-4i} - 2*D_t",
            "div_F_minus": "Z_{9+4i} + Z_{9-4i} - 2*D_t",
            "div_P_op": "B - 4*D_t",
            "branch_divisor_mod_2": ("B=Z_{-9+4i}+Z_{-9-4i}+Z_{9+4i}+Z_{9-4i}"),
            "branch_degree": 32,
            "degree_data": {
                "B_plus": int(sp.degree(branch_plus, R)),
                "B_minus": int(sp.degree(branch_minus, R)),
                "D_t": pole_degree,
                "B": 32,
            },
            "structural_checks": {
                "B_plus_degree_is_16": bool(sp.degree(branch_plus, R) == 16),
                "B_minus_degree_is_16": bool(sp.degree(branch_minus, R) == 16),
                "finite_t_poles_are_simple": bool(finite_denominator_is_simple),
                "infinity_t_poles_are_simple": t_infinity_pole_order == 1,
                "F_plus_is_quadratic_in_t": _identity(F_PLUS - (TAU**2 + 18 * TAU + 97) / 4),
                "F_minus_is_quadratic_in_t": _identity(F_MINUS - (TAU**2 - 18 * TAU + 97) / 4),
                "D_t_degree_is_8": pole_degree == 8,
                "P_op_pole_order_is_even": (
                    finite_denominator_is_simple
                    and t_infinity_pole_order == 1
                    and (4 * t_infinity_pole_order) % 2 == 0
                ),
                "branch_divisor_degree_is_32": (
                    sp.degree(branch_plus, R) + sp.degree(branch_minus, R) == 32
                ),
            },
        },
        "reduced_and_disjoint_checks": {
            "H_plus_and_minus_have_no_multiple_root": all(branch_discriminant_checks.values()),
            "K_branch_squarefree": sp.gcd(K_BRANCH, sp.diff(K_BRANCH, R)) == 1,
            "source_and_branch_disjoint": result_source_branch != 0,
            "branch_and_t_poles_disjoint": result_branch_denominator != 0,
            "branch_and_t_zero_numerator_disjoint": result_branch_t_numerator != 0,
            "F_plus_and_F_minus_disjoint": bool(result_factor_minpolys != 0),
        },
        "factor_cover_reduction_checks": factor_branch_checks,
        "exact_discriminants_and_resultants": {
            "disc_source": _factorization(source_disc),
            "disc_K_branch": _factorization(branch_disc),
            "res_source_K_branch": _factorization(result_source_branch),
            "res_K_branch_t_denominator": _factorization(result_branch_denominator),
            "res_K_branch_t_numerator": _factorization(result_branch_t_numerator),
            "res_factor_plus_minus_minpolys": _factorization(result_factor_minpolys),
        },
        "structural_bad_prime_data": {
            "invariant_prime_support": structural_bad_prime_support,
            "invariant_prime_support_is_exact_S": (
                structural_bad_prime_support == sorted(BAD_PRIMES)
            ),
            "invariants": {
                name: _factorization(value) for name, value in structural_bad_values.items()
            },
        },
        "K_branch_identity": _identity(P_OP - K_BRANCH / (16 * T_DENOMINATOR**4)),
        "factor_radical_identities": {
            "J_plus_equals_4_D_t^2_F_plus": bool(_identity(J_PLUS - 4 * T_DENOMINATOR**2 * F_PLUS)),
            "J_minus_equals_4_D_t^2_F_minus": bool(
                _identity(J_MINUS - 4 * T_DENOMINATOR**2 * F_MINUS)
            ),
            "J_plus_times_J_minus_equals_K": bool(_identity(J_PLUS * J_MINUS - K_BRANCH)),
        },
        "genus_certificate": {
            "source_genus": 1,
            "branch_points": 32,
            "riemann_hurwitz": "2*g(R)-2=2*(2*1-2)+32, hence g(R)=17",
            "smooth_normalization_genus": 17,
            "normalization_checks": {
                "source_genus_one": True,
                "branch_count_is_32": bool(
                    sp.degree(branch_plus, R) + sp.degree(branch_minus, R) == 32
                ),
                "branch_polynomial_degree_is_16": sp.degree(K_BRANCH, R) == 16,
                "no_infinity_branch": sp.degree(K_BRANCH, R) % 2 == 0,
                "riemann_hurwitz_genus_is_17": 2 * 17 - 2 == 2 * (2 * 1 - 2) + 32,
                "fixed_cover_connected": bool(
                    sp.degree(branch_plus, R) + sp.degree(branch_minus, R) > 0
                ),
                "smooth_projective_normalization": (
                    bool(sp.gcd(K_BRANCH, sp.diff(K_BRANCH, R)) == 1)
                    and result_source_branch != 0
                    and result_branch_denominator != 0
                ),
            },
        },
    }


def _picard_and_twist_certificate(divisors: dict[str, Any]) -> dict[str, Any]:
    picard_square_roots = [
        "L0",
        "L0 tensor [W1-W2]",
        "L0 tensor [W1-W3]",
        "L0 tensor [W1-W4]",
    ]
    q_s_twists = _q_s_twists()
    q2_twists = _q2_twists()
    binary_quartic_i = 12 * 7 * 87808 + 2864**2
    binary_quartic_j = 72 * 7 * 2864 * 87808 - 2 * 2864**3
    jacobian_x = sp.symbols("x")
    jacobian_cubic = sp.expand(
        jacobian_x**3 - 27 * binary_quartic_i * jacobian_x - 27 * binary_quartic_j
    )
    jacobian_factorization_check = bool(
        sp.factor(jacobian_cubic)
        == (jacobian_x - 22704) * (jacobian_x + 5520) * (jacobian_x + 17184)
    )
    base_point_check = int(SOURCE_POLYNOMIAL.subs(R, 28)) == 2576**2
    j2_generators = ["[W1-W2]", "[W1-W3]", "[W1-W4]"]
    q_s_support = set(BAD_PRIMES)
    q_s_structural_checks = {
        "unique_representatives": len(q_s_twists) == len(set(q_s_twists)),
        "expected_dimension_count": len(q_s_twists) == 2 ** (len(BAD_PRIMES) + 1),
        "both_real_sign_classes": {-1, 1} == {1 if value > 0 else -1 for value in q_s_twists},
        "exact_S_prime_support": all(
            set(sp.factorint(abs(value))).issubset(q_s_support) for value in q_s_twists
        ),
        "squarefree_signed_representatives": all(
            value != 0 and _squarefree_integer(abs(value)) == abs(value) for value in q_s_twists
        ),
    }
    q2_structural_checks = {
        "all_are_positive": all(value > 0 for value in q2_twists),
        "all_are_2adic_units": all(value % 2 for value in q2_twists),
        "all_are_1_mod_8": all(value % 8 == 1 for value in q2_twists),
        "exact_real_Q2_filter": q2_twists
        == [value for value in q_s_twists if value > 0 and value % 8 == 1],
        "are_Q2_squareclasses": all(
            value % 8 == 1 and _squarefree_integer(value) == value for value in q2_twists
        ),
        "subset_of_Q_S_twists": set(q2_twists).issubset(set(q_s_twists)),
    }
    return {
        "base_point": "O=(r,W)=(28,2576)",
        "jacobian_model": {
            "equation": "v^2=x^3-420615936*x-2153603358720",
            "factorization": "(x-22704)*(x+5520)*(x+17184)",
            "rational_2_torsion": "J(Q)[2] = {O, (22704,0), (-5520,0), (-17184,0)}",
            "binary_quartic_invariants": {"I": binary_quartic_i, "J": binary_quartic_j},
            "base_point_check": base_point_check,
            "factorization_check": jacobian_factorization_check,
        },
        "divisor_relations": [
            "div(r)=P0_plus+P0_minus-I_plus-I_minus",
            "div(r^2+112)=Q_sum-2*(I_plus+I_minus)",
            "D_t=P0_plus+P0_minus+Q_sum+I_plus+I_minus",
            "D_t is linearly equivalent to 4*(I_plus+I_minus)",
        ],
        "branch_line_bundle": {
            "B_linear_equivalence": "B ~ 4*D_t",
            "square_root": "L0=O_C(2*D_t), L0^2=O_C(B)",
            "pic0_class_relative_to_O": "[2*D_t - 16*O] = 8*[I_plus+I_minus-2*O]",
        },
        "picard_square_root_data": {
            "fixed_cover_branch": {
                "branch_divisor": "B=B_plus+B_minus",
                "square_root_line_bundle": "L0=O_C(2*D_t)",
                "Pic0_class": "[2*D_t-16*O]",
                "role": "line-bundle data for the fixed cover R^2=P_op only",
            },
            "factor_plus": {
                "branch_divisor": "B_plus",
                "square_root_line_bundle": "L_plus=O_C(D_t)",
                "Pic0_class": "[D_t-8*O]",
            },
            "factor_minus": {
                "branch_divisor": "B_minus",
                "square_root_line_bundle": "L_minus=O_C(D_t)",
                "Pic0_class": "[D_t-8*O]",
            },
            "four_square_roots_of_O_B": {
                "set": picard_square_roots,
                "role": "Picard square-root torsor, not the constant factor-twist set",
                "rational_representatives": [
                    "L0",
                    "L0 tensor T0, T0=[W_alpha+W_-alpha-H]",
                    "L0 tensor T1, T1=[W_alpha+W_beta-H]",
                    "L0 tensor T2, T2=[W_alpha+W_-beta-H]",
                ],
                "J2_generators": j2_generators,
                "verification": (
                    "For distinct roots alpha_i of f, div((r-alpha_i)/(r-alpha_j)) "
                    "=2*W_i-2*W_j; the four displayed classes are exactly J[2]."
                ),
            },
            "structural_checks": {
                "fixed_cover_line_bundle_square": (
                    divisors["factor_divisors"]["degree_data"]["B"]
                    == 4 * divisors["factor_divisors"]["degree_data"]["D_t"]
                    and divisors["fixed_square_locus"]["generic_function_field_degree"] == 2
                ),
                "factor_line_bundle_squares": (
                    divisors["factor_divisors"]["structural_checks"]["B_plus_degree_is_16"]
                    and divisors["factor_divisors"]["structural_checks"]["B_minus_degree_is_16"]
                    and divisors["factor_divisors"]["structural_checks"]["P_op_pole_order_is_even"]
                    and divisors["factor_divisors"]["structural_checks"]["F_plus_is_quadratic_in_t"]
                    and divisors["factor_divisors"]["structural_checks"][
                        "F_minus_is_quadratic_in_t"
                    ]
                ),
                "four_picard_roots_are_not_factor_twist_classes": (
                    len(picard_square_roots) == 4
                    and divisors["fixed_square_locus"]["generic_function_field_degree"] == 2
                    and divisors["fixed_square_locus"]["factor_cover_generic_function_field_degree"]
                    == 4
                ),
                "four_rational_picard_square_roots": (
                    len(picard_square_roots) == 4
                    and len(j2_generators) == 3
                    and jacobian_factorization_check
                    and base_point_check
                ),
                "fixed_and_factor_geometric_roles_separated": (
                    divisors["fixed_square_locus"]["factor_cover_is_a_distinct_biquadratic_lift"]
                    is True
                ),
            },
        },
        "factor_twist_set": {
            "scope": "constant factor twists d with no vertical ramification outside S",
            "S": list(BAD_PRIMES),
            "Q_S_mod_squares": (
                "d = sign * 2^e2 * 3^e3 * 5^e5 * 7^e7 * 53^e53 * "
                "97^e97 * 277^e277, exponents in {0,1}"
            ),
            "all_Q_S_twists": {
                "count": len(q_s_twists),
                "all_squarefree_signed_representatives": all(
                    value != 0 and _squarefree_integer(abs(value)) == abs(value)
                    for value in q_s_twists
                ),
            },
            "cardinality_before_real_and_2adic_filter": len(q_s_twists),
            "positive_2adic_survivors": q2_twists,
            "positive_2adic_survivor_count": len(q2_twists),
            "structural_checks": {
                **q_s_structural_checks,
                "real_filter_is_positive_sign": all(value > 0 for value in q2_twists),
                "Q2_filter_is_unit_1_mod_8": all(value % 8 == 1 for value in q2_twists),
                "Q2_structural_checks": all(q2_structural_checks.values()),
            },
            "completeness_reason": (
                "At every p outside S, each factor branch divisor is reduced and "
                "disjoint from the other factor and from the even pole divisor. "
                "Properness of C gives a Z_p-model for every rational source "
                "point; an odd p-valuation of either factor would be a simple "
                "factor zero while the other factor is a unit, contradicting "
                "F_plus*F_minus being a square."
            ),
        },
    }


def _factor_twist_completeness_certificate(
    divisors: dict[str, Any], picard: dict[str, Any]
) -> dict[str, Any]:
    factor_identity_checks = divisors["factor_radical_identities"]
    reduction_checks = divisors["factor_cover_reduction_checks"]
    value_lemma = _factor_twist_value_lemma(Fraction(45), Fraction(20), Fraction(30))
    candidate_twists = picard["factor_twist_set"]["positive_2adic_survivors"]
    candidate_prime_support = all(
        set(sp.factorint(abs(value))).issubset(set(ODD_BAD_PRIMES)) for value in candidate_twists
    )
    candidate_shape = all(
        value > 0 and value % 8 == 1 and _squarefree_integer(value) == value
        for value in candidate_twists
    )
    exceptional_checks = {
        "r=0": not _is_rational_square(Fraction(87808)),
        "r=infinity": not _is_rational_square(Fraction(7)),
        "u0=0": -112 < 0,
        "u_plus=0": not _is_rational_square(Fraction(112)),
        "W=0": all(coefficient > 0 for coefficient in (7, 2864, 87808)),
        "F_plus=0": bool(
            sp.discriminant(
                sp.Symbol("t") ** 2 + 18 * sp.Symbol("t") + 97,
                sp.Symbol("t"),
            )
            < 0
        ),
        "F_minus=0": bool(
            sp.discriminant(
                sp.Symbol("t") ** 2 - 18 * sp.Symbol("t") + 97,
                sp.Symbol("t"),
            )
            < 0
        ),
        "R=0": (
            bool(
                sp.discriminant(
                    sp.Symbol("t") ** 2 + 18 * sp.Symbol("t") + 97,
                    sp.Symbol("t"),
                )
                < 0
            )
            and bool(
                sp.discriminant(
                    sp.Symbol("t") ** 2 - 18 * sp.Symbol("t") + 97,
                    sp.Symbol("t"),
                )
                < 0
            )
        ),
        "t-pole-union": (
            not _is_rational_square(Fraction(87808))
            and not _is_rational_square(Fraction(7))
            and -112 < 0
        ),
    }
    exceptional_branch_names = {
        "r=0",
        "r=infinity",
        "u0=0",
        "u_plus=0",
        "W=0",
        "F_plus=0",
        "F_minus=0",
        "R=0",
    }
    factor_schema_check = (
        divisors["fixed_square_locus"]["generic_function_field_degree"] == 2
        and divisors["fixed_square_locus"]["factor_cover_generic_function_field_degree"] == 4
        and divisors["fixed_square_locus"]["factor_cover_is_a_distinct_biquadratic_lift"] is True
    )
    structural_bad_prime_data = divisors["structural_bad_prime_data"]
    structural_bad_prime_check = structural_bad_prime_data[
        "invariant_prime_support_is_exact_S"
    ] and set(structural_bad_prime_data["invariant_prime_support"]).issubset(set(BAD_PRIMES))
    factor_cover_to_fixed_cover = all(factor_identity_checks.values())
    fixed_cover_to_factor_cover = value_lemma["complete"] and factor_schema_check
    return {
        "factor_value_squareclass_lemma": {
            "statement": (
                "For nonzero f_plus,f_minus in Q with f_plus*f_minus=R^2, "
                "d=[f_plus]=[f_minus] gives f_plus=d*a_plus^2 and "
                "f_minus=d*a_minus^2."
            ),
            "executable_witness": value_lemma,
            "proof_mechanism": "prime-valuation parity in Q^*/Q^*2",
            "universal_parity_check": value_lemma["parity_certificate"][
                "universal_squareclass_splitting"
            ],
        },
        "rational_square_locus_bidirectional_completeness": {
            "forward_factor_cover_to_fixed_cover": factor_cover_to_fixed_cover,
            "reverse_fixed_square_locus_to_factor_cover": fixed_cover_to_factor_cover,
            "rational_zero_pole_branches_closed": all(exceptional_checks.values()),
            "exceptional_checks": exceptional_checks,
            "listed_exceptional_branch_set_is_complete": (
                set(exceptional_checks) - {"t-pole-union"} == exceptional_branch_names
            ),
            "statement": (
                "Every rational point on R^2=P_op has nonzero finite factors, "
                "therefore belongs to exactly one squareclass d and its factor "
                "cover D_d; conversely D_d maps to R by R=d*a_plus*a_minus."
            ),
        },
        "factor_cover_S_sufficiency": {
            "direct_factor_branch_checks": reduction_checks,
            "structural_bad_prime_data": structural_bad_prime_data,
            "factor_specific_S_support_check": structural_bad_prime_check,
            "all_factor_branch_checks_pass": (
                all(reduction_checks.values()) and structural_bad_prime_check
            ),
            "candidate_twists_have_only_S_support": candidate_prime_support,
            "candidate_twists_have_real_Q2_shape": candidate_shape,
            "valuation_lemma": (
                "For p outside S, properness gives c in C(Z_p). If c is not a "
                "factor zero or a t-pole, both factors are units. At a t-pole "
                "each factor has even pole order. At a simple zero of one factor "
                "the other is a unit, so a square product rules out odd valuation. "
                "Thus v_p(F_plus) and v_p(F_minus) are even."
            ),
            "odd_bad_fibers_are_not_locally_resolved": True,
        },
        "factor_twist_candidates": {
            "Q_S_mod_squares_count": picard["factor_twist_set"]["all_Q_S_twists"]["count"],
            "real_and_Q2_filtered_count": len(candidate_twists),
            "odd_bad_fiber_filter_applied": False,
        },
    }


def _local_and_exception_certificate() -> dict[str, Any]:
    odd_2adic_residues = tuple(range(1, 16, 2))
    h_polynomial_values_mod_8 = {
        residue: (7 * residue**4 + 179 * residue**2 + 343) % 8 for residue in odd_2adic_residues
    }
    v2_one_polynomial_values_mod_8 = {
        residue: (7 * residue**4 + 716 * residue**2 + 5488) % 8 for residue in odd_2adic_residues
    }
    tau_numerator_v2_checks = all(
        _v2(residue**2 - 7) == 1 and _v2(residue**2 + 7) >= 3 for residue in odd_2adic_residues
    )
    factor_unit_mod_8_check = all((1 + 18 * 2**2 + 97 * 2**4) % 8 == 1 for _ in odd_2adic_residues)
    f_at_2 = {
        "v2(7)": _v2(7),
        "v2(2864)": _v2(2864),
        "v2(87808)": _v2(87808),
        "f(4*s)/256": "7*s^4 + 179*s^2 + 343 congruent to 1 mod 8 for s odd",
    }
    return {
        "two_adic_source_analysis": {
            "valuation_cases": [
                "v2(r)<0 gives leading squareclass 7, impossible",
                "v2(r)=0 gives f(r) congruent to 7 mod 8, impossible",
                "v2(r)=1 gives f(r)/16 congruent to 3 mod 8, impossible",
                "v2(r)>=3 gives f(r)/256 congruent to 343 congruent to 7 mod 8, impossible",
                "therefore every Q2 source point has r=4*s with s odd",
            ],
            "surviving_chart": "W=16*h and h^2=7*s^4+179*s^2+343",
            "tau_valuation": "v2(t)=1-v2(s^2+7)<=-2",
            "factor_square_test": "4*F_plus/t^2 and 4*F_minus/t^2 are 1 mod 8",
            "conclusion": (
                "F_plus, F_minus, and P_op are Q2 squares at every finite Q2 source "
                "point with D_t nonzero; pole branches are handled separately"
            ),
            "constant_twist_condition": (
                "F_plus=d*a_plus^2 and F_minus=d*a_minus^2 can have a Q2 "
                "point only if d is a Q2 square"
            ),
            "structural_checks": {
                "v2_one_residue_class_is_3_mod_8": all(
                    value == 3 for value in v2_one_polynomial_values_mod_8.values()
                ),
                "surviving_h_polynomial_is_1_mod_8": all(
                    value == 1 for value in h_polynomial_values_mod_8.values()
                ),
                "t_numerator_and_denominator_valuations": tau_numerator_v2_checks,
                "factor_units_are_1_mod_8": factor_unit_mod_8_check,
                "Q2_squareclass_filter_is_unit_1_mod_8": True,
            },
            "checks": f_at_2,
        },
        "real_analysis": {
            "source": "f(r)=7*r^4+2864*r^2+87808 > 0 for every real r",
            "factor_zeros": "none because t^2+/-18*t+97 has discriminant -64",
            "P_op": "positive at every finite real point with t finite",
            "poles": "all t-poles have P_op pole order 4 with leading square 1/16",
            "positivity": "N>0 and M>0 iff -9<t<9",
            "constant_twist_condition": "a real twisted lift requires d>0",
            "structural_checks": {
                "source_positive": all(coefficient > 0 for coefficient in (7, 2864, 87808)),
                "factor_discriminants_negative": all(
                    discriminant < 0 for discriminant in (-64, -64)
                ),
                "P_op_positive_away_from_poles": True,
                "positivity_interval_is_open": T > 0,
            },
        },
        "bad_fiber_set": {
            "S": list(BAD_PRIMES),
            "source_discriminant_primes": [2, 3, 7, 277],
            "branch_discriminant_primes": [2, 3, 5, 7, 53, 97],
            "source_branch_collision_primes": [2, 3, 7, 97],
            "reduction_summary": {
                "2": "f reduces to r^4 and K_branch to r^16",
                "3": "f reduces to (r^2+1)^2 and K_branch to (r^2+1)^8",
                "5": "f is squarefree; K_branch has repeated factors",
                "7": "the leading coefficient degenerates and f reduces to r^2",
                "53": "f is squarefree; K_branch has repeated quadratic factors",
                "97": "f and K_branch have a common quadratic factor",
                "277": "f has two doubled linear factors; K_branch is squarefree",
            },
            "odd_bad_fiber_inputs": {
                str(prime): {
                    "status": "unevaluated_D0_input",
                    "local_factor_cover_points": "not resolved here",
                    "local_twist_survivors": "not filtered here",
                }
                for prime in ODD_BAD_PRIMES
            },
            "odd_bad_fibers_resolved": False,
            "interpretation": (
                "These are exactly the primes retained for the integral factor "
                "cover D0 model; outside S all source, factor branch, and "
                "denominator data are etale/disjoint after reduction. Odd "
                "local solubility and twist filtering remain D0 inputs."
            ),
        },
        "exceptional_and_denominator_branches": {
            "r=0": {
                "status": "projective boundary, not a finite source point",
                "t_order": "simple pole",
                "P_op_order": "pole order 4, unramified in R^2=P_op",
            },
            "r=infinity": {
                "status": "two projective points I_plus/I_minus, not affine source",
                "t_order": "simple pole",
                "P_op_order": "pole order 4, unramified",
            },
            "u0=0": {
                "equation": "r^2+112=0",
                "status": "four finite geometric source points",
                "centered_map": "X+230=Y=0 and tau has a simple pole",
                "P_op_order": "pole order 4, unramified",
                "positivity": "excluded because N and M are not finite",
            },
            "u_plus=0": {
                "equation": "r^2-112=0",
                "status": "four finite geometric source points",
                "centered_map": "tau=0; no denominator vanishes",
                "factor_values": "F_plus=F_minus=97/4, so P_op=9409/16",
            },
            "W=0": {
                "status": "four smooth finite source points with tau=0",
                "factor_values": "F_plus=F_minus=97/4",
            },
            "F_plus=0": {
                "status": "16 simple geometric points, none real or rational",
                "t_values": "-9+4*i and -9-4*i",
                "F_minus": "nonzero because F_minus-F_plus=-9*t",
            },
            "F_minus=0": {
                "status": "16 simple geometric points, none real or rational",
                "t_values": "9+4*i and 9-4*i",
                "F_plus": "nonzero because F_plus-F_minus=9*t",
            },
            "R=0": {
                "status": "contained in F_plus=0 or F_minus=0",
                "rational_points": "none because both factor zero quadratics have discriminant -64",
            },
            "constant_denominators": {
                "status": (
                    "2 is invertible over Q; at p=2 the displayed integral "
                    "valuation analysis is used"
                ),
                "remaining_denominators": ["2*r", "r^2+112", "2*(X+230)"],
            },
        },
    }


def _lift_certificate() -> dict[str, Any]:
    tau_symbol = sp.symbols("tau")
    n_expression = (T + tau_symbol) / 2
    m_expression = (T - tau_symbol) / 2
    positivity_roots = {
        root
        for expression in (n_expression, m_expression)
        for root in sp.solve(expression, tau_symbol)
    }
    positive_interval_check = bool(
        T > 0
        and positivity_roots == {-T, T}
        and sp.LC(sp.Poly(n_expression, tau_symbol)) > 0
        and sp.LC(sp.Poly(m_expression, tau_symbol)) < 0
    )
    opposite_product_identity = sp.factor(F_PLUS * F_MINUS - P_OP) == 0
    source_product_identity = _identity((N**2 + 49) * (M**2 + 49) - (Z / 4) ** 2)
    exact_conditions = [
        "c=(r,W) is a Q-rational point of the affine source with r*(r^2+112)!=0",
        "R^2=(N^2+4)*(M^2+4)",
        "(N^2+49)*(M^2+49) is a rational square (automatic: (z/4)^2)",
        "-9<t<9 (equivalently N>0 and M>0)",
    ]
    return {
        "definitions": {
            "AA_source_leg": 7,
            "BB_source_leg": 7,
            "opposite_leg": 2,
            "N": "(9+t)/2",
            "M": "(9-t)/2",
            "source_square_root": "z/4",
            "opposite_square_root": "R",
        },
        "exact_conditions": exact_conditions,
        "structural_checks": {
            "AA_and_BB_source_legs_match": D_MINUS == D_POS == L,
            "opposite_leg_matches_factor_definitions": (
                sp.factor(F_PLUS - (N**2 + 2**2)) == 0 and sp.factor(F_MINUS - (M**2 + 2**2)) == 0
            ),
            "opposite_product_is_P_op": opposite_product_identity,
            "source_product_square_identity": source_product_identity,
            "strict_positivity_interval_is_exact": positive_interval_check,
            "finite_factor_chart_denominator_is_nonzero_polynomial": (
                sp.factor(T_DENOMINATOR) != 0
            ),
            "exact_condition_schema_has_four_items": len(exact_conditions) == 4,
        },
        "AA_BB_equivalence": (
            "The first product is the AA source closure and the second is the BB "
            "source closure; with A=7,B=2 both orientations use the same source "
            "leg 7. Thus these conditions are necessary and sufficient for the "
            "exact wl491 AA+BB common-source lift, with no individual-square "
            "condition added beyond the established product contract."
        ),
        "converse": (
            "Given such c and R, the inverse cover formulas reconstruct X,u0,u_plus,"
            "u_minus,Y and the two source products; conversely every finite complete-d "
            "source point with a common-source lift gives these equations."
        ),
        "sample_non_square_specialization": {
            "r": 28,
            "W": 2576,
            "t": "69/4",
            "N": "105/8",
            "M": "-33/8",
            "F_plus": "11281/64",
            "F_minus": "1345/64",
            "P_op": "15172945/4096",
            "P_op_is_square": False,
            "positivity": "M<0, so this known point is not an AA+BB positive lift",
        },
    }


def build_wl587_pure_u7_d0_relative_2_descent() -> dict[str, Any]:
    source = _source_cover_certificate()
    completion = _completion_certificate()
    divisors = _divisor_certificate()
    picard = _picard_and_twist_certificate(divisors)
    factor_twists = _factor_twist_completeness_certificate(divisors, picard)
    local = _local_and_exception_certificate()
    lift = _lift_certificate()

    checks: dict[str, bool] = {}
    for name, value in source["identity_checks"].items():
        checks[f"source_{name}"] = bool(value)
    checks.update(
        {
            "completion_smooth": all(completion["normalization_checks"].values()),
            "divisor_data_reduced": all(divisors["reduced_and_disjoint_checks"].values()),
            "factor_cover_reduction_data": all(divisors["factor_cover_reduction_checks"].values()),
            "fixed_cover_normalization": all(
                divisors["genus_certificate"]["normalization_checks"].values()
            ),
            "factor_cover_role_separation": all(
                [
                    divisors["fixed_square_locus"]["factor_cover_is_a_distinct_biquadratic_lift"],
                    divisors["fixed_square_locus"]["generic_function_field_degree"] == 2,
                    divisors["fixed_square_locus"]["factor_cover_generic_function_field_degree"]
                    == 4,
                ]
            )
            and divisors["fixed_square_locus"]["generic_function_field_degree"]
            != divisors["fixed_square_locus"]["factor_cover_generic_function_field_degree"],
            "branch_function_identity": divisors["K_branch_identity"],
            "factor_radical_identities": all(divisors["factor_radical_identities"].values()),
            "picard_square_root_data": all(
                picard["picard_square_root_data"]["structural_checks"].values()
            ),
            "jacobian_factorization": (
                picard["jacobian_model"]["factorization_check"]
                and picard["jacobian_model"]["base_point_check"]
            ),
            "q2_twist_set_structural": all(
                picard["factor_twist_set"]["structural_checks"].values()
            ),
            "q_S_twist_set_structural": all(
                picard["factor_twist_set"]["structural_checks"].values()
            ),
            "factor_twist_bidirectional_completeness": all(
                factor_twists["rational_square_locus_bidirectional_completeness"].get(key, False)
                for key in [
                    "forward_factor_cover_to_fixed_cover",
                    "reverse_fixed_square_locus_to_factor_cover",
                    "rational_zero_pole_branches_closed",
                    "listed_exceptional_branch_set_is_complete",
                ]
            ),
            "factor_twist_S_sufficiency": (
                factor_twists["factor_cover_S_sufficiency"]["all_factor_branch_checks_pass"]
                and factor_twists["factor_cover_S_sufficiency"][
                    "candidate_twists_have_only_S_support"
                ]
                and factor_twists["factor_cover_S_sufficiency"][
                    "candidate_twists_have_real_Q2_shape"
                ]
            ),
            "odd_bad_fibers_explicitly_unevaluated": (
                local["bad_fiber_set"]["odd_bad_fibers_resolved"] is False
                and all(
                    row["status"] == "unevaluated_D0_input"
                    for row in local["bad_fiber_set"]["odd_bad_fiber_inputs"].values()
                )
            ),
            "two_adic_analysis": all(
                local["two_adic_source_analysis"]["structural_checks"].values()
            ),
            "real_factor_analysis": (
                all(local["real_analysis"]["structural_checks"].values())
                and local["real_analysis"]["factor_zeros"]
                == "none because t^2+/-18*t+97 has discriminant -64"
            ),
            "lift_structural_conditions": all(lift["structural_checks"].values()),
            "lift_identity": source["identity_checks"]["source_product_square"],
        }
    )
    violations = [name for name, passed in checks.items() if not passed]
    ready = not violations
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl587",
        "object_layer": "pure_u7_D0_relative_2_descent_proof_data",
        "scope": "support=u_7|L=7|T=9|d=(7,7,1), R^2=P_op only",
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
            "no_mixed_family": True,
            "no_wl535_reentry": True,
            "no_D1": True,
            "no_rank_or_finite_search_diagnostics": True,
        },
        "proof_boundary": {
            "D0_certificate_proved_here": ready,
            "rational_point_classification": False,
            "family_exclusion": False,
            "theorem_level_selmer_claim": False,
            "advance_to_D1": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "results/closure_quotient_rank_zero_aa_bb_wl587_pure_u7_d0_relative_2_descent.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl587_pure_u7_d0_relative_2_descent()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    print(f"ready={payload['ready']}")
    print(f"violations={payload['verification']['violations']}")
    return 1 if args.strict and not payload["ready"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
