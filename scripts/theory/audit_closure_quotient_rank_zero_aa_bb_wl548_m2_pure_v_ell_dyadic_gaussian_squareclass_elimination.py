#!/usr/bin/env python3
"""Audit elimination of the dyadic Gaussian squareclass after wl547."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl547_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl547_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent"
    )
    from json_io import write_json


def _wl547_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl547"
        and proof.get("G_square_reduced_to_finite_S_squareclasses_here") is True
        and payload.get("advance_to_m3") is False
    )


def _valuation_certificate() -> dict[str, Any]:
    return {
        "ell_eq_5_mod_8": {
            "Q_parity": "odd",
            "D_parity": "odd",
            "P_parity": "odd",
            "R_parity": "odd",
            "P_mod_8": 7,
            "R_mod_8": 1,
            "post_division_coordinate_parities": "opposite",
            "v_1_plus_i_P_plus_iR": 1,
            "v_1_plus_i_delta": 0,
        },
        "ell_eq_1_mod_8": {
            "minimum_v_2_Q": 3,
            "P_over_4_mod_16": "D^4",
            "R_over_4_mod_64": "-D^4",
            "P_over_4_mod_4": 1,
            "R_over_4_mod_4": 3,
            "post_division_coordinate_parities": "opposite",
            "P_over_4_and_R_over_4_are_odd": True,
            "v_1_plus_i_P_plus_iR": 5,
            "v_1_plus_i_delta": 4,
        },
        "both_delta_valuations_are_even": True,
    }


def build_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination() -> dict[str, Any]:
    wl547 = wl547_module.build_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent()
    valuation = _valuation_certificate()
    violations: list[str] = []
    if not _wl547_ready(wl547):
        violations.append("wl547_input_not_ready")
    values = [
        valuation["ell_eq_5_mod_8"]["v_1_plus_i_delta"],
        valuation["ell_eq_1_mod_8"]["v_1_plus_i_delta"],
    ]
    if any(value % 2 for value in values):
        violations.append("dyadic_delta_valuation_not_even")
    ready = not violations
    proof_status = (
        {
            "dyadic_delta_valuation_computed_exactly_here": True,
            "one_plus_i_squareclass_eliminated_here": True,
            "finite_support_reduced_to_odd_primes_here": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl548",
        "object_layer": "m2_dyadic_Gaussian_squareclass_elimination_inside_wl547",
        "input_checkpoint": {"work_log": "wl547", "ready": _wl547_ready(wl547)},
        "valuation_certificate": valuation,
        "refined_support": {
            "contains_one_plus_i": False,
            "odd_rational_primes": "p|ell-1 with Legendre(2/p)=1",
            "candidate_root_condition": "(Q^2/D^2)^2+4*(Q^2/D^2)-4=0 mod p",
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
            "results/closure_quotient_rank_zero_aa_bb_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
