#!/usr/bin/env python3
"""Audit generic-cover denominator coupling forced by integral ell."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl572_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl572_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality"
    )
    from json_io import write_json


def _wl572_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl572"
        and proof.get("tau_half_excluded_for_odd_prime_parameter_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    a, b, m, n = sp.symbols("a b m n", integer=True)
    delta = m**2 + 2 * m * n - n**2
    h = (
        a**4 * m * n
        + 2 * a**2 * b**2 * m**2
        + 8 * a**2 * b**2 * m * n
        - 2 * a**2 * b**2 * n**2
        - 4 * b**4 * m * n
    )
    k = a**4 + 4 * a**2 * b**2 - 4 * b**4
    return {
        "numerator_mod_a2": sp.rem(h, a**2, a) == -4 * b**4 * m * n,
        "numerator_mod_b2": sp.rem(h, b**2, b) == a**4 * m * n,
        "numerator_mod_delta": sp.factor(sp.rem(h, delta, m) - m * n * k) == 0,
        "delta_resultant": sp.factor(sp.resultant(h, delta, m)) == -n**4 * k**2,
    }


def build_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling() -> dict[str, Any]:
    wl572 = wl572_module.build_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl572_ready(wl572):
        violations.append("wl572_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "q_numerator_square_supports_on_four_mn_here": True,
            "q_denominator_square_supports_on_mn_here": True,
            "Delta_coprime_to_mn_here": True,
            "Delta_divides_positive_quartic_form_here": True,
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
        "work_log": "wl573",
        "object_layer": "m2_generic_cover_integral_denominator_coupling",
        "input_checkpoint": {"work_log": "wl572", "ready": _wl572_ready(wl572)},
        "denominator_certificate": {
            "coordinates": "X=a^2/b^2, tau=m/n",
            "Delta": "m^2+2*m*n-n^2>0",
            "q_numerator": "a^2 divides 4*m*n",
            "q_denominator": "b^2 divides m*n",
            "Delta_coprimality": "gcd(Delta,m*n)=1",
            "Delta_divisibility": "Delta divides a^4+4*a^2*b^2-4*b^4",
            "Delta_dyadic": "v2(Delta)=0 for opposite parity and 1 for both odd",
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
            "results/closure_quotient_rank_zero_aa_bb_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
