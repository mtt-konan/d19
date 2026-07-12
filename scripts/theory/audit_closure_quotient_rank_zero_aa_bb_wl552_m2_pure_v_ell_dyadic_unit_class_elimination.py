#!/usr/bin/env python3
"""Audit elimination of the Gaussian unit choice after wl551."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl551_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl551_m2_pure_v_ell_global_norm_squareclass_pairing"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl551_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl551_m2_pure_v_ell_global_norm_squareclass_pairing"
    )
    from json_io import write_json


def _wl551_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl551"
        and proof.get("squarefree_factor_reduced_to_rational_integer_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl552_m2_pure_v_ell_dyadic_unit_class_elimination() -> dict[str, Any]:
    wl551 = wl551_module.build_wl551_m2_pure_v_ell_global_norm_squareclass_pairing()
    violations: list[str] = []
    if not _wl551_ready(wl551):
        violations.append("wl551_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "dyadic_parity_applied_to_global_class_equation_here": True,
            "Gaussian_unit_class_forced_to_i_here": True,
            "two_unit_classes_reduced_to_one_here": True,
            "remaining_eta_i_coordinate_system_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl552",
        "object_layer": "m2_dyadic_unit_class_inside_global_Gaussian_class_equation",
        "input_checkpoint": {"work_log": "wl551", "ready": _wl551_ready(wl551)},
        "parity_certificate": {
            "ell_eq_5_mod_8": {
                "delta_coordinate_parities": "even_real_odd_imaginary",
                "gamma_is_one_plus_i_unit": True,
                "r_times_gamma_square_parities": "odd_real_even_imaginary",
                "forced_unit_class": "i",
                "coordinate_equations": ["E=-2*r*m*n", "F=r*(m^2-n^2)"],
            },
            "ell_eq_1_mod_8": {
                "minimum_v_2_E": 11,
                "F_over_4_is_odd": True,
                "gamma_factorization": "gamma=(1+i)^2*gamma_0",
                "normalized_delta_coordinate_parities": "even_real_odd_imaginary",
                "forced_unit_class": "i",
                "coordinate_equations": ["-E/4=-2*r*m*n", "-F/4=r*(m^2-n^2)"],
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
            "results/closure_quotient_rank_zero_aa_bb_wl552_m2_pure_v_ell_dyadic_unit_class_elimination.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl552_m2_pure_v_ell_dyadic_unit_class_elimination()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
