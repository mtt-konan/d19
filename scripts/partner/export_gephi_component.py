#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent.parent


@dataclass
class Args:
    components: Path
    edges: Path
    component_id: int
    out_dir: Path | None


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "--components",
        type=Path,
        default=Path("results/partner_full_bfs_components.jsonl"),
    )
    _ = parser.add_argument(
        "--edges",
        type=Path,
        default=Path("results/partner_full_bfs_edges.jsonl"),
    )
    _ = parser.add_argument("--component-id", type=int, default=0)
    _ = parser.add_argument("--out-dir", type=Path)
    namespace = parser.parse_args()
    return Args(
        components=cast(Path, namespace.components),
        edges=cast(Path, namespace.edges),
        component_id=cast(int, namespace.component_id),
        out_dir=cast(Path | None, namespace.out_dir),
    )


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def parse_int(value: object) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        return int(value)
    raise TypeError(f"expected int-like value, got {type(value).__name__}")


def parse_vertex(value: object) -> tuple[int, int]:
    pair = cast(list[object], value)
    return parse_int(pair[0]), parse_int(pair[1])


def load_component_vertices(
    components_path: Path,
    component_id: int,
) -> list[tuple[int, int]]:
    with components_path.open() as f:
        for line in f:
            row = cast(dict[str, object], json.loads(line))
            if parse_int(row["component_id"]) == component_id:
                vertices = cast(list[object], row["vertices"])
                return [parse_vertex(v) for v in vertices]
    raise ValueError(f"component_id={component_id} not found: {components_path}")


def visible_k_from_degree(degree: int) -> int:
    if degree == 0:
        return 1
    disc = 1 + 8 * degree
    root = math.isqrt(disc)
    if root * root != disc:
        return -1
    k = (1 + root) // 2
    return k if k * (k - 1) // 2 == degree else -1


def main() -> int:
    args = parse_args()
    components_path = resolve_path(args.components)
    edges_path = resolve_path(args.edges)
    out_dir = (
        resolve_path(args.out_dir)
        if args.out_dir is not None
        else ROOT / "results" / f"gephi_comp{args.component_id}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    vertices = sorted(load_component_vertices(components_path, args.component_id))
    vertex_set = set(vertices)
    vertex_to_id = {vertex: i for i, vertex in enumerate(vertices)}
    degree: Counter[tuple[int, int]] = Counter()

    edges_out = out_dir / "edges.csv"
    edge_count = 0
    with edges_path.open() as src, edges_out.open("w", newline="") as dst:
        writer = csv.writer(dst)
        writer.writerow(["Source", "Target", "Type", "Weight"])
        for line in src:
            row = cast(dict[str, object], json.loads(line))
            u = parse_vertex(row["u"])
            v = parse_vertex(row["v"])
            if u not in vertex_set or v not in vertex_set:
                continue
            writer.writerow([vertex_to_id[u], vertex_to_id[v], "Undirected", 1])
            degree[u] += 1
            degree[v] += 1
            edge_count += 1

    nodes_out = out_dir / "nodes.csv"
    with nodes_out.open("w", newline="") as dst:
        writer = csv.writer(dst)
        writer.writerow(["Id", "A", "B", "degree", "k_visible"])
        for vertex in vertices:
            d = degree[vertex]
            writer.writerow([
                vertex_to_id[vertex],
                vertex[0],
                vertex[1],
                d,
                visible_k_from_degree(d),
            ])

    summary = {
        "component_id": args.component_id,
        "vertex_count": len(vertices),
        "edge_count": edge_count,
        "nodes_csv": str(nodes_out),
        "edges_csv": str(edges_out),
        "degree_histogram": dict(sorted(Counter(degree.values()).items())),
    }
    summary_out = out_dir / "summary.json"
    with summary_out.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"component_id = {args.component_id}")
    print(f"vertices     = {len(vertices)}")
    print(f"edges        = {edge_count}")
    print(f"nodes.csv    = {nodes_out}")
    print(f"edges.csv    = {edges_out}")
    print(f"summary.json = {summary_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
