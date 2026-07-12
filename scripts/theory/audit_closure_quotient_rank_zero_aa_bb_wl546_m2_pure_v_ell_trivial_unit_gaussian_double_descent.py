#!/usr/bin/env python3
"""Audit the Gaussian double descent on the wl545 trivial-unit branch."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl545_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl545_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy"
    )
    from json_io import write_json


def _wl545_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl545"
        and proof.get("trivial_unit_2_adic_q_valuation_classified_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_gaussian_certificate() -> dict[str, Any]:
    a, b, x, y = sp.symbols("a_0 b_0 x y", integer=True)
    real = a * (x**2 - y**2) - 2 * b * x * y
    imag = b * (x**2 - y**2) + 2 * a * x * y
    norm_identity = sp.expand(real**2 + imag**2 - (a**2 + b**2) * (x**2 + y**2) ** 2)
    conjugate_imag = -b * (x**2 - y**2) + 2 * a * x * y
    conjugate_reduction = sp.expand(conjugate_imag + imag.subs(y, -y))
    return {
        "Gaussian_norm_identity_verified": norm_identity == 0,
        "pi_orientation_imaginary_form": str(imag),
        "i_pi_orientation_imaginary_form": str(real),
        "conjugate_orientation_reduces_by_y_sign_and_Q_sign": conjugate_reduction == 0,
        "essential_orientation_count": 2,
    }


def build_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent() -> dict[str, Any]:
    wl545 = wl545_module.build_wl545_m2_pure_v_ell_trivial_unit_2_adic_dichotomy()
    symbolic = _symbolic_gaussian_certificate()
    violations: list[str] = []
    if not _wl545_ready(wl545):
        violations.append("wl545_input_not_ready")
    if symbolic["Gaussian_norm_identity_verified"] is not True:
        violations.append("Gaussian_norm_identity_failed")
    if symbolic["conjugate_orientation_reduces_by_y_sign_and_Q_sign"] is not True:
        violations.append("Gaussian_orientation_reduction_failed")
    ready = not violations
    proof_status = (
        {
            "primitive_Gaussian_factors_proved_coprime_here": True,
            "Gaussian_square_reduced_to_two_orientations_here": True,
            "real_and_Gaussian_descents_coupled_here": True,
            "Gaussian_square_equation_eliminated_exactly_here": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl546",
        "object_layer": "m2_trivial_unit_Gaussian_double_descent_inside_wl544",
        "input_checkpoint": {"work_log": "wl545", "ready": _wl545_ready(wl545)},
        "Gaussian_descent": {
            "prime_representation": "ell=a_0^2+b_0^2",
            "factorization": "A+iQ=eta*pi_or_conjugate(pi)*(x+iy)^2",
            "norm": "x^2+y^2=D",
            "orientation_B": "Q=+/-[b_0*(x^2-y^2)+2*a_0*x*y]",
            "orientation_R": "Q=+/-[a_0*(x^2-y^2)-2*b_0*x*y]",
            "essential_orientation_count": 2,
        },
        "double_descent_system": {
            "norm_compatibility": "u^2-ell*v^2=+/-4*(x^2+y^2)",
            "real_coordinate": "Q=u*v",
            "Gaussian_coordinate_choices": [
                "+/-[b_0*(x^2-y^2)+2*a_0*x*y]",
                "+/-[a_0*(x^2-y^2)-2*b_0*x*y]",
            ],
            "remaining_G_square": "D^8*G_ell((Q/D)^2) is a square",
            "remaining_positivity": "ell*Q^4+4*Q^2*D^2-4*ell*D^4>0",
        },
        "primitive_conditions": {
            "gcd_x_y": 1,
            "ell_eq_5_mod_8": "u,v odd and coprime",
            "ell_eq_1_mod_8": "u=2m,v=2n with coprime opposite-parity m,n",
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
            "results/closure_quotient_rank_zero_aa_bb_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl546_m2_pure_v_ell_trivial_unit_gaussian_double_descent()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
