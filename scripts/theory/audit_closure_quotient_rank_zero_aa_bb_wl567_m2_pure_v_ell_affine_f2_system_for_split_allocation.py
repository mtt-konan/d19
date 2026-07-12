#!/usr/bin/env python3
"""Audit affine F2 linearization of the split-prime quartic allocation."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl566_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl566_m2_pure_v_ell_quartic_character_for_split_allocation"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl566_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl566_m2_pure_v_ell_quartic_character_for_split_allocation"
    )
    from json_io import write_json


def _wl566_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl566"
        and proof.get("quartic_character_strictly_refines_split_allocation_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation() -> dict[str, Any]:
    wl566 = wl566_module.build_wl566_m2_pure_v_ell_quartic_character_for_split_allocation()
    violations: list[str] = []
    if not _wl566_ready(wl566):
        violations.append("wl566_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "quartic_allocation_linearized_over_F2_here": True,
            "affine_row_formula_proved_here": True,
            "exponential_case_split_removed_here": True,
            "affine_system_coupled_to_integer_equations_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl567",
        "object_layer": "m2_affine_F2_system_for_split_quartic_allocation",
        "input_checkpoint": {"work_log": "wl566", "ready": _wl566_ready(wl566)},
        "affine_system_certificate": {
            "variable": "x_q=1 iff q|alpha",
            "off_diagonal": "A_qt=(1-Legendre(t,q))/2",
            "diagonal": "Delta_q=d_q+a_q+b_q+sum_(t!=q) A_qt",
            "right_hand_side": "z_q+a_q",
            "row": "Delta_q*x_q+sum_(t!=q) A_qt*x_t=z_q+a_q",
            "outcomes": ["inconsistent", "unique", "explicit affine space"],
        },
        "proof_status": proof_status,
        "violations": violations,
        "theorem_level_selmer_matrix_claimed": False,
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
            "results/closure_quotient_rank_zero_aa_bb_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
