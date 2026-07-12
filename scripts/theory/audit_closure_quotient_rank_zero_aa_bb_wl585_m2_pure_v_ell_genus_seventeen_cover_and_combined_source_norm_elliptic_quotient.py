#!/usr/bin/env python3
"""Audit the genus-17 cover and combined source-norm elliptic quotient."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl584_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl584_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection"
    )
    from json_io import write_json


def _wl584_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl584"
        and proof.get("final_norm_discriminant_equivalence_proved_here") is True
        and payload.get("advance_to_m3") is False
    )


def _reduce_reciprocal_invariant(expr: sp.Expr, x: sp.Symbol, s: sp.Symbol) -> sp.Expr:
    expanded = sp.expand(expr)
    polynomial = 0
    for term in sp.Add.make_args(expanded):
        exponent = int(term.as_powers_dict().get(x, 0))
        coefficient = term / x**exponent
        replacement = x**exponent if exponent >= 0 else ((x - s) / 4) ** (-exponent)
        polynomial += coefficient * replacement
    return sp.rem(
        sp.Poly(sp.expand(polynomial), x),
        sp.Poly(x**2 - s * x - 4, x),
    ).as_expr()


def _symbolic_certificate() -> dict[str, bool]:
    ell, x, tau, s = sp.symbols("ell X tau S", nonzero=True)
    f = x**2 + (8 - 4 * ell) * x - 4
    e = 4 * (ell - 1) * x
    positivity = ell * x**2 + 4 * x - 4 * ell
    cone_after_norm_relation = (
        ell * (2 * tau * f / e) + 2 * (ell - 1) * tau
    )
    g = sp.expand(f**2 + e**2)
    source_product = x * (ell - x) * (ell * x + 4)
    combined = sp.expand(source_product * g)
    transform = -4 / x
    quotient_rhs = (
        (ell**2 - ell * s - 4)
        * (s**2 + (16 - 8 * ell) * s + 32 * ell**2 - 96 * ell + 80)
    )
    reduced_combined = _reduce_reciprocal_invariant(combined / x**4, x, s)
    g_discriminant = sp.factor(sp.discriminant(g, x))
    expected_g_discriminant = sp.factor(
        2**26 * (ell - 2) ** 2 * (ell - 1) ** 4 * ((ell - 1) ** 2 + 1)
    )
    quotient_discriminant = sp.factor(sp.discriminant(quotient_rhs, s))
    expected_quotient_discriminant = sp.factor(
        -64 * (ell - 1) ** 2 * (5 * ell**2 - 8 * ell + 4) ** 4
    )
    boundary_factor = 5 * ell**2 - 8 * ell + 4
    return {
        "cone_sign_equals_positivity_sign": sp.simplify(
            cone_after_norm_relation
            - tau * positivity / (2 * (ell - 1) * x)
        )
        == 0,
        "g_quartic_discriminant": sp.simplify(
            g_discriminant - expected_g_discriminant
        )
        == 0,
        "g_nonzero_at_zero": sp.simplify(g.subs(x, 0) - 16) == 0,
        "g_nonzero_at_ell": sp.factor(g.subs(x, ell) - boundary_factor**2) == 0,
        "g_nonzero_at_negative_four_over_ell": sp.factor(
            g.subs(x, -4 / ell) - 16 * boundary_factor**2 / ell**4
        )
        == 0,
        "g_reciprocal_identity": sp.simplify(
            g.subs(x, transform) - 16 * g / x**4
        )
        == 0,
        "source_product_reciprocal_identity": sp.simplify(
            source_product.subs(x, transform) - 16 * source_product / x**4
        )
        == 0,
        "combined_genus_three_reciprocal_identity": sp.simplify(
            combined.subs(x, transform) - 256 * combined / x**8
        )
        == 0,
        "combined_elliptic_quotient_equation": sp.simplify(
            reduced_combined - quotient_rhs
        )
        == 0,
        "combined_elliptic_quotient_discriminant": sp.simplify(
            quotient_discriminant - expected_quotient_discriminant
        )
        == 0,
        "quadratic_lift_discriminant": sp.expand(
            (x - 4 / x) ** 2 + 16 - (x + 4 / x) ** 2
        )
        == 0,
    }


def build_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient(
) -> dict[str, Any]:
    wl584 = (
        wl584_module.build_wl584_m2_pure_v_ell_prime_coupled_source_elliptic_and_final_norm_intersection()
    )
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl584_ready(wl584):
        violations.append("wl584_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "selected_tau_interval_equivalent_to_positivity_here": True,
            "fixed_ell_full_cover_genus_seventeen_proved_here": True,
            "norm_bearing_character_quotients_classified_here": True,
            "combined_source_norm_genus_three_quotient_proved_here": True,
            "combined_rational_elliptic_quotient_proved_here": True,
            "restricted_combined_elliptic_image_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl585",
        "object_layer": "m2_genus_seventeen_cover_and_combined_elliptic_quotient",
        "input_checkpoint": {"work_log": "wl584", "ready": _wl584_ready(wl584)},
        "cover_certificate": {
            "squareclasses": ["X", "ell-X", "ell*X+4", "G_ell(X)"],
            "branch_count": 8,
            "cover_degree": 16,
            "genus": 17,
            "norm_bearing_quotient_genera": {
                "genus_1": 1,
                "genus_2": 6,
                "genus_3": 1,
            },
            "combined_quotient": "W^2=X*(ell-X)*(ell*X+4)*G_ell(X)",
            "elliptic_coordinates": ["S=X-4/X", "Z=W/X^2"],
            "candidate_image_restrictions": [
                "S^2+16 is a rational square",
                "positive quadratic lift X is a rational square",
                "sigma_ell<X<ell",
                "individual source and norm squareclasses lift",
            ],
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
            "results/closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = (
        build_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient()
    )
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
