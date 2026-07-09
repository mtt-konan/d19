#!/usr/bin/env python3
"""Build the wl493 queue from existing M_tail diagnostics."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl493 / candidate queue construction from existing "
    "wl481 M_tail diagnostics after the wl491 admissibility filter and wl492 "
    "route selection. It builds an ordered queue ledger, records why the "
    "already processed u_3 support is excluded/deprioritized, and stops before "
    "proving a new M_tail row, proving ambient C_d solubility for a new "
    "candidate, selecting a final obstruction candidate, running broad rank or "
    "Selmer diagnostics, using the old package-x S~ bridge, or claiming a "
    "complete Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, or "
    "any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]

TARGET_CANDIDATE_ID = "AA_A3_B1_u_3_complete_d_candidate"
TARGET_SAMPLE = {"side": "AA", "A": 3, "B": 1}
TARGET_SUPPORT = ["u_3"]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl481_ready(wl481: dict[str, Any]) -> bool:
    return (
        wl481.get("status") == "ok"
        and wl481.get("ready") is True
        and wl481.get("lemma_id") == "WL481_M_tail_explicit_matrix_builder"
        and wl481.get("work_log") == "wl481"
        and wl481.get("matrix_object", {}).get("id") == "M_tail"
        and wl481.get("old_package_x_coordinate_collapse_used") is False
        and not _claims_forbidden_bound(wl481)
    )


def _wl482_ready(wl482: dict[str, Any]) -> bool:
    return (
        wl482.get("status") == "ok"
        and wl482.get("ready") is True
        and wl482.get("lemma_id") == "WL482_M_tail_kernel_classification_gate"
        and wl482.get("work_log") == "wl482"
        and wl482.get("input_work_log") == "wl481"
        and wl482.get("target_kernel", {}).get("support") == TARGET_SUPPORT
        and wl482.get("old_package_x_coordinate_collapse_used") is False
        and not _claims_forbidden_bound(wl482)
    )


def _wl490_ready(wl490: dict[str, Any]) -> bool:
    ledger = wl490.get("ledger_update", {})
    killed = ledger.get("killed_candidate", {})
    return (
        wl490.get("status") == "ok"
        and wl490.get("ready") is True
        and wl490.get("lemma_id") == "WL490_route_impact_after_wl489_admissibility_failure"
        and wl490.get("work_log") == "wl490"
        and wl490.get("input_work_log") == "wl489"
        and killed.get("candidate_id") == TARGET_CANDIDATE_ID
        and wl490.get("old_package_x_coordinate_collapse_used") is False
        and wl490.get("package_x_s_tilde_bridge_used") is False
        and wl490.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl490.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl490)
    )


def _wl491_ready(wl491: dict[str, Any]) -> bool:
    u3 = wl491.get("u3_regression", {})
    return (
        wl491.get("status") == "ok"
        and wl491.get("ready") is True
        and wl491.get("lemma_id") == "WL491_reusable_ambient_C_d_to_AA_BB_admissibility_filter"
        and wl491.get("work_log") == "wl491"
        and wl491.get("input_work_log") == "wl490"
        and wl491.get("admissibility_filter_defined_here") is True
        and u3.get("candidate_id") == TARGET_CANDIDATE_ID
        and u3.get("output_class") == "not_admissible"
        and u3.get("ledger_route") == "globally_soluble_but_not_aa_bb_admissible_ledger"
        and wl491.get("old_package_x_coordinate_collapse_used") is False
        and wl491.get("package_x_s_tilde_bridge_used") is False
        and wl491.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl491.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl491)
    )


def _wl492_ready(wl492: dict[str, Any]) -> bool:
    selected = wl492.get("selected_next_gate", {})
    return (
        wl492.get("status") == "ok"
        and wl492.get("ready") is True
        and wl492.get("lemma_id") == "WL492_route_selection_after_reusable_admissibility_filter"
        and wl492.get("work_log") == "wl492"
        and wl492.get("input_work_log") == "wl491"
        and selected.get("gate") == "build_candidate_queue_from_existing_M_tail_diagnostics"
        and selected.get("entered_here") is False
        and selected.get("candidate_queue_built_here") is False
        and wl492.get("candidate_queue_built_here") is False
        and wl492.get("old_package_x_coordinate_collapse_used") is False
        and wl492.get("package_x_s_tilde_bridge_used") is False
        and wl492.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl492.get("single_curve_diagnostics_run") is False
        and not _claims_forbidden_bound(wl492)
    )


def _sample_matches(sample: dict[str, Any], expected: dict[str, Any]) -> bool:
    return all(sample.get(key) == value for key, value in expected.items())


def _candidate_id(sample: dict[str, Any], support: list[str]) -> str:
    if _sample_matches(sample, TARGET_SAMPLE) and support == TARGET_SUPPORT:
        return TARGET_CANDIDATE_ID
    support_id = "_plus_".join(support) or "empty_support"
    return f"{sample['side']}_A{sample['A']}_B{sample['B']}_{support_id}_m_tail_candidate"


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


def _row_coverage_status(
    *,
    sample_matrix: dict[str, Any],
    support: list[str],
    wl482: dict[str, Any],
) -> dict[str, Any]:
    is_target = (
        _sample_matches(sample_matrix.get("sample", {}), TARGET_SAMPLE)
        and support == TARGET_SUPPORT
    )
    coverage_check = wl482.get("known_local_row_coverage_check", {})
    return {
        "wl481_computed_rank_status": sample_matrix["computed_rank_status"],
        "wl482_final_classification": (
            wl482.get("classification", {}).get("final_classification")
            if is_target
            else "not_classified_by_wl482"
        ),
        "known_row_ids_covering_sample": [
            row["id"] for row in sample_matrix.get("rows", [])
        ],
        "known_rows_with_nonzero_entry_on_support": _support_nonzero_rows(
            sample_matrix=sample_matrix,
            support=support,
        ),
        "known_local_row_coverage_decision": (
            coverage_check.get("decision")
            if is_target
            else "not_yet_classified_against_wl482_target_gate"
        ),
    }


def _u3_routing_state(
    *, wl490: dict[str, Any], wl491: dict[str, Any]
) -> dict[str, Any]:
    u3 = wl491["u3_regression"]
    ledger_entries = wl490.get("ledger_update", {}).get(
        "globally_soluble_but_not_aa_bb_admissible_ledger", []
    )
    is_globally_soluble = any(
        entry.get("candidate_id") == TARGET_CANDIDATE_ID for entry in ledger_entries
    )
    return {
        "ambient_c_d_global_solubility_status": (
            "globally_soluble" if is_globally_soluble else "not_recorded"
        ),
        "aa_bb_admissibility_status": u3["output_class"],
        "ledger_route": u3["ledger_route"],
        "blocking_reasons": list(u3["blocking_reasons"]),
    }


def _active_routing_state() -> dict[str, Any]:
    return {
        "ambient_c_d_global_solubility_status": "not_tested_here",
        "aa_bb_admissibility_status": "not_tested_here",
        "ledger_route": "candidate_queue_pending_ambient_C_d_solubility",
        "blocking_reasons": [],
    }


def _queue_entry(
    *,
    queue_rank: int,
    queue_status: str,
    sample_matrix: dict[str, Any],
    support: list[str],
    row_coverage_status: dict[str, Any],
    routing_state: dict[str, Any],
    required_next_gate: str,
    why_queued: str,
) -> dict[str, Any]:
    sample = sample_matrix["sample"]
    return {
        "queue_rank": queue_rank,
        "queue_status": queue_status,
        "candidate_id": _candidate_id(sample, support),
        "candidate_support": list(support),
        "sample": {
            "side": sample["side"],
            "A": sample["A"],
            "B": sample["B"],
            "L": sample["L"],
            "T": sample["T"],
            "sqrt_q": sample["sqrt_q"],
            "primitive": sample["primitive"],
        },
        "family_metadata": {
            "pattern": "AA+BB",
            "source_quotient": sample["side"],
            "m_tail_object": "M_tail",
            "complete_d_coordinate_route": True,
            "old_package_x_s_tilde_bridge_used": False,
        },
        "known_row_coverage_status": row_coverage_status,
        "routing_state": routing_state,
        "required_next_gate": required_next_gate,
        "why_queued": why_queued,
    }


def _kernel_support_records(wl481: dict[str, Any]) -> list[tuple[dict[str, Any], list[str]]]:
    records: list[tuple[dict[str, Any], list[str]]] = []
    for sample_matrix in wl481.get("sample_matrices", []):
        for support in sample_matrix.get("kernel_diagnostics", {}).get(
            "basis_supports", []
        ):
            records.append((sample_matrix, list(support)))
    return records


def _build_queue_entries(
    *,
    wl481: dict[str, Any],
    wl482: dict[str, Any],
    wl490: dict[str, Any],
    wl491: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    active: list[dict[str, Any]] = []
    processed: list[dict[str, Any]] = []
    for sample_matrix, support in _kernel_support_records(wl481):
        row_coverage = _row_coverage_status(
            sample_matrix=sample_matrix,
            support=support,
            wl482=wl482,
        )
        is_processed_u3 = (
            _sample_matches(sample_matrix.get("sample", {}), TARGET_SAMPLE)
            and support == TARGET_SUPPORT
        )
        if is_processed_u3:
            processed.append(
                _queue_entry(
                    queue_rank=len(processed) + 1,
                    queue_status="deprioritized_already_processed_not_admissible",
                    sample_matrix=sample_matrix,
                    support=support,
                    row_coverage_status=row_coverage,
                    routing_state=_u3_routing_state(wl490=wl490, wl491=wl491),
                    required_next_gate=(
                        "do_not_reenter_current_candidate_queue; "
                        "extend_or_refresh_M_tail_diagnostics"
                    ),
                    why_queued=(
                        "Kept only as an ordered processed/deprioritized entry "
                        "so the queue audit records that the wl481 u_3 support "
                        "has already become an ambient global C_d point and "
                        "failed the wl491 AA+BB admissibility filter."
                    ),
                )
            )
            continue
        active.append(
            _queue_entry(
                queue_rank=len(active) + 1,
                queue_status="active_unprocessed_kernel_support",
                sample_matrix=sample_matrix,
                support=support,
                row_coverage_status=row_coverage,
                routing_state=_active_routing_state(),
                required_next_gate=(
                    "prove_ambient_C_d_global_solubility_then_apply_wl491_"
                    "admissibility_filter"
                ),
                why_queued=(
                    "This wl481 kernel support has not yet been processed as "
                    "an ambient global C_d point, so the next gate would first "
                    "test ambient C_d solubility and only then apply the wl491 "
                    "AA+BB admissibility filter."
                ),
            )
        )
    return active, processed, len(active) + len(processed)


def build_wl493_candidate_queue_from_existing_m_tail_diagnostics(
    *,
    wl481: dict[str, Any],
    wl482: dict[str, Any],
    wl490: dict[str, Any],
    wl491: dict[str, Any],
    wl492: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl481_ready(wl481):
        violations.append("wl481_input_not_ready_or_not_scoped")
    if not _wl482_ready(wl482):
        violations.append("wl482_input_not_ready_or_not_scoped")
    if not _wl490_ready(wl490):
        violations.append("wl490_input_not_ready_or_not_scoped")
    if not _wl491_ready(wl491):
        violations.append("wl491_input_not_ready_or_not_scoped")
    if not _wl492_ready(wl492):
        violations.append("wl492_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    active, processed, kernel_count = (
        _build_queue_entries(wl481=wl481, wl482=wl482, wl490=wl490, wl491=wl491)
        if status == "ok"
        else ([], [], 0)
    )
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl481 M_tail diagnostics plus wl482/wl490/wl491/wl492 route state",
        "pattern": "AA+BB",
        "lemma_id": "WL493_candidate_queue_from_existing_M_tail_diagnostics",
        "work_log": "wl493",
        "input_work_logs": ["wl481", "wl482", "wl490", "wl491", "wl492"],
        "queue_summary": {
            "kernel_support_entry_count_from_wl481": kernel_count,
            "active_unprocessed_candidate_count": len(active),
            "deprioritized_or_excluded_candidate_count": len(processed),
            "ordered_active_queue_empty_because": (
                "The only existing wl481 kernel support is u_3, and wl490/wl491 "
                "already route it as globally soluble but not AA+BB-admissible."
                if status == "ok" and not active and processed
                else ""
            ),
        },
        "ordered_active_candidate_queue": active,
        "deprioritized_or_excluded_candidates": processed,
        "next_gate_if_active_queue_empty": "extend_or_refresh_M_tail_diagnostics",
        "candidate_queue_built_here": status == "ok",
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "ambient_c_d_solubility_proved_for_new_candidate_here": False,
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
        "advance_to_wl494": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl481", type=Path, required=True)
    parser.add_argument("--wl482", type=Path, required=True)
    parser.add_argument("--wl490", type=Path, required=True)
    parser.add_argument("--wl491", type=Path, required=True)
    parser.add_argument("--wl492", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl493_candidate_queue_from_existing_m_tail_diagnostics(
        wl481=load_json(args.wl481),
        wl482=load_json(args.wl482),
        wl490=load_json(args.wl490),
        wl491=load_json(args.wl491),
        wl492=load_json(args.wl492),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl493 candidate-queue audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(
        "active_unprocessed_candidate_count="
        f"{audit['queue_summary']['active_unprocessed_candidate_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
