#!/usr/bin/env python3
"""Audit odd-prime side transport under the scaled Gaussian rotation."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl575_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl575_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs"
    )
    from json_io import write_json


def _wl575_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl575"
        and proof.get("two_k_allocations_structurally_coupled_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    a, b, m, n = sp.symbols("a b m n", integer=True)
    first = a**2 * m + 2 * a**2 * n - 2 * b**2 * n
    second = a**2 * n + 2 * b**2 * m - 2 * a**2 * m
    third = a**2 * m + 4 * b**2 * m - 2 * b**2 * n
    fourth = a**2 * n + 2 * b**2 * m + 4 * b**2 * n
    p_form = a**4 + 4 * b**4
    k_form = a**4 + 4 * a**2 * b**2 - 4 * b**4
    return {
        "AC_cross_resultant": sp.factor(sp.resultant(first, third, m)) == -2 * n * k_form,
        "AD_cross_resultant": sp.expand(sp.resultant(first, fourth, m) - n * p_form) == 0,
        "BC_cross_resultant": sp.expand(sp.resultant(second, third, m) + n * p_form) == 0,
        "BD_cross_resultant": sp.factor(sp.resultant(second, fourth, m)) == -2 * n * k_form,
        "Delta_discriminant": sp.discriminant(m**2 + 2 * m * n - n**2, m) == 8 * n**2,
    }


def build_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation() -> dict[str, Any]:
    wl575 = wl575_module.build_wl575_m2_pure_v_ell_scaled_gaussian_rotation_between_source_pairs()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl575_ready(wl575):
        violations.append("wl575_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "odd_k_primes_force_two_quadratic_residue_here": True,
            "regular_same_side_transport_by_K_here": True,
            "regular_crossed_side_transport_by_P_here": True,
            "R1_singular_pair_vanishes_together_here": True,
            "R2_singular_pair_vanishes_together_here": True,
            "singular_side_requires_higher_valuation_here": True,
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
        "work_log": "wl576",
        "object_layer": "m2_odd_prime_side_transport_under_scaled_rotation",
        "input_checkpoint": {"work_log": "wl575", "ready": _wl575_ready(wl575)},
        "transport_certificate": {
            "odd_k_prime_class": "Legendre(2,p)=1, p congruent 1 or 7 mod 8",
            "regular_K": "same side: A->C, B->D",
            "regular_P": "crossed side: A->D, B->C",
            "R1_singular": "p divides A and B; exactly one of C,D",
            "R2_singular": "p divides C and D; exactly one of A,B",
            "remaining_data": "larger normalized valuation in the singular pair",
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
            "results/closure_quotient_rank_zero_aa_bb_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl576_m2_pure_v_ell_odd_prime_side_transport_under_rotation()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
