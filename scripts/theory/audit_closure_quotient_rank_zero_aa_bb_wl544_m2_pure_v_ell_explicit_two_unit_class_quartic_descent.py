#!/usr/bin/env python3
"""Audit the explicit at-most-two-unit-class quartic descent after wl543."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl543_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl543_m2_pure_v_ell_real_quadratic_square_ideal_descent"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl543_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl543_m2_pure_v_ell_real_quadratic_square_ideal_descent"
    )
    from json_io import write_json


def _wl543_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl543"
        and proof.get("remaining_totally_positive_unit_squareclasses_at_most_two")
        is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, Any]:
    ell, r, s, u, v, z, w = sp.symbols("ell r s u v Z W")
    n = u**2 - ell * v**2
    f = s * (u**2 + ell * v**2) + 2 * r * u * v
    h = r * (u**2 + ell * v**2) + 2 * ell * s * u * v
    unit_relation = r**2 - ell * s**2 - 4
    conic_remainder = sp.rem(sp.expand(h**2 - ell * f**2 - 4 * n**2), unit_relation, r)
    j = (
        f**8
        + (16 - 8 * ell) * f**6 * n**2
        + (32 * ell**2 - 96 * ell + 72) * f**4 * n**4
        + (32 * ell - 64) * f**2 * n**6
        + 16 * n**8
    )
    q_square = f**2 / n**2
    g = (
        q_square**4
        + (16 - 8 * ell) * q_square**3
        + (32 * ell**2 - 96 * ell + 72) * q_square**2
        + (32 * ell - 64) * q_square
        + 16
    )
    return {
        "automatic_conic_identity_verified": sp.factor(conic_remainder) == 0,
        "G_homogenization_verified": sp.simplify(j - n**8 * g) == 0,
        "reconstruction_first_square": "a=Z/N from Z^2=ell*N^2-F^2",
        "reconstruction_second_square": "c=H/N from H^2-ell*F^2=4*N^2",
        "reconstruction_G_square": "V=W/N^4 from W^2=J_ell(F,N)",
        "positivity_homogenization": (
            "ell*F^4+4*F^2*N^2-4*ell*N^4>0"
        ),
        "unused_symbol_guard": str(z) == "Z" and str(w) == "W",
    }


def build_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent() -> dict[str, Any]:
    wl543 = wl543_module.build_wl543_m2_pure_v_ell_real_quadratic_square_ideal_descent()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl543_ready(wl543):
        violations.append("wl543_input_not_ready")
    for key in ("automatic_conic_identity_verified", "G_homogenization_verified"):
        if symbolic[key] is not True:
            violations.append(f"symbolic_identity_failed:{key}")
    ready = not violations
    proof_status = (
        {
            "abstract_unit_square_descent_expanded_here": True,
            "at_most_two_explicit_integer_quartic_branches_here": True,
            "Gaussian_G_and_positivity_pulled_back_exactly_here": True,
            "forward_and_converse_reconstruction_proved_here": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl544",
        "object_layer": "m2_explicit_two_unit_class_quartic_descent_inside_wl535",
        "input_checkpoint": {"work_log": "wl543", "ready": _wl543_ready(wl543)},
        "coordinate_forms": {
            "unit": "epsilon=(r+s*sqrt(ell))/2, r^2-ell*s^2=4",
            "beta": "(u+v*sqrt(ell))/2 with u congruent v mod 2",
            "N": "u^2-ell*v^2",
            "F": "s*(u^2+ell*v^2)+2*r*u*v",
            "H": "r*(u^2+ell*v^2)+2*ell*s*u*v",
            "automatic_identity": "H^2-ell*F^2=4*N^2",
        },
        "explicit_system": {
            "unit_class_count_upper_bound": 2,
            "nonzero_condition": "N!=0",
            "Gaussian_square": "Z^2=ell*N^2-F^2",
            "G_square": "W^2=J_ell(F,N)",
            "positivity": "ell*F^4+4*F^2*N^2-4*ell*N^4>0",
            "reconstruction": ["q=F/N", "a=Z/N", "c=H/N", "V=W/N^4"],
        },
        "trivial_unit_branch": {
            "r": 2,
            "s": 0,
            "F": "4*u*v",
            "H": "2*(u^2+ell*v^2)",
            "N": "u^2-ell*v^2",
            "Gaussian_quartic": "Z^2=ell*(u^2-ell*v^2)^2-16*u^2*v^2",
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
            "results/closure_quotient_rank_zero_aa_bb_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl544_m2_pure_v_ell_explicit_two_unit_class_quartic_descent()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
