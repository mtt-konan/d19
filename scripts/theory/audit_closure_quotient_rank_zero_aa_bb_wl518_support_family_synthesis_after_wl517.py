#!/usr/bin/env python3
"""Synthesize wl491-wl517 AA+BB ledgers by support and cover family."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

COORDINATE_ORDER = ["d_minus_p", "d_pos_2sqrt_q", "d_neg_2sqrt_q"]

EXPECTED_INPUT_WORK_LOGS = [f"wl{index}" for index in range(491, 518)]

LEDGER_ENTRY_FIELDS = [
    "deprioritized_or_excluded_candidates",
    "routed_refreshed_supports",
    "resolved_deferred_entries",
    "routed_active_u5_supports",
    "routed_active_shell7_supports",
    "routed_active_shell9_supports",
    "classified_deferred_entries",
    "classified_u7_entries",
    "routed_active_shell10_supports",
    "classified_shell10_u5_entries",
    "excluded_duplicate_or_processed_supports",
]

STATUS_ORDER = [
    "already_closed",
    "genuinely_deferred",
    "globally_soluble_but_not_aa_bb_admissible",
    "refuted",
]

BOUNDARY = (
    "This audits only wl518 / support_family_synthesis_after_wl517. It uses "
    "wl517 as the immediate input and aggregates existing wl491-wl517 ledger "
    "outputs by support family and cover family rather than worklog order. It "
    "does not execute shell 11, does not resolve the two shell-10 deferred "
    "covers, does not run broad rank or Selmer diagnostics, does not select a "
    "final obstruction candidate, does not enter proof-level generalization, "
    "does not use the old package-x S~ bridge, and does not claim a complete "
    "Sel_2(E) upper bound, dim Sel_2(E)=2, rank zero, Sha[2]=0, uniform M_tail "
    "full rank, or any family exclusion."
)

FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]


def _work_log_number(work_log: str) -> int:
    match = re.fullmatch(r"wl(\d+)", work_log)
    if not match:
        return -1
    return int(match.group(1))


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _payloads_ready(payloads: list[dict[str, Any]]) -> bool:
    by_work_log = {payload.get("work_log"): payload for payload in payloads}
    if sorted(by_work_log) != EXPECTED_INPUT_WORK_LOGS:
        return False
    wl517 = by_work_log.get("wl517", {})
    return (
        all(payload.get("status") == "ok" for payload in payloads)
        and all(payload.get("ready") is True for payload in payloads)
        and all(not _claims_forbidden_bound(payload) for payload in payloads)
        and wl517.get("lemma_id")
        == (
            "WL517_route_active_shell10_M_tail_supports_through_ambient_C_d_"
            "solubility_then_wl491_filter"
        )
        and wl517.get("all_active_shell10_supports_classified_here") is True
        and wl517.get("all_active_shell10_supports_fully_routed_here") is False
        and wl517.get("route_summary", {}).get("ambient_global_solubility_deferred_count")
        == 2
        and wl517.get("shell11_executed_here") is False
        and wl517.get("candidate_selected_here") is False
        and wl517.get("broad_rank_or_selmer_diagnostics_run") is False
        and wl517.get("family_rank_or_selmer_diagnostics_run") is False
        and wl517.get("old_package_x_coordinate_collapse_used") is False
        and wl517.get("package_x_s_tilde_bridge_used") is False
    )


def _support_family(entry: dict[str, Any]) -> str:
    support = entry.get("candidate_support", [])
    if not support:
        return "unknown_support"
    return "+".join(str(part) for part in support)


def _d_vector(entry: dict[str, Any]) -> dict[str, int]:
    raw = entry.get("complete_c_d_cover", {}).get("d_vector", {})
    return {
        coordinate: int(raw[coordinate])
        for coordinate in COORDINATE_ORDER
        if coordinate in raw
    }


def _d_tuple(entry: dict[str, Any]) -> tuple[int | str, int | str, int | str]:
    d_vector = _d_vector(entry)
    return tuple(d_vector.get(coordinate, "?") for coordinate in COORDINATE_ORDER)


def _cover_summary(entry: dict[str, Any]) -> dict[str, Any]:
    sample = entry.get("sample", {})
    return {
        "L": sample.get("L"),
        "T": sample.get("T"),
        "d_vector": _d_vector(entry),
    }


def _cover_family_key(entry: dict[str, Any]) -> str:
    sample = entry.get("sample", {})
    d_tuple = _d_tuple(entry)
    return (
        f"support={_support_family(entry)}|L={sample.get('L')}|T={sample.get('T')}"
        f"|d=({d_tuple[0]},{d_tuple[1]},{d_tuple[2]})"
    )


def _entry_status(entry: dict[str, Any]) -> str:
    route = entry.get("routing_state", {}).get("ledger_route")
    solubility = entry.get("ambient_c_d_global_solubility", {}).get("status")
    filter_class = entry.get("wl491_filter_result", {}).get("output_class")
    queue_status = str(entry.get("queue_status", ""))

    if route == "excluded_duplicate_or_processed_m_tail_support":
        return "already_closed"
    if (
        route == "ambient_c_d_solubility_deferred_ledger"
        or solubility == "global_solubility_deferred"
    ):
        return "genuinely_deferred"
    if (
        route == "ambient_c_d_global_solubility_refuted_ledger"
        or solubility == "globally_not_soluble"
    ):
        return "refuted"
    if (
        route == "globally_soluble_but_not_aa_bb_admissible_ledger"
        or filter_class == "not_admissible"
    ):
        return "globally_soluble_but_not_aa_bb_admissible"
    if "processed" in queue_status:
        return "already_closed"
    return "already_closed"


def _normal_entry(source_work_log: str, entry: dict[str, Any]) -> dict[str, Any]:
    status = _entry_status(entry)
    sample = entry.get("sample", {})
    return {
        "candidate_id": entry["candidate_id"],
        "source_work_log": source_work_log,
        "support_family": _support_family(entry),
        "cover_family": _cover_family_key(entry),
        "classification": status,
        "sample": {
            "side": sample.get("side"),
            "A": sample.get("A"),
            "B": sample.get("B"),
            "L": sample.get("L"),
            "T": sample.get("T"),
        },
        "cover_summary": _cover_summary(entry),
        "ledger_route": entry.get("routing_state", {}).get("ledger_route"),
        "ambient_c_d_global_solubility_status": entry.get(
            "ambient_c_d_global_solubility", {}
        ).get("status"),
        "wl491_filter_output_class": entry.get("wl491_filter_result", {}).get(
            "output_class"
        ),
    }


def _iter_ledger_entries(payload: dict[str, Any]) -> list[dict[str, Any]]:
    work_log = payload["work_log"]
    entries: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for field in LEDGER_ENTRY_FIELDS:
        for entry in payload.get(field, []) or []:
            if not isinstance(entry, dict) or "candidate_id" not in entry:
                continue
            key = (field, entry["candidate_id"])
            if key in seen:
                continue
            seen.add(key)
            entries.append(_normal_entry(work_log, entry))
    return entries


def _final_candidate_ledgers(payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for payload in sorted(payloads, key=lambda item: _work_log_number(item["work_log"])):
        for entry in _iter_ledger_entries(payload):
            candidate_id = entry["candidate_id"]
            previous = latest.get(candidate_id)
            if previous is None or _work_log_number(entry["source_work_log"]) >= _work_log_number(
                previous["source_work_log"]
            ):
                latest[candidate_id] = entry
    return sorted(
        latest.values(),
        key=lambda entry: (
            entry["support_family"],
            str(entry["sample"].get("L")),
            str(entry["sample"].get("T")),
            entry["candidate_id"],
        ),
    )


def _status_counts(entries: list[dict[str, Any]]) -> dict[str, int]:
    return {
        status: sum(1 for entry in entries if entry["classification"] == status)
        for status in STATUS_ORDER
    }


def _family_classification(entries: list[dict[str, Any]]) -> str:
    statuses = {entry["classification"] for entry in entries}
    if "genuinely_deferred" in statuses:
        return "genuinely_deferred"
    if "already_closed" in statuses:
        return "already_closed"
    if "globally_soluble_but_not_aa_bb_admissible" in statuses:
        return "globally_soluble_but_not_aa_bb_admissible"
    return "refuted"


def _group_by(entries: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        grouped.setdefault(entry[key], []).append(entry)
    return grouped


def _support_family_synthesis(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped = _group_by(entries, "support_family")
    rows = []
    for support_family, family_entries in grouped.items():
        rows.append(
            {
                "support_family": support_family,
                "classification": _family_classification(family_entries),
                "status_counts": _status_counts(family_entries),
                "entry_count": len(family_entries),
                "cover_family_count": len({entry["cover_family"] for entry in family_entries}),
                "candidate_ids": sorted(entry["candidate_id"] for entry in family_entries),
                "work_logs": sorted(
                    {entry["source_work_log"] for entry in family_entries},
                    key=_work_log_number,
                ),
            }
        )
    return sorted(rows, key=lambda row: row["support_family"])


def _cover_family_synthesis(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped = _group_by(entries, "cover_family")
    rows = []
    for cover_family, family_entries in grouped.items():
        rows.append(
            {
                "cover_family": cover_family,
                "support_family": family_entries[0]["support_family"],
                "classification": _family_classification(family_entries),
                "candidate_ids": sorted(entry["candidate_id"] for entry in family_entries),
                "entry_count": len(family_entries),
                "work_logs": sorted(
                    {entry["source_work_log"] for entry in family_entries},
                    key=_work_log_number,
                ),
                "cover_summary": family_entries[0]["cover_summary"],
            }
        )
    return sorted(rows, key=lambda row: row["cover_family"])


def _ledger_summary(
    *,
    entries: list[dict[str, Any]],
    support_rows: list[dict[str, Any]],
    cover_rows: list[dict[str, Any]],
) -> dict[str, int]:
    counts = _status_counts(entries)
    return {
        "final_candidate_ledger_entry_count": len(entries),
        "support_family_count": len(support_rows),
        "cover_family_count": len(cover_rows),
        "refuted_entry_count": counts["refuted"],
        "globally_soluble_but_not_aa_bb_admissible_entry_count": counts[
            "globally_soluble_but_not_aa_bb_admissible"
        ],
        "genuinely_deferred_entry_count": counts["genuinely_deferred"],
        "already_closed_entry_count": counts["already_closed"],
        "aa_bb_admissible_entry_count": 0,
    }


def _genuinely_deferred_cover_families(cover_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        row
        for row in cover_rows
        if row["classification"] == "genuinely_deferred"
    ]


def _theorem_candidate_patterns(
    deferred_cover_rows: list[dict[str, Any]],
    support_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    support_by_id = {row["support_family"]: row for row in support_rows}
    patterns = []
    for row in deferred_cover_rows:
        support_family = row["support_family"]
        support = support_by_id.get(support_family, {})
        counts = support.get("status_counts", {})
        if support_family == "u_5" and counts.get("refuted") and counts.get(
            "globally_soluble_but_not_aa_bb_admissible"
        ):
            patterns.append(
                {
                    "pattern_id": "u5_mirror_deferred_cover_after_mixed_u5_history",
                    "support_family": "u_5",
                    "current_cover_family": row["cover_family"],
                    "candidate_ids": row["candidate_ids"],
                    "status": "candidate_pattern_not_theorem",
                    "why_interesting": (
                        "The same u_5 d-vector family already has a refuted "
                        "shell-5 cover and a shell-10 globally soluble but not "
                        "AA+BB-admissible mirror cover; the only remaining open "
                        "instance is the shared L=10,T=19 cover."
                    ),
                }
            )
    return patterns


def _route_options() -> dict[str, dict[str, str]]:
    return {
        "resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover": {
            "decision": "selected_next_narrow_gate",
            "reason": (
                "The wl491-wl517 family synthesis leaves exactly one genuinely "
                "deferred cover family: the two mirror shell-10 u_5 entries "
                "sharing L=10,T=19,d=(5,5,1). Resolving that cover is narrower "
                "than shell 11 or a proof-level generalization."
            ),
        },
        "proof_level_generalization_task": {
            "decision": "defer_until_current_deferred_cover_is_classified",
            "reason": (
                "A proof-level generalization would be meaningful only after "
                "the current shared shell-10 u_5 ambient C_d cover is either "
                "globally soluble and filtered by wl491, or refuted by an "
                "explicit certificate."
            ),
        },
        "execute_shell11": {
            "decision": "reject",
            "reason": (
                "Shell 10 still has a genuinely deferred ambient C_d cover, "
                "so widening to shell 11 would skip the current narrow gap."
            ),
        },
        "select_final_obstruction_candidate": {
            "decision": "reject",
            "reason": (
                "No AA+BB-admissible ambient C_d point appears in the family "
                "synthesis, and the only open cover is still deferred."
            ),
        },
    }


def _selected_next_gate(deferred_cover_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(deferred_cover_rows) != 1:
        return {
            "gate": "not_selected_deferred_cover_family_count_not_one",
            "entered_here": False,
        }
    row = deferred_cover_rows[0]
    return {
        "gate": "resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover",
        "entered_here": False,
        "candidate_ids": row["candidate_ids"],
        "shared_cover": "L=10,T=19,d=(5,5,1)",
        "shared_cover_summary": row["cover_summary"],
        "allowed_future_certificates": [
            "exact_ambient_C_d_global_point",
            "exhaustive_no_lift_certificate",
        ],
        "wl491_filter_allowed_only_after_global_solubility": True,
        "shell11_executed_here": False,
        "resolved_shell10_deferred_covers_here": False,
        "new_local_row_proved_here": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "candidate_selected_here": False,
        "minimum_later_question": (
            "Resolve the shared shell-10 u_5 ambient C_d cover at "
            "L=10,T=19,d=(5,5,1) by either an exact ambient point or an "
            "exhaustive no-lift certificate; apply wl491 only after ambient "
            "global solubility is established."
        ),
    }


def build_wl518_support_family_synthesis_after_wl517(
    *,
    ledger_payloads: list[dict[str, Any]],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _payloads_ready(ledger_payloads):
        violations.append("wl491_to_wl517_inputs_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    entries = _final_candidate_ledgers(ledger_payloads) if status == "ok" else []
    support_rows = _support_family_synthesis(entries)
    cover_rows = _cover_family_synthesis(entries)
    deferred_cover_rows = _genuinely_deferred_cover_families(cover_rows)
    patterns = _theorem_candidate_patterns(deferred_cover_rows, support_rows)

    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl491-wl517 ledger outputs with wl517 as immediate input",
        "pattern": "AA+BB",
        "lemma_id": "WL518_support_family_synthesis_after_wl517",
        "work_log": "wl518",
        "input_work_log": "wl517",
        "input_work_logs": list(EXPECTED_INPUT_WORK_LOGS),
        "support_family_synthesis_built_here": status == "ok",
        "aggregation_axis": [
            "support_family",
            "cover_family",
        ],
        "ledger_summary": _ledger_summary(
            entries=entries,
            support_rows=support_rows,
            cover_rows=cover_rows,
        ),
        "final_candidate_ledgers": entries,
        "support_family_synthesis": support_rows,
        "cover_family_synthesis": cover_rows,
        "genuinely_deferred_cover_families": deferred_cover_rows,
        "theorem_candidate_patterns": patterns,
        "route_options": _route_options(),
        "selected_next_gate": _selected_next_gate(deferred_cover_rows),
        "closed_ledgers_reopened_count": 0,
        "not_admissible_ledgers_reopened_count": 0,
        "refuted_ledgers_reopened_count": 0,
        "resolved_shell10_deferred_covers_here": False,
        "new_c_d_solubility_tested_here": False,
        "wl491_filter_applied_to_new_point_here": False,
        "shell11_executed_here": False,
        "candidate_selected_here": False,
        "new_m_tail_or_kernel_candidate_selected_here": False,
        "new_m_tail_row_proved_here": False,
        "new_local_row_proved_here": False,
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
        "advance_to_selected_next_gate": False,
        "advance_to_wl519": False,
        "stop_after_current_task": True,
        "next_gap_not_entered": (
            "wl518 selects targeted resolution of the shared shell-10 u_5 "
            "ambient C_d cover, but does not enter that gate, resolve the "
            "cover, execute shell 11, or pivot to proof-level generalization."
        ),
        "violations": violations,
        "boundary": BOUNDARY,
    }


def load_wl491_to_wl517_payloads(ledger_dir: Path) -> list[dict[str, Any]]:
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
    audit = build_wl518_support_family_synthesis_after_wl517(
        ledger_payloads=load_wl491_to_wl517_payloads(args.ledger_dir)
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB wl518 support-family synthesis to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"selected_gate={audit['selected_next_gate']['gate']}")
    print(
        "genuinely_deferred_cover_family_count="
        f"{len(audit['genuinely_deferred_cover_families'])}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
