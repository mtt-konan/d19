#!/usr/bin/env python3
"""Audit the exact mod-19 local obstruction inside wl535."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl537_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl537_m2_pure_v_ell_mod_11_local_obstruction"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl537_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl537_m2_pure_v_ell_mod_11_local_obstruction"
    )
    from json_io import write_json


def _wl537_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl537"
        and proof.get("local_prime_11_integrality_obstruction_proved_here") is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and payload.get("advance_to_m3") is False
    )


def _square_residues(modulus: int) -> list[int]:
    return sorted({x * x % modulus for x in range(modulus)})


def _g_mod_19_for_ell_15(r: int) -> int:
    return (r**4 + 10 * r**3 + 18 * r**2 + 17 * r + 16) % 19


def _local_obstruction_data() -> dict[str, Any]:
    squares = _square_residues(19)
    cases: list[dict[str, Any]] = []
    for r in squares:
        values = ((15 - r) % 19, (15 * r + 4) % 19, _g_mod_19_for_ell_15(r))
        labels = (
            "ell-q^2 is a nonsquare mod 19",
            "ell*q^2+4 is a nonsquare mod 19",
            "G_ell(q^2) is a nonsquare mod 19",
        )
        failures = [
            label
            for value, label in zip(values, labels, strict=True)
            if value not in squares
        ]
        cases.append(
            {
                "q_square_mod_19": r,
                "ell_minus_q_square_mod_19": values[0],
                "ell_q_square_plus_4_mod_19": values[1],
                "G_ell_q_square_mod_19": values[2],
                "failure_reasons": failures,
                "survives_all_mod_19_square_conditions": not failures,
            }
        )
    survivors = [
        case["q_square_mod_19"]
        for case in cases
        if case["survives_all_mod_19_square_conditions"]
    ]
    return {
        "local_prime": 19,
        "target_ell_residue_mod_19": 15,
        "square_residues_mod_19": squares,
        "g_ell_mod_19_specialization": (
            "G_ell(Q) ≡ Q^4 + 10*Q^3 + 18*Q^2 + 17*Q + 16 (mod 19)"
        ),
        "minus_one_is_nonsquare_mod_19": True,
        "q_square_residue_cases": cases,
        "surviving_q_square_residues_mod_19": survivors,
        "obstruction_proved": survivors == [],
    }


def build_wl538_m2_pure_v_ell_mod_19_local_obstruction() -> dict[str, Any]:
    wl537 = wl537_module.build_wl537_m2_pure_v_ell_mod_11_local_obstruction()
    local = _local_obstruction_data()
    violations: list[str] = []
    if not _wl537_ready(wl537):
        violations.append("wl537_input_not_ready")
    if local["obstruction_proved"] is not True:
        violations.append("mod_19_local_obstruction_not_complete")
    ready = not violations
    proof_status = (
        {
            "wl535_residue_class_ell_eq_15_mod_19_excluded_here": True,
            "local_prime_19_integrality_obstruction_proved_here": True,
            "equivalent_prime_class_ell_eq_53_mod_76": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "strict_counterexample_found_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl538",
        "object_layer": "m2_q_root_coordinate_mod_19_local_obstruction_inside_wl535",
        "input_checkpoint": {"work_log": "wl537", "ready": _wl537_ready(wl537)},
        "local_obstruction": {
            "statement": (
                "For odd prime ell congruent to 1 mod 4 and 15 mod 19, the exact "
                "wl535 rational system has no solution."
            ),
            "mod_19_case_table": local,
            "removed_prime_class_mod_76": 53,
            "infinite_prime_subfamily_reason": (
                "gcd(53,76)=1, so Dirichlet's theorem gives infinitely many primes "
                "ell congruent to 53 mod 76."
            ),
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
            "results/closure_quotient_rank_zero_aa_bb_wl538_m2_pure_v_ell_mod_19_local_obstruction.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl538_m2_pure_v_ell_mod_19_local_obstruction()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
