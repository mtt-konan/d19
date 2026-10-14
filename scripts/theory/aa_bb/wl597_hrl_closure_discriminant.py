#!/usr/bin/env python3
"""Derive the symmetric closure-discriminant gate for the wl596 blocker.

This is an exact algebraic projection, not an exclusion theorem.  For source
values ``U_i`` and divisor coordinates ``q_i`` it eliminates ``U_1,U_2`` and
the individual ordering of ``q_1,q_2`` from a necessary closure condition.
The resulting square condition is useful only together with the original
source-square, divisor, positivity, and root-discriminant conditions.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

S, R, z, E, T = sp.symbols("S R z E T", nonzero=True)
D = S * R


def closure_quadratic(target: sp.Expr) -> sp.Expr:
    """Return the cleared quadratic in E=q1^2+q2^2."""
    q1, q2 = sp.symbols("q1 q2", nonzero=True)
    e1 = q1**2 + D**2 / q1**2 - (S**2 + R**2)
    e2 = q2**2 + D**2 / q2**2 - (S**2 + R**2)
    raw = (4 * target**2 - e1 - e2) ** 2 - 4 * e1 * e2
    x, y = sp.symbols("x y", nonzero=True)
    numerator = sp.together(raw.subs({q1**2: x, q2**2: y})).as_numer_denom()[0]
    symmetric = sp.symmetrize(numerator, [x, y], formal=True)[0]
    # symmetrize uses generated names s1,s2; substitute E and z^2.
    s1, s2 = sorted(
        [symbol for symbol in symmetric.free_symbols if str(symbol).startswith("s")],
        key=str,
    )
    return sp.factor(symmetric.subs({s1: E, s2: z**2}))


def expected_quadratic(target: sp.Expr) -> sp.Expr:
    """Closed form of the symmetric quadratic, with z=q1*q2."""
    # This form is the numerator after clearing q1^4*q2^4.
    return sp.factor(
        (z**2 - D**2) ** 2 * E**2
        - 8 * target**2 * z**2 * (z**2 + D**2) * E
        - 4 * z**2 * (D**4 - 6 * D**2 * z**2 - 8 * target**4 * z**2 + z**4)
    )


def discriminant_factors(target: sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    f0 = z**4 - 6 * D**2 * z**2 + D**4
    ft = z**4 - 2 * D**2 * z**2 - 4 * target**4 * z**2 + D**4
    return f0, ft, sp.factor(16 * z**2 * f0 * ft)


def dyadic_branch_reduction() -> dict[str, Any]:
    """Record the parity lemma that removes one parameter class and T branch."""
    return {
        "opposite_parity": {
            "condition": "Abar,Bbar have opposite parity",
            "conclusion": "s,r,q_i,d_i are odd and 4 divides every finite U_i",
            "reason": (
                "a_i,b_i have opposite parity; the leg paired with an odd base "
                "must be odd, and an odd-square difference is 0 or 8 mod 16, "
                "while a square cannot be 8 mod 16"
            ),
            "closure": "all six finite T=s/r branches are impossible because 4 divides U1 +/- U2",
        },
        "both_odd": {
            "condition": "Abar,Bbar are both odd",
            "conclusion": "q_i,d_i are even, a_i,b_i are odd, and 4 divides every finite U_i",
            "surviving_branch": "the physical T branch with 4 dividing T",
            "allocation": (
                "v2(q_i) is in {1, v2(Delta)-1}; intermediate dyadic allocations "
                "are excluded"
            ),
        },
        "scope": "This is a branch reduction, not a determination of the odd squareclass of q1*q2.",
    }


def build_certificate() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    for target in (S, R):
        checks[f"quadratic_identity_{target}"] = sp.factor(
            closure_quadratic(target) - expected_quadratic(target)
        ) == 0
        a = (z**2 - D**2) ** 2
        b = -8 * target**2 * z**2 * (z**2 + D**2)
        c = -4 * z**2 * (D**4 - 6 * D**2 * z**2 - 8 * target**4 * z**2 + z**4)
        disc = sp.factor(b**2 - 4 * a * c)
        checks[f"discriminant_factorization_{target}"] = disc == discriminant_factors(target)[2]

    return {
        "status": "ok" if all(checks.values()) else "invalid",
        "ready": all(checks.values()),
        "task": "universal-four-factor-hrl-closure-discriminant",
        "accepted_input": "wl596_precise_smaller_arithmetic_blocker",
        "accepted_outcome": "precise_smaller_arithmetic_proposition",
        "notation": {
            "S": "Abar+Bbar",
            "R": "Abar-Bbar>0",
            "Delta": "S*R",
            "z": "q1*q2",
            "E": "q1^2+q2^2",
            "e_i": "4*U_i^2=q_i^2+Delta^2/q_i^2-S^2-R^2",
        },
        "quadratic": {
            "sum_target": sp.sstr(expected_quadratic(S)),
            "difference_target": sp.sstr(expected_quadratic(R)),
            "interpretation": (
                "The equation is (4*T^2-e1-e2)^2=4*e1*e2 after substituting "
                "q1*q2=z and q1^2+q2^2=E. With e_i=4*U_i^2, the sign "
                "condition selects a member of the closure union."
            ),
        },
        "discriminant": {
            "common_factor": sp.sstr(discriminant_factors(S)[0]),
            "sum_factor": sp.sstr(discriminant_factors(S)[1]),
            "difference_factor": sp.sstr(discriminant_factors(R)[1]),
            "necessary_square": (
                "For either T=S or T=R, every strict point has "
                "F0(z)*FT(z) a rational square; since it is integral, an "
                "integer square. On the exact wl596 domain this is not an "
                "independent local obstruction because the individual source "
                "squares already make the product square."
            ),
        },
        "dyadic_branch_reduction": dyadic_branch_reduction(),
        "removed_freedoms": [
            "the two source radicals U_1,U_2",
            "the ordering variable q1^2-q2^2 from the square condition itself",
        ],
        "retained_conditions": [
            "q_i positive divisors of Delta with q_i congruent Delta/q_i mod 2",
            "q_i>=S and both source values F(q_i) are nonnegative integer squares",
            "E^2-4*z^2=(q1^2-q2^2)^2 is a square",
            "the sign inequality selecting sum or ordered-difference closure",
            "all midpoint, endpoint, factor-zero, infinity, p=2, and AA/BB lift boundaries",
        ],
        "proof_boundary": {
            "uniform_exclusion": False,
            "source_square_conditions_eliminated": False,
            "divisor_pair_classified": False,
            "selmer_rank_or_family_claim": False,
        },
        "verification": {"checks": checks, "violations": [k for k, v in checks.items() if not v]},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_certificate()
    if args.strict:
        print(f"status={payload['status']}")
        print(f"task={payload['task']}")
        print(f"ready={payload['ready']}")
        print(f"accepted_outcome={payload['accepted_outcome']}")
        print(f"violations={payload['verification']['violations']}")
    return 0 if payload["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
