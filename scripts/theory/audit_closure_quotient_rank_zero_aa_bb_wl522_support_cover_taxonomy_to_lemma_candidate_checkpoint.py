#!/usr/bin/env python3
"""Compress wl491-wl521 AA+BB support/cover taxonomy to lemma candidates."""

from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

try:
    from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517 import (  # noqa: E501
        _claims_forbidden_bound,
        _work_log_number,
    )
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from audit_closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517 import (
        _claims_forbidden_bound,
        _work_log_number,
    )
    from json_io import load_json, write_json

EXPECTED_INPUT_WORK_LOGS = [f"wl{index}" for index in range(491, 522)]

BOUNDARY = (
    "This audits only wl522 / support_cover_taxonomy_to_lemma_candidate_checkpoint. "
    "It uses wl521 as the latest state, compresses existing wl491-wl521 "
    "support-family and cover-family ledgers into a taxonomy by classification "
    "and failure mode, and extracts lemma candidates from already-recorded "
    "failure patterns. It does not execute shell 11, compute new M_tail "
    "supports, test new ambient C_d solubility, apply wl491 to a new point, "
    "run broad rank or Selmer diagnostics, select a final obstruction "
    "candidate, use the old package-x S~ bridge, or claim a complete "
    "Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform "
    "M_tail full rank, or any family exclusion."
)

CLASSIFICATION_ORDER = [
    "ambient_globally_not_soluble",
    "globally_soluble_but_not_aa_bb_admissible",
    "processed_or_duplicate_m_tail_support",
]

STATUS_ORDER = [
    "already_closed",
    "genuinely_deferred",
    "globally_soluble_but_not_aa_bb_admissible",
    "refuted",
]


def _payloads_ready(payloads: list[dict[str, Any]]) -> bool:
    by_work_log = {payload.get("work_log"): payload for payload in payloads}
    if sorted(by_work_log) != EXPECTED_INPUT_WORK_LOGS:
        return False

    wl521 = by_work_log.get("wl521", {})
    decision = wl521.get("proof_gap_or_shell_extension_decision", {})
    summary = wl521.get("ledger_summary", {})
    return (
        all(payload.get("status") == "ok" for payload in payloads)
        and all(payload.get("ready") is True for payload in payloads)
        and all(not _claims_forbidden_bound(payload) for payload in payloads)
        and wl521.get("lemma_id") == "WL521_support_family_synthesis_after_wl519"
        and wl521.get("support_family_synthesis_built_here") is True
        and summary.get("final_candidate_ledger_entry_count") == 43
        and summary.get("genuinely_deferred_entry_count") == 0
        and summary.get("aa_bb_admissible_entry_count") == 0
        and decision.get("next_shell") == "max(A,B)=11"
        and decision.get("entered_here") is False
        and wl521.get("shell11_executed_here") is False
        and wl521.get("new_supports_computed_here") is False
        and wl521.get("new_c_d_solubility_tested_here") is False
        and wl521.get("wl491_filter_applied_to_new_point_here") is False
        and wl521.get("candidate_selected_here") is False
        and wl521.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl521.get("old_package_x_coordinate_collapse_used") is False
        and wl521.get("package_x_s_tilde_bridge_used") is False
    )


def _iter_objects(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _iter_objects(child)
    elif isinstance(value, list):
        for item in value:
            yield from _iter_objects(item)


def _candidate_failure_details(payloads: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}
    for payload in payloads:
        work_log = payload.get("work_log")
        for obj in _iter_objects(payload):
            candidates: list[tuple[str | None, dict[str, Any]]] = []
            if isinstance(obj.get("wl491_filter_result"), dict):
                result = obj["wl491_filter_result"]
                candidates.append((result.get("candidate_id") or obj.get("candidate_id"), result))
            if "blocking_reasons" in obj and "candidate_id" in obj:
                candidates.append((obj.get("candidate_id"), obj))
            routing = obj.get("routing_state")
            if isinstance(routing, dict) and "blocking_reasons" in routing:
                candidates.append((obj.get("candidate_id"), routing))

            for candidate_id, result in candidates:
                if not candidate_id:
                    continue
                work_log_number = _work_log_number(str(work_log))
                row = details.setdefault(
                    str(candidate_id),
                    {
                        "blocking_reasons": set(),
                        "source_work_logs": set(),
                        "wl491_output_classes": set(),
                        "latest_work_log_number": work_log_number,
                    },
                )
                if work_log_number > row["latest_work_log_number"]:
                    row["blocking_reasons"].clear()
                    row["source_work_logs"].clear()
                    row["wl491_output_classes"].clear()
                    row["latest_work_log_number"] = work_log_number
                row["blocking_reasons"].update(
                    str(reason) for reason in result.get("blocking_reasons", [])
                )
                if work_log:
                    row["source_work_logs"].add(str(work_log))
                output_class = result.get("output_class") or result.get(
                    "aa_bb_admissibility_status"
                )
                if output_class:
                    row["wl491_output_classes"].add(str(output_class))

    normalized = {}
    for candidate_id, row in details.items():
        normalized[candidate_id] = {
            "blocking_reasons": sorted(row["blocking_reasons"]),
            "source_work_logs": sorted(row["source_work_logs"], key=_work_log_number),
            "wl491_output_classes": sorted(row["wl491_output_classes"]),
        }
    return normalized


def _group_by(entries: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        grouped.setdefault(entry[key], []).append(entry)
    return grouped


def _family_classification(entries: list[dict[str, Any]]) -> str:
    statuses = {entry["classification"] for entry in entries}
    if "genuinely_deferred" in statuses:
        return "genuinely_deferred"
    if "already_closed" in statuses:
        return "already_closed"
    if "globally_soluble_but_not_aa_bb_admissible" in statuses:
        return "globally_soluble_but_not_aa_bb_admissible"
    return "refuted"


def _failure_mode(classification: str) -> str:
    if classification == "refuted":
        return "ambient_globally_not_soluble"
    if classification == "globally_soluble_but_not_aa_bb_admissible":
        return "common_source_aa_bb_admissibility_failure"
    if classification == "genuinely_deferred":
        return "genuinely_deferred_ambient_c_d_solubility"
    return "processed_or_duplicate_m_tail_support"


def _ambient_status(classification: str) -> str:
    if classification == "refuted":
        return "globally_not_soluble"
    if classification == "globally_soluble_but_not_aa_bb_admissible":
        return "globally_soluble"
    if classification == "genuinely_deferred":
        return "global_solubility_deferred"
    return "not_applicable_processed_m_tail_support"


def _lemma_candidate_status(failure_mode: str) -> str:
    if failure_mode == "common_source_aa_bb_admissibility_failure":
        return "theorem-candidate"
    if failure_mode == "ambient_globally_not_soluble":
        return "dead_end"
    return "data-only"


def _support_cover_taxonomy(
    entries: list[dict[str, Any]],
    failure_details: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for cover_family, family_entries in _group_by(entries, "cover_family").items():
        classification = _family_classification(family_entries)
        failure_mode = _failure_mode(classification)
        candidate_ids = sorted(entry["candidate_id"] for entry in family_entries)
        blocking_reasons = sorted(
            {
                reason
                for candidate_id in candidate_ids
                for reason in failure_details.get(candidate_id, {}).get("blocking_reasons", [])
            }
        )
        rows.append(
            {
                "support_family": family_entries[0]["support_family"],
                "cover_family": cover_family,
                "classification": classification,
                "failure_mode": failure_mode,
                "ambient_c_d_global_solubility_status": _ambient_status(classification),
                "lemma_candidate_status": _lemma_candidate_status(failure_mode),
                "candidate_ids": candidate_ids,
                "entry_count": len(family_entries),
                "work_logs": sorted(
                    {entry["source_work_log"] for entry in family_entries},
                    key=_work_log_number,
                ),
                "cover_summary": family_entries[0]["cover_summary"],
                "blocking_reasons": blocking_reasons,
            }
        )
    return sorted(rows, key=lambda row: (row["support_family"], row["cover_family"]))


def _taxonomy_summary(
    *,
    wl521_summary: dict[str, Any],
    taxonomy_rows: list[dict[str, Any]],
) -> dict[str, int]:
    failure_counts = Counter(row["failure_mode"] for row in taxonomy_rows)
    return {
        "final_candidate_ledger_entry_count": wl521_summary["final_candidate_ledger_entry_count"],
        "support_family_count": wl521_summary["support_family_count"],
        "cover_family_count": wl521_summary["cover_family_count"],
        "taxonomy_row_count": len(taxonomy_rows),
        "ambient_globally_not_soluble_entry_count": wl521_summary["refuted_entry_count"],
        "globally_soluble_but_not_aa_bb_admissible_entry_count": wl521_summary[
            "globally_soluble_but_not_aa_bb_admissible_entry_count"
        ],
        "already_closed_entry_count": wl521_summary["already_closed_entry_count"],
        "genuinely_deferred_entry_count": wl521_summary["genuinely_deferred_entry_count"],
        "aa_bb_admissible_entry_count": wl521_summary["aa_bb_admissible_entry_count"],
        "ambient_globally_not_soluble_cover_family_count": failure_counts[
            "ambient_globally_not_soluble"
        ],
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": failure_counts[
            "common_source_aa_bb_admissibility_failure"
        ],
        "processed_or_duplicate_cover_family_count": failure_counts[
            "processed_or_duplicate_m_tail_support"
        ],
        "genuinely_deferred_cover_family_count": failure_counts[
            "genuinely_deferred_ambient_c_d_solubility"
        ],
        "aa_bb_admissible_cover_family_count": 0,
    }


def _lemma_candidate_patterns(taxonomy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    common_rows = [
        row
        for row in taxonomy_rows
        if row["failure_mode"] == "common_source_aa_bb_admissibility_failure"
    ]
    refuted_rows = [
        row for row in taxonomy_rows if row["failure_mode"] == "ambient_globally_not_soluble"
    ]
    processed_rows = [
        row
        for row in taxonomy_rows
        if row["failure_mode"] == "processed_or_duplicate_m_tail_support"
    ]
    support_modes: dict[str, set[str]] = {}
    for row in taxonomy_rows:
        support_modes.setdefault(row["support_family"], set()).add(row["failure_mode"])
    mixed_supports = sorted(
        support
        for support, modes in support_modes.items()
        if "ambient_globally_not_soluble" in modes
        and "common_source_aa_bb_admissibility_failure" in modes
    )
    reason_counts = Counter(
        reason for row in common_rows for reason in row.get("blocking_reasons", [])
    )

    return [
        {
            "pattern_id": "common_source_square_obstruction_across_not_admissible_cover_families",
            "candidate_status": "theorem-candidate",
            "support_family_count": len({row["support_family"] for row in common_rows}),
            "cover_family_count": len(common_rows),
            "entry_count": sum(int(row["entry_count"]) for row in common_rows),
            "failure_mode": "common_source_aa_bb_admissibility_failure",
            "blocking_reason_counts": dict(sorted(reason_counts.items())),
            "why_interesting": (
                "The reusable non-admissibility signal is not ambient C_d "
                "failure: these covers already have global ambient points, "
                "then fail the opposite AA/BB common-source square check."
            ),
        },
        {
            "pattern_id": "mixed_refuted_not_admissible_same_support_families",
            "candidate_status": "data-only",
            "support_families": mixed_supports,
            "support_family_count": len(mixed_supports),
            "why_not_selected": (
                "Mixed finite history shows recurring diagnostic families, "
                "but it combines ambient refutations with not-admissible "
                "points and does not itself state one proof-level condition."
            ),
        },
        {
            "pattern_id": "ambient_globally_not_soluble_cover_families",
            "candidate_status": "dead_end",
            "cover_family_count": len(refuted_rows),
            "cover_families": [row["cover_family"] for row in refuted_rows],
            "why_dead_end": (
                "These covers are already ambient globally not soluble, so "
                "wl491 is not applicable and they do not produce an AA+BB "
                "common-source lemma candidate."
            ),
        },
        {
            "pattern_id": "processed_or_duplicate_m_tail_supports",
            "candidate_status": "data-only",
            "cover_family_count": len(processed_rows),
            "cover_families": [row["cover_family"] for row in processed_rows],
            "why_data_only": (
                "These rows record finite M_tail bookkeeping, not new ambient "
                "C_d points or proof-level Selmer information."
            ),
        },
    ]


def _selected_next_proof_level_lemma_candidate() -> dict[str, Any]:
    return {
        "status": "named_lemma_candidate_isolated",
        "lemma_candidate_id": (
            "common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families"
        ),
        "candidate_status": "theorem-candidate",
        "entered_here": False,
        "proof_level_work_done_here": False,
        "why_this_one": (
            "Every globally soluble non-admissible cover family in the wl491-wl521 "
            "taxonomy fails the opposite AA/BB common-source square check; this is "
            "the only reusable pattern that is not already an ambient refutation "
            "or processed M_tail duplicate."
        ),
    }


def _selected_next_gate() -> dict[str, Any]:
    return {
        "gate": "try_common_source_square_obstruction_lemma_candidate",
        "entered_here": False,
        "lemma_candidate_id": (
            "common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families"
        ),
        "minimum_next_question": (
            "Can the recorded wl491 common-source product-not-square failures "
            "be stated as a reusable AA+BB admissibility obstruction lemma, "
            "without using finite support counts as Selmer progress?"
        ),
        "shell11_executed_here": False,
        "from_existing_wl521_state": True,
    }


def build_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint(
    *,
    ledger_payloads: list[dict[str, Any]],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _payloads_ready(ledger_payloads):
        violations.append("wl491_to_wl521_inputs_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    wl521 = {payload.get("work_log"): payload for payload in ledger_payloads}.get("wl521", {})
    entries = wl521.get("final_candidate_ledgers", []) if status == "ok" else []
    failure_details = _candidate_failure_details(ledger_payloads) if status == "ok" else {}
    taxonomy_rows = _support_cover_taxonomy(entries, failure_details)
    patterns = _lemma_candidate_patterns(taxonomy_rows)

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl491-wl521 ledger outputs with wl521 as latest state",
        "pattern": "AA+BB",
        "lemma_id": "WL522_support_cover_taxonomy_to_lemma_candidate_checkpoint",
        "work_log": "wl522",
        "input_work_log": "wl521",
        "input_work_logs": list(EXPECTED_INPUT_WORK_LOGS),
        "support_cover_taxonomy_built_here": status == "ok",
        "aggregation_axis": [
            "support_family",
            "cover_family",
            "classification",
            "failure_mode",
        ],
        "classification_order": list(CLASSIFICATION_ORDER),
        "taxonomy_summary": _taxonomy_summary(
            wl521_summary=wl521.get("ledger_summary", {}),
            taxonomy_rows=taxonomy_rows,
        )
        if status == "ok"
        else {},
        "support_cover_taxonomy": taxonomy_rows,
        "lemma_candidate_patterns": patterns,
        "selected_next_proof_level_lemma_candidate": (
            _selected_next_proof_level_lemma_candidate() if status == "ok" else {}
        ),
        "selected_next_gate": _selected_next_gate() if status == "ok" else {},
        "shell11_executed_here": False,
        "m_tail_diagnostics_extended_here": False,
        "new_supports_computed_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_to_new_point_here": False,
        "candidate_selected_here": False,
        "final_obstruction_candidate_selected_here": False,
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
        "advance_to_wl523": False,
        "stop_after_current_task": True,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def load_wl491_to_wl521_payloads(ledger_dir: Path) -> list[dict[str, Any]]:
    payloads = []
    for work_log in EXPECTED_INPUT_WORK_LOGS:
        matches = sorted(
            ledger_dir.glob(f"closure_quotient_rank_zero_aa_bb_{work_log}_*.json")
        )
        if len(matches) != 1:
            raise FileNotFoundError(
                f"expected exactly one result JSON for {work_log} in {ledger_dir}"
            )
        payloads.append(load_json(matches[0]))
    return payloads


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl522_support_cover_taxonomy_to_lemma_candidate_checkpoint(
        ledger_payloads=load_wl491_to_wl521_payloads(args.ledger_dir)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl522 support/cover taxonomy checkpoint to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    selected = audit.get("selected_next_proof_level_lemma_candidate", {})
    print(f"selected_lemma={selected.get('lemma_candidate_id')}")
    print(f"shell11_executed_here={audit['shell11_executed_here']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
