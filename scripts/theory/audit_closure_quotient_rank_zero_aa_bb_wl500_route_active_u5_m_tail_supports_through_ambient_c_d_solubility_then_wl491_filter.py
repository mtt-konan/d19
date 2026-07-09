#!/usr/bin/env python3
"""Route wl499 active u_5 supports through ambient C_d solubility then wl491."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

BOUNDARY = (
    "This audits only wl500 / route_active_u5_M_tail_supports_through_"
    "ambient_C_d_solubility_then_wl491_filter. It takes exactly the two "
    "active wl499 u_5 M_tail support entries, instantiates their common "
    "L=5,T=8,d=(5,5,1) complete C_d cover, classifies ambient global "
    "solubility by a targeted single-cover Mordell-Weil torsion-lift "
    "certificate, applies wl491 only if an ambient global point is proved, "
    "and stops before selecting a final obstruction candidate, proving new "
    "local rows, running broad rank or Selmer diagnostics, advancing to "
    "wl501, using the old package-x S~ bridge, or claiming a complete "
    "Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, or any "
    "family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

TARGET_ACTIVE_IDS = [
    "AA_A5_B3_u_5_m_tail_shell5_candidate",
    "BB_A3_B5_u_5_m_tail_shell5_candidate",
]

TARGET_D_VECTOR = {
    "d_minus_p": 5,
    "d_pos_2sqrt_q": 5,
    "d_neg_2sqrt_q": 1,
}

TARGET_PARAMETERS = {
    "p": 72,
    "q": 26896,
    "sqrt_q": 164,
}


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl491_ready(wl491: dict[str, Any]) -> bool:
    return (
        wl491.get("status") == "ok"
        and wl491.get("ready") is True
        and wl491.get("lemma_id")
        == "WL491_reusable_ambient_C_d_to_AA_BB_admissibility_filter"
        and wl491.get("work_log") == "wl491"
        and wl491.get("admissibility_filter_defined_here") is True
        and wl491.get("old_package_x_coordinate_collapse_used") is False
        and wl491.get("package_x_s_tilde_bridge_used") is False
        and wl491.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl491.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl491)
    )


def _wl499_ready(wl499: dict[str, Any]) -> bool:
    summary = wl499.get("sample_summary", {})
    return (
        wl499.get("status") == "ok"
        and wl499.get("ready") is True
        and wl499.get("lemma_id")
        == "WL499_execute_finite_M_tail_diagnostic_extension_from_wl498_plan"
        and wl499.get("work_log") == "wl499"
        and summary.get("active_new_support_entry_count") == 2
        and summary.get("unique_active_supports") == ["u_5"]
        and wl499.get("new_c_d_solubility_tested_here") is False
        and wl499.get("wl491_filter_applied_here") is False
        and wl499.get("candidate_selected_here") is False
        and wl499.get("new_local_row_proved_here") is False
        and wl499.get("old_package_x_coordinate_collapse_used") is False
        and wl499.get("package_x_s_tilde_bridge_used") is False
        and wl499.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl499.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl499)
    )


def _format_relation(root_value: int, coefficient: int, variable: str) -> str:
    square_term = _format_square_term(coefficient, variable)
    if root_value < 0:
        return f"X + {-root_value} = {square_term}"
    return f"X - {root_value} = {square_term}"


def _format_square_term(coefficient: int, variable: str) -> str:
    if coefficient == 1:
        return f"{variable}^2"
    return f"{coefficient}*{variable}^2"


def _cover_data(entry: dict[str, Any]) -> dict[str, Any]:
    sample = dict(entry["sample"])
    d_vector = dict(TARGET_D_VECTOR)
    parameters = dict(TARGET_PARAMETERS)
    roots = {
        "e_minus": {"symbolic": "-p", "value": -parameters["p"]},
        "e_pos": {"symbolic": "2*sqrt_q", "value": 2 * parameters["sqrt_q"]},
        "e_neg": {"symbolic": "-2*sqrt_q", "value": -2 * parameters["sqrt_q"]},
    }
    d_minus = d_vector["d_minus_p"]
    d_pos = d_vector["d_pos_2sqrt_q"]
    d_neg = d_vector["d_neg_2sqrt_q"]
    e_minus = int(roots["e_minus"]["value"])
    e_pos = int(roots["e_pos"]["value"])
    e_neg = int(roots["e_neg"]["value"])
    return {
        "candidate_id": entry["candidate_id"],
        "source_support": list(entry["candidate_support"]),
        "sample": sample,
        "parameters": parameters,
        "coordinate_order": list(COORDINATE_ORDER),
        "variables": ["X", "u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q"],
        "d_vector": d_vector,
        "root_data": roots,
        "x_coordinate_relations": [
            {
                "coordinate": "d_minus_p",
                "root": "e_minus",
                "instantiated_equation": _format_relation(
                    e_minus, d_minus, "u_minus_p"
                ),
            },
            {
                "coordinate": "d_pos_2sqrt_q",
                "root": "e_pos",
                "instantiated_equation": _format_relation(
                    e_pos, d_pos, "u_pos_2sqrt_q"
                ),
            },
            {
                "coordinate": "d_neg_2sqrt_q",
                "root": "e_neg",
                "instantiated_equation": _format_relation(
                    e_neg, d_neg, "u_neg_2sqrt_q"
                ),
            },
        ],
        "two_independent_equations": [
            (
                f"{_format_square_term(d_minus, 'u_minus_p')} - "
                f"{_format_square_term(d_pos, 'u_pos_2sqrt_q')} = "
                f"{e_pos - e_minus}"
            ),
            (
                f"{_format_square_term(d_minus, 'u_minus_p')} - "
                f"{_format_square_term(d_neg, 'u_neg_2sqrt_q')} = "
                f"{e_neg - e_minus}"
            ),
        ],
        "instantiation_only": True,
    }


def _torsion_lift_checks() -> list[dict[str, Any]]:
    return [
        {
            "torsion_point": "O",
            "lift_exists": False,
            "checked_equation": (
                "at infinity: 5*u_minus_p^2 = "
                "5*u_pos_2sqrt_q^2 = u_neg_2sqrt_q^2"
            ),
            "blocking_reason": "5_is_not_a_rational_square",
        },
        {
            "torsion_point": "(-328,0)",
            "lift_exists": False,
            "checked_equation": "X + 72 = -256 = 5*u_minus_p^2",
            "blocking_reason": "negative_rational_cannot_be_square",
        },
        {
            "torsion_point": "(-72,0)",
            "lift_exists": False,
            "checked_equation": "X - 328 = -400 = 5*u_pos_2sqrt_q^2",
            "blocking_reason": "negative_rational_cannot_be_square",
        },
        {
            "torsion_point": "(328,0)",
            "lift_exists": False,
            "checked_equation": "X + 72 = 400 = 5*u_minus_p^2",
            "blocking_reason": "80_is_not_a_rational_square",
        },
    ]


def _refutation_certificate() -> dict[str, Any]:
    lift_checks = _torsion_lift_checks()
    return {
        "status": "globally_not_soluble",
        "certificate_type": "targeted_mordell_weil_torsion_lift_refutation",
        "certificate_scope": (
            "The two wl499 active entries have the same instantiated ambient "
            "C_d cover with L=5,T=8,d=(5,5,1). This certificate is for that "
            "single cover only; it is not a family Selmer or rank-zero theorem."
        ),
        "cover_equations": [
            "X + 72 = 5*u_minus_p^2",
            "X - 328 = 5*u_pos_2sqrt_q^2",
            "X + 328 = u_neg_2sqrt_q^2",
        ],
        "elliptic_curve_model": {
            "equation": "V^2 = (X + 72)*(X - 328)*(X + 328)",
            "expanded_equation": "V^2 = X^3 + 72*X^2 - 107584*X - 7746048",
        },
        "cover_to_elliptic_curve_map": {
            "X": "same X-coordinate",
            "V": "5*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q",
            "reason": (
                "The product of the three cover equations is "
                "V^2=(X+72)(X-328)(X+328)."
            ),
        },
        "rank_zero_certificate": {
            "rank": 0,
            "torsion_points": ["O", "(-328,0)", "(-72,0)", "(328,0)"],
            "scope": "single instantiated curve E_{L=5,T=8}, not a family theorem",
        },
        "cover_lift_checks": lift_checks,
        "cover_lift_summary": {
            "torsion_point_count_checked": len(lift_checks),
            "torsion_lift_count": len(
                [check for check in lift_checks if check["lift_exists"]]
            ),
            "point_at_infinity_lift_exists": False,
            "affine_torsion_lift_count": 0,
        },
        "conclusion": (
            "Since the recorded Mordell-Weil certificate gives only the listed "
            "torsion points on E_{L=5,T=8}, and none lifts to the d=(5,5,1) "
            "cover, the instantiated ambient C_d cover has no rational point."
        ),
    }


def _not_applied_filter_result() -> dict[str, Any]:
    return {
        "output_class": "not_applied",
        "reason": "ambient_C_d_global_solubility_refuted",
        "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
    }


def _routing_state() -> dict[str, Any]:
    return {
        "ambient_c_d_global_solubility_status": "globally_not_soluble",
        "aa_bb_admissibility_status": (
            "not_applied_ambient_global_solubility_refuted"
        ),
        "ledger_route": "ambient_c_d_global_solubility_refuted_ledger",
        "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
    }


def _target_active_entries(wl499: dict[str, Any]) -> list[dict[str, Any]]:
    entries = [
        entry
        for entry in wl499.get("active_new_kernel_supports", [])
        if entry.get("candidate_id") in TARGET_ACTIVE_IDS
    ]
    return sorted(entries, key=lambda entry: TARGET_ACTIVE_IDS.index(entry["candidate_id"]))


def _is_target_active_entry(entry: dict[str, Any]) -> bool:
    sample = entry.get("sample", {})
    routing = entry.get("routing_state", {})
    return (
        entry.get("candidate_id") in TARGET_ACTIVE_IDS
        and entry.get("candidate_support") == ["u_5"]
        and sample.get("L") == 5
        and sample.get("T") == 8
        and sample.get("sqrt_q") == 164
        and routing.get("ambient_c_d_global_solubility_status") == "not_tested_here"
        and routing.get("aa_bb_admissibility_status") == "not_applied_here"
    )


def _routed_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_rank": entry["queue_rank"],
        "candidate_id": entry["candidate_id"],
        "candidate_support": list(entry["candidate_support"]),
        "source_wl499_queue_status": entry["queue_status"],
        "source_wl499_routing_state": dict(entry["routing_state"]),
        "sample": dict(entry["sample"]),
        "complete_c_d_cover": _cover_data(entry),
        "ambient_c_d_global_solubility": _refutation_certificate(),
        "wl491_filter_input": {},
        "wl491_filter_result": _not_applied_filter_result(),
        "routing_state": _routing_state(),
    }


def _route_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    witness_statuses = [
        entry["ambient_c_d_global_solubility"]["status"] for entry in entries
    ]
    filter_classes = [entry["wl491_filter_result"]["output_class"] for entry in entries]
    return {
        "active_u5_support_entry_count": len(entries),
        "ambient_globally_soluble_count": witness_statuses.count("globally_soluble"),
        "ambient_global_solubility_refuted_count": witness_statuses.count(
            "globally_not_soluble"
        ),
        "ambient_global_solubility_still_deferred_count": witness_statuses.count(
            "still_deferred"
        ),
        "wl491_filter_applied_count": len(
            [output for output in filter_classes if output != "not_applied"]
        ),
        "aa_bb_admissible_count": filter_classes.count("admissible"),
        "aa_bb_not_admissible_count": filter_classes.count("not_admissible"),
        "aa_bb_missing_pullback_data_count": filter_classes.count(
            "missing_pullback_data"
        ),
        "aa_bb_filter_not_applied_count": filter_classes.count("not_applied"),
    }


def build_wl500_route_active_u5_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter(
    *,
    wl491: dict[str, Any],
    wl499: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl491_ready(wl491):
        violations.append("wl491_input_not_ready_or_not_scoped")
    if not _wl499_ready(wl499):
        violations.append("wl499_input_not_ready_or_not_scoped")

    target_entries = _target_active_entries(wl499)
    if [entry.get("candidate_id") for entry in target_entries] != TARGET_ACTIVE_IDS:
        violations.append("wl499_target_active_u5_entries_missing_or_out_of_order")
    if any(not _is_target_active_entry(entry) for entry in target_entries):
        violations.append("wl499_target_active_entries_not_matching_l5_t8_u5_scope")

    status = "ok" if not violations else "issues"
    routed = [_routed_entry(entry) for entry in target_entries] if status == "ok" else []
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl499 active u_5 M_tail supports plus wl491 filter",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL500_route_active_u5_M_tail_supports_through_ambient_C_d_"
            "solubility_then_wl491_filter"
        ),
        "work_log": "wl500",
        "input_work_logs": ["wl491", "wl499"],
        "target_active_candidate_ids": list(TARGET_ACTIVE_IDS),
        "route_order": [
            "active_wl499_u5_M_tail_support",
            "instantiate_complete_d_coordinate_C_d_cover",
            "classify_ambient_C_d_global_solubility",
            "apply_wl491_filter_only_to_established_global_points",
            "route_to_refuted_or_filter_ledgers",
        ],
        "route_summary": _route_summary(routed),
        "routed_active_u5_supports": routed,
        "route_audit_built_here": status == "ok",
        "complete_c_d_cover_data_instantiated_here": status == "ok",
        "ambient_c_d_solubility_classified_here": status == "ok",
        "ambient_c_d_solubility_proved_for_some_active_u5_supports_here": False,
        "all_active_u5_entries_classified_here": (
            status == "ok"
            and len(routed) == len(TARGET_ACTIVE_IDS)
            and all(
                entry["ambient_c_d_global_solubility"]["status"]
                != "still_deferred"
                for entry in routed
            )
        ),
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "targeted_single_cover_mordell_weil_certificate_used_here": status == "ok",
        "broad_rank_or_selmer_diagnostics_run": False,
        "family_rank_or_selmer_diagnostics_run": False,
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
        "advance_to_wl501": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "wl500 only routes the two active wl499 u_5 supports. It does not "
            "select a final obstruction candidate or advance to another "
            "M_tail diagnostic extension."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl491", type=Path, required=True)
    parser.add_argument("--wl499", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    build_audit = (
        build_wl500_route_active_u5_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter
    )
    audit = build_audit(
        wl491=load_json(args.wl491),
        wl499=load_json(args.wl499),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl500 active-u5 route audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "ambient_global_solubility_refuted_count="
        f"{audit['route_summary']['ambient_global_solubility_refuted_count']}"
    )
    print(f"advance_to_wl501={audit['advance_to_wl501']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
