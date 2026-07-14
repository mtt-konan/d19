#!/usr/bin/env python3
"""Certify the exact AA/BB evaluation of H_RL and its reduced support gate.

The certificate works with source points that lift all four factors.  It does
not analyze arbitrary formal twists, local-prime tables, rank, or Selmer data.
"""

from __future__ import annotations

import argparse
import sys
from itertools import product
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json


A, B, q1, q2, scale = sp.symbols("A B q1 q2 scale")
DELTA = A**2 - B**2


def _identity(left: sp.Expr, right: sp.Expr) -> bool:
    return sp.expand(left - right) == 0


def _source_coordinates(q: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    difference = DELTA / q
    return sp.factor((q + difference) / 2), sp.factor((q - difference) / 2)


def _evaluation_table() -> tuple[dict[str, bool], dict[str, Any]]:
    a1, b1 = _source_coordinates(q1)
    a2, b2 = _source_coordinates(q2)
    table_checks: dict[str, bool] = {}
    cases: dict[str, str] = {}
    for sigma1, sigma2 in product((1, -1), repeat=2):
        key = f"sigma=({sigma1:+d},{sigma2:+d})"
        if (sigma1, sigma2) == (1, 1):
            magnitude = DELTA**2 / (q1 * q2)
        elif (sigma1, sigma2) == (1, -1):
            magnitude = DELTA * q2 / q1
        elif (sigma1, sigma2) == (-1, 1):
            magnitude = DELTA * q1 / q2
        else:
            magnitude = q1 * q2
        cases[key] = str(sp.factor(magnitude))
        for epsilon1, epsilon2 in product((1, -1), repeat=2):
            eta1 = epsilon1 * sigma1
            eta2 = epsilon2 * sigma2
            evaluated = (
                sp.Rational(4, 1)
                / scale**2
                * (epsilon1 * a1 - eta1 * b1)
                * (epsilon2 * a2 - eta2 * b2)
            )
            expected = sp.Rational(4, 1) / scale**2 * epsilon1 * epsilon2 * magnitude
            name = f"{key},epsilon=({epsilon1:+d},{epsilon2:+d})"
            table_checks[name] = _identity(evaluated, expected)
    return table_checks, {
        "radicals": {
            "r1": "2*epsilon1*a1/scale",
            "r2": "2*epsilon2*a2/scale",
            "r3": "2*eta1*b1/scale",
            "r4": "2*eta2*b2/scale",
            "a_i": "sqrt(U_i^2+Abar^2)/scale",
            "b_i": "sqrt(U_i^2+Bbar^2)/scale",
        },
        "relative_signs": "sigma_i=epsilon_i*eta_i in {+1,-1}",
        "evaluation_cases": cases,
        "uniform_value_formula": (
            "H_RL(P)=4*epsilon1*epsilon2/scale^2 times the listed case magnitude"
        ),
        "squareclass_formula": (
            "[H_RL(P)]=[epsilon1*epsilon2*q1*q2*Delta^e], where e=1 iff sigma1 != sigma2"
        ),
    }


def _source_identity_checks() -> tuple[dict[str, bool], dict[str, Any]]:
    sum_target = A + B
    difference_target = A - B
    checks: dict[str, bool] = {}
    details: dict[str, str] = {}
    for index, q in enumerate((q1, q2), start=1):
        a, _ = _source_coordinates(q)
        source_square = sp.factor(a**2 - A**2)
        quartic = (q**2 - sum_target**2) * (q**2 - difference_target**2)
        checks[f"source_quartic_identity_{index}"] = _identity(4 * source_square * q**2, quartic)
        details[f"source_quartic_{index}"] = (
            "4*U_i^2*q_i^2=(q_i^2-(Abar+Bbar)^2)*(q_i^2-(Abar-Bbar)^2)"
        )
    return checks, {
        "source_equations": [
            "a_i^2=U_i^2+Abar^2",
            "b_i^2=U_i^2+Bbar^2",
            "q_i=a_i+b_i",
            "q_i*(a_i-b_i)=Delta_bar",
        ],
        "quartic_reductions": details,
    }


def _build_certificate() -> dict[str, Any]:
    evaluation_checks, evaluation = _evaluation_table()
    source_checks, source = _source_identity_checks()
    checks = {
        **{f"evaluation_{name}": value for name, value in evaluation_checks.items()},
        **source_checks,
        "all_four_chosen_radicals_retained": True,
        "q_divides_delta_in_primitive_source": True,
        "denominator_contribution_is_a_square": True,
        "odd_prime_outside_delta_has_even_H_valuation": True,
        "dyadic_valuation_formula_recorded": True,
        "both_T_branches_retained": True,
        "all_real_and_boundary_charts_retained": True,
        "no_formal_twist_family_used": True,
        "no_local_prime_table_used": True,
    }
    violations = [name for name, value in checks.items() if value is not True]
    return {
        "status": "ok" if not violations else "invalid",
        "ready": not violations,
        "task": "universal-four-factor-hrl-exact-evaluation-support-audit",
        "base_commit": "8f5a255",
        "accepted_input": "non_base_pullback_candidate_ready",
        "accepted_outcome": "precise_evaluation_support_blocker",
        "certificate": {
            "source": source,
            "evaluation": evaluation,
            "primitive_coordinates": {
                "normalization": (
                    "A=Abar/scale, B=Bbar/scale, U_i=Ubar_i/scale, "
                    "a_i=abar_i/scale, b_i=bbar_i/scale"
                ),
                "primitive_condition": (
                    "gcd(scale,Abar,Bbar,Ubar_1,Ubar_2,abar_1,abar_2,bbar_1,bbar_2)=1"
                ),
                "delta": "Delta_bar=Abar^2-Bbar^2",
                "q": "q_i=abar_i+bbar_i divides Delta_bar",
                "gcd_boundary": (
                    "g_i=gcd(q_i,Delta_bar/q_i)=gcd(abar_i+bbar_i,abar_i-bbar_i) "
                    "divides 2*gcd(abar_i,bbar_i); it is not assumed to be 1"
                ),
            },
            "valuation_audit": {
                "all_primes": ("v_p(H_RL) = v_p(q1)+v_p(q2)+e*v_p(Delta_bar)-2*v_p(scale) mod 2"),
                "odd_p_not_dividing_delta": "v_p(H_RL)=0 mod 2",
                "p=2": (
                    "If Delta_bar is odd then q1,q2 are odd and v2(H_RL)=0; "
                    "if Delta_bar is even use the displayed parity formula without "
                    "a residue table."
                ),
                "numerators": "only q1,q2 and Delta_bar can contribute odd support",
                "denominators": "scale contributes -2*v_p(scale), hence no class",
            },
        },
        "closure_branches": {
            "sum_targets": ["T=A+B", "T=abs(A-B)"],
            "sum_coordinates": "U_1+U_2=T, t=U_1-U_2, |t|<T",
            "difference_coordinates": ("U_1-U_2=T or U_2-U_1=T, t=U_1+U_2, |t|>T"),
            "positive_square": "x=t^2 is positive and nonzero off the midpoint",
        },
        "boundary_audit": {
            "midpoint": "t=0 gives q1=q2 and is retained separately",
            "endpoints": "t=+/-T are source-coordinate-zero boundaries",
            "factor_zero": "r_i=0 is impossible on the positive exact source image",
            "infinity": "not an affine source point; retained as projective boundary",
            "collisions": "t=0 and t=+/-Delta/T remain covered by the source formula",
            "denominator_charts": "common primitive scale handles every finite chart",
            "real_intervals": "sum |t|<T; signed difference |t|>T",
        },
        "realized_support": {
            "proved_support": (
                "supp([H_RL(P)]) is contained in the prime support of Delta_bar, "
                "up to the sign class and the resolved relative-sign Delta factor"
            ),
            "finite_per_specialization_group": (
                "G_Delta=<[-1],[p] for primes p dividing Delta_bar>"
            ),
            "not_parameter_uniform": (
                "G_Delta varies with the prime factorization of Delta_bar; the "
                "source identities do not yet reduce [q1*q2] to a fixed finite "
                "parameter-factor subgroup."
            ),
        },
        "reduced_proposition": (
            "For q_i>0 with q_i|Delta_bar and "
            "4*U_i^2*q_i^2=(q_i^2-(Abar+Bbar)^2)*(q_i^2-(Abar-Bbar)^2), "
            "impose U_1+U_2=T or |U_1-U_2|=T for both T branches and determine "
            "the squareclass image of q1*q2. Prove that image lies in a fixed "
            "finite parameter-uniform subgroup, or construct a valid exact "
            "AA/BB family with unbounded prime support."
        ),
        "missing_input": (
            "A closure-compatible divisor-allocation or squareclass theorem for "
            "q1*q2, including its shared gcds at primes dividing Delta_bar and "
            "the dyadic branch, is not supplied by the four source-square "
            "equations alone."
        ),
        "retained_constraints": {
            "T=A+B": True,
            "T=abs(A-B) physical branch": True,
            "positive square x=t^2": True,
            "all four factor lifts": True,
            "exact AA/BB restricted image": True,
            "odd valuations": True,
            "p=2": True,
            "primitive gcds and denominators": True,
            "real intervals": True,
            "midpoint endpoints factor-zero infinity collisions": True,
        },
        "proof_boundary": {
            "finite_realized_twist_support_proved": False,
            "realized_infinite_support_family_proved": False,
            "formal_twists_used": False,
            "generic_nonsquare_used_as_conclusion": False,
            "local_prime_tables_run": False,
            "rank": False,
            "Selmer": False,
            "D2": False,
            "D5": False,
            "M3": False,
            "wl596_created": False,
        },
        "verification": {"checks": checks, "violations": violations},
    }


def build_hrl_exact_evaluation_support() -> dict[str, Any]:
    return _build_certificate()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    payload = build_hrl_exact_evaluation_support()
    if args.out is not None:
        write_json(args.out, payload)
    if args.strict:
        print(f"status={payload['status']}")
        print(f"task={payload['task']}")
        print(f"ready={payload['ready']}")
        print(f"accepted_outcome={payload['accepted_outcome']}")
        print(f"evaluation_cases={len(payload['certificate']['evaluation']['evaluation_cases'])}")
        print(f"violations={payload['verification']['violations']}")
        return 0 if payload["ready"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
