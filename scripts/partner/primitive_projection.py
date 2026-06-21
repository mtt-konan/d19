#!/usr/bin/env python3
"""Project partner-graph edges onto primitive-pair templates.

This is a small research helper for wl223: an edge ``(A,B)--(N_i,N_j)`` is
compressed to ``prim(A,B)--prim(N_i,N_j)``. If many raw edges collapse to a
small number of primitive templates, that is evidence for a lower-dimensional
correspondence structure underneath the large partner graph.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from math import gcd
from pathlib import Path
from typing import Any, Iterable


Pair = tuple[int, int]


@dataclass(frozen=True)
class EdgeTemplate:
    source: Pair
    target: Pair
    source_scale: int
    target_scale: int

    @property
    def key(self) -> tuple[Pair, Pair]:
        return tuple(sorted((self.source, self.target)))  # type: ignore[return-value]


def primitive_pair(pair: tuple[int, int] | list[int]) -> Pair:
    """Return the sorted coprime representative of a positive integer pair."""
    a, b = int(pair[0]), int(pair[1])
    if a <= 0 or b <= 0:
        raise ValueError(f"pair must be positive: {pair}")
    g = gcd(a, b)
    pa, pb = a // g, b // g
    return (pa, pb) if pa <= pb else (pb, pa)


def _scale(pair: tuple[int, int] | list[int]) -> int:
    return gcd(int(pair[0]), int(pair[1]))


def edge_template(row: dict[str, Any]) -> EdgeTemplate:
    """Project one edge JSON row from ``partner_full_bfs_edges.jsonl``."""
    u = row["u"]
    v = row["v"]
    return EdgeTemplate(
        source=primitive_pair(u),
        target=primitive_pair(v),
        source_scale=_scale(u),
        target_scale=_scale(v),
    )


def summarize_templates(
    rows: Iterable[dict[str, Any]],
    *,
    top: int = 20,
) -> dict[str, Any]:
    counts: Counter[tuple[Pair, Pair]] = Counter()
    source_counts: Counter[Pair] = Counter()
    loop_edges = 0
    edges_scanned = 0

    for row in rows:
        tmpl = edge_template(row)
        key = tmpl.key
        counts[key] += 1
        source_counts[tmpl.source] += 1
        source_counts[tmpl.target] += 1
        if tmpl.source == tmpl.target:
            loop_edges += 1
        edges_scanned += 1

    top_template_items = counts.most_common(top)
    top_primitive_items = source_counts.most_common(top)
    top_templates = [
        {
            "source_primitive": list(source),
            "target_primitive": list(target),
            "count": count,
        }
        for (source, target), count in top_template_items
    ]
    top_primitives = [
        {"primitive": list(pair), "incident_edges": count}
        for pair, count in top_primitive_items
    ]
    top_template_edges = sum(count for _, count in top_template_items)
    top_primitive_incidents = sum(count for _, count in top_primitive_items)
    return {
        "edges_scanned": edges_scanned,
        "unique_templates": len(counts),
        "unique_primitives": len(source_counts),
        "loop_edges": loop_edges,
        "top_templates_edge_share_pct": round(
            100 * top_template_edges / max(1, edges_scanned), 2
        ),
        "top_primitives_incident_share_pct": round(
            100 * top_primitive_incidents / max(1, 2 * edges_scanned), 2
        ),
        "top_templates": top_templates,
        "top_primitives": top_primitives,
    }


def summarize_by_layer(
    rows: Iterable[dict[str, Any]],
    *,
    layer_of: dict[Pair, str],
    top: int = 20,
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    cross_layer_edges = 0
    missing_layer_edges = 0

    for row in rows:
        u = (int(row["u"][0]), int(row["u"][1]))
        v = (int(row["v"][0]), int(row["v"][1]))
        lu = layer_of.get(u)
        lv = layer_of.get(v)
        if lu is None or lv is None:
            missing_layer_edges += 1
            continue
        if lu == lv:
            grouped[lu].append(row)
        else:
            cross_layer_edges += 1
            grouped[f"{lu}->{lv}"].append(row)

    return {
        "by_layer": {
            layer: summarize_templates(layer_rows, top=top)
            for layer, layer_rows in sorted(grouped.items())
        },
        "cross_layer_edges": cross_layer_edges,
        "missing_layer_edges": missing_layer_edges,
    }


def load_vertex_layers(components_path: Path, layers_path: Path) -> dict[Pair, str]:
    component_layer: dict[int, str] = {}
    with layers_path.open() as f:
        for line in f:
            row = json.loads(line)
            component_layer[int(row["component_id"])] = str(row["layer"])

    out: dict[Pair, str] = {}
    with components_path.open() as f:
        for line in f:
            component = json.loads(line)
            cid = int(component["component_id"])
            layer = component_layer[cid]
            for vertex in component["vertices"]:
                out[(int(vertex[0]), int(vertex[1]))] = layer
    return out


def _iter_jsonl(path: Path, limit: int | None) -> Iterable[dict[str, Any]]:
    with path.open() as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            yield json.loads(line)


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
        default=Path("results/partner/primitive_projection_1M_summary.json"),
    )
    _ = parser.add_argument(
        "--components",
        type=Path,
        default=None,
        help="Optional component dump used with --layers for layer summaries.",
    )
    _ = parser.add_argument(
        "--layers",
        type=Path,
        default=None,
        help="Optional comp0_island_analysis jsonl used with --components.",
    )
    _ = parser.add_argument("--top", type=int, default=25)
    _ = parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional edge limit for quick smoke runs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = list(_iter_jsonl(args.edges, args.limit))
    summary = summarize_templates(rows, top=int(args.top))
    if args.components is not None or args.layers is not None:
        if args.components is None or args.layers is None:
            raise SystemExit("--components and --layers must be provided together")
        summary.update(
            summarize_by_layer(
                rows,
                layer_of=load_vertex_layers(args.components, args.layers),
                top=int(args.top),
            )
        )
    summary["edges_file"] = str(args.edges)
    summary["limit"] = args.limit

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
