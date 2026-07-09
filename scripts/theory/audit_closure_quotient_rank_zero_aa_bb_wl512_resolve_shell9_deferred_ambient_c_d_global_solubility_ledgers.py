#!/usr/bin/env python3
"""Resolve wl511 deferred shell-9 ambient C_d global-solubility ledgers."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl512 / resolve_shell9_deferred_ambient_C_d_global_"
    "solubility_ledgers. It takes wl511 as input, classifies exactly the four "
    "deferred shell-9 ambient C_d ledgers, does not re-open the four shell-9 "
    "globally soluble but not AA+BB-admissible ledgers or any closed ledger "
    "through wl511, routes the two v_13 entries to the ambient global-"
    "solubility refuted ledger by a targeted Mordell-Weil torsion-lift "
    "certificate, keeps the two u_7 entries deferred with an explicit "
    "missing-certificate reason, and stops before executing shell 10, "
    "selecting a final obstruction candidate, proving new local rows, running "
    "broad rank or Selmer diagnostics, advancing to wl513, using the old "
    "package-x S~ bridge, or claiming a complete Sel_2(E) upper bound, "
    "dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform M_tail full rank, or any "
    "family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

TARGET_DEFERRED_IDS = [
    "AA_A4_B9_v_13_m_tail_shell9_candidate",
    "AA_A7_B9_u_7_m_tail_shell9_candidate",
    "BB_A9_B4_v_13_m_tail_shell9_candidate",
    "BB_A9_B7_u_7_m_tail_shell9_candidate",
]

REFUTED_V13_IDS = [
    "AA_A4_B9_v_13_m_tail_shell9_candidate",
    "BB_A9_B4_v_13_m_tail_shell9_candidate",
]

DEFERRED_U7_IDS = [
    "AA_A7_B9_u_7_m_tail_shell9_candidate",
    "BB_A9_B7_u_7_m_tail_shell9_candidate",
]

SHELL9_NOT_ADMISSIBLE_IDS_FROM_WL511 = [
    "AA_A9_B1_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate",
    "AA_A9_B4_v_13_m_tail_shell9_candidate",
    "BB_A1_B9_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate",
    "BB_A4_B9_v_13_m_tail_shell9_candidate",
]

V13_D_VECTOR = {
    "d_minus_p": 13,
    "d_pos_2sqrt_q": 1,
    "d_neg_2sqrt_q": 13,
}

V13_PARAMETERS = {
    "p": -210,
    "q": 54289,
    "sqrt_q": 233,
}

U7_D_VECTOR = {
    "d_minus_p": 7,
    "d_pos_2sqrt_q": 7,
    "d_neg_2sqrt_q": 1,
}

U7_PARAMETERS = {
    "p": -120,
    "q": 204304,
    "sqrt_q": 452,
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


def _wl511_ready(wl511: dict[str, Any]) -> bool:
    summary = wl511.get("route_summary", {})
    return (
        wl511.get("status") == "ok"
        and wl511.get("ready") is True
        and wl511.get("lemma_id")
        == (
            "WL511_route_active_shell9_M_tail_supports_through_ambient_C_d_"
            "solubility_then_wl491_filter"
        )
        and wl511.get("work_log") == "wl511"
        and summary.get("active_shell9_support_entry_count") == 8
        and summary.get("ambient_globally_soluble_count") == 4
        and summary.get("ambient_global_solubility_deferred_count") == 4
        and summary.get("aa_bb_filter_deferred_count") == 4
        and wl511.get("all_active_shell9_supports_fully_routed_here") is False
        and wl511.get("candidate_selected_here") is False
        and wl511.get("new_m_tail_row_proved_here") is False
        and wl511.get("new_local_row_proved_here") is False
        and wl511.get("shell10_executed_here") is False
        and wl511.get("old_package_x_coordinate_collapse_used") is False
        and wl511.get("package_x_s_tilde_bridge_used") is False
        and wl511.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl511.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl511)
    )


def _target_deferred_entries(wl511: dict[str, Any]) -> list[dict[str, Any]]:
    entries = [
        entry
        for entry in wl511.get("routed_active_shell9_supports", [])
        if entry.get("candidate_id") in TARGET_DEFERRED_IDS
    ]
    return sorted(entries, key=lambda entry: TARGET_DEFERRED_IDS.index(entry["candidate_id"]))


def _globally_soluble_not_admissible_ids(wl511: dict[str, Any]) -> list[str]:
    return [
        entry["candidate_id"]
        for entry in wl511.get("routed_active_shell9_supports", [])
        if entry.get("ambient_c_d_global_solubility", {}).get("status")
        == "globally_soluble"
    ]


def _is_deferred_target(entry: dict[str, Any]) -> bool:
    return (
        entry.get("ambient_c_d_global_solubility", {}).get("status")
        == "global_solubility_deferred"
        and entry.get("wl491_filter_result", {}).get("output_class") == "not_applied"
        and entry.get("routing_state", {}).get("ledger_route")
        == "ambient_c_d_solubility_deferred_ledger"
    )


def _is_v13_target(entry: dict[str, Any]) -> bool:
    return (
        entry.get("candidate_id") in REFUTED_V13_IDS
        and entry.get("candidate_support") == ["v_13"]
        and entry.get("complete_c_d_cover", {}).get("d_vector") == V13_D_VECTOR
        and entry.get("complete_c_d_cover", {}).get("parameters") == V13_PARAMETERS
        and _is_deferred_target(entry)
    )


def _is_u7_target(entry: dict[str, Any]) -> bool:
    return (
        entry.get("candidate_id") in DEFERRED_U7_IDS
        and entry.get("candidate_support") == ["u_7"]
        and entry.get("complete_c_d_cover", {}).get("d_vector") == U7_D_VECTOR
        and entry.get("complete_c_d_cover", {}).get("parameters") == U7_PARAMETERS
        and _is_deferred_target(entry)
    )


def _v13_refutation_certificate() -> dict[str, Any]:
    lift_checks = [
        {
            "torsion_point": "O",
            "lift_exists": False,
            "checked_equation": (
                "at infinity: 13*u_minus_p^2 = "
                "u_pos_2sqrt_q^2 = 13*u_neg_2sqrt_q^2"
            ),
            "blocking_reason": "13_is_not_a_rational_square",
        },
        {
            "torsion_point": "(-466,0)",
            "lift_exists": False,
            "checked_equation": "X - 210 = -676 = 13*u_minus_p^2",
            "blocking_reason": "negative_rational_cannot_be_square",
        },
        {
            "torsion_point": "(210,0)",
            "lift_exists": False,
            "checked_equation": "X - 466 = -256 = u_pos_2sqrt_q^2",
            "blocking_reason": "negative_rational_cannot_be_square",
        },
        {
            "torsion_point": "(466,0)",
            "lift_exists": False,
            "checked_equation": "X - 210 = 256 = 13*u_minus_p^2",
            "blocking_reason": "256_over_13_is_not_a_rational_square",
        },
    ]
    return {
        "status": "globally_not_soluble",
        "certificate_type": "targeted_mordell_weil_torsion_lift_refutation",
        "certificate_scope": (
            "The two v_13 wl511 deferred entries have the same instantiated "
            "ambient C_d cover with L=4,T=13,d=(13,1,13). This certificate is "
            "for that single cover only; it is not a family Selmer or "
            "rank-zero theorem."
        ),
        "cover_equations": [
            "X - 210 = 13*u_minus_p^2",
            "X - 466 = u_pos_2sqrt_q^2",
            "X + 466 = 13*u_neg_2sqrt_q^2",
        ],
        "elliptic_curve_model": {
            "equation": "V^2 = (X - 210)*(X - 466)*(X + 466)",
            "expanded_equation": "V^2 = X^3 - 210*X^2 - 217156*X + 45602760",
        },
        "cover_to_elliptic_curve_map": {
            "X": "same X-coordinate",
            "V": "13*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q",
            "reason": (
                "The product of the three cover equations is "
                "V^2=(X-210)(X-466)(X+466)."
            ),
        },
        "rank_zero_certificate": {
            "rank": 0,
            "torsion_points": ["O", "(-466,0)", "(210,0)", "(466,0)"],
            "scope": "single instantiated curve E_{L=4,T=13}, not a family theorem",
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
            "torsion points on E_{L=4,T=13}, and none lifts to the d=(13,1,13) "
            "cover, the instantiated ambient C_d cover has no rational point."
        ),
    }


def _u7_still_deferred_certificate() -> dict[str, Any]:
    return {
        "status": "global_solubility_deferred",
        "certificate_type": "none_recorded_here",
        "deferred_reason": (
            "rank_one_ambient_curve_has_no_exhaustive_cover_lift_certificate_here"
        ),
        "certificate_scope": (
            "The two u_7 wl511 deferred entries have the same instantiated "
            "ambient C_d cover with L=7,T=16,d=(7,7,1). wl512 records the "
            "cover data and the currently missing certificate only; it is not "
            "a global insolubility theorem and not a family Selmer or rank "
            "statement."
        ),
        "cover_equations": [
            "X + 120 = 7*u_minus_p^2",
            "X - 904 = 7*u_pos_2sqrt_q^2",
            "X + 904 = u_neg_2sqrt_q^2",
        ],
        "elliptic_curve_model": {
            "equation": "V^2 = (X + 120)*(X - 904)*(X + 904)",
            "expanded_equation": "V^2 = X^3 + 120*X^2 - 817216*X - 98065920",
        },
        "cover_to_elliptic_curve_map": {
            "X": "same X-coordinate",
            "V": "7*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q",
            "reason": (
                "The product of the three cover equations is "
                "V^2=(X+120)(X-904)(X+904)."
            ),
        },
        "mordell_weil_status_recorded_here": {
            "rank": 1,
            "generator_recorded": "G=(1032,16896)",
            "torsion_points": ["O", "(-904,0)", "(-120,0)", "(904,0)"],
            "scope": (
                "single instantiated curve E_{L=7,T=16}; this is not a "
                "family rank or Selmer diagnostic"
            ),
        },
        "bounded_mordell_weil_probe": {
            "generator_multiple_bound": 200,
            "torsion_translates_checked": 4,
            "cover_lift_found": False,
            "not_a_global_insolubility_proof": True,
        },
        "blocking_reasons": [
            "ambient_C_d_global_point_not_established",
            "no_Mordell_Weil_sieve_or_exhaustive_cover_lift_certificate_recorded_here",
        ],
        "deferred_to": "shell9_u7_ambient_C_d_global_solubility_ledger",
        "evidence_scope": (
            "The bounded Mordell-Weil probe is only route information. Without "
            "an exact cover point or an exhaustive no-lift certificate, the "
            "ambient C_d global-solubility ledger remains genuinely deferred."
        ),
    }


def _not_applied_filter_result_for_refuted() -> dict[str, Any]:
    return {
        "output_class": "not_applied",
        "reason": "ambient_C_d_global_solubility_refuted",
        "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
    }


def _not_applied_filter_result_for_deferred() -> dict[str, Any]:
    return {
        "output_class": "not_applied",
        "reason": "ambient_global_C_d_solubility_not_established",
        "blocking_reasons": ["ambient_C_d_global_point_not_established"],
    }


def _refuted_routing_state() -> dict[str, Any]:
    return {
        "ambient_c_d_global_solubility_status": "globally_not_soluble",
        "aa_bb_admissibility_status": (
            "not_applied_ambient_global_solubility_refuted"
        ),
        "ledger_route": "ambient_c_d_global_solubility_refuted_ledger",
        "blocking_reasons": ["ambient_C_d_has_no_rational_point"],
    }


def _deferred_routing_state() -> dict[str, Any]:
    return {
        "ambient_c_d_global_solubility_status": "global_solubility_deferred",
        "aa_bb_admissibility_status": (
            "not_applied_ambient_global_solubility_unproved"
        ),
        "ledger_route": "ambient_c_d_solubility_deferred_ledger",
        "blocking_reasons": ["ambient_C_d_global_point_not_established"],
    }


def _classified_entry(entry: dict[str, Any]) -> dict[str, Any]:
    base = {
        "route_rank": entry["route_rank"],
        "candidate_id": entry["candidate_id"],
        "candidate_support": list(entry["candidate_support"]),
        "source_wl511_routing_state": dict(entry["routing_state"]),
        "sample": dict(entry["sample"]),
        "complete_c_d_cover": dict(entry["complete_c_d_cover"]),
    }
    if entry["candidate_id"] in REFUTED_V13_IDS:
        return {
            **base,
            "ambient_c_d_global_solubility": _v13_refutation_certificate(),
            "wl491_filter_input": {},
            "wl491_filter_result": _not_applied_filter_result_for_refuted(),
            "routing_state": _refuted_routing_state(),
        }

    return {
        **base,
        "ambient_c_d_global_solubility": _u7_still_deferred_certificate(),
        "wl491_filter_input": {},
        "wl491_filter_result": _not_applied_filter_result_for_deferred(),
        "routing_state": _deferred_routing_state(),
    }


def _resolution_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    witness_statuses = [
        entry["ambient_c_d_global_solubility"]["status"] for entry in entries
    ]
    filter_classes = [entry["wl491_filter_result"]["output_class"] for entry in entries]
    return {
        "wl511_deferred_entry_count": len(entries),
        "explicitly_classified_entry_count": len(entries),
        "ambient_globally_soluble_count": witness_statuses.count("globally_soluble"),
        "ambient_global_solubility_refuted_count": witness_statuses.count(
            "globally_not_soluble"
        ),
        "ambient_global_solubility_still_deferred_count": witness_statuses.count(
            "global_solubility_deferred"
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


def build_wl512_resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers(
    *,
    wl491: dict[str, Any],
    wl511: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl491_ready(wl491):
        violations.append("wl491_input_not_ready_or_not_scoped")
    if not _wl511_ready(wl511):
        violations.append("wl511_input_not_ready_or_not_scoped")

    target_entries = _target_deferred_entries(wl511)
    not_admissible_ids = _globally_soluble_not_admissible_ids(wl511)
    if [entry.get("candidate_id") for entry in target_entries] != TARGET_DEFERRED_IDS:
        violations.append("wl511_target_deferred_entries_missing_or_out_of_order")
    if any(
        not (_is_v13_target(entry) or _is_u7_target(entry))
        for entry in target_entries
    ):
        violations.append("wl511_target_deferred_entries_not_matching_expected_covers")
    if not_admissible_ids != SHELL9_NOT_ADMISSIBLE_IDS_FROM_WL511:
        violations.append("wl511_not_admissible_ledgers_not_preserved")

    status = "ok" if not violations else "issues"
    classified = (
        [_classified_entry(entry) for entry in target_entries] if status == "ok" else []
    )

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl511 deferred shell-9 ambient C_d global-solubility ledgers",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL512_resolve_shell9_deferred_ambient_C_d_global_solubility_ledgers"
        ),
        "work_log": "wl512",
        "input_work_logs": ["wl491", "wl511"],
        "target_deferred_candidate_ids": list(TARGET_DEFERRED_IDS),
        "do_not_reopen_candidate_ids": {
            "shell9_globally_soluble_not_admissible_from_wl511": list(
                not_admissible_ids
            ),
            "closed_ledgers_through_wl511": [
                "u_3_processed_or_deprioritized_after_wl493_wl491",
                "bounded_v_5_entries_disposed_by_wl495_wl496",
                "shell5_u_5_entries_refuted_by_wl500",
                "shell7_entries_disposed_by_wl505_wl506",
                "shell8_pure_u_3_processed_exclusions_from_wl508",
                "four_shell9_not_admissible_ledgers_from_wl511",
            ],
        },
        "shell9_globally_soluble_not_admissible_reopened_count": 0,
        "closed_ledgers_reopened_count": 0,
        "resolution_method": {
            "kind": "targeted_single_cover_classification",
            "v13_cover": (
                "L=4,T=13,d=(13,1,13) refuted by a rank-zero "
                "torsion-lift certificate"
            ),
            "u7_cover": (
                "L=7,T=16,d=(7,7,1) remains deferred because no exact "
                "ambient C_d point or exhaustive no-lift certificate is "
                "recorded here"
            ),
            "wl491_filter_policy": (
                "not applied because no wl512 entry has ambient C_d global "
                "solubility established here"
            ),
            "new_local_row_added": False,
            "broad_family_rank_or_selmer_diagnostic": False,
        },
        "resolution_summary": _resolution_summary(classified),
        "classified_deferred_entries": classified,
        "classified_wl511_deferred_ledgers_here": status == "ok",
        "all_wl511_deferred_entries_resolved_here": (
            status == "ok"
            and len(classified) == len(TARGET_DEFERRED_IDS)
            and all(
                entry["ambient_c_d_global_solubility"]["status"]
                != "global_solubility_deferred"
                for entry in classified
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
        "uniform_m_tail_full_rank_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "search_count_used_as_progress": False,
        "shell10_executed_here": False,
        "advance_to_wl513": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "wl512 refutes the two v_13 shell-9 deferred ledgers but leaves "
            "the two u_7 shell-9 ambient C_d global-solubility ledgers "
            "genuinely deferred. It does not execute shell 10, select a final "
            "obstruction candidate, prove a local row, run theorem-level "
            "Selmer diagnostics, or choose the next roadmap step."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl491", type=Path, required=True)
    parser.add_argument("--wl511", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl512_resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers(
        wl491=load_json(args.wl491),
        wl511=load_json(args.wl511),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl512 shell9 deferred-ledger audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "ambient_global_solubility_refuted_count="
        f"{audit['resolution_summary']['ambient_global_solubility_refuted_count']}"
    )
    print(
        "ambient_global_solubility_still_deferred_count="
        f"{audit['resolution_summary']['ambient_global_solubility_still_deferred_count']}"
    )
    print(f"advance_to_wl513={audit['advance_to_wl513']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
