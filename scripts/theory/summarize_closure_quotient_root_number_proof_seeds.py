#!/usr/bin/env python3
"""Group root-number lambda triage targets into combined proof seeds."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This groups root-number/rank diagnostic patterns for future lambda-family "
    "routing. It does not prove any no-point or family exclusion theorem."
)

NEXT_ACTION = (
    "Study this combined root-number/rank pattern as a lambda family routing "
    "problem; it is not a no-point proof."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _combined_pattern(root_number_pattern: str, rank_key_pattern: str) -> str:
    return f"root[{root_number_pattern}] rank[{rank_key_pattern}]"


def summarize_root_number_proof_seeds(triage: dict[str, Any]) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for target in triage.get("targets", []):
        grouped[
            (
                str(target.get("root_number_pattern", "")),
                str(target.get("rank_key_pattern", "")),
            )
        ].append(target)

    groups: list[dict[str, Any]] = []
    for (root_number_pattern, rank_key_pattern), targets in sorted(
        grouped.items(),
        key=lambda item: (-len(item[1]), item[0]),
    ):
        classes = sorted(str(target.get("class", "")) for target in targets)
        target_pair_count = sum(
            len(target.get("observed_pairs", [])) for target in targets
        )
        groups.append(
            {
                "root_number_pattern": root_number_pattern,
                "rank_key_pattern": rank_key_pattern,
                "combined_pattern": _combined_pattern(
                    root_number_pattern,
                    rank_key_pattern,
                ),
                "target_class_count": len(targets),
                "target_pair_count": target_pair_count,
                "classes": classes,
                "family_exclusion_proved": False,
                "next_action": NEXT_ACTION,
            }
        )

    return {
        "status": "ok",
        "ready": True,
        "seed_group_count": len(groups),
        "target_class_count": sum(group["target_class_count"] for group in groups),
        "target_pair_count": sum(group["target_pair_count"] for group in groups),
        "family_exclusion_proved_count": 0,
        "groups": groups,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = summarize_root_number_proof_seeds(load_json(args.triage))
    write_json(args.out, summary)
    print(f"wrote closure quotient root-number proof seeds to {args.out}")
    print(f"status={summary['status']}")
    print(f"seed_group_count={summary['seed_group_count']}")
    print(f"target_class_count={summary['target_class_count']}")
    print(f"target_pair_count={summary['target_pair_count']}")
    print(f"family_exclusion_proved_count={summary['family_exclusion_proved_count']}")
    if args.strict and summary["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
