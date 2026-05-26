from __future__ import annotations

import argparse
import heapq
import json
import sys
import time
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import TypedDict, cast

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


class ClosestRowRecord(TypedDict):
    N1: int
    N2: int
    delta: int
    N1_plus_N2: int


class TopEntry(TypedDict):
    A: int
    B: int
    A_plus_B: int
    k: int
    component_id: int
    total_pairs: int
    min_abs_delta: int
    closest_rows: list[ClosestRowRecord]


@dataclass(frozen=True)
class ScanResult:
    pair: tuple[int, int]
    k: int
    total_pairs: int
    min_abs_delta: int | None
    closest_rows: list[tuple[int, int, int]]
    negative_count: int
    positive_count: int
    zero_count: int


def parse_int(value: object) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        return int(value)
    raise TypeError(f"expected int-like value, got {type(value).__name__}")


def _scan_pair(p: tuple[int, int]) -> ScanResult:
    from rational_distance.concordant.factor_search import find_concordant_by_factorization
    from rational_distance.results.gm_closure_delta import summarize_pair_deltas

    a, b = p
    ns = sorted(find_concordant_by_factorization(a, b))
    summary = summarize_pair_deltas(a, b, ns)

    negative_count = 0
    positive_count = 0
    zero_count = 0
    target = a + b
    for n1, n2 in combinations(ns, 2):
        delta = target - (n1 + n2)
        if delta < 0:
            negative_count += 1
        elif delta > 0:
            positive_count += 1
        else:
            zero_count += 1

    return ScanResult(
        pair=p,
        k=summary.k,
        total_pairs=summary.total_pairs,
        min_abs_delta=summary.min_abs_delta,
        closest_rows=[(row.N1, row.N2, row.delta) for row in summary.closest_rows],
        negative_count=negative_count,
        positive_count=positive_count,
        zero_count=zero_count,
    )


def main() -> int:
    from rational_distance.parallel import add_parallel_args, get_parallel_config_from_args

    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--components",
        type=Path,
        default=Path("results/partner_full_bfs_components.jsonl"),
    )
    _ = parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("results/full_gm_delta_summary.json"),
    )
    _ = parser.add_argument(
        "--top-out",
        type=Path,
        default=Path("results/full_gm_delta_top.jsonl"),
    )
    _ = parser.add_argument("--top-n", type=int, default=50)
    add_parallel_args(parser)
    args = parser.parse_args()
    cfg = get_parallel_config_from_args(args)
    components_path = cast(Path, args.components)
    summary_out = cast(Path, args.summary_out)
    top_out = cast(Path, args.top_out)
    top_n = cast(int, args.top_n)

    t0 = time.time()
    all_pairs: list[tuple[int, int]] = []
    component_of: dict[tuple[int, int], int] = {}
    with components_path.open() as f:
        for line in f:
            row = cast(dict[str, object], json.loads(line))
            component_id = parse_int(row["component_id"])
            vertices = cast(list[list[object]], row["vertices"])
            for vertex in vertices:
                pair = (parse_int(vertex[0]), parse_int(vertex[1]))
                all_pairs.append(pair)
                component_of[pair] = component_id

    print(f"[{time.time() - t0:.1f}s] 加载 {len(all_pairs)} 顶点", flush=True)
    print(f"  workers={cfg.workers}, chunksize={cfg.chunksize}", flush=True)

    thresholds = [1, 2, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000]
    k_counter: Counter[int] = Counter()
    min_abs_counter: Counter[int] = Counter()
    threshold_counter: Counter[int] = Counter()
    sign_counter: Counter[str] = Counter()
    total_candidate_pairs = 0
    n_processed = 0
    last_report_t = t0
    top_heap: list[tuple[int, int, TopEntry]] = []
    sequence = 0

    def on_result(result: ScanResult) -> None:
        nonlocal total_candidate_pairs, n_processed, last_report_t, sequence

        n_processed += 1
        k_counter[result.k] += 1
        total_candidate_pairs += result.total_pairs
        sign_counter["negative"] += result.negative_count
        sign_counter["positive"] += result.positive_count
        sign_counter["zero"] += result.zero_count

        if result.min_abs_delta is not None:
            min_abs_counter[result.min_abs_delta] += 1
            for threshold in thresholds:
                if result.min_abs_delta <= threshold:
                    threshold_counter[threshold] += 1

            pair = result.pair
            entry: TopEntry = {
                "A": pair[0],
                "B": pair[1],
                "A_plus_B": pair[0] + pair[1],
                "k": result.k,
                "component_id": component_of[pair],
                "total_pairs": result.total_pairs,
                "min_abs_delta": result.min_abs_delta,
                "closest_rows": [
                    {
                        "N1": n1,
                        "N2": n2,
                        "delta": delta,
                        "N1_plus_N2": n1 + n2,
                    }
                    for n1, n2, delta in result.closest_rows
                ],
            }
            heap_item = (-result.min_abs_delta, sequence, entry)
            sequence += 1
            if len(top_heap) < top_n:
                _ = heapq.heappush(top_heap, heap_item)
            elif result.min_abs_delta < -top_heap[0][0]:
                _ = heapq.heapreplace(top_heap, heap_item)

        if time.time() - last_report_t > 5:
            rate = n_processed / (time.time() - t0)
            eta = (len(all_pairs) - n_processed) / rate if rate > 0 else 0
            min_abs_seen = min(min_abs_counter) if min_abs_counter else "n/a"
            print(
                (
                    f"  [{time.time() - t0:.1f}s] {n_processed}/{len(all_pairs)} "
                    f"({rate:.0f}/s, ETA {eta:.0f}s), min_abs_seen={min_abs_seen}"
                ),
                flush=True,
            )
            last_report_t = time.time()

    _ = cfg.map(_scan_pair, all_pairs, on_result=on_result, collect_results=False)

    top_entries = [item[2] for item in sorted(top_heap, key=lambda item: (-item[0], item[1]))]
    summary_out.parent.mkdir(parents=True, exist_ok=True)
    top_out.parent.mkdir(parents=True, exist_ok=True)

    with top_out.open("w", encoding="utf-8") as f:
        for entry in top_entries:
            _ = f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    summary = {
        "total_vertices": len(all_pairs),
        "total_candidate_pairs": total_candidate_pairs,
        "total_closure_hits": sign_counter["zero"],
        "signed_delta_counts": {
            "negative": sign_counter["negative"],
            "positive": sign_counter["positive"],
            "zero": sign_counter["zero"],
        },
        "k_distribution": {str(k): k_counter[k] for k in sorted(k_counter)},
        "min_abs_delta_global": min(min_abs_counter) if min_abs_counter else None,
        "vertex_count_by_min_abs_delta_le_100": {
            str(delta): min_abs_counter[delta]
            for delta in sorted(min_abs_counter)
            if delta <= 100
        },
        "closest_threshold_counts": {
            str(threshold): threshold_counter[threshold] for threshold in thresholds
        },
        "top_n": top_n,
        "top_out": str(top_out),
        "elapsed_s": round(time.time() - t0, 1),
        "workers": cfg.workers,
    }
    with summary_out.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print()
    print(f"Total vertices scanned: {len(all_pairs)}")
    print(f"Total candidate pairs:  {total_candidate_pairs}")
    print(f"Total closure hits:     {sign_counter['zero']}")
    print(f"Global min |Δ|:         {summary['min_abs_delta_global']}")
    print(f"Summary:                {summary_out}")
    print(f"Top near-misses:        {top_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
