#!/usr/bin/env python3
"""Memory-bounded pivot-on-N multi-concordant-N scan (one-off, for max_hyp=2e6+).

`fast_multi_concordant_pairs` holds two big dicts simultaneously
(`a_sets` = every N->A relation, and `pairs_with_n` = every coprime
co-occurring A-pair). At max_hyp=2e6 the combined peak exceeds an 8 GiB box
and the process is OOM-killed.

This variant keeps the result identical but bounds peak RAM:
  1. build a_sets, then DROP singleton buckets (frees the bulk of stage-1 memory);
  2. generate pairs in K disjoint shards by `ai % K`, so the pair dict only
     ever holds ~1/K of the co-occurring pairs at once. Each pair has a fixed
     smaller element ai, so shards partition the pairs exactly — no double count.

Output identical schema/aggregates to `fast_multi_concordant_scan.py`.
"""

from __future__ import annotations

import argparse
import sys
import time
from collections import defaultdict
from math import gcd
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def scan_lowmem(max_hyp: int, shards: int) -> dict[tuple[int, int], list[int]]:
    from rational_distance.concordant.fast_multi_n import iter_concordant_a_n

    # stage 1: N -> list of A
    a_sets: dict[int, list[int]] = defaultdict(list)
    for a, n in iter_concordant_a_n(max_hyp):
        a_sets[n].append(a)

    # drop singleton buckets (cannot form a pair) and sort survivors
    buckets: list[tuple[int, list[int]]] = []
    for n, a_set in a_sets.items():
        if len(a_set) >= 2:
            a_set.sort()
            buckets.append((n, a_set))
    a_sets.clear()

    result: dict[tuple[int, int], list[int]] = {}
    # stage 2: sharded pair generation by ai % shards
    for shard in range(shards):
        pairs_with_n: dict[tuple[int, int], list[int]] = defaultdict(list)
        for n, a_set in buckets:
            m = len(a_set)
            for i in range(m):
                ai = a_set[i]
                if ai % shards != shard:
                    continue
                ai_is_odd = ai & 1
                for j in range(i + 1, m):
                    aj = a_set[j]
                    if not ai_is_odd and not (aj & 1):
                        continue
                    if gcd(ai, aj) != 1:
                        continue
                    pairs_with_n[(ai, aj)].append(n)
        for key, ns in pairs_with_n.items():
            if len(ns) >= 2:
                result[key] = sorted(ns)
        pairs_with_n.clear()
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Low-memory pivot-on-N scan")
    _ = parser.add_argument("--max-hyp", type=int, default=2000000)
    _ = parser.add_argument("--shards", type=int, default=8)
    _ = parser.add_argument("--out", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    max_hyp = cast(int, args.max_hyp)
    shards = cast(int, args.shards)

    t0 = time.perf_counter()
    pairs = scan_lowmem(max_hyp, shards)
    elapsed = time.perf_counter() - t0

    k_hist: dict[int, int] = defaultdict(int)
    n_closure = 0
    closure_examples: list[tuple[int, int, list[list[int]]]] = []
    for (a, b), ns in pairs.items():
        k_hist[len(ns)] += 1
        target = a + b
        ns_set = set(ns)
        cps = [[n1, target - n1] for n1 in ns
               if (target - n1) != n1 and (target - n1) in ns_set and target - n1 > 0]
        if cps:
            n_closure += 1
            if len(closure_examples) < 10:
                closure_examples.append((a, b, cps))

    print(f"max_hyp={max_hyp}  shards={shards}")
    print(f"multi-N pairs: {len(pairs)}")
    print(f"k histogram: {dict(sorted(k_hist.items()))}")
    print(f"closure pairs (N1+N2=A+B): {n_closure}")
    if closure_examples:
        print(f"closure examples: {closure_examples}")
    print(f"elapsed: {elapsed:.2f}s")

    out_path = cast("Path | None", args.out)
    if out_path is not None:
        import json
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as fh:
            for (a, b), ns in sorted(pairs.items()):
                _ = fh.write(json.dumps({"A": a, "B": b, "n_concordant": len(ns),
                                         "concordant_N": ns, "A_plus_B": a + b}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
