#!/usr/bin/env python3
"""Audit exclusion of the exceptional tau=1/2 branch by integrality."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl571_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl571_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus"
    )
    from json_io import write_json


def _wl571_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl571"
        and proof.get("tau_half_unique_genus_drop_to_one_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    a, b = sp.symbols("a b", nonzero=True, integer=True)
    x = a**2 / b**2
    ell = sp.factor(x + 5 - 4 / x)
    numerator, denominator = sp.fraction(ell)
    return {
        "reduced_parameter_formula": sp.expand(
            numerator - (a**4 + 5 * a**2 * b**2 - 4 * b**4)
        )
        == 0
        and denominator == a**2 * b**2,
        "numerator_mod_a2": sp.rem(numerator, a**2, a) == -4 * b**4,
        "numerator_mod_b2": sp.rem(numerator, b**2, b) == a**4,
        "sole_positive_candidate_value": sp.simplify((x + 5 - 4 / x).subs({a: 2, b: 1}))
        == 8,
    }


def build_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality() -> dict[str, Any]:
    wl571 = wl571_module.build_wl571_m2_pure_v_ell_source_square_multiquadratic_cover_genus()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl571_ready(wl571):
        violations.append("wl571_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "integral_parameter_forces_q_denominator_one_here": True,
            "integral_parameter_forces_q_numerator_square_divides_four_here": True,
            "positivity_leaves_only_X_four_here": True,
            "tau_half_excluded_for_odd_prime_parameter_here": True,
            "generic_tau_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl572",
        "object_layer": "m2_exceptional_tau_half_integrality_exclusion",
        "input_checkpoint": {"work_log": "wl571", "ready": _wl571_ready(wl571)},
        "integrality_certificate": {
            "reduced_q": "q=a/b, gcd(a,b)=1, b>0",
            "parameter": "(a^4+5*a^2*b^2-4*b^4)/(a^2*b^2)",
            "mod_a2": "a^2|4*b^4, hence a^2|4",
            "mod_b2": "b^2|a^4, hence b=1",
            "positivity": "X=q^2>1, hence X=4",
            "contradiction": "ell=8 is not an odd prime",
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
            "results/closure_quotient_rank_zero_aa_bb_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl572_m2_pure_v_ell_exclude_tau_half_by_integrality()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
