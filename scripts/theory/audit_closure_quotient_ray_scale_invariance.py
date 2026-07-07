#!/usr/bin/env python3
"""Audit closure quotient scale invariance along primitive A:B rays."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.mixed_closure_curves import (  # noqa: E402
    closure_quotient_polynomials,
)

BOUNDARY = (
    "This audits the exact scaling identity for closure quotient quartics and "
    "checks observed rank-key consistency across sampled scales. It does not "
    "prove a new no-point theorem by itself."
)


def load_jsonl(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _primitive_ray(A: int, B: int) -> tuple[int, int, int]:
    scale = math.gcd(A, B)
    return A // scale, B // scale, scale


def _curve_by_name(A: int, B: int, curve_name: str):
    curves = {curve.name: curve for curve in closure_quotient_polynomials(A, B)}
    return curves[curve_name]


def coefficient_scale_relations(
    *,
    A: int,
    B: int,
    curve_name: str,
) -> dict[str, Any]:
    primitive_A, primitive_B, scale = _primitive_ray(A, B)
    primitive_curve = _curve_by_name(primitive_A, primitive_B, curve_name)
    scaled_curve = _curve_by_name(A, B, curve_name)
    relations = []
    for power, (primitive_coeff, scaled_coeff) in enumerate(
        zip(primitive_curve.coeffs, scaled_curve.coeffs, strict=True)
    ):
        scale_power = 4 - power
        expected = primitive_coeff * (scale**scale_power)
        relations.append(
            {
                "power": power,
                "primitive_coeff": primitive_coeff,
                "scaled_coeff": scaled_coeff,
                "scale_power": scale_power,
                "expected_scaled_coeff": expected,
                "matches": scaled_coeff == expected,
            }
        )
    return {
        "A": A,
        "B": B,
        "primitive_A": primitive_A,
        "primitive_B": primitive_B,
        "scale": scale,
        "curve": curve_name,
        "all_coefficients_match": all(row["matches"] for row in relations),
        "coefficient_relations": relations,
    }


def _rank_key(row: dict[str, Any]) -> str:
    if row.get("status") == "ok":
        return f"{row.get('rank_lower')}/{row.get('rank_upper')}"
    return str(row.get("status", "unknown"))


def audit_scale_invariance(rank_rows: list[dict[str, Any]]) -> dict[str, Any]:
    rows_by_pair: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    rows_by_ray_curve: dict[tuple[int, int, str], list[dict[str, Any]]] = defaultdict(list)
    coefficient_identity_verified_count = 0
    coefficient_violations: list[dict[str, Any]] = []

    for row in rank_rows:
        A = int(row["A"])
        B = int(row["B"])
        curve = str(row["curve"])
        primitive_A, primitive_B, _scale = _primitive_ray(A, B)
        rows_by_pair[(A, B)].append(row)
        rows_by_ray_curve[(primitive_A, primitive_B, curve)].append(row)
        relations = coefficient_scale_relations(A=A, B=B, curve_name=curve)
        if relations["all_coefficients_match"]:
            coefficient_identity_verified_count += 1
        else:
            coefficient_violations.append(
                {
                    "A": A,
                    "B": B,
                    "curve": curve,
                    "reason": "coefficient-scale-identity-failed",
                }
            )

    observed_rays = {
        _primitive_ray(A, B)[:2] for A, B in rows_by_pair
    }
    multi_scale_rays = {
        ray
        for ray in observed_rays
        if len(
            {
                _primitive_ray(A, B)[2]
                for A, B in rows_by_pair
                if _primitive_ray(A, B)[:2] == ray
            }
        )
        > 1
    }

    rank_key_consistent_group_count = 0
    rank_key_inconsistent_group_count = 0
    violations = list(coefficient_violations)
    group_summaries = []
    for (primitive_A, primitive_B, curve), rows in sorted(rows_by_ray_curve.items()):
        scales = sorted({_primitive_ray(int(row["A"]), int(row["B"]))[2] for row in rows})
        rank_keys = sorted({_rank_key(row) for row in rows})
        if len(scales) < 2:
            continue
        if len(rank_keys) == 1:
            rank_key_consistent_group_count += 1
        else:
            rank_key_inconsistent_group_count += 1
            violations.append(
                {
                    "primitive_A": primitive_A,
                    "primitive_B": primitive_B,
                    "curve": curve,
                    "reason": "rank-key-varies-across-observed-scales",
                    "rank_keys": rank_keys,
                    "scales": scales,
                }
            )
        group_summaries.append(
            {
                "primitive_A": primitive_A,
                "primitive_B": primitive_B,
                "curve": curve,
                "scales": scales,
                "rank_keys": rank_keys,
                "rank_key_consistent": len(rank_keys) == 1,
            }
        )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "observed_pair_count": len(rows_by_pair),
        "observed_ray_count": len(observed_rays),
        "multi_scale_ray_count": len(multi_scale_rays),
        "rank_row_count": len(rank_rows),
        "coefficient_identity_verified_count": coefficient_identity_verified_count,
        "coefficient_identity_violation_count": len(coefficient_violations),
        "rank_key_consistent_group_count": rank_key_consistent_group_count,
        "rank_key_inconsistent_group_count": rank_key_inconsistent_group_count,
        "violations": violations,
        "multi_scale_groups": group_summaries,
        "scaling_map": {
            "primitive_to_scaled": "A=d*a, B=d*b, N=d*n, y=d^2*y0",
            "coefficient_rule": (
                "coeff_scaled[N^i] = d^(4-i) * coeff_primitive[n^i]"
            ),
        },
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank-jsonl", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_scale_invariance(load_jsonl(args.rank_jsonl))
    write_json(args.out, audit)
    print(f"wrote closure quotient ray scale-invariance audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"observed_ray_count={audit['observed_ray_count']}")
    print(f"multi_scale_ray_count={audit['multi_scale_ray_count']}")
    print(
        "rank_key_inconsistent_group_count="
        f"{audit['rank_key_inconsistent_group_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
