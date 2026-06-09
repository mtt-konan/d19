#!/usr/bin/env python3
"""Summarize D4-invariant coordinates for closure-first 3/4 near-miss points."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.equationize_closure_first_near_miss import equationize_sample  # noqa: E402


def _fraction(value: str | int) -> Fraction:
    return Fraction(value)


def _sorted_fraction_pair(left: Fraction, right: Fraction) -> tuple[Fraction, Fraction]:
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def _sample(record: dict[str, Any]) -> dict[str, Any]:
    sample = record["best_sample"]
    return {
        "A": int(sample["A"]),
        "B": int(sample["B"]),
        "N1": int(sample["N1"]),
        "N2": int(sample["N2"]),
        "relation": str(sample["relation"]),
        "missing_edges": list(sample["missing_edges"]),
        "failed_nearest_delta": int(sample["failed_nearest_delta"]),
        "side_n": int(sample["square_coordinate"]["side_n"]),
    }


def invariant_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return D4-invariant scalar fields for one D4-canonical point record."""
    x = _fraction(record["x"])
    y = _fraction(record["y"])
    x1mx = x * (1 - x)
    y1my = y * (1 - y)
    uv_left, uv_right = _sorted_fraction_pair(x1mx, y1my)
    sample = _sample(record)
    shared_variables = equationize_sample(
        sample["A"],
        sample["B"],
        sample["N1"],
        sample["N2"],
        sample["relation"],
    )["shared_variables"]
    shared_variable_roles = _shared_variable_roles(shared_variables)
    return {
        "x": str(x),
        "y": str(y),
        "x1mx": str(x1mx),
        "y1my": str(y1my),
        "uv_pair": [str(uv_left), str(uv_right)],
        "uv_sum": str(uv_left + uv_right),
        "uv_product": str(uv_left * uv_right),
        "raw_count": int(record["raw_count"]),
        "best_failed_nearest_delta": int(record["best_failed_nearest_delta"]),
        "best_relation": str(record["best_relation"]),
        "best_missing_edges": list(record["best_missing_edges"]),
        "side_n": sample["side_n"],
        "ab_sum": sample["A"] + sample["B"],
        "ab_diff": abs(sample["A"] - sample["B"]),
        "n_sum": sample["N1"] + sample["N2"],
        "n_diff": abs(sample["N1"] - sample["N2"]),
        "shared_variable_roles": shared_variable_roles,
        "shared_role_pattern": _shared_role_pattern(shared_variable_roles),
        "best_sample": sample,
    }


def _shared_variable_roles(
    shared_variables: dict[str, list[dict[str, Any]]]
) -> dict[str, list[str]]:
    return {
        label: [str(entry["role"]) for entry in entries]
        for label, entries in sorted(shared_variables.items())
    }


def _shared_role_pattern(shared_variable_roles: dict[str, list[str]]) -> str:
    if not shared_variable_roles:
        return "none"
    return "|".join(
        f"{label}:{'+'.join(roles)}"
        for label, roles in shared_variable_roles.items()
    )


def _counter_to_json(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def _top_groups(
    groups: dict[tuple[str, str], list[dict[str, Any]]], limit: int
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, records in groups.items():
        best = min(
            records,
            key=lambda record: (
                record["best_failed_nearest_delta"],
                record["side_n"],
                record["x"],
                record["y"],
            ),
        )
        rows.append(
            {
                "uv_pair": list(key),
                "d4_points": len(records),
                "raw_count": sum(record["raw_count"] for record in records),
                "best_failed_nearest_delta": best["best_failed_nearest_delta"],
                "best_relation": best["best_relation"],
                "best_missing_edges": best["best_missing_edges"],
                "example": {
                    "x": best["x"],
                    "y": best["y"],
                    "side_n": best["side_n"],
                    "best_sample": best["best_sample"],
                },
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            -row["d4_points"],
            -row["raw_count"],
            row["best_failed_nearest_delta"],
            row["uv_pair"],
        ),
    )[:limit]


def summarize_records(
    records: list[dict[str, Any]],
    *,
    low_delta: int = 10,
    top_groups: int = 20,
    top_records: int = 20,
) -> dict[str, Any]:
    invariants = [invariant_record(record) for record in records]
    relation_counts = Counter(record["best_relation"] for record in invariants)
    missing_counts = Counter(edge for record in invariants for edge in record["best_missing_edges"])
    shared_pattern_counts = Counter(record["shared_role_pattern"] for record in invariants)
    uv_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in invariants:
        uv_groups[tuple(record["uv_pair"])].append(record)

    low_records = [
        record for record in invariants if record["best_failed_nearest_delta"] <= low_delta
    ]
    low_records.sort(
        key=lambda record: (
            record["best_failed_nearest_delta"],
            record["side_n"],
            record["x"],
            record["y"],
        )
    )
    top_invariant_records = sorted(
        invariants,
        key=lambda record: (
            record["best_failed_nearest_delta"],
            -record["raw_count"],
            record["side_n"],
            record["x"],
            record["y"],
        ),
    )[:top_records]

    return {
        "record_count": len(invariants),
        "raw_count_total": sum(record["raw_count"] for record in invariants),
        "uv_pair_group_count": len(uv_groups),
        "relation_counts": _counter_to_json(relation_counts),
        "missing_edge_counts": _counter_to_json(missing_counts),
        "shared_role_pattern_counts": _counter_to_json(shared_pattern_counts),
        "uv_pair_groups_top": _top_groups(uv_groups, top_groups),
        "low_delta_threshold": low_delta,
        "low_delta_records": low_records,
        "top_invariant_records": top_invariant_records,
    }


def load_records(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("d4_point_records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{path} has no d4_point_records")
    return payload, records


def build_summary(
    input_path: Path,
    *,
    low_delta: int = 10,
    top_groups: int = 20,
    top_records: int = 20,
) -> dict[str, Any]:
    payload, records = load_records(input_path)
    summary = summarize_records(
        records,
        low_delta=low_delta,
        top_groups=top_groups,
        top_records=top_records,
    )
    summary["source"] = {
        "path": str(input_path),
        "max_leg": payload.get("max_leg"),
        "diff_tail": payload.get("diff_tail"),
        "near_miss_3of4_total": payload.get("near_miss_3of4_total"),
        "near_miss_3of4_d4_point_total": payload.get("near_miss_3of4_d4_point_total"),
    }
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--low-delta", type=int, default=10)
    parser.add_argument("--top-groups", type=int, default=20)
    parser.add_argument("--top-records", type=int, default=20)
    args = parser.parse_args(argv)

    summary = build_summary(
        args.input,
        low_delta=args.low_delta,
        top_groups=args.top_groups,
        top_records=args.top_records,
    )
    out = args.out or args.input.with_name(args.input.stem + "_d4_invariants.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(f"wrote {out}")
    print(
        "records={records} uv_pair_groups={groups} low_delta_records={low}".format(
            records=summary["record_count"],
            groups=summary["uv_pair_group_count"],
            low=len(summary["low_delta_records"]),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
