#!/usr/bin/env python3
"""Full-plane GEN-CLOSURE delta scan for every G_M partner-graph vertex.

This is the full-plane companion to ``full_gm_delta_stats.py``. The old script
only measured the inside-square relation ``N1 + N2 = A + B``. This script keeps
all four GEN-CLOSURE relations:

    N1 + N2 = A + B
    N1 + N2 = |A - B|
    |N1 - N2| = A + B
    |N1 - N2| = |A - B|

Sum relations allow ``N1 == N2``; difference relations do not. That matches
``rational_distance.concordant.analysis.gen_closure_hit``.
"""

from __future__ import annotations

import argparse
import heapq
import json
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.results.gm_closure_delta import FullPlaneDeltaRow  # noqa: E402


@dataclass(frozen=True)
class ScanResult:
    pair: tuple[int, int]
    k: int
    total_relation_rows: int
    min_abs_delta: int | None
    min_abs_delta_by_relation: dict[str, int]
    closest_rows: list[dict[str, Any]]
    closure_hits: list[dict[str, Any]]


def parse_int(value: object) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        return int(value)
    raise TypeError(f"expected int-like value, got {type(value).__name__}")


def row_to_record(a: int, b: int, k: int, row: FullPlaneDeltaRow) -> dict[str, Any]:
    n1 = row.N1
    n2 = row.N2
    relation = row.relation
    lhs = row.lhs
    rhs = row.rhs
    signed_delta = row.signed_delta
    return {
        "A": a,
        "B": b,
        "A_plus_B": a + b,
        "A_abs_diff": abs(a - b),
        "k": k,
        "relation": relation,
        "N1": n1,
        "N2": n2,
        "value": lhs,
        "target": rhs,
        "delta": signed_delta,
        "abs_delta": abs(signed_delta),
        "equal_N": n1 == n2,
        "equal_N_allowed": relation.startswith("sum="),
    }


def _scan_pair(pair: tuple[int, int]) -> ScanResult:
    from rational_distance.concordant.factor_search import find_concordant_by_factorization
    from rational_distance.results.gm_closure_delta import summarize_full_plane_pair_deltas

    a, b = pair
    ns = sorted(find_concordant_by_factorization(a, b))
    summary = summarize_full_plane_pair_deltas(a, b, ns)
    return ScanResult(
        pair=pair,
        k=summary.k,
        total_relation_rows=summary.total_relation_rows,
        min_abs_delta=summary.min_abs_delta,
        min_abs_delta_by_relation=summary.min_abs_delta_by_relation,
        closest_rows=[row_to_record(a, b, summary.k, row) for row in summary.closest_rows],
        closure_hits=[row_to_record(a, b, summary.k, row) for row in summary.closure_hits],
    )


def load_component_vertices(
    components_path: Path,
    *,
    limit: int | None = None,
) -> tuple[list[tuple[int, int]], dict[tuple[int, int], int]]:
    all_pairs: list[tuple[int, int]] = []
    component_of: dict[tuple[int, int], int] = {}
    with components_path.open(encoding="utf-8") as f:
        for line in f:
            row = cast(dict[str, object], json.loads(line))
            component_id = parse_int(row["component_id"])
            vertices = cast(list[list[object]], row["vertices"])
            for vertex in vertices:
                pair = (parse_int(vertex[0]), parse_int(vertex[1]))
                all_pairs.append(pair)
                component_of[pair] = component_id
                if limit is not None and len(all_pairs) >= limit:
                    return all_pairs, component_of
    return all_pairs, component_of


def main() -> int:
    from rational_distance.parallel import add_parallel_args, get_parallel_config_from_args

    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--components",
        type=Path,
        default=Path("results/partner/partner_full_bfs_components.jsonl"),
    )
    _ = parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("results/partner/full_gm_full_plane_delta_summary.json"),
    )
    _ = parser.add_argument(
        "--top-out",
        type=Path,
        default=Path("results/partner/full_gm_full_plane_delta_top.jsonl"),
    )
    _ = parser.add_argument(
        "--hits-out",
        type=Path,
        default=Path("results/partner/full_gm_full_plane_closure_hits.jsonl"),
    )
    _ = parser.add_argument("--top-n", type=int, default=100)
    _ = parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional smoke-test limit on loaded vertices; default scans all vertices.",
    )
    add_parallel_args(parser)
    args = parser.parse_args()
    cfg = get_parallel_config_from_args(args)

    components_path = cast(Path, args.components)
    summary_out = cast(Path, args.summary_out)
    top_out = cast(Path, args.top_out)
    hits_out = cast(Path, args.hits_out)
    top_n = cast(int, args.top_n)
    limit = cast(int | None, args.limit)

    t0 = time.time()
    all_pairs, component_of = load_component_vertices(components_path, limit=limit)
    print(f"[{time.time() - t0:.1f}s] loaded {len(all_pairs)} vertices", flush=True)
    print(f"  workers={cfg.workers}, chunksize={cfg.chunksize}", flush=True)

    thresholds = [1, 2, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000]
    k_counter: Counter[int] = Counter()
    min_abs_counter: Counter[int] = Counter()
    threshold_counter: Counter[int] = Counter()
    relation_min: dict[str, int] = {}
    hit_count_by_relation: Counter[str] = Counter()
    total_relation_rows = 0
    total_full_plane_hits = 0
    vertices_with_hits = 0
    n_processed = 0
    last_report_t = t0
    top_heap: list[tuple[int, int, dict[str, Any]]] = []
    hit_records: list[dict[str, Any]] = []
    sequence = 0

    def on_result(result: ScanResult) -> None:
        nonlocal total_relation_rows, total_full_plane_hits, vertices_with_hits
        nonlocal n_processed, last_report_t, sequence

        n_processed += 1
        k_counter[result.k] += 1
        total_relation_rows += result.total_relation_rows
        for relation, abs_delta in result.min_abs_delta_by_relation.items():
            old = relation_min.get(relation)
            if old is None or abs_delta < old:
                relation_min[relation] = abs_delta

        if result.min_abs_delta is not None:
            min_abs_counter[result.min_abs_delta] += 1
            for threshold in thresholds:
                if result.min_abs_delta <= threshold:
                    threshold_counter[threshold] += 1

            a, b = result.pair
            entry: dict[str, Any] = {
                "A": a,
                "B": b,
                "A_plus_B": a + b,
                "A_abs_diff": abs(a - b),
                "k": result.k,
                "component_id": component_of[result.pair],
                "total_relation_rows": result.total_relation_rows,
                "min_abs_delta": result.min_abs_delta,
                "min_abs_delta_by_relation": result.min_abs_delta_by_relation,
                "closest_rows": [
                    {**row, "component_id": component_of[result.pair]}
                    for row in result.closest_rows
                ],
            }
            heap_item = (-result.min_abs_delta, sequence, entry)
            sequence += 1
            if len(top_heap) < top_n:
                _ = heapq.heappush(top_heap, heap_item)
            elif result.min_abs_delta < -top_heap[0][0]:
                _ = heapq.heapreplace(top_heap, heap_item)

        if result.closure_hits:
            vertices_with_hits += 1
            total_full_plane_hits += len(result.closure_hits)
            for hit in result.closure_hits:
                relation = str(hit["relation"])
                hit_count_by_relation[relation] += 1
                hit_records.append({**hit, "component_id": component_of[result.pair]})

        if time.time() - last_report_t > 5:
            rate = n_processed / (time.time() - t0)
            eta = (len(all_pairs) - n_processed) / rate if rate > 0 else 0
            min_abs_seen = min(min_abs_counter) if min_abs_counter else "n/a"
            print(
                (
                    f"  [{time.time() - t0:.1f}s] {n_processed}/{len(all_pairs)} "
                    f"({rate:.0f}/s, ETA {eta:.0f}s), "
                    f"min_abs_seen={min_abs_seen}, hits={total_full_plane_hits}"
                ),
                flush=True,
            )
            last_report_t = time.time()

    _ = cfg.map(_scan_pair, all_pairs, on_result=on_result, collect_results=False)

    top_entries = [item[2] for item in sorted(top_heap, key=lambda item: (-item[0], item[1]))]
    summary_out.parent.mkdir(parents=True, exist_ok=True)
    top_out.parent.mkdir(parents=True, exist_ok=True)
    hits_out.parent.mkdir(parents=True, exist_ok=True)

    with top_out.open("w", encoding="utf-8") as f:
        for entry in top_entries:
            _ = f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    with hits_out.open("w", encoding="utf-8") as f:
        for hit in hit_records:
            _ = f.write(json.dumps(hit, ensure_ascii=False) + "\n")

    elapsed_s = round(time.time() - t0, 1)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "components": str(components_path),
        "scope": "all vertices unless --limit is set",
        "limit": limit,
        "closure_predicate": (
            "full-plane GEN-CLOSURE: {N1+N2, |N1-N2|} intersects "
            "{A+B, |A-B|}; sum allows equal N, difference requires distinct N"
        ),
        "concordant_N_enumeration": (
            "exact find_concordant_by_factorization per vertex; no N upper bound"
        ),
        "total_vertices": len(all_pairs),
        "total_candidate_relation_rows": total_relation_rows,
        "total_full_plane_hits": total_full_plane_hits,
        "vertices_with_full_plane_hits": vertices_with_hits,
        "hit_count_by_relation": {
            relation: hit_count_by_relation[relation] for relation in sorted(hit_count_by_relation)
        },
        "k_distribution": {str(k): k_counter[k] for k in sorted(k_counter)},
        "min_abs_delta_global": min(min_abs_counter) if min_abs_counter else None,
        "min_abs_delta_by_relation": {
            relation: relation_min[relation] for relation in sorted(relation_min)
        },
        "vertex_count_by_min_abs_delta_le_100": {
            str(delta): min_abs_counter[delta] for delta in sorted(min_abs_counter) if delta <= 100
        },
        "closest_threshold_counts": {
            str(threshold): threshold_counter[threshold] for threshold in thresholds
        },
        "top_n": top_n,
        "top_out": str(top_out),
        "hits_out": str(hits_out),
        "elapsed_s": elapsed_s,
        "workers": cfg.workers,
        "chunksize": cfg.chunksize,
    }
    with summary_out.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print()
    print(f"Total vertices scanned:     {len(all_pairs)}")
    print(f"Total relation rows:        {total_relation_rows}")
    print(f"Total full-plane hits:      {total_full_plane_hits}")
    print(f"Global min |delta|:         {summary['min_abs_delta_global']}")
    print(f"Summary:                    {summary_out}")
    print(f"Top near-misses:            {top_out}")
    print(f"Closure hits:               {hits_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
