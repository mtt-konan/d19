#!/usr/bin/env python3
"""Exact B0 covering certificate for the committed Berry degree-six pilot.

This file freezes only the two genus-2 covers attached to the selected
sextic. It checks the weighted projective models, boundary charts, the map to
the genus-5 Berry pullback and its support-theoretic converse, all Berry node
and coordinate-zero fibers, and finite bad-place supports. It also separates
the actual curve reduction audit from the bad support of the displayed
integral equations. It deliberately does not search for points or make rank,
Selmer, or Jacobian claims.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json


t, A, B = sp.symbols("t A B")
GAUSSIAN_I = sp.I
SQRT2 = sp.sqrt(2)


def _homogenize(
    poly: sp.Expr,
    variable: sp.Symbol,
    first: sp.Expr,
    second: sp.Expr,
    degree: int,
) -> sp.Expr:
    polynomial = sp.Poly(poly, variable)
    return sp.expand(
        sum(
            coefficient * first ** power[0] * second ** (degree - power[0])
            for power, coefficient in polynomial.terms()
        )
    )


def _conjugate(poly: sp.Expr) -> sp.Expr:
    return sp.expand(sp.conjugate(poly).xreplace({sp.conjugate(t): t}))


def berry_coordinates() -> dict[str, sp.Expr]:
    """Return the one committed Berry degree-six parameterization."""
    return {
        "X": t**6 + 6 * t**5 + 29 * t**4 + 44 * t**3 - 13 * t**2 - 2 * t - 1,
        "Y": t**6 + 12 * t**5 + 21 * t**4 - 16 * t**3 - 21 * t**2 + 4 * t - 1,
        "Z": t**6 + 4 * t**5 + 7 * t**4 + 24 * t**3 + 39 * t**2 - 12 * t + 1,
        "T": 10 * t**5 + 40 * t**4 + 28 * t**3 - 24 * t**2 + 10 * t,
    }


def g6_polynomial() -> sp.Expr:
    """Return the selected factor over K=Q(i)."""
    return sp.expand(
        t**6
        + (-2 - 2 * GAUSSIAN_I) * t**5
        + (-35 - 8 * GAUSSIAN_I) * t**4
        + (-52 - 28 * GAUSSIAN_I) * t**3
        + (19 - 40 * GAUSSIAN_I) * t**2
        + (6 + 14 * GAUSSIAN_I) * t
        - 1
    )


def _is_irreducible_factor_list(
    factor_list: tuple[sp.Expr, list[tuple[sp.Expr, int]]],
    variable: sp.Symbol,
    degree: int,
) -> bool:
    _, factors = factor_list
    return len(factors) == 1 and factors[0][1] == 1 and sp.degree(factors[0][0], variable) == degree


def _monic_gcd(expressions: list[sp.Expr], extension: sp.Expr | None = None) -> sp.Expr:
    polynomial = sp.Poly(expressions[0], t, extension=extension)
    for expression in expressions[1:]:
        polynomial = sp.gcd(polynomial, sp.Poly(expression, t, extension=extension))
    return sp.expand(polynomial.monic().as_expr())


def _node_data() -> list[tuple[str, tuple[sp.Expr, ...], sp.Expr, bool]]:
    h = t**4 + 12 * t**3 + 22 * t**2 - 4 * t + 1
    return [
        ("A++", (1, 1, 1, 0), sp.Integer(1), True),
        ("A+-", (1, 1, -1, 0), t, False),
        ("A-+", (1, -1, 1, 0), sp.Integer(1), False),
        ("A--", (1, -1, -1, 0), sp.Integer(1), False),
        ("B++", (1, 0, 1, 1), t - 1, False),
        ("B+-", (1, 0, 1, -1), h, False),
        ("B-+", (1, 0, -1, 1), t + 1, False),
        ("B--", (1, 0, -1, -1), sp.Integer(1), False),
        ("C+1", (0, 1, SQRT2, 1), sp.Integer(1), False),
        ("C+-1", (0, 1, SQRT2, -1), t + 1 + SQRT2, False),
        ("C-1", (0, 1, -SQRT2, 1), sp.Integer(1), False),
        ("C--1", (0, 1, -SQRT2, -1), t + 1 - SQRT2, False),
        ("D++", (SQRT2, 1, 0, 1), sp.Integer(1), False),
        ("D+-", (SQRT2, 1, 0, -1), sp.Integer(1), False),
        ("D-+", (-SQRT2, 1, 0, 1), sp.Integer(1), False),
        ("D--", (-SQRT2, 1, 0, -1), sp.Integer(1), False),
    ]


def _actual_reduction_audit() -> tuple[dict[str, Any], dict[str, bool]]:
    """Record the actual-reduction result and the unresolved dyadic gap.

    The odd prime ``(94*i-169)`` is settled by a nonintegral absolute Igusa
    invariant, independently of the chosen integral sextic model. At
    ``(1+i)`` the exact calculations below are only for fixed-center radial
    lattices. They do not classify the right PGL2(O) directions in the
    Bruhat-Tits tree, so no actual dyadic conclusion is asserted.
    """
    p = 37397
    residue_i = 1991
    j1_numerator_real = 580427774
    j1_numerator_imaginary = 23671901
    j1_residue = (j1_numerator_real + residue_i * j1_numerator_imaginary) % p
    igusa_invariants = {
        "j1": "(23671901*i + 580427774)/37397",
        "j2": "(-157525606640*i - 91084807952)/37397",
        "j3": "(-53747630344*i - 24975272704)/37397",
    }
    audit = {
        "normalization": {
            "dyadic_uniformizer": "varpi=1+i, v_varpi(varpi)=1",
            "odd_prime": "pi=94*i-169, Norm(pi)=37397, v_pi(pi)=1",
        },
        "criterion_at_pi": {
            "criterion": (
                "At residue characteristic 37397, good reduction gives an "
                "integral binary sextic with unit discriminant, so every absolute "
                "Igusa invariant lies in O_(K_pi)."
            ),
            "absolute_igusa_invariant": igusa_invariants["j1"],
            "residue_map": "i -> 1991 in F_37397 because 94*1991=169 mod 37397",
            "numerator_residue": str(j1_residue),
            "valuation": "v_pi(j1)=-1",
            "conclusion": "actual bad reduction, not just badness of the displayed model",
        },
        "twist_invariance": {
            "equations": ["d=1: v^2=g6", "d=i: v^2=(-i)*g6"],
            "absolute_invariants": "identical for the two unit quadratic twists",
            "pi_conclusion": "both twists have actual bad reduction at pi",
            "varpi_conclusion": "twist dependence remains unresolved with the dyadic gap",
            "twist_changes_varpi_answer": None,
        },
        "at_varpi": {
            "displayed_reduction": "i=1 and g6(t)=(t+1)^6 in k_varpi[t]",
            "displayed_model_status": "singular",
            "absolute_igusa_invariants": igusa_invariants,
            "invariant_integrality": (
                "37397 is a varpi-unit, so all three displayed absolute Igusa "
                "invariants are varpi-integral"
            ),
            "criterion": (
                "A complete obstruction would have to classify every smooth "
                "integral generalized model Y^2+Q(X)Y=P(X), deg(Q)<=3, "
                "deg(P)<=6, arising from every quotient lattice in the "
                "Bruhat-Tits tree. The calculations below audit only the fixed "
                "center z=t+1 radial slices."
            ),
            "normal_form": {
                "uniformizer": "pi=1+i, 2=-i*pi^2, pi^4=-4",
                "shifted_polynomial": (
                    "H(z)=g6(z-1)=z^6+(-2*i-8)z^5+(2*i-10)z^4+ "
                    "(-16*i+48)z^3+16*i*z^2+(32*i-64)z+32-32*i"
                ),
                "coefficient_valuations_low_to_high": [11, 10, 8, 9, 3, 2, 0],
                "unit_data": {
                    "H5_over_pi2": "4*i-1, residue 1",
                    "H0_over_pi11": "-1, residue 1",
                },
                "coordinate_reduction": (
                    "The fixed-center audit uses z=pi^r*X with r in Z. Cartan "
                    "double-coset data alone does not remove the right "
                    "PGL2(O_(varpi)) factor, which changes the branch sextic."
                ),
                "r_ge_2": (
                    "Fixed-center result only: the radial raw binary sextic has "
                    "odd content v_pi=11. This is not a global tree-direction "
                    "obstruction."
                ),
                "r_le_1": {
                    "normalized_sextic": "F_r=pi^(-6*r)*H(pi^r*X)",
                    "top_valuations": "v_pi([X^6]F_r)=0, v_pi([X^5]F_r)=2-r, v_pi([X^4]F_r)=3-2*r",
                    "d=1": (
                        "Fixed-center result only: for r=1,0,-1 the X^5/X^4 "
                        "valuations forbid a square modulo pi^4; for r<=-2 the "
                        "displayed radial residual forms are singular."
                    ),
                    "d=i": (
                        "Fixed-center result only: the radial X^6 coefficient is "
                        "-i and the corresponding square congruence fails modulo "
                        "pi^2. Other tree directions remain unaudited."
                    ),
                },
                "infinity_covered": (
                    "The fixed-center reciprocal chart is checked, but this does "
                    "not replace the missing full projective tree audit."
                ),
                "conclusion": (
                    "The fixed-center radial calculation is not an intrinsic "
                    "bad-reduction certificate. Actual dyadic reduction remains "
                    "unresolved for both twists."
                ),
            },
            "criterion_status": "fixed-center radial audit only; not complete",
            "d=1": "unresolved actual reduction",
            "d=i": "unresolved actual reduction",
        },
        "outside_remaining_places": {
            "d=1": "good reduction at every finite prime outside {varpi, pi}",
            "d=i": "good reduction at every finite prime outside {varpi, pi}",
            "proof": (
                "2 and Disc(g6) are units there, so the displayed weighted model "
                "has smooth affine and infinity reductions; the twist coefficient "
                "i is a unit."
            ),
        },
        "actual_reduction_status": {
            "d=1": {
                "good_proved": "outside {varpi, pi}",
                "bad_proved": "{pi}",
                "unresolved": "{varpi}",
            },
            "d=i": {
                "good_proved": "outside {varpi, pi}",
                "bad_proved": "{pi}",
                "unresolved": "{varpi}",
            },
        },
        "resolved": False,
        "blocker": (
            "Classify every quotient P1 lattice over K_(1+i), including all "
            "Bruhat-Tits-tree directions and centers after the right "
            "PGL2(O_(varpi)) factor, then construct or obstruct the resulting "
            "smooth proper generalized model for both twists."
        ),
    }
    checks = {
        "pi_j1_numerator_residue": j1_residue == 15271,
        "pi_j1_obstruction": j1_residue != 0,
        "twist_invariant_audit_recorded": (
            audit["twist_invariance"]["absolute_invariants"]
            == "identical for the two unit quadratic twists"
        ),
        "dyadic_fixed_center_audit_recorded": (
            audit["at_varpi"]["criterion_status"] == "fixed-center radial audit only; not complete"
        ),
        "dyadic_full_tree_gap_recorded": ("Bruhat-Tits-tree directions" in audit["blocker"]),
        "outside_good_reduction_recorded": all(
            audit["outside_remaining_places"][key].startswith("good reduction")
            for key in ("d=1", "d=i")
        ),
    }
    return audit, checks


def _node_fiber_audit(
    coordinates: dict[str, sp.Expr], homogeneous: dict[str, sp.Expr]
) -> tuple[dict[str, Any], dict[str, bool]]:
    affine_coordinates = [coordinates[name] for name in ("X", "Y", "Z", "T")]
    homogeneous_coordinates = [homogeneous[name] for name in ("X", "Y", "Z", "T")]
    Xs, Ys, Zs, Ts = sp.symbols("Xs Ys Zs Ts")
    surface = 2 * (Ys**4 + Ts**4) + Xs**4 + Zs**4 - 2 * (Xs**2 + Zs**2) * (Ys**2 + Ts**2)
    surface_gradient = [sp.diff(surface, variable) for variable in (Xs, Ys, Zs, Ts)]

    fibers: dict[str, Any] = {}
    checks: dict[str, bool] = {"node_count_is_16": len(_node_data()) == 16}
    for label, node, expected, expected_infinity in _node_data():
        extension = SQRT2 if any(sp.sympify(value).has(SQRT2) for value in node) else None
        minors = [
            sp.expand(affine_coordinates[i] * node[j] - affine_coordinates[j] * node[i])
            for i in range(4)
            for j in range(i + 1, 4)
        ]
        actual = _monic_gcd(minors, extension=extension)
        homogeneous_minors = [
            sp.expand(homogeneous_coordinates[i] * node[j] - homogeneous_coordinates[j] * node[i])
            for i in range(4)
            for j in range(i + 1, 4)
        ]
        at_infinity = all(sp.expand(minor.subs({A: 1, B: 0})) == 0 for minor in homogeneous_minors)
        node_substitution = {Xs: node[0], Ys: node[1], Zs: node[2], Ts: node[3]}
        node_is_singular = sp.expand(surface.subs(node_substitution)) == 0 and all(
            sp.expand(derivative.subs(node_substitution)) == 0 for derivative in surface_gradient
        )
        fibers[label] = {
            "node": [str(value) for value in node],
            "finite_parameter_gcd": str(actual),
            "infinity_fiber": at_infinity,
        }
        checks[f"node_{label}_is_singular"] = node_is_singular
        checks[f"node_{label}_finite_fiber"] = sp.expand(actual - expected) == 0
        checks[f"node_{label}_infinity_fiber"] = at_infinity is expected_infinity
    checks["node_fiber_audit_complete"] = all(
        checks[name] for name in checks if name.startswith("node_")
    )
    return fibers, checks


def build_b0_certificate() -> dict[str, Any]:
    row = berry_coordinates()
    X, Y, Z, T = (row[name] for name in ("X", "Y", "Z", "T"))
    g = g6_polynomial()
    gbar = _conjugate(g)
    f = sp.expand(X**2 + Z**2 - Y**2)
    F = _homogenize(f, t, A, B, 12)
    homogeneous = {
        "X": _homogenize(X, t, A, B, 6),
        "Y": _homogenize(Y, t, A, B, 6),
        "Z": _homogenize(Z, t, A, B, 6),
        "T": B * _homogenize(T, t, A, B, 5),
    }
    h = t**4 + 12 * t**3 + 22 * t**2 - 4 * t + 1
    t_zero_quartic = 5 * t**4 + 20 * t**3 + 14 * t**2 - 12 * t + 5
    x_zero_quartic = t**4 + 4 * t**3 + 22 * t**2 + 4 * t + 1
    x_zero_quadratic = t**2 + 2 * t - 1
    reciprocal = sp.expand(t**6 * g.subs(t, 1 / t))
    inverse_one = sp.expand((X - 2 * Y - Z) - t * (Z - X))
    inverse_two = sp.expand((-X + 3 * Y + 2 * Z + T) - t * (X - Y + T))
    node_fibers, node_checks = _node_fiber_audit(row, homogeneous)

    factor_list_f = sp.factor_list(f)
    factor_list_g = sp.factor_list(g, extension=GAUSSIAN_I)
    factor_list_gbar = sp.factor_list(gbar, extension=GAUSSIAN_I)
    gcd_coordinates = sp.gcd(sp.gcd(X, Y), sp.gcd(Z, T))
    disc_g = sp.discriminant(g, t)
    disc_gbar = sp.discriminant(gbar, t)
    disc_f = sp.discriminant(f, t)
    disc_h = sp.discriminant(h, t)
    disc_t_zero_quartic = sp.discriminant(t_zero_quartic, t)
    disc_x_zero_quartic = sp.discriminant(x_zero_quartic, t)
    disc_x_zero_quadratic = sp.discriminant(x_zero_quadratic, t)
    disc_z = sp.discriminant(Z, t)
    resultant = sp.resultant(g, gbar, t)
    expected_disc_g = sp.expand((GAUSSIAN_I - 1) ** 75 * (94 * GAUSSIAN_I - 169))
    expected_disc_gbar = _conjugate(expected_disc_g)
    actual_reduction, reduction_checks = _actual_reduction_audit()

    p = 37397
    i_mod_p = 1991
    g_coefficients = [
        1,
        -2 - 2 * GAUSSIAN_I,
        -35 - 8 * GAUSSIAN_I,
        -52 - 28 * GAUSSIAN_I,
        19 - 40 * GAUSSIAN_I,
        6 + 14 * GAUSSIAN_I,
        -1,
    ]
    g_mod_p = sp.Poly(
        sum(
            (int(sp.re(coefficient)) + i_mod_p * int(sp.im(coefficient))) * t ** (6 - index)
            for index, coefficient in enumerate(g_coefficients)
        ),
        t,
        modulus=p,
    )
    expected_g_mod_p = sp.Poly(
        (t - 11745) ** 2 * (t + 3615) * (t + 9390) * (t**2 + 6501 * t - 12218),
        t,
        modulus=p,
    )
    g_mod_2 = sp.Poly(
        sum(
            (int(sp.re(coefficient)) + int(sp.im(coefficient))) * t ** (6 - index)
            for index, coefficient in enumerate(g_coefficients)
        ),
        t,
        modulus=2,
    )
    expected_g_mod_2 = sp.Poly((t + 1) ** 6, t, modulus=2)

    reciprocal_expected = sp.expand(
        1
        + (-2 - 2 * GAUSSIAN_I) * t
        + (-35 - 8 * GAUSSIAN_I) * t**2
        + (-52 - 28 * GAUSSIAN_I) * t**3
        + (19 - 40 * GAUSSIAN_I) * t**4
        + (6 + 14 * GAUSSIAN_I) * t**5
        - t**6
    )
    checks = {
        "surface_equation": sp.expand(
            2 * (Y**4 + T**4) + X**4 + Z**4 - 2 * (X**2 + Z**2) * (Y**2 + T**2)
        )
        == 0,
        "pullback_factorization": sp.expand(f - g * gbar) == 0,
        "g_irreducible_over_K": _is_irreducible_factor_list(factor_list_g, t, 6),
        "gbar_irreducible_over_K": _is_irreducible_factor_list(factor_list_gbar, t, 6),
        "f_irreducible_over_Q": _is_irreducible_factor_list(factor_list_f, t, 12),
        "g_squarefree": sp.gcd(g, sp.diff(g, t), extension=GAUSSIAN_I) == 1,
        "gbar_squarefree": sp.gcd(gbar, sp.diff(gbar, t), extension=GAUSSIAN_I) == 1,
        "f_squarefree": sp.gcd(f, sp.diff(f, t)) == 1,
        "resultant_g_gbar": resultant == 2**40,
        "disc_g_factorization": sp.expand(disc_g - expected_disc_g) == 0,
        "disc_gbar_factorization": sp.expand(disc_gbar - expected_disc_gbar) == 0,
        "disc_f_factorization": disc_f == 2**155 * 37397,
        "weighted_model_basepoint_free": (
            gcd_coordinates == 1 and homogeneous["X"].subs({A: 1, B: 0}) == 1
        ),
        "reciprocal_chart_identity": sp.expand(reciprocal - reciprocal_expected) == 0,
        "inverse_relation_one": inverse_one == 0,
        "inverse_relation_two": inverse_two == 0,
        "h_irreducible_over_Q": _is_irreducible_factor_list(sp.factor_list(h), t, 4),
        "h_squarefree": sp.gcd(h, sp.diff(h, t)) == 1,
        "h_discriminant": disc_h == -(2**16) * 43,
        "t_zero_factorization": sp.expand(T - 2 * t * t_zero_quartic) == 0,
        "t_zero_quartic_discriminant": disc_t_zero_quartic == 2**20 * 5,
        "t_zero_quartic_squarefree": sp.gcd(t_zero_quartic, sp.diff(t_zero_quartic, t)) == 1,
        "t_zero_quartic_has_no_Q_root": sp.ground_roots(t_zero_quartic, t) == {},
        "t_zero_has_only_rational_root_zero": sp.ground_roots(T, t) == {sp.Integer(0): 1},
        "y_zero_factorization": sp.expand(Y - (t - 1) * (t + 1) * h) == 0,
        "x_zero_factorization": sp.expand(X - x_zero_quadratic * x_zero_quartic) == 0,
        "x_zero_factors_disjoint": sp.gcd(x_zero_quadratic, x_zero_quartic) == 1,
        "x_zero_squarefree": sp.gcd(X, sp.diff(X, t)) == 1,
        "x_zero_quartic_squarefree": sp.gcd(x_zero_quartic, sp.diff(x_zero_quartic, t)) == 1,
        "x_zero_quartic_has_no_Q_root": sp.ground_roots(x_zero_quartic, t) == {},
        "x_zero_quartic_discriminant": disc_x_zero_quartic == 2**21,
        "x_zero_quadratic_discriminant": disc_x_zero_quadratic == 2**3,
        "z_zero_squarefree": sp.gcd(Z, sp.diff(Z, t)) == 1,
        "z_zero_has_no_Q_root": sp.ground_roots(Z, t) == {},
        "z_zero_discriminant": disc_z == -(2**31) * 53,
        "denominator_one_factorization": sp.expand((Z - X) + 2 * (t - 1) * h) == 0,
        "denominator_two_factorization": sp.expand((X - Y + T) - 4 * t * h) == 0,
        "coordinate_forms_have_no_affine_common_root": gcd_coordinates == 1,
        "infinity_image": [homogeneous[name].subs({A: 1, B: 0}) for name in ("X", "Y", "Z", "T")]
        == [1, 1, 1, 0],
        "zero_image": [row[name].subs(t, 0) for name in ("X", "Y", "Z", "T")] == [-1, -1, 1, 0],
        "f_at_zero": f.subs(t, 0) == 1,
        "f_at_one": f.subs(t, 1) == 2**13,
        "f_at_minus_one": f.subs(t, -1) == 2**11,
        "f_at_infinity": F.subs({A: 1, B: 0}) == 1,
        "node_boundary_identity": all(
            sp.rem(expression, h, t) == 0 for expression in (Y, X - Z, T + Z, f - 2 * Z**2)
        ),
        "g_mod_pi_factorization": g_mod_p == expected_g_mod_p,
        "g_mod_pi_has_one_double_root": sp.degree(sp.gcd(g_mod_p, g_mod_p.diff())) == 1,
        "g_mod_pi2_factorization": g_mod_2 == expected_g_mod_2,
        "branch_factor_disjoint": sp.gcd(g, gbar, extension=GAUSSIAN_I) == 1,
        "branch_points_not_rational": sp.ground_roots(f, t) == {},
        "node_checks_complete": all(node_checks.values()),
    }
    checks.update(reduction_checks)

    twist_data = {
        "d=1": {
            "affine_equation": "v^2=g6(t)",
            "weighted_projective_equation": "V^2=G(T,S)",
            "infinity_equation": "V^2=1",
            "K_rational_infinity_points": "[1:1:0], [1:-1:0]",
            "branch_points": "g6(alpha)=0; six simple geometric points [alpha:0:1]",
        },
        "d=i": {
            "affine_equation": "i*v^2=g6(t)",
            "weighted_projective_equation": "i*V^2=G(T,S)",
            "infinity_equation": "i*V^2=1, equivalently V^2=-i",
            "K_rational_infinity_points": "none; points are [1:+/-sqrt(-i):0] over K(sqrt(-i))",
            "branch_points": "g6(alpha)=0; six simple geometric points [alpha:0:1]",
        },
    }

    bad_places = {
        "field": "K=Q(i), O_K=Z[i]",
        "prime_labels": {
            "p2": "(1+i), with (2)=(1+i)^2 up to a unit",
            "p37397": "(94*i-169), norm 37397",
            "p37397_conjugate": "(-94*i-169), norm 37397",
        },
        "curve_displayed_integral_model_support": ["(1+i)", "(94*i-169)"],
        "curve_support_proof": (
            "For either unit twist d, the weighted integral model is smooth at every "
            "finite prime outside 2*Disc(g6). Disc(g6) has only (1+i) and "
            "(94*i-169). This proves good reduction outside the two displayed "
            "candidate places; the actual candidate-place decisions are recorded "
            "separately in actual_reduction_audit."
        ),
        "curve_reduction_scope": (
            "The displayed-model support is separate from the actual curve set. "
            "The actual status is recorded in actual_reduction_audit: (94*i-169) "
            "is proved bad for both twists, while (1+i) remains unresolved."
        ),
        "curve_actual_reduction_proved_bad": {
            "d=1": ["(94*i-169)"],
            "d=i": ["(94*i-169)"],
        },
        "curve_actual_reduction_proved_good_outside": {
            "d=1": "all finite primes outside {(1+i),(94*i-169)}",
            "d=i": "all finite primes outside {(1+i),(94*i-169)}",
        },
        "curve_actual_reduction_unresolved": {
            "d=1": ["(1+i)"],
            "d=i": ["(1+i)"],
        },
        "curve_actual_reduction_set_complete": False,
        "berry_pullback_support": [
            "(1+i)",
            "(94*i-169)",
            "(-94*i-169)",
        ],
        "berry_pullback_proof": (
            "Disc(f12)=2^155*37397, so over K both primes over 37397 occur, together with (1+i)."
        ),
        "factor_resultant_support": ["(1+i)"],
        "factor_resultant_proof": (
            "Res(g6,conjugate(g6))=2^40; no prime over 37397 is a common-root/resultant place."
        ),
        "auxiliary_fiber_separability_support_over_Q": ["2", "5", "43", "53"],
        "auxiliary_fiber_separability_proof": (
            "The discriminants of h, the T quartic, the X quartic, t^2+2*t-1, "
            "and Z have rational prime support {2,43}, {2,5}, {2}, {2}, and "
            "{2,53}, respectively. These are chart-fiber collision supports, "
            "not curve bad-reduction or factor-resultant supports."
        ),
        "completeness": (
            "The displayed discriminant and resultant factorizations are complete in "
            "Z[i]. No finite prime outside the listed curve, pullback, or resultant "
            "supports can enter B0 through smoothness or factor collision."
        ),
    }

    model = {
        "base_field": "K=Q(i)",
        "weighted_projective_space": "P_K(1,3,1) with [T:V:S]~[lambda*T:lambda^3*V:lambda*S]",
        "homogeneous_polynomial": "G(T,S)=S^6*g6(T/S)",
        "affine_chart": "S!=0: t=T/S, v=V/S^3",
        "infinity_chart": "T!=0: x=S/T=1/t, z=V/T^3, d*z^2=g6^*(x)",
        "reciprocal_polynomial": str(reciprocal),
        "ordinary_plane_closure": (
            "d*V^2*S^4=G(T,S) in P^2; [0:1:0] is singular, so the "
            "weighted model is the smooth projective model."
        ),
        "hyperelliptic_map": "pi_d([T:V:S])=[T:S]",
        "hyperelliptic_involution": "[T:V:S] -> [T:-V:S]",
        "genus_argument": (
            "g6 is squarefree of degree 6: six finite simple branch points, no "
            "infinity branch, so Riemann-Hurwitz gives genus 2."
        ),
        "smoothness_argument": (
            "The affine and reciprocal-chart Jacobian tests reduce to "
            "gcd(g6,g6')=1; P(1,3,1) has only [0:1:0] singular in the "
            "ambient space and the curve avoids it."
        ),
    }
    maps = {
        "berry_pullback": {
            "equation": "C_B: W^2=F(A,B), F=B^12*f12(A/B)=G*Gbar",
            "weighted_coordinates": "[A:B:W] in P(1,1,6), [A:B:W]~[lambda*A:lambda*B:lambda^6*W]",
            "surface_map": "[A:B:W] -> [X_h(A,B):Y_h(A,B):Z_h(A,B):T_h(A,B):W] in Berry's P^4",
            "forward_for_rational_t": (
                "For [T:S]=[A:B] in P^1(Q), d*V^2=G and "
                "U=epsilon*V*conjugate(V), epsilon=+/-1; map to "
                "[A:B:W]=[A:B:U]."
            ),
            "affine_forward": "(t,v) -> (t,U=epsilon*Norm_K/Q(v))",
            "converse_affine": (
                "For (t,U) in C_B(Q), t=A/B with gcd(A,B)=1 and B!=0, "
                "G(A,B)*Gbar(A,B)=W^2 forces G(A,B)=d*V^2 for exactly "
                "one d in {1,i} modulo K^2; set v=V/B^3."
            ),
            "converse_infinity": (
                "At B=0, G(A,0)=A^6; only d=1 has K-rational points above infinity."
            ),
            "sign_and_lift": (
                "Changing epsilon gives the two Berry W-signs; changing V to "
                "-V is the hyperelliptic lift and does not change Norm(V)."
            ),
            "support_proof": (
                "Away from (1+i), common divisors of G and Gbar divide the "
                "resultant 2^40; at (1+i), v_(1+i)(G) is even because W is "
                "rational. Thus G is a unit times a square, and unit "
                "squareclasses are {1,i}."
            ),
        },
        "parameter_inverse_charts": {
            "relation_one": str(inverse_one),
            "relation_two": str(inverse_two),
            "first_chart": "t=(X-2*Y-Z)/(Z-X) when Z-X!=0",
            "second_chart": "t=(-X+3*Y+2*Z+T)/(X-Y+T) when X-Y+T!=0",
            "denominators": {
                "Z-X": "-2*(t-1)*h(t)",
                "X-Y+T": "4*t*h(t)",
                "common_exception": "h(t)=0 maps to [1:0:1:-1] and h has no rational root",
                "t=0": "first chart is nonzero; second chart vanishes",
                "t=1": "second chart is nonzero; first chart vanishes",
                "infinity": (
                    "both affine denominators are replaced by the T!=0 "
                    "projective chart and F(1,0)=1"
                ),
            },
        },
    }

    node_fiber_table = {
        label: data
        for label, data in node_fibers.items()
        if data["finite_parameter_gcd"] != "1" or data["infinity_fiber"]
    }
    exceptional_fibers = {
        "nodes": node_fiber_table,
        "all_node_fibers_statement": (
            "The 16 singular Berry nodes are the four A, four B, four C, and "
            "four D nodes listed by the exact gradient case split; the gcd "
            "audit is exhaustive."
        ),
        "t_zero": "t=0 maps to [-1:-1:1:0]=[1:1:-1:0], f=1.",
        "t_plus_minus_one": "t=1 maps to [1:0:1:1], f=2^13; t=-1 maps to [1:0:-1:1], f=2^11.",
        "infinity": "t=infinity maps to [1:1:1:0], F(1,0)=1.",
        "node5": (
            "h(t)=0 maps to [1:0:1:-1], f=2*Z(t)^2; h is irreducible over "
            "Q, so this fiber has no rational parameter."
        ),
        "branch_and_factor_zero": {
            "g6": (
                "six simple geometric roots alpha; each gives one ramified "
                "point v=0 on either twist and W=0 on C_B."
            ),
            "conjugate_g6": (
                "six simple geometric roots beta; these are the conjugate "
                "factor-zero fibers of the literal V4 cover."
            ),
            "disjointness": (
                "Res(g6,conjugate(g6))=2^40 and f is irreducible over Q, so "
                "no rational branch parameter and no factor collision occur."
            ),
        },
        "coordinate_zero_fibers": {
            "Y": "(t-1)(t+1)h(t); all its fibers are the three B-node fibers above.",
            "X": (
                "(t^2+2*t-1)(t^4+4*t^3+22*t^2+4*t+1); the two "
                "quadratic roots are C nodes [0:1:+/-sqrt(2):-1], and the "
                "quartic roots are nonnode X=0 fibers."
            ),
            "T": (
                "2*t*(5*t^4+20*t^3+14*t^2-12*t+5), plus projective infinity; only t=0 is rational."
            ),
            "Z": (
                "The six geometric roots of Z(t) are retained; none is a "
                "Berry node and Z has no rational root."
            ),
        },
    }
    trivial_ledger = {
        "scope": (
            "Currently certified rational-t fibers only; this is not a claim "
            "that the ledger is complete as a K-point classification."
        ),
        "d=1": [
            {
                "t": "0",
                "weighted_point": "[0:+/-i:1]",
                "equation_check": "g6(0)=-1 and v^2=-1",
                "Berry_images": "(t,U)=(0,+/-1), since Norm(v)=1",
            },
            {
                "t": "infinity",
                "weighted_point": "[1:+/-1:0]",
                "equation_check": "leading coefficient is 1",
                "Berry_images": "(infinity,U)=+/-1",
            },
        ],
        "d=i": [],
        "certified_special_nonpoints": [
            {
                "t": "0",
                "twist": "d=i",
                "reason": "i*v^2=-1 gives v^2=i, and i is not a square in Q(i).",
            },
            {
                "t": "+1 and -1",
                "twist": "d=1 or d=i",
                "reason": (
                    "f(1)=2^13 and f(-1)=2^11 are not rational squares, so "
                    "Norm(v)^2=f(t) is impossible."
                ),
            },
            {
                "t": "infinity",
                "twist": "d=i",
                "reason": "i*V^2=1 gives V^2=-i, and -i is not a square in Q(i).",
            },
        ],
    }
    proof_boundary = {
        "rank_or_selmer_claimed": False,
        "bounded_search_used": False,
        "other_sextics_processed": False,
        "b0_only": True,
        "actual_reduction_resolved": actual_reduction["resolved"],
        "remaining_b0": actual_reduction["blocker"],
        "remaining_b1": (
            "After the B0 reduction blocker is resolved, determine K-points on "
            "C_1 and C_i with t in P^1(Q), beginning with exact local analysis "
            "at the actual bad places and then enforce rational-t globally."
        ),
    }

    checks.update(node_checks)
    violations = [name for name, passed in checks.items() if passed is not True]
    blockers = [] if actual_reduction["resolved"] else ["actual_reduction_at_(1+i)_unresolved"]
    if violations:
        status = "invalid"
    elif blockers:
        status = "blocked"
    else:
        status = "ok"
    return {
        "status": status,
        "ready": not violations and not blockers,
        "task": "berry-sextic-genus2-b0",
        "outcome": (
            "berry_sextic_b0_covering_certificate"
            if not blockers
            else "precise_b0_actual_reduction_blocker"
        ),
        "selected_input": {
            "degree": 6,
            "g6": str(g),
            "conjugate_g6": str(gbar),
            "berry_coordinates": {name: str(poly) for name, poly in row.items()},
        },
        "models": model,
        "twists": twist_data,
        "maps_and_converses": maps,
        "exceptional_fibers": exceptional_fibers,
        "trivial_rational_t_ledger": trivial_ledger,
        "bad_places": bad_places,
        "actual_reduction_audit": actual_reduction,
        "verification": {
            "checks": checks,
            "violations": violations,
            "blockers": blockers,
            "exact_values": {
                "f12": str(f),
                "resultant_g_gbar": str(resultant),
                "disc_g": str(disc_g),
                "disc_f": str(disc_f),
                "h": str(h),
                "T_zero_quartic": str(t_zero_quartic),
                "X_zero_quadratic": str(x_zero_quadratic),
                "X_zero_quartic": str(x_zero_quartic),
            },
        },
        "proof_boundary": proof_boundary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_b0_certificate()
    if args.out is not None:
        write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"task={payload['task']}")
    print(f"ready={payload['ready']}")
    print(f"outcome={payload['outcome']}")
    print(f"violations={payload['verification']['violations']}")
    print(f"blockers={payload['verification']['blockers']}")
    if args.strict and not payload["ready"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
