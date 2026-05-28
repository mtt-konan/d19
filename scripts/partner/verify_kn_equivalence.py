#!/usr/bin/env python3
"""验证 "K_n (共享 partner) ≡ partner pair 自身是 k>=n multi-N pair"。

读取 results/partner_kn_subgraphs.jsonl 里所有 shared_partner K_n，
对每个 partner pair (P_a, P_b) 跑权威 factor_search，对比：
  - n nodes（K_n 节点集）⊆ factor_search(P_a, P_b) 的 N 列表？
  - factor_search 的 N 列表是否就等于 n nodes，或者还包含额外的 N？

如果完全等价，那 "K_n 枚举" 可以被简化为 "找所有 multi-N pair 按 k 降序排"。
"""

from __future__ import annotations

import json
import sys
from math import gcd
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    rows = []
    with (ROOT / "results/partner_kn_subgraphs.jsonl").open() as f:
        for line in f:
            r = json.loads(line)
            if r["kind"] == "shared_partner":
                rows.append(r)

    print(f"shared_partner K_n 总数: {len(rows)}")
    print()

    matches = 0
    superset_only = 0  # n nodes ⊊ N，partner 自己 k 比 n 还大
    mismatches = 0

    for r in rows:
        n = r["n"]
        nodes = list(r["nodes"])
        p_a, p_b = r["shared_partner"]
        ns = find_concordant_by_factorization(p_a, p_b)
        contains_all = all(x in ns for x in nodes)
        extra = sorted(set(ns) - set(nodes))
        g = gcd(p_a, p_b)
        partner_k = len(ns)

        tag = ""
        if contains_all and partner_k == n:
            tag = "EQUAL"
            matches += 1
        elif contains_all and partner_k > n:
            tag = f"SUPERSET (+{partner_k - n})"
            superset_only += 1
        else:
            tag = "MISMATCH"
            mismatches += 1

        print(f"  K_{n} nodes = {nodes}")
        print(f"      partner ({p_a}, {p_b})  gcd={g}  factor_search k={partner_k}")
        print(f"      partner N = {ns}")
        if extra:
            print(f"      extra (in N but not in K_n): {extra}")
        print(f"      → {tag}")
        print()

    print(f"统计:")
    print(f"  EQUAL    (partner N 恰好 = K_n nodes):  {matches}")
    print(f"  SUPERSET (partner N ⊋ K_n nodes):       {superset_only}")
    print(f"  MISMATCH (partner N 不含全部 K_n):       {mismatches}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
