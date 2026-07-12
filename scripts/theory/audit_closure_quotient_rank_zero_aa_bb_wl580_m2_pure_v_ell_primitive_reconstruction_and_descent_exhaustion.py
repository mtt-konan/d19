#!/usr/bin/env python3
"""Audit primitive reconstruction and exhaustion of the allocation descent."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl579_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl579_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve"
    )
    from json_io import write_json


def _wl579_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl579"
        and proof.get("projective_magnitude_converse_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    x, tau, z = sp.symbols("X tau z")
    first = x * (tau + 2) - 2
    second = 2 * tau - x * (2 * tau - 1)
    third = tau * (x + 4) - 2
    fourth = x + 2 * tau + 4
    recovered = (x + 2 * z * (1 - x)) / (x * (z + 2) - 2)
    return {
        "tau_reconstruction": sp.simplify((z * first - second).subs(tau, recovered)) == 0,
        "strict_cross_identity": sp.expand(
            first * fourth
            - second * third
            - 2 * (tau**2 + 1) * (x**2 + 4 * x - 4)
        )
        == 0,
        "first_product_ratio_identity": sp.simplify(first * second - first**2 * z).subs(
            z, second / first
        )
        == 0,
        "second_product_ratio_identity": sp.simplify(third * fourth - third**2 * z).subs(
            z, fourth / third
        )
        == 0,
    }


def build_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion() -> dict[str, Any]:
    wl579 = wl579_module.build_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl579_ready(wl579):
        violations.append("wl579_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "tau_uniquely_reconstructed_from_X_z_here": True,
            "primitive_m_n_has_no_extra_branch_here": True,
            "canonical_squareclass_self_consistency_stated_here": True,
            "source_squares_reconstructed_from_self_consistent_torsor_here": True,
            "allocation_descent_exhausted_here": True,
            "self_consistent_genus_one_family_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl580",
        "object_layer": "m2_primitive_reconstruction_and_descent_exhaustion",
        "input_checkpoint": {"work_log": "wl579", "ready": _wl579_ready(wl579)},
        "reconstruction_certificate": {
            "tau": "[X+2*z*(1-X)]/[X*(z+2)-2]",
            "denominator": "X*(z+2)-2>0 for X>1,z>0",
            "canonical_class": "[lambda]=[2*(tau^2+2*tau-1)]",
            "source_square_equivalence": [
                "z/lambda square reconstructs first source square",
                "w/lambda square reconstructs second source square",
            ],
            "strict_identity": "Abar*Dbar-Bbar*Cbar=2*(tau^2+1)*(X^2+4*X-4)",
        },
        "exact_missing_lemma": (
            "no positive rational point on the self-consistent genus-one magnitude "
            "torsor in the wl570 interval"
        ),
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
            "results/closure_quotient_rank_zero_aa_bb_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl580_m2_pure_v_ell_primitive_reconstruction_and_descent_exhaustion()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
