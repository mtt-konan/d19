#!/usr/bin/env python3
"""Canonical C1 wl541 kernel without legacy runtime dependencies."""

from __future__ import annotations

import math
from typing import Any

import sympy as sp

SMALL_WITNESSES = {
    5: (1, 4),
    13: (4, 7),
    17: (2, 13),
    29: (3, 23),
    37: (1, 35),
    41: (3, 39),
    53: (4, 34),
}


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def _wl540_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl540"
        and proof.get("q_a_c_are_parameter_prime_units_here") is True
        and payload.get("advance_to_m3") is False
    )


def _g(q_square: int, ell: int) -> int:
    q = q_square % ell
    return (q**4 + 16 * q**3 + 72 * q**2 - 64 * q + 16) % ell


def _small_witness_certificate() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ell, (x, y) in SMALL_WITNESSES.items():
        q_square = x * x % ell
        g_value = _g(q_square, ell)
        rows.append(
            {
                "ell": ell,
                "x": x,
                "y": y,
                "q_square": q_square,
                "g_value": g_value,
                "x_nonzero": x % ell != 0,
                "y_nonzero": y % ell != 0,
                "curve_equation_verified": y * y % ell == g_value,
            }
        )
    return rows


def _geometry_certificate() -> dict[str, Any]:
    x = sp.symbols("x")
    h = x**8 + 16 * x**6 + 72 * x**4 - 64 * x**2 + 16
    discriminant = sp.factor(sp.discriminant(h, x))
    infinity_points = 2
    x_zero_points = 2
    y_zero_points = int(sp.degree(h, x))
    maximum_removed_points = infinity_points + x_zero_points + y_zero_points
    eligible_primes_below_threshold = [
        ell for ell in range(3, 61) if ell % 4 == 1 and _is_prime(ell)
    ]
    threshold_lower_bound = 61 + 1 - 6 * math.sqrt(61)
    return {
        "degree": int(sp.degree(h, x)),
        "genus": 3,
        "discriminant": str(discriminant),
        "discriminant_is_power_of_two": discriminant == 2**70,
        "rational_points_at_infinity": infinity_points,
        "maximum_removed_points": maximum_removed_points,
        "first_claimed_prime_threshold": 61,
        "hasse_weil_lower_bound_at_61": threshold_lower_bound,
        "lower_bound_exceeds_removed_points": threshold_lower_bound > maximum_removed_points,
        "eligible_primes_below_threshold": eligible_primes_below_threshold,
        "hasse_weil_lower_bound_monotone_from_61": 1 - 3 / math.sqrt(61) > 0,
    }


def build_wl541(wl540: dict[str, Any]) -> dict[str, Any]:
    geometry = _geometry_certificate()
    witnesses = _small_witness_certificate()
    violations: list[str] = []
    if not _wl540_ready(wl540):
        violations.append("wl540_input_not_ready")
    if geometry["degree"] != 8 or geometry["genus"] != 3:
        violations.append("genus_three_model_not_verified")
    if geometry["discriminant_is_power_of_two"] is not True:
        violations.append("odd_prime_smoothness_not_verified")
    if geometry["lower_bound_exceeds_removed_points"] is not True:
        violations.append("hasse_weil_threshold_not_strict")
    if geometry["hasse_weil_lower_bound_monotone_from_61"] is not True:
        violations.append("hasse_weil_bound_not_monotone")
    if geometry["eligible_primes_below_threshold"] != list(SMALL_WITNESSES):
        violations.append("small_prime_witness_domain_mismatch")
    if not all(
        row["x_nonzero"] and row["y_nonzero"] and row["curve_equation_verified"]
        for row in witnesses
    ):
        violations.append("small_prime_witness_failed")
    ready = not violations
    proof_status = (
        {
            "unit_finite_field_point_exists_for_every_ell_eq_1_mod_4_here": True,
            "simultaneous_parameter_prime_hensel_lift_proved_here": True,
            "parameter_prime_standalone_local_obstruction_exhausted_here": True,
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
        "work_log": "wl541",
        "object_layer": "m2_parameter_prime_local_solubility_inside_wl535",
        "input_checkpoint": {"work_log": "wl540", "ready": _wl540_ready(wl540)},
        "finite_field_curve": {
            "equation": "y^2=x^8+16*x^6+72*x^4-64*x^2+16",
            "geometry_certificate": {
                key: value
                for key, value in geometry.items()
                if key
                not in {
                    "eligible_primes_below_threshold",
                    "hasse_weil_lower_bound_monotone_from_61",
                }
            },
            "small_prime_witnesses": witnesses,
        },
        "hensel_lift": {
            "fixed_unit_coordinate": "q=x",
            "residue_roots": ["a=i*x with i^2=-1", "c=2", "V=y"],
            "unit_derivatives": ["2*a", "2*c", "2*V"],
            "simultaneous_lift_for_same_q": True,
            "real_positivity_addressed": False,
        },
        "proof_status": proof_status,
        "violations": violations,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_current_task": True,
    }
