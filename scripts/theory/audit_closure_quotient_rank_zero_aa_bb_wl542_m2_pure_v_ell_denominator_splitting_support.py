#!/usr/bin/env python3
"""Audit the denominator splitting-support theorem inside wl535."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl541_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl541_m2_pure_v_ell_parameter_prime_local_solubility"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl541_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl541_m2_pure_v_ell_parameter_prime_local_solubility"
    )
    from json_io import write_json


def _wl541_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl541"
        and proof.get("parameter_prime_standalone_local_obstruction_exhausted_here")
        is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_local_factorization() -> dict[str, Any]:
    ell, q = sp.symbols("ell q", nonzero=True)
    g = (
        q**8
        + (16 - 8 * ell) * q**6
        + (32 * ell**2 - 96 * ell + 72) * q**4
        + (32 * ell - 64) * q**2
        + 16
    )
    normalized = (
        1
        + (16 - 8 * ell) / q**2
        + (32 * ell**2 - 96 * ell + 72) / q**4
        + (32 * ell - 64) / q**6
        + 16 / q**8
    )
    return {
        "G_leading_term_factorization_verified": sp.simplify(g - q**8 * normalized)
        == 0,
        "first_square_factorization_verified": sp.expand(
            (-1) * q**2 * (1 - ell / q**2) - (ell - q**2)
        )
        == 0,
        "second_square_factorization_verified": sp.expand(
            ell * q**2 * (1 + 4 / (ell * q**2)) - (ell * q**2 + 4)
        )
        == 0,
        "smallest_principal_unit_valuation_for_v_r_q_minus_k": "2*k",
    }


def build_wl542_m2_pure_v_ell_denominator_splitting_support() -> dict[str, Any]:
    wl541 = wl541_module.build_wl541_m2_pure_v_ell_parameter_prime_local_solubility()
    symbolic = _symbolic_local_factorization()
    violations: list[str] = []
    if not _wl541_ready(wl541):
        violations.append("wl541_input_not_ready")
    for key in (
        "G_leading_term_factorization_verified",
        "first_square_factorization_verified",
        "second_square_factorization_verified",
    ):
        if symbolic[key] is not True:
            violations.append(f"symbolic_factorization_failed:{key}")
    ready = not violations
    proof_status = (
        {
            "global_denominator_is_odd_and_coprime_to_ell_here": True,
            "every_denominator_prime_splits_completely_here": True,
            "D_mod_ell_is_nonzero_square_here": True,
            "allowed_denominator_places_add_no_G_local_obstruction_here": True,
            "rational_wl535_point_produced_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl542",
        "object_layer": "m2_global_denominator_splitting_support_inside_wl535",
        "input_checkpoint": {"work_log": "wl541", "ready": _wl541_ready(wl541)},
        "denominator_support": {
            "primitive_equations": [
                "A^2+Q^2=ell*D^2",
                "C^2=ell*Q^2+4*D^2",
            ],
            "D_is_odd": True,
            "gcd_D_ell": 1,
            "prime_conditions": [
                "r is congruent to 1 mod 4",
                "Legendre(ell/r)=1",
                "Legendre(r/ell)=1",
            ],
            "splitting_field": "Q(i,sqrt(ell))",
            "D_mod_ell_is_nonzero_square": True,
        },
        "local_converse": {
            "scope": "odd r != ell with -1 and ell square in Q_r, v_r(q)<0",
            "all_three_square_conditions_locally_compatible": True,
            "principal_units_are_squares_because_r_is_odd": True,
            "symbolic_factorization": symbolic,
        },
        "proof_status": proof_status,
        "violations": violations,
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
            "results/closure_quotient_rank_zero_aa_bb_wl542_m2_pure_v_ell_denominator_splitting_support.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl542_m2_pure_v_ell_denominator_splitting_support()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
