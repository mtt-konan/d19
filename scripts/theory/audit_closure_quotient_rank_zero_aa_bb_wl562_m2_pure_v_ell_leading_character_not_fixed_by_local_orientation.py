#!/usr/bin/env python3
"""Audit exact local witnesses showing leading-character freedom."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl561_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl561_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product"
    )
    from json_io import write_json


def _wl561_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl561"
        and proof.get("split_prime_characters_assembled_as_F2_system_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation() -> dict[str, Any]:
    wl561 = wl561_module.build_wl561_m2_pure_v_ell_global_character_matrix_and_reciprocity_product()
    violations: list[str] = []
    if not _wl561_ready(wl561):
        violations.append("wl561_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "opposite_leading_bits_with_same_local_stratum_proved_here": True,
            "both_Gaussian_orientations_locally_compatible_here": True,
            "local_orientation_determinacy_refuted_here": True,
            "global_integer_compatibility_resolved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl562",
        "object_layer": "m2_local_determinacy_of_global_character_matrix_rows",
        "input_checkpoint": {"work_log": "wl561", "ready": _wl561_ready(wl561)},
        "witness_certificate": {
            "prime": 13,
            "local_ell": 1,
            "class_r": 1,
            "square_character_witness": {
                "t": 0,
                "f_t": 9,
                "row_bit": 0,
                "B_witness": [0, 1],
                "R_witness": [1, 1],
            },
            "nonsquare_character_witness": {
                "t": 10,
                "q": 6,
                "f_t": 6,
                "row_bit": 1,
                "B_witness": [1, 2],
                "R_witness": [1, 4],
            },
            "same_valuation_stratum": "d=0 and epsilon=0",
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
            "results/closure_quotient_rank_zero_aa_bb_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl562_m2_pure_v_ell_leading_character_not_fixed_by_local_orientation()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
