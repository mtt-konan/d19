#!/usr/bin/env python3
"""Reformulate wl534 in the direct q-root coordinate."""

from __future__ import annotations

import argparse
import importlib
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl534_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl534_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction"
    )
    from json_io import write_json


BOUNDARY = (
    "This rewrites the wl534 exact one-parameter square-predicate proposition "
    "as one coordinate-free direct q-root-coordinate square/quartic "
    "reformulation. It removes the fixed sum-of-two-squares chart from the "
    "final statement, rewrites the three wl534 predicates in the direct q-root "
    "coordinate, and packages the last square predicate into one explicit "
    "q-coordinate quartic curve equation. It does not prove the remaining "
    "obstruction, does not produce a strict counterexample, does not enter M3, "
    "and does not claim a complete Selmer upper bound, rank zero, Sha[2]=0, "
    "or family exclusion."
)


def _wl534_ready(wl534: dict[str, Any]) -> bool:
    proof = wl534.get("proof_status", {})
    return (
        wl534.get("status") == "ok"
        and wl534.get("ready") is True
        and wl534.get("work_log") == "wl534"
        and wl534.get("object_layer")
        == "m2_one_parameter_square_predicate_obstruction_after_wl533"
        and proof.get("wl533_reduced_to_one_parameter_square_predicate_obstruction_here")
        is True
        and proof.get("auxiliary_C_and_Y_variables_eliminated_here") is True
        and proof.get("lower_positivity_and_zero_branches_automatic_here") is True
        and proof.get("remaining_problem_is_two_square_predicates_plus_one_inequality")
        is True
        and proof.get("uniform_infinite_subfamily_exclusion_proved_here") is False
        and proof.get("strict_counterexample_found_here") is False
        and wl534.get("advance_to_m3") is False
    )


def _verified_zero(expr: sp.Expr, sub_map: dict[sp.Symbol, sp.Expr] | None = None) -> bool:
    expr = expr.subs(sub_map or {})
    return sp.factor(sp.together(expr).as_numer_denom()[0]) == 0


def _verified_mod_circle_relation(expr: sp.Expr) -> bool:
    p, q, a, b = sp.symbols("p q a b", nonzero=True)
    circle_gap = p**2 + q**2 - a**2 - b**2
    numerator = sp.expand(sp.together(expr).as_numer_denom()[0])
    _, remainder = sp.Poly(numerator, p, q, a, b).div(
        sp.Poly(circle_gap, p, q, a, b)
    )
    return remainder == 0


def _identity_checks() -> list[dict[str, Any]]:
    ell, a, b, u = sp.symbols("ell a b u", nonzero=True)
    D = 1 + u**2
    N = b * (1 - u**2) + 2 * a * u
    P = a * (1 - u**2) - 2 * b * u
    q_u = sp.together(N / D)
    p_u = sp.together(P / D)
    Q_u = q_u**2
    S = ell * N**2 + 4 * D**2
    R = ell * N**4 + 4 * N**2 * D**2 - 4 * ell * D**4
    A = -N**4 + (8 * ell - 12) * N**2 * D**2 + 4 * D**4
    B = N**4 + 4 * N**2 * D**2 - 4 * D**4
    T = (A**2 + B**2) / 2
    G = (
        Q_u**4
        + (16 - 8 * ell) * Q_u**3
        + (32 * ell**2 - 96 * ell + 72) * Q_u**2
        + (32 * ell - 64) * Q_u
        + 16
    )

    checks: list[tuple[str, str, sp.Expr, dict[sp.Symbol, sp.Expr]]] = [
        (
            "circle_identity_in_q_root_coordinate",
            "with ell=a^2+b^2, the direct q(u),p(u) coordinates satisfy q(u)^2+p(u)^2=ell",
            q_u**2 + p_u**2 - ell,
            {ell: a**2 + b**2},
        ),
        (
            "ell_minus_q_square_is_automatic",
            "ell-q(u)^2 = p(u)^2",
            ell - q_u**2 - p_u**2,
            {ell: a**2 + b**2},
        ),
        (
            "s_predicate_descends_to_q_root_coordinate",
            "S(u)=D(u)^2*(ell*q(u)^2+4)",
            S - D**2 * (ell * q_u**2 + 4),
            {},
        ),
        (
            "r_predicate_descends_to_q_root_coordinate",
            "R(u)=D(u)^4*(ell*q(u)^4+4*q(u)^2-4*ell)",
            R - D**4 * (ell * q_u**4 + 4 * q_u**2 - 4 * ell),
            {},
        ),
        (
            "t_predicate_descends_to_q_root_quartic",
            "T(u)=D(u)^8*G_ell(q(u)^2)",
            T - D**8 * G,
            {},
        ),
        (
            "first_inverse_cross_product",
            "q(u)-b = u*(p(u)+a)",
            (q_u - b) - u * (p_u + a),
            {},
        ),
        (
            "second_inverse_cross_product",
            "a-p(u) = u*(q(u)+b)",
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
        verified = _verified_zero(expr, sub_map)
        payload.append({"check_id": check_id, "identity": identity, "verified": verified})
    return payload


def _inverse_and_branch_analysis() -> dict[str, Any]:
    a, b, p, q, u, ell = sp.symbols("a b p q u ell", nonzero=True)
    D = 1 + u**2
    N = b * (1 - u**2) + 2 * a * u
    P = a * (1 - u**2) - 2 * b * u
    q_u = sp.together(N / D)
    p_u = sp.together(P / D)
    u_first_patch = sp.together((q - b) / (p + a))
    u_second_patch = sp.together((a - p) / (q + b))

    def stringify(expr: sp.Expr) -> str:
        return sp.sstr(sp.simplify(expr))

    generic_patch_checks = [
        {
            "check_id": "first_patch_recovers_q",
            "identity": "if p+a != 0 and p^2+q^2=a^2+b^2, then q((q-b)/(p+a)) = q",
            "verified": _verified_mod_circle_relation(
                (b * (1 - u_first_patch**2) + 2 * a * u_first_patch)
                / (1 + u_first_patch**2)
                - q
            ),
        },
        {
            "check_id": "first_patch_recovers_p",
            "identity": "if p+a != 0 and p^2+q^2=a^2+b^2, then p((q-b)/(p+a)) = p",
            "verified": _verified_mod_circle_relation(
                (a * (1 - u_first_patch**2) - 2 * b * u_first_patch)
                / (1 + u_first_patch**2)
                - p
            ),
        },
        {
            "check_id": "second_patch_recovers_q",
            "identity": "if q+b != 0 and p^2+q^2=a^2+b^2, then q((a-p)/(q+b)) = q",
            "verified": _verified_mod_circle_relation(
                (b * (1 - u_second_patch**2) + 2 * a * u_second_patch)
                / (1 + u_second_patch**2)
                - q
            ),
        },
        {
            "check_id": "second_patch_recovers_p",
            "identity": "if q+b != 0 and p^2+q^2=a^2+b^2, then p((a-p)/(q+b)) = p",
            "verified": _verified_mod_circle_relation(
                (a * (1 - u_second_patch**2) - 2 * b * u_second_patch)
                / (1 + u_second_patch**2)
                - p
            ),
        },
    ]

    branch_minus_a_b = {
        "branch_point": "(-a,b)",
        "branch_condition": "p+a = 0 and q+b != 0",
        "recovered_u": "a/b",
        "point_coordinates": {
            "q(a/b)": stringify(q_u.subs(u, a / b)),
            "p(a/b)": stringify(p_u.subs(u, a / b)),
        },
        "alternate_denominator": stringify((q_u + b).subs(u, a / b)),
        "alternate_formula_value": stringify(((a - p_u) / (q_u + b)).subs(u, a / b)),
        "verified": all(
            [
                _verified_zero(q_u.subs(u, a / b) - b),
                _verified_zero(p_u.subs(u, a / b) + a),
                _verified_zero((q_u + b).subs(u, a / b) - 2 * b),
                _verified_zero(((a - p_u) / (q_u + b)).subs(u, a / b) - a / b),
            ]
        ),
    }
    branch_a_minus_b = {
        "branch_point": "(a,-b)",
        "branch_condition": "q+b = 0 and p+a != 0",
        "recovered_u": "-b/a",
        "point_coordinates": {
            "q(-b/a)": stringify(q_u.subs(u, -b / a)),
            "p(-b/a)": stringify(p_u.subs(u, -b / a)),
        },
        "alternate_denominator": stringify((p_u + a).subs(u, -b / a)),
        "alternate_formula_value": stringify(((q_u - b) / (p_u + a)).subs(u, -b / a)),
        "verified": all(
            [
                _verified_zero(q_u.subs(u, -b / a) + b),
                _verified_zero(p_u.subs(u, -b / a) - a),
                _verified_zero((p_u + a).subs(u, -b / a) - 2 * a),
                _verified_zero(((q_u - b) / (p_u + a)).subs(u, -b / a) + b / a),
            ]
        ),
    }

    q_symbol = sp.symbols("q", nonzero=True)
    G_q = (
        q_symbol**8
        + (16 - 8 * ell) * q_symbol**6
        + (32 * ell**2 - 96 * ell + 72) * q_symbol**4
        + (32 * ell - 64) * q_symbol**2
        + 16
    )
    q_sign_invariance_checks = [
        {
            "check_id": "ell_minus_q_square_even_in_q",
            "identity": "ell-(-q)^2 = ell-q^2",
            "verified": _verified_zero((ell - (-q_symbol) ** 2) - (ell - q_symbol**2)),
        },
        {
            "check_id": "ell_q_square_plus_4_even_in_q",
            "identity": "ell*(-q)^2+4 = ell*q^2+4",
            "verified": _verified_zero(
                (ell * (-q_symbol) ** 2 + 4) - (ell * q_symbol**2 + 4)
            ),
        },
        {
            "check_id": "positivity_polynomial_even_in_q",
            "identity": "ell*(-q)^4+4*(-q)^2-4*ell = ell*q^4+4*q^2-4*ell",
            "verified": _verified_zero(
                ell * (-q_symbol) ** 4
                + 4 * (-q_symbol) ** 2
                - 4 * ell
                - (ell * q_symbol**4 + 4 * q_symbol**2 - 4 * ell)
            ),
        },
        {
            "check_id": "quartic_curve_rhs_even_in_q",
            "identity": "G_ell((-q)^2) = G_ell(q^2)",
            "verified": _verified_zero(
                G_q.subs(q_symbol, -q_symbol) - G_q
            ),
        },
    ]
    antipode_sign_branch = {
        "missed_point": "(-a,-b)",
        "sign_switched_visible_point": "(a,-b)",
        "same_q_after_sign_switch": "-b",
        "recovered_u_after_sign_switch": "-b/a",
        "verified": all(
            [
                _verified_zero(a - a),
                _verified_zero(((-b) - b) / (a + a) + b / a),
            ]
        )
        and all(check["verified"] for check in q_sign_invariance_checks),
    }

    all_q_values_covered = (
        all(check["verified"] for check in generic_patch_checks)
        and branch_minus_a_b["verified"] is True
        and branch_a_minus_b["verified"] is True
        and antipode_sign_branch["verified"] is True
        and all(check["verified"] for check in q_sign_invariance_checks)
    )

    return {
        "q_root_coordinate_statement": (
            "Use the direct rational q-root coordinate on p^2+q^2=ell rather than the "
            "chart variable u."
        ),
        "inverse_formula": (
            "Given q and a chosen rational square root p of ell-q^2, use "
            "u=(q-b)/(p+a) when p+a is nonzero, and u=(a-p)/(q+b) when q+b is nonzero."
        ),
        "nonzero_a_b_reason": (
            "For an odd prime ell with a^2+b^2=ell, neither a nor b can vanish; "
            "otherwise ell would be an integer square."
        ),
        "generic_patch_reconstruction_checks": generic_patch_checks,
        "removable_branches": {
            "visible_branch_minus_a_b": branch_minus_a_b,
            "visible_branch_a_minus_b": branch_a_minus_b,
        },
        "antipode_sign_branch": antipode_sign_branch,
        "q_sign_invariance_checks": q_sign_invariance_checks,
        "branch_summary": (
            "The p+a patch covers every circle point except (-a,b) and (-a,-b); the "
            "q+b patch covers every circle point except (a,-b) and (-a,-b). The two "
            "visible exceptional points are removable by the alternate quotient, and "
            "the antipode is recovered by switching the sign of p."
        ),
        "nonzero_denominator_reason": (
            "D(u)=1+u^2 is never zero over Q, so the descents and lifts across D(u)^2 "
            "and D(u)^8 are exact."
        ),
        "q_nonzero_from_positivity": (
            "The positivity polynomial ell*q^4+4*q^2-4*ell equals -4*ell at q=0, so any "
            "positive solution automatically has q != 0."
        ),
        "all_q_values_covered": all_q_values_covered,
    }


def _is_rational_square(value: Fraction) -> bool:
    if value < 0:
        return False
    return (
        isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def _g_value(ell: int, q: Fraction) -> Fraction:
    Q = q * q
    return (
        Q**4
        + Fraction(16 - 8 * ell, 1) * Q**3
        + Fraction(32 * ell**2 - 96 * ell + 72, 1) * Q**2
        + Fraction(32 * ell - 64, 1) * Q
        + 16
    )


def _boundary_examples() -> dict[str, Any]:
    def values(ell: int, q: Fraction) -> dict[str, str | int | bool]:
        ell_minus_q_square = Fraction(ell, 1) - q * q
        s_value = Fraction(ell, 1) * q * q + 4
        r_value = Fraction(ell, 1) * q**4 + 4 * q * q - 4 * ell
        g_value = _g_value(ell, q)
        return {
            "ell": ell,
            "q": str(q),
            "ell-q^2": str(ell_minus_q_square),
            "ell-q^2_is_rational_square": _is_rational_square(ell_minus_q_square),
            "ell*q^2+4": str(s_value),
            "ell*q^2+4_is_rational_square": _is_rational_square(s_value),
            "ell*q^4+4*q^2-4*ell": str(r_value),
            "positivity_holds": r_value > 0,
            "G_ell(q^2)": str(g_value),
            "G_ell(q^2)_is_rational_square": _is_rational_square(g_value),
        }

    example_5 = values(ell=5, q=Fraction(1, 1))
    example_5["meaning"] = (
        "Both square predicates already hold at ell=5, q=1, but the strict positivity "
        "condition still fails."
    )

    example_13 = values(ell=13, q=Fraction(3, 1))
    example_13["meaning"] = (
        "At ell=13, q=3 the two square predicates and the strict positivity condition "
        "all hold, but the remaining failure is exactly the direct q-coordinate "
        "quartic-square condition."
    )

    return {
        "prime_5_square_predicates_hold_but_positivity_fails": example_5,
        "prime_13_only_the_q_root_quartic_square_condition_remains": example_13,
    }


def build_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction() -> dict[str, Any]:
    wl534 = wl534_module.build_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction()
    identity_checks = _identity_checks()
    inverse_analysis = _inverse_and_branch_analysis()
    examples = _boundary_examples()

    violations: list[str] = []
    if not _wl534_ready(wl534):
        violations.append("wl534_input_not_ready")
    if not all(check["verified"] is True for check in identity_checks):
        violations.append("q_root_coordinate_identity_check_failed")
    if inverse_analysis["all_q_values_covered"] is not True:
        violations.append("q_root_coordinate_inverse_not_recorded")

    status = "ok" if not violations else "issues"
    ready = status == "ok"
    proof_status = (
        {
            "wl534_reduced_to_q_root_coordinate_exact_obstruction_here": True,
            "representation_choice_and_chart_removed_from_statement_here": True,
            "remaining_problem_is_direct_q_root_square_quartic_obstruction": True,
            "uniform_infinite_subfamily_exclusion_proved_here": False,
            "strict_counterexample_found_here": False,
            "advance_to_m3": False,
            "stop_after_coordinate_free_exact_reformulation": True,
        }
        if ready
        else {}
    )

    return {
        "status": status,
        "ready": ready,
        "work_log": "wl535",
        "object_layer": "m2_q_root_coordinate_square_quartic_obstruction_after_wl534",
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
                "q is rational",
                "ell-q^2 is a rational square",
                "ell*q^2+4 is a rational square",
                "ell*q^4+4*q^2-4*ell is positive",
                (
                    "V^2 = q^8 + (16-8*ell)q^6 + (32*ell^2-96*ell+72)q^4 "
                    "+ (32*ell-64)q^2 + 16"
                ),
            ],
            "touches_only_M2_for_the_wl534_pure_family": True,
        },
        "input_checkpoint": {
            "work_log": "wl534",
            "ready": _wl534_ready(wl534),
            "handoff": "wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction_stop",
        },
        "q_root_coordinate_reduction": {
            "classical_input": "Fermat_two_squares_for_primes_1_mod_4",
            "definitions": {
                "q(u)": "N(u) / D(u)",
                "p(u)": "P(u) / D(u)",
                "D(u)": "1 + u^2",
                "N(u)": "b*(1-u^2) + 2*a*u",
                "P(u)": "a*(1-u^2) - 2*b*u",
                "G_ell(Q)": (
                    "Q^4 + (16-8*ell)Q^3 + (32*ell^2-96*ell+72)Q^2 "
                    "+ (32*ell-64)Q + 16"
                ),
                "V_definition": "V^2 = G_ell(q^2)",
            },
            "identity_checks": identity_checks,
            "inverse_and_branch_analysis": inverse_analysis,
        },
        "exact_coordinate_free_reformulation": {
            "handoff_name": "wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction_stop",
            "statement": (
                "For every odd prime ell congruent to 1 mod 4, there is no rational pair "
                "(q,V) such that ell-q^2 is a rational square, ell*q^2+4 is a rational "
                "square, ell*q^4+4*q^2-4*ell > 0, and "
                "V^2 = q^8 + (16-8*ell)q^6 + (32*ell^2-96*ell+72)q^4 "
                "+ (32*ell-64)q^2 + 16."
            ),
            "why_equivalent_to_wl534": [
                (
                    "From wl534, q(u)=N(u)/D(u) and p(u)=P(u)/D(u) satisfy "
                    "q(u)^2+p(u)^2=ell, so ell-q(u)^2 is automatically a rational square."
                ),
                (
                    "The square predicate S(u) descends exactly because "
                    "S(u)=D(u)^2*(ell*q(u)^2+4)."
                ),
                (
                    "The positivity predicate descends exactly because "
                    "R(u)=D(u)^4*(ell*q(u)^4+4*q(u)^2-4*ell)."
                ),
                (
                    "The last square predicate descends exactly because "
                    "T(u)=D(u)^8*G_ell(q(u)^2), so T(u) is a rational square exactly "
                    "when G_ell(q(u)^2) is one."
                ),
                (
                    "Conversely, any rational q with ell-q^2 square gives a rational "
                    "point (p,q) on p^2+q^2=ell; the two visible inverse-denominator "
                    "branches (-a,b) and (a,-b) are removable by the alternate quotient, "
                    "and the antipode is recovered by switching the sign of p before "
                    "applying the wl533 inverse formulas, "
                    "and the descended identities lift the q-coordinate conditions back "
                    "to the exact wl534 predicates."
                ),
            ],
            "coordinate_free_exact_reformulation_reason": (
                "This rewrites wl534 without keeping the representation choice "
                "a^2+b^2=ell or the affine chart data inside the final proposition, "
                "replaces the last square predicate by one explicit q-coordinate "
                "quartic curve equation, and leaves the same exact arithmetic content "
                "in direct q-root-coordinate form."
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
            "results/closure_quotient_rank_zero_aa_bb_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction.json"
        ),
        help="Output path for the wl535 q-root-coordinate square/quartic audit JSON.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_wl535_m2_pure_v_ell_q_root_coordinate_square_quartic_obstruction()
    write_json(args.out, payload)
    print(f"wrote wl535 q-root-coordinate square/quartic audit to {args.out}")
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
