#!/usr/bin/env python3
"""Group 2-cover frontier targets by strict certificate need."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This groups 2-cover frontier targets by future strict certificate needs. "
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


def _rank_pattern(rank_counts_by_curve: dict[str, Any]) -> str:
    pieces: list[str] = []
    for curve, counts in sorted(rank_counts_by_curve.items()):
        rank_keys = sorted(str(key) for key in counts)
        pieces.append(f"{curve}:{','.join(rank_keys)}")
    return "|".join(pieces)


def _seed_pattern(
    *,
    curve: str,
    selmer_gap: int,
    cover_count: int,
    rank_pattern: str,
) -> str:
    return (
        f"curve={curve} selmer_gap={selmer_gap} cover_count={cover_count} "
        f"rank[{rank_pattern}]"
    )


def summarize_two_cover_proof_seeds(frontier: dict[str, Any]) -> dict[str, Any]:
    grouped: dict[tuple[str, int, int, str], list[dict[str, Any]]] = defaultdict(list)
    for target in frontier.get("targets", []):
        rank_pattern = _rank_pattern(target.get("rank_counts_by_curve", {}))
        for cover_row in target.get("residual_cover_rows", []):
            curve = str(cover_row.get("curve", ""))
            selmer_gap = int(cover_row.get("selmer_gap", 0))
            cover_count = len(cover_row.get("no_point_cover_indices", []))
            grouped[(curve, selmer_gap, cover_count, rank_pattern)].append(target)

    groups: list[dict[str, Any]] = []
    for (curve, selmer_gap, cover_count, rank_pattern), targets in sorted(
        grouped.items()
    ):
        classes = sorted(str(target.get("class", "")) for target in targets)
        target_pairs = {
            tuple(int(value) for value in target.get("observed_pair", []))
            for target in targets
        }
        groups.append(
            {
                "seed_pattern": _seed_pattern(
                    curve=curve,
                    selmer_gap=selmer_gap,
                    cover_count=cover_count,
                    rank_pattern=rank_pattern,
                ),
                "curve": curve,
                "selmer_gap": selmer_gap,
                "cover_count": cover_count,
                "rank_pattern": rank_pattern,
                "target_class_count": len(targets),
                "target_pair_count": len(target_pairs),
                "candidate_cover_total": len(targets) * cover_count,
                "classes": classes,
                "candidate_not_proof": True,
                "family_exclusion_proved": False,
                "required_strict_evidence": REQUIRED_STRICT_EVIDENCE,
            }
        )

    return {
        "status": "ok",
        "ready": True,
        "seed_group_count": len(groups),
        "target_class_count": sum(group["target_class_count"] for group in groups),
        "target_pair_count": sum(group["target_pair_count"] for group in groups),
        "candidate_cover_total": sum(group["candidate_cover_total"] for group in groups),
        "family_exclusion_proved_count": 0,
        "groups": groups,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontier", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = summarize_two_cover_proof_seeds(load_json(args.frontier))
    write_json(args.out, summary)
    print(f"wrote closure quotient two-cover proof seeds to {args.out}")
    print(f"status={summary['status']}")
    print(f"seed_group_count={summary['seed_group_count']}")
    print(f"target_class_count={summary['target_class_count']}")
    print(f"candidate_cover_total={summary['candidate_cover_total']}")
    print(f"family_exclusion_proved_count={summary['family_exclusion_proved_count']}")
    if args.strict and summary["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
