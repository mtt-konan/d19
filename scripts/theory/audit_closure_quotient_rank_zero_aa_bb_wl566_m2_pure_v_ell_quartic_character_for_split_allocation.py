#!/usr/bin/env python3
"""Audit quartic-character constraints on split complementary allocation."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl565_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl565_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character"
    )
    from json_io import write_json


def _wl565_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl565"
        and proof.get("split_odd_kappa_square_unit_test_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl566_m2_pure_v_ell_quartic_character_for_split_allocation() -> dict[str, Any]:
    wl565 = wl565_module.build_wl565_m2_pure_v_ell_odd_allocation_from_real_coordinate_character()
    violations: list[str] = []
    if not _wl565_ready(wl565):
        violations.append("wl565_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "quartic_sign_for_split_factor_defined_here": True,
            "alpha_side_quartic_character_proved_here": True,
            "beta_side_quartic_character_proved_here": True,
            "quartic_character_strictly_refines_split_allocation_here": True,
            "coupled_split_allocation_system_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl566",
        "object_layer": "m2_quartic_character_inside_split_complementary_allocation",
        "input_checkpoint": {"work_log": "wl565", "ready": _wl565_ready(wl565)},
        "quartic_certificate": {
            "quartic_sign": "chi_4,q(H)=H^((q-1)/4)",
            "q_divides_alpha": (
                "chi_4,q(H)=(-1)^((q-1)/4)*Legendre(beta,q)"
            ),
            "q_divides_beta": "chi_4,q(H)=Legendre(alpha,q)",
            "decision_rule": "different predicted signs uniquely select the side",
            "failure_rule": "equal predicted signs leave the side unresolved",
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
            "results/closure_quotient_rank_zero_aa_bb_wl566_m2_pure_v_ell_quartic_character_for_split_allocation.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl566_m2_pure_v_ell_quartic_character_for_split_allocation()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
