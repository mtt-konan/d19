"""Load and assemble the tracked A1 arithmetic certificate layer."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.theory.aa_bb.a1_ambient import verify_cover_certificate
from scripts.theory.aa_bb.a1_shells import SHELL_BOUNDS, ShellResult, evaluate_shell


@dataclass(frozen=True)
class A1Evidence:
    shells: dict[int, ShellResult]
    certificates: tuple[dict[str, Any], ...]
    cover_stages: dict[str, tuple[dict[str, Any], ...]]


def load_certificates(path: Path) -> tuple[dict[str, Any], ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if (
        set(payload) != {"schema_version", "kind", "rows"}
        or payload["schema_version"] != 1
        or payload["kind"] != "a1-certificates"
    ):
        raise ValueError("invalid A1 certificate document")
    rows = payload["rows"]
    if len(rows) != 12:
        raise ValueError(f"expected 12 A1 certificates, got {len(rows)}")
    ids = [row["certificate_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate A1 certificate ID")
    if sum(row["status"] == "globally_not_soluble" for row in rows) != 4:
        raise ValueError("expected four no-lift certificates")
    if sum(row["status"] == "globally_soluble" for row in rows) != 8:
        raise ValueError("expected eight exact-point certificates")
    for row in rows:
        if not verify_cover_certificate(row).passed:
            raise ValueError(f"certificate arithmetic failed: {row['certificate_id']}")
    return tuple(rows)


def build_a1(a0: Any, certificates: tuple[dict[str, Any], ...]) -> A1Evidence:
    ids = {row["candidate_id"] for row in a0.ledger}
    for certificate in certificates:
        if not set(certificate["candidate_ids"]).issubset(ids):
            raise ValueError(f"certificate aliases absent from A0: {certificate['certificate_id']}")
    shells = {bound: evaluate_shell(a0, bound) for bound in SHELL_BOUNDS}
    ledger = {row["candidate_id"]: row for row in a0.ledger}
    certificate_by_candidate = {
        candidate_id: row
        for row in certificates
        for candidate_id in row["candidate_ids"]
    }
    witness_ids = {row["candidate_id"] for row in a0.witnesses}
    stage_ids = {
        "wl500": [
            candidate_id
            for row in certificates
            if row["source_work_log"] == "wl500"
            for candidate_id in row["candidate_ids"]
        ],
        "wl505": [row["candidate_id"] for row in shells[7].active_supports],
        "wl506": [
            candidate_id
            for row in certificates
            if row["source_work_log"] == "wl506"
            for candidate_id in row["candidate_ids"]
        ],
        "wl511": [row["candidate_id"] for row in shells[9].active_supports],
        "wl512": [
            candidate_id
            for row in certificates
            if row["source_work_log"] in {"wl512", "wl514"}
            for candidate_id in row["candidate_ids"]
        ],
        "wl514": [
            candidate_id
            for row in certificates
            if row["source_work_log"] == "wl514"
            for candidate_id in row["candidate_ids"]
        ],
        "wl517": [row["candidate_id"] for row in shells[10].active_supports],
        "wl519": [
            candidate_id
            for row in certificates
            if row["source_work_log"] == "wl519"
            for candidate_id in row["candidate_ids"]
        ],
    }

    cover_stages = {}
    for work_log, candidate_ids in stage_ids.items():
        rows = []
        for candidate_id in candidate_ids:
            ledger_row = ledger[candidate_id]
            certificate = certificate_by_candidate.get(candidate_id)
            status = "global_solubility_deferred"
            certificate_type = "none_recorded_here"
            point_ref = None
            if work_log == "wl505" and candidate_id in witness_ids:
                status = "globally_soluble"
                certificate_type = "exact_integral_point_on_C_d"
                point_ref = f"a0:{candidate_id}"
            elif certificate is not None and certificate["source_work_log"] == work_log:
                status = certificate["status"]
                certificate_type = certificate["certificate_type"]
                if status == "globally_soluble":
                    point_ref = f"a1:{certificate['certificate_id']}"
            row = {
                "candidate_id": candidate_id,
                "d_vector": ledger_row["cover_summary"]["d_vector"],
                "ambient_status": status,
                "certificate_type": certificate_type,
            }
            if point_ref is not None:
                row["point_ref"] = point_ref
            rows.append(row)
        cover_stages[work_log] = tuple(rows)
    return A1Evidence(shells, certificates, cover_stages)


def project_a1(a1: A1Evidence, work_log: str) -> dict[str, Any]:
    number = int(work_log.removeprefix("wl"))
    shell_map = {502: 6, 504: 7, 508: 8, 510: 9, 516: 10}
    if number in shell_map:
        return a1.shells[shell_map[number]].projection()
    if work_log in a1.cover_stages:
        rows = list(a1.cover_stages[work_log])
        return {
            "work_log": work_log,
            "candidate_rows": rows,
            "status_counts": dict(
                sorted(Counter(row["ambient_status"] for row in rows).items())
            ),
        }
    certificates = [row for row in a1.certificates if work_log in row["consumed_at"]]
    return {
        "work_log": work_log,
        "certificates": certificates,
        "certificate_count": len(certificates),
        "no_claims": {
            "complete_selmer_upper_bound_proved": False,
            "rank_zero_claimed": False,
            "sha2_trivial_claimed": False,
            "uniform_m_tail_full_rank_claimed": False,
            "family_exclusion_proved_count": 0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    args = parser.parse_args()
    from scripts.theory.aa_bb.consolidation_inputs import load_a0

    a0 = load_a0(args.data_dir)
    certificates = load_certificates(args.data_dir / "a1-certificates.v1.json")
    evidence = build_a1(a0, certificates)
    print(
        json.dumps(
            {
                "status": "ok",
                "certificate_count": len(evidence.certificates),
                "shell_summaries": {
                    str(bound): result.summary for bound, result in evidence.shells.items()
                },
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
