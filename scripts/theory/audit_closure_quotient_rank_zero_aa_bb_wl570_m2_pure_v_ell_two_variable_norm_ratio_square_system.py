#!/usr/bin/env python3
"""Audit the exact two-variable norm-ratio square system for wl535."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl569_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl569_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch"
    )
    from json_io import write_json


def _wl569_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl569"
        and proof.get("positive_ordered_norm_ratio_branch_unique_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    ell, x, tau = sp.symbols("ell X tau", positive=True)
    delta = tau**2 + 2 * tau - 1
    f = x**2 + (8 - 4 * ell) * x - 4
    e = 4 * (ell - 1) * x
    relation = sp.expand(2 * tau * f - e * (tau**2 - 1))
    ell_formula = (
        tau * x**2 + 2 * x * tau**2 + 8 * x * tau - 2 * x - 4 * tau
    ) / (2 * x * delta)
    p_square = -(
        (x * tau + 2 * x - 2) * (2 * x * tau - x - 2 * tau)
    ) / (2 * x * delta)
    c_square = (
        (x + 2 * tau + 4) * (x * tau + 4 * tau - 2)
    ) / (2 * delta)
    reconstructed_f = e * (tau**2 - 1) / (2 * tau)
    reconstructed_c = e * (1 + tau**2) / (2 * tau)
    return {
        "ell_formula_solves_norm_ratio_relation": sp.simplify(
            relation.subs(ell, ell_formula)
        )
        == 0,
        "first_source_square_factorization": sp.simplify(
            (ell - x).subs(ell, ell_formula) - p_square
        )
        == 0,
        "second_source_square_factorization": sp.simplify(
            (ell * x + 4).subs(ell, ell_formula) - c_square
        )
        == 0,
        "converse_norm_identity": sp.simplify(
            reconstructed_c**2 - reconstructed_f**2 - e**2
        )
        == 0,
    }


def build_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system() -> dict[str, Any]:
    wl569 = wl569_module.build_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl569_ready(wl569):
        violations.append("wl569_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "quartic_square_root_eliminated_by_unique_tau_here": True,
            "parameter_formula_in_X_tau_proved_here": True,
            "both_source_squares_factored_in_X_tau_here": True,
            "forward_and_converse_wl535_reconstruction_proved_here": True,
            "two_variable_square_system_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl570",
        "object_layer": "m2_exact_two_variable_norm_ratio_square_system",
        "input_checkpoint": {"work_log": "wl569", "ready": _wl569_ready(wl569)},
        "system_certificate": {
            "variables": ["X=q^2", "tau=(C+F)/E"],
            "delta": "tau^2+2*tau-1",
            "ell": (
                "(tau*X^2+2*X*tau^2+8*X*tau-2*X-4*tau)"
                "/(2*X*delta)"
            ),
            "first_square": (
                "-(X*tau+2*X-2)*(2*X*tau-X-2*tau)/(2*X*delta)"
            ),
            "second_square": (
                "(X+2*tau+4)*(X*tau+4*tau-2)/(2*delta)"
            ),
            "intervals": "sigma_ell<X<ell and rho_ell<tau<1",
            "strict_consequence": "X*(2*tau-1)<2*tau",
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
            "results/closure_quotient_rank_zero_aa_bb_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl570_m2_pure_v_ell_two_variable_norm_ratio_square_system()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
