#!/usr/bin/env python3
"""Select the wl492 route after the wl491 admissibility filter."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl492 / route selection after the reusable ambient-C_d "
    "to AA+BB admissibility filter. It uses wl491 as input, observes that the "
    "only currently known ambient C_d point in that input is the u_3 regression "
    "already classified as not_admissible, and selects the next narrow route: "
    "build a candidate queue from existing M_tail diagnostics. It does not "
    "build that queue, does not select or prove a new M_tail/kernel candidate, "
    "does not run broad rank or Selmer diagnostics, does not use the old "
    "package-x S~ bridge, does not run single-curve diagnostics, does not prove "
    "a complete Sel_2(E) upper bound, and does not claim dim Sel_2(E)=2, rank "
    "zero, Sha[2]=0, full Mordell-Weil torsion, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

TARGET_CANDIDATE_ID = "AA_A3_B1_u_3_complete_d_candidate"


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl491_ready(wl491: dict[str, Any]) -> bool:
    contract = wl491.get("point_level_filter_contract", {})
    u3 = wl491.get("u3_regression", {})
    return (
        wl491.get("status") == "ok"
        and wl491.get("ready") is True
        and wl491.get("lemma_id") == "WL491_reusable_ambient_C_d_to_AA_BB_admissibility_filter"
        and wl491.get("work_log") == "wl491"
        and wl491.get("input_work_log") == "wl490"
        and contract.get("contract_id") == "ambient_global_C_d_point_to_AA_BB_admissible_point"
        and wl491.get("admissibility_filter_defined_here") is True
        and u3.get("candidate_id") == TARGET_CANDIDATE_ID
        and u3.get("output_class") == "not_admissible"
        and u3.get("can_enter_admissible_point_ledger") is False
        and u3.get("ledger_route") == "globally_soluble_but_not_aa_bb_admissible_ledger"
        and wl491.get("old_package_x_coordinate_collapse_used") is False
        and wl491.get("package_x_s_tilde_bridge_used") is False
        and wl491.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl491.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl491)
    )


def _known_ambient_filter_status(wl491: dict[str, Any]) -> dict[str, Any]:
    u3 = wl491["u3_regression"]
    return {
        "known_filtered_point_count": 1,
        "admissible_point_count": 0,
        "not_admissible_point_count": 1,
        "missing_pullback_data_count": 0,
        "invalid_input_count": 0,
        "unfiltered_already_known_ambient_c_d_point_count": 0,
        "current_admissible_point_ledger_entries": [],
        "globally_soluble_but_not_aa_bb_admissible_entries": [
            {
                "candidate_id": u3["candidate_id"],
                "output_class": u3["output_class"],
                "ledger_route": u3["ledger_route"],
                "blocking_reasons": list(u3["blocking_reasons"]),
            }
        ],
    }


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "first_apply_filter_to_already_known_ambient_C_d_point_ledgers": {
            "decision": "already_exhausted_for_current_inputs",
            "reason": (
                "The only currently known ambient C_d point in the wl491 input "
                "is the u_3 regression, and wl491 already routes it as "
                "not_admissible."
            ),
        },
        "return_directly_to_M_tail_kernel_candidate_discovery": {
            "decision": "defer",
            "reason": (
                "Direct discovery is allowed later, but after one killed "
                "ambient point the next controllable unit is an ordered queue "
                "from existing M_tail diagnostics, not an unscoped new pick."
            ),
        },
        "build_candidate_queue_from_existing_M_tail_diagnostics": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "The reusable filter is available and no unfiltered known "
                "ambient C_d points remain, so the next route should organize "
                "existing M_tail kernel diagnostics into a queue whose entries "
                "must still prove ambient C_d solubility and then pass the "
                "wl491 admissibility filter."
            ),
        },
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "build_candidate_queue_from_existing_M_tail_diagnostics",
        "entered_here": False,
        "candidate_queue_built_here": False,
        "candidate_selected_here": False,
        "required_source_inputs_for_next_gate": [
            "wl481_sample_matrices_kernel_diagnostics",
            "wl482_classified_u3_support_as_already_disposed",
            "wl491_classify_ambient_c_d_point_for_aa_bb_admissibility",
        ],
        "minimum_later_question": (
            "Which existing M_tail kernel diagnostics should be queued next, "
            "with u_3 excluded or deprioritized as already globally soluble "
            "but not AA+BB-admissible?"
        ),
    }


def build_wl492_route_selection_after_admissibility_filter(
    *, wl491: dict[str, Any]
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl491_ready(wl491):
        violations.append("wl491_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl491 reusable ambient C_d to AA+BB admissibility filter",
        "pattern": "AA+BB",
        "lemma_id": "WL492_route_selection_after_reusable_admissibility_filter",
        "work_log": "wl492",
        "input_work_log": "wl491",
        "known_ambient_filter_status": (
            _known_ambient_filter_status(wl491) if status == "ok" else {}
        ),
        "route_options": _route_options(),
        "selected_next_gate": _selected_next_gate(),
        "routing_audit_only": True,
        "admissibility_filter_defined_here": False,
        "point_level_admissibility_decided_here": False,
        "candidate_queue_built_here": False,
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
        "advance_to_wl493": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl491", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl492_route_selection_after_admissibility_filter(
        wl491=load_json(args.wl491)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl492 route-selection audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(f"advance_to_wl493={audit['advance_to_wl493']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
