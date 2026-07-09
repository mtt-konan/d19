#!/usr/bin/env python3
"""Structure the next M_tail diagnostic extension without executing it."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl498 / structure_next_M_tail_diagnostic_extension_plan. "
    "It uses wl497 as input, records the allowed parameter axes, exclusion "
    "ledger, duplicate-support guard, future output schema, stop conditions, "
    "and routing contract for genuinely new M_tail support, and stops before "
    "refreshing a new grid, computing new supports, testing new ambient C_d "
    "solubility, applying wl491 to a new point, proving local rows, selecting "
    "a final obstruction candidate, running broad rank or Selmer diagnostics, "
    "advancing to wl499, using the old package-x S~ bridge, or claiming a "
    "complete Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, or "
    "any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

REQUIRED_POST_WL496_STATE = {
    "u3_active_unprocessed_candidate_count_after_wl493": 0,
    "u3_processed_or_deprioritized_count_after_wl493": 1,
    "bounded_v5_active_support_entry_count_from_wl494": 6,
    "bounded_v5_routed_not_admissible_count_from_wl495": 4,
    "bounded_v5_refuted_ambient_count_from_wl496": 2,
    "bounded_v5_still_deferred_count_after_wl496": 0,
    "aa_bb_admissible_count_after_wl496": 0,
    "active_candidate_count_after_wl496": 0,
}

BOUNDED_V5_EXCLUSION_ENTRIES = [
    {
        "candidate_id": "AA_A1_B4_v_5_m_tail_refresh_candidate",
        "route_key": {
            "source_quotient": "AA",
            "A": 1,
            "B": 4,
            "L": 1,
            "T": 5,
            "candidate_support": ["v_5"],
        },
        "wl495_or_wl496_route": "globally_soluble_but_not_aa_bb_admissible_ledger",
    },
    {
        "candidate_id": "AA_A2_B3_v_5_m_tail_refresh_candidate",
        "route_key": {
            "source_quotient": "AA",
            "A": 2,
            "B": 3,
            "L": 2,
            "T": 5,
            "candidate_support": ["v_5"],
        },
        "wl495_or_wl496_route": "globally_soluble_but_not_aa_bb_admissible_ledger",
    },
    {
        "candidate_id": "AA_A4_B1_v_5_m_tail_refresh_candidate",
        "route_key": {
            "source_quotient": "AA",
            "A": 4,
            "B": 1,
            "L": 4,
            "T": 5,
            "candidate_support": ["v_5"],
        },
        "wl495_or_wl496_route": "ambient_c_d_global_solubility_refuted_ledger",
    },
    {
        "candidate_id": "BB_A1_B4_v_5_m_tail_refresh_candidate",
        "route_key": {
            "source_quotient": "BB",
            "A": 1,
            "B": 4,
            "L": 4,
            "T": 5,
            "candidate_support": ["v_5"],
        },
        "wl495_or_wl496_route": "ambient_c_d_global_solubility_refuted_ledger",
    },
    {
        "candidate_id": "BB_A3_B2_v_5_m_tail_refresh_candidate",
        "route_key": {
            "source_quotient": "BB",
            "A": 3,
            "B": 2,
            "L": 2,
            "T": 5,
            "candidate_support": ["v_5"],
        },
        "wl495_or_wl496_route": "globally_soluble_but_not_aa_bb_admissible_ledger",
    },
    {
        "candidate_id": "BB_A4_B1_v_5_m_tail_refresh_candidate",
        "route_key": {
            "source_quotient": "BB",
            "A": 4,
            "B": 1,
            "L": 1,
            "T": 5,
            "candidate_support": ["v_5"],
        },
        "wl495_or_wl496_route": "globally_soluble_but_not_aa_bb_admissible_ledger",
    },
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl497_ready(wl497: dict[str, Any]) -> bool:
    selected = wl497.get("selected_next_gate", {})
    return (
        wl497.get("status") == "ok"
        and wl497.get("ready") is True
        and wl497.get("lemma_id") == "WL497_post_wl496_route_choice_audit"
        and wl497.get("work_log") == "wl497"
        and wl497.get("post_wl496_route_choice_made_here") is True
        and wl497.get("post_wl496_route_state_summary") == REQUIRED_POST_WL496_STATE
        and selected.get("gate") == "structure_next_M_tail_diagnostic_extension"
        and selected.get("entered_here") is False
        and selected.get("m_tail_diagnostics_extended_here") is False
        and selected.get("new_grid_refreshed_here") is False
        and selected.get("candidate_selected_here") is False
        and wl497.get("new_c_d_solubility_tested_here") is False
        and wl497.get("old_package_x_coordinate_collapse_used") is False
        and wl497.get("package_x_s_tilde_bridge_used") is False
        and wl497.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl497.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl497)
    )


def _allowed_parameter_axes() -> dict[str, Any]:
    return {
        "extension_unit": "finite_primitive_shell",
        "candidate_source": "future_M_tail_matrix_builder_only",
        "sides": ["AA", "BB"],
        "integer_parameters": ["A", "B"],
        "parameter_domain": {"A": "positive_integer", "B": "positive_integer"},
        "primitive_condition": "gcd(A,B)=1",
        "shell_axis": "max(A,B)",
        "prior_completed_shell_bound": 4,
        "allowed_future_shells": (
            "finite shells with max(A,B) > 4, declared before execution"
        ),
        "sample_order": "shell_bound ascending, side, then A ascending, then B ascending",
        "derived_fields_only_after_future_execution": [
            "L",
            "T",
            "sqrt_q",
            "M_tail_rows",
            "kernel_basis_supports",
            "complete_d_coordinate_cover_input",
        ],
    }


def _exclusion_ledger() -> dict[str, Any]:
    return {
        "source_work_logs": ["wl493", "wl494", "wl495", "wl496", "wl497"],
        "family_level_exclusions": [
            {
                "support": ["u_3"],
                "scope": "support_family",
                "reason": "already_processed_and_not_AA_BB_admissible_by_wl493_wl491",
                "future_action": "exclude_or_deprioritize_without_reentering",
            }
        ],
        "bounded_v5_entry_exclusions": BOUNDED_V5_EXCLUSION_ENTRIES,
        "exclusion_summary": {
            "u3_family_exclusion_count": 1,
            "bounded_v5_route_key_exclusion_count": len(
                BOUNDED_V5_EXCLUSION_ENTRIES
            ),
            "excluded_entries_may_not_be_selected_as_final_obstruction": True,
            "excluded_entries_may_not_be_retested_for_ambient_c_d_here": True,
        },
    }


def _duplicate_support_guard() -> dict[str, Any]:
    return {
        "route_key_fields": [
            "source_quotient",
            "A",
            "B",
            "L",
            "T",
            "candidate_support",
        ],
        "duplicate_key_policy": (
            "same route key as exclusion ledger is not a genuinely new support"
        ),
        "candidate_id_collision_policy": (
            "candidate_id collision with exclusion ledger must route to "
            "excluded_duplicate_or_processed_supports"
        ),
        "support_family_policy": {
            "u_3": "always_excluded_as_processed",
            "v_5": (
                "exclude only bounded wl494-wl496 route keys; new shells must "
                "still be labeled existing_support_family_new_sample"
            ),
            "other_supports": (
                "eligible only if route key is absent from the exclusion ledger"
            ),
        },
        "required_duplicate_guard_result_fields": [
            "route_key",
            "is_duplicate_route_key",
            "matches_processed_support_family",
            "matches_bounded_disposed_entry",
            "genuinely_new_support",
            "guard_action",
        ],
    }


def _expected_future_extension_output_schema() -> dict[str, list[str]]:
    return {
        "top_level_required_fields": [
            "status",
            "ready",
            "work_log",
            "input_work_log",
            "declared_extension_scope",
            "sample_summary",
            "rank_kernel_summary_by_sample",
            "active_new_kernel_supports",
            "excluded_duplicate_or_processed_supports",
            "duplicate_support_guard_summary",
            "next_gate_after_extension",
        ],
        "candidate_entry_required_fields": [
            "candidate_id",
            "candidate_support",
            "sample",
            "route_key",
            "rank_and_row_status",
            "duplicate_guard_result",
            "routing_state",
            "required_next_gate",
        ],
        "required_false_claim_flags": [
            "candidate_selected_here",
            "new_local_row_proved_here",
            "new_c_d_solubility_tested_here",
            "complete_selmer_upper_bound_proved",
            "dim_sel2_eq_2_claimed",
            "rank_zero_claimed",
            "sha2_trivial_claimed",
        ],
    }


def build_wl498_structure_next_m_tail_diagnostic_extension_plan(
    *,
    wl497: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl497_ready(wl497):
        violations.append("wl497_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl497 selected but unentered M_tail diagnostic extension gate",
        "pattern": "AA+BB",
        "lemma_id": "WL498_structure_next_M_tail_diagnostic_extension_plan",
        "work_log": "wl498",
        "input_work_log": "wl497",
        "post_wl496_route_state_summary": (
            dict(wl497["post_wl496_route_state_summary"])
            if status == "ok"
            else {}
        ),
        "allowed_parameter_axes": _allowed_parameter_axes(),
        "exclusion_ledger": _exclusion_ledger(),
        "duplicate_support_guard": _duplicate_support_guard(),
        "expected_future_extension_output_schema": (
            _expected_future_extension_output_schema()
        ),
        "stop_conditions_for_future_extension": [
            "stop_after_finite_declared_shell_is_audited",
            "stop_if_only_duplicate_or_processed_supports_remain",
            "stop_immediately_after_recording_any_genuinely_new_support_queue",
            "do_not_test_ambient_C_d_solubility_inside_the_M_tail_extension",
            "do_not_apply_wl491_until_ambient_C_d_global_solubility_is_proved",
        ],
        "future_routing_contract_for_genuinely_new_support": [
            "M_tail_support",
            "ambient_C_d_global_solubility",
            "wl491_AA_BB_admissibility_filter",
            "admissible_or_not_admissible_or_refuted_ledger",
        ],
        "extension_plan_built_here": status == "ok",
        "routing_audit_only": True,
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_grid_refreshed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "aa_bb_admissibility_proved_for_new_candidate_here": False,
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
        "advance_to_wl499": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "Execute a finite M_tail diagnostic extension only in a later "
            "work-log, using this axis/exclusion/duplicate-guard plan as its "
            "input. Any genuinely new support must still route through "
            "ambient C_d solubility before wl491."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl497", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl498_structure_next_m_tail_diagnostic_extension_plan(
        wl497=load_json(args.wl497),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl498 M_tail extension plan audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"extension_plan_built_here={audit['extension_plan_built_here']}")
    print(f"advance_to_wl499={audit['advance_to_wl499']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
