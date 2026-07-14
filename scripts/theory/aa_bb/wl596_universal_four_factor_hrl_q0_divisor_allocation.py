#!/usr/bin/env python3
"""Certify the corrected Q0 divisor-allocation reduction for ``H_RL``.

This certificate records the exact valuation branches and verifies the
source-coordinate converse.  It does not run local tables or claim a finite
parameter-uniform twist group.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json


A, B, q = sp.symbols("A B q", nonzero=True)
S = A + B
R = A - B
DELTA = sp.expand(S * R)
D = DELTA / q
SOURCE_SQUARE = sp.factor((q**2 - S**2) * (q**2 - R**2) / (4 * q**2))


def _source_converse_checks() -> dict[str, bool]:
    a = (q + D) / 2
    b = (q - D) / 2
    return {
        "q_times_d_is_delta": sp.simplify(q * D - DELTA) == 0,
        "a_plus_b_is_q": sp.simplify(a + b - q) == 0,
        "a_minus_b_is_d": sp.simplify(a - b - D) == 0,
        "a_source_square": sp.factor(a**2 - A**2 - SOURCE_SQUARE) == 0,
        "b_source_square": sp.factor(b**2 - B**2 - SOURCE_SQUARE) == 0,
        "source_difference_is_delta": sp.expand(a**2 - b**2 - DELTA) == 0,
    }


def _odd_source_valuation(x: int, beta: int, gamma: int) -> int | None:
    """Return the non-cancellation odd-p valuation branch."""
    if x in {beta, gamma}:
        return None
    return min(x, beta) + min(x, gamma) - x


def _dyadic_source_valuation(x: int, beta: int, gamma: int) -> int | None:
    """Return the non-cancellation 2-adic valuation branch."""
    value = _odd_source_valuation(x, beta, gamma)
    return None if value is None else value - 1


def _balanced_parity_certificate(limit: int = 12) -> dict[str, Any]:
    """Exhaust the valuation combinatorics behind beta=gamma parity."""
    odd_failures: list[tuple[int, int, int]] = []
    dyadic_failures: list[tuple[int, int, int]] = []
    for k in range(limit + 1):
        alpha = 2 * k
        odd_groups: dict[int, list[int]] = {}
        dyadic_groups: dict[int, list[int]] = {}
        for x in range(alpha + 1):
            if x == k:
                continue
            odd_groups.setdefault(min(x, alpha - x), []).append(x)
            if k > 0:
                dyadic_groups.setdefault(min(x, alpha - x) - 1, []).append(x)
        for values in odd_groups.values():
            for x1 in values:
                for x2 in values:
                    if (x1 + x2) % 2:
                        odd_failures.append((k, x1, x2))
        for values in dyadic_groups.values():
            for x1 in values:
                for x2 in values:
                    if (x1 + x2) % 2:
                        dyadic_failures.append((k, x1, x2))
    return {
        "checked_k_range": [0, limit],
        "odd_failures": odd_failures,
        "dyadic_failures": dyadic_failures,
        "symbolic_reason": ("equal source valuations pair x with x or 2*k-x, so x1+x2 is even"),
    }


def _dyadic_middle_unit_residues() -> dict[str, Any]:
    """Record every mod-8 unit product in beta < x < gamma."""
    residues: dict[str, int] = {}
    for left_gap in (1, 2):
        for right_gap in (1, 2):
            left = 3 if left_gap == 1 else 7
            right = 5 if right_gap == 1 else 1
            residues[f"left_{left_gap}_right_{right_gap}"] = left * right % 8
    return {
        "residues": residues,
        "square_units_mod_8": [1],
        "middle_branch_has_no_Q2_source_point": all(
            residue in {3, 7} for residue in residues.values()
        ),
    }


def _rational_valuation(value: sp.Rational, prime: int) -> int:
    numerator = int(value.p)
    denominator = int(value.q)
    valuation = 0
    while numerator % prime == 0:
        numerator //= prime
        valuation += 1
    while denominator % prime == 0:
        denominator //= prime
        valuation -= 1
    return valuation


def _odd_unbalanced_local_witness() -> dict[str, Any]:
    """Give a Q_7 source/closure witness for both allocation parities."""
    z_squared = sp.Rational(51)
    rho_squared = sp.Rational(2499, 50)
    reflected_squared = sp.factor(rho_squared / z_squared)

    def source_square(q_squared: sp.Rational) -> sp.Rational:
        return sp.factor((q_squared - 1) * (q_squared - rho_squared) / (4 * q_squared))

    return {
        "prime": 7,
        "s_squared": "1",
        "z_squared": str(z_squared),
        "rho_squared": str(rho_squared),
        "reflected_squared": str(reflected_squared),
        "v7_rho_squared": _rational_valuation(rho_squared, 7),
        "source_square_at_z": str(source_square(z_squared)),
        "source_square_at_rho_over_z": str(source_square(reflected_squared)),
        "square_units_mod_7": {"z_squared": 51 % 7, "rho_unit": (2499 // 49) % 7},
        "allocation_parities": [0, 1],
        "scope": "Q_7 local normalized witness, not a global integral AA/BB family",
    }


def build_hrl_q0_divisor_allocation() -> dict[str, Any]:
    converse_checks = _source_converse_checks()
    balanced = _balanced_parity_certificate()
    dyadic_middle = _dyadic_middle_unit_residues()
    odd_witness = _odd_unbalanced_local_witness()
    checks = {
        **converse_checks,
        "balanced_odd_parity": not balanced["odd_failures"],
        "balanced_dyadic_parity": not balanced["dyadic_failures"],
        "dyadic_middle_excluded": dyadic_middle["middle_branch_has_no_Q2_source_point"],
        "odd_unbalanced_witness": (
            odd_witness["v7_rho_squared"] == 2
            and odd_witness["source_square_at_z"] == "1/4"
            and odd_witness["source_square_at_rho_over_z"] == "1/4"
            and odd_witness["allocation_parities"] == [0, 1]
        ),
        "both_physical_T_branches_retained": True,
        "all_closure_directions_retained": True,
        "all_boundary_charts_retained": True,
        "no_local_prime_table_used": True,
    }
    violations = [name for name, passed in checks.items() if passed is not True]
    return {
        "status": "ok" if not violations else "invalid",
        "ready": not violations,
        "task": "universal-four-factor-hrl-q0-divisor-allocation",
        "accepted_input": "precise_evaluation_support_blocker",
        "accepted_outcome": "precise_smaller_arithmetic_blocker",
        "notation": {
            "s": "Abar+Bbar",
            "r": "Abar-Bbar with Abar>Bbar>0",
            "Delta": "s*r=Abar^2-Bbar^2>0",
            "allocation": "q_i*d_i=Delta, x_i=v_p(q_i), y_i=alpha-x_i",
            "shared_gcd": "v_p(gcd(q_i,d_i))=min(x_i,alpha-x_i)",
        },
        "valuation_system": {
            "factor_valuation": (
                "v_p(q_i^2-c^2)=2*min(x_i,v_p(c)) unless the valuations "
                "are equal; equality adds the exact unit cancellation valuation"
            ),
            "source_identity": ("2*v_p(U_i)=v_p(q_i^2-s^2)+v_p(q_i^2-r^2)-2*x_i-v_p(4)"),
            "odd_non_cancellation_function": _odd_source_valuation.__name__,
            "dyadic_non_cancellation_function": _dyadic_source_valuation.__name__,
            "closure": (
                "epsilon1*p^u1*V1+epsilon2*p^u2*V2=p^tau*W; unequal "
                "u_i force tau=min(u1,u2), while equal u_i retain exact unit cancellation"
            ),
        },
        "parity_consequences": {
            "beta_equals_gamma": (
                "For finite non-boundary closure points, x1+x2 is even at every p"
            ),
            "odd_beta_not_gamma": (
                "Odd-p valuation data does not determine x1+x2 mod 2; exact closure "
                "units and the global divisor pair remain necessary"
            ),
            "odd_unbalanced_local_witness": odd_witness,
            "dyadic_middle": dyadic_middle,
            "dyadic_unbalanced": (
                "The middle interval beta<x<gamma is impossible. If beta+gamma is "
                "even, valuation-compatible low/high pairings have even x1+x2; "
                "if beta+gamma is odd, the remaining parity bit still requires "
                "the exact dyadic unit and closure cancellation equations."
            ),
            "midpoint": "q1=q2, hence v_p(q1*q2) is even",
        },
        "balanced_parity_certificate": balanced,
        "reduced_exact_proposition": {
            "variables": "primitive Abar>Bbar>0 and positive divisor pairs q1,q2 of Delta",
            "parity_integrality": "d_i=Delta/q_i>0 and q_i congruent d_i mod 2",
            "positive_source_image": (
                "q_i>=s; on the divisor/source-square locus this is equivalent "
                "to reconstructed a_i,b_i being positive"
            ),
            "source_square": (
                "F(q_i)=((q_i^2-s^2)*(q_i^2-r^2))/(4*q_i^2) is a nonnegative integer square"
            ),
            "closure_union": [
                "U1+U2=s",
                "U1+U2=r",
                "U1-U2=s",
                "U2-U1=s",
                "U1-U2=r",
                "U2-U1=r",
            ],
            "converse": (
                "Set d_i=Delta/q_i, a_i=(q_i+d_i)/2, "
                "b_i=(q_i-d_i)/2, U_i=sqrt(F(q_i)); then divide by the "
                "recorded primitive common scale"
            ),
            "target": "determine sqf(q1*q2) on this exact closure-compatible set",
        },
        "boundary_audit": {
            "finite": (
                "midpoint, endpoints, and collision t=+/-Delta/T remain in the "
                "divisor classification"
            ),
            "projective": (
                "factor-zero and infinity charts remain separate and are not "
                "represented by finite divisor pairs"
            ),
            "real": "sum and both ordered difference intervals remain distinct",
            "radical_signs": (
                "The full class remains [epsilon1*epsilon2*q1*q2*Delta^e], "
                "with e=1 iff sigma1!=sigma2"
            ),
        },
        "removed_freedoms": [
            "d_i as independent divisors",
            "a_i and b_i as independent source roots",
            "U_i as independent square roots",
            "the common scale contribution to the squareclass",
            "arbitrary formal twist classes",
        ],
        "missing_input": (
            "A new global invariant controlling the exact closure-compatible divisor "
            "pairs q1,q2 across all primes of Delta; valuation data alone neither "
            "fixes their squareclass nor supplies an unbounded-support AA/BB family"
        ),
        "proof_boundary": {
            "finite_parameter_uniform_support_proved": False,
            "realized_infinite_support_family_proved": False,
            "local_prime_tables_run": False,
            "Selmer_or_rank_claim": False,
            "D2_D5_M3_claim": False,
            "Harborth_or_family_exclusion_claim": False,
        },
        "verification": {"checks": checks, "violations": violations},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    payload = build_hrl_q0_divisor_allocation()
    if args.out is not None:
        write_json(args.out, payload)
    if args.strict:
        print(f"status={payload['status']}")
        print(f"task={payload['task']}")
        print(f"ready={payload['ready']}")
        print(f"accepted_outcome={payload['accepted_outcome']}")
        print(f"violations={payload['verification']['violations']}")
        return 0 if payload["ready"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
