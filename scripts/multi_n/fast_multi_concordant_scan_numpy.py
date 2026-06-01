#!/usr/bin/env python3
"""Numpy sort-and-group pivot-on-N multi-concordant-N scan (scales to max_hyp=5e6+).

`fast_multi_concordant_pairs` stores relations in Python dicts; at max_hyp=2e6
that is ~5.3 GiB to hold what is fundamentally ~0.6 GB of raw (n, a) data, and
the box OOMs at 2e6. This variant stores the (n, a) relation stream in **numpy
arrays** (int64 n + int32 a) and replaces both dicts with two sorts:

  1. sort relations by N, walk equal-N runs (= concordant buckets), emit every
     coprime not-both-even A-pair (ai, aj) together with that N;
  2. encode each pair as key = ai*(max_hyp+1) + aj, sort, and count run lengths:
     a key occurring k>=2 times is a pair sharing k distinct concordant N.

Each (ai, aj) is emitted at most once per N (a bucket lists each A once), so a
key-run has length exactly k = number of shared N and all its N are distinct.

Peak RAM at 5e6 is ~4 GiB (vs ~13 GiB for the dict build) — fits an 8 GiB box.
Output aggregates match `fast_multi_concordant_scan.py` exactly.
"""

from __future__ import annotations

import argparse
import sys
import time
from collections import defaultdict
from math import gcd
from pathlib import Path
from typing import cast

import numpy as np

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

_CHUNK = 1 << 22  # 4.19M relations per numpy chunk


def _collect_relations(max_hyp: int) -> tuple[np.ndarray, np.ndarray]:
    """Stream iter_concordant_a_n into chunked numpy arrays; return (n[], a[])."""
    from rational_distance.concordant.fast_multi_n import iter_concordant_a_n

    n_chunks: list[np.ndarray] = []
    a_chunks: list[np.ndarray] = []
    buf_n = np.empty(_CHUNK, dtype=np.int64)
    buf_a = np.empty(_CHUNK, dtype=np.int32)
    i = 0
    for a, n in iter_concordant_a_n(max_hyp):
        buf_n[i] = n
        buf_a[i] = a
        i += 1
        if i == _CHUNK:
            n_chunks.append(buf_n)
            a_chunks.append(buf_a)
            buf_n = np.empty(_CHUNK, dtype=np.int64)
            buf_a = np.empty(_CHUNK, dtype=np.int32)
            i = 0
    n_chunks.append(buf_n[:i].copy())
    a_chunks.append(buf_a[:i].copy())
    del buf_n, buf_a
    n_arr = np.concatenate(n_chunks)
    a_arr = np.concatenate(a_chunks)
    return n_arr, a_arr


def scan_numpy(max_hyp: int) -> dict[tuple[int, int], list[int]]:
    n_arr, a_arr = _collect_relations(max_hyp)

    # sort relations by N so equal-N rows are contiguous (= concordant buckets)
    order = np.argsort(n_arr, kind="stable")
    n_arr = n_arr[order]
    a_arr = a_arr[order]
    del order

    # bucket boundaries: positions where N changes
    change = np.flatnonzero(np.diff(n_arr)) + 1
    starts = np.concatenate(([0], change))
    ends = np.concatenate((change, [n_arr.shape[0]]))
    # keep only buckets with >= 2 entries (singletons cannot form a pair)
    multi = np.flatnonzero((ends - starts) >= 2)
    ms = starts[multi].tolist()
    me = ends[multi].tolist()
    del change, starts, ends, multi

    # stage 2: emit coprime not-both-even pairs per bucket into a growable
    # numpy buffer (avoid millions of tiny arrays / giant python lists).
    factor = max_hyp + 1
    cap = 1 << 22
    keys = np.empty(cap, dtype=np.int64)
    nns = np.empty(cap, dtype=np.int64)
    cnt = 0
    for s, e in zip(ms, me, strict=True):
        bucket = sorted(int(x) for x in a_arr[s:e])
        nval = int(n_arr[s])
        m = len(bucket)
        for i in range(m):
            ai = bucket[i]
            ai_odd = ai & 1
            for j in range(i + 1, m):
                aj = bucket[j]
                if not ai_odd and not (aj & 1):
                    continue
                if gcd(ai, aj) != 1:
                    continue
                if cnt == cap:
                    cap <<= 1
                    keys.resize(cap, refcheck=False)
                    nns.resize(cap, refcheck=False)
                keys[cnt] = ai * factor + aj
                nns[cnt] = nval
                cnt += 1
    del a_arr, n_arr, ms, me

    if cnt == 0:
        return {}
    keys = keys[:cnt]
    nns = nns[:cnt]

    # sort by pair key; equal-key runs share that pair across distinct N
    korder = np.argsort(keys, kind="stable")
    keys = keys[korder]
    nns = nns[korder]
    del korder

    uniq, first_idx, counts = np.unique(keys, return_index=True, return_counts=True)
    multi_mask = counts >= 2
    result: dict[tuple[int, int], list[int]] = {}
    for key, idx, cnt in zip(
        uniq[multi_mask].tolist(),
        first_idx[multi_mask].tolist(),
        counts[multi_mask].tolist(),
        strict=True,
    ):
        a = key // factor
        b = key % factor
        ns = sorted(nns[idx : idx + cnt].tolist())
        result[(a, b)] = ns
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Numpy sort-and-group pivot-on-N scan")
    _ = parser.add_argument("--max-hyp", type=int, default=5000000)
    _ = parser.add_argument("--out", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    max_hyp = cast(int, args.max_hyp)

    t0 = time.perf_counter()
    pairs = scan_numpy(max_hyp)
    elapsed = time.perf_counter() - t0

    k_hist: dict[int, int] = defaultdict(int)
    n_closure = 0
    closure_examples: list[tuple[int, int, list[int]]] = []
    for (a, b), ns in pairs.items():
        k_hist[len(ns)] += 1
        target = a + b
        ns_set = set(ns)
        if any((target - x) != x and (target - x) in ns_set and target - x > 0 for x in ns):
            n_closure += 1
            if len(closure_examples) < 10:
                closure_examples.append((a, b, ns))

    print(f"max_hyp={max_hyp}")
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
