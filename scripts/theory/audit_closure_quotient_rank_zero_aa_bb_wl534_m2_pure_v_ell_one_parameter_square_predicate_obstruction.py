#!/usr/bin/env python3
"""Shrink wl533 to a one-parameter square-predicate obstruction."""

from __future__ import annotations

import argparse
import importlib
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl533_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl533_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction"
    )
    from json_io import write_json


BOUNDARY = (
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


def _wl533_ready(wl533: dict[str, Any]) -> bool:
    proof = wl533.get("proof_status", {})
    return (
        wl533.get("status") == "ok"
        and wl533.get("ready") is True
        and wl533.get("work_log") == "wl533"
        and wl533.get("object_layer")
        == "m2_one_parameter_conic_quartic_obstruction_after_wl532"
        and proof.get("wl532_reduced_to_one_parameter_exact_obstruction_here") is True
        and proof.get("q_and_ell_minus_q_square_conditions_absorbed_here") is True
        and proof.get("remaining_ell_q_plus_4_and_v_obstructions_recorded_here") is True
        and proof.get("uniform_infinite_subfamily_exclusion_proved_here") is False
        and proof.get("strict_counterexample_found_here") is False
        and wl533.get("advance_to_m3") is False
    )


def _identity_checks() -> list[dict[str, Any]]:
    ell, a, b, u = sp.symbols("ell a b u", nonzero=True)
    D = 1 + u**2
    N = b * (1 - u**2) + 2 * a * u
    P = a * (1 - u**2) - 2 * b * u
    S = ell * N**2 + 4 * D**2
    A = -N**4 + (8 * ell - 12) * N**2 * D**2 + 4 * D**4
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


def _zero_branch_analysis() -> dict[str, Any]:
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


def _boundary_examples() -> dict[str, Any]:
    def values(ell: int, a: int, b: int, u: Fraction) -> dict[str, str | int | bool]:
        D = Fraction(1, 1) + u**2
        N = b * (1 - u**2) + 2 * a * u
        A = -N**4 + (8 * ell - 12) * N**2 * D**2 + 4 * D**4
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
            "S(u)_is_rational_square": _is_rational_square(S),
            "R(u)": str(R),
            "R(u)_is_positive": R > 0,
            "T(u)": str(T),
            "T(u)_is_rational_square": _is_rational_square(T),
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


def _is_rational_square(value: Fraction) -> bool:
    if value < 0:
        return False
    return (
        isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def build_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction() -> dict[str, Any]:
    wl533 = wl533_module.build_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction()
    identity_checks = _identity_checks()
    zero_branch_analysis = _zero_branch_analysis()
    examples = _boundary_examples()

    violations: list[str] = []
    if not _wl533_ready(wl533):
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
            "ready": _wl533_ready(wl533),
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
            "results/closure_quotient_rank_zero_aa_bb_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction.json"
        ),
        help="Output path for the wl534 one-parameter square-predicate audit JSON.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_wl534_m2_pure_v_ell_one_parameter_square_predicate_obstruction()
    write_json(args.out, payload)
    print(f"wrote wl534 one-parameter square-predicate audit to {args.out}")
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
