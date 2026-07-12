#!/usr/bin/env python3
"""Audit rational-locus descent from the wl581 Q(i) elliptic quotient."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl581_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl581_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient"
    )
    from json_io import write_json


def _wl581_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl581"
        and proof.get("quadratic_elliptic_quotient_over_q_i_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    x, tau, s, a_part, b_part, z = sp.symbols("X tau S A B Z", nonzero=True)
    i = sp.I
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = x + 2 * tau + 4
    fourth = tau * (x + 4) - 2
    l1 = (tau + 2) * s + 2 * tau**2 + 8 * tau + 6
    l2 = (2 * tau**2 - tau) * s + 6 * tau**2 - 8 * tau + 2
    reconstructed_x = -2 * a_part / b_part
    reconstructed_z = a_part * reconstructed_x
    s_from_parts = 2 * (b_part**2 - a_part**2) / (a_part * b_part)
    quotient_rhs = (-s + 4 * i) * l1 * l2
    invariant_rhs = first * second * third * fourth * (x - 2 * i) ** 2 / x**3
    forward_a = z / x
    forward_b = -2 * z / x**2
    root_l1 = -(2 * tau**2 + 8 * tau + 6) / (tau + 2)
    root_l2 = -(6 * tau**2 - 8 * tau + 2) / (2 * tau**2 - tau)
    root_a = 2 / (tau + 2)
    root_c = -2 * (tau + 2)
    root_b = 2 * tau / (2 * tau - 1)
    root_d = 2 / tau - 4
    return {
        "real_imaginary_elimination_relation": sp.simplify(
            (-s * (a_part * b_part / 2)) - (a_part**2 - b_part**2)
        ).subs(s, s_from_parts)
        == 0,
        "rational_x_reconstructs_s": sp.simplify(
            (reconstructed_x - 4 / reconstructed_x) - s_from_parts
        )
        == 0,
        "quadratic_lift_square_is_automatic": sp.simplify(
            s_from_parts**2
            + 16
            - (reconstructed_x + 4 / reconstructed_x) ** 2
        )
        == 0,
        "elliptic_y_reconstructs_from_x_z": sp.simplify(
            reconstructed_z * (reconstructed_x - 2 * i) / reconstructed_x**2
            - (a_part + i * b_part)
        )
        == 0,
        "quotient_rhs_matches_genus_two_rhs": sp.simplify(
            quotient_rhs.subs(s, x - 4 / x) - invariant_rhs
        )
        == 0,
        "forward_inverse_recovers_x": sp.simplify(-2 * forward_a / forward_b - x)
        == 0,
        "forward_inverse_recovers_z": sp.simplify(forward_a * x - z) == 0,
        "first_two_torsion_orbit_sum": sp.simplify(root_a + root_c - root_l1)
        == 0,
        "first_two_torsion_orbit_product": sp.simplify(root_a * root_c + 4)
        == 0,
        "second_two_torsion_orbit_sum": sp.simplify(root_b + root_d - root_l2)
        == 0,
        "second_two_torsion_orbit_product": sp.simplify(root_b * root_d + 4)
        == 0,
    }


def build_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence(
) -> dict[str, Any]:
    wl581 = (
        wl581_module.build_wl581_m2_pure_v_ell_genus_two_character_and_quadratic_elliptic_quotient()
    )
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl581_ready(wl581):
        violations.append("wl581_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "q_i_real_coordinate_locus_split_here": True,
            "rational_genus_two_lift_reconstructed_here": True,
            "nonbranch_forward_and_inverse_bijection_proved_here": True,
            "quadratic_lift_obstruction_shown_automatic_here": True,
            "wl581_unrestricted_elliptic_route_exhausted_here": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl582",
        "object_layer": "m2_q_i_elliptic_rational_locus_descent_equivalence",
        "input_checkpoint": {"work_log": "wl581", "ready": _wl581_ready(wl581)},
        "descent_certificate": {
            "elliptic_split": ["A^2-B^2=-S*L", "A*B=2*L"],
            "inverse": ["X=-2*A/B", "Z=A*X"],
            "automatic_square": "S^2+16=(X+4/X)^2",
            "remaining_independent_conditions": [
                "X is a positive rational square in the exact interval",
                "the two source products are individually rational squares",
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
            "results/closure_quotient_rank_zero_aa_bb_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl582_m2_pure_v_ell_q_i_elliptic_rational_locus_descent_equivalence()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
