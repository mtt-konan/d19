#!/usr/bin/env python3
"""Audit global norm pairing of the odd Gaussian squareclasses."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl550_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl550_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility"
    )
    from json_io import write_json


def _wl550_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl550"
        and proof.get("same_prime_orientation_route_exhausted_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl551_m2_pure_v_ell_global_norm_squareclass_pairing() -> dict[str, Any]:
    wl550 = wl550_module.build_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility()
    violations: list[str] = []
    if not _wl550_ready(wl550):
        violations.append("wl550_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "global_norm_square_parity_used_here": True,
            "split_Gaussian_primes_paired_here": True,
            "squarefree_factor_reduced_to_rational_integer_here": True,
            "global_rational_class_equations_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl551",
        "object_layer": "m2_global_norm_pairing_inside_odd_Gaussian_class_equation",
        "input_checkpoint": {"work_log": "wl550", "ready": _wl550_ready(wl550)},
        "norm_certificate": {
            "element_equation": "delta=eta*d*gamma^2",
            "norm_equation": "W^2=Norm(d)*Norm(gamma)^2",
            "conclusion": "Norm(d) is an integer square",
            "split_prime_rule": "pi and conjugate(pi) have equal squarefree exponents",
            "inert_prime_rule": "the rational Gaussian prime p has norm p^2",
            "reduced_factor": "d=r up to a unit, with rational squarefree r|rad(ell-1)",
            "unit_classes_modulo_squares": ["1", "i"],
        },
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
            "results/closure_quotient_rank_zero_aa_bb_wl551_m2_pure_v_ell_global_norm_squareclass_pairing.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl551_m2_pure_v_ell_global_norm_squareclass_pairing()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
