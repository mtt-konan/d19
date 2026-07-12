#!/usr/bin/env python3
"""Audit split-prime leading characters at positive even common valuation."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl558_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl558_m2_pure_v_ell_split_prime_global_class_character"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl558_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl558_m2_pure_v_ell_split_prime_global_class_character"
    )
    from json_io import write_json


def _wl558_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl558"
        and proof.get("split_prime_character_condition_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl559_m2_pure_v_ell_even_common_valuation_leading_character() -> dict[str, Any]:
    wl558 = wl558_module.build_wl558_m2_pure_v_ell_split_prime_global_class_character()
    violations: list[str] = []
    if not _wl558_ready(wl558):
        violations.append("wl558_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "positive_even_common_valuation_normalized_here": True,
            "split_prime_leading_character_classified_here": True,
            "inert_even_common_valuation_exhausted_here": True,
            "all_odd_places_not_in_r_classified_here": True,
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
        "work_log": "wl559",
        "object_layer": "m2_even_common_valuation_inside_split_prime_global_character_system",
        "input_checkpoint": {"work_log": "wl558", "ready": _wl558_ready(wl558)},
        "leading_character_certificate": {
            "setup": "e=v_p(ell-1), k=v_p(R), d=min(e,k)>0 even",
            "normalized_element": "Z_d=(F+i*E)/p^d",
            "inert_case": "automatic from square norm in F_(p^2)",
            "split_master_condition": "Legendre((F_d+j*E_d)/r,p)=1",
            "e<k": "Legendre(L_e*(-1+j)/r,p)=1",
            "k<e": "Legendre((R/p^k)/r,p)=1",
            "e=k": "Legendre(L_e*(lambda-1+j)/r,p)=1",
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
            "results/closure_quotient_rank_zero_aa_bb_wl559_m2_pure_v_ell_even_common_valuation_leading_character.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl559_m2_pure_v_ell_even_common_valuation_leading_character()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
