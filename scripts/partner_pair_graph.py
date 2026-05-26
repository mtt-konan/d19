#!/usr/bin/env python3
"""Multi-N partner-pair symmetry graph (un-reduced).

A pair (A, B) with concordant N = [N_1, ..., N_k] has the structural identity:
for any i != j, the *un-reduced* pair (N_i, N_j) is itself a multi-concordant
pair whose N-list contains at least {A, B}.

The catalog only stores reduced coprime pairs, so partner (N_i, N_j) almost
never appears in it (typically gcd > 1). To capture the full partner web we
build the graph on un-reduced pairs:

  - vertex: any sorted (a, b) appearing as an original catalog pair OR as a
    partner (N_i, N_j) spawned from an original pair.
  - edge:   (A, B) <-> (N_i, N_j) for each i < j of (A, B)'s concordant N.

This script writes the edge list and reports connected component sizes plus
the highest-degree vertices so we can probe the graph structure.
"""

from __future__ import annotations

import argparse
import json
from math import isqrt
from pathlib import Path


def is_sq(n: int) -> bool:
    return n > 0 and isqrt(n) ** 2 == n


def sorted_pair(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--in",
        dest="in_path",
        type=Path,
        default=Path("results/multi_concordant_N_max100000_fast.jsonl"),
    )
    _ = p.add_argument(
        "--graph-out",
        type=Path,
        default=Path("results/partner_pair_graph.jsonl"),
    )
    _ = p.add_argument(
        "--summary-out",
        type=Path,
        default=Path("results/partner_pair_graph_summary.json"),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    catalog: dict[tuple[int, int], list[int]] = {}
    with args.in_path.open() as f:
        for line in f:
            row = json.loads(line)
            catalog[(int(row["A"]), int(row["B"]))] = [int(n) for n in row["concordant_N"]]

    print(f"Catalog: {len(catalog)} multi-N pairs")

    edges: list[tuple[tuple[int, int], tuple[int, int]]] = []
    vertices: set[tuple[int, int]] = set(catalog.keys())
    partner_only: set[tuple[int, int]] = set()

    for (A, B), Ns in catalog.items():
        for i in range(len(Ns)):
            for j in range(i + 1, len(Ns)):
                Ni, Nj = Ns[i], Ns[j]
                partner = sorted_pair(Ni, Nj)
                edges.append(((A, B), partner))
                if partner not in catalog:
                    partner_only.add(partner)
                vertices.add(partner)

    print()
    print(f"Vertices: {len(vertices)}  ({len(catalog)} catalog + {len(partner_only)} partner-only)")
    print(f"Edges:    {len(edges)}")

    # Connected components (union-find)
    parent: dict[tuple[int, int], tuple[int, int]] = {v: v for v in vertices}

    def find(x: tuple[int, int]) -> tuple[int, int]:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: tuple[int, int], y: tuple[int, int]) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for u, v in edges:
        union(u, v)

    components: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for v in vertices:
        components.setdefault(find(v), []).append(v)

    comp_sizes = sorted((len(c) for c in components.values()), reverse=True)
    print()
    print(f"Connected components: {len(components)}")
    print(f"  size distribution: top10 = {comp_sizes[:10]}, "
          f"singletons = {sum(1 for s in comp_sizes if s == 1)}, "
          f"max = {comp_sizes[0]}")

    # Vertex degrees
    degree: dict[tuple[int, int], int] = {v: 0 for v in vertices}
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1

    top_deg = sorted(degree.items(), key=lambda kv: -kv[1])[:15]
    print()
    print("Top 15 highest-degree vertices:")
    for (a, b), d in top_deg:
        in_cat = "catalog" if (a, b) in catalog else "partner"
        ns = catalog.get((a, b), [])
        print(f"  ({a:>6}, {b:>6})  degree={d:<3}  {in_cat}  N={ns[:5]}{'...' if len(ns) > 5 else ''}")

    # Largest component dump
    largest_root = max(components, key=lambda r: len(components[r]))
    largest = sorted(components[largest_root])
    print()
    print(f"Largest component ({len(largest)} vertices):")
    for v in largest[:30]:
        in_cat = "C" if v in catalog else "P"
        print(f"  {in_cat} ({v[0]:>6}, {v[1]:>6})  deg={degree[v]}")
    if len(largest) > 30:
        print(f"  ... ({len(largest) - 30} more)")

    # Persist
    args.graph_out.parent.mkdir(parents=True, exist_ok=True)
    with args.graph_out.open("w") as f:
        for u, v in edges:
            _ = f.write(
                json.dumps(
                    {"u": list(u), "v": list(v), "u_in_catalog": u in catalog,
                     "v_in_catalog": v in catalog},
                    ensure_ascii=False,
                )
                + "\n"
            )

    summary = {
        "catalog_size": len(catalog),
        "vertices": len(vertices),
        "partner_only_vertices": len(partner_only),
        "edges": len(edges),
        "components": len(components),
        "largest_component_size": comp_sizes[0],
        "top_degree": [{"a": a, "b": b, "degree": d} for (a, b), d in top_deg],
        "component_size_distribution": comp_sizes[:50],
    }
    with args.summary_out.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print()
    print(f"graph edges: {args.graph_out}")
    print(f"summary:     {args.summary_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
