#!/usr/bin/env python3
"""Canonical C1 kernels for the wl530-wl534 pure-v_ell reductions."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

import sympy as sp

if __package__:
    from scripts.theory.aa_bb.c1_wl535 import build_wl535
else:
    from c1_wl535 import build_wl535

# --- wl530 kernel ---

WL530_BOUNDARY = (
    "This resolves only M1 for the pure support family "
    "support=v_ell|L=1|T=ell|d=(ell,1,ell). It derives the exact complete-d "
    "cover formulas, one rational function-field chart, the centered-even "
    "t,N,M maps, the opposite-side square product, and the resulting "
    "square-specialization elliptic family, and it verifies exact recovery of "
    "wl528 and wl529 at ell=5. It does not classify rational points for the "
    "general ell family, does not enter M2, does not prove a uniform "
    "cover-family obstruction, and does not claim a complete Selmer upper "
    "bound, rank zero, Sha[2]=0, or family exclusion."
)


def _sympy_reduces_to_zero_wl530(
    expr: sp.Expr, *, ell: sp.Symbol, r: sp.Symbol, y: sp.Symbol
) -> bool:
    function_field_rhs = ell * r**4 - 8 * (ell**2 + 8) * r**2 + 16 * ell**3
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(sp.expand(numerator), y),
        sp.Poly(y**2 - function_field_rhs, y),
    ).as_expr()
    return sp.factor(remainder) == 0


def _function_field_identity_checks_wl530() -> list[dict[str, Any]]:
    ell, r, y, t, U, Xq, Yq = sp.symbols("ell r y t U Xq Yq")

    u_minus = (r**2 - 4 * ell) / (2 * r)
    u_pos = y / (2 * r)
    u_neg = (r**2 + 4 * ell) / (2 * r)
    x_coord = 2 * ell**2 - 8 + ell * u_minus**2
    y_coord = ell * u_minus * u_pos * u_neg
    t_value = y * (r**2 + 4 * ell) / (4 * r * (r**2 - 4 * ell))
    z_value = x_coord / 2 - t_value**2
    n_value = (ell + t_value) / 2
    m_value = (ell - t_value) / 2
    opposite_product = (n_value**2 + (ell - 1) ** 2) * (m_value**2 + (ell - 1) ** 2)
    c_value = 5 * ell**2 - 8 * ell + 4
    quartic = t**4 + (6 * ell**2 - 16 * ell + 8) * t**2 + c_value**2
    checks: list[tuple[str, str, sp.Expr, bool]] = [
        (
            "cover_relation_minus",
            "X - (2*ell^2 - 8) = ell*u_minus_p^2",
            x_coord - (2 * ell**2 - 8) - ell * u_minus**2,
            True,
        ),
        (
            "cover_relation_pos",
            "X - (2*ell^2 + 8) = u_pos_2sqrt_q^2",
            x_coord - (2 * ell**2 + 8) - u_pos**2,
            True,
        ),
        (
            "cover_relation_neg",
            "X + (2*ell^2 + 8) = ell*u_neg_2sqrt_q^2",
            x_coord + (2 * ell**2 + 8) - ell * u_neg**2,
            True,
        ),
        (
            "centered_even_t_formula",
            "t = Y/(2*(X+p)) = y*(r^2 + 4*ell)/(4*r*(r^2 - 4*ell))",
            y_coord / (2 * (x_coord + (8 - 2 * ell**2))) - t_value,
            True,
        ),
        (
            "source_leg_one_square_identity",
            "(N^2+1)(M^2+1) = (z/4)^2",
            (n_value**2 + 1) * (m_value**2 + 1) - (z_value / 4) ** 2,
            True,
        ),
        (
            "opposite_product_t_identity",
            "16*(N^2+(ell-1)^2)(M^2+(ell-1)^2) = (t^2 + 5*ell^2 - 8*ell + 4)^2 - 4*ell^2*t^2",
            16 * opposite_product - ((t_value**2 + c_value) ** 2 - 4 * ell**2 * t_value**2),
            True,
        ),
        (
            "square_locus_quartic_identity",
            "U^2 = t^4 + (6*ell^2 - 16*ell + 8)*t^2 + (5*ell^2 - 8*ell + 4)^2",
            ((t**2 + c_value) ** 2 - 4 * ell**2 * t**2) - quartic,
            False,
        ),
        (
            "elliptic_quotient_map",
            "X = t^2, Y = t*U sends the square locus quartic to the elliptic quotient",
            Yq**2 - (Xq**3 + (6 * ell**2 - 16 * ell + 8) * Xq**2 + c_value**2 * Xq),
            False,
        ),
    ]

    payload: list[dict[str, Any]] = []
    for check_id, identity, expr, reduce_on_function_field in checks:
        if reduce_on_function_field:
            verified = _sympy_reduces_to_zero_wl530(expr, ell=ell, r=r, y=y)
        elif check_id == "square_locus_quartic_identity":
            verified = sp.factor(expr) == 0
        else:
            verified = sp.factor(expr.subs({Xq: t**2, Yq: t * U}) - t**2 * (U**2 - quartic)) == 0
        payload.append(
            {
                "check_id": check_id,
                "identity": identity,
                "verified": verified,
            }
        )

    quartic_discriminant = sp.factor(sp.discriminant(sp.expand(quartic), t))
    elliptic_rhs_discriminant = sp.factor(
        sp.discriminant(
            Xq**3 + (6 * ell**2 - 16 * ell + 8) * Xq**2 + c_value**2 * Xq,
            Xq,
        )
    )
    payload.extend(
        [
            {
                "check_id": "square_locus_quartic_discriminant",
                "identity": (
                    "disc_t(t^4 + (6*ell^2 - 16*ell + 8)*t^2 + "
                    "(5*ell^2 - 8*ell + 4)^2) = "
                    "65536*ell^4*(ell - 1)^4*(5*ell^2 - 8*ell + 4)^2"
                ),
                "verified": quartic_discriminant
                == 65536 * ell**4 * (ell - 1) ** 4 * (5 * ell**2 - 8 * ell + 4) ** 2,
            },
            {
                "check_id": "elliptic_quotient_rhs_cubic_discriminant",
                "identity": (
                    "disc_X(X^3 + (6*ell^2 - 16*ell + 8)*X^2 + "
                    "(5*ell^2 - 8*ell + 4)^2*X) = "
                    "-64*ell^2*(ell - 1)^2*(5*ell^2 - 8*ell + 4)^4"
                ),
                "verified": elliptic_rhs_discriminant
                == -64 * ell**2 * (ell - 1) ** 2 * (5 * ell**2 - 8 * ell + 4) ** 4,
            },
        ]
    )
    return payload


def _ell_5_recovery_wl530() -> dict[str, Any]:
    ell, r, y, t, Xq = sp.symbols("ell r y t Xq")
    c_value = 5 * ell**2 - 8 * ell + 4
    function_field_rhs = ell * r**4 - 8 * (ell**2 + 8) * r**2 + 16 * ell**3
    t_value = y * (r**2 + 4 * ell) / (4 * r * (r**2 - 4 * ell))
    quartic = t**4 + (6 * ell**2 - 16 * ell + 8) * t**2 + c_value**2
    elliptic = Xq**3 + (6 * ell**2 - 16 * ell + 8) * Xq**2 + c_value**2 * Xq

    checks = [
        sp.expand(function_field_rhs.subs(ell, 5) - (5 * r**4 - 264 * r**2 + 2000)) == 0,
        sp.simplify(t_value.subs(ell, 5) - y * (r**2 + 20) / (4 * r * (r**2 - 20))) == 0,
        sp.expand(quartic.subs(ell, 5) - (t**4 + 78 * t**2 + 7921)) == 0,
        sp.expand(elliptic.subs(ell, 5) - (Xq**3 + 78 * Xq**2 + 7921 * Xq)) == 0,
    ]
    return {
        "ell": 5,
        "function_field_equation": "y^2 = 5*r^4 - 264*r^2 + 2000",
        "t_formula": "y*(r^2+20)/(4*r*(r^2-20))",
        "N_formula": "(5+t)/2",
        "M_formula": "(5-t)/2",
        "opposite_side_product": "(N^2+16)(M^2+16)",
        "square_locus_quartic": "U^2 = t^4 + 78*t^2 + 7921",
        "elliptic_quotient": "Y^2 = X^3 + 78*X^2 + 7921*X",
        "all_recovery_checks_passed": all(checks),
    }


def build_wl530_m1_pure_v_ell_symbolic_family() -> dict[str, Any]:
    identity_checks = _function_field_identity_checks_wl530()
    recovery = _ell_5_recovery_wl530()
    violations: list[str] = []

    if not all(check["verified"] is True for check in identity_checks):
        violations.append("symbolic_identity_check_failed")
    if recovery["all_recovery_checks_passed"] is not True:
        violations.append("ell_5_recovery_failed")

    status = "ok" if not violations else "issues"
    ready = status == "ok"
    proof_status = (
        {
            "symbolic_complete_d_family_derived_here": True,
            "function_field_chart_derived_here": True,
            "rational_n_m_maps_derived_here": True,
            "opposite_side_square_product_derived_here": True,
            "square_specialization_elliptic_family_derived_here": True,
            "exact_ell_5_recovery_verified_here": True,
            "uniform_cover_family_obstruction_proved_here": False,
            "m2_entered_here": False,
            "stop_after_m1": True,
        }
        if ready
        else {}
    )

    return {
        "status": status,
        "ready": ready,
        "work_log": "wl530",
        "object_layer": "symbolic_pure_support_function_field_family",
        "family_scope": {
            "support": "v_ell",
            "L": 1,
            "T": "ell",
            "d_vector": {
                "d_minus_p": "ell",
                "d_pos_2sqrt_q": 1,
                "d_neg_2sqrt_q": "ell",
            },
            "source_leg": 1,
            "opposite_leg": "ell - 1",
            "parameter_restrictions": [
                "ell is an odd prime",
                "r != 0",
                "r^2 != 4*ell",
            ],
            "touches_only_M1_symbolic_derivation": True,
        },
        "complete_d_family": {
            "parameters": {
                "p": "8 - 2*ell^2",
                "sqrt_q": "ell^2 + 4",
                "q": "(ell^2 + 4)^2",
            },
            "cover_equations": [
                "X - (2*ell^2 - 8) = ell*u_minus_p^2",
                "X - (2*ell^2 + 8) = u_pos_2sqrt_q^2",
                "X + (2*ell^2 + 8) = ell*u_neg_2sqrt_q^2",
            ],
            "difference_equations": [
                "ell*u_minus_p^2 - u_pos_2sqrt_q^2 = 16",
                "u_minus_p^2 - u_neg_2sqrt_q^2 = -4*ell",
            ],
        },
        "function_field_model": {
            "base_field": "Q(ell)",
            "function_field": "Q(ell)(r,y)/(y^2 - (ell*r^4 - 8*(ell^2+8)*r^2 + 16*ell^3))",
            "cover_parameter": "r = u_neg_2sqrt_q + u_minus_p",
            "cover_maps": {
                "u_minus_p": "(r^2 - 4*ell)/(2*r)",
                "u_pos_2sqrt_q": "y/(2*r)",
                "u_neg_2sqrt_q": "(r^2 + 4*ell)/(2*r)",
                "X": "2*ell^2 - 8 + ell*((r^2 - 4*ell)/(2*r))^2",
                "Y": "ell*y*(r^4 - 16*ell^2)/(8*r^3)",
            },
            "identity_checks": identity_checks,
        },
        "source_side_maps_and_n_m": {
            "centered_even_map": {
                "t": "y*(r^2 + 4*ell)/(4*r*(r^2 - 4*ell))",
                "N": "(ell + t)/2",
                "M": "(ell - t)/2",
                "positivity_domain": "|t| < ell",
                "source_product_square_identity": "(N^2+1)(M^2+1) = (z/4)^2",
            }
        },
        "opposite_side_square_locus": {
            "opposite_side_product": "(N^2+(ell-1)^2)(M^2+(ell-1)^2)",
            "product_in_t": "((t^2 + 5*ell^2 - 8*ell + 4)^2 - 4*ell^2*t^2)/16",
            "square_locus_quartic": (
                "U^2 = t^4 + (6*ell^2 - 16*ell + 8)*t^2 + (5*ell^2 - 8*ell + 4)^2"
            ),
            "elliptic_quotient": (
                "Y^2 = X^3 + (6*ell^2 - 16*ell + 8)*X^2 + (5*ell^2 - 8*ell + 4)^2*X"
            ),
            "degree_two_map": "X = t^2, Y = t*U",
            "quartic_discriminant": "65536*ell^4*(ell - 1)^4*(5*ell^2 - 8*ell + 4)^2",
            "elliptic_rhs_cubic_discriminant": ("-64*ell^2*(ell - 1)^2*(5*ell^2 - 8*ell + 4)^4"),
        },
        "ell_5_recovery": recovery,
        "proof_status": proof_status,
        "violations": violations,
        "boundary": WL530_BOUNDARY,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "advance_to_m2": False,
        "stop_after_current_task": True,
    }


# --- wl531 kernel ---

WL531_BOUNDARY = (
    "This resolves wl530 M2 only to one exact missing arithmetic proposition "
    "for support=v_ell|L=1|T=ell|d=(ell,1,ell). It handles the square-X, "
    "positivity, source-side square identity, opposite-side square identity, "
    "and complete-d lift formulas exactly, then isolates one X-fiber-product "
    "square-lift proposition whose proof would close M2. It does not prove a "
    "uniform infinite-subfamily exclusion theorem, does not exhibit a strict "
    "counterexample, does not classify the rational points of the general "
    "fiber-product curve, does not enter M3, and does not claim a complete "
    "Selmer upper bound, rank zero, Sha[2]=0, or family exclusion."
)


def _wl530_ready_wl531(wl530: dict[str, Any]) -> bool:
    proof = wl530.get("proof_status", {})
    return (
        wl530.get("status") == "ok"
        and wl530.get("ready") is True
        and wl530.get("work_log") == "wl530"
        and wl530.get("object_layer") == "symbolic_pure_support_function_field_family"
        and proof.get("symbolic_complete_d_family_derived_here") is True
        and proof.get("square_specialization_elliptic_family_derived_here") is True
        and proof.get("m2_entered_here") is False
        and proof.get("uniform_cover_family_obstruction_proved_here") is False
        and wl530.get("advance_to_m2") is False
    )


def _sympy_reduces_to_zero_wl531(
    expr: sp.Expr, *, ell: sp.Symbol, r: sp.Symbol, y: sp.Symbol
) -> bool:
    function_field_rhs = ell * r**4 - 8 * (ell**2 + 8) * r**2 + 16 * ell**3
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(sp.expand(numerator), y),
        sp.Poly(y**2 - function_field_rhs, y),
    ).as_expr()
    return sp.factor(remainder) == 0


def _identity_checks_wl531() -> list[dict[str, Any]]:
    ell, r, y = sp.symbols("ell r y", nonzero=True)
    X = sp.symbols("X")
    z = sp.symbols("z")
    um, up, un, t_chosen = sp.symbols("um up un t_chosen", nonzero=True)

    u_minus = (r**2 - 4 * ell) / (2 * r)
    u_pos = y / (2 * r)
    t_value = y * (r**2 + 4 * ell) / (4 * r * (r**2 - 4 * ell))
    x_coord = 2 * ell**2 - 8 + ell * u_minus**2
    z_value = x_coord / 2 - t_value**2
    x_value = t_value**2

    q_source = X**2 + (8 - 2 * ell**2) * X + (ell**2 + 4) ** 2
    a_value = 2 * (x_value - ell**2 + 4 + z_value) / ell
    b_value = 2 * (x_value - ell**2 - 4 + z_value)

    checks: list[tuple[str, str, sp.Expr, str]] = [
        (
            "source_square_locus_from_wl530_chart",
            "z^2 = X^2 + (8-2*ell^2)*X + (ell^2+4)^2 with X=t^2 and z=X_cover/2-t^2",
            z_value**2 - q_source.subs(X, x_value),
            "function_field",
        ),
        (
            "u_minus_square_as_linear_form_in_X_and_z",
            "u_minus_p^2 = 2*(X-ell^2+4+z)/ell",
            u_minus**2 - a_value,
            "function_field",
        ),
        (
            "u_pos_square_as_linear_form_in_X_and_z",
            "u_pos_2sqrt_q^2 = 2*(X-ell^2-4+z)",
            u_pos**2 - b_value,
            "function_field",
        ),
        (
            "source_locus_recovers_t_squared_factorization",
            "4*A_ell(X,z)*X = B_ell(X,z)*(A_ell(X,z)+4*ell)",
            4 * (2 * (X - ell**2 + 4 + z) / ell) * X
            - (2 * (X - ell**2 - 4 + z)) * (2 * (X - ell**2 + 4 + z) / ell + 4 * ell),
            "source_quadratic",
        ),
        (
            "b_is_ell_a_minus_16",
            "B_ell(X,z) = ell*A_ell(X,z) - 16",
            (2 * (X - ell**2 - 4 + z)) - (ell * (2 * (X - ell**2 + 4 + z) / ell) - 16),
            "plain",
        ),
        (
            "b_zero_forces_x_zero_on_source_quadratic",
            "B_ell(X,z)=0 and the source quadratic imply -16*X=0",
            (ell**2 + 4 - X) ** 2 - q_source + 16 * X,
            "plain",
        ),
        (
            "a_zero_forces_b_negative",
            "A_ell(X,z)=0 implies B_ell(X,z)=-16",
            2 * (X - ell**2 - 4 + (ell**2 - 4 - X)) + 16,
            "plain",
        ),
        (
            "reconstruct_u_minus_from_r",
            "if r=u_minus+u_neg and u_neg^2-u_minus^2=4*ell then u_minus=(r^2-4*ell)/(2*r)",
            ((um + un) ** 2 - 4 * ell) / (2 * (um + un)) - um,
            "difference_of_squares",
        ),
        (
            "reconstruct_u_neg_from_r",
            "if r=u_minus+u_neg and u_neg^2-u_minus^2=4*ell then u_neg=(r^2+4*ell)/(2*r)",
            ((um + un) ** 2 + 4 * ell) / (2 * (um + un)) - un,
            "difference_of_squares",
        ),
        (
            "reconstructed_y_satisfies_wl530_quartic",
            "with y=2*r*u_pos and the two square relations, y^2=ell*r^4-8*(ell^2+8)*r^2+16*ell^3",
            (2 * (um + un) * up) ** 2
            - (ell * (um + un) ** 4 - 8 * (ell**2 + 8) * (um + un) ** 2 + 16 * ell**3),
            "two_square_relations",
        ),
        (
            "reconstructed_t_matches_centered_even_map",
            (
                "with r=u_minus+u_neg and y=2*r*u_pos, the centered-even map "
                "gives t=u_pos*u_neg/(2*u_minus)"
            ),
            ((2 * (um + un) * up) * ((um + un) ** 2 + 4 * ell))
            / (4 * (um + un) * ((um + un) ** 2 - 4 * ell))
            - up * un / (2 * um),
            "difference_of_squares",
        ),
        (
            "chosen_t_is_recovered_after_sign_choice",
            "if u_neg=2*t_chosen*u_minus/u_pos then u_pos*u_neg/(2*u_minus)=t_chosen",
            up * (2 * t_chosen * um / up) / (2 * um) - t_chosen,
            "plain",
        ),
    ]

    payload: list[dict[str, Any]] = []
    for check_id, identity, expr, mode in checks:
        if mode == "function_field":
            verified = _sympy_reduces_to_zero_wl531(expr, ell=ell, r=r, y=y)
        elif mode == "source_quadratic":
            numerator = sp.together(expr).as_numer_denom()[0]
            remainder = sp.rem(
                sp.Poly(sp.expand(numerator), z),
                sp.Poly(z**2 - q_source, z),
            ).as_expr()
            verified = sp.factor(remainder) == 0
        elif mode == "difference_of_squares":
            numerator = sp.together(expr).as_numer_denom()[0]
            remainder = sp.rem(
                sp.Poly(sp.expand(numerator), un),
                sp.Poly(un**2 - um**2 - 4 * ell, un),
            ).as_expr()
            verified = sp.factor(remainder) == 0
        elif mode == "two_square_relations":
            numerator = sp.together(expr).as_numer_denom()[0]
            reduced_up = sp.rem(
                sp.Poly(sp.expand(numerator), up),
                sp.Poly(up**2 - ell * um**2 + 16, up),
            ).as_expr()
            reduced_un = sp.rem(
                sp.Poly(sp.expand(reduced_up), un),
                sp.Poly(un**2 - um**2 - 4 * ell, un),
            ).as_expr()
            verified = sp.factor(reduced_un) == 0
        else:
            verified = sp.factor(expr) == 0
        payload.append({"check_id": check_id, "identity": identity, "verified": verified})
    return payload


def _t_zero_analysis_wl531() -> dict[str, Any]:
    ell = sp.symbols("ell", positive=True)
    a_plus = sp.simplify(2 * (0 - ell**2 + 4 + (ell**2 + 4)) / ell)
    a_minus = sp.simplify(2 * (0 - ell**2 + 4 - (ell**2 + 4)) / ell)
    return {
        "source_fiber_points_at_X_zero": [
            {"z": "ell^2 + 4", "A_ell(0,z)": str(a_plus)},
            {"z": "-ell^2 - 4", "A_ell(0,z)": str(a_minus)},
        ],
        "candidate_square_values": ["16/ell", "-4*ell"],
        "certificate": (
            "For an odd prime ell, 16/ell is a rational square only if ell is a rational square, "
            "and -4*ell is negative. Hence X=0 cannot satisfy the square-lift conditions."
        ),
        "t_zero_can_satisfy_square_lift_conditions": False,
        "positivity_domain_reduces_to": "0 < X < ell^2",
    }


def _converse_denominator_analysis_wl531() -> dict[str, Any]:
    return {
        "B_nonzero": (
            "If B_ell(X,z)=0, then z=ell^2+4-X; substituting in the source "
            "quadratic gives -16*X=0. Thus 0<X forces B_ell(X,z) != 0, "
            "so the definition u_neg=2*t*u_minus/u_pos is valid."
        ),
        "A_nonzero": (
            "If A_ell(X,z)=0, then z=ell^2-4-X and B_ell(X,z)=-16, "
            "which cannot be a rational square. Thus A_ell(X,z) != 0."
        ),
        "r_nonzero": (
            "With u_neg^2-u_minus^2=4*ell and ell>0, r=u_minus+u_neg "
            "cannot be zero, since r=0 would force u_neg^2=u_minus^2."
        ),
        "r_squared_minus_4ell_nonzero": (
            "r^2-4*ell=2*r*u_minus. The preceding two nonzero facts make "
            "the centered-even denominator nonzero."
        ),
        "all_converse_denominators_excluded": True,
    }


def _is_rational_square_wl531(value: Fraction) -> bool:
    if value < 0:
        return False
    return (
        isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def _boundary_examples_wl531() -> dict[str, Any]:
    ell = 7
    x = Fraction(4, 1)
    u = Fraction(195, 1)
    q_source = x * x + (8 - 2 * ell * ell) * x + (ell * ell + 4) ** 2

    ell2 = 13
    r = Fraction(6, 1)
    y = Fraction(32, 1)
    t = y * (r * r + 4 * ell2) / (4 * r * (r * r - 4 * ell2))
    x2 = t * t
    z2 = Fraction(1105, 9)
    q_opp = x2 * x2 + (6 * ell2 * ell2 - 16 * ell2 + 8) * x2 + (5 * ell2 * ell2 - 8 * ell2 + 4) ** 2
    a2 = Fraction(2 * (x2 - ell2 * ell2 + 4 + z2), ell2)
    b2 = Fraction(2 * (x2 - ell2 * ell2 - 4 + z2), 1)

    return {
        "opposite_side_only_example": {
            "ell": ell,
            "point_on_opposite_square_locus": {"X": str(x), "U": str(u)},
            "X_is_rational_square": True,
            "positivity_range": "0 < X < ell^2",
            "source_quadratic_value": str(q_source),
            "source_quadratic_is_rational_square": _is_rational_square_wl531(q_source),
            "meaning": (
                "The opposite-side elliptic quotient can contribute a square-X point in the "
                "positivity range without giving a source-side square lift."
            ),
        },
        "source_lift_only_example": {
            "ell": ell2,
            "quartic_point": {"r": str(r), "y": str(y)},
            "induced_values": {"t": str(t), "X": str(x2), "z": str(z2)},
            "A_ell(X,z)": str(a2),
            "B_ell(X,z)": str(b2),
            "A_is_rational_square": _is_rational_square_wl531(a2),
            "B_is_rational_square": _is_rational_square_wl531(b2),
            "opposite_quadratic_value": str(q_opp),
            "opposite_quadratic_is_rational_square": _is_rational_square_wl531(q_opp),
            "meaning": (
                "A genuine complete-d lift can satisfy the source-side square conditions in the "
                "positivity range while still failing the opposite-side square condition."
            ),
        },
    }


def build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition(
    wl530: dict[str, Any] | None = None,
) -> dict[str, Any]:
    wl530 = wl530 if wl530 is not None else build_wl530_m1_pure_v_ell_symbolic_family()
    identity_checks = _identity_checks_wl531()
    t_zero = _t_zero_analysis_wl531()
    converse_denominators = _converse_denominator_analysis_wl531()
    examples = _boundary_examples_wl531()

    violations: list[str] = []
    if not _wl530_ready_wl531(wl530):
        violations.append("wl530_input_not_ready")
    if not all(check["verified"] is True for check in identity_checks):
        violations.append("reduction_identity_check_failed")
    if t_zero["t_zero_can_satisfy_square_lift_conditions"] is not False:
        violations.append("t_zero_not_excluded")
    if converse_denominators["all_converse_denominators_excluded"] is not True:
        violations.append("converse_denominator_not_excluded")

    status = "ok" if not violations else "issues"
    ready = status == "ok"
    proof_status = (
        {
            "m2_reduced_to_exact_missing_proposition_here": True,
            "exact_x_fiber_product_square_lift_proposition_identified_here": True,
            "t_zero_excluded_from_the_missing_proposition_here": True,
            "uniform_infinite_subfamily_exclusion_proved_here": False,
            "strict_counterexample_found_here": False,
            "advance_to_m3": False,
            "stop_after_exact_missing_proposition": True,
        }
        if ready
        else {}
    )

    return {
        "status": status,
        "ready": ready,
        "work_log": "wl531",
        "object_layer": "m2_exact_missing_proposition_after_square_x_and_complete_d_lift_reduction",
        "family_scope": {
            "support": "v_ell",
            "L": 1,
            "T": "ell",
            "d_vector": {
                "d_minus_p": "ell",
                "d_pos_2sqrt_q": 1,
                "d_neg_2sqrt_q": "ell",
            },
            "parameter_restrictions": [
                "ell is an odd prime",
                "0 < X < ell^2",
                "X is a rational square",
            ],
            "touches_only_M2_for_the_wl530_pure_family": True,
        },
        "input_checkpoint": {
            "work_log": "wl530",
            "ready": _wl530_ready_wl531(wl530),
            "handoff": "wl530_m1_pure_v_ell_symbolic_derivation_stop",
        },
        "fiber_product_reduction": {
            "source_square_quadratic": "z^2 = X^2 + (8 - 2*ell^2)*X + (ell^2 + 4)^2",
            "opposite_square_quadratic": (
                "U^2 = X^2 + (6*ell^2 - 16*ell + 8)*X + (5*ell^2 - 8*ell + 4)^2"
            ),
            "lift_square_forms": {
                "A_ell(X,z)": "2*(X - ell^2 + 4 + z)/ell",
                "B_ell(X,z)": "2*(X - ell^2 - 4 + z) = ell*A_ell(X,z) - 16",
            },
            "identity_checks": identity_checks,
            "t_zero_analysis": t_zero,
            "converse_denominator_analysis": converse_denominators,
        },
        "exact_missing_proposition": {
            "handoff_name": (
                "wl531_m2_pure_v_ell_exact_x_fiber_product_square_lift_proposition_stop"
            ),
            "statement": (
                "For every odd prime ell, the affine X-fiber-product curve defined by "
                "z^2 = X^2 + (8 - 2*ell^2)*X + (ell^2 + 4)^2 and "
                "U^2 = X^2 + (6*ell^2 - 16*ell + 8)*X + (5*ell^2 - 8*ell + 4)^2 "
                "has no rational point (X,z,U) with 0 < X < ell^2, X a rational square, "
                "and both A_ell(X,z) and B_ell(X,z) rational squares."
            ),
            "why_equivalent_to_original_m2": [
                (
                    "Any original quartic point gives X=t^2 together with "
                    "rational z and U on the two quadratics."
                ),
                (
                    "For that point, A_ell(X,z)=u_minus_p^2 and "
                    "B_ell(X,z)=u_pos_2sqrt_q^2 are rational squares."
                ),
                (
                    "Conversely, from X=t^2 and rational squares A_ell(X,z), "
                    "B_ell(X,z), one reconstructs u_minus_p, "
                    "u_pos_2sqrt_q, u_neg_2sqrt_q, then r and y, and the "
                    "reconstructed point satisfies the wl530 quartic and "
                    "centered-even map exactly; the B, r, and r^2-4*ell "
                    "denominators are explicitly nonzero."
                ),
                (
                    "The t=0 / X=0 branch is already excluded, so the only "
                    "remaining positivity range is 0 < X < ell^2."
                ),
            ],
            "first_missing_lemma_reason": (
                "All earlier reductions are exact symbolic identities. The "
                "only unresolved arithmetic step is the simultaneous "
                "rational-point and square-lift claim on this X-fiber-product "
                "curve."
            ),
        },
        "boundary_examples": examples,
        "proof_status": proof_status,
        "violations": violations,
        "boundary": WL531_BOUNDARY,
        "uniform_infinite_subfamily_exclusion_proved_here": False,
        "strict_counterexample_found_here": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


# --- wl532 kernel ---

WL532_BOUNDARY = (
    "This resolves the wl531 exact X-fiber-product proposition only to one "
    "strictly smaller exact arithmetic obstruction. It excludes every odd "
    "prime ell congruent to 3 mod 4, rewrites the remaining 1 mod 4 case in "
    "one square parameter Q, and converts the opposite-side square condition "
    "to one explicit Q-quartic. It does not prove the remaining 1 mod 4 "
    "proposition, does not produce a strict counterexample, does not classify "
    "all rational points on the new quartic, does not enter M3, and does not "
    "claim a complete Selmer upper bound, rank zero, Sha[2]=0, or family "
    "exclusion."
)


def _wl531_ready_wl532(wl531: dict[str, Any]) -> bool:
    proof = wl531.get("proof_status", {})
    return (
        wl531.get("status") == "ok"
        and wl531.get("ready") is True
        and wl531.get("work_log") == "wl531"
        and wl531.get("object_layer")
        == "m2_exact_missing_proposition_after_square_x_and_complete_d_lift_reduction"
        and proof.get("m2_reduced_to_exact_missing_proposition_here") is True
        and proof.get("exact_x_fiber_product_square_lift_proposition_identified_here") is True
        and proof.get("t_zero_excluded_from_the_missing_proposition_here") is True
        and proof.get("uniform_infinite_subfamily_exclusion_proved_here") is False
        and proof.get("strict_counterexample_found_here") is False
        and wl531.get("advance_to_m3") is False
    )


def _identity_checks_wl532() -> list[dict[str, Any]]:
    ell, X = sp.symbols("ell X", nonzero=True)
    A, B, Q, V = sp.symbols("A B Q V", nonzero=True)

    source_quadratic = X**2 + (8 - 2 * ell**2) * X + (ell**2 + 4) ** 2
    opposite_quadratic = X**2 + (6 * ell**2 - 16 * ell + 8) * X + (5 * ell**2 - 8 * ell + 4) ** 2
    x_q = ((ell - Q) * (ell * Q + 4)) / Q
    quartic_q = (
        Q**4
        + (16 - 8 * ell) * Q**3
        + (32 * ell**2 - 96 * ell + 72) * Q**2
        + (32 * ell - 64) * Q
        + 16
    )
    z_q = ell**2 - 4 + 8 * ell / Q - x_q
    A_q = 16 / Q
    B_q = 16 * (ell - Q) / Q

    checks: list[tuple[str, str, sp.Expr]] = [
        (
            "q_definition_from_wl531_lift_square",
            "if Q = 16/A_ell(X,z), then ell - Q = B_ell(X,z)/A_ell(X,z)",
            (ell - 16 / A) - B / A,
        ),
        (
            "x_formula_in_q_coordinate",
            "4*A*X = B*(A+4*ell) and Q=16/A imply X=((ell-Q)*(ell*Q+4))/Q",
            B * (A + 4 * ell) / (4 * A) - ((ell - Q) * (ell * Q + 4)) / Q,
        ),
        (
            "opposite_square_becomes_q_quartic",
            (
                "with X=((ell-Q)*(ell*Q+4))/Q and V=U*Q/ell, the opposite "
                "quadratic becomes V^2=G_ell(Q)"
            ),
            (
                (V * ell / Q) ** 2
                - opposite_quadratic.subs(X, x_q)
                - ell**2 * (V**2 - quartic_q) / Q**2
            ),
        ),
        (
            "quartic_completed_square_form",
            "G_ell(Q) = (Q^2+(8-4*ell)Q-4)^2 + 16*(ell-1)^2*Q^2",
            quartic_q - ((Q**2 + (8 - 4 * ell) * Q - 4) ** 2 + 16 * (ell - 1) ** 2 * Q**2),
        ),
        (
            "converse_a_formula_from_q",
            "A_ell(X,z)=16/Q under the converse reconstruction",
            A_q - 2 * (x_q - ell**2 + 4 + z_q) / ell,
        ),
        (
            "converse_b_formula_from_q",
            "B_ell(X,z)=16*(ell-Q)/Q under the converse reconstruction",
            B_q - 2 * (x_q - ell**2 - 4 + z_q),
        ),
        (
            "converse_source_quadratic_from_q",
            "the reconstructed (X,z) still satisfies the wl531 source quadratic exactly",
            z_q**2 - source_quadratic.subs(X, x_q),
        ),
        (
            "converse_opposite_quadratic_from_q",
            (
                "the reconstructed U=ell*V/Q satisfies the wl531 opposite "
                "quadratic exactly iff V^2=G_ell(Q)"
            ),
            (
                (ell * V / Q) ** 2
                - opposite_quadratic.subs(X, x_q)
                - ell**2 * (V**2 - quartic_q) / Q**2
            ),
        ),
    ]

    payload: list[dict[str, Any]] = []
    substitutions = [
        {B: ell * A - 16, Q: 16 / A},
        {B: ell * A - 16, Q: 16 / A},
        {},
        {},
        {},
        {},
        {},
        {},
    ]

    for (check_id, identity, expr), sub_map in zip(checks, substitutions, strict=True):
        verified = sp.factor(sp.together(expr.subs(sub_map)).as_numer_denom()[0]) == 0
        payload.append({"check_id": check_id, "identity": identity, "verified": verified})
    return payload


def _mod_4_obstruction_wl532() -> dict[str, Any]:
    return {
        "derived_square_coordinates": [
            "Q = 16 / A_ell(X,z)",
            "ell - Q = B_ell(X,z) / A_ell(X,z)",
        ],
        "certificate": {
            "rational_to_primitive_integer_step": (
                "Q=q^2 and ell-Q=p^2 give ell=p^2+q^2. Clearing denominators and "
                "dividing the common gcd gives primitive integers u,w,v with "
                "u^2+w^2=ell*v^2."
            ),
            "mod_ell_step": (
                "Modulo ell, u^2+w^2=0. If w is nonzero modulo ell, then "
                "(u/w)^2=-1. For ell congruent to 3 mod 4, Euler's criterion gives "
                "(-1)^((ell-1)/2)=-1 modulo ell, so -1 is not a square. Thus w=0 "
                "modulo ell, and then u=0 modulo ell."
            ),
            "descent_step": (
                "Writing u=ell*u1 and w=ell*w1 gives ell^2*(u1^2+w1^2)=ell*v^2, "
                "so ell divides v. This contradicts primitiveness."
            ),
            "conclusion": (
                "Therefore, only for the pure v_ell M2 point-existence proposition under "
                "study, a wl531 point can exist only when ell congruent to 1 mod 4."
            ),
        },
        "primes_3_mod_4_excluded": True,
        "remaining_prime_congruence_class": "ell ≡ 1 mod 4",
    }


def _q_coordinate_nonzero_analysis_wl532() -> dict[str, Any]:
    return {
        "Q_nonzero": ("Q=16/A_ell(X,z) is nonzero because wl531 proves A_ell(X,z) is nonzero."),
        "ell_minus_Q_nonzero": (
            "ell-Q=B_ell(X,z)/A_ell(X,z). If ell-Q=0, then B_ell(X,z)=0; "
            "the wl531 source quadratic then forces X=0, contrary to 0<X."
        ),
        "square_factor_inference": (
            "After Q and ell-Q are nonzero rational squares, divide the square identity "
            "X(Q)=((ell-Q)*(ell*Q+4))/Q by the two nonzero square factors. This proves "
            "ell*Q+4 is a rational square."
        ),
        "converse_denominators": (
            "In the converse, Q is nonzero because it is a rational square and X(Q)>0. "
            "Also ell-Q and ell*Q+4 are nonzero: otherwise X(Q)=0. Thus the formulas for "
            "A, B, z, and U have legitimate denominators."
        ),
        "all_nonzero_branches_excluded": True,
    }


def _boundary_examples_wl532() -> dict[str, Any]:
    ell = 13
    q_square = Fraction(9, 1)
    x_value = Fraction((ell - q_square) * (ell * q_square + 4), q_square)
    z_value = Fraction(ell**2 - 4, 1) + Fraction(8 * ell, q_square) - x_value
    quartic_value = (
        q_square**4
        + Fraction(16 - 8 * ell, 1) * q_square**3
        + Fraction(32 * ell**2 - 96 * ell + 72, 1) * q_square**2
        + Fraction(32 * ell - 64, 1) * q_square
        + 16
    )
    return {
        "prime_7_immediate_exclusion": {
            "ell": 7,
            "reason": (
                "Any wl531 point would force ell to be a sum of two rational squares. "
                "The odd prime 7 is congruent to 3 mod 4, so the new Q-coordinate "
                "reduction excludes it immediately."
            ),
        },
        "prime_13_recovered_source_lift_point": {
            "ell": ell,
            "Q": str(q_square),
            "ell_minus_Q": "4",
            "ell_Q_plus_4": "121",
            "X(Q)": str(x_value),
            "z(Q)": str(z_value),
            "quartic_value_G_13(Q)": str(quartic_value),
            "quartic_value_is_rational_square": _is_rational_square_wl532(quartic_value),
            "meaning": (
                "The wl531 source-side lift example at ell=13 becomes the single "
                "Q-value Q=9. The remaining failure is now only the new quartic "
                "square condition G_13(9)."
            ),
        },
    }


def _is_rational_square_wl532(value: Fraction) -> bool:
    if value < 0:
        return False
    return (
        isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction(
    wl531: dict[str, Any] | None = None,
) -> dict[str, Any]:
    wl531 = (
        wl531
        if wl531 is not None
        else build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition()
    )
    identity_checks = _identity_checks_wl532()
    mod_4 = _mod_4_obstruction_wl532()
    nonzero = _q_coordinate_nonzero_analysis_wl532()
    examples = _boundary_examples_wl532()

    violations: list[str] = []
    if not _wl531_ready_wl532(wl531):
        violations.append("wl531_input_not_ready")
    if not all(check["verified"] is True for check in identity_checks):
        violations.append("q_coordinate_identity_check_failed")
    if mod_4["primes_3_mod_4_excluded"] is not True:
        violations.append("mod_4_obstruction_not_recorded")
    if nonzero["all_nonzero_branches_excluded"] is not True:
        violations.append("q_coordinate_nonzero_branch_not_excluded")

    status = "ok" if not violations else "issues"
    ready = status == "ok"
    proof_status = (
        {
            "wl531_shrunk_to_strictly_smaller_exact_obstruction_here": True,
            "primes_3_mod_4_excluded_here": True,
            "remaining_case_is_q_coordinate_quartic_here": True,
            "uniform_infinite_subfamily_exclusion_proved_here": False,
            "strict_counterexample_found_here": False,
            "advance_to_m3": False,
            "stop_after_exact_smaller_obstruction": True,
        }
        if ready
        else {}
    )

    return {
        "status": status,
        "ready": ready,
        "work_log": "wl532",
        "object_layer": "m2_strictly_smaller_q_coordinate_quartic_obstruction_after_wl531",
        "family_scope": {
            "support": "v_ell",
            "L": 1,
            "T": "ell",
            "d_vector": {
                "d_minus_p": "ell",
                "d_pos_2sqrt_q": 1,
                "d_neg_2sqrt_q": "ell",
            },
            "parameter_restrictions": [
                "ell is an odd prime",
                "0 < X(Q) < ell^2",
                "Q is a rational square",
                "ell - Q is a rational square",
                "ell*Q + 4 is a rational square",
            ],
            "touches_only_M2_for_the_wl531_pure_family": True,
        },
        "input_checkpoint": {
            "work_log": "wl531",
            "ready": _wl531_ready_wl532(wl531),
            "handoff": "wl531_m2_pure_v_ell_exact_x_fiber_product_square_lift_proposition_stop",
        },
        "q_coordinate_reduction": {
            "Q_definition": "Q = 16 / A_ell(X,z)",
            "derived_square_relations": {
                "ell - Q": "B_ell(X,z) / A_ell(X,z)",
                "X(Q)": "((ell - Q)*(ell*Q + 4)) / Q",
                "G_ell(Q)": (
                    "Q^4 + (16 - 8*ell)Q^3 + (32*ell^2 - 96*ell + 72)Q^2 + (32*ell - 64)Q + 16"
                ),
                "completed_square_form": ("(Q^2 + (8 - 4*ell)Q - 4)^2 + 16*(ell - 1)^2*Q^2"),
                "V_definition": "V = U*Q/ell",
                "z(Q)": "ell^2 - 4 + 8*ell/Q - X(Q)",
            },
            "identity_checks": identity_checks,
            "mod_4_obstruction": mod_4,
            "nonzero_analysis": nonzero,
        },
        "exact_smaller_obstruction": {
            "handoff_name": "wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction_stop",
            "statement": (
                "For every odd prime ell congruent to 1 mod 4, there is no rational "
                "point (Q,V) such that Q is a rational square, ell-Q is a rational "
                "square, ell*Q+4 is a rational square, 0 < ((ell-Q)*(ell*Q+4))/Q < ell^2, "
                "and V^2 = Q^4 + (16 - 8*ell)Q^3 + (32*ell^2 - 96*ell + 72)Q^2 "
                "+ (32*ell - 64)Q + 16."
            ),
            "why_equivalent_to_wl531": [
                (
                    "Any wl531 point has A_ell(X,z) != 0, so Q=16/A_ell(X,z) is defined "
                    "and is a rational square."
                ),
                (
                    "Because B_ell(X,z)=ell*A_ell(X,z)-16, the ratio B_ell/A_ell equals "
                    "ell-Q and is a rational square."
                ),
                (
                    "The wl531 factorization 4*A_ell*X = B_ell*(A_ell+4*ell) rewrites "
                    "exactly as X(Q)=((ell-Q)*(ell*Q+4))/Q, so ell*Q+4 must also be a "
                    "rational square after the ell-Q=0 branch is excluded by X>0."
                ),
                ("Writing V=U*Q/ell converts the opposite quadratic exactly to V^2=G_ell(Q)."),
                (
                    "Conversely, any Q and V satisfying the displayed conditions "
                    "reconstruct A_ell, B_ell, X, z, and U explicitly and therefore "
                    "rebuild a wl531 point."
                ),
            ],
            "strictly_smaller_reason": (
                "This removes z, A_ell, and B_ell as free variables and discards the "
                "whole ell congruent to 3 mod 4 prime class for this pure-v_ell M2 "
                "point-existence proposition before the last unresolved "
                "quartic square condition is asked."
            ),
        },
        "boundary_examples": examples,
        "proof_status": proof_status,
        "violations": violations,
        "boundary": WL532_BOUNDARY,
        "uniform_infinite_subfamily_exclusion_proved_here": False,
        "strict_counterexample_found_here": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


# --- wl533 kernel ---

WL533_BOUNDARY = (
    "This resolves the wl532 exact Q-coordinate proposition only to one "
    "strictly smaller one-parameter conic-quartic obstruction. It uses the "
    "already-forced prime class ell congruent to 1 mod 4 together with a fixed "
    "integer representation ell=a^2+b^2 to absorb the Q and ell-Q square "
    "conditions into one rational parameter u. It does not prove the remaining "
    "obstruction, does not produce a strict counterexample, does not classify "
    "all rational points on the remaining quartic/conic system, does not enter "
    "M3, and does not claim a complete Selmer upper bound, rank zero, Sha[2]=0, "
    "or family exclusion."
)


def _wl532_ready_wl533(wl532: dict[str, Any]) -> bool:
    proof = wl532.get("proof_status", {})
    return (
        wl532.get("status") == "ok"
        and wl532.get("ready") is True
        and wl532.get("work_log") == "wl532"
        and wl532.get("object_layer")
        == "m2_strictly_smaller_q_coordinate_quartic_obstruction_after_wl531"
        and proof.get("wl531_shrunk_to_strictly_smaller_exact_obstruction_here") is True
        and proof.get("primes_3_mod_4_excluded_here") is True
        and proof.get("remaining_case_is_q_coordinate_quartic_here") is True
        and proof.get("uniform_infinite_subfamily_exclusion_proved_here") is False
        and proof.get("strict_counterexample_found_here") is False
        and wl532.get("advance_to_m3") is False
    )


def _identity_checks_wl533() -> list[dict[str, Any]]:
    ell, a, b, u = sp.symbols("ell a b u", nonzero=True)
    q = sp.symbols("q", nonzero=True)
    D = 1 + u**2
    N = b * (1 - u**2) + 2 * a * u
    P = a * (1 - u**2) - 2 * b * u
    q_u = N / D
    p_u = P / D
    q_quartic = ell * N**2 + 4 * D**2
    a_q = -(q**4) + (8 * ell - 12) * q**2 + 4
    b_q = q**4 + 4 * q**2 - 4
    a_u = -(N**4) + (8 * ell - 12) * N**2 * D**2 + 4 * D**4
    b_u = N**4 + 4 * N**2 * D**2 - 4 * D**4
    Q_u = q_u**2
    G_q = (
        Q_u**4
        + (16 - 8 * ell) * Q_u**3
        + (32 * ell**2 - 96 * ell + 72) * Q_u**2
        + (32 * ell - 64) * Q_u
        + 16
    )

    checks: list[tuple[str, str, sp.Expr, dict[sp.Symbol, sp.Expr]]] = [
        (
            "circle_parameterization_on_ell",
            "with ell=a^2+b^2, the parameter u gives p(u)^2+q(u)^2=ell",
            p_u**2 + q_u**2 - ell,
            {ell: a**2 + b**2},
        ),
        (
            "ell_q_square_plus_4_clears_to_one_quartic",
            "ell*q(u)^2+4 clears exactly to C^2 = ell*N(u)^2 + 4*(1+u^2)^2 with c=C/(1+u^2)",
            D**2 * (ell * q_u**2 + 4) - q_quartic,
            {ell: a**2 + b**2},
        ),
        (
            "x_positivity_formula_in_u",
            "X(u)=((ell-Q(u))*(ell*Q(u)+4))/Q(u)=P(u)^2*(ell*N(u)^2+4*(1+u^2)^2)/(N(u)^2*(1+u^2)^2)",
            (((ell - Q_u) * (ell * Q_u + 4)) / Q_u - (P**2 * q_quartic) / (N**2 * D**2)),
            {ell: a**2 + b**2},
        ),
        (
            "v_quartic_becomes_two_square_sum_in_q",
            "2*G_ell(q^2)=(-q^4+(8*ell-12)q^2+4)^2 + (q^4+4*q^2-4)^2",
            2
            * (
                q**8
                + (16 - 8 * ell) * q**6
                + (32 * ell**2 - 96 * ell + 72) * q**4
                + (32 * ell - 64) * q**2
                + 16
            )
            - (a_q**2 + b_q**2),
            {},
        ),
        (
            "v_relation_clears_to_one_u_sum_of_squares",
            "with Y=V*(1+u^2)^4, the quartic square becomes 2*Y^2=A(u)^2+B(u)^2",
            2 * D**8 * G_q - (a_u**2 + b_u**2),
            {ell: a**2 + b**2},
        ),
        (
            "first_inverse_cross_product",
            "q(u)-b = u*(p(u)+a), with p(u)+a=2*(a-b*u)/(1+u^2)",
            (q_u - b) - u * (p_u + a),
            {},
        ),
        (
            "second_inverse_cross_product",
            "a-p(u) = u*(q(u)+b), with q(u)+b=2*(b+a*u)/(1+u^2)",
            (a - p_u) - u * (q_u + b),
            {},
        ),
        (
            "first_inverse_denominator",
            "p(u)+a = 2*(a-b*u)/(1+u^2)",
            p_u + a - 2 * (a - b * u) / D,
            {},
        ),
        (
            "second_inverse_denominator",
            "q(u)+b = 2*(b+a*u)/(1+u^2)",
            q_u + b - 2 * (b + a * u) / D,
            {},
        ),
    ]

    payload: list[dict[str, Any]] = []
    for check_id, identity, expr, sub_map in checks:
        verified = sp.factor(sp.together(expr.subs(sub_map)).as_numer_denom()[0]) == 0
        payload.append({"check_id": check_id, "identity": identity, "verified": verified})
    return payload


def _inverse_and_branch_analysis_wl533() -> dict[str, Any]:
    return {
        "two_squares_input": (
            "For an odd prime ell congruent to 1 mod 4, fix integers a,b with a^2+b^2=ell."
        ),
        "parameterization": (
            "Set q(u)=(b*(1-u^2)+2*a*u)/(1+u^2) and "
            "p(u)=(a*(1-u^2)-2*b*u)/(1+u^2). Then q(u)^2+p(u)^2=ell."
        ),
        "inverse_formula": (
            "Use u=(q-b)/(p+a) when p+a is nonzero, and u=(a-p)/(q+b) when "
            "q+b is nonzero. The first denominator vanishes only at (-a,b), where "
            "the second equals 2*b; the second vanishes only at (a,-b), where the "
            "first equals 2*a."
        ),
        "antipodal_branch": (
            "The two displayed inverse quotients have removable 0/0 forms at the two "
            "visible points (-a,b) and (a,-b), but the alternate quotient recovers u. "
            "The affine map misses only (-a,-b); that point gives the same Q=q^2=b^2 "
            "as the visible basepoint (a,b) at u=0. Since all wl532 conditions depend "
            "only on Q and V, no wl532 state is lost."
        ),
        "c_nonzero": (
            "The cleared quartic C^2=ell*N(u)^2+4*(1+u^2)^2 has strictly positive "
            "right-hand side, so C is automatically nonzero."
        ),
        "positivity_cross_multiplication": (
            "The strict inequality 0<P(u)^2*C^2<ell^2*N(u)^2*(1+u^2)^2 forces "
            "N(u) != 0. Since (1+u^2)^2 is positive and C^2 is strictly positive, "
            "this makes Q=(N(u)/(1+u^2))^2 nonzero and proves equivalence with the "
            "wl532 range 0<X<ell^2."
        ),
        "all_q_values_covered": True,
    }


def _boundary_examples_wl533() -> dict[str, Any]:
    ell = 13
    a = 2
    b = 3
    u = Fraction(0, 1)
    D = Fraction(1, 1) + u**2
    N = b * (1 - u**2) + 2 * a * u
    P = a * (1 - u**2) - 2 * b * u
    q_square = Fraction(N**2, D**2)
    x_value = Fraction(P**2 * (ell * N**2 + 4 * D**2), N**2 * D**2)
    a_u = -(N**4) + (8 * ell - 12) * N**2 * D**2 + 4 * D**4
    b_u = N**4 + 4 * N**2 * D**2 - 4 * D**4
    g_value = (
        q_square**4
        + Fraction(16 - 8 * ell, 1) * q_square**3
        + Fraction(32 * ell**2 - 96 * ell + 72, 1) * q_square**2
        + Fraction(32 * ell - 64, 1) * q_square
        + 16
    )
    return {
        "prime_5_basepoint_fails_at_the_remaining_c_quartic": {
            "ell": 5,
            "a": 1,
            "b": 2,
            "u": "0",
            "Q(u)": "4",
            "cleared_c_quartic_value": "24",
            "cleared_c_quartic_is_rational_square": False,
            "meaning": (
                "The one-parameter reduction is real: the q and ell-q square conditions "
                "are already absorbed at u=0, and the first remaining failure can occur "
                "immediately at the cleared ell*q(u)^2+4 quartic."
            ),
        },
        "prime_13_recovers_the_wl532_boundary_q_value": {
            "ell": ell,
            "a": a,
            "b": b,
            "u": "0",
            "Q(u)": str(q_square),
            "cleared_c_quartic_value": str(ell * N**2 + 4 * D**2),
            "C(u)": "11",
            "X(u)": str(x_value),
            "A(u)": str(a_u),
            "B(u)": str(b_u),
            "two_g_value": str(2 * g_value),
            "g_value_is_rational_square": _is_rational_square_wl533(g_value),
            "meaning": (
                "At ell=13 with a^2+b^2=13 given by 2^2+3^2, the new parameter u=0 "
                "recovers the old Q=9 boundary point exactly. The remaining failure is "
                "now only the denominator-cleared two-square V-condition."
            ),
        },
    }


def _is_rational_square_wl533(value: Fraction) -> bool:
    if value < 0:
        return False
    return (
        isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def build_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction(
    wl532: dict[str, Any] | None = None,
) -> dict[str, Any]:
    wl532 = (
        wl532 if wl532 is not None else build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction()
    )
    identity_checks = _identity_checks_wl533()
    inverse_analysis = _inverse_and_branch_analysis_wl533()
    examples = _boundary_examples_wl533()

    violations: list[str] = []
    if not _wl532_ready_wl533(wl532):
        violations.append("wl532_input_not_ready")
    if not all(check["verified"] is True for check in identity_checks):
        violations.append("one_parameter_identity_check_failed")
    if inverse_analysis["all_q_values_covered"] is not True:
        violations.append("one_parameter_inverse_not_recorded")

    status = "ok" if not violations else "issues"
    ready = status == "ok"
    proof_status = (
        {
            "wl532_reduced_to_one_parameter_exact_obstruction_here": True,
            "q_and_ell_minus_q_square_conditions_absorbed_here": True,
            "remaining_ell_q_plus_4_and_v_obstructions_recorded_here": True,
            "uniform_infinite_subfamily_exclusion_proved_here": False,
            "strict_counterexample_found_here": False,
            "advance_to_m3": False,
            "stop_after_exact_smaller_obstruction": True,
        }
        if ready
        else {}
    )

    return {
        "status": status,
        "ready": ready,
        "work_log": "wl533",
        "object_layer": "m2_one_parameter_conic_quartic_obstruction_after_wl532",
        "family_scope": {
            "support": "v_ell",
            "L": 1,
            "T": "ell",
            "d_vector": {
                "d_minus_p": "ell",
                "d_pos_2sqrt_q": 1,
                "d_neg_2sqrt_q": "ell",
            },
            "parameter_restrictions": [
                "ell is an odd prime with ell ≡ 1 mod 4",
                "choose integers a,b with a^2+b^2=ell",
                "u is rational",
                "0 < X(u) < ell^2",
                "C^2 = ell*N(u)^2 + 4*(1+u^2)^2",
                "2*Y^2 = A(u)^2 + B(u)^2",
            ],
            "touches_only_M2_for_the_wl532_pure_family": True,
        },
        "input_checkpoint": {
            "work_log": "wl532",
            "ready": _wl532_ready_wl533(wl532),
            "handoff": "wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction_stop",
        },
        "one_parameter_reduction": {
            "classical_input": "Fermat_two_squares_for_primes_1_mod_4",
            "definitions": {
                "D(u)": "1 + u^2",
                "N(u)": "b*(1-u^2) + 2*a*u",
                "P(u)": "a*(1-u^2) - 2*b*u",
                "q(u)": "N(u) / D(u)",
                "Q(u)": "(N(u) / D(u))^2",
                "A(u)": "-N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4",
                "B(u)": "N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4",
                "Y_definition": "Y = V*D(u)^4",
            },
            "identity_checks": identity_checks,
            "inverse_and_branch_analysis": inverse_analysis,
        },
        "exact_smaller_obstruction": {
            "handoff_name": "wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction_stop",
            "statement": (
                "For every odd prime ell congruent to 1 mod 4, fix integers a,b with "
                "a^2+b^2=ell. Define D(u)=1+u^2, N(u)=b*(1-u^2)+2*a*u, "
                "P(u)=a*(1-u^2)-2*b*u, A(u)=-N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4, "
                "and B(u)=N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4. Then there is no rational "
                "triple (u,C,Y) such that C^2 = ell*N(u)^2 + 4*D(u)^2, "
                "0 < P(u)^2*C^2 < ell^2*N(u)^2*D(u)^2, and 2*Y^2 = A(u)^2 + B(u)^2."
            ),
            "why_equivalent_to_wl532": [
                (
                    "Because ell=a^2+b^2, the standard rational-circle parameterization "
                    "q(u)=N(u)/D(u), p(u)=P(u)/D(u) gives q(u)^2+p(u)^2=ell, so "
                    "Q=q(u)^2 and ell-Q=p(u)^2 are automatic."
                ),
                (
                    "The remaining square ell*Q+4 clears exactly to the quartic "
                    "C^2 = ell*N(u)^2 + 4*D(u)^2 with c=C/D(u)."
                ),
                (
                    "The wl532 quartic identity simplifies on the q-coordinate locus to "
                    "2*G_ell(q^2)=(-q^4+(8*ell-12)q^2+4)^2 + (q^4+4*q^2-4)^2, and after "
                    "clearing denominators this becomes 2*Y^2=A(u)^2+B(u)^2."
                ),
                (
                    "Conversely, any rational (u,C,Y) satisfying the displayed conditions "
                    "reconstructs q=N(u)/D(u), Q=q^2, c=C/D(u), and V=Y/D(u)^4, hence a "
                    "genuine wl532 point."
                ),
            ],
            "strictly_smaller_reason": (
                "This absorbs the Q-square and ell-Q-square constraints into one rational "
                "parameter u, leaves only one cleared quartic square condition for ell*Q+4, "
                "and rewrites the V-condition so it no longer depends on the ell*Q+4 square "
                "variable at all."
            ),
        },
        "boundary_examples": examples,
        "proof_status": proof_status,
        "violations": violations,
        "boundary": WL533_BOUNDARY,
        "uniform_infinite_subfamily_exclusion_proved_here": False,
        "strict_counterexample_found_here": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


# --- wl534 kernel ---

WL534_BOUNDARY = (
    "This resolves the wl533 exact one-parameter conic-quartic proposition only "
    "to one strictly smaller one-parameter square-predicate obstruction. It "
    "proves that the lower positivity branch and the hidden Q=0 branch are "
    "automatic for rational u, rewrites the upper positivity range as one "
    "quartic inequality, and removes the auxiliary square-root variables C and "
    "Y in favor of two rational-square predicates. It does not prove the "
    "remaining obstruction, does not produce a strict counterexample, does not "
    "enter M3, and does not claim a complete Selmer upper bound, rank zero, "
    "Sha[2]=0, or family exclusion."
)


def _wl533_ready_wl534(wl533: dict[str, Any]) -> bool:
    proof = wl533.get("proof_status", {})
    return (
        wl533.get("status") == "ok"
        and wl533.get("ready") is True
        and wl533.get("work_log") == "wl533"
        and wl533.get("object_layer") == "m2_one_parameter_conic_quartic_obstruction_after_wl532"
        and proof.get("wl532_reduced_to_one_parameter_exact_obstruction_here") is True
        and proof.get("q_and_ell_minus_q_square_conditions_absorbed_here") is True
        and proof.get("remaining_ell_q_plus_4_and_v_obstructions_recorded_here") is True
        and proof.get("uniform_infinite_subfamily_exclusion_proved_here") is False
        and proof.get("strict_counterexample_found_here") is False
        and wl533.get("advance_to_m3") is False
    )


def _identity_checks_wl534() -> list[dict[str, Any]]:
    ell, a, b, u = sp.symbols("ell a b u", nonzero=True)
    D = 1 + u**2
    N = b * (1 - u**2) + 2 * a * u
    P = a * (1 - u**2) - 2 * b * u
    S = ell * N**2 + 4 * D**2
    A = -(N**4) + (8 * ell - 12) * N**2 * D**2 + 4 * D**4
    B = N**4 + 4 * N**2 * D**2 - 4 * D**4
    T = (A**2 + B**2) / 2
    R = ell * N**4 + 4 * N**2 * D**2 - 4 * ell * D**4
    Q = N**2 / D**2

    checks: list[tuple[str, str, sp.Expr, dict[sp.Symbol, sp.Expr]]] = [
        (
            "p_n_norm_identity",
            "P(u)^2 + N(u)^2 = ell*(1+u^2)^2",
            P**2 + N**2 - ell * D**2,
            {ell: a**2 + b**2},
        ),
        (
            "upper_positivity_difference",
            "ell^2*N(u)^2*D(u)^2 - P(u)^2*S(u) = R(u)",
            ell**2 * N**2 * D**2 - P**2 * S - R,
            {ell: a**2 + b**2},
        ),
        (
            "range_quartic_in_q",
            "R(u) = D(u)^4*(ell*Q(u)^2 + 4*Q(u) - 4*ell)",
            R - D**4 * (ell * Q**2 + 4 * Q - 4 * ell),
            {ell: a**2 + b**2},
        ),
        (
            "a_plus_b_positive_identity",
            "A(u) + B(u) = 8*(ell-1)*N(u)^2*D(u)^2",
            A + B - 8 * (ell - 1) * N**2 * D**2,
            {},
        ),
        (
            "t_is_half_sum_of_squares",
            "2*T(u) = A(u)^2 + B(u)^2",
            2 * T - (A**2 + B**2),
            {},
        ),
    ]

    payload: list[dict[str, Any]] = []
    for check_id, identity, expr, sub_map in checks:
        verified = sp.factor(sp.together(expr.subs(sub_map)).as_numer_denom()[0]) == 0
        payload.append({"check_id": check_id, "identity": identity, "verified": verified})
    return payload


def _zero_branch_analysis_wl534() -> dict[str, Any]:
    a, b, u = sp.symbols("a b u", nonzero=True)
    p_poly = sp.Poly(a * (1 - u**2) - 2 * b * u, u)
    n_poly = sp.Poly(b * (1 - u**2) + 2 * a * u, u)
    p_disc = sp.factor(p_poly.discriminant())
    n_disc = sp.factor(n_poly.discriminant())
    discriminants_equal = (
        sp.simplify(p_disc - 4 * (a**2 + b**2)) == 0
        and sp.simplify(n_disc - 4 * (a**2 + b**2)) == 0
    )
    return {
        "P(u)_quadratic": "a*u^2 + 2*b*u - a = 0",
        "N(u)_quadratic": "b*u^2 - 2*a*u - b = 0",
        "P(u)_discriminant": "4*ell",
        "N(u)_discriminant": "4*ell",
        "discriminants_equal_4ell": discriminants_equal,
        "reason": (
            "For an odd prime ell, sqrt(ell) is not rational. Therefore a quadratic "
            "with discriminant 4*ell has no rational root. So P(u)=0 and N(u)=0 are "
            "impossible for rational u."
        ),
        "P(u)_has_rational_root": False,
        "N(u)_has_rational_root": False,
        "lower_positivity_branch_automatic": True,
        "hidden_q_zero_branch_automatic": True,
    }


def _boundary_examples_wl534() -> dict[str, Any]:
    def values(ell: int, a: int, b: int, u: Fraction) -> dict[str, str | int | bool]:
        D = Fraction(1, 1) + u**2
        N = b * (1 - u**2) + 2 * a * u
        A = -(N**4) + (8 * ell - 12) * N**2 * D**2 + 4 * D**4
        B = N**4 + 4 * N**2 * D**2 - 4 * D**4
        S = ell * N**2 + 4 * D**2
        R = ell * N**4 + 4 * N**2 * D**2 - 4 * ell * D**4
        T = Fraction(A**2 + B**2, 2)
        return {
            "ell": ell,
            "a": a,
            "b": b,
            "u": str(u),
            "S(u)": str(S),
            "S(u)_is_rational_square": _is_rational_square_wl534(S),
            "R(u)": str(R),
            "R(u)_is_positive": R > 0,
            "T(u)": str(T),
            "T(u)_is_rational_square": _is_rational_square_wl534(T),
        }

    example_5 = values(ell=5, a=1, b=2, u=Fraction(0, 1))
    example_5["meaning"] = (
        "At ell=5 and u=0, the new upper range already holds, but the first "
        "remaining failure is exactly the square predicate S(u)."
    )

    example_13 = values(ell=13, a=2, b=3, u=Fraction(0, 1))
    example_13["meaning"] = (
        "At ell=13 and u=0, the conic-quartic part and the strict range both hold, "
        "but the remaining failure is exactly the square predicate T(u)."
    )

    return {
        "prime_5_basepoint_fails_at_s_square_predicate": example_5,
        "prime_13_basepoint_fails_at_t_square_predicate": example_13,
    }


def _is_rational_square_wl534(value: Fraction) -> bool:
    if value < 0:
        return False
    return (
        isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def build_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction(
    wl533: dict[str, Any] | None = None,
) -> dict[str, Any]:
    wl533 = (
        wl533
        if wl533 is not None
        else build_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction()
    )
    identity_checks = _identity_checks_wl534()
    zero_branch_analysis = _zero_branch_analysis_wl534()
    examples = _boundary_examples_wl534()

    violations: list[str] = []
    if not _wl533_ready_wl534(wl533):
        violations.append("wl533_input_not_ready")
    if not all(check["verified"] is True for check in identity_checks):
        violations.append("square_predicate_identity_check_failed")
    if zero_branch_analysis["discriminants_equal_4ell"] is not True:
        violations.append("zero_branch_discriminant_check_failed")

    status = "ok" if not violations else "issues"
    ready = status == "ok"
    proof_status = (
        {
            "wl533_reduced_to_one_parameter_square_predicate_obstruction_here": True,
            "auxiliary_C_and_Y_variables_eliminated_here": True,
            "lower_positivity_and_zero_branches_automatic_here": True,
            "remaining_problem_is_two_square_predicates_plus_one_inequality": True,
            "uniform_infinite_subfamily_exclusion_proved_here": False,
            "strict_counterexample_found_here": False,
            "advance_to_m3": False,
            "stop_after_exact_smaller_obstruction": True,
        }
        if ready
        else {}
    )

    return {
        "status": status,
        "ready": ready,
        "work_log": "wl534",
        "object_layer": "m2_one_parameter_square_predicate_obstruction_after_wl533",
        "family_scope": {
            "support": "v_ell",
            "L": 1,
            "T": "ell",
            "d_vector": {
                "d_minus_p": "ell",
                "d_pos_2sqrt_q": 1,
                "d_neg_2sqrt_q": "ell",
            },
            "parameter_restrictions": [
                "ell is an odd prime with ell ≡ 1 mod 4",
                "choose integers a,b with a^2+b^2=ell",
                "u is rational",
                "S(u) = ell*N(u)^2 + 4*D(u)^2 is a rational square",
                "R(u) = ell*N(u)^4 + 4*N(u)^2*D(u)^2 - 4*ell*D(u)^4 is positive",
                "T(u) = (A(u)^2 + B(u)^2)/2 is a rational square",
            ],
            "touches_only_M2_for_the_wl533_pure_family": True,
        },
        "input_checkpoint": {
            "work_log": "wl533",
            "ready": _wl533_ready_wl534(wl533),
            "handoff": "wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction_stop",
        },
        "one_parameter_square_predicate_reduction": {
            "definitions": {
                "D(u)": "1 + u^2",
                "N(u)": "b*(1-u^2) + 2*a*u",
                "P(u)": "a*(1-u^2) - 2*b*u",
                "S(u)": "ell*N(u)^2 + 4*D(u)^2",
                "R(u)": "ell*N(u)^4 + 4*N(u)^2*D(u)^2 - 4*ell*D(u)^4",
                "A(u)": "-N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4",
                "B(u)": "N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4",
                "T(u)": "(A(u)^2 + B(u)^2) / 2",
            },
            "identity_checks": identity_checks,
            "zero_branch_analysis": zero_branch_analysis,
        },
        "exact_smaller_obstruction": {
            "handoff_name": "wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction_stop",
            "statement": (
                "For every odd prime ell congruent to 1 mod 4, fix integers a,b with "
                "a^2+b^2=ell. Define D(u)=1+u^2, N(u)=b*(1-u^2)+2*a*u, "
                "A(u)=-N(u)^4 + (8*ell-12)N(u)^2*D(u)^2 + 4*D(u)^4, "
                "B(u)=N(u)^4 + 4*N(u)^2*D(u)^2 - 4*D(u)^4, "
                "S(u)=ell*N(u)^2 + 4*D(u)^2, "
                "R(u)=ell*N(u)^4 + 4*N(u)^2*D(u)^2 - 4*ell*D(u)^4, and "
                "T(u)=(A(u)^2 + B(u)^2)/2. Then there is no rational u such that "
                "S(u) is a rational square, R(u) > 0, and T(u) is a rational square."
            ),
            "why_equivalent_to_wl533": [
                (
                    "The wl533 quartic variable is purely existential: C exists exactly "
                    "when S(u)=ell*N(u)^2 + 4*D(u)^2 is a rational square."
                ),
                (
                    "The wl533 Y-variable is purely existential: 2*Y^2 = A(u)^2 + B(u)^2 "
                    "holds exactly when T(u)=(A(u)^2 + B(u)^2)/2 is a rational square."
                ),
                (
                    "The lower positivity branch is automatic for rational u because "
                    "P(u)=0 has discriminant 4*ell and therefore no rational root."
                ),
                (
                    "The upper positivity branch is exactly R(u)>0, because "
                    "ell^2*N(u)^2*D(u)^2 - P(u)^2*(ell*N(u)^2 + 4*D(u)^2) = R(u)."
                ),
            ],
            "strictly_smaller_reason": (
                "This removes the auxiliary square-root variables C and Y, removes the "
                "automatic lower positivity and Q=0 branch checks, and leaves only one "
                "rational parameter with two square predicates and one quartic inequality."
            ),
        },
        "boundary_examples": examples,
        "proof_status": proof_status,
        "violations": violations,
        "boundary": WL534_BOUNDARY,
        "uniform_infinite_subfamily_exclusion_proved_here": False,
        "strict_counterexample_found_here": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


@dataclass(frozen=True)
class C1Evidence:
    """Computed C1 stages, kept immutable at the public boundary."""

    stages: Mapping[str, dict[str, Any]]

    def __getitem__(self, work_log: str) -> dict[str, Any]:
        return self.stages[work_log]


def build_c1() -> C1Evidence:
    """Run the wl530-wl541 canonical C1 kernels without legacy runtime inputs."""
    from scripts.theory.aa_bb.c1_local_tables import build_local_stages
    from scripts.theory.aa_bb.c1_wl539 import build_wl539
    from scripts.theory.aa_bb.c1_wl540 import build_wl540
    from scripts.theory.aa_bb.c1_wl541 import build_wl541

    wl530 = build_wl530_m1_pure_v_ell_symbolic_family()
    wl531 = build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition(wl530)
    wl532 = build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction(wl531)
    wl533 = build_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction(wl532)
    wl534 = build_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction(wl533)
    stages = {
        "wl530": wl530,
        "wl531": wl531,
        "wl532": wl532,
        "wl533": wl533,
        "wl534": wl534,
    }
    stages["wl535"] = build_wl535(stages["wl534"])
    stages.update(build_local_stages(stages["wl535"]))
    stages["wl539"] = build_wl539(stages["wl538"])
    stages["wl540"] = build_wl540(stages["wl539"])
    stages["wl541"] = build_wl541(stages["wl540"])
    return C1Evidence(stages=stages)


def project_stage(evidence: C1Evidence, work_log: str) -> dict[str, Any]:
    """Return one computed stage after enforcing the explicit C1 stage map."""
    if work_log not in {f"wl{number}" for number in range(530, 542)}:
        raise KeyError(f"unknown C1 work log: {work_log}")
    payload = evidence.stages[work_log]
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    return payload


def semantic_projection(payload: Mapping[str, Any], work_log: str) -> dict[str, Any]:
    """Remove only execution-cache fields from a C1 parity payload."""
    if payload.get("work_log") != work_log:
        raise ValueError(f"stage label mismatch for {work_log}")
    projected = {key: value for key, value in payload.items() if key not in {"ready", "violations"}}
    return json.loads(json.dumps(projected, sort_keys=True))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    evidence = build_c1()
    payload = {"schema_version": 1, "stages": evidence.stages}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote C1 consolidated audit to {args.out}")
    print(f"stage_count={len(evidence.stages)}")
    ok = all(stage.get("status") == "ok" for stage in evidence.stages.values())
    print(f"status={'ok' if ok else 'issues'}")
    return 1 if args.strict and not ok else 0


if __name__ == "__main__":
    raise SystemExit(main())
