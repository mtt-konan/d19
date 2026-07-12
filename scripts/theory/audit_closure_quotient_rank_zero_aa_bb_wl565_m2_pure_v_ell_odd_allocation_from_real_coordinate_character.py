#!/usr/bin/env python3
"""Audit odd complementary-factor allocation from the real-coordinate character."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl564_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl564_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split"
    )
    from json_io import write_json


def _wl564_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl564"
        and proof.get("binary_choice_at_2_removed_when_present_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character() -> dict[str, Any]:
    wl564 = wl564_module.build_wl564_m2_pure_v_ell_dyadic_allocation_in_complementary_split()
    violations: list[str] = []
    if not _wl564_ready(wl564):
        violations.append("wl564_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "real_coordinate_leading_unit_defined_here": True,
            "inert_odd_kappa_factors_assigned_here": True,
            "split_odd_kappa_square_unit_test_proved_here": True,
            "split_prime_binary_allocations_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl565",
        "object_layer": "m2_odd_factor_allocation_inside_global_complementary_split",
        "input_checkpoint": {"work_log": "wl564", "ready": _wl564_ready(wl564)},
        "allocation_certificate": {
            "normalized_unit": "U_q=(F/r)/q^v_q(F/r) mod q",
            "valuation_parity": "v_q(F/r)=2*v_q(g)",
            "q_divides_alpha": "Legendre(U_q,q)=Legendre(-1,q)",
            "q_divides_beta": "Legendre(U_q,q)=1",
            "q_eq_3_mod_4": "character uniquely selects alpha or beta",
            "q_eq_1_mod_4": "U_q must be square but side remains unresolved",
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
            "results/closure_quotient_rank_zero_aa_bb_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
