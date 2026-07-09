#!/usr/bin/env python3
"""Audit the AA+BB pullback/common-source constraints for the wl487 point."""

from __future__ import annotations

import argparse
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl489 / closure_pullback_common_source_constraints_for_"
    "global_C_d_point for the explicit AA A=3,B=1 point selected by wl488. "
    "It checks the centered even AA pullback and the same-source AA+BB closure "
    "constraints for this point only. It does not run broad rank or Selmer "
    "diagnostics, does not use the old package-x S~ bridge, does not run "
    "single-curve diagnostics, does not prove a complete Sel_2(E) upper bound, "
    "and does not claim dim Sel_2(E)=2, rank zero, Sha[2]=0, full "
    "Mordell-Weil torsion, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

A = 3
B = 1
TOTAL = A + B
L = A
P = 40
SQRT_Q = 52
Q = SQRT_Q * SQRT_Q
POINT_X = 152
POINT_Y = 1536
D_VECTOR = {
    "d_minus_p": 3,
    "d_pos_2sqrt_q": 3,
    "d_neg_2sqrt_q": 1,
}
TARGET_CANDIDATE_ID = "AA_A3_B1_u_3_complete_d_candidate"
TARGET_GATE = "AA_BB_closure_pullback_common_source_constraints_for_global_C_d_point"


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl488_ready(wl488: dict[str, Any]) -> bool:
    point = wl488.get("u3_global_point_impact", {})
    selected_gate = wl488.get("selected_next_gate", {})
    return (
        wl488.get("status") == "ok"
        and wl488.get("ready") is True
        and wl488.get("lemma_id")
        == "WL488_select_next_complete_d_coordinate_route_after_u3_global_point"
        and wl488.get("work_log") == "wl488"
        and wl488.get("input_work_log") == "wl487"
        and point.get("candidate_id") == TARGET_CANDIDATE_ID
        and point.get("d_vector") == D_VECTOR
        and point.get("point_classification")
        == "non_torsion_candidate_not_visible_two_torsion_baseline"
        and selected_gate.get("gate") == TARGET_GATE
        and selected_gate.get("entered_here") is False
        and wl488.get("closure_pullback_common_source_gate_selected_here") is True
        and wl488.get("old_package_x_coordinate_collapse_used") is False
        and wl488.get("package_x_s_tilde_bridge_used") is False
        and wl488.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl488.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl488)
    )


def _is_int_square(n: int) -> bool:
    return n >= 0 and isqrt(n) ** 2 == n


def _format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _explicit_global_point() -> dict[str, Any]:
    return {
        "candidate_id": TARGET_CANDIDATE_ID,
        "quotient": "AA",
        "A": A,
        "B": B,
        "total": TOTAL,
        "L": L,
        "E_L_model": "Y^2=(X+p)*(X^2-4*q)",
        "parameters": {"p": P, "q": Q, "sqrt_q": SQRT_Q},
        "point_on_E_L": {"X": POINT_X, "Y": POINT_Y},
        "complete_d_squareclass": dict(D_VECTOR),
    }


def _ambient_e_l_checks() -> dict[str, Any]:
    return {
        "curve_equation_holds": POINT_Y * POINT_Y
        == (POINT_X + P) * (POINT_X * POINT_X - 4 * Q),
        "complete_d_coordinate_relations": {
            "X_plus_p": "192 = 3*8^2",
            "X_minus_2sqrt_q": "48 = 3*4^2",
            "X_plus_2sqrt_q": "256 = 1*16^2",
        },
        "product_relation_square": "3*3*1 = 3^2",
    }


def _pullback_values() -> dict[str, Fraction]:
    denominator = 2 * (POINT_X + P)
    t = Fraction(POINT_Y, denominator)
    z = Fraction(POINT_X, 2) - t * t
    n = Fraction(TOTAL) + t
    n /= 2
    m = Fraction(TOTAL) - n
    quartic_y = z / 4
    return {
        "denominator": Fraction(denominator),
        "t": t,
        "z": z,
        "N": n,
        "M": m,
        "quartic_y": quartic_y,
    }


def _aa_pullback() -> dict[str, Any]:
    values = _pullback_values()
    t = values["t"]
    z = values["z"]
    n = values["N"]
    m = values["M"]
    quartic_y = values["quartic_y"]
    even_rhs = t**4 + P * t * t + Q
    aa_rhs = (n * n + A * A) * (m * m + A * A)
    return {
        "map_source": "centered even AA/BB quotient inverse map",
        "formulas": {
            "t": "Y/(2*(X+p))",
            "z": "X/2 - t^2",
            "N": "(A+B+t)/2",
            "M": "A+B-N",
            "quartic_y": "z/4",
        },
        "values": {
            "t": _format_fraction(t),
            "z": _format_fraction(z),
            "N": _format_fraction(n),
            "M": _format_fraction(m),
            "quartic_y": _format_fraction(quartic_y),
        },
        "checks": {
            "denominator_nonzero": values["denominator"] != 0,
            "even_quartic_identity": "60^2 = 4^4 + 40*4^2 + 2704",
            "aa_quotient_identity": "15^2 = (4^2+3^2)*(0^2+3^2)",
            "aa_pullback_proved_for_this_point": (
                z * z == even_rhs and quartic_y * quartic_y == aa_rhs
            ),
        },
    }


def _common_source_constraint_audit() -> dict[str, Any]:
    values = _pullback_values()
    n = values["N"]
    m = values["M"]
    aa_n = int(n * n + A * A)
    aa_m = int(m * m + A * A)
    bb_n = int(n * n + B * B)
    bb_m = int(m * m + B * B)
    return {
        "same_source_variables": {
            "N": _format_fraction(n),
            "M": _format_fraction(m),
            "A": A,
            "B": B,
        },
        "aa_side": {
            "N2_plus_A2": aa_n,
            "M2_plus_A2": aa_m,
            "product": aa_n * aa_m,
            "product_is_square": _is_int_square(aa_n * aa_m),
            "individual_square_flags": {
                "N2_plus_A2": _is_int_square(aa_n),
                "M2_plus_A2": _is_int_square(aa_m),
            },
        },
        "bb_side": {
            "N2_plus_B2": bb_n,
            "M2_plus_B2": bb_m,
            "product": bb_n * bb_m,
            "product_is_square": _is_int_square(bb_n * bb_m),
            "individual_square_flags": {
                "N2_plus_B2": _is_int_square(bb_n),
                "M2_plus_B2": _is_int_square(bb_m),
            },
        },
        "closure_positivity_checks": {
            "N_positive": n > 0,
            "M_positive": m > 0,
        },
        "failing_constraints": [
            "BB quotient product is not a rational square",
            "N^2+B^2 is not a rational square",
            "M is not positive for a nondegenerate closure point",
        ],
    }


def _wl489_verdict() -> dict[str, Any]:
    return {
        "status": "proved_fails_for_this_explicit_point",
        "proved_satisfies_AA_BB_constraints": False,
        "proved_fails_AA_BB_constraints": True,
        "missing_pullback_data_gate_triggered": False,
        "reason": (
            "The explicit AA ambient E_L point pulls back to N=4, M=0 on the "
            "AA closure quotient, but the same common-source values give "
            "(N^2+B^2)*(M^2+B^2)=17, not a square."
        ),
    }


def build_wl489_closure_pullback_common_source_constraints_for_global_c_d_point(
    *, wl488: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl488_ready(wl488):
        violations.append("wl488_input_not_ready_or_not_scoped")
    if not _ambient_e_l_checks()["curve_equation_holds"]:
        violations.append("ambient_e_l_curve_equation_check_failed")
    if not _aa_pullback()["checks"]["aa_pullback_proved_for_this_point"]:
        violations.append("aa_pullback_check_failed")
    if _common_source_constraint_audit()["bb_side"]["product_is_square"]:
        violations.append("bb_common_source_failure_not_verified")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl488 selected AA+BB closure/pullback/common-source gate",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL489_closure_pullback_common_source_constraints_for_global_C_d_point"
        ),
        "work_log": "wl489",
        "input_work_log": "wl488",
        "explicit_global_point": _explicit_global_point() if status == "ok" else {},
        "ambient_e_l_checks": _ambient_e_l_checks() if status == "ok" else {},
        "aa_pullback": _aa_pullback() if status == "ok" else {},
        "common_source_constraint_audit": (
            _common_source_constraint_audit() if status == "ok" else {}
        ),
        "wl489_verdict": _wl489_verdict() if status == "ok" else {},
        "routing_audit_only": True,
        "point_level_admissibility_decided_here": status == "ok",
        "broad_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "search_count_used_as_progress": False,
        "advance_to_wl490": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl488", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl489_closure_pullback_common_source_constraints_for_global_c_d_point(
        wl488=load_json(args.wl488)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl489 pullback/common-source audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    if audit["status"] == "ok":
        print(f"wl489_status={audit['wl489_verdict']['status']}")
        print(f"advance_to_wl490={audit['advance_to_wl490']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
