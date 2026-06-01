#!/usr/bin/env python3
"""Verify the truncation hypothesis by comparing two BFS windows (wl096).

Takes a SMALL-window components dump and a LARGE-window dump (both from
``partner_full_bfs.py``). For every non-giant component of the small window,
classify it as ``branch`` (truncated) or ``island`` (untruncated) with the
exact kernel, then check how its vertices landed in the LARGE-window giant:

  * branches are predicted to be absorbed into the large giant (preferentially
    the higher-k ones, whose bridge coordinates are nearer the window);
  * islands are predicted to remain completely separate (0 vertices leak).

Reports a per-max_k merge table and an explicit check of the largest branches.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument("--small", type=Path,
                       default=Path("results/partner/partner_full_bfs_components.jsonl"))
    _ = p.add_argument("--small-window", type=int, default=1_000_000)
    _ = p.add_argument("--large", type=Path,
                       default=Path("results/partner/partner_full_bfs_7M_components.jsonl"))
    _ = p.add_argument("--out", type=Path,
                       default=Path("results/partner/window_merge_1M_7M.json"))
    return p.parse_args()


def load_giant(path: Path) -> set[tuple[int, int]]:
    giant: set[tuple[int, int]] = set()
    best = -1
    with path.open() as f:
        for line in f:
            c = json.loads(line)
            if c["size"] > best:
                best = c["size"]
                giant = {(a, b) for a, b in c["vertices"]}
    return giant


def main() -> int:
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    args = parse_args()
    w = int(args.small_window)
    large_giant = load_giant(Path(args.large))
    large_giant_size = len(large_giant)

    small_comps = []
    with Path(args.small).open() as f:
        for line in f:
            small_comps.append(json.loads(line))
    small_giant_size = max(c["size"] for c in small_comps)

    # (layer, max_k) -> [n_comps, n_fully_merged, n_verts, n_verts_in_giant]
    agg: dict[tuple[str, int], list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    big_rows = []
    for c in small_comps:
        if c["size"] == small_giant_size:
            continue
        verts = [(a, b) for a, b in c["vertices"]]
        max_k = 0
        truncated = False
        for a, b in verts:
            if a < 2:
                continue
            ns = exact_concordant_pair(a, b)
            max_k = max(max_k, len(ns))
            if not truncated and any(max(ni, nj) > w for ni, nj in combinations(ns, 2)):
                truncated = True
        in_giant = sum(1 for v in verts if v in large_giant)
        fully = in_giant == len(verts)
        layer = "branch" if truncated else "island"
        a = agg[(layer, max_k)]
        a[0] += 1
        a[1] += 1 if fully else 0
        a[2] += len(verts)
        a[3] += in_giant
        if c["size"] >= 90:
            big_rows.append({"id": c["component_id"], "size": c["size"],
                             "max_k": max_k, "layer": layer,
                             "in_large_giant": in_giant, "fully_merged": fully})

    out = {
        "small_window": w,
        "small_giant_size": small_giant_size,
        "large_giant_size": large_giant_size,
        "by_layer_max_k": {
            f"{lay}/K_{k}": {"components": n, "fully_merged": fm,
                             "vertices": nv, "vertices_in_large_giant": ig}
            for (lay, k), (n, fm, nv, ig) in sorted(agg.items())
        },
        "large_components": sorted(big_rows, key=lambda r: -r["size"]),
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.out).open("w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"small giant={small_giant_size}  large giant={large_giant_size}")
    print("\nlayer/max_k : components / fully_merged_into_large_giant / verts_in_giant")
    for (lay, k), (n, fm, nv, ig) in sorted(agg.items()):
        print(f"  {lay:>7}/K_{k:<3} {n:>5} / {fm:>5} / {ig:>6}of{nv}")
    print("\nlargest small non-giant comps (size>=90):")
    for r in sorted(big_rows, key=lambda r: -r["size"]):
        tag = "ALL" if r["fully_merged"] else f"{r['in_large_giant']}/{r['size']}"
        print(f"  id={r['id']:>4} size={r['size']:>4} K_{r['max_k']:<3} "
              f"{r['layer']:>7} -> giant {tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
