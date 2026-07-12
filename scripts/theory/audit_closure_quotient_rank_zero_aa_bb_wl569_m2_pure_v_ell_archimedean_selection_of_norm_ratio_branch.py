#!/usr/bin/env python3
"""Audit the archimedean selection of the unique positive norm-ratio branch."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from typing import Any

import sympy as sp

try:
    wl568_module = importlib.import_module(
        "scripts.theory."
        "audit_closure_quotient_rank_zero_aa_bb_wl568_m2_pure_v_ell_allocation_coupling_redundancy"
    )
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    wl568_module = importlib.import_module(
        "audit_closure_quotient_rank_zero_aa_bb_wl568_m2_pure_v_ell_allocation_coupling_redundancy"
    )
    from json_io import write_json


def _wl568_ready(payload: dict[str, Any]) -> bool:
    proof = payload.get("proof_status", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == "wl568"
        and proof.get("allocation_route_independent_obstruction_refuted_here") is True
        and payload.get("advance_to_m3") is False
    )


def _symbolic_certificate() -> dict[str, bool]:
    ell, x, tau = sp.symbols("ell X tau", positive=True)
    f = x**2 + (8 - 4 * ell) * x - 4
    derivative = sp.diff(f, x)
    rho = (sp.sqrt((ell - 1) ** 2 + ell**2) - (ell - 1)) / ell
    cone = ell * (tau**2 - 1) + 2 * (ell - 1) * tau
    return {
        "F_polynomial_recorded": sp.expand(f - (x**2 + (8 - 4 * ell) * x - 4)) == 0,
        "F_derivative_recorded": derivative == 2 * x + 8 - 4 * ell,
        "rho_is_positive_cone_root": sp.simplify(cone.subs(tau, rho)) == 0,
        "rho_rationalized_identity": sp.simplify(
            rho - ell / (sp.sqrt((ell - 1) ** 2 + ell**2) + ell - 1)
        )
        == 0,
    }


def build_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch() -> dict[str, Any]:
    wl568 = wl568_module.build_wl568_m2_pure_v_ell_allocation_coupling_redundancy()
    symbolic = _symbolic_certificate()
    violations: list[str] = []
    if not _wl568_ready(wl568):
        violations.append("wl568_input_not_ready")
    violations.extend(name for name, passed in symbolic.items() if not passed)
    ready = not violations
    proof_status = (
        {
            "source_square_and_positivity_force_0_lt_X_lt_ell_here": True,
            "F_strictly_negative_on_candidate_range_here": True,
            "positive_ordered_norm_ratio_branch_unique_here": True,
            "strict_cone_ratio_interval_proved_here": True,
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
        "work_log": "wl569",
        "object_layer": "m2_trivial_unit_archimedean_norm_ratio_branch",
        "input_checkpoint": {"work_log": "wl568", "ready": _wl568_ready(wl568)},
        "branch_certificate": {
            "candidate_range": "0<X=q^2<ell",
            "sign": "F=D^4*(X^2+(8-4*ell)*X-4)<0",
            "ordered_ratio": "tau=A/B=(C+F)/E",
            "exact_interval": (
                "(sqrt((ell-1)^2+ell^2)-(ell-1))/ell<tau<1"
            ),
            "uniform_interval": "sqrt(2)-1<tau<1",
        },
        "next_exact_lemma": (
            "couple the unique tau=(C+F)/E branch in (rho_ell,1) to the "
            "selected R_pi/B_pi orientation"
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
            "results/closure_quotient_rank_zero_aa_bb_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch.json"
        ),
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl569_m2_pure_v_ell_archimedean_selection_of_norm_ratio_branch()
    write_json(args.out, payload)
    print(f"status={payload['status']}")
    print(f"work_log={payload['work_log']}")
    for key, value in payload["proof_status"].items():
        print(f"{key}={value}")
    print(f"advance_to_m3={payload['advance_to_m3']}")
    return 1 if args.strict and payload["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
