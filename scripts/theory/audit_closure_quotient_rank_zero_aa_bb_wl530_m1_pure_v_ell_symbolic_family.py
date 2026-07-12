#!/usr/bin/env python3
"""Derive the M1 symbolic pure v_ell family and its square-locus formulas."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import sympy as sp

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json


BOUNDARY = (
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


def _sympy_reduces_to_zero(expr: sp.Expr, *, ell: sp.Symbol, r: sp.Symbol, y: sp.Symbol) -> bool:
    function_field_rhs = ell * r**4 - 8 * (ell**2 + 8) * r**2 + 16 * ell**3
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(sp.expand(numerator), y),
        sp.Poly(y**2 - function_field_rhs, y),
    ).as_expr()
    return sp.factor(remainder) == 0


def _function_field_identity_checks() -> list[dict[str, Any]]:
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
            verified = _sympy_reduces_to_zero(expr, ell=ell, r=r, y=y)
        elif check_id == "square_locus_quartic_identity":
            verified = sp.factor(expr) == 0
        else:
            verified = sp.factor(
                expr.subs({Xq: t**2, Yq: t * U}) - t**2 * (U**2 - quartic)
            ) == 0
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


def _ell_5_recovery() -> dict[str, Any]:
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
    identity_checks = _function_field_identity_checks()
    recovery = _ell_5_recovery()
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
                "Y^2 = X^3 + (6*ell^2 - 16*ell + 8)*X^2 + "
                "(5*ell^2 - 8*ell + 4)^2*X"
            ),
            "degree_two_map": "X = t^2, Y = t*U",
            "quartic_discriminant": "65536*ell^4*(ell - 1)^4*(5*ell^2 - 8*ell + 4)^2",
            "elliptic_rhs_cubic_discriminant": (
                "-64*ell^2*(ell - 1)^2*(5*ell^2 - 8*ell + 4)^4"
            ),
        },
        "ell_5_recovery": recovery,
        "proof_status": proof_status,
        "violations": violations,
        "boundary": BOUNDARY,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "advance_to_m2": False,
        "stop_after_current_task": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family.json"),
        help="Output path for the wl530 M1 symbolic family audit JSON.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_wl530_m1_pure_v_ell_symbolic_family()
    write_json(args.out, payload)
    print(f"wrote wl530 M1 symbolic family audit to {args.out}")
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m2={payload['advance_to_m2']}")
    if args.strict and payload["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
