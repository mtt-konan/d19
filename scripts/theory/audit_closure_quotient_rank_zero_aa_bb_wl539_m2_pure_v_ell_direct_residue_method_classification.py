#!/usr/bin/env python3
"""Classify the direct single-prime residue obstruction used after wl535."""

from __future__ import annotations

import argparse
import importlib
import math
from pathlib import Path
from typing import Any

try:
    wl538_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl538_m2_pure_v_ell_mod_19_local_obstruction"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl538_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl538_m2_pure_v_ell_mod_19_local_obstruction"
    )
    from json_io import write_json


BOUND = 1907
EXPECTED_EXCLUDING_PAIRS = [(7, 5), (11, 10), (19, 15), (23, 5)]


def _wl538_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl538"
        and proof.get("local_prime_19_integrality_obstruction_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def _primes_below(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * limit
    sieve[:2] = b"\x00\x00"
    for n in range(2, math.isqrt(limit - 1) + 1):
        if sieve[n]:
            sieve[n * n : limit : n] = b"\x00" * (((limit - 1 - n * n) // n) + 1)
    return [n for n in range(limit) if sieve[n]]


def _g_mod(e: int, r: int, p: int) -> int:
    return (
        r**4
        + (16 - 8 * e) * r**3
        + (32 * e * e - 96 * e + 72) * r**2
        + (32 * e - 64) * r
        + 16
    ) % p


def _excluding_residues(p: int) -> list[int]:
    squares = {x * x % p for x in range(p)}
    excluded: list[int] = []
    for e in range(1, p):
        survives = any(
            (e - r) % p in squares
            and (e * r + 4) % p in squares
            and _g_mod(e, r, p) in squares
            for r in squares
        )
        if not survives:
            excluded.append(e)
    return excluded


def _finite_classification() -> dict[str, Any]:
    primes = [p for p in _primes_below(BOUND) if p % 4 == 3]
    rows = [
        {"auxiliary_prime": p, "excluding_parameter_residues": _excluding_residues(p)}
        for p in primes
    ]
    pairs = [
        (row["auxiliary_prime"], e)
        for row in rows
        for e in row["excluding_parameter_residues"]
    ]
    return {
        "bound_exclusive": BOUND,
        "checked_auxiliary_prime_count": len(primes),
        "rows_with_exclusions": [row for row in rows if row["excluding_parameter_residues"]],
        "excluding_pairs": pairs,
        "matches_expected_complete_list": pairs == EXPECTED_EXCLUDING_PAIRS,
    }


def build_wl539_m2_pure_v_ell_direct_residue_method_classification() -> dict[str, Any]:
    wl538 = wl538_module.build_wl538_m2_pure_v_ell_mod_19_local_obstruction()
    finite = _finite_classification()
    threshold_value = (BOUND - 41 * math.sqrt(BOUND)) / 16
    violations: list[str] = []
    if not _wl538_ready(wl538):
        violations.append("wl538_input_not_ready")
    if threshold_value <= 7:
        violations.append("large_prime_survivor_bound_not_strict")
    if finite["matches_expected_complete_list"] is not True:
        violations.append("finite_residue_classification_mismatch")
    ready = not violations
    proof_status = (
        {
            "direct_single_prime_good_reduction_method_classified_here": True,
            "only_auxiliary_primes_7_11_19_23_exclude_residues": True,
            "new_prime_class_ell_eq_5_mod_92_excluded_here": True,
            "method_exhausted_outside_four_pairs": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl539",
        "object_layer": "m2_direct_good_reduction_residue_method_classification_inside_wl535",
        "input_checkpoint": {"work_log": "wl538", "ready": _wl538_ready(wl538)},
        "large_prime_argument": {
            "factor_degrees": [1, 1, 1, 4],
            "total_weil_error_coefficient": 41,
            "maximum_zero_residue_contribution": 7,
            "first_relevant_prime_with_strict_bound": BOUND,
            "weighted_lower_bound_at_threshold": threshold_value,
            "strictly_greater_than_zero_contribution_bound": threshold_value > 7,
            "G_discriminant": "2^26*(e-2)^2*(e-1)^4*(e^2-2*e+2)",
            "degenerate_square_cases": {
                1: "(R^2+4*R-4)^2",
                2: "(R^2+4)^2",
            },
        },
        "finite_classification": finite,
        "new_local_obstruction": {
            "auxiliary_prime": 23,
            "parameter_residue_mod_23": 5,
            "prime_class_mod_92": 5,
            "infinite_prime_subfamily_reason": (
                "gcd(5,92)=1, so Dirichlet's theorem gives infinitely many primes "
                "ell congruent to 5 mod 92."
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
            "results/closure_quotient_rank_zero_aa_bb_wl539_m2_pure_v_ell_direct_residue_method_classification.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl539_m2_pure_v_ell_direct_residue_method_classification()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    print(f"excluding_pairs={payload['finite_classification']['excluding_pairs']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
