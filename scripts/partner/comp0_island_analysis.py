#!/usr/bin/env python3
"""Decompose a partner-graph BFS dump into three structural layers (wl096).

Given a ``*_components.jsonl`` produced by ``partner_full_bfs.py`` at some
window ``W = max_value``, classify every NON-giant component using the exact,
range-free divisor kernel (``exact_concordant_pair`` from wl095):

  * **giant**      — the single largest component (comp0).
  * **branch**     — *truncated*: some vertex has a concordant partner pair
                     with a coordinate > W, i.e. the component continues past
                     the window and is a severed branch of the giant-to-be.
  * **island**     — *untruncated*: every partner pair of every vertex stays
                     <= W, so the component is closed under the partner
                     relation and is a genuine, permanently-separate component
                     of the infinite graph G_M.

For each component we also record ``max_k`` (largest concordant count among
its vertices) and check the Harborth closure condition ``N_i + N_j == A + B``
on every partner edge (a hit would be a counterexample).

Outputs a per-component JSONL and a summary JSON.
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
    _ = p.add_argument(
        "--components",
        type=Path,
        default=Path("results/partner/partner_full_bfs_components.jsonl"),
    )
    _ = p.add_argument("--window", type=int, default=1_000_000,
                       help="max_value used to build the dump")
    _ = p.add_argument(
        "--out-prefix",
        type=Path,
        default=Path("results/partner/comp0_island_analysis"),
    )
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    args = parse_args()
    window = int(args.window)

    comps = []
    with Path(args.components).open() as f:
        for line in f:
            c = json.loads(line)
            comps.append(c)
    giant_size = max(c["size"] for c in comps)

    rows = []
    # (layer, max_k) -> [n_comps, n_vertices]
    agg: dict[tuple[str, int], list[int]] = defaultdict(lambda: [0, 0])
    closure_hits_total = 0

    for c in comps:
        if c["size"] == giant_size:
            rows.append({
                "component_id": c["component_id"], "size": c["size"],
                "layer": "giant", "max_k": None, "truncated": None,
                "closure_hits": None,
            })
            continue
        verts = [(a, b) for a, b in c["vertices"]]
        max_k = 0
        truncated = False
        closure_hits = 0
        for a, b in verts:
            if a < 2:
                continue
            ns = exact_concordant_pair(a, b)
            if len(ns) > max_k:
                max_k = len(ns)
            for ni, nj in combinations(ns, 2):
                if max(ni, nj) > window:
                    truncated = True
                if ni + nj == a + b:
                    closure_hits += 1
        closure_hits_total += closure_hits
        layer = "branch" if truncated else "island"
        agg[(layer, max_k)][0] += 1
        agg[(layer, max_k)][1] += c["size"]
        rows.append({
            "component_id": c["component_id"], "size": c["size"],
            "layer": layer, "max_k": max_k, "truncated": truncated,
            "closure_hits": closure_hits,
        })

    out_prefix = Path(args.out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    with (out_prefix.parent / f"{out_prefix.name}.jsonl").open("w") as f:
        for r in rows:
            _ = f.write(json.dumps(r, ensure_ascii=False) + "\n")

    branch_comps = sum(n for (lay, _), (n, _) in agg.items() if lay == "branch")
    branch_verts = sum(v for (lay, _), (_, v) in agg.items() if lay == "branch")
    island_comps = sum(n for (lay, _), (n, _) in agg.items() if lay == "island")
    island_verts = sum(v for (lay, _), (_, v) in agg.items() if lay == "island")
    summary = {
        "components_file": str(args.components),
        "window": window,
        "giant_size": giant_size,
        "branch_components": branch_comps,
        "branch_vertices": branch_verts,
        "island_components": island_comps,
        "island_vertices": island_verts,
        "closure_hits_total": closure_hits_total,
        "by_layer_max_k": {
            f"{lay}/K_{k}": {"components": n, "vertices": v}
            for (lay, k), (n, v) in sorted(agg.items())
        },
    }
    with (out_prefix.parent / f"{out_prefix.name}_summary.json").open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"giant_size={giant_size}")
    print(f"branch (truncated): {branch_comps} comps, {branch_verts} verts")
    print(f"island (genuine):   {island_comps} comps, {island_verts} verts")
    print(f"closure hits (N_i+N_j==A+B) total: {closure_hits_total}")
    print("\nby layer / max_k:")
    for (lay, k), (n, v) in sorted(agg.items()):
        print(f"  {lay:>7}/K_{k:<3} comps={n:>5} verts={v:>6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
