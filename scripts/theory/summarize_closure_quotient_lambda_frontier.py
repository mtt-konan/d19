#!/usr/bin/env python3
"""Route primitive lambda classes to structural proof tracks."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This is a lambda-frontier routing ledger. It does not prove any primitive "
    "ratio class is excluded as a family."
)

ACCEPTED_STRUCTURAL_ROUTES = (
    "family rank-zero mechanism over a primitive lambda class",
    "rigorous root-number/parity argument combined with a rank or descent theorem",
    "family 2-cover or Selmer obstruction",
    "reviewable cover-level no-point certificate for every remaining cover",
)

REJECTED_PROGRESS_METRICS = (
    "more individual (A,B) search hits",
    "bounded point search with zero points",
    "longer timeout without a certificate",
    "root number by itself",
    "candidate 2-cover without a proof transcript",
)

TRACK_BY_COVERAGE_STATUS = {
    "all-observed-pairs-strict": "rank-zero-family-generalization",
    "some-observed-pairs-strict": "rank-zero-family-generalization",
    "residual-candidate-open": "two-cover-or-reviewable-no-point-certificate",
    "observed-open": "root-number-rank-structure-triage",
}

NEXT_ACTION_BY_TRACK = {
    "rank-zero-family-generalization": (
        "Try to prove that the observed AA/BB rank-zero torsion-pullback "
        "mechanism persists on the primitive lambda class, instead of adding "
        "more scaled (A,B) samples."
    ),
    "two-cover-or-reviewable-no-point-certificate": (
        "Replace the residual candidate with a family 2-cover obstruction or "
        "a reviewable cover-level no-point certificate."
    ),
    "root-number-rank-structure-triage": (
        "Use root-number and rank-pattern diagnostics only to choose a family "
        "rank/descent problem; do not count the diagnostic as proof."
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _route_class(row: dict[str, Any]) -> dict[str, Any]:
    coverage_status = str(row.get("coverage_status", ""))
    track = TRACK_BY_COVERAGE_STATUS.get(
        coverage_status,
        "manual-review",
    )
    return {
        "class": str(row.get("class", "")),
        "unordered_primitive_ray": row.get("unordered_primitive_ray", []),
        "possible_oriented_rays": row.get("possible_oriented_rays", []),
        "observed_oriented_rays": row.get("observed_oriented_rays", []),
        "c_ratio": str(row.get("c_ratio", "")),
        "coverage_status": coverage_status,
        "track": track,
        "next_action": NEXT_ACTION_BY_TRACK.get(
            track,
            "Manually inspect this lambda class before promoting any claim.",
        ),
        "family_exclusion_proved": False,
        "candidate_not_proof": True,
    }


def summarize_lambda_frontier(ray_ledger: dict[str, Any]) -> dict[str, Any]:
    routes = [_route_class(row) for row in ray_ledger.get("c_ratio_class_rows", [])]
    track_counts = Counter(str(route["track"]) for route in routes)
    coverage_counts = Counter(str(route["coverage_status"]) for route in routes)
    return {
        "status": "ok",
        "ready": True,
        "lambda_class_count": len(routes),
        "track_counts": dict(sorted(track_counts.items())),
        "coverage_status_counts": dict(sorted(coverage_counts.items())),
        "family_exclusion_proved_count": 0,
        "candidate_not_proof": True,
        "accepted_structural_routes": list(ACCEPTED_STRUCTURAL_ROUTES),
        "rejected_progress_metrics": list(REJECTED_PROGRESS_METRICS),
        "mainline": (
            "Move from pair-count accumulation to lambda=A/B structural proof "
            "tracks."
        ),
        "routes": routes,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ray-ledger", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = summarize_lambda_frontier(load_json(args.ray_ledger))
    write_json(args.out, summary)
    print(f"wrote closure quotient lambda frontier to {args.out}")
    print(f"status={summary['status']}")
    print(f"lambda_class_count={summary['lambda_class_count']}")
    print(f"track_counts={summary['track_counts']}")
    print(f"family_exclusion_proved_count={summary['family_exclusion_proved_count']}")
    if args.strict and summary["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
