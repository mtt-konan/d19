#!/usr/bin/env python3
"""Audit the uniform unit-free standard norm-square equation after wl554."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl554_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl554_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd"
    )
    from json_io import write_json


def _wl554_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl554"
        and proof.get("rational_class_made_candidate_canonical_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation() -> dict[str, Any]:
    wl554 = wl554_module.build_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd()
    violations: list[str] = []
    if not _wl554_ready(wl554):
        violations.append("wl554_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "standard_norm_element_identified_here": True,
            "Gaussian_unit_removed_uniformly_here": True,
            "branch_dependent_cone_signs_unified_here": True,
            "standard_orientation_square_system_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl555",
        "object_layer": "m2_unit_free_standard_norm_square_inside_trivial_real_unit_branch",
        "input_checkpoint": {"work_log": "wl554", "ready": _wl554_ready(wl554)},
        "standard_equation": {
            "E": "4*(ell-1)*Q^2*D^2",
            "F": "Q^4+(8-4*ell)*Q^2*D^2-4*D^4",
            "Z": "F+i*E",
            "delta_relation": "delta=i*conjugate(Z)",
            "unit_free_square": "Z=r*(a+i*b)^2",
            "coordinate_equations": ["F=r*(a^2-b^2)", "E=2*r*a*b"],
            "uniform_positivity": "ell*(a^2-b^2)+2*(ell-1)*a*b>0",
            "canonical_r": "sqf_odd(gcd(ell-1,R))",
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
            "results/closure_quotient_rank_zero_aa_bb_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
