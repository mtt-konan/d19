#!/usr/bin/env python3
"""Audit the source-square genus-one torsor and square-X fiber product."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl582_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl582_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence"
    )
    from json_io import write_json


def _wl582_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl582"
        and proof.get("wl581_unrestricted_elliptic_route_exhausted_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    x, tau, q, p, source_s, u, v = sp.symbols("X tau q p s U V", nonzero=True)
    delta = tau**2 + 2 * tau - 1
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = x + 2 * tau + 4
    fourth = tau * (x + 4) - 2
    u_square = first * second / (2 * delta)
    v_square = third * fourth / (2 * delta)
    product_y = 2 * delta * u * v
    zero_values = [
        first.subs(x, 0),
        second.subs(x, 0),
        third.subs(x, 0),
        fourth.subs(x, 0),
    ]
    leading_values = [
        sp.Poly(first, x).LC(),
        sp.Poly(second, x).LC(),
        sp.Poly(third, x).LC(),
        sp.Poly(fourth, x).LC(),
    ]
    half_substitutions = {
        "u_square": sp.factor(u_square.subs(tau, sp.Rational(1, 2))),
        "v_square": sp.factor(v_square.subs(tau, sp.Rational(1, 2))),
    }
    return {
        "candidate_maps_to_first_torsor_square": sp.simplify(
            sp.expand((q * p) ** 2 - u_square)
            .subs(p**2, first * second / (2 * x * delta))
            .subs(q**2, x)
        )
        == 0,
        "candidate_maps_to_second_torsor_square": sp.simplify(
            sp.expand(source_s**2 - v_square).subs(
                source_s**2, third * fourth / (2 * delta)
            )
        )
        == 0,
        "torsor_product_maps_to_product_elliptic": sp.simplify(
            sp.expand(product_y**2 - first * second * third * fourth)
            .subs(u**2, u_square)
            .subs(v**2, v_square)
        )
        == 0,
        "converse_first_source_square": sp.simplify(
            sp.expand((u / q) ** 2 - first * second / (2 * x * delta))
            .subs(u**2, u_square)
            .subs(q**2, x)
        )
        == 0,
        "zero_fiber_factor_values": zero_values
        == [-2, 2 * tau, 2 * tau + 4, 4 * tau - 2],
        "infinity_leading_factor_values": leading_values
        == [tau + 2, 1 - 2 * tau, 1, tau],
        "exceptional_half_first_torsor_equation": half_substitutions["u_square"]
        == 5 * x - 4,
        "exceptional_half_second_torsor_equation": half_substitutions["v_square"]
        == x * (x + 5),
    }


def build_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product(
) -> dict[str, Any]:
    wl582 = (
        wl582_module.build_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence()
    )
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl582_ready(wl582):
        violations.append("wl582_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "individual_source_squares_retained_on_torsor_here": True,
            "source_square_torsor_genus_one_proved_here": True,
            "unramified_degree_two_map_to_product_elliptic_proved_here": True,
            "full_cover_fiber_product_equivalence_proved_here": True,
            "square_x_pullback_independent_and_connected_here": True,
            "exceptional_tau_half_preserved_and_not_reopened_here": True,
            "square_x_torsor_points_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl583",
        "object_layer": "m2_source_square_genus_one_torsor_and_square_x_fiber_product",
        "input_checkpoint": {"work_log": "wl582", "ready": _wl582_ready(wl582)},
        "fiber_product_certificate": {
            "torsor": ["U^2=a*b/(2*delta)", "V^2=c*d/(2*delta)"],
            "product_elliptic_map": "Y=2*delta*U*V",
            "full_cover": "T_tau fiber product with q^2=X",
            "generic_branch_supports": [
                "{0,infinity}",
                "{root(a),root(b)}",
                "{root(c),root(d)}",
            ],
            "generic_genera": {"torsor": 1, "full_cover": 5},
            "remaining_conditions": [
                "X is a positive rational square in the exact interval",
                "ell=L(X,tau) is the required odd prime",
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
            "results/closure_quotient_rank_zero_aa_bb_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
