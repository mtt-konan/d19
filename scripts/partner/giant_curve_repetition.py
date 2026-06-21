#!/usr/bin/env python3
"""Measure repeated primitive elliptic-curve classes in partner components.

Each raw vertex ``(A, B)`` has its own integer model
``E_{A,B}: y^2 = x(x+A^2)(x+B^2)``.  Vertices with the same gcd-reduced
``primitive(A,B)`` are rationally isomorphic by D-scaling, so this helper asks
whether a component repeatedly lands on the same primitive curve class.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.partner.primitive_projection import primitive_pair


Pair = tuple[int, int]


def j_invariant_key(pair: Pair | list[int]) -> str:
    """Return the exact j-invariant key for ``E_{a,b}`` as a rational string."""
    a, b = primitive_pair(pair)
    lam = Fraction(a * a, b * b)
    j = Fraction(256) * (1 - lam + lam * lam) ** 3 / (lam * lam * (1 - lam) ** 2)
    return f"{j.numerator}/{j.denominator}"


def _scale(pair: list[int] | tuple[int, int]) -> int:
    return gcd(int(pair[0]), int(pair[1]))


def _load_components(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    components: list[dict[str, Any]] = []
    with path.open() as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            components.append(json.loads(line))
    return components


def component_curve_repetition(component: dict[str, Any], *, top: int = 25) -> dict[str, Any]:
    """Summarize primitive-curve reuse inside one component."""
    grouped: dict[Pair, list[tuple[Pair, int]]] = defaultdict(list)
    j_counts: defaultdict[str, int] = defaultdict(int)
    for vertex in component["vertices"]:
        pair = (int(vertex[0]), int(vertex[1]))
        primitive = primitive_pair(pair)
        grouped[primitive].append((pair, _scale(pair)))
        j_counts[j_invariant_key(primitive)] += 1

    vertex_count = sum(len(vertices) for vertices in grouped.values())
    primitive_count = len(grouped)
    repeated = {pair: vertices for pair, vertices in grouped.items() if len(vertices) > 1}
    top_items = sorted(
        grouped.items(),
        key=lambda item: (-len(item[1]), item[0][0], item[0][1]),
    )[:top]
    top_curves = []
    for primitive, vertices in top_items:
        scales = [scale for _pair, scale in vertices]
        sample = sorted(pair for pair, _scale_value in vertices)[:10]
        top_curves.append(
            {
                "primitive": list(primitive),
                "scaled_vertex_count": len(vertices),
                "share_pct": round(100 * len(vertices) / max(1, vertex_count), 4),
                "min_scale": min(scales),
                "max_scale": max(scales),
                "sample_vertices": [list(pair) for pair in sample],
            }
        )

    return {
        "component_id": int(component["component_id"]),
        "vertex_count": vertex_count,
        "edge_count": int(component.get("edges", 0)),
        "primitive_curve_count": primitive_count,
        "repeated_primitive_curve_count": len(repeated),
        "singleton_primitive_curve_count": primitive_count - len(repeated),
        "primitive_reuse_ratio": round(vertex_count / max(1, primitive_count), 6),
        "j_curve_count": len(j_counts),
        "repeated_j_curve_count": sum(1 for count in j_counts.values() if count > 1),
        "j_reuse_ratio": round(vertex_count / max(1, len(j_counts)), 6),
        "largest_primitive_class_size": max((len(v) for v in grouped.values()), default=0),
        "top_primitive_curves": top_curves,
    }


def _combine_components(components: Iterable[dict[str, Any]], *, top: int) -> dict[str, Any]:
    grouped: dict[Pair, list[Pair]] = defaultdict(list)
    j_counts: defaultdict[str, int] = defaultdict(int)
    component_count = 0
    for component in components:
        component_count += 1
        for vertex in component["vertices"]:
            pair = (int(vertex[0]), int(vertex[1]))
            primitive = primitive_pair(pair)
            grouped[primitive].append(pair)
            j_counts[j_invariant_key(primitive)] += 1

    vertex_count = sum(len(vertices) for vertices in grouped.values())
    top_items = sorted(
        grouped.items(),
        key=lambda item: (-len(item[1]), item[0][0], item[0][1]),
    )[:top]
    return {
        "component_count": component_count,
        "vertex_count": vertex_count,
        "primitive_curve_count": len(grouped),
        "repeated_primitive_curve_count": sum(1 for vertices in grouped.values() if len(vertices) > 1),
        "primitive_reuse_ratio": round(vertex_count / max(1, len(grouped)), 6),
        "j_curve_count": len(j_counts),
        "repeated_j_curve_count": sum(1 for count in j_counts.values() if count > 1),
        "j_reuse_ratio": round(vertex_count / max(1, len(j_counts)), 6),
        "largest_primitive_class_size": max((len(v) for v in grouped.values()), default=0),
        "top_primitive_curves": [
            {
                "primitive": list(primitive),
                "scaled_vertex_count": len(vertices),
                "share_pct": round(100 * len(vertices) / max(1, vertex_count), 4),
                "sample_vertices": [list(pair) for pair in sorted(vertices)[:10]],
            }
            for primitive, vertices in top_items
        ],
    }


def summarize_curve_repetition(
    components: list[dict[str, Any]],
    *,
    top: int = 25,
) -> dict[str, Any]:
    """Compare primitive-curve reuse in the giant component vs the rest."""
    if not components:
        return {
            "component_count": 0,
            "giant": None,
            "non_giant_totals": _combine_components([], top=top),
        }

    giant = max(components, key=lambda component: int(component["size"]))
    non_giant = [component for component in components if component is not giant]
    return {
        "component_count": len(components),
        "giant": component_curve_repetition(giant, top=top),
        "non_giant_totals": _combine_components(non_giant, top=top),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "--components",
        type=Path,
        default=Path("results/partner/partner_full_bfs_components.jsonl"),
    )
    _ = parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/partner/giant_curve_repetition_summary.json"),
    )
    _ = parser.add_argument("--top", type=int, default=25)
    _ = parser.add_argument("--limit-components", type=int, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    components = _load_components(args.components, limit=args.limit_components)
    summary = summarize_curve_repetition(components, top=int(args.top))
    summary["components_file"] = str(args.components)
    summary["limit_components"] = args.limit_components

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
