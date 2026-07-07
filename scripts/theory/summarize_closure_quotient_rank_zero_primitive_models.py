#!/usr/bin/env python3
"""Index primitive AA/BB models for rank-zero family candidates."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This indexes primitive AA/BB models for rank-zero family candidates. "
    "It does not prove rank zero or a family exclusion theorem."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _even_model(
    *,
    primitive_A: int,
    primitive_B: int,
    curve: str,
) -> dict[str, Any]:
    total = primitive_A + primitive_B
    leg = primitive_A if curve == "AA" else primitive_B
    sqrt_q = total * total + 4 * leg * leg
    p = 8 * leg * leg - 2 * total * total
    q = sqrt_q * sqrt_q
    return {
        "curve": curve,
        "primitive_A": primitive_A,
        "primitive_B": primitive_B,
        "leg": leg,
        "total": total,
        "p": p,
        "q": q,
        "sqrt_q": sqrt_q,
        "weierstrass_model": [0, p, 0, -4 * q, -4 * p * q],
    }


def primitive_model_for_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    primitive_A, primitive_B = [
        int(value) for value in candidate.get("unordered_primitive_ray", [])
    ]
    patterns = [str(curve) for curve in candidate.get("certifying_curve_patterns", [])]
    return {
        "class": str(candidate.get("class", "")),
        "unordered_primitive_ray": [primitive_A, primitive_B],
        "possible_oriented_rays": candidate.get("possible_oriented_rays", []),
        "c_ratio": str(candidate.get("c_ratio", "")),
        "coverage_status": str(candidate.get("coverage_status", "")),
        "certifying_curve_patterns": patterns,
        "family_exclusion_proved": False,
        "models": [
            _even_model(
                primitive_A=primitive_A,
                primitive_B=primitive_B,
                curve=curve,
            )
            for curve in patterns
            if curve in {"AA", "BB"}
        ],
    }


def summarize_primitive_models(candidates: dict[str, Any]) -> dict[str, Any]:
    rows = [
        primitive_model_for_candidate(candidate)
        for candidate in candidates.get("candidates", [])
    ]
    curve_counts: Counter[str] = Counter(
        str(model["curve"])
        for row in rows
        for model in row.get("models", [])
    )
    return {
        "status": "ok",
        "ready": True,
        "candidate_class_count": len(rows),
        "model_count": sum(len(row.get("models", [])) for row in rows),
        "model_counts_by_curve": dict(sorted(curve_counts.items())),
        "family_exclusion_proved_count": 0,
        "primitive_model_rows": rows,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = summarize_primitive_models(load_json(args.candidates))
    write_json(args.out, summary)
    print(f"wrote closure quotient rank-zero primitive models to {args.out}")
    print(f"status={summary['status']}")
    print(f"candidate_class_count={summary['candidate_class_count']}")
    print(f"model_count={summary['model_count']}")
    print(f"family_exclusion_proved_count={summary['family_exclusion_proved_count']}")
    if args.strict and summary["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
