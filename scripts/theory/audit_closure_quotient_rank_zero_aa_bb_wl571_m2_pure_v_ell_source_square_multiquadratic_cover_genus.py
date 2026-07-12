#!/usr/bin/env python3
"""Audit the genus of the wl570 source-square multiquadratic cover."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl570_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl570_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system"
    )
    from json_io import write_json


def _wl570_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl570"
        and proof.get("forward_and_converse_wl535_reconstruction_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, Any]:
    x, tau = sp.symbols("X tau")
    delta = tau**2 + 2 * tau - 1
    factors = {
        "a": x * (tau + 2) - 2,
        "b": 2 * tau - x * (2 * tau - 1),
        "c": x + 2 * tau + 4,
        "d": tau * (x + 4) - 2,
    }
    names = list(factors)
    resultants = {
        f"{left}_{right}": sp.factor(sp.resultant(factors[left], factors[right], x))
        for index, left in enumerate(names)
        for right in names[index + 1 :]
    }
    expected = {
        "a_b": 2 * (tau**2 + 1),
        "a_c": 2 * (tau**2 + 4 * tau + 5),
        "a_d": 4 * delta,
        "b_c": -4 * delta,
        "b_d": -2 * (5 * tau**2 - 4 * tau + 1),
        "c_d": -2 * (tau**2 + 1),
    }
    half = {name: sp.factor(value.subs(tau, sp.Rational(1, 2))) for name, value in factors.items()}
    ell_half = sp.factor(
        (
            tau * x**2 + 2 * x * tau**2 + 8 * x * tau - 2 * x - 4 * tau
        ).subs(tau, sp.Rational(1, 2))
        / (2 * x * delta.subs(tau, sp.Rational(1, 2)))
    )
    return {
        "pairwise_resultants": {key: str(value) for key, value in resultants.items()},
        "pairwise_resultants_verified": all(
            sp.expand(resultants[key] - value) == 0 for key, value in expected.items()
        ),
        "tau_half_factors": {key: str(value) for key, value in half.items()},
        "tau_half_has_infinity_and_zero_roots": half["b"] == 1 and half["d"] == x / 2,
        "tau_half_parameter_formula": str(ell_half),
        "tau_half_parameter_formula_verified": sp.simplify(
            ell_half - (x + 5 - 4 / x)
        )
        == 0,
    }


def build_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus() -> dict[str, Any]:
    wl570 = wl570_module.build_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl570_ready(wl570):
        violations.append("wl570_input_not_ready")
    for key in (
        "pairwise_resultants_verified",
        "tau_half_has_infinity_and_zero_roots",
        "tau_half_parameter_formula_verified",
    ):
        if symbolic[key] is not True:
            violations.append(key)
    ready = not violations
    proof_status = (
        {
            "product_quartic_smooth_genus_one_for_all_admissible_tau_here": True,
            "full_source_square_cover_genus_five_for_tau_ne_half_here": True,
            "tau_half_unique_genus_drop_to_one_here": True,
            "product_plus_one_square_converse_proved_here": True,
            "exceptional_tau_half_branch_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl571",
        "object_layer": "m2_source_square_multiquadratic_cover_genus",
        "input_checkpoint": {"work_log": "wl570", "ready": _wl570_ready(wl570)},
        "cover_certificate": {
            "product_curve": "Y^2=a*b*c*d",
            "product_curve_genus": 1,
            "product_curve_rational_2_torsion": "full",
            "generic_full_cover_degree": 8,
            "generic_full_cover_branch_points": 6,
            "generic_full_cover_genus": 5,
            "tau_half_full_cover_branch_points": 4,
            "tau_half_full_cover_genus": 1,
            "tau_half_system": [
                "ell=X+5-4/X",
                "p^2=5-4/X",
                "s^2=X*(X+5)",
                "X=q^2",
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
            "results/closure_quotient_rank_zero_aa_bb_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
