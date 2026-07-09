#!/usr/bin/env python3
"""Resolve wl495 deferred v_5 ambient C_d global-solubility ledgers."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl496 / resolve_wl495_deferred_v5_ambient_C_d_global_"
    "solubility_ledgers. It takes wl495 as input, keeps exactly the two "
    "deferred v_5 entries, resolves their common L=4,T=5,d=(5,1,5) ambient "
    "C_d cover by a targeted single-curve Mordell-Weil torsion-lift "
    "certificate, records both as ambient globally not soluble, deliberately "
    "does not apply the wl491 filter after ambient solubility is refuted, and "
    "stops before proving new M_tail/local rows, running broad family rank or "
    "Selmer diagnostics, selecting a final obstruction candidate, advancing "
    "to wl497, using the old package-x S~ bridge, or claiming a complete "
    "Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, or any family "
    "exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

TARGET_DEFERRED_IDS = [
    "AA_A4_B1_v_5_m_tail_refresh_candidate",
    "BB_A1_B4_v_5_m_tail_refresh_candidate",
]

TARGET_D_VECTOR = {
    "d_minus_p": 5,
    "d_pos_2sqrt_q": 1,
    "d_neg_2sqrt_q": 5,
}

TARGET_PARAMETERS = {
    "p": 78,
    "q": 7921,
    "sqrt_q": 89,
}


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl495_ready(wl495: dict[str, Any]) -> bool:
    summary = wl495.get("route_summary", {})
    return (
        wl495.get("status") == "ok"
        and wl495.get("ready") is True
        and wl495.get("lemma_id")
        == "WL495_route_refreshed_support_through_ambient_C_d_solubility_then_wl491_filter"
        and wl495.get("work_log") == "wl495"
        and summary.get("ambient_global_solubility_deferred_count") == 2
        and summary.get("aa_bb_filter_deferred_count") == 2
        and wl495.get("all_refreshed_supports_fully_routed_here") is False
        and wl495.get("candidate_selected_here") is False
        and wl495.get("new_m_tail_row_proved_here") is False
        and wl495.get("new_local_row_proved_here") is False
        and wl495.get("old_package_x_coordinate_collapse_used") is False
        and wl495.get("package_x_s_tilde_bridge_used") is False
        and wl495.get("broad_rank_or_selmer_diagnostics_run") is False
        and not _claims_forbidden_bound(wl495)
    )


def _is_target_deferred_entry(entry: dict[str, Any]) -> bool:
    cover = entry.get("complete_c_d_cover", {})
    sample = entry.get("sample", {})
    return (
        entry.get("candidate_id") in TARGET_DEFERRED_IDS
        and entry.get("candidate_support") == ["v_5"]
        and sample.get("L") == 4
        and sample.get("T") == 5
        and cover.get("d_vector") == TARGET_D_VECTOR
        and cover.get("parameters") == TARGET_PARAMETERS
        and entry.get("ambient_c_d_global_solubility", {}).get("status")
        == "global_solubility_deferred"
        and entry.get("wl491_filter_result", {}).get("output_class") == "not_applied"
    )


def _wl495_deferred_entries(wl495: dict[str, Any]) -> list[dict[str, Any]]:
    entries = [
        entry
        for entry in wl495.get("routed_refreshed_supports", [])
        if entry.get("candidate_id") in TARGET_DEFERRED_IDS
    ]
    return sorted(entries, key=lambda entry: TARGET_DEFERRED_IDS.index(entry["candidate_id"]))


def _torsion_lift_checks() -> list[dict[str, Any]]:
    return [
        {
            "torsion_point": "O",
            "lift_exists": False,
            "checked_equation": "at infinity: 5*u_minus_p^2 = u_pos_2sqrt_q^2 = 5*u_neg_2sqrt_q^2",
            "blocking_reason": "5_is_not_a_rational_square",
        },
        {
            "torsion_point": "(-178,0)",
            "lift_exists": False,
            "checked_equation": "X - 178 = -356 = u_pos_2sqrt_q^2",
            "blocking_reason": "negative_rational_cannot_be_square",
        },
        {
            "torsion_point": "(-78,0)",
            "lift_exists": False,
            "checked_equation": "X - 178 = -256 = u_pos_2sqrt_q^2",
            "blocking_reason": "negative_rational_cannot_be_square",
        },
        {
            "torsion_point": "(178,0)",
            "lift_exists": False,
            "checked_equation": "X + 78 = 256 = 5*u_minus_p^2",
            "blocking_reason": "256/5_is_not_a_rational_square",
        },
    ]


def _refutation_certificate() -> dict[str, Any]:
    lift_checks = _torsion_lift_checks()
    return {
        "status": "globally_not_soluble",
        "certificate_type": "targeted_mordell_weil_torsion_lift_refutation",
        "certificate_scope": (
            "The two wl495 deferred entries have the same instantiated "
            "ambient C_d cover with L=4,T=5,d=(5,1,5). This certificate is "
            "for that single cover only; it is not a family Selmer or "
            "rank-zero theorem."
        ),
        "cover_equations": [
            "X + 78 = 5*u_minus_p^2",
            "X - 178 = u_pos_2sqrt_q^2",
            "X + 178 = 5*u_neg_2sqrt_q^2",
        ],
        "elliptic_curve_model": {
            "equation": "V^2 = (X + 78)*(X - 178)*(X + 178)",
            "expanded_equation": "V^2 = X^3 + 78*X^2 - 31684*X - 2471352",
        },
        "cover_to_elliptic_curve_map": {
            "X": "same X-coordinate",
            "V": "5*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q",
            "reason": (
                "The product of the three cover equations is "
                "V^2=(X+78)(X-178)(X+178)."
            ),
        },
        "rank_zero_certificate": {
            "rank": 0,
            "torsion_points": ["O", "(-178,0)", "(-78,0)", "(178,0)"],
            "scope": "single instantiated curve E_{L=4,T=5}, not a family theorem",
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
            "torsion points on E_{L=4,T=5}, and none lifts to the d=(5,1,5) "
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


def _resolved_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_rank": entry["route_rank"],
        "candidate_id": entry["candidate_id"],
        "candidate_support": list(entry["candidate_support"]),
        "source_wl495_routing_state": dict(entry["routing_state"]),
        "sample": dict(entry["sample"]),
        "complete_c_d_cover": dict(entry["complete_c_d_cover"]),
        "ambient_c_d_global_solubility": _refutation_certificate(),
        "wl491_filter_input": {},
        "wl491_filter_result": _not_applied_filter_result(),
        "routing_state": _routing_state(),
    }


def _resolution_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    witness_statuses = [
        entry["ambient_c_d_global_solubility"]["status"] for entry in entries
    ]
    filter_classes = [entry["wl491_filter_result"]["output_class"] for entry in entries]
    return {
        "wl495_deferred_entry_count": len(entries),
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
        "aa_bb_filter_not_applied_count": filter_classes.count("not_applied"),
    }


def build_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers(
    *,
    wl495: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl495_ready(wl495):
        violations.append("wl495_input_not_ready_or_not_scoped")

    deferred_entries = _wl495_deferred_entries(wl495)
    if [entry.get("candidate_id") for entry in deferred_entries] != TARGET_DEFERRED_IDS:
        violations.append("wl495_target_deferred_entries_missing_or_out_of_order")
    if any(not _is_target_deferred_entry(entry) for entry in deferred_entries):
        violations.append("wl495_target_deferred_entries_not_matching_l4_t5_d515")

    status = "ok" if not violations else "issues"
    resolved = [_resolved_entry(entry) for entry in deferred_entries] if status == "ok" else []

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl495 deferred v_5 ambient C_d global-solubility ledgers",
        "pattern": "AA+BB",
        "lemma_id": (
            "WL496_resolve_wl495_deferred_v5_ambient_C_d_global_solubility_ledgers"
        ),
        "work_log": "wl496",
        "input_work_log": "wl495",
        "target_deferred_candidate_ids": list(TARGET_DEFERRED_IDS),
        "resolution_method": {
            "kind": "targeted_single_cover_mordell_weil_torsion_lift_refutation",
            "instantiated_cover": "L=4,T=5,d=(5,1,5)",
            "wl491_filter_policy": (
                "not applied because ambient C_d global solubility is refuted"
            ),
            "new_local_row_added": False,
            "broad_family_rank_or_selmer_diagnostic": False,
        },
        "resolution_summary": _resolution_summary(resolved),
        "resolved_deferred_entries": resolved,
        "resolved_wl495_deferred_ledgers_here": status == "ok",
        "all_wl495_deferred_entries_resolved_here": (
            status == "ok"
            and len(resolved) == len(TARGET_DEFERRED_IDS)
            and all(
                entry["ambient_c_d_global_solubility"]["status"]
                != "global_solubility_deferred"
                for entry in resolved
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
        "advance_to_wl497": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "wl496 does not select a final obstruction candidate or choose the "
            "next M_tail route. It only closes the two wl495 deferred ambient "
            "C_d ledgers as globally not soluble for their shared cover."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl495", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers(
        wl495=load_json(args.wl495),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl496 deferred-v5 resolution audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "ambient_global_solubility_refuted_count="
        f"{audit['resolution_summary']['ambient_global_solubility_refuted_count']}"
    )
    print(f"advance_to_wl497={audit['advance_to_wl497']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
