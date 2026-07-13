"""Taxonomy, point-level lemma, and route-boundary projections for A2."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.theory.aa_bb.consolidation_inputs import A2_DESTINATIONS

ROUTE_CHOICES = {
    "abandon_this_obstruction_line_and_select_different_candidate",
    "gather_minimal_function_field_squareclass_proof_data_for_named_cover_families",
    "name_theorem_level_complete_selmer_local_hilbert_row_obligation",
    "return_to_finite_shell_m_tail_diagnostics",
}
NO_CLAIM_KEYS = {
    "broad_rank_or_selmer_diagnostics_run",
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "family_exclusion_proved",
    "final_obstruction_candidate_selected",
    "new_local_row_proved",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
    "uniform_m_tail_full_rank_claimed",
}


@dataclass(frozen=True)
class A2Evidence:
    ledger: tuple[dict[str, Any], ...]
    taxonomy: tuple[dict[str, Any], ...]
    inventory: tuple[dict[str, Any], ...]
    boundary: dict[str, Any]


def load_boundary_spec(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if set(payload) != {
        "schema_version", "kind", "work_logs", "route_choices", "no_claims",
        "source_payloads", "stages",
    }:
        raise ValueError("invalid A2 boundary spec keys")
    if payload["schema_version"] != 1 or payload["kind"] != "a2-boundary-spec":
        raise ValueError("invalid A2 boundary spec version/kind")
    expected_work_logs = {f"wl{number}": A2_DESTINATIONS[number] for number in range(500, 528)}
    if payload["work_logs"] != expected_work_logs:
        raise ValueError("A2 worklog-destination mapping mismatch")
    if set(payload["route_choices"]) != ROUTE_CHOICES or len(payload["route_choices"]) != 4:
        raise ValueError("A2 route choice set mismatch")
    if set(payload["no_claims"]) != NO_CLAIM_KEYS or any(payload["no_claims"].values()):
        raise ValueError("A2 theorem boundary was weakened")
    if set(payload["stages"]) != set(expected_work_logs):
        raise ValueError("A2 stage projection set mismatch")
    if set(payload["source_payloads"]) != set(expected_work_logs):
        raise ValueError("A2 source provenance set mismatch")
    for work_log, destination in expected_work_logs.items():
        if payload["stages"][work_log].get("destination") != destination:
            raise ValueError(f"A2 stage destination mismatch: {work_log}")
        source = payload["source_payloads"][work_log]
        if set(source) != {"path", "sha256", "size"} or len(source["sha256"]) != 64:
            raise ValueError(f"A2 source provenance invalid: {work_log}")
    return payload


def build_a2(a0: Any, a1: Any, boundary_spec: dict[str, Any]) -> A2Evidence:
    if len(a1.certificates) != 12:
        raise ValueError("A1 certificate layer is incomplete")
    counts = Counter(row["classification"] for row in a0.ledger)
    if counts != Counter(
        {"globally_soluble_but_not_aa_bb_admissible": 29, "refuted": 10, "already_closed": 4}
    ):
        raise ValueError("A0 ledger classification parity failed")
    if len(a0.taxonomy) != 22 or len(a0.inventory) != 15:
        raise ValueError("A0 taxonomy/inventory cardinality parity failed")
    wl521_ids = {row["candidate_id"] for row in boundary_spec["stages"]["wl521"]["ledger_rows"]}
    if wl521_ids != {row["candidate_id"] for row in a0.ledger}:
        raise ValueError("A2 wl521 ledger projection mismatch")
    taxonomy = boundary_spec["stages"]["wl522"]["taxonomy_summary"]
    if taxonomy["taxonomy_row_count"] != 22 or taxonomy["final_candidate_ledger_entry_count"] != 43:
        raise ValueError("A2 wl522 taxonomy projection mismatch")
    point_refs = {
        row["point_ref"]
        for stage in boundary_spec["stages"].values()
        for row in stage.get("candidate_rows", [])
        if row["ambient_status"] == "globally_soluble"
    }
    available_refs = {f"a0:{row['candidate_id']}" for row in a0.witnesses}
    available_refs.update(f"a1:{row['certificate_id']}" for row in a1.certificates)
    if not point_refs.issubset(available_refs):
        raise ValueError("A2 cover point reference mismatch")
    return A2Evidence(tuple(a0.ledger), tuple(a0.taxonomy), tuple(a0.inventory), boundary_spec)


def _summary(a2: A2Evidence) -> dict[str, Any]:
    cover_counts = Counter(row["classification"] for row in a2.taxonomy)
    squareclass_failure_entries = sum(
        row["entry_count"]
        for row in a2.taxonomy
        if {
            "AA_common_source_product_not_square",
            "BB_common_source_product_not_square",
        }.intersection(row["blocking_reasons"])
    )
    return {
        "ledger_entry_count": len(a2.ledger),
        "support_family_count": len({row["support_family"] for row in a2.ledger}),
        "cover_family_count": len(a2.taxonomy),
        "entry_counts": dict(Counter(row["classification"] for row in a2.ledger)),
        "cover_counts": dict(cover_counts),
        "opposite_side_squareclass_failure_entry_count": squareclass_failure_entries,
        "not_ready_cover_family_count": len(a2.inventory),
        "missing_explicit_d_vector_count": sum(
            not row["cover_family_model_availability"]["has_explicit_d_vector"]
            for row in a2.inventory
        ),
    }


def project_a2(a2: A2Evidence, work_log: str) -> dict[str, Any]:
    if work_log not in a2.boundary["work_logs"]:
        raise ValueError(f"unsupported A2 work log: {work_log}")
    return {
        "work_log": work_log,
        **a2.boundary["stages"][work_log],
        "global_summary": _summary(a2),
        "no_claims": a2.boundary["no_claims"],
    }
