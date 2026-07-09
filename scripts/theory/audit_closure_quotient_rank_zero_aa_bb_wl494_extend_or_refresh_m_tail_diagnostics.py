#!/usr/bin/env python3
"""Refresh sampled M_tail diagnostics after the wl493 queue is empty."""

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
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from audit_closure_quotient_rank_zero_aa_bb_wl481_m_tail_explicit_matrix_builder import (
        COORDINATE_ORDER,
        build_wl481_m_tail_audit,
    )
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl494 / extend_or_refresh_M_tail_diagnostics. It reruns "
    "the existing wl481 M_tail matrix builder on a bounded deterministic "
    "primitive AA/BB sample grid, records rank/kernel summaries, separates "
    "new unprocessed kernel supports from the already processed u_3 support, "
    "and stops before proving any new local row, proving ambient C_d "
    "solubility, applying or proving AA+BB admissibility for a new candidate, "
    "selecting a final obstruction candidate, running broad rank or Selmer "
    "diagnostics, using the old package-x S~ bridge, or claiming a complete "
    "Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, or any family "
    "exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

DEFAULT_GRID_BOUND = 4
TARGET_CANDIDATE_ID = "AA_A3_B1_u_3_complete_d_candidate"
TARGET_SUPPORT = ["u_3"]


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


def _wl493_ready(wl493: dict[str, Any]) -> bool:
    summary = wl493.get("queue_summary", {})
    return (
        wl493.get("status") == "ok"
        and wl493.get("ready") is True
        and wl493.get("lemma_id") == "WL493_candidate_queue_from_existing_M_tail_diagnostics"
        and wl493.get("work_log") == "wl493"
        and wl493.get("next_gate_if_active_queue_empty")
        == "extend_or_refresh_M_tail_diagnostics"
        and summary.get("active_unprocessed_candidate_count") == 0
        and summary.get("deprioritized_or_excluded_candidate_count", 0) >= 1
        and wl493.get("candidate_queue_built_here") is True
        and wl493.get("candidate_selected_here") is False
        and wl493.get("new_m_tail_row_proved_here") is False
        and wl493.get("ambient_c_d_solubility_proved_for_new_candidate_here")
        is False
        and wl493.get("old_package_x_coordinate_collapse_used") is False
        and wl493.get("package_x_s_tilde_bridge_used") is False
        and wl493.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl493.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl493)
    )


def _primitive_grid_samples(grid_bound: int) -> list[tuple[str, int, int]]:
    if grid_bound < 1:
        raise ValueError("grid_bound must be positive")
    return [
        (side, a, b)
        for side in ["AA", "BB"]
        for a in range(1, grid_bound + 1)
        for b in range(1, grid_bound + 1)
        if math.gcd(a, b) == 1
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


def _candidate_id(sample: dict[str, Any], support: list[str]) -> str:
    if (
        sample.get("side") == "AA"
        and sample.get("A") == 3
        and sample.get("B") == 1
        and support == TARGET_SUPPORT
    ):
        return TARGET_CANDIDATE_ID
    support_id = "_plus_".join(support) or "empty_support"
    return (
        f"{sample['side']}_A{sample['A']}_B{sample['B']}_"
        f"{support_id}_m_tail_refresh_candidate"
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


def _processed_u3_state_from_wl493(wl493: dict[str, Any]) -> dict[str, Any]:
    for entry in wl493.get("deprioritized_or_excluded_candidates", []):
        if entry.get("candidate_support") == TARGET_SUPPORT:
            return dict(entry["routing_state"])
    return {
        "ambient_c_d_global_solubility_status": "not_recorded",
        "aa_bb_admissibility_status": "not_recorded",
        "ledger_route": "u3_processed_status_missing_from_wl493",
        "blocking_reasons": [],
    }


def _active_routing_state() -> dict[str, Any]:
    return {
        "ambient_c_d_global_solubility_status": "not_tested_here",
        "aa_bb_admissibility_status": "not_tested_here",
        "ledger_route": "refreshed_m_tail_support_pending_ambient_C_d_solubility",
        "blocking_reasons": [],
    }


def _kernel_support_entries(
    *, refreshed_wl481: dict[str, Any], wl493: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    active: list[dict[str, Any]] = []
    processed_u3: list[dict[str, Any]] = []
    u3_routing_state = _processed_u3_state_from_wl493(wl493)
    for sample_matrix in refreshed_wl481.get("sample_matrices", []):
        for support in sample_matrix.get("kernel_diagnostics", {}).get(
            "basis_supports", []
        ):
            sample = sample_matrix["sample"]
            base_entry = {
                "candidate_id": _candidate_id(sample, support),
                "candidate_support": list(support),
                "sample": _sample_payload(sample),
                "rank_and_row_status": _rank_and_row_status(
                    sample_matrix=sample_matrix,
                    support=list(support),
                ),
                "family_metadata": {
                    "pattern": "AA+BB",
                    "source_quotient": sample["side"],
                    "m_tail_object": "M_tail",
                    "complete_d_coordinate_route": True,
                    "old_package_x_s_tilde_bridge_used": False,
                    "refreshed_by_work_log": "wl494",
                },
            }
            if support == TARGET_SUPPORT:
                processed_u3.append(
                    {
                        **base_entry,
                        "queue_status": "processed_or_excluded_u3_support",
                        "routing_state": dict(u3_routing_state),
                        "processed_status_source": TARGET_CANDIDATE_ID,
                        "required_next_gate": (
                            "do_not_reenter_u3; route_only_new_supports_after_wl494"
                        ),
                        "why_not_active": (
                            "The support family is u_3, already routed by "
                            "wl493 as processed/deprioritized after global "
                            "ambient solubility and wl491 not_admissible "
                            "status."
                        ),
                    }
                )
                continue
            active.append(
                {
                    **base_entry,
                    "queue_rank": len(active) + 1,
                    "queue_status": "active_new_kernel_support_from_refreshed_sample",
                    "routing_state": _active_routing_state(),
                    "required_next_gate": (
                        "route_refreshed_support_through_ambient_C_d_solubility_"
                        "then_wl491_filter"
                    ),
                    "why_active": (
                        "This refreshed M_tail kernel support is not the "
                        "already processed u_3 support. wl494 records it as "
                        "active diagnostic output only; ambient C_d "
                        "solubility and AA+BB admissibility are not tested "
                        "here."
                    ),
                }
            )
    return active, processed_u3


def _kernel_support_entry_count(refreshed_wl481: dict[str, Any]) -> int:
    return sum(
        len(
            sample_matrix.get("kernel_diagnostics", {}).get(
                "basis_supports", []
            )
        )
        for sample_matrix in refreshed_wl481.get("sample_matrices", [])
    )


def build_wl494_extend_or_refresh_m_tail_diagnostics(
    *,
    wl480: dict[str, Any],
    wl493: dict[str, Any],
    grid_bound: int = DEFAULT_GRID_BOUND,
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl480_ready(wl480):
        violations.append("wl480_input_not_ready_or_not_scoped")
    if not _wl493_ready(wl493):
        violations.append("wl493_input_not_ready_or_not_scoped")

    samples = _primitive_grid_samples(grid_bound)
    refreshed_wl481 = build_wl481_m_tail_audit(wl480=wl480, samples=samples)
    if refreshed_wl481.get("status") != "ok":
        violations.append("refreshed_wl481_builder_not_ready")

    status = "ok" if not violations else "issues"
    active, processed_u3 = (
        _kernel_support_entries(refreshed_wl481=refreshed_wl481, wl493=wl493)
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
        "source": "wl493 empty active queue plus refreshed wl481 M_tail machinery",
        "pattern": "AA+BB",
        "lemma_id": "WL494_extend_or_refresh_M_tail_diagnostics",
        "work_log": "wl494",
        "input_work_logs": ["wl480", "wl493"],
        "refresh_method": {
            "kind": "deterministic_primitive_AA_BB_sample_grid",
            "grid_bound": grid_bound,
            "sides": ["AA", "BB"],
            "primitive_condition": "gcd(A,B)=1",
            "sample_order": "side, then A ascending, then B ascending",
            "uses_existing_wl481_matrix_builder": True,
            "sample_expansion_is_not_uniform_proof": True,
        },
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
            "processed_or_excluded_u3_entry_count": len(processed_u3),
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
        "processed_or_excluded_u3_supports": processed_u3,
        "next_gate_after_wl494": (
            "For any active refreshed support, first prove ambient C_d "
            "solubility and then apply the wl491 AA+BB admissibility filter."
        ),
        "diagnostic_refresh_built_here": status == "ok",
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "ambient_c_d_solubility_proved_for_new_candidate_here": False,
        "aa_bb_admissibility_proved_for_new_candidate_here": False,
        "admissibility_filter_defined_here": False,
        "routing_audit_only": True,
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
        "advance_to_wl495": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl480", type=Path, required=True)
    parser.add_argument("--wl493", type=Path, required=True)
    parser.add_argument("--grid-bound", type=int, default=DEFAULT_GRID_BOUND)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl494_extend_or_refresh_m_tail_diagnostics(
        wl480=load_json(args.wl480),
        wl493=load_json(args.wl493),
        grid_bound=args.grid_bound,
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl494 M_tail refresh audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "active_new_support_entry_count="
        f"{audit['sample_summary']['active_new_support_entry_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
