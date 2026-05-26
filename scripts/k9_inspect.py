#!/usr/bin/env python3
"""检查 wl062 发现的 4 个 K_9 实例：N 列表、gcd、F2-rank。"""

from __future__ import annotations

import sys
from math import gcd
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    k9 = [
        (61200, 222768),
        (76440, 831600),
        (184800, 308880),
        (69615, 221760),
    ]
    print(f"{'pair':<24}{'gcd':<8}{'k':<4}{'N (前 6 个)':<60}{'A+B':<14}")
    print("-" * 110)

    for a, b in k9:
        ns = find_concordant_by_factorization(a, b)
        g = gcd(a, b)
        ns_preview = ", ".join(str(n) for n in ns[:6])
        if len(ns) > 6:
            ns_preview += f", +{len(ns)-6} more"
        print(f"({a:>7}, {b:>7})  {g:<8}{len(ns):<4}{ns_preview:<60}{a+b:<14}")
        # closure 检查
        target = a + b
        closure = []
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                if ns[i] + ns[j] == target:
                    closure.append((ns[i], ns[j]))
        if closure:
            print(f"     CLOSURE FOUND: {closure}")

    # 也跟 K_8 比较一下
    print()
    print("对比 K_8 (wl055):")
    k8 = [(55440, 445536), (58800, 98280)]
    for a, b in k8:
        ns = find_concordant_by_factorization(a, b)
        g = gcd(a, b)
        ns_preview = ", ".join(str(n) for n in ns[:6])
        if len(ns) > 6:
            ns_preview += f", +{len(ns)-6} more"
        print(f"({a:>7}, {b:>7})  {g:<8}{len(ns):<4}{ns_preview:<60}{a+b:<14}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
