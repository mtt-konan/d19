#!/usr/bin/env python3
"""Audit the genus-two character quotient and its Q(i) elliptic quotient."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl580_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl580_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion"
    )
    from json_io import write_json


def _wl580_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl580"
        and proof.get("allocation_descent_exhausted_here") is True
        and payload.get("advance_to_m3") is False
    )


def _reduce_reciprocal_invariant(expr: sp.Expr, x: sp.Symbol, s: sp.Symbol) -> sp.Expr:
    """Reduce a Laurent expression using 1/x=(x-s)/4 and x^2=s*x+4."""
    expanded = sp.expand(expr)
    polynomial = 0
    for term in sp.Add.make_args(expanded):
        exponent = int(term.as_powers_dict().get(x, 0))
        coefficient = term / x**exponent
        replacement = x**exponent if exponent >= 0 else ((x - s) / 4) ** (-exponent)
        polynomial += coefficient * replacement
    return sp.rem(
        sp.Poly(sp.expand(polynomial), x),
        sp.Poly(x**2 - s * x - 4, x),
    ).as_expr()


def _symbolic_certificate() -> dict[str, bool]:
    x, tau, s = sp.symbols("X tau S")
    i = sp.I
    delta = tau**2 + 2 * tau - 1
    a = x * (tau + 2) - 2
    b = 2 * tau - x * (2 * tau - 1)
    c = x + 2 * tau + 4
    d = tau * (x + 4) - 2
    transform = -4 / x
    h = x * a * b * c * d
    transformed = {
        "a": sp.simplify(a.subs(x, transform) + 2 * c / x),
        "b": sp.simplify(b.subs(x, transform) - 2 * d / x),
        "c": sp.simplify(c.subs(x, transform) - 2 * a / x),
        "d": sp.simplify(d.subs(x, transform) + 2 * b / x),
    }
    quotient_rhs = -(
        (s - 4 * i)
        * ((tau + 2) * s + 2 * tau**2 + 8 * tau + 6)
        * ((2 * tau**2 - tau) * s + 6 * tau**2 - 8 * tau + 2)
    )
    invariant_y_square = h * (x - 2 * i) ** 2 / x**4
    reduced_y_square = _reduce_reciprocal_invariant(invariant_y_square, x, s)
    cubic_discriminant = sp.factor(sp.discriminant(quotient_rhs, s))
    expected_discriminant = sp.factor(
        256
        * (tau - i) ** 2
        * (tau + i) ** 2
        * ((1 - 2 * i) * tau + i) ** 4
        * (tau + 2 + i) ** 4
        * delta**2
    )
    return {
        "candidate_product_maps_to_genus_two_curve": sp.simplify(
            (2 * x * delta) ** 2
            * (a * b / (2 * x * delta))
            * (c * d / (2 * delta))
            - h
        )
        == 0,
        "four_linear_factors_pair_under_reciprocal_map": all(
            value == 0 for value in transformed.values()
        ),
        "genus_two_polynomial_transform_ratio": sp.simplify(
            h.subs(x, transform) / h + 64 / x**6
        )
        == 0,
        "quadratic_lift_is_an_involution": sp.simplify(
            (8 * i / transform**3) * (8 * i / x**3) - 1
        )
        == 0,
        "base_quotient_coordinate_is_invariant": sp.simplify(
            transform - 4 / transform - (x - 4 / x)
        )
        == 0,
        "elliptic_y_coordinate_is_invariant": sp.simplify(
            (8 * i / x**3) * (transform - 2 * i) / transform**2
            - (x - 2 * i) / x**2
        )
        == 0,
        "elliptic_quotient_equation": sp.simplify(reduced_y_square - quotient_rhs)
        == 0,
        "elliptic_quotient_cubic_discriminant": sp.simplify(
            cubic_discriminant - expected_discriminant
        )
        == 0,
        "rational_quadratic_lift_discriminant": sp.expand(
            (x - 4 / x) ** 2 + 16 - (x + 4 / x) ** 2
        )
        == 0,
    }


def build_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient(
) -> dict[str, Any]:
    wl580 = wl580_module.build_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl580_ready(wl580):
        violations.append("wl580_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "genus_two_character_quotient_proved_here": True,
            "quadratic_elliptic_quotient_over_q_i_proved_here": True,
            "restricted_affine_candidate_image_proved_here": True,
            "restricted_elliptic_image_locus_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl581",
        "object_layer": "m2_genus_two_character_and_q_i_elliptic_quotient",
        "input_checkpoint": {"work_log": "wl580", "ready": _wl580_ready(wl580)},
        "quotient_certificate": {
            "genus_two_curve": "Z^2=X*a*b*c*d",
            "genus_two_branch_count": 6,
            "base_involution": "X->-4/X",
            "quadratic_lift": "(X,Z)->(-4/X,8*i*Z/X^3)",
            "elliptic_coordinates": ["S=X-4/X", "Y=Z*(X-2*i)/X^2"],
            "candidate_image_restrictions": [
                "tau rational in the exact wl570 interval",
                "S rational and S^2+16 a nonzero rational square",
                "positive quadratic lift X is the original rational square",
                "Y nonzero",
                "ell=L(X,tau) is the original odd prime",
            ],
        },
        "symbolic_certificate": symbolic,
        "proof_status": proof_status,
        "violations": violations,
        "rational_wl535_point_produced_here": False,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "results/closure_quotient_rank_zero_aa_bb_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
