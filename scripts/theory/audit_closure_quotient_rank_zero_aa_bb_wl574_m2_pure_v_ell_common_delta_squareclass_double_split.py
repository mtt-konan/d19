#!/usr/bin/env python3
"""Audit the common Delta-squareclass split of both source-factor pairs."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl573_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl573_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling"
    )
    from json_io import write_json


def _wl573_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl573"
        and proof.get("Delta_divides_positive_quartic_form_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    a, b, m, n = sp.symbols("a b m n", integer=True)
    first = a**2 * m + 2 * a**2 * n - 2 * b**2 * n
    second = a**2 * n + 2 * b**2 * m - 2 * a**2 * m
    third = a**2 * m + 4 * b**2 * m - 2 * b**2 * n
    fourth = a**2 * n + 2 * b**2 * m + 4 * b**2 * n
    r1 = 5 * a**4 - 8 * a**2 * b**2 + 4 * b**4
    r2 = a**4 + 8 * a**2 * b**2 + 20 * b**4
    return {
        "AB_determinant_in_m": sp.factor(sp.resultant(first, second, m)) == n * r1,
        "AB_determinant_in_n": sp.factor(sp.resultant(first, second, n)) == -m * r1,
        "CD_determinant_in_m": sp.factor(sp.resultant(third, fourth, m)) == n * r2,
        "CD_determinant_in_n": sp.factor(sp.resultant(third, fourth, n)) == -m * r2,
        "R1_positive_completion": sp.expand(
            r1 - (5 * (a**2 - sp.Rational(4, 5) * b**2) ** 2 + sp.Rational(4, 5) * b**4)
        )
        == 0,
    }


def build_wl574_m2_pure_v_ell_common_delta_squareclass_double_split() -> dict[str, Any]:
    wl573 = wl573_module.build_wl573_m2_pure_v_ell_generic_cover_integral_denominator_coupling()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl573_ready(wl573):
        violations.append("wl573_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "both_source_pairs_share_canonical_Delta_squareclass_here": True,
            "AB_common_gcd_supported_on_R1_here": True,
            "CD_common_gcd_supported_on_R2_here": True,
            "two_complementary_splits_of_same_k_proved_here": True,
            "generic_genus_five_cover_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl574",
        "object_layer": "m2_common_Delta_squareclass_double_split",
        "input_checkpoint": {"work_log": "wl573", "ready": _wl573_ready(wl573)},
        "double_split_certificate": {
            "canonical_class": "2*Delta=k*h^2 with k positive squarefree",
            "source_products": ["A*B=k*U^2", "C*D=k*V^2"],
            "first_gcd_support": "gcd(A,B) divides 5*a^4-8*a^2*b^2+4*b^4",
            "second_gcd_support": "gcd(C,D) divides a^4+8*a^2*b^2+20*b^4",
            "first_split": "A/g1=alpha*r1^2, B/g1=beta*s1^2, alpha*beta=k",
            "second_split": "C/g2=gamma*r2^2, D/g2=delta0*s2^2, gamma*delta0=k",
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
            "results/closure_quotient_rank_zero_aa_bb_wl574_m2_pure_v_ell_common_delta_squareclass_double_split.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl574_m2_pure_v_ell_common_delta_squareclass_double_split()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
