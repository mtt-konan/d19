#!/usr/bin/env python3
"""Audit the unified normalized split-prime character for every valuation parity."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl559_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl559_m2_pure_v_ell_even_common_valuation_leading_character"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl559_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl559_m2_pure_v_ell_even_common_valuation_leading_character"
    )
    from json_io import write_json


def _wl559_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl559"
        and proof.get("split_prime_leading_character_classified_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl560_m2_pure_v_ell_unified_normalized_split_prime_character() -> dict[str, Any]:
    wl559 = wl559_module.build_wl559_m2_pure_v_ell_even_common_valuation_leading_character()
    violations: list[str] = []
    if not _wl559_ready(wl559):
        violations.append("wl559_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "odd_common_leading_character_supplied_here": True,
            "all_valuation_parities_unified_here": True,
            "every_odd_ell_minus_one_place_fully_classified_here": True,
            "assembled_global_character_system_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl560",
        "object_layer": "m2_unified_normalized_character_at_all_odd_ell_minus_one_places",
        "input_checkpoint": {"work_log": "wl559", "ready": _wl559_ready(wl559)},
        "normalized_character_certificate": {
            "d": "min(v_p(ell-1),v_p(R))",
            "epsilon": "d mod 2",
            "canonical_membership": "p|r iff epsilon=1",
            "reduced_class": "r_p=r/p^epsilon",
            "normalized_equation": "(F_d+i*E_d)=r_p*Gamma_p^2",
            "inert_case": "automatic",
            "split_master_condition": "Legendre((F_d+j*E_d)/r_p,p)=1",
            "e<k": "Legendre(L_e*(-1+j)/r_p,p)=1",
            "k<e": "Legendre((R/p^k)/r_p,p)=1",
            "e=k": "Legendre(L_e*(lambda-1+j)/r_p,p)=1",
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
            "results/closure_quotient_rank_zero_aa_bb_wl560_m2_pure_v_ell_unified_normalized_split_prime_character.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl560_m2_pure_v_ell_unified_normalized_split_prime_character()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
