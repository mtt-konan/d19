#!/usr/bin/env python3
"""Summarize certifying invariants for rank-zero primitive models."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This summarizes observed rank-zero certifying invariants after collapsing "
    "scaled pairs to primitive lambda models. It does not prove any lambda-family "
    "exclusion theorem."
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


def _primitive_targets(
    primitive_models: dict[str, Any],
) -> dict[tuple[str, str], dict[str, Any]]:
    targets: dict[tuple[str, str], dict[str, Any]] = {}
    for row in primitive_models.get("primitive_model_rows", []):
        class_name = str(row.get("class", ""))
        primitive_ray = row.get("unordered_primitive_ray", [])
        for model in row.get("models", []):
            curve = str(model.get("curve", ""))
            targets[(class_name, curve)] = {
                "class": class_name,
                "curve": curve,
                "unordered_primitive_ray": primitive_ray,
            }
    return targets


def _status_for_model(
    *,
    rank_keys: list[str],
    torsion_orders: list[int],
    root_numbers: list[int],
) -> str:
    if rank_keys == ["0/0"] and torsion_orders == [4] and root_numbers == [1]:
        return "observed-rank-zero-torsion4-root1"
    return "observed-invariant-mixed"


def summarize_certifying_invariants(
    *,
    primitive_models: dict[str, Any],
    rank_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    targets = _primitive_targets(primitive_models)
    grouped_rank_rows: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rank_rows:
        key = (_class_name(int(row["A"]), int(row["B"])), str(row.get("curve", "")))
        if key in targets:
            grouped_rank_rows[key].append(row)

    models: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    rank_key_counts: Counter[str] = Counter()
    torsion_order_counts: Counter[str] = Counter()
    root_number_counts: Counter[str] = Counter()
    sha2_lower_value_counts: Counter[str] = Counter()

    for key, target in sorted(targets.items()):
        rows = grouped_rank_rows.get(key, [])
        if not rows:
            missing.append(target)
            continue

        observed_pairs = sorted({(int(row["A"]), int(row["B"])) for row in rows})
        rank_keys = sorted({_rank_key(row) for row in rows})
        torsion_orders = sorted({int(row["torsion_order"]) for row in rows})
        root_numbers = sorted({int(row["root_number"]) for row in rows})
        sha2_lower_values = sorted({int(row["sha2_lower"]) for row in rows})

        for rank_key in rank_keys:
            rank_key_counts[rank_key] += 1
        for torsion_order in torsion_orders:
            torsion_order_counts[str(torsion_order)] += 1
        for root_number in root_numbers:
            root_number_counts[str(root_number)] += 1
        for row in rows:
            sha2_lower_value_counts[str(int(row["sha2_lower"]))] += 1

        models.append(
            {
                "class": target["class"],
                "curve": target["curve"],
                "unordered_primitive_ray": target["unordered_primitive_ray"],
                "observed_pairs": [[A, B] for A, B in observed_pairs],
                "rank_keys": rank_keys,
                "torsion_orders": torsion_orders,
                "root_numbers": root_numbers,
                "sha2_lower_values": sha2_lower_values,
                "certifying_invariant_status": _status_for_model(
                    rank_keys=rank_keys,
                    torsion_orders=torsion_orders,
                    root_numbers=root_numbers,
                ),
                "family_exclusion_proved": False,
            }
        )

    all_rank_zero = all(model["rank_keys"] == ["0/0"] for model in models)
    all_torsion_order_four = all(model["torsion_orders"] == [4] for model in models)
    all_root_number_one = all(model["root_numbers"] == [1] for model in models)
    status = "ok" if not missing else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "primitive_model_count": len(targets),
        "matched_primitive_model_count": len(models),
        "missing_primitive_model_count": len(missing),
        "matched_rank_row_count": sum(len(rows) for rows in grouped_rank_rows.values()),
        "family_exclusion_proved_count": 0,
        "rank_key_counts": dict(sorted(rank_key_counts.items())),
        "torsion_order_counts": dict(sorted(torsion_order_counts.items())),
        "root_number_counts": dict(sorted(root_number_counts.items())),
        "sha2_lower_value_counts": dict(sorted(sha2_lower_value_counts.items())),
        "all_matched_models_rank_zero": all_rank_zero,
        "all_matched_models_torsion_order_four": all_torsion_order_four,
        "all_matched_models_root_number_one": all_root_number_one,
        "models": models,
        "missing_primitive_models": missing,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primitive-models", type=Path, required=True)
    parser.add_argument("--rank-jsonl", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = summarize_certifying_invariants(
        primitive_models=load_json(args.primitive_models),
        rank_rows=load_jsonl(args.rank_jsonl),
    )
    write_json(args.out, summary)
    print(f"wrote closure quotient rank-zero certifying invariants to {args.out}")
    print(f"status={summary['status']}")
    print(f"primitive_model_count={summary['primitive_model_count']}")
    print(f"matched_primitive_model_count={summary['matched_primitive_model_count']}")
    print(f"matched_rank_row_count={summary['matched_rank_row_count']}")
    print(f"family_exclusion_proved_count={summary['family_exclusion_proved_count']}")
    if args.strict and summary["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
