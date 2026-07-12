#!/usr/bin/env python3
"""Audit the scaled Gaussian rotation between the two source-factor pairs."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl574_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl574_m2_pure_v_ell_common_delta_squareclass_double_split"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl574_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl574_m2_pure_v_ell_common_delta_squareclass_double_split"
    )
    from json_io import write_json


def _wl574_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl574"
        and proof.get("two_complementary_splits_of_same_k_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, Any]:
    a, b, m, n = sp.symbols("a b m n", integer=True)
    first = a**2 * m + 2 * a**2 * n - 2 * b**2 * n
    second = a**2 * n + 2 * b**2 * m - 2 * a**2 * m
    third = a**2 * m + 4 * b**2 * m - 2 * b**2 * n
    fourth = a**2 * n + 2 * b**2 * m + 4 * b**2 * n
    p = a**4 + 4 * b**4
    k_form = a**4 + 4 * a**2 * b**2 - 4 * b**4
    r1 = 5 * a**4 - 8 * a**2 * b**2 + 4 * b**4
    r2 = a**4 + 8 * a**2 * b**2 + 20 * b**4
    x, y = sp.symbols("x y")
    p_xy = x**2 + 4 * y**2
    k_xy = x**2 + 4 * x * y - 4 * y**2
    r1_xy = 5 * x**2 - 8 * x * y + 4 * y**2
    r2_xy = x**2 + 8 * x * y + 20 * y**2
    return {
        "forward_C": sp.expand(r1 * third - (p * first - 2 * k_form * second)) == 0,
        "forward_D": sp.expand(r1 * fourth - (2 * k_form * first + p * second)) == 0,
        "inverse_A": sp.expand(r2 * first - (p * third + 2 * k_form * fourth)) == 0,
        "inverse_B": sp.expand(r2 * second - (-2 * k_form * third + p * fourth)) == 0,
        "norm_identity": sp.expand(p**2 + 4 * k_form**2 - r1 * r2) == 0,
        "sum_square_identity": sp.expand(
            r1 * (third**2 + fourth**2) - r2 * (first**2 + second**2)
        )
        == 0,
        "PK_resultant": str(sp.factor(sp.resultant(p_xy, k_xy, x))),
        "R1R2_resultant": str(sp.factor(sp.resultant(r1_xy, r2_xy, x))),
        "resultants_verified": sp.factor(sp.resultant(p_xy, k_xy, x)) == 128 * y**4
        and sp.factor(sp.resultant(r1_xy, r2_xy, x)) == 18432 * y**4,
    }


def build_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs() -> dict[str, Any]:
    wl574 = wl574_module.build_wl574_m2_pure_v_ell_common_delta_squareclass_double_split()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl574_ready(wl574):
        violations.append("wl574_input_not_ready")
    for key, value in symbolic.items():
        if key.endswith("_resultant"):
            continue
        if value is not True:
            violations.append(key)
    ready = not violations
    proof_status = (
        {
            "exact_scaled_Gaussian_rotation_proved_here": True,
            "inverse_rotation_and_norm_identity_proved_here": True,
            "PK_primitive_away_from_two_here": True,
            "R1R2_primitive_away_from_two_here": True,
            "two_k_allocations_structurally_coupled_here": True,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl575",
        "object_layer": "m2_scaled_Gaussian_rotation_between_source_pairs",
        "input_checkpoint": {"work_log": "wl574", "ready": _wl574_ready(wl574)},
        "rotation_certificate": {
            "forward": ["R1*C=P*A-2*K*B", "R1*D=2*K*A+P*B"],
            "inverse": ["R2*A=P*C+2*K*D", "R2*B=-2*K*C+P*D"],
            "norm": "P^2+4*K^2=R1*R2",
            "pair_norm": "R1*(C^2+D^2)=R2*(A^2+B^2)",
            "gcd_PK": "1 if a odd; 4 if a even",
            "gcd_R1_R2": "1 if a odd; 4 if a even",
        },
        "symbolic_certificate": symbolic,
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
            "results/closure_quotient_rank_zero_aa_bb_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
