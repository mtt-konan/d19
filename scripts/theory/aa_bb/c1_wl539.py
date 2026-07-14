#!/usr/bin/env python3
"""Canonical C1 wl539 kernel without legacy runtime dependencies."""

from __future__ import annotations

import math
from itertools import combinations
from typing import Any

import sympy as sp

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
        r**4 + (16 - 8 * e) * r**3 + (32 * e * e - 96 * e + 72) * r**2 + (32 * e - 64) * r + 16
    ) % p


def _excluding_residues(p: int) -> list[int]:
    squares = {x * x % p for x in range(p)}
    excluded: list[int] = []
    for e in range(1, p):
        survives = any(
            (e - r) % p in squares and (e * r + 4) % p in squares and _g_mod(e, r, p) in squares
            for r in squares
        )
        if not survives:
            excluded.append(e)
    return excluded


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def _large_prime_certificate() -> dict[str, Any]:
    r, e = sp.symbols("R e")
    factors = [
        r,
        e - r,
        e * r + 4,
        r**4 + (16 - 8 * e) * r**3 + (32 * e**2 - 96 * e + 72) * r**2 + (32 * e - 64) * r + 16,
    ]
    degrees = [int(sp.degree(factor, r)) for factor in factors]
    error_coefficient = sum(
        sum(degrees[index] for index in subset) - 1
        for size in range(1, len(factors) + 1)
        for subset in combinations(range(len(factors)), size)
    )
    discriminant = sp.factor(sp.discriminant(factors[-1], r))
    expected_discriminant = 2**26 * (e - 2) ** 2 * (e - 1) ** 4 * (e**2 - 2 * e + 2)
    degenerate_checks = {
        1: sp.factor(factors[-1].subs(e, 1) - (r**2 + 4 * r - 4) ** 2) == 0,
        2: sp.factor(factors[-1].subs(e, 2) - (r**2 + 4) ** 2) == 0,
    }
    common_expression = 5 * e**2 - 8 * e + 4
    resultant_checks = [
        sp.factor(sp.resultant(factors[0], factors[1], r) - e) == 0,
        sp.factor(sp.resultant(factors[0], factors[2], r) - 4) == 0,
        sp.factor(sp.resultant(factors[1], factors[2], r) + e**2 + 4) == 0,
        sp.factor(factors[-1].subs(r, 0) - 16) == 0,
        sp.factor(factors[-1].subs(r, e) - common_expression**2) == 0,
        sp.factor(e**4 * factors[-1].subs(r, -4 / e) - 16 * common_expression**2) == 0,
        sp.discriminant(common_expression, e) == -16,
        sp.discriminant(e**2 - 2 * e + 2, e) == -4,
    ]

    def bound_is_strict(prime: int) -> bool:
        return (prime - error_coefficient * math.sqrt(prime)) / 16 > sum(degrees)

    first_relevant_prime = next(
        prime
        for prime in range(3, BOUND + 1)
        if prime % 4 == 3 and _is_prime(prime) and bound_is_strict(prime)
    )
    return {
        "factor_degrees": degrees,
        "total_weil_error_coefficient": error_coefficient,
        "maximum_zero_residue_contribution": sum(degrees),
        "first_relevant_prime_with_strict_bound": first_relevant_prime,
        "discriminant_verified": sp.factor(discriminant - expected_discriminant) == 0,
        "degenerate_square_cases_verified": all(degenerate_checks.values()),
        "factor_coprimeness_identities_verified": all(resultant_checks),
        "bound_monotone_from_cutoff": 1 - error_coefficient / (2 * math.sqrt(BOUND)) > 0,
    }


def _finite_classification() -> dict[str, Any]:
    primes = [p for p in _primes_below(BOUND) if p % 4 == 3]
    rows = [
        {"auxiliary_prime": p, "excluding_parameter_residues": _excluding_residues(p)}
        for p in primes
    ]
    pairs = [
        (row["auxiliary_prime"], e) for row in rows for e in row["excluding_parameter_residues"]
    ]
    return {
        "bound_exclusive": BOUND,
        "checked_auxiliary_prime_count": len(primes),
        "rows_with_exclusions": [row for row in rows if row["excluding_parameter_residues"]],
        "excluding_pairs": pairs,
        "matches_expected_complete_list": pairs == EXPECTED_EXCLUDING_PAIRS,
    }


def build_wl539(wl538: dict[str, Any]) -> dict[str, Any]:
    finite = _finite_classification()
    large_prime = _large_prime_certificate()
    threshold_value = (BOUND - large_prime["total_weil_error_coefficient"] * math.sqrt(BOUND)) / 16
    violations: list[str] = []
    if not _wl538_ready(wl538):
        violations.append("wl538_input_not_ready")
    if threshold_value <= large_prime["maximum_zero_residue_contribution"]:
        violations.append("large_prime_survivor_bound_not_strict")
    if large_prime["first_relevant_prime_with_strict_bound"] != BOUND:
        violations.append("large_prime_cutoff_mismatch")
    if large_prime["discriminant_verified"] is not True:
        violations.append("G_discriminant_mismatch")
    if large_prime["degenerate_square_cases_verified"] is not True:
        violations.append("degenerate_square_case_mismatch")
    if large_prime["factor_coprimeness_identities_verified"] is not True:
        violations.append("factor_coprimeness_identity_mismatch")
    if large_prime["bound_monotone_from_cutoff"] is not True:
        violations.append("large_prime_bound_not_monotone")
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
            "factor_degrees": large_prime["factor_degrees"],
            "total_weil_error_coefficient": large_prime["total_weil_error_coefficient"],
            "maximum_zero_residue_contribution": large_prime["maximum_zero_residue_contribution"],
            "first_relevant_prime_with_strict_bound": large_prime[
                "first_relevant_prime_with_strict_bound"
            ],
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
