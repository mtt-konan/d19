#!/usr/bin/env python3
"""给定一个 partner pair (P_a, P_b)，找它是从 catalog 哪些行抛出来的。

按 partner 恒等式：partner (P_a, P_b) 由 catalog 行 (A, B) 抛出
  ⇔  catalog 行 (A, B) 的 concordant_N 列表同时包含 P_a 和 P_b。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    _ = ap.add_argument("partner_a", type=int)
    _ = ap.add_argument("partner_b", type=int)
    _ = ap.add_argument(
        "--catalog",
        type=Path,
        default=Path("results/multi_concordant_N_max100000_fast.jsonl"),
    )
    args = ap.parse_args()

    pa, pb = sorted((args.partner_a, args.partner_b))
    sources = []
    with args.catalog.open() as f:
        for line in f:
            r = json.loads(line)
            ns = set(int(n) for n in r["concordant_N"])
            if pa in ns and pb in ns:
                sources.append(r)

    print(f"Partner ({pa}, {pb}) 由 {len(sources)} 条 catalog 行抛出:")
    for r in sources:
        print(f"  ({int(r['A']):>5}, {int(r['B']):>5})  k={int(r['n_concordant'])}  N={r['concordant_N']}")

    if sources:
        # 这些 source row 涉及到的不同 a/b 节点 = 共享 partner 的"K_n 候选节点集"（来自 catalog 视角）
        node_set: set[int] = set()
        for r in sources:
            node_set.add(int(r["A"]))
            node_set.add(int(r["B"]))
        print()
        print(f"涉及节点集（K_n 候选, 来自 catalog 入边）: {sorted(node_set)}  共 {len(node_set)} 个")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
