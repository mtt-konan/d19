#!/usr/bin/env python3
"""Summarize root-number/rank-pattern triage for lambda classes."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This summarizes root-number and rank-key diagnostics for lambda classes. "
    "Root number is a routing signal here, not a no-point proof."
)

NEXT_ACTION = (
    "Use this root-number/rank pattern only to choose a family rank or descent "
    "problem; root number alone is not a no-point proof."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _class_name(A: int, B: int) -> str:
    scale = math.gcd(A, B)
    primitive = sorted((A // scale, B // scale))
    return f"{primitive[0]}:{primitive[1]}"


def _rank_key(row: dict[str, Any]) -> str:
    if row.get("status") == "ok":
        return f"{row.get('rank_lower')}/{row.get('rank_upper')}"
    return str(row.get("status", "unknown"))


def _pattern(by_curve: dict[str, list[Any]]) -> str:
    return "|".join(
        f"{curve}:{','.join(str(value) for value in values)}"
        for curve, values in sorted(by_curve.items())
    )


def _target_classes(ray_ledger: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("class", "")): row
        for row in ray_ledger.get("c_ratio_class_rows", [])
        if row.get("coverage_status") == "observed-open"
    }


def summarize_root_number_triage(
    *,
    rank_rows: list[dict[str, Any]],
    ray_ledger: dict[str, Any],
) -> dict[str, Any]:
    target_classes = _target_classes(ray_ledger)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rank_rows:
        class_name = _class_name(int(row["A"]), int(row["B"]))
        if class_name in target_classes:
            grouped[class_name].append(row)

    targets: list[dict[str, Any]] = []
    root_pattern_counts: Counter[str] = Counter()
    rank_pattern_counts: Counter[str] = Counter()
    for class_name, rows in sorted(grouped.items()):
        class_row = target_classes[class_name]
        root_numbers_by_curve: dict[str, list[int]] = defaultdict(list)
        rank_keys_by_curve: dict[str, list[str]] = defaultdict(list)
        pairs = sorted({(int(row["A"]), int(row["B"])) for row in rows})
        for row in rows:
            curve = str(row["curve"])
            root_number = row.get("root_number")
            if root_number is not None:
                value = int(root_number)
                if value not in root_numbers_by_curve[curve]:
                    root_numbers_by_curve[curve].append(value)
            rank_key = _rank_key(row)
            if rank_key not in rank_keys_by_curve[curve]:
                rank_keys_by_curve[curve].append(rank_key)

        sorted_roots = {
            curve: sorted(values)
            for curve, values in sorted(root_numbers_by_curve.items())
        }
        sorted_ranks = {
            curve: sorted(values)
            for curve, values in sorted(rank_keys_by_curve.items())
        }
        root_pattern = _pattern(sorted_roots)
        rank_pattern = _pattern(sorted_ranks)
        root_pattern_counts[root_pattern] += 1
        rank_pattern_counts[rank_pattern] += 1
        targets.append(
            {
                "class": class_name,
                "unordered_primitive_ray": class_row.get(
                    "unordered_primitive_ray",
                    [],
                ),
                "c_ratio": str(class_row.get("c_ratio", "")),
                "coverage_status": str(class_row.get("coverage_status", "")),
                "observed_pairs": [[A, B] for A, B in pairs],
                "root_numbers_by_curve": sorted_roots,
                "rank_keys_by_curve": sorted_ranks,
                "root_number_pattern": root_pattern,
                "rank_key_pattern": rank_pattern,
                "family_exclusion_proved": False,
                "next_action": NEXT_ACTION,
            }
        )

    return {
        "status": "ok",
        "ready": True,
        "target_class_count": len(targets),
        "target_pair_count": sum(len(target["observed_pairs"]) for target in targets),
        "family_exclusion_proved_count": 0,
        "root_number_pattern_counts": dict(sorted(root_pattern_counts.items())),
        "rank_key_pattern_counts": dict(sorted(rank_pattern_counts.items())),
        "targets": targets,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank-jsonl", type=Path, action="append", required=True)
    parser.add_argument("--ray-ledger", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = summarize_root_number_triage(
        rank_rows=load_jsonl(args.rank_jsonl),
        ray_ledger=load_json(args.ray_ledger),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient root-number lambda triage to {args.out}")
    print(f"status={audit['status']}")
    print(f"target_class_count={audit['target_class_count']}")
    print(f"target_pair_count={audit['target_pair_count']}")
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
