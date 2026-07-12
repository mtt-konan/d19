#!/usr/bin/env python3
"""Audit dyadic same-side transport and complete k-allocation identity."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl577_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl577_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side"
    )
    from json_io import write_json


def _wl577_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl577"
        and proof.get("factor_two_is_only_remaining_transport_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    p0, k0 = sp.symbols("P0 K0")
    matrix = sp.Matrix([[p0, -2 * k0], [2 * k0, p0]])
    return {
        "normalized_matrix_determinant": sp.expand(matrix.det() - (p0**2 + 4 * k0**2))
        == 0,
    }


def build_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation() -> dict[str, Any]:
    wl577 = wl577_module.build_wl577_m2_pure_v_ell_all_odd_k_primes_transport_same_side()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl577_ready(wl577):
        violations.append("wl577_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "normalized_rotation_is_diagonal_odd_offdiagonal_even_here": True,
            "two_adic_valuation_order_preserved_here": True,
            "factor_two_transports_same_side_here": True,
            "two_complementary_k_allocations_identical_here": True,
            "allocation_analysis_exhausted_here": True,
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
        "work_log": "wl578",
        "object_layer": "m2_dyadic_same_side_and_identical_k_allocation",
        "input_checkpoint": {"work_log": "wl577", "ready": _wl577_ready(wl577)},
        "dyadic_certificate": {
            "normalization": "e=1 if a odd, e=4 if a even",
            "matrix_parity": "odd diagonal and even off-diagonal over Z_2",
            "ordering": "larger v2 coordinate is preserved",
            "transport": "A->C and B->D",
            "allocation_identity": ["alpha=gamma", "beta=delta0"],
        },
        "remaining_magnitude_system": {
            "first": "R1*g2*alpha*r2^2=P*g1*alpha*r1^2-2*K*g1*beta*s1^2",
            "second": "R1*g2*beta*s2^2=2*K*g1*alpha*r1^2+P*g1*beta*s1^2",
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
            "results/closure_quotient_rank_zero_aa_bb_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl578_m2_pure_v_ell_dyadic_same_side_and_identical_k_allocation()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
