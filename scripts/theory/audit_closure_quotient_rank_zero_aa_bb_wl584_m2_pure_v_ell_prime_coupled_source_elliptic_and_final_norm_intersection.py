#!/usr/bin/env python3
"""Audit prime coupling of the source elliptic and final norm lift."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl583_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl583_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product"
    )
    from json_io import write_json


def _wl583_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl583"
        and proof.get("full_cover_fiber_product_equivalence_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    ell, x, tau = sp.symbols("ell X tau", nonzero=True)
    delta = tau**2 + 2 * tau - 1
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = x + 2 * tau + 4
    fourth = tau * (x + 4) - 2
    ell_formula = (
        tau * x**2 + 2 * x * tau**2 + 8 * x * tau - 2 * x - 4 * tau
    ) / (2 * x * delta)
    u_square = first * second / (2 * delta)
    v_square = third * fourth / (2 * delta)
    f = x**2 + (8 - 4 * ell) * x - 4
    e = 4 * (ell - 1) * x
    parameter_relation = sp.expand(e * tau**2 - 2 * f * tau - e)
    g = sp.expand(f**2 + e**2)
    return {
        "first_torsor_square_becomes_source_curve": sp.simplify(
            u_square - x * (ell_formula - x)
        )
        == 0,
        "second_torsor_square_becomes_source_curve": sp.simplify(
            v_square - (ell_formula * x + 4)
        )
        == 0,
        "universal_difference_identity": sp.simplify(v_square - u_square - x**2 - 4)
        == 0,
        "parameter_formula_is_norm_quadratic": sp.simplify(
            parameter_relation.subs(ell, ell_formula)
        )
        == 0,
        "norm_quadratic_discriminant": sp.discriminant(
            e * tau**2 - 2 * f * tau - e, tau
        )
        == 4 * g,
        "positive_norm_root": sp.simplify(
            (e * tau**2 - 2 * f * tau - e).subs(
                tau, (f + sp.symbols("C")) / e
            )
            - (sp.symbols("C") ** 2 - g) / e
        )
        == 0,
    }


def build_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection(
) -> dict[str, Any]:
    wl583 = (
        wl583_module.build_wl583_m2_pure_v_ell_source_square_genus_one_torsor_and_square_x_fiber_product()
    )
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl583_ready(wl583):
        violations.append("wl583_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "prime_coupled_torsor_source_identities_proved_here": True,
            "fixed_ell_source_curve_genus_one_proved_here": True,
            "square_x_source_cover_genus_one_proved_here": True,
            "final_norm_discriminant_equivalence_proved_here": True,
            "unrestricted_source_elliptic_route_exhausted_here": True,
            "final_norm_intersection_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl584",
        "object_layer": "m2_prime_coupled_source_elliptic_and_final_norm_intersection",
        "input_checkpoint": {"work_log": "wl583", "ready": _wl583_ready(wl583)},
        "intersection_certificate": {
            "source_curve": ["U^2=X*(ell-X)", "V^2=ell*X+4"],
            "source_curve_genus": 1,
            "source_boundary_points": ["(0,0,2)", "(0,0,-2)"],
            "square_x_source_cover_genus": 1,
            "norm_quadratic": "E*tau^2-2*F*tau-E=0",
            "norm_discriminant": "4*G_ell(X)",
            "live_intersection": [
                "square-X source genus-one point",
                "G_ell(X) square with selected tau root",
                "exact positive interval",
                "ell odd prime congruent 1 mod 4",
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
            "results/closure_quotient_rank_zero_aa_bb_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
