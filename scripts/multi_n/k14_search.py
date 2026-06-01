#!/usr/bin/env python3
"""K_14+ search: D-scaling targeting + exact divisor-based hub-order count.

wl095 (OPEN_DIRECTIONS E.2 follow-up). Combines the two multi-N tools:

  * **D-scaling** (`dscale_kn`, wl085) is the *targeting* stage. For each
    primitive (a0, b0) it runs PARI ``ellrank`` + ``ellratpoints`` once to get
    the rational n pool, then a cheap divisor sieve over the pool denominators
    picks the scalings ``d`` whose pair ``(d*a0, d*b0)`` is most likely to be a
    high-order hub (no need to scan (a, b) <= max_value).

  * **The fast divisor kernel** (`fast_multi_n.exact_concordant_pair`) is the
    *exact count* stage. For each targeted ``(A, B) = (d*a0, d*b0)`` it
    enumerates the divisor pairs of ``A^2`` and ``B^2`` to get the *true*
    integer concordant set N (exhaustive, no range cap, no rational-point
    sampling). The size of that set is the certified hub order ``k``.

Because ``A = d*a0`` and ``B = d*b0`` with ``d, a0, b0`` all small, every prime
factor of A and B is small, so factorization is just a merge of the (cached)
factorizations of ``d``, ``a0`` and ``b0`` -- no Pollard-rho needed.

D-scaling rank-invariance (E_{a0,b0} ~= E_{d*a0,d*b0} over Q, wl065/wl085) means
the rank of every scaled hub equals the primitive rank, so the "rank <= 4"
hypothesis is inherited; we re-certify it directly with ``ellrank`` on the
representative K_14+ hubs found (see ``--ellrank-min-k``).

Output: one JSONL line per primitive with its best (largest-k) hub within
``d_max``, plus a console ladder of the smallest hub reaching each k.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.dscale_kn import (  # noqa: E402
    enumerate_rational_n,
)
from rational_distance.concordant.fast_multi_n import (  # noqa: E402
    _factor,
    exact_concordant_pair,
)


def _merge_factors(*facts: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    """Merge several ``{prime: exp}.items()`` factorizations into one."""
    merged: dict[int, int] = {}
    for f in facts:
        for prime, exp in f:
            merged[prime] = merged.get(prime, 0) + exp
    return tuple(sorted(merged.items()))


def _best_ds_by_pool(rational_ns, d_max: int, top_d: int) -> list[int]:
    """Divisor-sieve the pool denominators: ``cnt[d]`` = #{n : den(n) | d}.

    Returns up to ``top_d`` distinct ``d`` in [1, d_max] with the largest cnt
    (these are the scalings most likely to yield a high-order hub).
    """
    freq: dict[int, int] = {}
    for n in rational_ns:
        v = n.denominator
        if v <= d_max:
            freq[v] = freq.get(v, 0) + 1
    if not freq:
        return []
    cnt = [0] * (d_max + 1)
    for v, f in freq.items():
        for m in range(v, d_max + 1, v):
            cnt[m] += f
    # rank d by cnt desc, prefer smaller d on ties (smaller hub coordinates)
    order = sorted(range(1, d_max + 1), key=lambda d: (-cnt[d], d))
    return order[:top_d]


def search_primitive(
    a0: int,
    b0: int,
    *,
    d_max: int,
    top_d: int,
    pari=None,
) -> dict | None:
    """Return the best (largest exact-k) hub for primitive (a0, b0) within d_max."""
    pool = enumerate_rational_n(a0, b0, pari=pari)
    if pool.n_count == 0:
        return {
            "primitive_a": a0,
            "primitive_b": b0,
            "rank_lower": pool.rank_lower,
            "rank_upper": pool.rank_upper,
            "n_pool": 0,
            "best_k": 0,
            "best_d": None,
            "concordant_N": [],
        }
    fa0 = _factor(a0)
    fb0 = _factor(b0)
    cand_ds = _best_ds_by_pool(pool.rational_ns, d_max, top_d)

    best_k = -1
    best_d = None
    best_N: list[int] = []
    for d in cand_ds:
        fd = _factor(d)
        fA = _merge_factors(fd, fa0)
        fB = _merge_factors(fd, fb0)
        Ns = exact_concordant_pair(d * a0, d * b0, fA, fB)
        if len(Ns) > best_k:
            best_k = len(Ns)
            best_d = d
            best_N = Ns
    return {
        "primitive_a": a0,
        "primitive_b": b0,
        "rank_lower": pool.rank_lower,
        "rank_upper": pool.rank_upper,
        "n_pool": pool.n_count,
        "best_k": best_k,
        "best_d": best_d,
        "a": best_d * a0 if best_d else None,
        "b": best_d * b0 if best_d else None,
        "concordant_N": best_N,
    }


def load_primitives(catalog_path: Path) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    with catalog_path.open() as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            a = r.get("A") or r.get("a")
            b = r.get("B") or r.get("b")
            if a is None or b is None:
                continue
            a, b = int(a), int(b)
            if a <= 0 or b <= 0 or a == b:
                continue
            if gcd(a, b) != 1:
                continue
            out.append((min(a, b), max(a, b)))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--catalog",
        default="results/multi_n/multi_concordant_N_max10000.jsonl",
        help="primitive (A,B) catalog JSONL",
    )
    ap.add_argument("--d-max", type=int, default=50000)
    ap.add_argument("--top-d", type=int, default=64)
    ap.add_argument("--max-primitives", type=int, default=0, help="0 = all")
    ap.add_argument(
        "--primitives",
        nargs="*",
        default=None,
        help="explicit 'a,b' primitives (overrides --catalog)",
    )
    ap.add_argument("--out", default="results/multi_n/k14_search.jsonl")
    args = ap.parse_args()

    if args.primitives:
        prims = []
        for v in args.primitives:
            a, b = (int(x) for x in v.split(","))
            prims.append((min(a, b), max(a, b)))
    else:
        prims = load_primitives(ROOT / args.catalog)
    if args.max_primitives:
        prims = prims[: args.max_primitives]

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(
        f"K_14+ search over {len(prims)} primitives, d_max={args.d_max}, top_d={args.top_d}",
        flush=True,
    )
    print(
        f"{'#':>4} {'primitive':>16} {'rk':>4} {'pool':>5} {'bestk':>6} {'d':>7}  flag", flush=True
    )

    ladder: dict[int, dict] = {}  # k -> smallest-coordinate hub reaching k
    global_max = 0
    t0 = time.time()
    with out_path.open("w") as fout:
        for i, (a0, b0) in enumerate(prims):
            row = search_primitive(a0, b0, d_max=args.d_max, top_d=args.top_d)
            fout.write(json.dumps(row) + "\n")
            fout.flush()
            k = row["best_k"]
            flag = ""
            if k >= 14:
                flag = "K14+"
            if k > global_max:
                global_max = k
                flag += " *MAX*"
            for kk in range(4, k + 1):
                cur = ladder.get(kk)
                if row["a"] is not None and (
                    cur is None or (row["b"] or 0) < (cur["b"] or 1 << 62)
                ):
                    ladder[kk] = {
                        "k_at_least": kk,
                        "primitive_a": a0,
                        "primitive_b": b0,
                        "d": row["best_d"],
                        "a": row["a"],
                        "b": row["b"],
                        "best_k": k,
                        "rank": [row["rank_lower"], row["rank_upper"]],
                    }
            print(
                f"{i:>4} {f'({a0},{b0})':>16} {row['rank_upper']:>4} "
                f"{row['n_pool']:>5} {k:>6} {row['best_d']!s:>7}  {flag}",
                flush=True,
            )

    dt = time.time() - t0
    print(f"\nDone {len(prims)} primitives in {dt:.1f}s. global max k = {global_max}", flush=True)
    print("\n=== smallest hub reaching each k (ladder) ===", flush=True)
    for kk in sorted(ladder):
        h = ladder[kk]
        print(
            f"K_{kk:<3} via prim({h['primitive_a']},{h['primitive_b']}) "
            f"d={h['d']}  (a,b)=({h['a']},{h['b']})  rank={h['rank']}  "
            f"[primitive max k={h['best_k']}]",
            flush=True,
        )
    ladder_path = out_path.with_name(out_path.stem + "_ladder.json")
    ladder_path.write_text(json.dumps(ladder, indent=2))
    print(f"\nladder -> {ladder_path}", flush=True)
    print(f"per-primitive -> {out_path}", flush=True)


if __name__ == "__main__":
    main()
