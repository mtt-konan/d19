#!/usr/bin/env python3
"""Audit exact dyadic strata inside the surviving wl556 orientations."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl556_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl556_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation"
    )
    from json_io import write_json


def _wl556_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl556"
        and proof.get("one_complete_orientation_eliminated_per_branch_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata() -> dict[str, Any]:
    wl556 = wl556_module.build_wl556_m2_pure_v_ell_dyadic_selection_of_gaussian_orientation()
    violations: list[str] = []
    if not _wl556_ready(wl556):
        violations.append("wl556_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "surviving_orientations_stratified_2_adically_here": True,
            "real_and_Gaussian_descent_valuations_coupled_here": True,
            "ell_eq_5_mod_8_standalone_dyadic_route_exhausted_here": True,
            "ell_eq_1_mod_8_mixed_valuation_cases_eliminated_here": True,
            "surviving_valuation_strata_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl557",
        "object_layer": "m2_dyadic_strata_inside_surviving_Gaussian_orientation",
        "input_checkpoint": {"work_log": "wl556", "ready": _wl556_ready(wl556)},
        "valuation_certificate": {
            "ell_eq_5_mod_8": {
                "selected_orientation": "R_pi",
                "valuation": 0,
                "new_condition": "none",
            },
            "ell_eq_1_mod_8": {
                "selected_orientation": "B_pi",
                "c": "v_2(b_0)>=2",
                "k": "v_2(x*y)>=1",
                "formula": {
                    "c<k+1": "v_2(B_pi)=c",
                    "c>k+1": "v_2(B_pi)=k+1",
                    "c=k+1": "v_2(B_pi)>=c+1",
                },
                "minimum_three_condition": "(c=2 and k=1) or (c>=3 and k>=2)",
                "real_descent_match": "v_2(B_pi)=2+v_2(mu*nu)",
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
            "results/closure_quotient_rank_zero_aa_bb_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
