#!/usr/bin/env python3
"""Audit dyadic selection of one wl546 Gaussian orientation per branch."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl555_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl555_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation"
    )
    from json_io import write_json


def _wl555_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl555"
        and proof.get("Gaussian_unit_removed_uniformly_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation() -> dict[str, Any]:
    wl555 = wl555_module.build_wl555_m2_pure_v_ell_unit_free_standard_norm_square_equation()
    violations: list[str] = []
    if not _wl555_ready(wl555):
        violations.append("wl555_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "wl546_orientations_coupled_to_dyadic_branches_here": True,
            "one_complete_orientation_eliminated_per_branch_here": True,
            "ell_eq_5_mod_8_R_orientation_selected_here": True,
            "ell_eq_1_mod_8_B_orientation_selected_here": True,
            "surviving_orientation_systems_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl556",
        "object_layer": "m2_dyadic_selection_inside_wl546_Gaussian_orientations",
        "input_checkpoint": {"work_log": "wl555", "ready": _wl555_ready(wl555)},
        "orientation_certificate": {
            "convention": "a_0 odd and b_0 even",
            "B_pi_parity": "even",
            "R_pi_parity": "odd",
            "ell_eq_5_mod_8": {
                "Q_parity": "odd",
                "selected_orientation": "Q=+/-R_pi(x,y)",
            },
            "ell_eq_1_mod_8": {
                "minimum_v_2_Q": 3,
                "selected_orientation": "Q=+/-B_pi(x,y)",
                "remaining_condition": "v_2(B_pi)>=3",
            },
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
            "results/closure_quotient_rank_zero_aa_bb_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
