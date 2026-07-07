#!/usr/bin/env python3
"""Group rank-zero primitive models into proof-seed buckets."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This groups rank-zero primitive model seeds for future lambda-family proof "
    "work. It does not prove any family exclusion theorem."
)

NEXT_ACTION = (
    "Try to prove this rank-zero pattern as a primitive lambda family; this "
    "seed group is not itself a theorem."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _pattern(row: dict[str, Any]) -> str:
    return "+".join(str(pattern) for pattern in row.get("certifying_curve_patterns", []))


def _p_sign(p_value: object) -> str:
    p = int(p_value)
    if p < 0:
        return "negative"
    if p > 0:
        return "positive"
    return "zero"


def summarize_rank_zero_proof_seeds(
    primitive_models: dict[str, Any],
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    rows = list(primitive_models.get("primitive_model_rows", []))
    for row in rows:
        grouped[_pattern(row)].append(row)

    groups: list[dict[str, Any]] = []
    for pattern, pattern_rows in sorted(grouped.items()):
        model_counts_by_curve: Counter[str] = Counter()
        p_sign_counts: Counter[str] = Counter()
        classes: list[str] = []
        model_count = 0

        for row in pattern_rows:
            classes.append(str(row.get("class", "")))
            for model in row.get("models", []):
                model_count += 1
                model_counts_by_curve[str(model.get("curve", ""))] += 1
                p_sign_counts[_p_sign(model.get("p", 0))] += 1

        groups.append(
            {
                "pattern": pattern,
                "candidate_class_count": len(pattern_rows),
                "model_count": model_count,
                "model_counts_by_curve": dict(sorted(model_counts_by_curve.items())),
                "p_sign_counts": dict(sorted(p_sign_counts.items())),
                "classes": sorted(classes),
                "family_exclusion_proved": False,
                "next_action": NEXT_ACTION,
            }
        )

    return {
        "status": "ok",
        "ready": True,
        "seed_group_count": len(groups),
        "candidate_class_count": len(rows),
        "model_count": sum(group["model_count"] for group in groups),
        "family_exclusion_proved_count": 0,
        "groups": groups,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primitive-models", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = summarize_rank_zero_proof_seeds(load_json(args.primitive_models))
    write_json(args.out, summary)
    print(f"wrote closure quotient rank-zero proof seeds to {args.out}")
    print(f"status={summary['status']}")
    print(f"seed_group_count={summary['seed_group_count']}")
    print(f"candidate_class_count={summary['candidate_class_count']}")
    print(f"model_count={summary['model_count']}")
    print(f"family_exclusion_proved_count={summary['family_exclusion_proved_count']}")
    if args.strict and summary["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
