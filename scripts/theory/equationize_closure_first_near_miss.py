#!/usr/bin/env python3
"""Turn selected closure-first 3/4 near-misses into square-equation ledgers."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from math import gcd, isqrt
from pathlib import Path
from typing import Any

EDGES: tuple[tuple[str, str, str], ...] = (
    ("A-N1", "A", "N1"),
    ("B-N1", "B", "N1"),
    ("B-N2", "B", "N2"),
    ("A-N2", "A", "N2"),
)


def _nearest_square(value: int) -> tuple[bool, int | None, int, int, int]:
    root = isqrt(value)
    if root * root == value:
        return True, root, root, 0, 0
    lower_delta = value - root * root
    upper_root = root + 1
    upper_delta = upper_root * upper_root - value
    if lower_delta <= upper_delta:
        return False, None, root, lower_delta, lower_delta
    return False, None, upper_root, upper_delta, -upper_delta


def _triple_for(leg1: int, leg2: int, hypotenuse: int) -> dict[str, Any]:
    scale = gcd(gcd(leg1, leg2), hypotenuse)
    primitive = [*sorted([leg1 // scale, leg2 // scale]), hypotenuse // scale]
    return {
        "leg1": leg1,
        "leg2": leg2,
        "hypotenuse": hypotenuse,
        "primitive": primitive,
        "scale": scale,
    }


def _edge_summary(name: str, leg1: int, leg2: int) -> dict[str, Any]:
    value = leg1 * leg1 + leg2 * leg2
    is_square, root, nearest_root, nearest_delta, signed_delta = _nearest_square(value)
    out: dict[str, Any] = {
        "leg1": leg1,
        "leg2": leg2,
        "value": value,
        "is_square": is_square,
        "nearest_root": nearest_root,
        "nearest_delta": nearest_delta,
        "signed_delta": signed_delta,
    }
    if root is not None:
        out["root"] = root
        out["triple"] = _triple_for(leg1, leg2, root)
    else:
        out["nearest_square"] = nearest_root * nearest_root
    return out


def _closure_left(a: int, b: int, n1: int, n2: int, relation: str) -> tuple[int, int]:
    if relation == "sum=A+B":
        return n1 + n2, a + b
    if relation == "sum=|A-B|":
        return n1 + n2, abs(a - b)
    if relation == "diff=A+B":
        return abs(n1 - n2), a + b
    if relation == "diff=|A-B|":
        return abs(n1 - n2), abs(a - b)
    raise ValueError(f"unknown relation: {relation}")


def equationize_sample(a: int, b: int, n1: int, n2: int, relation: str) -> dict[str, Any]:
    values = {"A": a, "B": b, "N1": n1, "N2": n2}
    edges = {
        name: _edge_summary(name, values[left], values[right])
        for name, left, right in EDGES
    }
    missing_edges = [name for name, edge in edges.items() if not edge["is_square"]]
    left, target = _closure_left(a, b, n1, n2, relation)
    return {
        "A": a,
        "B": b,
        "N1": n1,
        "N2": n2,
        "relation": relation,
        "closure": {
            "relation": relation,
            "left": left,
            "target": target,
            "holds": left == target,
        },
        "square_count": len(edges) - len(missing_edges),
        "missing_edges": missing_edges,
        "edges": edges,
    }


def _parse_sample(text: str) -> tuple[int, int, int, int, str]:
    parts = text.split(",", 4)
    if len(parts) != 5:
        raise ValueError("sample must be A,B,N1,N2,relation")
    a, b, n1, n2 = (int(part) for part in parts[:4])
    return a, b, n1, n2, parts[4]


def build_payload(samples: list[tuple[int, int, int, int, str]]) -> dict[str, Any]:
    return {
        "sample_count": len(samples),
        "samples": [equationize_sample(*sample) for sample in samples],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sample",
        action="append",
        default=[],
        help="sample as A,B,N1,N2,relation; may be passed multiple times",
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)

    samples = [_parse_sample(text) for text in args.sample]
    if not samples:
        raise ValueError("pass at least one --sample")
    payload = build_payload(samples)
    if args.out is None:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
