#!/usr/bin/env python3
"""Summarize 2-cover/Selmer frontier for residual lambda classes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This summarizes residual 2-cover/Selmer lambda frontier targets. "
    "Bounded-search no-point candidates are not no-point proofs."
)

REQUIRED_STRICT_EVIDENCE = [
    "family 2-cover or Selmer obstruction",
    "or reviewable cover-level no-point certificates for every listed cover",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _target_from_pair(row: dict[str, Any]) -> dict[str, Any]:
    residual_rows = list(row.get("residual_cover_rows", []))
    candidate_cover_count = sum(
        len(cover_row.get("no_point_cover_indices", []))
        for cover_row in residual_rows
    )
    return {
        "class": str(row.get("c_ratio_class", "")),
        "primitive_A": int(row.get("primitive_A", 0)),
        "primitive_B": int(row.get("primitive_B", 0)),
        "lambda": str(row.get("lambda", "")),
        "c_ratio": str(row.get("c_ratio", "")),
        "observed_pair": [int(row.get("A", 0)), int(row.get("B", 0))],
        "rank_counts_by_curve": row.get("rank_counts_by_curve", {}),
        "residual_cover_rows": residual_rows,
        "candidate_cover_count": candidate_cover_count,
        "required_strict_evidence": REQUIRED_STRICT_EVIDENCE,
        "family_exclusion_proved": False,
        "candidate_not_proof": True,
    }


def summarize_two_cover_frontier(ray_ledger: dict[str, Any]) -> dict[str, Any]:
    targets = [
        _target_from_pair(row)
        for row in ray_ledger.get("pair_rows", [])
        if row.get("status") == "residual-candidate-not-proof"
    ]
    selmer_gap_counts: Counter[str] = Counter()
    evidence_level_counts: Counter[str] = Counter()
    for target in targets:
        for row in target["residual_cover_rows"]:
            selmer_gap_counts[str(row.get("selmer_gap", ""))] += 1
            evidence_level_counts[str(row.get("evidence_level", ""))] += 1
    return {
        "status": "ok",
        "ready": True,
        "target_class_count": len(targets),
        "target_pair_count": len({tuple(target["observed_pair"]) for target in targets}),
        "candidate_cover_total": sum(
            int(target["candidate_cover_count"]) for target in targets
        ),
        "selmer_gap_counts": dict(sorted(selmer_gap_counts.items())),
        "evidence_level_counts": dict(sorted(evidence_level_counts.items())),
        "family_exclusion_proved_count": 0,
        "targets": targets,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ray-ledger", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = summarize_two_cover_frontier(load_json(args.ray_ledger))
    write_json(args.out, audit)
    print(f"wrote closure quotient two-cover lambda frontier to {args.out}")
    print(f"status={audit['status']}")
    print(f"target_class_count={audit['target_class_count']}")
    print(f"candidate_cover_total={audit['candidate_cover_total']}")
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
