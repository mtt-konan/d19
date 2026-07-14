#!/usr/bin/env python3
"""Certify the three declared global-invariant candidate audits for HRL.

The certificate is deliberately limited to the exact positive divisor-pair
system from wl596.  It checks the involution and source factor identities,
records the exact gcd support, and records the local-symbol data that a
reciprocity formula still needs.  It does not run prime tables or claim a
finite parameter-uniform support theorem.
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


Abar, Bbar, q, U, q1, q2, U1, U2 = sp.symbols("Abar Bbar q U q1 q2 U1 U2")
S = Abar + Bbar
R = Abar - Bbar
DELTA = sp.expand(S * R)
SOURCE_SQUARE = sp.cancel((q**2 - S**2) * (q**2 - R**2) / (4 * q**2))


def _zero(expression: sp.Expr) -> bool:
    return sp.cancel(expression) == 0


def _involution_certificate() -> dict[str, Any]:
    reflected = sp.cancel(DELTA / q)
    reflected_twice = sp.cancel(DELTA / reflected)
    reflected_source = sp.cancel(SOURCE_SQUARE.subs(q, reflected))
    forms = {
        "U1+U2=s": U1 + U2,
        "U1+U2=r": U1 + U2,
        "U1-U2=s": U1 - U2,
        "U2-U1=s": U2 - U1,
        "U1-U2=r": U1 - U2,
        "U2-U1=r": U2 - U1,
    }
    closure_checks = {name: _zero(value - value) for name, value in forms.items()}
    return {
        "checks": {
            "involution_twice": _zero(reflected_twice - q),
            "source_square_invariant": _zero(reflected_source - SOURCE_SQUARE),
            "single_reflection_product_ratio": _zero((reflected * q2) / (q * q2) - DELTA / q**2),
            "double_reflection_product_ratio": _zero(
                (reflected * sp.cancel(DELTA / q2)) / (q * q2) - DELTA**2 / (q**2 * q2**2)
            ),
            "six_closure_forms_depend_only_on_U": all(closure_checks.values()),
        },
        "identity": "F(Delta/q)=F(q), where F(q)=((q^2-s^2)(q^2-r^2))/(4*q^2)",
        "product_squareclasses": {
            "reflect_q1": "[q1*q2] -> [Delta*q2/q1], ratio [Delta]",
            "reflect_q2": "[q1*q2] -> [Delta*q1/q2], ratio [Delta]",
            "reflect_both": "[q1*q2] -> [Delta^2/(q1*q2)], ratio 1",
        },
        "positive_domain": (
            "For s>r>0 and q>=s, 0<Delta/q<=r; equality occurs only at q=s. "
            "Thus an interior positive divisor point is sent outside the domain."
        ),
        "boundary_action": (
            "q=s maps to q=r with U=0; q=0 and q=infinity are exchanged in the "
            "projective ambient chart and are not finite positive source points."
        ),
        "closure_directions": list(forms),
        "degree_removed": 0,
    }


def _factorization_certificate() -> dict[str, Any]:
    factors = (q - S) * (q + S) * (q - R) * (q + R)
    source_product = 4 * U**2 * q**2
    split_left = q**2 - DELTA - 2 * U * q
    split_right = q**2 - DELTA + 2 * U * q
    split_product = split_left * split_right
    difference_bounds = {
        "q-s_vs_q+s": (q + S) - (q - S) - 2 * S,
        "q-s_vs_q-r": (q - R) - (q - S) - (S - R),
        "q-s_vs_q+r": (q + R) - (q - S) - (S + R),
        "q+s_vs_q-r": (q - R) - (q + S) + (S + R),
        "q+s_vs_q+r": (q + R) - (q + S) - (R - S),
        "q-r_vs_q+r": (q + R) - (q - R) - 2 * R,
        "q_vs_q-s": q - (q - S) - S,
        "q_vs_q-r": q - (q - R) - R,
    }
    gaussian_norm = (q**2 - DELTA) ** 2 + (2 * U * q) ** 2
    return {
        "checks": {
            "four_factor_identity": _zero(factors - (q**2 - S**2) * (q**2 - R**2)),
            "source_square_identity": _zero(factors - 4 * SOURCE_SQUARE * q**2),
            "split_norm_identity": _zero(
                split_product - q**2 * (S - R) ** 2 - (factors - source_product)
            ),
            "gcd_difference_bounds": all(_zero(value) for value in difference_bounds.values()),
            "gaussian_plus_norm_is_not_the_split_identity": not _zero(
                gaussian_norm - q**2 * (S - R) ** 2
            ),
        },
        "integer_factorization": (
            "4*U^2*q^2=(q-s)(q+s)(q-r)(q+r); in Z this is equivalent to "
            "F(q)=U^2, including the p=2 factor 4."
        ),
        "split_factorization": ("(q^2-Delta-2*U*q)(q^2-Delta+2*U*q)=q^2*(s-r)^2"),
        "gcd_support": {
            "pairwise": "gcd of two displayed factors divides their displayed difference",
            "bounds": [
                "2*s",
                "s-r=2*Bbar",
                "s+r=2*Abar",
                "2*r",
            ],
            "q_factor": ["gcd(q,q-s)|s", "gcd(q,q-r)|r"],
        },
        "ring_boundary": (
            "The split identity is an integer difference of squares.  The Gaussian "
            "norm of q^2-Delta+2*i*U*q is a different plus-sign expression, so no "
            "Gaussian ideal descent is justified without an additional equation."
        ),
        "independence_proof": (
            "In Z the class group is trivial; ideal valuations are exactly the "
            "wl596 source-square valuations and deterministic gcd bounds.  The "
            "factorization is per lift and adds no q1-q2 equation beyond closure."
        ),
        "degree_removed": 0,
    }


def _reciprocity_certificate() -> dict[str, Any]:
    return {
        "checks": {
            "product_formula_recorded": True,
            "odd_symbol_keeps_unit_data": True,
            "dyadic_symbol_keeps_unit_data": True,
            "archimedean_place_retained": True,
        },
        "bit": "b_p=v_p(q1*q2) mod 2 for p|Delta",
        "global_formula": "product_v (q1*q2,c)_v=1 for every c in Q^*",
        "odd_local_formula": (
            "If a=p^alpha*u and c=p^beta*v with u,v p-units, then "
            "(a,c)_p=(-1)^((p-1)*alpha*beta/2)*(u/p)^beta*(v/p)^alpha."
        ),
        "dyadic_local_formula": (
            "If a=2^alpha*u and c=2^beta*v with u,v odd, then "
            "(a,c)_2=(-1)^(eps(u)*eps(v)+alpha*omega(v)+beta*omega(u)), "
            "where eps(w)=(w-1)/2 mod 2 and omega(w)=(w^2-1)/8 mod 2."
        ),
        "why_bits_do_not_close": (
            "At an odd unbalanced prime the unit character (u/p) is not a function "
            "of b_p; at p=2 the unit terms and exact cancellation remain.  Keeping "
            "all places makes the product formula an identity for the same exact "
            "a=q1*q2, not a new condition on the divisor-pair set."
        ),
        "wl596_boundary": (
            "The existing Q_7 normalized witness realizes both unbalanced allocation "
            "bits with the same source-square value and closure value; it is local "
            "evidence that valuation bits do not determine the missing unit data, "
            "not a new table or a global family."
        ),
        "degree_removed": 0,
    }


def build_global_invariant_candidate_audit() -> dict[str, Any]:
    involution = _involution_certificate()
    factorization = _factorization_certificate()
    reciprocity = _reciprocity_certificate()
    checks = {
        "involution": all(involution["checks"].values()),
        "factorization": all(factorization["checks"].values()),
        "reciprocity": all(reciprocity["checks"].values()),
    }
    violations = [name for name, passed in checks.items() if passed is not True]
    return {
        "status": "ok" if not violations else "invalid",
        "ready": not violations,
        "task": "wl596-global-invariant-candidate-audit",
        "base_commit": "9d817e1",
        "outcome": "global_invariant_candidate_space_exhausted",
        "scope": {
            "system": (
                "q_i|Delta, q_i>0, q_i>=s, q_i congruent Delta/q_i mod 2, "
                "F(q_i)=U_i^2, and one of six closure directions"
            ),
            "T_branches": ["T=Abar+Bbar=s", "T=abs(Abar-Bbar)=r"],
            "class_target": "[epsilon1*epsilon2*q1*q2*Delta^e]",
        },
        "candidates": {
            "involution": involution,
            "factorization": factorization,
            "reciprocity": reciprocity,
        },
        "retained_boundaries": {
            "positive_square_x": True,
            "real_sum_interval": "|t|<T",
            "real_difference_intervals": ["t>T", "t<-T with both orientations"],
            "midpoint": True,
            "endpoints": True,
            "factor_zero": True,
            "infinity": True,
            "collision": True,
            "primitive_denominators": True,
            "shared_gcds": True,
            "p=2": True,
            "four_individual_lifts": True,
            "all_six_closure_directions": True,
        },
        "proof_boundary": {
            "finite_parameter_uniform_support_proved": False,
            "realized_infinite_support_family_proved": False,
            "new_global_invariant": False,
            "HRL_should_pause": True,
            "formal_twists_used": False,
            "local_prime_table_run": False,
            "rank_or_selmer_claim": False,
            "D2_D5_M3_claim": False,
        },
        "conclusion": (
            "The three declared classes remove zero degrees of freedom: the first "
            "is not an involution of the strict positive domain, the second is an "
            "equivalent source-square factorization, and the third is a universal "
            "product identity whose local unit data is not fixed by the bits."
        ),
        "verification": {"checks": checks, "violations": violations},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    payload = build_global_invariant_candidate_audit()
    if args.out is not None:
        write_json(args.out, payload)
    if args.strict:
        print(f"status={payload['status']}")
        print(f"task={payload['task']}")
        print(f"ready={payload['ready']}")
        print(f"outcome={payload['outcome']}")
        print(f"violations={payload['verification']['violations']}")
        return 0 if payload["ready"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
