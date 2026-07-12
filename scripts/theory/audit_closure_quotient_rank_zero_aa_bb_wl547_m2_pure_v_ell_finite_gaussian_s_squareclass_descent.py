#!/usr/bin/env python3
"""Audit the finite Gaussian S-squareclass descent for the G square."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl546_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl546_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent"
    )
    from json_io import write_json


def _wl546_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl546"
        and proof.get("Gaussian_square_equation_eliminated_exactly_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_support_certificate() -> dict[str, Any]:
    ell, q, d, t, q2 = sp.symbols("ell Q D t Q2")
    p_form = -q**4 + (8 * ell - 12) * q**2 * d**2 + 4 * d**4
    r_form = q**4 + 4 * q**2 * d**2 - 4 * d**4
    sum_identity = sp.factor(p_form + r_form)
    p_in_q2 = -q2**2 + (8 * ell - 12) * q2 * d**2 + 4 * d**4
    reduced_in_t = sp.factor(p_in_q2.subs({ell: 1, q2: t * d**2}) / d**4)
    root_polynomial = t**2 + 4 * t - 4
    return {
        "P_plus_R": str(sum_identity),
        "P_plus_R_identity_verified": sum_identity == 8 * q**2 * d**2 * (ell - 1),
        "ell_eq_1_root_polynomial_verified": sp.factor(reduced_in_t + root_polynomial)
        == 0,
        "root_polynomial": "t^2+4*t-4",
        "root_discriminant": int(sp.discriminant(root_polynomial, t)),
        "root_discriminant_equals_32": sp.discriminant(root_polynomial, t) == 32,
    }


def build_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent() -> dict[str, Any]:
    wl546 = wl546_module.build_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent()
    symbolic = _symbolic_support_certificate()
    violations: list[str] = []
    if not _wl546_ready(wl546):
        violations.append("wl546_input_not_ready")
    for key in (
        "P_plus_R_identity_verified",
        "ell_eq_1_root_polynomial_verified",
        "root_discriminant_equals_32",
    ):
        if symbolic[key] is not True:
            violations.append(f"symbolic_support_failed:{key}")
    ready = not violations
    proof_status = (
        {
            "G_square_rewritten_as_Gaussian_norm_square_here": True,
            "common_odd_prime_support_bounded_by_ell_minus_1_here": True,
            "common_odd_primes_require_Legendre_2_eq_1_here": True,
            "G_square_reduced_to_finite_S_squareclasses_here": True,
            "theorem_level_Selmer_object_claimed_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl547",
        "object_layer": "m2_finite_Gaussian_S_squareclass_descent_for_G_inside_wl546",
        "input_checkpoint": {"work_log": "wl546", "ready": _wl546_ready(wl546)},
        "Gaussian_norm": {
            "P": "-Q^4+(8*ell-12)*Q^2*D^2+4*D^4",
            "R": "Q^4+4*Q^2*D^2-4*D^4",
            "delta": "(P+iR)/(1+i)",
            "norm_delta": "W^2",
        },
        "finite_support": {
            "dyadic_prime": "1+i",
            "odd_rational_primes": "p|ell-1 with Legendre(2/p)=1",
            "candidate_root_condition": "(Q^2/D^2)^2+4*(Q^2/D^2)-4=0 mod p",
            "outside_support_Gaussian_valuations_are_even": True,
        },
        "squareclass_equation": {
            "equation": "delta=eta*d*gamma^2",
            "Gaussian_unit_class_count": 2,
            "d_is_squarefree": True,
            "d_supported_on_finite_S_ell": True,
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
            "results/closure_quotient_rank_zero_aa_bb_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl547_m2_pure_v_ell_finite_gaussian_s_squareclass_descent()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
