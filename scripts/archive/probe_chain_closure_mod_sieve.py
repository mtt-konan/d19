#!/usr/bin/env python3
"""Probe: 验证 chain closure 在 mod p^k 上的联立筛是否能砍 hard_case。

数学逻辑
========

对 (A, B)，定义：

    T(A, B, M) = { N mod M : N² + A² ≡ □ (mod M)
                              AND  N² + B² ≡ □ (mod M) }

chain closure 要求存在整数 N 使：

    - N² + A² 是平方
    - N² + B² 是平方
    - b = A + B - N 是正整数
    - b² + A² 是平方
    - b² + B² 是平方

把后两个条件 mod M：b mod M ∈ T(A, B, M)，即
(A + B - N) mod M ∈ T。

记 S := T(A, B, M) ⊆ Z/MZ。chain closure 在 mod M 上的必要条件是：

    S ∩ ((A + B) - S) ≠ ∅    (mod M)

如果对某 M 这个交集为空，则该 (A, B) 不存在 chain 解 ⇒ 可标记为
no_solution。

wl037 Layer 1/2 只检查 N ∈ T，没有联立 b = A+B-N ∈ T 这个 chain-closure
端的对称条件。本脚本探测这条筛能不能真的砍掉 hard_case 数。

用法
====

    uv run python scripts/probe_chain_closure_mod_sieve.py \\
        --db results/proof_status.db --limit 50

输出
====

对每个 hard_case 报告：被哪个 M 砍掉（如果有）；总 kill 数；耗时。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.proof_status import schema  # noqa: E402


def squares_mod_M(M: int) -> set[int]:
    """Return the set of residues x mod M with x ≡ □ (mod M)."""
    return {(x * x) % M for x in range(M)}


def allowed_n_mod_M(A: int, B: int, M: int, squares: set[int]) -> set[int]:
    """T(A, B, M) = {N mod M : N²+A² and N²+B² are both squares mod M}."""
    a2 = (A * A) % M
    b2 = (B * B) % M
    out: set[int] = set()
    for n in range(M):
        n2 = (n * n) % M
        if (n2 + a2) % M in squares and (n2 + b2) % M in squares:
            out.add(n)
    return out


def chain_closure_kills(A: int, B: int, M: int) -> tuple[bool, int, int]:
    """Return (killed, |T|, |T ∩ (A+B-T)|) for the given (A, B) at modulus M.

    killed == True iff T ∩ ((A+B) - T) (mod M) is empty.
    """
    squares = squares_mod_M(M)
    T = allowed_n_mod_M(A, B, M, squares)
    if not T:
        # No concordant N mod M at all — already killed before chain closure.
        return True, 0, 0
    ab_mod = (A + B) % M
    reflected = {(ab_mod - n) % M for n in T}
    inter = T & reflected
    return len(inter) == 0, len(T), len(inter)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default="results/proof_status.db")
    ap.add_argument("--limit", type=int, default=None, help="Limit hard_case count")
    ap.add_argument(
        "--moduli",
        nargs="+",
        type=int,
        default=[
            # 小 prime power: 2^k, 3^k, 5^k, 7^k, 11^k
            4, 8, 16, 32, 64,
            9, 27, 81,
            25, 125,
            49, 343,
            121,
            169,
        ],
        help="List of moduli M to probe (each tested independently)",
    )
    ap.add_argument(
        "--combined-moduli",
        nargs="+",
        type=int,
        default=None,
        help="若给定，在最后再用 lcm 联合 mod 测一遍",
    )
    args = ap.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"ERROR: {db_path} not found.")
        return 1

    conn = schema.connect_db(db_path)
    schema.init_schema(conn)
    pairs = list(schema.iter_hard_cases(conn, limit=args.limit))
    print(f"Loaded {len(pairs)} hard_case pairs from {db_path}")
    print(f"Testing moduli: {args.moduli}")
    print()

    # 对每个 M 统计 kill 数
    kill_per_M: dict[int, list[tuple[int, int]]] = {M: [] for M in args.moduli}
    # 每对在某 M 上被 kill：(A, B, M_killer)
    killed_by_any: dict[tuple[int, int], list[int]] = {}

    t_start = time.perf_counter()
    for pair in pairs:
        A = int(pair["A"])
        B = int(pair["B"])
        killers: list[int] = []
        for M in args.moduli:
            killed, _T_size, _inter_size = chain_closure_kills(A, B, M)
            if killed:
                kill_per_M[M].append((A, B))
                killers.append(M)
        if killers:
            killed_by_any[(A, B)] = killers

    elapsed = time.perf_counter() - t_start

    print(f"=== Per-modulus kill counts ===")
    print(f"{'M':>6} {'kills':>8} {'pct':>7}")
    for M in args.moduli:
        kills = len(kill_per_M[M])
        pct = 100.0 * kills / len(pairs) if pairs else 0.0
        print(f"{M:>6} {kills:>8} {pct:>6.2f}%")

    n_any = len(killed_by_any)
    print()
    print(f"=== Union over all moduli ===")
    print(f"hard_case killed by at least one M: {n_any} / {len(pairs)} "
          f"({100.0 * n_any / len(pairs) if pairs else 0:.2f}%)")
    print(f"Time elapsed: {elapsed:.2f}s")

    if killed_by_any:
        print()
        print(f"=== First 10 killed hard_cases ===")
        for i, ((A, B), Ms) in enumerate(list(killed_by_any.items())[:10]):
            print(f"  ({A:>6}, {B:>6})  killed by M in {Ms}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
