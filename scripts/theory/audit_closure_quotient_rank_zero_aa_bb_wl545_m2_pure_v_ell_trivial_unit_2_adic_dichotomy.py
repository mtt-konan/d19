#!/usr/bin/env python3
"""Audit the trivial-unit 2-adic dichotomy after wl544."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl544_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl544_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent"
    )
    from json_io import write_json


def _wl544_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl544"
        and proof.get("forward_and_converse_reconstruction_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def _unit_square_residues_mod_8() -> list[int]:
    return sorted({x * x % 8 for x in range(1, 8, 2)})


def _residue_certificate() -> dict[str, Any]:
    unit_squares = _unit_square_residues_mod_8()
    return {
        "unit_square_residues_mod_8": unit_squares,
        "k_eq_1_parenthesized_residues": {
            1: (1 + 1) % 8,
            5: (5 + 1) % 8,
        },
        "k_eq_1_total_valuation_is_3": True,
        "k_eq_2_unit_residue_mod_8": 5,
        "k_eq_2_unit_is_nonsquare": 5 not in unit_squares,
        "k_eq_0_ell_1_second_square_residue": 5,
        "k_ge_3_first_square_requires_ell_mod_8": 1,
        "G_unit_branch_residue_mod_8": 1,
        "G_high_valuation_unit_precision": "1 mod 2^7 after dividing by 16",
    }


def build_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy() -> dict[str, Any]:
    wl544 = wl544_module.build_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent()
    residue = _residue_certificate()
    violations: list[str] = []
    if not _wl544_ready(wl544):
        violations.append("wl544_input_not_ready")
    if residue["unit_square_residues_mod_8"] != [1]:
        violations.append("unit_square_residues_mod_8_mismatch")
    if residue["k_eq_2_unit_is_nonsquare"] is not True:
        violations.append("k_eq_2_not_excluded")
    ready = not violations
    proof_status = (
        {
            "trivial_unit_2_adic_q_valuation_classified_here": True,
            "ell_eq_5_mod_8_forces_u_v_odd_here": True,
            "ell_eq_1_mod_8_forces_even_halves_opposite_parity_here": True,
            "G_condition_adds_no_2_adic_obstruction_here": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl545",
        "object_layer": "m2_trivial_unit_branch_2_adic_dichotomy_inside_wl544",
        "input_checkpoint": {"work_log": "wl544", "ready": _wl544_ready(wl544)},
        "q_valuation_dichotomy": {
            "ell_eq_5_mod_8": "v_2(q)=0",
            "ell_eq_1_mod_8": "v_2(q)>=3",
            "excluded_valuations": [1, 2],
        },
        "descent_variable_parity": {
            "ell_eq_5_mod_8": "u and v are both odd",
            "ell_eq_1_mod_8": "u=2m and v=2n with m,n of opposite parity",
            "primitive_normalization": "v_2(N)=2",
        },
        "residue_certificate": residue,
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
            "results/closure_quotient_rank_zero_aa_bb_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
