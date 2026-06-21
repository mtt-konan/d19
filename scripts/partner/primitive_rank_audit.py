#!/usr/bin/env python3
"""Run ellrank on primitive hotspots from primitive_projection.py output."""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

Pair = tuple[int, int]
SelectedPrimitive = tuple[Pair, str, int]


def _primitive_from_row(row: dict[str, Any]) -> Pair:
    primitive = row["primitive"]
    return int(primitive[0]), int(primitive[1])


def select_primitives(summary: dict[str, Any], *, limit: int) -> list[SelectedPrimitive]:
    """Select primitive hotspots, preserving global/layer order and deduping."""
    selected: list[SelectedPrimitive] = []
    seen: set[Pair] = set()

    def add_rows(rows: list[dict[str, Any]], source: str) -> None:
        for row in rows:
            pair = _primitive_from_row(row)
            if pair in seen:
                continue
            seen.add(pair)
            selected.append((pair, source, int(row["incident_edges"])))

    add_rows(list(summary.get("top_primitives", [])), "global")
    for layer in ("giant", "branch", "island"):
        layer_rows = (
            summary.get("by_layer", {})
            .get(layer, {})
            .get("top_primitives", [])
        )
        add_rows(list(layer_rows), layer)

    return selected[:limit]


def audit_primitives(
    selected: list[SelectedPrimitive],
    *,
    effort: int = 1,
    include_pool: bool = False,
    max_depth: int = 50,
    ratpoints_bound: int = 200_000,
    rank_combo_bound: int = 5,
) -> list[dict[str, Any]]:
    from rational_distance.concordant.analysis import compute_rank
    from rational_distance.concordant.dscale_kn import enumerate_rational_n

    rows: list[dict[str, Any]] = []
    for (a, b), source, incident_edges in selected:
        t0 = time.time()
        _rank, (lo, hi), sha2, gens = compute_rank(a, b, effort=effort)
        row = {
            "primitive_a": a,
            "primitive_b": b,
            "source": source,
            "incident_edges": incident_edges,
            "rank_lower": lo,
            "rank_upper": hi,
            "rank_certified": lo == hi,
            "sha2_lower": sha2,
            "n_gens": len(gens),
        }
        if include_pool:
            pool = enumerate_rational_n(
                a,
                b,
                max_depth=max_depth,
                ratpoints_bound=ratpoints_bound,
                rank_combo_bound=rank_combo_bound,
            )
            row.update(
                {
                    "rational_n_pool_size": pool.n_count,
                    "denominator_count": len(pool.denominators),
                    "denominators": pool.denominators,
                }
            )
        row["elapsed_s"] = round(time.time() - t0, 3)
        rows.append(row)
    return rows


def summarize_rank_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    rank_hist = Counter(int(row["rank_lower"]) for row in rows)
    by_source: dict[str, Counter[int]] = {}
    for row in rows:
        by_source.setdefault(str(row["source"]), Counter())[int(row["rank_lower"])] += 1
    summary = {
        "total": len(rows),
        "certified": sum(1 for row in rows if row["rank_certified"]),
        "rank_hist": {str(k): v for k, v in sorted(rank_hist.items())},
        "rank_gt_4": sum(1 for row in rows if int(row["rank_lower"]) > 4),
        "by_source_rank_hist": {
            source: {str(k): v for k, v in sorted(counter.items())}
            for source, counter in sorted(by_source.items())
        },
    }
    pool_sizes = [
        int(row["rational_n_pool_size"])
        for row in rows
        if "rational_n_pool_size" in row
    ]
    if pool_sizes:
        summary.update(
            {
                "pool_size_min": min(pool_sizes),
                "pool_size_max": max(pool_sizes),
                "pool_size_avg": round(sum(pool_sizes) / len(pool_sizes), 2),
            }
        )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--projection-summary",
        type=Path,
        default=Path("results/partner/primitive_projection_1M_summary.json"),
    )
    _ = parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/partner/primitive_rank_audit_top.jsonl"),
    )
    _ = parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("results/partner/primitive_rank_audit_top_summary.json"),
    )
    _ = parser.add_argument("--limit", type=int, default=40)
    _ = parser.add_argument("--effort", type=int, default=1)
    _ = parser.add_argument("--include-pool", action="store_true")
    _ = parser.add_argument("--max-depth", type=int, default=50)
    _ = parser.add_argument("--ratpoints-bound", type=int, default=200_000)
    _ = parser.add_argument("--rank-combo-bound", type=int, default=5)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = json.loads(args.projection_summary.read_text())
    selected = select_primitives(summary, limit=int(args.limit))
    rows = audit_primitives(
        selected,
        effort=int(args.effort),
        include_pool=bool(args.include_pool),
        max_depth=int(args.max_depth),
        ratpoints_bound=int(args.ratpoints_bound),
        rank_combo_bound=int(args.rank_combo_bound),
    )
    rank_summary = summarize_rank_rows(rows)
    rank_summary["projection_summary"] = str(args.projection_summary)
    rank_summary["limit"] = args.limit
    rank_summary["effort"] = args.effort
    rank_summary["include_pool"] = args.include_pool

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        for row in rows:
            _ = f.write(json.dumps(row, ensure_ascii=False) + "\n")
    args.summary_out.write_text(json.dumps(rank_summary, indent=2, ensure_ascii=False))

    print(json.dumps(rank_summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
