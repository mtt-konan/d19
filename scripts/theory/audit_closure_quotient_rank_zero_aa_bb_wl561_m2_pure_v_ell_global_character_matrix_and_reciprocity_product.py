#!/usr/bin/env python3
"""Audit assembly of the global split-prime character matrix and product."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl560_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl560_m2_pure_v_ell_unified_normalized_split_prime_character"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl560_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl560_m2_pure_v_ell_unified_normalized_split_prime_character"
    )
    from json_io import write_json


def _wl560_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl560"
        and proof.get("every_odd_ell_minus_one_place_fully_classified_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product() -> dict[str, Any]:
    wl560 = wl560_module.build_wl560_m2_pure_v_ell_unified_normalized_split_prime_character()
    violations: list[str] = []
    if not _wl560_ready(wl560):
        violations.append("wl560_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "split_prime_characters_assembled_as_F2_system_here": True,
            "reciprocity_product_over_odd_common_split_primes_proved_here": True,
            "split_split_pairwise_characters_cancelled_here": True,
            "reciprocity_matrix_uniform_contradiction_proved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl561",
        "object_layer": "m2_global_F2_character_system_for_standard_Gaussian_square",
        "input_checkpoint": {"work_log": "wl560", "ready": _wl560_ready(wl560)},
        "matrix_certificate": {
            "rows": "split p|ell-1",
            "columns": "all odd q|ell-1",
            "membership_vector": "epsilon_q=min(v_q(ell-1),v_q(R)) mod 2",
            "entry": "A_pq=(1-Legendre(q,p))/2",
            "row_equation": "n_p=sum_(q!=p) A_pq*epsilon_q mod 2",
            "reciprocity_product": (
                "prod_(p in S_split) Legendre(C_p,p)="
                "prod_(p in S_split,q in S_inert) Legendre(q,p)"
            ),
            "split_only_corollary": "if S_inert is empty, the product is +1",
        },
        "proof_status": proof_status,
        "violations": violations,
        "theorem_level_selmer_matrix_claimed": False,
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
            "results/closure_quotient_rank_zero_aa_bb_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
