#!/usr/bin/env python3
"""Audit common-prime compatibility with both wl546 orientations."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl549_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl549_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification"
    )
    from json_io import write_json


def _wl549_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl549"
        and proof.get("root_square_condition_classified_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility() -> dict[str, Any]:
    wl549 = wl549_module.build_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification()
    violations: list[str] = []
    if not _wl549_ready(wl549):
        violations.append("wl549_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "both_wl546_orientations_locally_compatible_here": True,
            "quadratic_etale_hilbert_90_witness_given_here": True,
            "same_prime_orientation_route_exhausted_here": True,
            "global_odd_class_equation_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl550",
        "object_layer": "m2_common_prime_local_compatibility_with_fixed_Gaussian_orientations",
        "input_checkpoint": {"work_log": "wl549", "ready": _wl549_ready(wl549)},
        "certificate": {
            "quadratic_etale_algebra": "F_p[i] with conjugation",
            "norm_one_parameterization": "h=z/conjugate(z)=z^2/Norm(z)",
            "witness_if_h_not_minus_one": "z=1+h",
            "witness_if_h_is_minus_one": "z=i",
            "first_orientation_target": "w=A+i*q",
            "second_orientation_target": "w=q+i*A",
            "wl549_root_witness": "A=+/-t/2 when q^2=t",
        },
        "proof_status": proof_status,
        "violations": violations,
        "global_integer_candidate_produced_here": False,
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
            "results/closure_quotient_rank_zero_aa_bb_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl550_m2_pure_v_ell_common_prime_orientation_local_compatibility()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
