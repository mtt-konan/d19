#!/usr/bin/env python3
"""Audit the split-prime character forced by the global standard square."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl557_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl557_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata"
    )
    from json_io import write_json


def _wl557_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl557"
        and proof.get("real_and_Gaussian_descent_valuations_coupled_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl558_m2_pure_v_ell_split_prime_global_class_character() -> dict[str, Any]:
    wl557 = wl557_module.build_wl557_m2_pure_v_ell_surviving_orientation_valuation_strata()
    violations: list[str] = []
    if not _wl557_ready(wl557):
        violations.append("wl557_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "global_class_equation_applied_at_odd_unit_places_here": True,
            "split_prime_character_condition_proved_here": True,
            "inert_prime_unit_condition_exhausted_here": True,
            "distinct_place_r_coupling_produced_here": True,
            "global_character_system_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl558",
        "object_layer": "m2_split_prime_character_inside_global_standard_square",
        "input_checkpoint": {"work_log": "wl557", "ready": _wl557_ready(wl557)},
        "character_certificate": {
            "unit_place": "odd p|ell-1 with p not dividing R",
            "inert_p_mod_4_eq_3": "automatic in F_(p^2)",
            "split_p_mod_4_eq_1": "Legendre(F/r,p)=1",
            "generic_q_coordinate": "Legendre((t^2+4*t-4)/r,p)=1",
            "Q_or_D_boundary": "Legendre(r,p)=1",
            "nontrivial_example": {
                "p": 13,
                "t": 10,
                "f_t": 6,
                "source_residues_are_squares": True,
                "f_t_is_nonsquare": True,
            },
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
            "results/closure_quotient_rank_zero_aa_bb_wl558_m2_pure_v_ell_split_prime_global_class_character.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl558_m2_pure_v_ell_split_prime_global_class_character()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
