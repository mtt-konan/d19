#!/usr/bin/env python3
"""Summarize rank-zero family-generalization candidates from the ray ledger."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This summarizes observed rank-zero local-tool candidates for future "
    "lambda-family generalization. It does not prove any family exclusion."
)

NEXT_ACTION = (
    "Try to prove the listed AA/BB rank-zero mechanism over the primitive "
    "lambda class; do not add more scaled pair samples as the main progress "
    "metric."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _class_rows(ray_ledger: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("class", "")): row
        for row in ray_ledger.get("c_ratio_class_rows", [])
    }


def _strict_pair_rows(ray_ledger: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in ray_ledger.get("pair_rows", []):
        if row.get("status") == "strict-local-tool-excludes-observed-pair":
            grouped[str(row.get("c_ratio_class", ""))].append(row)
    return dict(grouped)


def summarize_rank_zero_family_candidates(
    ray_ledger: dict[str, Any],
) -> dict[str, Any]:
    classes = _class_rows(ray_ledger)
    strict_pairs = _strict_pair_rows(ray_ledger)
    candidates: list[dict[str, Any]] = []
    pattern_counts: Counter[str] = Counter()
    strict_observed_pair_count = 0

    for class_name, pairs in sorted(strict_pairs.items()):
        class_row = classes.get(class_name, {})
        patterns = sorted(
            {
                str(curve)
                for pair in pairs
                for curve in pair.get("certifying_curves", [])
            }
        )
        for pattern in patterns:
            pattern_counts[pattern] += 1
        strict_observed_pair_count += len(pairs)
        candidates.append(
            {
                "class": class_name,
                "unordered_primitive_ray": class_row.get(
                    "unordered_primitive_ray",
                    [],
                ),
                "possible_oriented_rays": class_row.get(
                    "possible_oriented_rays",
                    [],
                ),
                "c_ratio": str(class_row.get("c_ratio", "")),
                "coverage_status": str(class_row.get("coverage_status", "")),
                "observed_pair_count": len(
                    [
                        row
                        for row in ray_ledger.get("pair_rows", [])
                        if row.get("c_ratio_class") == class_name
                    ]
                ),
                "strict_observed_pair_count": len(pairs),
                "certifying_curve_patterns": patterns,
                "family_exclusion_proved": False,
                "next_action": NEXT_ACTION,
            }
        )

    return {
        "status": "ok",
        "ready": True,
        "candidate_class_count": len(candidates),
        "strict_observed_pair_count": strict_observed_pair_count,
        "family_exclusion_proved_count": 0,
        "certifying_curve_pattern_counts": dict(sorted(pattern_counts.items())),
        "candidates": candidates,
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
    audit = summarize_rank_zero_family_candidates(load_json(args.ray_ledger))
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero family candidates to {args.out}")
    print(f"status={audit['status']}")
    print(f"candidate_class_count={audit['candidate_class_count']}")
    print(f"strict_observed_pair_count={audit['strict_observed_pair_count']}")
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
