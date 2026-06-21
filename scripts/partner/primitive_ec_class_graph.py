#!/usr/bin/env python3
"""Build the primitive elliptic-curve class graph from partner-graph edges.

The raw partner graph has vertices ``(A, B)``.  This projection contracts every
raw vertex to its gcd-reduced primitive class ``prim(A,B)`` and keeps an edge
between two primitive classes when any raw partner edge realizes that jump.

Self-loops are counted separately: they are evidence for activity within one
primitive family, while cross edges are the primitive-level correspondence graph
whose components, cycles, and core are the main object here.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.partner.primitive_projection import primitive_pair  # noqa: E402


Pair = tuple[int, int]
EdgeKey = tuple[Pair, Pair]


@dataclass(frozen=True)
class PrimitiveEdge:
    source: Pair
    target: Pair
    source_scale: int
    target_scale: int

    @property
    def is_loop(self) -> bool:
        return self.source == self.target

    @property
    def key(self) -> EdgeKey:
        return tuple(sorted((self.source, self.target)))  # type: ignore[return-value]


@dataclass
class PrimitiveGraph:
    nodes: set[Pair] = field(default_factory=set)
    adjacency: dict[Pair, set[Pair]] = field(default_factory=lambda: defaultdict(set))
    edge_weights: Counter[EdgeKey] = field(default_factory=Counter)
    loop_weights: Counter[Pair] = field(default_factory=Counter)
    raw_edges: int = 0

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edge_weights)

    @property
    def loop_raw_edges(self) -> int:
        return sum(self.loop_weights.values())

    @property
    def loop_template_count(self) -> int:
        return len(self.loop_weights)

    def add_projected_edge(self, edge: PrimitiveEdge) -> None:
        self.raw_edges += 1
        self.nodes.add(edge.source)
        self.nodes.add(edge.target)
        if edge.is_loop:
            self.loop_weights[edge.source] += 1
            return
        key = edge.key
        u, v = key
        self.edge_weights[key] += 1
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)


def _scale(pair: tuple[int, int] | list[int]) -> int:
    from math import gcd

    return gcd(int(pair[0]), int(pair[1]))


def project_edge(row: dict[str, Any]) -> PrimitiveEdge:
    """Project one raw JSONL edge row to primitive classes."""
    u = row["u"]
    v = row["v"]
    return PrimitiveEdge(
        source=primitive_pair(u),
        target=primitive_pair(v),
        source_scale=_scale(u),
        target_scale=_scale(v),
    )


def build_primitive_graph(rows: Iterable[dict[str, Any]]) -> PrimitiveGraph:
    graph = PrimitiveGraph()
    for row in rows:
        graph.add_projected_edge(project_edge(row))
    return graph


def _connected_components(graph: PrimitiveGraph) -> list[set[Pair]]:
    seen: set[Pair] = set()
    components: list[set[Pair]] = []
    for start in sorted(graph.nodes):
        if start in seen:
            continue
        component: set[Pair] = set()
        queue: deque[Pair] = deque([start])
        seen.add(start)
        while queue:
            node = queue.popleft()
            component.add(node)
            for neighbor in graph.adjacency.get(node, ()):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        components.append(component)
    components.sort(key=lambda comp: (-len(comp), sorted(comp)[0]))
    return components


def _edge_count_inside(graph: PrimitiveGraph, component: set[Pair]) -> int:
    return sum(1 for u, v in graph.edge_weights if u in component and v in component)


def component_stats(graph: PrimitiveGraph, *, top: int = 20) -> dict[str, Any]:
    components = _connected_components(graph)
    sizes = [len(component) for component in components]
    edge_counts = [_edge_count_inside(graph, component) for component in components]
    component_rows = []
    for idx, component in enumerate(components[:top]):
        edges = edge_counts[idx]
        component_rows.append(
            {
                "rank": idx + 1,
                "size": len(component),
                "edges": edges,
                "circuit_rank": edges - len(component) + 1,
                "sample_nodes": [list(node) for node in sorted(component)[:10]],
            }
        )

    largest_size = sizes[0] if sizes else 0
    largest_edges = edge_counts[0] if edge_counts else 0
    return {
        "component_count": len(components),
        "largest_component_size": largest_size,
        "largest_component_edges": largest_edges,
        "largest_component_circuit_rank": (
            largest_edges - largest_size + 1 if largest_size else 0
        ),
        "largest_component_share_pct": round(
            100 * largest_size / max(1, graph.node_count), 4
        ),
        "component_size_hist": {
            str(size): count for size, count in sorted(Counter(sizes).items())
        },
        "top_components": component_rows,
    }


def _degree_histogram(graph: PrimitiveGraph) -> tuple[dict[Pair, int], dict[str, int]]:
    degree = {node: len(graph.adjacency.get(node, ())) for node in graph.nodes}
    hist = Counter(degree.values())
    return degree, {str(deg): hist[deg] for deg in sorted(hist)}


def _weighted_degree(graph: PrimitiveGraph) -> dict[Pair, int]:
    weighted = {node: 0 for node in graph.nodes}
    for (u, v), weight in graph.edge_weights.items():
        weighted[u] += weight
        weighted[v] += weight
    return weighted


def _top_nodes(graph: PrimitiveGraph, *, top: int) -> list[dict[str, Any]]:
    degree = {node: len(graph.adjacency.get(node, ())) for node in graph.nodes}
    weighted = _weighted_degree(graph)
    loop_weight = graph.loop_weights
    rows = []
    for node in sorted(
        graph.nodes,
        key=lambda n: (-degree[n], -weighted[n], -loop_weight[n], n[0], n[1]),
    )[:top]:
        rows.append(
            {
                "primitive": list(node),
                "degree": degree[node],
                "weighted_degree": weighted[node],
                "loop_raw_edges": loop_weight[node],
            }
        )
    return rows


def _top_edges(graph: PrimitiveGraph, *, top: int) -> list[dict[str, Any]]:
    return [
        {
            "source_primitive": list(source),
            "target_primitive": list(target),
            "raw_edge_weight": weight,
        }
        for (source, target), weight in graph.edge_weights.most_common(top)
    ]


def _core_nodes(graph: PrimitiveGraph, min_degree: int) -> set[Pair]:
    degree = {node: len(graph.adjacency.get(node, ())) for node in graph.nodes}
    removed: set[Pair] = set()
    queue: deque[Pair] = deque(
        node for node, deg in degree.items() if deg < min_degree
    )
    while queue:
        node = queue.popleft()
        if node in removed:
            continue
        removed.add(node)
        for neighbor in graph.adjacency.get(node, ()):
            if neighbor in removed:
                continue
            degree[neighbor] -= 1
            if degree[neighbor] < min_degree:
                queue.append(neighbor)
    return graph.nodes - removed


def _core_stats(graph: PrimitiveGraph, min_degree: int) -> dict[str, Any]:
    nodes = _core_nodes(graph, min_degree)
    edges = _edge_count_inside(graph, nodes)
    return {
        "nodes": len(nodes),
        "edges": edges,
        "circuit_rank": edges - len(nodes) + 1 if nodes else 0,
        "share_pct": round(100 * len(nodes) / max(1, graph.node_count), 4),
    }


def _node_id(pair: Pair) -> str:
    return f"{pair[0]}_{pair[1]}"


def export_gephi_tables(graph: PrimitiveGraph, out_dir: Path) -> dict[str, Any]:
    """Write Gephi-friendly ``nodes.csv`` and ``edges.csv`` for a graph."""
    out_dir.mkdir(parents=True, exist_ok=True)
    degree = {node: len(graph.adjacency.get(node, ())) for node in graph.nodes}
    weighted = _weighted_degree(graph)
    core_2 = _core_nodes(graph, 2)
    core_3 = _core_nodes(graph, 3)

    nodes_out = out_dir / "nodes.csv"
    with nodes_out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Id",
                "Label",
                "A",
                "B",
                "degree",
                "weighted_degree",
                "loop_raw_edges",
                "core_2",
                "core_3",
            ]
        )
        for node in sorted(graph.nodes):
            writer.writerow(
                [
                    _node_id(node),
                    f"({node[0]},{node[1]})",
                    node[0],
                    node[1],
                    degree[node],
                    weighted[node],
                    graph.loop_weights[node],
                    str(node in core_2).lower(),
                    str(node in core_3).lower(),
                ]
            )

    edges_out = out_dir / "edges.csv"
    with edges_out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Type", "Weight"])
        for (source, target), weight in sorted(graph.edge_weights.items()):
            writer.writerow([_node_id(source), _node_id(target), "Undirected", weight])

    summary = {
        "node_count": graph.node_count,
        "edge_count": graph.edge_count,
        "raw_edges": graph.raw_edges,
        "loop_raw_edges": graph.loop_raw_edges,
        "nodes_csv": str(nodes_out),
        "edges_csv": str(edges_out),
    }
    with (out_dir / "summary.json").open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    return summary


def _triangle_stats(graph: PrimitiveGraph) -> dict[str, Any]:
    triangles = 0
    triples = 0
    for node in graph.nodes:
        neighbors = sorted(graph.adjacency.get(node, ()))
        degree = len(neighbors)
        triples += degree * (degree - 1) // 2
        for i, u in enumerate(neighbors):
            u_neighbors = graph.adjacency.get(u, set())
            for v in neighbors[i + 1 :]:
                if v in u_neighbors:
                    triangles += 1
    triangle_count = triangles // 3
    return {
        "triangles": triangle_count,
        "connected_triples": triples,
        "transitivity": round(3 * triangle_count / triples, 6) if triples else 0.0,
    }


def summarize_primitive_graph(
    rows: Iterable[dict[str, Any]],
    *,
    raw_vertices: set[Pair] | None = None,
    top: int = 25,
) -> dict[str, Any]:
    raw_edges_seen = 0
    raw_edges_skipped = 0
    used_rows = []
    for row in rows:
        raw_edges_seen += 1
        if raw_vertices is not None:
            u = (int(row["u"][0]), int(row["u"][1]))
            v = (int(row["v"][0]), int(row["v"][1]))
            if u not in raw_vertices or v not in raw_vertices:
                raw_edges_skipped += 1
                continue
        used_rows.append(row)

    graph = build_primitive_graph(used_rows)
    _degree, degree_hist = _degree_histogram(graph)
    circuit_rank = graph.edge_count - graph.node_count + component_stats(graph)["component_count"]
    return {
        "raw_edges_seen": raw_edges_seen,
        "raw_edges_used": graph.raw_edges,
        "raw_edges_skipped_by_filter": raw_edges_skipped,
        "primitive_nodes": graph.node_count,
        "primitive_edges": graph.edge_count,
        "loop_raw_edges": graph.loop_raw_edges,
        "loop_template_count": graph.loop_template_count,
        "cross_raw_edges": graph.raw_edges - graph.loop_raw_edges,
        "cross_raw_edge_share_pct": round(
            100 * (graph.raw_edges - graph.loop_raw_edges) / max(1, graph.raw_edges),
            4,
        ),
        "components": component_stats(graph, top=top),
        "degree": {
            "histogram": degree_hist,
            "max": max((int(deg) for deg in degree_hist), default=0),
            "mean": round(
                2 * graph.edge_count / max(1, graph.node_count),
                6,
            ),
        },
        "cycle": {
            "circuit_rank": circuit_rank,
            "cycle_density": round(
                circuit_rank / max(1, graph.edge_count), 6,
            ),
        },
        "clustering": _triangle_stats(graph),
        "core_2": _core_stats(graph, 2),
        "core_3": _core_stats(graph, 3),
        "top_nodes": _top_nodes(graph, top=top),
        "top_edges": _top_edges(graph, top=top),
        "top_loops": [
            {"primitive": list(node), "raw_loop_weight": weight}
            for node, weight in graph.loop_weights.most_common(top)
        ],
    }


def _iter_jsonl(path: Path, limit: int | None = None) -> Iterable[dict[str, Any]]:
    with path.open() as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            yield json.loads(line)


def load_component_vertices(path: Path, component_id: int) -> set[Pair]:
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            if int(row["component_id"]) == component_id:
                return {
                    (int(vertex[0]), int(vertex[1]))
                    for vertex in row["vertices"]
                }
    raise ValueError(f"component_id {component_id} not found in {path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--edges",
        type=Path,
        default=Path("results/partner/partner_full_bfs_edges.jsonl"),
    )
    _ = parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/partner/primitive_ec_class_graph_1M_summary.json"),
    )
    _ = parser.add_argument("--top", type=int, default=25)
    _ = parser.add_argument("--limit", type=int, default=None)
    _ = parser.add_argument(
        "--components",
        type=Path,
        default=None,
        help="Optional raw component dump used with --component-id filtering.",
    )
    _ = parser.add_argument(
        "--component-id",
        type=int,
        default=None,
        help="Only keep raw edges whose endpoints both lie in this component.",
    )
    _ = parser.add_argument(
        "--gephi-out-dir",
        type=Path,
        default=None,
        help="Optional directory for Gephi nodes.csv / edges.csv export.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    t0 = time.time()
    raw_vertices = None
    if args.component_id is not None:
        if args.components is None:
            raise SystemExit("--component-id requires --components")
        raw_vertices = load_component_vertices(args.components, int(args.component_id))
    rows = list(_iter_jsonl(args.edges, args.limit))
    used_rows = rows
    if raw_vertices is not None:
        used_rows = [
            row
            for row in rows
            if (int(row["u"][0]), int(row["u"][1])) in raw_vertices
            and (int(row["v"][0]), int(row["v"][1])) in raw_vertices
        ]
    graph = build_primitive_graph(used_rows)
    summary = summarize_primitive_graph(rows, raw_vertices=raw_vertices, top=int(args.top))
    if args.gephi_out_dir is not None:
        summary["gephi"] = export_gephi_tables(graph, args.gephi_out_dir)
    summary["edges_file"] = str(args.edges)
    summary["components_file"] = str(args.components) if args.components is not None else None
    summary["component_id_filter"] = args.component_id
    summary["limit"] = args.limit
    summary["elapsed_s"] = round(time.time() - t0, 3)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
