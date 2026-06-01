#!/usr/bin/env python3
"""Empirical test of the law: COPRIME multi-N pair (A,B) => every concordant N ≡ 0 (mod 12).

Equivalently: no coprime pair ever has a coprime concordant N-pair (every
gcd(N_i,N_j) is a multiple of 12). This is the modular skeleton behind the
closure obstruction (closure needs 12 | (A+B) or 12 | |A-B|), and the empirical
counterpart of A.9 §8.6 (the dangerous high-k structure lives on NON-coprime
legs, where gcd-scaling breaks this law).

Two input modes:
  --scan  FILE   jsonl rows with {"A","B","concordant_N":[...]} (fast scanner dump)
  --bfs   FILE   partner BFS components jsonl ({"vertices":[[a,b],...]}); concordant
                 sets are recomputed with the range-free divisor kernel.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations
from math import gcd
from pathlib import Path


def iter_scan(path: Path):
    for line in path.open():
        r = json.loads(line)
        a, b = r["A"], r["B"]
        if gcd(a, b) == 1:
            yield a, b, r["concordant_N"]


def iter_bfs(path: Path):
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    seen: set[tuple[int, int]] = set()
    for line in path.open():
        for a, b in json.loads(line)["vertices"]:
            if gcd(a, b) == 1 and (a, b) not in seen:
                seen.add((a, b))
                yield a, b, exact_concordant_pair(a, b)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    _ = g.add_argument("--scan", type=Path)
    _ = g.add_argument("--bfs", type=Path)
    _ = p.add_argument("--modulus", type=int, default=12)
    args = p.parse_args()

    src = iter_scan(args.scan) if args.scan else iter_bfs(args.bfs)
    m = args.modulus
    pairs = totN = 0
    maxc = 0
    viol: list[tuple[int, int, int]] = []
    coprime_npair: list[tuple[int, int, int, int]] = []
    gcdN: Counter[int] = Counter()

    for a, b, ns in src:
        pairs += 1
        totN += len(ns)
        maxc = max(maxc, a, b)
        for n in ns:
            if n % m != 0:
                viol.append((a, b, n))
        for ni, nj in combinations(ns, 2):
            d = gcd(ni, nj)
            gcdN[d] += 1
            if d == 1:
                coprime_npair.append((a, b, ni, nj))

    out = {
        "coprime_pairs_checked": pairs,
        "max_coordinate": maxc,
        "total_concordant_N": totN,
        "modulus": m,
        f"N_not_divisible_by_{m}": len(viol),
        "violation_examples": viol[:10],
        "coprime_concordant_N_pairs": len(coprime_npair),
        "coprime_N_pair_examples": coprime_npair[:10],
        "gcd_Ni_Nj_top": dict(gcdN.most_common(12)),
        "law_holds": len(viol) == 0,
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
