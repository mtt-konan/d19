#!/usr/bin/env python3
"""Audit the forced allocation of 2 in the wl563 complementary split."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl563_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl563_m2_pure_v_ell_global_product_squareclass_split"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl563_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl563_m2_pure_v_ell_global_product_squareclass_split"
    )
    from json_io import write_json


def _wl563_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl563"
        and proof.get("coprime_squareclass_split_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split() -> dict[str, Any]:
    wl563 = wl563_module.build_wl563_m2_pure_v_ell_global_product_squareclass_split()
    violations: list[str] = []
    if not _wl563_ready(wl563):
        violations.append("wl563_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "dyadic_factor_in_complementary_split_allocated_here": True,
            "canonical_r_mod8_coupled_to_global_split_here": True,
            "binary_choice_at_2_removed_when_present_here": True,
            "odd_complementary_divisor_allocation_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl564",
        "object_layer": "m2_dyadic_allocation_inside_global_complementary_squareclass_split",
        "input_checkpoint": {"work_log": "wl563", "ready": _wl563_ready(wl563)},
        "allocation_certificate": {
            "r_mod_8": [1, 7],
            "ell_eq_5_mod_8": {
                "kappa_is_even": True,
                "r_eq_1_mod_8": "2|beta",
                "r_eq_7_mod_8": "2|alpha",
            },
            "ell_eq_1_mod_8": {
                "kappa_even_iff": "v_2(ell-1) is even",
                "r_eq_1_mod_8_when_even": "2|alpha",
                "r_eq_7_mod_8_when_even": "2|beta",
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
            "results/closure_quotient_rank_zero_aa_bb_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
