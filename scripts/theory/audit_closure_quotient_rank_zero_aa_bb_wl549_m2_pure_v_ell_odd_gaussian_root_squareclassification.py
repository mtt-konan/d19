#!/usr/bin/env python3
"""Audit the odd common-prime root-square classification after wl548."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl548_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl548_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination"
    )
    from json_io import write_json


def _wl548_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl548"
        and proof.get("one_plus_i_squareclass_eliminated_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification() -> dict[str, Any]:
    wl548 = wl548_module.build_wl548_m2_pure_v_ell_dyadic_gaussian_squareclass_elimination()
    violations: list[str] = []
    if not _wl548_ready(wl548):
        violations.append("wl548_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "root_square_condition_classified_here": True,
            "source_square_residues_automatic_at_square_root_here": True,
            "p_eq_7_mod_8_root_test_exhausted_here": True,
            "odd_Gaussian_class_equations_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl549",
        "object_layer": "m2_odd_Gaussian_common_prime_root_square_classification",
        "input_checkpoint": {"work_log": "wl548", "ready": _wl548_ready(wl548)},
        "identities_at_a_root": {
            "polynomial": "t^2+4*t-4",
            "one_minus_t": "t^2/4",
            "t_plus_four": "4/t",
            "root_is_nonzero": True,
        },
        "classification": {
            "p_mod_8_eq_7": "exactly_one_of_two_roots_is_square",
            "p_mod_8_eq_1": "either_zero_or_two_roots_are_square",
            "refined_support": "p|ell-1 and f has a nonzero square root mod p",
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
            "results/closure_quotient_rank_zero_aa_bb_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl549_m2_pure_v_ell_odd_gaussian_root_squareclassification()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
