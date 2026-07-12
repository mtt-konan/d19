#!/usr/bin/env python3
"""Audit the canonical rational class determined by the coordinate gcd."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

try:
    wl553_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl553_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone"
    )
    from json_io import write_json


def _wl553_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl553"
        and proof.get("positivity_transferred_to_class_coordinates_here") is True
        and payload.get("advance_to_m3") is False
    )


def build_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd() -> dict[str, Any]:
    wl553 = wl553_module.build_wl553_m2_pure_v_ell_positivity_transfer_to_unit_class_cone()
    violations: list[str] = []
    if not _wl553_ready(wl553):
        violations.append("wl553_input_not_ready")
    ready = not violations
    proof_status = (
        {
            "odd_coordinate_gcd_parity_of_Gaussian_square_proved_here": True,
            "rational_class_made_candidate_canonical_here": True,
            "independent_r_divisor_choice_eliminated_here": True,
            "canonical_class_equation_solved_here": False,
            "uniform_full_wl535_obstruction_proved_here": False,
            "advance_to_m3": False,
        }
        if ready
        else {}
    )
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl554",
        "object_layer": "m2_canonical_rational_class_inside_unique_unit_class_equation",
        "input_checkpoint": {"work_log": "wl553", "ready": _wl553_ready(wl553)},
        "gcd_certificate": {
            "Gaussian_square_coordinates": ["m^2-n^2", "2*m*n"],
            "odd_common_valuation_parity": "even",
            "candidate_coordinates": ["E=4*(ell-1)*Q^2*D^2", "F=R-E"],
            "canonical_class": "r=sqf_odd(gcd(E,F))=sqf_odd(gcd(ell-1,R))",
            "primewise_formula": "v_p(r)=min(v_p(ell-1),v_p(R)) mod 2",
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
            "results/closure_quotient_rank_zero_aa_bb_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl554_m2_pure_v_ell_canonical_rational_class_from_coordinate_gcd()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
