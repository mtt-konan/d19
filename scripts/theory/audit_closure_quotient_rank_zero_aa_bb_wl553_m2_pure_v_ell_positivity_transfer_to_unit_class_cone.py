#!/usr/bin/env python3
"""Audit transfer of wl535 positivity to the unique unit-class cone."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl552_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl552_m2_pure_v_ell_dyadic_unit_class_elimination"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl552_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl552_m2_pure_v_ell_dyadic_unit_class_elimination"
    )
    from json_io import write_json


def _wl552_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl552"
        and proof.get("Gaussian_unit_class_forced_to_i_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone() -> dict[str, Any]:
    wl552 = wl552_module.build_wl552_m2_pure_v_ell_dyadic_unit_class_elimination()
    violations: list[str] = []
    if not _wl552_ready(wl552):
        violations.append("wl552_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "positivity_transferred_to_class_coordinates_here": True,
            "rational_squareclass_cancels_from_sign_here": True,
            "positivity_alone_exhausted_on_both_mod8_branches_here": True,
            "simultaneous_orientation_class_cone_system_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl553",
        "object_layer": "m2_real_positivity_inside_unique_Gaussian_unit_class",
        "input_checkpoint": {"work_log": "wl552", "ready": _wl552_ready(wl552)},
        "positivity_certificate": {
            "identity": "H=(ell-1)*E+ell*F",
            "cone": "C_ell(m,n)=ell*(m^2-n^2)-2*(ell-1)*m*n",
            "ell_eq_5_mod_8": {
                "product_sign": "m*n<0",
                "condition": "C_ell(m,n)>0",
                "uniform_witness": "(m,n)=(5,-8)",
                "witness_value": "41*ell-80",
            },
            "ell_eq_1_mod_8": {
                "product_sign": "m*n>0",
                "condition": "C_ell(m,n)<0",
                "uniform_witness_family": "(m,n)=(1,2^k), k>=1",
            },
        },
        "proof_status": proof_status,
        "violations": violations,
        "full_coordinate_solution_produced_here": False,
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
            "results/closure_quotient_rank_zero_aa_bb_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
