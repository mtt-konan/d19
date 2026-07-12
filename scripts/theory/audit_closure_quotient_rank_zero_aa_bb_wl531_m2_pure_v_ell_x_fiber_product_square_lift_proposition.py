#!/usr/bin/env python3
"""Reduce wl530 M2 to an exact X-fiber-product square-lift proposition."""

from __future__ import annotations

import argparse
import importlib
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl530_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl530_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family"
    )
    from json_io import write_json


BOUNDARY = (
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


def _wl530_ready(wl530: dict[str, Any]) -> bool:
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


def _sympy_reduces_to_zero(expr: sp.Expr, *, ell: sp.Symbol, r: sp.Symbol, y: sp.Symbol) -> bool:
    function_field_rhs = ell * r**4 - 8 * (ell**2 + 8) * r**2 + 16 * ell**3
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(
        sp.Poly(sp.expand(numerator), y),
        sp.Poly(y**2 - function_field_rhs, y),
    ).as_expr()
    return sp.factor(remainder) == 0


def _identity_checks() -> list[dict[str, Any]]:
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
            - (2 * (X - ell**2 - 4 + z))
            * (2 * (X - ell**2 + 4 + z) / ell + 4 * ell),
            "source_quadratic",
        ),
        (
            "b_is_ell_a_minus_16",
            "B_ell(X,z) = ell*A_ell(X,z) - 16",
            (2 * (X - ell**2 - 4 + z))
            - (ell * (2 * (X - ell**2 + 4 + z) / ell) - 16),
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
            - (
                ell * (um + un) ** 4
                - 8 * (ell**2 + 8) * (um + un) ** 2
                + 16 * ell**3
            ),
            "two_square_relations",
        ),
        (
            "reconstructed_t_matches_centered_even_map",
            (
                "with r=u_minus+u_neg and y=2*r*u_pos, the centered-even map "
                "gives t=u_pos*u_neg/(2*u_minus)"
            ),
            (
                (2 * (um + un) * up) * ((um + un) ** 2 + 4 * ell)
            )
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
            verified = _sympy_reduces_to_zero(expr, ell=ell, r=r, y=y)
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


def _t_zero_analysis() -> dict[str, Any]:
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


def _converse_denominator_analysis() -> dict[str, Any]:
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


def _is_rational_square(value: Fraction) -> bool:
    if value < 0:
        return False
    return (
        isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def _boundary_examples() -> dict[str, Any]:
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
            "source_quadratic_is_rational_square": _is_rational_square(q_source),
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
            "A_is_rational_square": _is_rational_square(a2),
            "B_is_rational_square": _is_rational_square(b2),
            "opposite_quadratic_value": str(q_opp),
            "opposite_quadratic_is_rational_square": _is_rational_square(q_opp),
            "meaning": (
                "A genuine complete-d lift can satisfy the source-side square conditions in the "
                "positivity range while still failing the opposite-side square condition."
            ),
        },
    }


def build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition() -> dict[str, Any]:
    wl530 = wl530_module.build_wl530_m1_pure_v_ell_symbolic_family()
    identity_checks = _identity_checks()
    t_zero = _t_zero_analysis()
    converse_denominators = _converse_denominator_analysis()
    examples = _boundary_examples()

    violations: list[str] = []
    if not _wl530_ready(wl530):
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
            "ready": _wl530_ready(wl530),
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
        "boundary": BOUNDARY,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "results/closure_quotient_rank_zero_aa_bb_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition.json"
        ),
        help="Output path for the wl531 M2 exact-missing-proposition audit JSON.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition()
    write_json(args.out, payload)
    print(f"wrote wl531 M2 reduction audit to {args.out}")
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    if args.strict and payload["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
