#!/usr/bin/env python3
"""Audit the exact mod-11 local obstruction inside wl535."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl536_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl536_m2_pure_v_ell_mod_7_local_obstruction"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl536_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl536_m2_pure_v_ell_mod_7_local_obstruction"
    )
    from json_io import write_json


BOUNDARY = (
    "This proves only the direct 11-adic obstruction ell congruent to 10 mod 11 "
    "inside the exact wl535 system, equivalently the infinite prime class ell "
    "congruent to 21 mod 44. It does not solve the complementary classes, prove "
    "a complete Selmer bound, or enter M3."
)


def _wl536_ready(wl536: dict[str, Any]) -> bool:
    proof = wl536.get("proof_status", {})
    return (
        wl536.get("status") == "ok"
        and wl536.get("ready") is True
        and wl536.get("work_log") == "wl536"
        and proof.get("wl535_residue_class_ell_eq_5_mod_7_excluded_here") is True
        and proof.get("uniform_full_wl535_obstruction_proved_here") is False
        and wl536.get("advance_to_m3") is False
    )


def _square_residues(modulus: int) -> list[int]:
    return sorted({(x * x) % modulus for x in range(modulus)})


def _g_mod_11_for_ell_10(q_square: int) -> int:
    r = q_square % 11
    return (r**4 + 2 * r**3 + 2 * r**2 + 3 * r + 5) % 11


def _local_obstruction_data() -> dict[str, Any]:
    squares = _square_residues(11)
    entries: list[dict[str, Any]] = []
    for r in squares:
        ell_minus = (10 - r) % 11
        ell_q_plus_4 = (10 * r + 4) % 11
        g_value = _g_mod_11_for_ell_10(r)
        failures: list[str] = []
        if ell_minus not in squares:
            failures.append("ell-q^2 is a nonsquare mod 11")
        if ell_q_plus_4 not in squares:
            failures.append("ell*q^2+4 is a nonsquare mod 11")
        if g_value not in squares:
            failures.append("G_ell(q^2) is a nonsquare mod 11")
        entries.append(
            {
                "q_square_mod_11": r,
                "ell_minus_q_square_mod_11": ell_minus,
                "ell_q_square_plus_4_mod_11": ell_q_plus_4,
                "G_ell_q_square_mod_11": g_value,
                "failure_reasons": failures,
                "survives_all_mod_11_square_conditions": not failures,
            }
        )
    survivors = [
        entry["q_square_mod_11"]
        for entry in entries
        if entry["survives_all_mod_11_square_conditions"]
    ]
    return {
        "local_prime": 11,
        "target_ell_residue_mod_11": 10,
        "square_residues_mod_11": squares,
        "g_ell_mod_11_specialization": (
            "G_ell(Q) ≡ Q^4 + 2*Q^3 + 2*Q^2 + 3*Q + 5 (mod 11)"
        ),
        "integrality_lemma": {
            "minus_one_is_nonsquare_mod_11": True,
            "statement": (
                "If 11 does not divide ell and p^2+q^2=ell with p,q rational, "
                "then p and q are 11-adic integers."
            ),
        },
        "q_square_residue_cases": entries,
        "surviving_q_square_residues_mod_11": survivors,
        "obstruction_proved": survivors == [],
    }


def build_wl537_m2_pure_v_ell_mod_11_local_obstruction() -> dict[str, Any]:
    wl536 = wl536_module.build_wl536_m2_pure_v_ell_mod_7_local_obstruction()
    local = _local_obstruction_data()
    violations: list[str] = []
    if not _wl536_ready(wl536):
        violations.append("wl536_input_not_ready")
    if local["obstruction_proved"] is not True:
        violations.append("mod_11_local_obstruction_not_complete")
    ready = not violations
    proof_status = (
        {
            "wl535_residue_class_ell_eq_10_mod_11_excluded_here": True,
            "local_prime_11_integrality_obstruction_proved_here": True,
            "equivalent_prime_class_ell_eq_21_mod_44": True,
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
        "work_log": "wl537",
        "object_layer": "m2_q_root_coordinate_mod_11_local_obstruction_inside_wl535",
        "input_checkpoint": {"work_log": "wl536", "ready": _wl536_ready(wl536)},
        "local_obstruction": {
            "statement": (
                "If ell is an odd prime with ell ≡ 1 mod 4 and ell ≡ 10 mod 11, "
                "then the exact wl535 rational system has no solution."
            ),
            "mod_11_case_table": local,
            "removed_prime_class_mod_44": 21,
            "infinite_prime_subfamily_reason": (
                "gcd(21,44)=1, so Dirichlet's theorem gives infinitely many primes "
                "ell congruent to 21 mod 44."
            ),
        },
        "proof_status": proof_status,
        "violations": violations,
        "boundary": BOUNDARY,
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
            "results/closure_quotient_rank_zero_aa_bb_wl537_m2_pure_v_ell_mod_11_local_obstruction.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl537_m2_pure_v_ell_mod_11_local_obstruction()
    write_json(args.out, payload)
    print(f"wrote wl537 mod-11 local-obstruction audit to {args.out}")
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
