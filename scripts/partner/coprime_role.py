#!/usr/bin/env python3
"""Role of COPRIME multi-N pairs in G_M (wl096 follow-up).

Dual of ``island_properties.py``: over the full BFS graph (comp0 giant +
branches + islands), tag every vertex by (layer, coprime?, k via the complete
kernel) and report where coprime pairs live and whether they are 'single
points'. Output: per-layer coprime share, coprime k-distribution per layer,
max coprime k inside comp0, and the isolated-singleton / leaf share.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from math import gcd
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--components", type=Path,
        default=Path("results/partner/partner_full_bfs_components.jsonl"))
    _ = p.add_argument(
        "--layers", type=Path,
        default=Path("results/partner/comp0_island_analysis_1M.jsonl"))
    _ = p.add_argument(
        "--out", type=Path,
        default=Path("results/partner/coprime_role_1M.json"))
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    args = parse_args()
    layer = {}
    with args.layers.open() as f:
        for line in f:
            r = json.loads(line)
            layer[r["component_id"]] = r["layer"]

    comps = [json.loads(line) for line in args.components.open()]
    giant = max(c["size"] for c in comps)

    cnt: dict[str, dict[str, int]] = defaultdict(lambda: {"coprime": 0, "noncoprime": 0})
    cop_k: dict[str, Counter[int]] = defaultdict(Counter)
    noncop_k: dict[str, Counter[int]] = defaultdict(Counter)
    coprime_total = coprime_singleton = coprime_leaf = 0
    max_cop_k_giant = (0, [0, 0])

    for c in comps:
        lay = "giant" if c["size"] == giant else layer.get(c["component_id"], "?")
        for a, b in c["vertices"]:
            if a < 2:
                continue
            g = gcd(a, b)
            k = len(exact_concordant_pair(a, b))
            if g == 1:
                cnt[lay]["coprime"] += 1
                cop_k[lay][k] += 1
                coprime_total += 1
                if c["size"] == 1:
                    coprime_singleton += 1
                if k == 2:
                    coprime_leaf += 1
                if lay == "giant" and k > max_cop_k_giant[0]:
                    max_cop_k_giant = (k, [a, b])
            else:
                cnt[lay]["noncoprime"] += 1
                noncop_k[lay][k] += 1

    out = {
        "per_layer": {
            lay: {**cnt[lay],
                  "coprime_pct": round(
                      cnt[lay]["coprime"]
                      / max(1, cnt[lay]["coprime"] + cnt[lay]["noncoprime"]) * 100, 2)}
            for lay in ("giant", "branch", "island") if cnt[lay]},
        "coprime_total": coprime_total,
        "coprime_isolated_singletons": coprime_singleton,
        "coprime_leaves_k2_degree1": coprime_leaf,
        "coprime_k_hist": {lay: dict(sorted(cop_k[lay].items()))
                           for lay in ("giant", "branch", "island")},
        "max_coprime_k_in_comp0": {"k": max_cop_k_giant[0],
                                   "pair": max_cop_k_giant[1]},
        "noncoprime_k_hist_giant": dict(sorted(noncop_k["giant"].items())),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
