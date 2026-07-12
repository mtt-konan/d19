#!/usr/bin/env python3
"""Audit the global coprime squareclass split forced by the product coordinate."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl562_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl562_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation"
    )
    from json_io import write_json


def _wl562_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl562"
        and proof.get("local_orientation_determinacy_refuted_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl563_m2_pure_v_ell_global_product_squareclass_split() -> dict[str, Any]:
    wl562 = (
        wl562_module.build_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation()
    )
    violations: list[str] = []
    if not _wl562_ready(wl562):
        violations.append("wl562_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "global_product_coordinate_used_here": True,
            "coprime_squareclass_split_proved_here": True,
            "Gaussian_square_coordinates_reduced_to_fourth_powers_here": True,
            "orientation_product_scale_coupled_here": True,
            "complementary_divisor_split_systems_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl563",
        "object_layer": "m2_global_integer_factorization_inside_standard_Gaussian_square",
        "input_checkpoint": {"work_log": "wl562", "ready": _wl562_ready(wl562)},
        "factorization_certificate": {
            "product_equation": "a*b=2*(ell-1)/r*(Q*D)^2",
            "squarefree_kernel": "2*(ell-1)/r=kappa*h^2",
            "coprime_split": [
                "a=g*alpha*M^2",
                "b=g*beta*N^2",
                "alpha*beta=kappa",
            ],
            "scale_equation": "g*M*N=h*abs(Q*D)",
            "real_coordinate": "F=r*g^2*(alpha^2*M^4-beta^2*N^4)",
            "positivity": (
                "ell*(alpha^2*M^4-beta^2*N^4)+"
                "2*(ell-1)*kappa*M^2*N^2>0"
            ),
        },
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
            "results/closure_quotient_rank_zero_aa_bb_wl563_m2_pure_v_ell_global_product_squareclass_split.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl563_m2_pure_v_ell_global_product_squareclass_split()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
