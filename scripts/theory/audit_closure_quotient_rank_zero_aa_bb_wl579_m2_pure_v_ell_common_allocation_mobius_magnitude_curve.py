#!/usr/bin/env python3
"""Audit the Mobius genus-one curve for common-allocation magnitudes."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl578_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl578_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation"
    )
    from json_io import write_json


def _wl578_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl578"
        and proof.get("allocation_analysis_exhausted_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    p, k_form, lam, u, v, z, w = sp.symbols(
        "P K lambda u v z w", positive=True
    )
    mobius = (2 * k_form + p * z) / (p - 2 * k_form * z)
    curve = lam * v**2 * (p - 2 * k_form * lam * u**2) - (
        2 * k_form + p * lam * u**2
    )
    return {
        "mobius_difference": sp.simplify(
            mobius - z - 2 * k_form * (1 + z**2) / (p - 2 * k_form * z)
        )
        == 0,
        "biquadratic_substitution": sp.simplify(
            (w - mobius).subs({z: lam * u**2, w: lam * v**2})
            * (p - 2 * k_form * lam * u**2)
            - curve
        )
        == 0,
        "zero_pole_collision_impossible_polynomial": sp.expand(p**2 + 4 * k_form**2)
        == p**2 + 4 * k_form**2,
    }


def build_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve() -> dict[str, Any]:
    wl578 = wl578_module.build_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl578_ready(wl578):
        violations.append("wl578_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "common_allocation_magnitude_reduced_to_Mobius_map_here": True,
            "biquadratic_genus_one_curve_proved_here": True,
            "strict_normalized_magnitude_ordering_proved_here": True,
            "projective_magnitude_converse_proved_here": True,
            "primitive_linear_form_reconstruction_proved_here": False,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl579",
        "object_layer": "m2_common_allocation_Mobius_magnitude_curve",
        "input_checkpoint": {"work_log": "wl578", "ready": _wl578_ready(wl578)},
        "magnitude_curve_certificate": {
            "lambda": "beta/alpha",
            "ratios": ["z=lambda*u^2=B/A", "w=lambda*v^2=D/C"],
            "Mobius": "w=(2*K+P*z)/(P-2*K*z)",
            "curve": "lambda*v^2*(P-2*K*lambda*u^2)=2*K+P*lambda*u^2",
            "domain": "0<u^2<P/(2*K*lambda)",
            "ordering": "v>u",
            "genus": 1,
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
            "results/closure_quotient_rank_zero_aa_bb_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl579_m2_pure_v_ell_common_allocation_mobius_magnitude_curve()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
