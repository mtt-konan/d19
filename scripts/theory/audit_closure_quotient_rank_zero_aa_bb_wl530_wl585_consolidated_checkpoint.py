#!/usr/bin/env python3
"""Audit the consolidated wl530-wl585 pure-v_ell checkpoint."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl530_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family"
    )
    wl585_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl530_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family"
    )
    wl585_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient"
    )
    from json_io import write_json


def _wl530_ready(payload: dict[str, Any]) -> bool:
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl530"
        and payload.get("advance_to_m2") is False
    )


def _wl585_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl585"
        and proof.get("combined_rational_elliptic_quotient_proved_here") is True
        and proof.get("restricted_combined_elliptic_image_solved_here") is False
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


def _independent_symbolic_review() -> dict[str, bool]:
    ell, x, tau, s = sp.symbols("ell X tau S", nonzero=True)
    delta = tau**2 + 2 * tau - 1
    g = (
        x**4
        + (16 - 8 * ell) * x**3
        + (32 * ell**2 - 96 * ell + 72) * x**2
        + (32 * ell - 64) * x
        + 16
    )
    f = x**2 + (8 - 4 * ell) * x - 4
    e = 4 * (ell - 1) * x
    ell_formula = (
        tau * x**2 + 2 * x * tau**2 + 8 * x * tau - 2 * x - 4 * tau
    ) / (2 * x * delta)
    first_square = -(
        (x * tau + 2 * x - 2) * (2 * x * tau - x - 2 * tau)
    ) / (2 * x * delta)
    second_square = (
        (x + 2 * tau + 4) * (x * tau + 4 * tau - 2)
    ) / (2 * delta)
    positivity = ell * x**2 + 4 * x - 4 * ell
    cone_after_norm = ell * (2 * tau * f / e) + 2 * (ell - 1) * tau
    source_product = x * (ell - x) * (ell * x + 4)
    combined = sp.expand(source_product * g)
    quotient_rhs = (
        (ell**2 - ell * s - 4)
        * (s**2 + (16 - 8 * ell) * s + 32 * ell**2 - 96 * ell + 80)
    )
    quotient_reduction = _reduce_reciprocal_invariant(combined / x**4, x, s)
    boundary = 5 * ell**2 - 8 * ell + 4
    return {
        "completed_square_for_g": sp.expand(g - f**2 - e**2) == 0,
        "ell_formula_solves_norm_quadratic": sp.simplify(
            (e * tau**2 - 2 * f * tau - e).subs(ell, ell_formula)
        )
        == 0,
        "first_source_factorization": sp.simplify(
            (ell - x).subs(ell, ell_formula) - first_square
        )
        == 0,
        "second_source_factorization": sp.simplify(
            (ell * x + 4).subs(ell, ell_formula) - second_square
        )
        == 0,
        "norm_discriminant": sp.expand(
            sp.discriminant(e * tau**2 - 2 * f * tau - e, tau) - 4 * g
        )
        == 0,
        "cone_is_exact_positivity": sp.simplify(
            cone_after_norm - tau * positivity / (2 * (ell - 1) * x)
        )
        == 0,
        "g_reciprocal_identity": sp.simplify(
            g.subs(x, -4 / x) - 16 * g / x**4
        )
        == 0,
        "g_quartic_discriminant": sp.factor(sp.discriminant(g, x))
        == sp.factor(
            2**26 * (ell - 2) ** 2 * (ell - 1) ** 4 * ((ell - 1) ** 2 + 1)
        ),
        "g_avoids_source_branches": all(
            [
                sp.simplify(g.subs(x, 0) - 16) == 0,
                sp.factor(g.subs(x, ell) - boundary**2) == 0,
                sp.factor(g.subs(x, -4 / ell) - 16 * boundary**2 / ell**4)
                == 0,
            ]
        ),
        "combined_elliptic_quotient": sp.simplify(
            quotient_reduction - quotient_rhs
        )
        == 0,
        "combined_elliptic_discriminant": sp.factor(
            sp.discriminant(quotient_rhs, s)
        )
        == sp.factor(-64 * (ell - 1) ** 2 * boundary**4),
        "ell_5_g_recovery": sp.expand(g.subs(ell, 5))
        == x**4 - 24 * x**3 + 392 * x**2 + 96 * x + 16,
    }


def build_wl530_wl585_consolidated_checkpoint() -> dict[str, Any]:
    wl530 = wl530_module.build_wl530_m1_pure_v_ell_symbolic_family()
    wl585 = (
        wl585_module.build_wl585_m2_pure_v_ell_genus_seventeen_cover_and_combined_source_norm_elliptic_quotient()
    )
    symbolic = _independent_symbolic_review()
    violations: list[str] = []
    if not _wl530_ready(wl530):
        violations.append("wl530_input_not_ready")
    if not _wl585_ready(wl585):
        violations.append("wl585_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    review_status = (
        {
            "key_algebra_independently_rechecked": True,
            "forward_converse_and_exceptions_reviewed": True,
            "correctness_defect_found": False,
            "wl535_proved": False,
            "strict_counterexample_found": False,
            "strictly_smaller_arithmetic_proposition_found": False,
            "wl585_uniform_arithmetic_tool_available": False,
            "elliptic_quotient_route_exhausted": True,
            "m2_closed": False,
            "advance_to_m3": False,
            "allow_equivalent_model_as_future_progress": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "checkpoint": "wl530-wl585",
        "work_log": "wl530-wl585-consolidated",
        "input_checkpoints": {
            "wl530": _wl530_ready(wl530),
            "wl585": _wl585_ready(wl585),
        },
        "independent_symbolic_review": symbolic,
        "review_status": review_status,
        "exact_remaining_proposition": (
            "the four wl535 square/positivity conditions for every odd prime "
            "ell congruent to 1 mod 4"
        ),
        "accepted_future_outcomes": [
            "direct proof of wl535",
            "strict counterexample",
            "strictly smaller arithmetic proposition with removed freedom identified",
        ],
        "violations": violations,
        "complete_selmer_upper_bound_proved": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "advance_to_m3": False,
        "stop_after_consolidation": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(
            "results/closure_quotient_rank_zero_aa_bb_wl530_wl585_consolidated_checkpoint.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl530_wl585_consolidated_checkpoint()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"checkpoint={payload['checkpoint']}")
    for key, value in payload["review_status"].items():
        print(f"{key}={value}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
