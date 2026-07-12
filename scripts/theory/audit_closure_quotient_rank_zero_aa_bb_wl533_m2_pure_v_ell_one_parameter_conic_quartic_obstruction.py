#!/usr/bin/env python3
"""Shrink wl532 to a one-parameter conic-quartic obstruction."""

from __future__ import annotations

import argparse
import importlib
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl532_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl532_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction"
    )
    from json_io import write_json


BOUNDARY = (
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


def _wl532_ready(wl532: dict[str, Any]) -> bool:
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


def _identity_checks() -> list[dict[str, Any]]:
    ell, a, b, u = sp.symbols("ell a b u", nonzero=True)
    q = sp.symbols("q", nonzero=True)
    D = 1 + u**2
    N = b * (1 - u**2) + 2 * a * u
    P = a * (1 - u**2) - 2 * b * u
    q_u = N / D
    p_u = P / D
    q_quartic = ell * N**2 + 4 * D**2
    a_q = -q**4 + (8 * ell - 12) * q**2 + 4
    b_q = q**4 + 4 * q**2 - 4
    a_u = -N**4 + (8 * ell - 12) * N**2 * D**2 + 4 * D**4
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
            (
                ((ell - Q_u) * (ell * Q_u + 4)) / Q_u
                - (P**2 * q_quartic) / (N**2 * D**2)
            ),
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


def _inverse_and_branch_analysis() -> dict[str, Any]:
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


def _boundary_examples() -> dict[str, Any]:
    ell = 13
    a = 2
    b = 3
    u = Fraction(0, 1)
    D = Fraction(1, 1) + u**2
    N = b * (1 - u**2) + 2 * a * u
    P = a * (1 - u**2) - 2 * b * u
    q_square = Fraction(N**2, D**2)
    x_value = Fraction(P**2 * (ell * N**2 + 4 * D**2), N**2 * D**2)
    a_u = -N**4 + (8 * ell - 12) * N**2 * D**2 + 4 * D**4
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
            "g_value_is_rational_square": _is_rational_square(g_value),
            "meaning": (
                "At ell=13 with a^2+b^2=13 given by 2^2+3^2, the new parameter u=0 "
                "recovers the old Q=9 boundary point exactly. The remaining failure is "
                "now only the denominator-cleared two-square V-condition."
            ),
        },
    }


def _is_rational_square(value: Fraction) -> bool:
    if value < 0:
        return False
    return (
        isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def build_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction() -> dict[str, Any]:
    wl532 = wl532_module.build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction()
    identity_checks = _identity_checks()
    inverse_analysis = _inverse_and_branch_analysis()
    examples = _boundary_examples()

    violations: list[str] = []
    if not _wl532_ready(wl532):
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
            "ready": _wl532_ready(wl532),
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
            "results/closure_quotient_rank_zero_aa_bb_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction.json"
        ),
        help="Output path for the wl533 one-parameter obstruction audit JSON.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_wl533_m2_pure_v_ell_one_parameter_conic_quartic_obstruction()
    write_json(args.out, payload)
    print(f"wrote wl533 one-parameter obstruction audit to {args.out}")
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
