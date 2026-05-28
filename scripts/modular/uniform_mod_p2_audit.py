#!/usr/bin/env python3
"""Path B / 阶段 3a: 对 wl073 实证数据做 mod p² kill pattern 诊断。

任务: 加载 max_hyp = 1M (or smaller) 的 multi-N pair, 对每个 pair 记录:
  - 它被哪些 M ∈ STANDARD_MODULI kill (chain_closure_mod_sieve on (A, B))
  - 它被哪些 M kill via dual sieve (chain_closure_mod_sieve on (N_i, N_j))

然后统计:
  1. Per-M kill rate: 每个 M_i 单独能 kill 多少 (A, B) classes
  2. Joint coverage: 每个 multi-N pair 至少被一个 M kill 吗?
  3. 最少 M_0: 实证最小的 M_0 子集仍能全 cover

这给路径 B 严格证明的方向:
  - 如果某 M ∈ M_0 是冗余 (其他 M 总能 cover), 则 M_0 可以缩小
  - 如果某些 (A, B) 只被某个特定 M kill, 那个 M 是 "不可或缺"
  - 如果有的 (A, B) 不被任何 M kill on (A, B) but 被 dual sieve kill, 那
    dual sieve 是 essential
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from math import gcd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rational_distance.concordant.chain_closure_sieve import (
    STANDARD_MODULI,
    killed_at_modulus,
)
from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair


def _reduced_pair(p: int, q: int) -> tuple[int, int]:
    """Return ``(p, q)`` divided by their gcd, with the smaller value first."""
    g = gcd(p, q)
    a = p // g
    b = q // g
    return (a, b) if a <= b else (b, a)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Path B audit: per-M kill pattern on multi-N pairs."
    )
    parser.add_argument("--max-hyp", type=int, default=200000)
    parser.add_argument("--moduli", type=str, default="standard",
                        choices=["standard"], help="Currently only standard.")
    parser.add_argument("--jsonl-out", type=Path, default=None)
    args = parser.parse_args()

    moduli: tuple[int, ...] = STANDARD_MODULI
    print(f"Moduli: {moduli}")

    t0 = time.perf_counter()
    pairs = fast_multi_concordant_pairs(args.max_hyp)
    print(
        f"[phase] {len(pairs)} multi-N pairs at max_hyp={args.max_hyp} "
        f"({time.perf_counter() - t0:.2f}s)"
    )

    safe_pass: list[tuple[tuple[int, int], list[int]]] = [
        ((a, b), ns) for (a, b), ns in pairs.items() if allow_reduced_pair(a, b)
    ]
    print(f"  safe-pass: {len(safe_pass)} pairs")

    # Diagnostic counters.
    primary_kill_count: Counter[int] = Counter()  # M -> # pairs killed by M on (A, B)
    dual_kill_count: Counter[int] = Counter()  # M -> # pairs killed by M on some (N_i, N_j)

    # For each pair: which M values kill it?
    primary_records: list[dict] = []
    pairs_unkilled_by_primary: list[tuple[int, int]] = []

    t1 = time.perf_counter()
    for (a, b), ns in safe_pass:
        primary_killers = [m for m in moduli if killed_at_modulus(a, b, m)]
        for m in primary_killers:
            primary_kill_count[m] += 1

        if not primary_killers:
            pairs_unkilled_by_primary.append((a, b))

        # Dual: for each (N_i, N_j) reduced pair, find first killer M
        # (we only record per-pair existence of any dual killer + which M)
        dual_killers_per_pair: set[int] = set()
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                ai, bi = _reduced_pair(ns[i], ns[j])
                for m in moduli:
                    if killed_at_modulus(ai, bi, m):
                        dual_killers_per_pair.add(m)
                        break  # one killer per (N_i, N_j) is enough
        for m in dual_killers_per_pair:
            dual_kill_count[m] += 1

        primary_records.append(
            {
                "A": a,
                "B": b,
                "k": len(ns),
                "primary_killers": primary_killers,
                "dual_killers": sorted(dual_killers_per_pair),
            }
        )

    elapsed = time.perf_counter() - t1
    print(f"[phase] kill audit complete ({elapsed:.2f}s)")
    print()

    # Reports.
    total = len(safe_pass)
    print("=" * 72)
    print(f"Total safe-pass multi-N pairs: {total}")
    print()

    print("Per-M PRIMARY kill rate (chain_closure on (A, B)):")
    for m in moduli:
        pct = 100.0 * primary_kill_count[m] / total if total else 0.0
        print(f"  M={m:>5d}: kills {primary_kill_count[m]:>6d} pairs ({pct:5.2f}%)")

    print()
    print("Per-M DUAL kill rate (chain_closure on some (N_i, N_j)):")
    for m in moduli:
        pct = 100.0 * dual_kill_count[m] / total if total else 0.0
        print(f"  M={m:>5d}: kills {dual_kill_count[m]:>6d} pairs ({pct:5.2f}%)")

    # Pairs with no primary killer
    print()
    print(f"Pairs unkilled by ANY primary M: {len(pairs_unkilled_by_primary)}")
    if pairs_unkilled_by_primary[:5]:
        print("  first 5 examples:")
        for a, b in pairs_unkilled_by_primary[:5]:
            print(f"    ({a}, {b})")

    # How many pairs are killed by ALL primary M (i.e., redundancy)?
    all_killers_count = sum(
        1 for r in primary_records if len(r["primary_killers"]) == len(moduli)
    )
    print()
    print(f"Pairs killed by ALL primary M (heavy redundancy): {all_killers_count}")

    # Distribution of primary killer count per pair
    killer_count_dist: Counter[int] = Counter(
        len(r["primary_killers"]) for r in primary_records
    )
    print()
    print("Distribution of #primary killers per pair:")
    for n in sorted(killer_count_dist):
        pct = 100.0 * killer_count_dist[n] / total if total else 0.0
        print(f"  {n:>2d} killers: {killer_count_dist[n]:>6d} pairs ({pct:5.2f}%)")

    # Greedy minimum M_0 set: starting from the M with highest kill rate,
    # add Ms until all pairs are covered (by primary kill).
    print()
    print("Greedy minimum M_0 (primary kill only):")
    uncovered = set(range(total))
    chosen: list[int] = []
    while uncovered:
        # Find M with most uncovered pairs killed
        best_m = -1
        best_count = -1
        best_set: set[int] = set()
        for m in moduli:
            if m in chosen:
                continue
            killed_set = {
                i for i in uncovered if m in primary_records[i]["primary_killers"]
            }
            if len(killed_set) > best_count:
                best_count = len(killed_set)
                best_m = m
                best_set = killed_set
        if best_count <= 0:
            print(f"  cannot cover remaining {len(uncovered)} pairs with any M")
            break
        chosen.append(best_m)
        uncovered -= best_set
        print(
            f"  + M={best_m:>5d}, kills {best_count:>5d} new ({len(uncovered)} left)"
        )
    if not uncovered:
        print(f"  ⟹ minimum M_0 = {chosen} (size {len(chosen)})")

    if args.jsonl_out is not None:
        args.jsonl_out.parent.mkdir(parents=True, exist_ok=True)
        with args.jsonl_out.open("w") as fh:
            for r in primary_records:
                fh.write(json.dumps(r) + "\n")
        print(f"\nwrote {len(primary_records)} rows to {args.jsonl_out}")


if __name__ == "__main__":
    main()
