#!/usr/bin/env python3
"""Execute the wl509-selected finite M_tail diagnostic shell."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

try:
    from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder import (  # noqa: E501
        COORDINATE_ORDER,
        build_wl481_m_tail_audit,
    )
    from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl498_structure_next_m_tail_diagnostic_extension_plan import (  # noqa: E501
        BOUNDED_V5_EXCLUSION_ENTRIES,
    )
    from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl502_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
        SHELL5_U5_EXCLUSION_ENTRIES,
    )
    from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl508_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
        SHELL7_CLOSED_EXCLUSION_ENTRIES,
    )
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder import (
        COORDINATE_ORDER,
        build_wl481_m_tail_audit,
    )
    from audit_closure_quotient_rank_zero_aa_bb_wl498_structure_next_m_tail_diagnostic_extension_plan import (  # noqa: E501
        BOUNDED_V5_EXCLUSION_ENTRIES,
    )
    from audit_closure_quotient_rank_zero_aa_bb_wl502_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
        SHELL5_U5_EXCLUSION_ENTRIES,
    )
    from audit_closure_quotient_rank_zero_aa_bb_wl508_execute_next_finite_m_tail_shell_from_wl498_plan import (  # noqa: E501
        SHELL7_CLOSED_EXCLUSION_ENTRIES,
    )
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl510 / execute_next_finite_M_tail_shell_from_wl498_"
    "plan. It uses wl509 as route input, executes exactly one declared finite "
    "primitive shell with max(A,B)=9 and side in {AA,BB}, applies the wl498 "
    "duplicate-support guard plus all closed-ledger exclusions through wl509, "
    "records only M_tail diagnostic queue outputs, and stops before testing "
    "ambient C_d solubility, applying wl491, selecting a final obstruction "
    "candidate, proving local rows, running broad rank or Selmer diagnostics, "
    "advancing to wl511, using the old package-x S~ bridge, or claiming a "
    "complete Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, "
    "uniform M_tail full rank, or any family exclusion."
)

DEFAULT_SHELL_BOUND = 9
FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

REQUIRED_WL509_STATE = {
    "completed_finite_shell_bound_after_wl508": 8,
    "shell8_sample_count_from_wl508": 16,
    "shell8_full_rank_sample_count_from_wl508": 14,
    "shell8_kernel_sample_count_from_wl508": 2,
    "shell8_kernel_support_entry_count_from_wl508": 2,
    "shell8_active_new_support_entry_count_from_wl508": 0,
    "shell8_excluded_duplicate_or_processed_support_entry_count_from_wl508": 2,
    "active_candidate_count_after_wl508": 0,
}

REQUIRED_CLOSED_LEDGER_EXCLUSIONS = [
    "u_3_processed_or_deprioritized_after_wl493_wl491",
    "bounded_v_5_entries_disposed_by_wl495_wl496",
    "shell5_u_5_entries_refuted_by_wl500",
    "shell6_empty_diagnostic_output_from_wl502",
    "shell7_active_not_admissible_ledgers_from_wl505",
    "shell7_processed_u3_exclusions_from_wl505",
    "shell7_w5_deferred_ledgers_refuted_by_wl506",
    "shell7_u7_w37_deferred_ledgers_not_admissible_by_wl506",
    "shell8_empty_active_diagnostic_output_from_wl508",
    "shell8_processed_u3_exclusions_from_wl508",
]

SHELL8_PROCESSED_EXCLUSION_ENTRIES = [
    {
        "candidate_id": "AA_A3_B8_u_3_m_tail_shell8_candidate",
        "route_key": {
            "source_quotient": "AA",
            "A": 3,
            "B": 8,
            "L": 3,
            "T": 11,
            "candidate_support": ["u_3"],
        },
    },
    {
        "candidate_id": "BB_A8_B3_u_3_m_tail_shell8_candidate",
        "route_key": {
            "source_quotient": "BB",
            "A": 8,
            "B": 3,
            "L": 3,
            "T": 11,
            "candidate_support": ["u_3"],
        },
    },
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl480_ready(wl480: dict[str, Any]) -> bool:
    return (
        wl480.get("status") == "ok"
        and wl480.get("ready") is True
        and wl480.get("lemma_id") == "D4_AA_BB_uniform_matrix_rank_bound_audit"
        and wl480.get("work_log") == "wl480"
        and wl480.get("complete_d_coordinate_order") == COORDINATE_ORDER
        and wl480.get("local_character_matrix", {}).get("id") == "M_tail"
        and wl480.get("old_package_x_coordinate_collapse_used") is False
        and not _claims_forbidden_bound(wl480)
    )


def _wl509_ready(wl509: dict[str, Any]) -> bool:
    selected = wl509.get("selected_next_gate", {})
    return (
        wl509.get("status") == "ok"
        and wl509.get("ready") is True
        and wl509.get("lemma_id") == "WL509_post_wl508_empty_shell_route_choice_audit"
        and wl509.get("work_log") == "wl509"
        and wl509.get("input_work_log") == "wl508"
        and wl509.get("post_wl508_route_choice_made_here") is True
        and wl509.get("post_wl508_empty_shell_state_summary")
        == REQUIRED_WL509_STATE
        and wl509.get("closed_ledger_do_not_reopen")
        == REQUIRED_CLOSED_LEDGER_EXCLUSIONS
        and selected.get("gate") == "execute_next_finite_M_tail_shell_from_wl498_plan"
        and selected.get("entered_here") is False
        and selected.get("uses_existing_wl498_plan") is True
        and selected.get("shell_bound_to_execute_later") == DEFAULT_SHELL_BOUND
        and selected.get("preserve_wl498_duplicate_support_guard") is True
        and selected.get("new_shell_or_grid_refreshed_here") is False
        and selected.get("m_tail_diagnostics_extended_here") is False
        and selected.get("new_supports_computed_here") is False
        and selected.get("new_c_d_solubility_tested_here") is False
        and selected.get("wl491_filter_applied_here") is False
        and wl509.get("candidate_selected_here") is False
        and wl509.get("new_c_d_solubility_tested_here") is False
        and wl509.get("wl491_filter_applied_to_new_point_here") is False
        and wl509.get("old_package_x_coordinate_collapse_used") is False
        and wl509.get("package_x_s_tilde_bridge_used") is False
        and wl509.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl509.get("single_curve_diagnostics_run") is False
        and wl509.get("advance_to_wl510") is False
        and not _claims_forbidden_bound(wl509)
    )


def _primitive_shell_samples(shell_bound: int) -> list[tuple[str, int, int]]:
    if shell_bound != DEFAULT_SHELL_BOUND:
        raise ValueError("wl510 is scoped to exactly shell_bound=9")
    return [
        (side, a, b)
        for side in ["AA", "BB"]
        for a in range(1, shell_bound + 1)
        for b in range(1, shell_bound + 1)
        if max(a, b) == shell_bound and math.gcd(a, b) == 1
    ]


def _support_nonzero_rows(
    *, sample_matrix: dict[str, Any], support: list[str]
) -> list[str]:
    column_index = {
        column["id"]: index for index, column in enumerate(sample_matrix.get("columns", []))
    }
    support_indexes = [
        column_index[column_id] for column_id in support if column_id in column_index
    ]
    return [
        row["id"]
        for row in sample_matrix.get("rows", [])
        if sum(int(row["entries"][index]) for index in support_indexes) % 2
    ]


def _sample_payload(sample: dict[str, Any]) -> dict[str, Any]:
    return {
        "side": sample["side"],
        "A": sample["A"],
        "B": sample["B"],
        "L": sample["L"],
        "T": sample["T"],
        "sqrt_q": sample["sqrt_q"],
        "primitive": sample["primitive"],
    }


def _route_key(sample: dict[str, Any], support: list[str]) -> dict[str, Any]:
    return {
        "source_quotient": sample["side"],
        "A": sample["A"],
        "B": sample["B"],
        "L": sample["L"],
        "T": sample["T"],
        "candidate_support": list(support),
    }


def _route_key_tuple(route_key: dict[str, Any]) -> tuple[Any, ...]:
    return (
        route_key["source_quotient"],
        route_key["A"],
        route_key["B"],
        route_key["L"],
        route_key["T"],
        tuple(route_key["candidate_support"]),
    )


def _candidate_id(sample: dict[str, Any], support: list[str], shell_bound: int) -> str:
    support_id = "_plus_".join(support) or "empty_support"
    return (
        f"{sample['side']}_A{sample['A']}_B{sample['B']}_"
        f"{support_id}_m_tail_shell{shell_bound}_candidate"
    )


def _rank_and_row_status(
    *, sample_matrix: dict[str, Any], support: list[str]
) -> dict[str, Any]:
    return {
        "computed_rank_status": sample_matrix["computed_rank_status"],
        "rank_needed": sample_matrix["rank_needed"],
        "computed_rank": sample_matrix["computed_rank"],
        "kernel_dimension": sample_matrix["kernel_diagnostics"]["kernel_dimension"],
        "known_row_ids_covering_sample": [
            row["id"] for row in sample_matrix.get("rows", [])
        ],
        "known_rows_with_nonzero_entry_on_support": _support_nonzero_rows(
            sample_matrix=sample_matrix,
            support=support,
        ),
    }


def _active_routing_state() -> dict[str, Any]:
    return {
        "ambient_c_d_global_solubility_status": "not_tested_here",
        "aa_bb_admissibility_status": "not_applied_here",
        "ledger_route": "m_tail_shell_support_pending_ambient_C_d_solubility",
        "blocking_reasons": [],
    }


def _processed_support_families() -> set[tuple[str, ...]]:
    return {("u_3",)}


def _bounded_route_keys() -> set[tuple[Any, ...]]:
    return {_route_key_tuple(entry["route_key"]) for entry in BOUNDED_V5_EXCLUSION_ENTRIES}


def _shell5_closed_route_keys() -> set[tuple[Any, ...]]:
    return {_route_key_tuple(entry["route_key"]) for entry in SHELL5_U5_EXCLUSION_ENTRIES}


def _shell6_closed_route_keys() -> set[tuple[Any, ...]]:
    return set()


def _shell7_closed_route_keys() -> set[tuple[Any, ...]]:
    return {
        _route_key_tuple(entry["route_key"])
        for entry in SHELL7_CLOSED_EXCLUSION_ENTRIES
    }


def _shell8_closed_route_keys() -> set[tuple[Any, ...]]:
    return {
        _route_key_tuple(entry["route_key"])
        for entry in SHELL8_PROCESSED_EXCLUSION_ENTRIES
    }


def _excluded_candidate_ids() -> set[str]:
    return {
        entry["candidate_id"]
        for entry in [
            *BOUNDED_V5_EXCLUSION_ENTRIES,
            *SHELL5_U5_EXCLUSION_ENTRIES,
            *SHELL7_CLOSED_EXCLUSION_ENTRIES,
            *SHELL8_PROCESSED_EXCLUSION_ENTRIES,
        ]
    }


def _duplicate_guard_result(
    *,
    candidate_id: str,
    route_key: dict[str, Any],
    support: list[str],
) -> dict[str, Any]:
    support_tuple = tuple(support)
    route_key_tuple = _route_key_tuple(route_key)
    bounded_route_keys = _bounded_route_keys()
    shell5_closed_route_keys = _shell5_closed_route_keys()
    shell6_closed_route_keys = _shell6_closed_route_keys()
    shell7_closed_route_keys = _shell7_closed_route_keys()
    shell8_closed_route_keys = _shell8_closed_route_keys()
    excluded_candidate_ids = _excluded_candidate_ids()

    is_duplicate_route_key = route_key_tuple in bounded_route_keys.union(
        shell5_closed_route_keys,
        shell6_closed_route_keys,
        shell7_closed_route_keys,
        shell8_closed_route_keys,
    )
    matches_processed_support_family = support_tuple in _processed_support_families()
    matches_bounded_disposed_entry = (
        route_key_tuple in bounded_route_keys or candidate_id in excluded_candidate_ids
    )
    matches_shell5_closed_entry = route_key_tuple in shell5_closed_route_keys
    matches_shell6_closed_entry = route_key_tuple in shell6_closed_route_keys
    matches_shell7_closed_entry = route_key_tuple in shell7_closed_route_keys
    matches_shell8_closed_entry = route_key_tuple in shell8_closed_route_keys
    genuinely_new_support = not (
        is_duplicate_route_key
        or matches_processed_support_family
        or matches_bounded_disposed_entry
        or matches_shell5_closed_entry
        or matches_shell6_closed_entry
        or matches_shell7_closed_entry
        or matches_shell8_closed_entry
    )
    guard_action = (
        "record_active_new_kernel_support"
        if genuinely_new_support
        else "route_to_excluded_duplicate_or_processed_supports"
    )

    support_id = "_plus_".join(support)
    if matches_processed_support_family:
        support_family_status = "processed_support_family"
    elif support_id in {"v_5", "u_5", "w_5", "u_7+w_37", "u_7", "v_13"}:
        support_family_status = "existing_support_family_new_sample"
    else:
        support_family_status = "new_support_family"

    return {
        "route_key": route_key,
        "is_duplicate_route_key": is_duplicate_route_key,
        "matches_processed_support_family": matches_processed_support_family,
        "matches_bounded_disposed_entry": matches_bounded_disposed_entry,
        "matches_shell5_closed_entry": matches_shell5_closed_entry,
        "matches_shell6_closed_entry": matches_shell6_closed_entry,
        "matches_shell7_closed_entry": matches_shell7_closed_entry,
        "matches_shell8_closed_entry": matches_shell8_closed_entry,
        "genuinely_new_support": genuinely_new_support,
        "guard_action": guard_action,
        "support_family_status": support_family_status,
    }


def _candidate_entries(
    *,
    shell_bound: int,
    refreshed_wl481: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    active: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for sample_matrix in refreshed_wl481.get("sample_matrices", []):
        sample = sample_matrix["sample"]
        for support in sample_matrix.get("kernel_diagnostics", {}).get(
            "basis_supports", []
        ):
            support = list(support)
            route_key = _route_key(sample, support)
            candidate_id = _candidate_id(sample, support, shell_bound)
            guard = _duplicate_guard_result(
                candidate_id=candidate_id,
                route_key=route_key,
                support=support,
            )
            base_entry = {
                "candidate_id": candidate_id,
                "candidate_support": support,
                "sample": _sample_payload(sample),
                "route_key": route_key,
                "rank_and_row_status": _rank_and_row_status(
                    sample_matrix=sample_matrix,
                    support=support,
                ),
                "duplicate_guard_result": guard,
                "family_metadata": {
                    "pattern": "AA+BB",
                    "source_quotient": sample["side"],
                    "m_tail_object": "M_tail",
                    "complete_d_coordinate_route": True,
                    "old_package_x_s_tilde_bridge_used": False,
                    "extension_work_log": "wl510",
                },
            }
            if guard["genuinely_new_support"]:
                active.append(
                    {
                        **base_entry,
                        "queue_rank": len(active) + 1,
                        "queue_status": "active_new_kernel_support_from_shell9",
                        "routing_state": _active_routing_state(),
                        "required_next_gate": (
                            "route_active_m_tail_support_through_ambient_C_d_"
                            "solubility_then_wl491_filter"
                        ),
                    }
                )
            else:
                excluded.append(
                    {
                        **base_entry,
                        "queue_status": "excluded_duplicate_or_processed_support",
                        "routing_state": {
                            "ambient_c_d_global_solubility_status": (
                                "not_reentered_here"
                            ),
                            "aa_bb_admissibility_status": "not_reentered_here",
                            "ledger_route": (
                                "excluded_duplicate_or_processed_m_tail_support"
                            ),
                            "blocking_reasons": [
                                guard["support_family_status"],
                            ],
                        },
                        "required_next_gate": (
                            "do_not_reenter_duplicate_or_processed_support"
                        ),
                    }
                )
    return active, excluded


def _kernel_support_entry_count(refreshed_wl481: dict[str, Any]) -> int:
    return sum(
        len(sample_matrix.get("kernel_diagnostics", {}).get("basis_supports", []))
        for sample_matrix in refreshed_wl481.get("sample_matrices", [])
    )


def build_wl510_execute_next_finite_m_tail_shell_from_wl498_plan(
    *,
    wl480: dict[str, Any],
    wl509: dict[str, Any],
    shell_bound: int = DEFAULT_SHELL_BOUND,
) -> dict[str, Any]:
    violations: list[str] = []
    if shell_bound != DEFAULT_SHELL_BOUND:
        violations.append("wl510_requires_exactly_shell_bound_9")
    if not _wl480_ready(wl480):
        violations.append("wl480_input_not_ready_or_not_scoped")
    if not _wl509_ready(wl509):
        violations.append("wl509_input_not_ready_or_not_scoped")

    samples = _primitive_shell_samples(shell_bound)
    refreshed_wl481 = build_wl481_m_tail_audit(wl480=wl480, samples=samples)
    if refreshed_wl481.get("status") != "ok":
        violations.append("shell_wl481_builder_not_ready")

    status = "ok" if not violations else "issues"
    active, excluded = (
        _candidate_entries(shell_bound=shell_bound, refreshed_wl481=refreshed_wl481)
        if status == "ok"
        else ([], [])
    )
    kernel_entry_count = (
        _kernel_support_entry_count(refreshed_wl481) if status == "ok" else 0
    )
    unique_active_supports = sorted(
        {
            support
            for entry in active
            for support in entry.get("candidate_support", [])
        }
    )

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl509 route gate plus wl481 M_tail matrix builder",
        "pattern": "AA+BB",
        "lemma_id": "WL510_execute_next_finite_M_tail_shell_from_wl498_plan",
        "work_log": "wl510",
        "input_work_logs": ["wl480", "wl509"],
        "declared_extension_scope": {
            "extension_unit": "finite_primitive_shell",
            "shell_bound": shell_bound,
            "shell_axis": "max(A,B)",
            "sides": ["AA", "BB"],
            "primitive_condition": "gcd(A,B)=1",
            "sample_order": "side, then A ascending, then B ascending",
            "sample_count": len(samples),
            "uses_existing_wl481_matrix_builder": True,
            "uses_wl498_duplicate_support_guard": True,
            "uses_wl509_closed_ledger_exclusions": True,
        },
        "closed_ledger_exclusions_applied": list(REQUIRED_CLOSED_LEDGER_EXCLUSIONS),
        "sample_summary": {
            "sample_count": refreshed_wl481["sample_summary"]["sample_count"],
            "full_rank_sample_count": refreshed_wl481["sample_summary"][
                "full_rank_sample_count"
            ],
            "kernel_sample_count": refreshed_wl481["sample_summary"][
                "kernel_sample_count"
            ],
            "kernel_support_entry_count": kernel_entry_count,
            "active_new_support_entry_count": len(active),
            "excluded_duplicate_or_processed_support_entry_count": len(excluded),
            "unique_active_supports": unique_active_supports,
        },
        "rank_kernel_summary_by_sample": [
            {
                "sample": _sample_payload(sample_matrix["sample"]),
                "rank_needed": sample_matrix["rank_needed"],
                "computed_rank": sample_matrix["computed_rank"],
                "computed_rank_status": sample_matrix["computed_rank_status"],
                "kernel_dimension": sample_matrix["kernel_diagnostics"][
                    "kernel_dimension"
                ],
                "basis_supports": sample_matrix["kernel_diagnostics"][
                    "basis_supports"
                ],
            }
            for sample_matrix in refreshed_wl481.get("sample_matrices", [])
        ],
        "active_new_kernel_supports": active,
        "excluded_duplicate_or_processed_supports": excluded,
        "duplicate_support_guard_summary": {
            "route_key_fields": [
                "source_quotient",
                "A",
                "B",
                "L",
                "T",
                "candidate_support",
            ],
            "processed_support_family_exclusion_count": len(
                _processed_support_families()
            ),
            "bounded_route_key_exclusion_count": len(BOUNDED_V5_EXCLUSION_ENTRIES),
            "shell5_closed_route_key_exclusion_count": len(
                SHELL5_U5_EXCLUSION_ENTRIES
            ),
            "shell6_closed_route_key_exclusion_count": len(_shell6_closed_route_keys()),
            "shell7_closed_route_key_exclusion_count": len(
                SHELL7_CLOSED_EXCLUSION_ENTRIES
            ),
            "shell8_closed_route_key_exclusion_count": len(
                SHELL8_PROCESSED_EXCLUSION_ENTRIES
            ),
            "candidate_id_collision_exclusion_count": len(_excluded_candidate_ids()),
            "active_new_support_entry_count": len(active),
            "excluded_duplicate_or_processed_support_entry_count": len(excluded),
        },
        "next_gate_after_extension": (
            "Route active shell-9 M_tail supports through ambient C_d global "
            "solubility, then apply the wl491 AA+BB admissibility filter only "
            "where ambient global solubility is proved. wl510 does not enter "
            "that route."
        ),
        "m_tail_diagnostics_extended_here": status == "ok",
        "new_supports_computed_here": status == "ok",
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
        "new_c_d_solubility_tested_here": False,
        "ambient_c_d_solubility_proved_for_new_candidate_here": False,
        "wl491_filter_applied_here": False,
        "aa_bb_admissibility_proved_for_new_candidate_here": False,
        "routing_audit_only": True,
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
        "advance_to_wl511": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl480", type=Path, required=True)
    parser.add_argument("--wl509", type=Path, required=True)
    parser.add_argument("--shell-bound", type=int, default=DEFAULT_SHELL_BOUND)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl510_execute_next_finite_m_tail_shell_from_wl498_plan(
        wl480=load_json(args.wl480),
        wl509=load_json(args.wl509),
        shell_bound=args.shell_bound,
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl510 finite M_tail diagnostic shell to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "active_new_support_entry_count="
        f"{audit['sample_summary']['active_new_support_entry_count']}"
    )
    print(
        "excluded_duplicate_or_processed_support_entry_count="
        f"{audit['sample_summary']['excluded_duplicate_or_processed_support_entry_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
