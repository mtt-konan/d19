#!/usr/bin/env python3
"""Audit that the wl563-wl567 coupling adds no independent obstruction."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl567_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl567_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation"
    )
    from json_io import write_json


def _wl567_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl567"
        and proof.get("affine_row_formula_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    ell, q, d, r, g, kappa, h, alpha, beta, m, n = sp.symbols(
        "ell Q D r g kappa h alpha beta M N", positive=True
    )
    e = 4 * (ell - 1) * q**2 * d**2
    f = q**4 + (8 - 4 * ell) * q**2 * d**2 - 4 * d**4
    original_positive = ell * q**4 + 4 * q**2 * d**2 - 4 * ell * d**4
    cone = (
        ell * (alpha**2 * m**4 - beta**2 * n**4)
        + 2 * (ell - 1) * kappa * m**2 * n**2
    )
    a = alpha * m**2
    b = beta * n**2
    c = e * (a**2 + b**2) / (2 * a * b)
    ratio_relation = 2 * f * a * b - e * (a**2 - b**2)

    scale_substitution = sp.expand(
        (2 * r * g**2 * kappa * m**2 * n**2 - e).subs(
            ell, 1 + r * kappa * h**2 / 2
        )
    )
    scale_target = 2 * r * kappa * (
        (g * m * n) ** 2 - (h * q * d) ** 2
    )
    cone_substitution = sp.expand(
        ell * r * g**2 * (alpha**2 * m**4 - beta**2 * n**4)
        + (ell - 1) * 2 * r * g**2 * alpha * beta * m**2 * n**2
        - r * g**2 * cone
    ).subs(alpha * beta, kappa)
    norm_remainder = sp.factor(c**2 - f**2 - e**2)
    opposite_relation = 2 * f * a * b + e * (a**2 - b**2)
    expected_factorization = sp.factor(
        -ratio_relation * opposite_relation / (4 * a**2 * b**2)
    )

    return {
        "positivity_identity": sp.expand(original_positive - (ell * f + (ell - 1) * e)) == 0,
        "scale_equivalent_after_squareclass_cancellation": sp.expand(
            scale_substitution - scale_target
        )
        == 0,
        "cone_is_coordinate_substitution": sp.expand(cone_substitution) == 0,
        "norm_square_has_two_signed_ratio_branches": sp.simplify(
            norm_remainder - expected_factorization
        )
        == 0,
    }


def build_wl568_m2_pure_v_ell_allocation_coupling_redundancy() -> dict[str, Any]:
    wl567 = wl567_module.build_wl567_m2_pure_v_ell_affine_f2_system_for_split_allocation()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl567_ready(wl567):
        violations.append("wl567_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "scale_is_exact_product_coordinate_rewrite_here": True,
            "cone_is_exact_original_positivity_rewrite_here": True,
            "affine_rows_automatic_for_actual_factorization_here": True,
            "allocation_route_independent_obstruction_refuted_here": True,
            "selected_orientation_norm_intersection_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl568",
        "object_layer": "m2_trivial_unit_selected_orientation_norm_intersection",
        "input_checkpoint": {"work_log": "wl567", "ready": _wl567_ready(wl567)},
        "redundancy_certificate": {
            "scale": "2*r*a*b=E iff g*M*N=h*abs(Q*D)",
            "positivity": "original_strict_expression=ell*F+(ell-1)*E",
            "ratio": "2*F*A*B=E*(A^2-B^2)",
            "norm": (
                "C=E*(A^2+B^2)/(2*A*B); norm square factors into two "
                "ordered signed-ratio branches"
            ),
            "affine_rows": "necessary identities when z_q is computed from actual H",
        },
        "next_exact_lemma": (
            "selected B_pi/R_pi orientation intersected with F^2+E^2 square "
            "and the strict positivity condition"
        ),
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
            "results/closure_quotient_rank_zero_aa_bb_wl568_m2_pure_v_ell_allocation_coupling_redundancy.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl568_m2_pure_v_ell_allocation_coupling_redundancy()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
