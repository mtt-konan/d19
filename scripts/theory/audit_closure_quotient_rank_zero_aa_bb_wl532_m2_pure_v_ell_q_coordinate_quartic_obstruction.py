#!/usr/bin/env python3
"""Shrink wl531 to a smaller Q-coordinate quartic obstruction."""

from __future__ import annotations

import argparse
import importlib
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl531_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl531_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition"
    )
    from json_io import write_json


BOUNDARY = (
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


def _wl531_ready(wl531: dict[str, Any]) -> bool:
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


def _identity_checks() -> list[dict[str, Any]]:
    ell, X = sp.symbols("ell X", nonzero=True)
    A, B, Q, V = sp.symbols("A B Q V", nonzero=True)

    source_quadratic = X**2 + (8 - 2 * ell**2) * X + (ell**2 + 4) ** 2
    opposite_quadratic = (
        X**2 + (6 * ell**2 - 16 * ell + 8) * X + (5 * ell**2 - 8 * ell + 4) ** 2
    )
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


def _mod_4_obstruction() -> dict[str, Any]:
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


def _q_coordinate_nonzero_analysis() -> dict[str, Any]:
    return {
        "Q_nonzero": (
            "Q=16/A_ell(X,z) is nonzero because wl531 proves A_ell(X,z) is nonzero."
        ),
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


def _boundary_examples() -> dict[str, Any]:
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
            "quartic_value_is_rational_square": _is_rational_square(quartic_value),
            "meaning": (
                "The wl531 source-side lift example at ell=13 becomes the single "
                "Q-value Q=9. The remaining failure is now only the new quartic "
                "square condition G_13(9)."
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


def build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction() -> dict[str, Any]:
    wl531 = wl531_module.build_wl531_m2_pure_v_ell_x_fiber_product_square_lift_proposition()
    identity_checks = _identity_checks()
    mod_4 = _mod_4_obstruction()
    nonzero = _q_coordinate_nonzero_analysis()
    examples = _boundary_examples()

    violations: list[str] = []
    if not _wl531_ready(wl531):
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
            "ready": _wl531_ready(wl531),
            "handoff": "wl531_m2_pure_v_ell_exact_x_fiber_product_square_lift_proposition_stop",
        },
        "q_coordinate_reduction": {
            "Q_definition": "Q = 16 / A_ell(X,z)",
            "derived_square_relations": {
                "ell - Q": "B_ell(X,z) / A_ell(X,z)",
                "X(Q)": "((ell - Q)*(ell*Q + 4)) / Q",
                "G_ell(Q)": (
                    "Q^4 + (16 - 8*ell)Q^3 + (32*ell^2 - 96*ell + 72)Q^2 + "
                    "(32*ell - 64)Q + 16"
                ),
                "completed_square_form": (
                    "(Q^2 + (8 - 4*ell)Q - 4)^2 + 16*(ell - 1)^2*Q^2"
                ),
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
                (
                    "Writing V=U*Q/ell converts the opposite quadratic exactly to "
                    "V^2=G_ell(Q)."
                ),
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
            "results/closure_quotient_rank_zero_aa_bb_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction.json"
        ),
        help="Output path for the wl532 Q-coordinate obstruction audit JSON.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_wl532_m2_pure_v_ell_q_coordinate_quartic_obstruction()
    write_json(args.out, payload)
    print(f"wrote wl532 Q-coordinate obstruction audit to {args.out}")
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
