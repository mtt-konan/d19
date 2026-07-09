#!/usr/bin/env python3
"""Define the wl491 reusable ambient C_d to AA+BB admissibility filter."""

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
    "This audits only wl491 / reusable ambient-C_d-to-AA+BB admissibility "
    "filter. It defines the point-level filter contract and applies it as a "
    "regression to the known AA A=3,B=1 u_3 global C_d sample from wl489/wl490. "
    "It does not choose another M_tail/kernel candidate, does not run broad "
    "rank or Selmer diagnostics, does not use the old package-x S~ bridge, "
    "does not run single-curve diagnostics, does not prove a complete Sel_2(E) "
    "upper bound, and does not claim dim Sel_2(E)=2, rank zero, Sha[2]=0, "
    "full Mordell-Weil torsion, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

TARGET_CANDIDATE_ID = "AA_A3_B1_u_3_complete_d_candidate"
TARGET_D_VECTOR = {
    "d_minus_p": 3,
    "d_pos_2sqrt_q": 3,
    "d_neg_2sqrt_q": 1,
}

LEDGER_ROUTING_SEMANTICS = {
    "admissible": {
        "can_enter_admissible_point_ledger": True,
        "ledger_route": "admissible_point_ledger",
    },
    "not_admissible": {
        "can_enter_admissible_point_ledger": False,
        "ledger_route": "globally_soluble_but_not_aa_bb_admissible_ledger",
    },
    "missing_pullback_data": {
        "can_enter_admissible_point_ledger": False,
        "ledger_route": "missing_pullback_data_ledger",
    },
    "invalid_input": {
        "can_enter_admissible_point_ledger": False,
        "ledger_route": "invalid_or_unscoped_input_ledger",
    },
}


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl490_ready(wl490: dict[str, Any]) -> bool:
    selected_gate = wl490.get("selected_next_gate", {})
    ledger_update = wl490.get("ledger_update", {})
    killed_candidate = ledger_update.get("killed_candidate", {})
    return (
        wl490.get("status") == "ok"
        and wl490.get("ready") is True
        and wl490.get("lemma_id") == "WL490_route_impact_after_wl489_admissibility_failure"
        and wl490.get("work_log") == "wl490"
        and wl490.get("input_work_log") == "wl489"
        and selected_gate.get("gate") == "define_reusable_ambient_C_d_to_AA_BB_admissibility_filter"
        and selected_gate.get("entered_here") is False
        and killed_candidate.get("candidate_id") == TARGET_CANDIDATE_ID
        and killed_candidate.get("d_vector") == TARGET_D_VECTOR
        and wl490.get("admissibility_filter_defined_here") is False
        and wl490.get("old_package_x_coordinate_collapse_used") is False
        and wl490.get("package_x_s_tilde_bridge_used") is False
        and wl490.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl490.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl490)
    )


def _format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _as_fraction(value: Any) -> Fraction:
    return Fraction(str(value))


def _is_rational_square(value: Fraction) -> bool:
    return (
        value >= 0
        and isqrt(value.numerator) ** 2 == value.numerator
        and isqrt(value.denominator) ** 2 == value.denominator
    )


def _point_level_filter_contract() -> dict[str, Any]:
    return {
        "contract_id": "ambient_global_C_d_point_to_AA_BB_admissible_point",
        "scope": (
            "A reusable point-level filter for any ambient global C_d point "
            "before it can enter the AA+BB admissible-point ledger."
        ),
        "required_inputs": {
            "ambient_global_c_d_point": [
                "candidate_id",
                "quotient in {AA, BB}",
                "A",
                "B",
                "L matching the source quotient leg",
                "point_on_E_L.X",
                "point_on_E_L.Y",
                "parameters.p",
                "parameters.q",
                "complete_d_squareclass",
            ],
            "route_context": [
                "ambient_global_C_d_solubility_already_established",
                "old_package_x_S_tilde_bridge_not_used",
            ],
        },
        "checks_in_order": [
            "input_shape_and_scope",
            "centered_even_pullback",
            "AA_common_source_square_product",
            "BB_common_source_square_product",
            "positivity_and_nondegeneracy",
        ],
        "output_classes": {
            "admissible": "all checks pass",
            "not_admissible": (
                "pullback exists but a square or positivity/nondegeneracy check fails"
            ),
            "missing_pullback_data": (
                "input is scoped but the centered-even pullback cannot be certified"
            ),
            "invalid_input": "required point-level data or route context is missing",
        },
    }


def _u3_regression_point() -> dict[str, Any]:
    return {
        "candidate_id": TARGET_CANDIDATE_ID,
        "quotient": "AA",
        "A": 3,
        "B": 1,
        "L": 3,
        "point_on_E_L": {"X": 152, "Y": 1536},
        "parameters": {"p": 40, "q": 2704, "sqrt_q": 52},
        "complete_d_squareclass": dict(TARGET_D_VECTOR),
        "route_context": {
            "ambient_global_C_d_solubility_already_established": True,
            "old_package_x_S_tilde_bridge_not_used": True,
        },
    }


def _required_input_violations(point: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    required_top = [
        "candidate_id",
        "quotient",
        "A",
        "B",
        "L",
        "point_on_E_L",
        "parameters",
        "complete_d_squareclass",
        "route_context",
    ]
    for key in required_top:
        if key not in point:
            violations.append(f"missing_{key}")

    point_on_e = point.get("point_on_E_L", {})
    for key in ["X", "Y"]:
        if key not in point_on_e:
            violations.append(f"missing_point_on_E_L_{key}")

    params = point.get("parameters", {})
    for key in ["p", "q"]:
        if key not in params:
            violations.append(f"missing_parameters_{key}")

    context = point.get("route_context", {})
    if context.get("ambient_global_C_d_solubility_already_established") is not True:
        violations.append("ambient_global_C_d_solubility_not_established")
    if context.get("old_package_x_S_tilde_bridge_not_used") is not True:
        violations.append("old_package_x_S_tilde_bridge_scope_violation")

    quotient = point.get("quotient")
    if quotient not in {"AA", "BB"}:
        violations.append("quotient_not_centered_even_AA_or_BB")
    elif "L" in point:
        expected_leg = point.get("A") if quotient == "AA" else point.get("B")
        if point.get("L") != expected_leg:
            violations.append("L_does_not_match_source_quotient_leg")

    return violations


def _invalid_result(point: dict[str, Any], violations: list[str]) -> dict[str, Any]:
    route = LEDGER_ROUTING_SEMANTICS["invalid_input"]
    return {
        "candidate_id": point.get("candidate_id", "unknown"),
        "output_class": "invalid_input",
        "can_enter_admissible_point_ledger": route["can_enter_admissible_point_ledger"],
        "ledger_route": route["ledger_route"],
        "blocking_reasons": violations,
    }


def _pullback_check(point: dict[str, Any]) -> dict[str, Any]:
    a = _as_fraction(point["A"])
    b = _as_fraction(point["B"])
    leg = _as_fraction(point["L"])
    x_coord = _as_fraction(point["point_on_E_L"]["X"])
    y_coord = _as_fraction(point["point_on_E_L"]["Y"])
    p = _as_fraction(point["parameters"]["p"])
    q = _as_fraction(point["parameters"]["q"])

    denominator = 2 * (x_coord + p)
    if denominator == 0:
        return {
            "passed": False,
            "reason": "centered_even_inverse_denominator_zero",
        }

    t = y_coord / denominator
    z = x_coord / 2 - t * t
    n = (a + b + t) / 2
    m = a + b - n
    quartic_y = z / 4
    even_rhs = t**4 + p * t * t + q
    source_rhs = (n * n + leg * leg) * (m * m + leg * leg)
    passed = z * z == even_rhs and quartic_y * quartic_y == source_rhs
    return {
        "passed": passed,
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
            "denominator_nonzero": True,
            "even_quartic_identity_holds": z * z == even_rhs,
            "source_quotient_identity_holds": quartic_y * quartic_y == source_rhs,
        },
    }


def _side_square_check(label: str, leg: Fraction, n: Fraction, m: Fraction) -> dict[str, Any]:
    n_term = n * n + leg * leg
    m_term = m * m + leg * leg
    product = n_term * m_term
    return {
        "side": label,
        "N2_plus_leg2": _format_fraction(n_term),
        "M2_plus_leg2": _format_fraction(m_term),
        "product": _format_fraction(product),
        "product_is_square": _is_rational_square(product),
        "individual_square_flags": {
            "N2_plus_leg2": _is_rational_square(n_term),
            "M2_plus_leg2": _is_rational_square(m_term),
        },
    }


def classify_ambient_c_d_point_for_aa_bb_admissibility(
    point: dict[str, Any],
) -> dict[str, Any]:
    """Classify one ambient global C_d point for AA+BB ledger admission."""
    input_violations = _required_input_violations(point)
    if input_violations:
        return _invalid_result(point, input_violations)

    pullback = _pullback_check(point)
    if not pullback.get("passed"):
        route = LEDGER_ROUTING_SEMANTICS["missing_pullback_data"]
        return {
            "candidate_id": point["candidate_id"],
            "output_class": "missing_pullback_data",
            "can_enter_admissible_point_ledger": route["can_enter_admissible_point_ledger"],
            "ledger_route": route["ledger_route"],
            "centered_even_pullback_check": pullback,
            "blocking_reasons": [pullback.get("reason", "centered_even_pullback_failed")],
        }

    values = pullback["values"]
    n = Fraction(values["N"])
    m = Fraction(values["M"])
    a = _as_fraction(point["A"])
    b = _as_fraction(point["B"])
    aa_check = _side_square_check("AA", a, n, m)
    bb_check = _side_square_check("BB", b, n, m)
    positivity = {
        "A_positive": a > 0,
        "B_positive": b > 0,
        "N_positive": n > 0,
        "M_positive": m > 0,
        "nondegenerate_positive_closure_point": (a > 0 and b > 0 and n > 0 and m > 0),
    }

    blocking_reasons: list[str] = []
    if not aa_check["product_is_square"]:
        blocking_reasons.append("AA_common_source_product_not_square")
    if not bb_check["product_is_square"]:
        blocking_reasons.append("BB_common_source_product_not_square")
    if not positivity["A_positive"]:
        blocking_reasons.append("A_not_positive")
    if not positivity["B_positive"]:
        blocking_reasons.append("B_not_positive")
    if not positivity["N_positive"]:
        blocking_reasons.append("N_not_positive")
    if not positivity["M_positive"]:
        blocking_reasons.append("M_not_positive")

    output_class = "admissible" if not blocking_reasons else "not_admissible"
    route = LEDGER_ROUTING_SEMANTICS[output_class]
    return {
        "candidate_id": point["candidate_id"],
        "quotient": point["quotient"],
        "complete_d_squareclass": dict(point["complete_d_squareclass"]),
        "output_class": output_class,
        "can_enter_admissible_point_ledger": route["can_enter_admissible_point_ledger"],
        "ledger_route": route["ledger_route"],
        "centered_even_pullback_check": pullback,
        "common_source_square_checks": {
            "AA": aa_check,
            "BB": bb_check,
        },
        "positivity_nondegeneracy_checks": positivity,
        "blocking_reasons": blocking_reasons,
    }


def build_wl491_ambient_c_d_to_aa_bb_admissibility_filter(
    *, wl490: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl490_ready(wl490):
        violations.append("wl490_input_not_ready_or_not_scoped")

    u3_regression = classify_ambient_c_d_point_for_aa_bb_admissibility(_u3_regression_point())
    if u3_regression.get("output_class") != "not_admissible":
        violations.append("u3_regression_did_not_classify_not_admissible")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl490 selected reusable ambient C_d to AA+BB filter gate",
        "pattern": "AA+BB",
        "lemma_id": "WL491_reusable_ambient_C_d_to_AA_BB_admissibility_filter",
        "work_log": "wl491",
        "input_work_log": "wl490",
        "point_level_filter_contract": _point_level_filter_contract(),
        "ledger_routing_semantics": LEDGER_ROUTING_SEMANTICS,
        "u3_regression": u3_regression if status == "ok" else {},
        "routing_audit_only": True,
        "point_level_admissibility_decided_here": status == "ok",
        "admissibility_filter_defined_here": status == "ok",
        "new_m_tail_or_kernel_candidate_selected_here": False,
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
        "advance_to_wl492": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl490", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl491_ambient_c_d_to_aa_bb_admissibility_filter(wl490=load_json(args.wl490))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl491 admissibility-filter audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    if audit["status"] == "ok":
        print(f"u3_output_class={audit['u3_regression']['output_class']}")
        print(f"advance_to_wl492={audit['advance_to_wl492']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
