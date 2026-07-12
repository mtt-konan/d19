#!/usr/bin/env python3
"""Audit the parameter-prime valuation split inside wl535."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl539_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl539_m2_pure_v_ell_direct_residue_method_classification"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl539_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl539_m2_pure_v_ell_direct_residue_method_classification"
    )
    from json_io import write_json


def _wl539_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl539"
        and proof.get("method_exhausted_outside_four_pairs") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, Any]:
    q, ell, i = sp.symbols("Q ell i")
    g = q**4 + 16 * q**3 + 72 * q**2 - 64 * q + 16
    factor_product = (q**2 + (8 - 4 * i) * q - 4) * (
        q**2 + (8 + 4 * i) * q - 4
    )
    factor_remainder = sp.rem(sp.expand(g - factor_product), i**2 + 1, i)
    first_factor = q**2 + (8 - 4 * i) * q - 4
    root_identity = q * (q / 4 + 2 - i / 2) ** 2 - 2
    root_remainder = sp.rem(sp.expand(root_identity), first_factor, q)
    root_remainder = sp.rem(sp.expand(root_remainder), i**2 + 1, i)

    full_g = (
        q**4
        + (16 - 8 * ell) * q**3
        + (32 * ell**2 - 96 * ell + 72) * q**2
        + (32 * ell - 64) * q
        + 16
    )
    reduction = sp.expand(full_g.subs(ell, 0))
    discriminant = sp.factor(sp.discriminant(g, q))
    return {
        "reduction_identity_verified": sp.expand(reduction - g) == 0,
        "reduced_discriminant": str(discriminant),
        "reduced_discriminant_equals_2_pow_29": discriminant == 2**29,
        "gaussian_factorization_verified": factor_remainder == 0,
        "root_squareclass_identity_verified": root_remainder == 0,
        "root_squareclass_identity": "Q*(Q/4+2-i/2)^2=2",
    }


def build_wl540_m2_pure_v_ell_parameter_prime_valuation_split() -> dict[str, Any]:
    wl539 = wl539_module.build_wl539_m2_pure_v_ell_direct_residue_method_classification()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl539_ready(wl539):
        violations.append("wl539_input_not_ready")
    for key in (
        "reduction_identity_verified",
        "reduced_discriminant_equals_2_pow_29",
        "gaussian_factorization_verified",
        "root_squareclass_identity_verified",
    ):
        if symbolic[key] is not True:
            violations.append(f"symbolic_certificate_failed:{key}")
    ready = not violations
    proof_status = (
        {
            "q_a_c_are_parameter_prime_units_here": True,
            "G_square_condition_split_by_simple_hensel_roots_here": True,
            "root_reduction_branch_requires_ell_eq_1_mod_8_here": True,
            "ell_eq_5_mod_8_reduced_to_nonzero_unit_branch_here": True,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl540",
        "object_layer": "m2_parameter_prime_valuation_split_inside_wl535",
        "input_checkpoint": {"work_log": "wl539", "ready": _wl539_ready(wl539)},
        "valuation_lemma": {
            "forced_values": [
                "v_ell(q)=0",
                "v_ell(a)=0 for a^2=ell-q^2",
                "v_ell(c)=0 for c^2=ell*q^2+4",
                "c is congruent to plus or minus 2 mod ell",
            ],
            "negative_q_valuation_failure": (
                "v_ell(ell*q^2+4)=1+2*v_ell(q) is odd"
            ),
            "positive_q_valuation_failure": "v_ell(ell-q^2)=1 is odd",
        },
        "G_local_split": {
            "unit_branch": "g(q^2 mod ell) is a nonzero square and V is a unit",
            "root_branch": (
                "for the unique Hensel root alpha in the residue class, "
                "v_ell(q^2-alpha)=v_ell(G_ell(q^2)) is positive and even"
            ),
            "root_branch_only_if_ell_mod_8": 1,
            "unit_squareclass_after_even_root_distance_still_required": True,
        },
        "symbolic_certificate": symbolic,
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
            "results/closure_quotient_rank_zero_aa_bb_wl540_m2_pure_v_ell_parameter_prime_valuation_split.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl540_m2_pure_v_ell_parameter_prime_valuation_split()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
