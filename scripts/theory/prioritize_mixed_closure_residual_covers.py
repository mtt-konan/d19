#!/usr/bin/env python3
"""Prioritize explicit mixed-closure residual 2-cover candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sympy import Poly, symbols, sympify


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _row_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return int(row["A"]), int(row["B"]), str(row["curve"])


def _evidence_index(evidence_audit: dict[str, Any]) -> dict[tuple[int, int, str], dict[str, Any]]:
    return {_row_key(row): row for row in evidence_audit.get("residual_rows", [])}


def quartic_complexity(quartic: str) -> dict[str, int]:
    x = symbols("x")
    expr = sympify(quartic.replace("^", "**"), locals={"x": x})
    poly = Poly(expr, x)
    coefficients = [int(coefficient) for coefficient in poly.all_coeffs()]
    return {
        "degree": int(poly.degree()),
        "term_count": len(poly.terms()),
        "coefficient_height": max(abs(coefficient) for coefficient in coefficients),
    }


def prioritize_residual_covers(
    *,
    cover_summary: dict[str, Any],
    evidence_audit: dict[str, Any],
) -> dict[str, Any]:
    evidence_by_key = _evidence_index(evidence_audit)
    rows: list[dict[str, Any]] = []

    for cover_row in cover_summary.get("no_point_cover_rows", []):
        key = _row_key(cover_row)
        evidence = evidence_by_key.get(key, {})
        bsd_status = str(evidence.get("bsd_status", "missing"))
        bsd_analytic_rank = evidence.get("bsd_analytic_rank")
        has_bsd_conditional_rank0 = bsd_status == "ok" and bsd_analytic_rank == 0
        proof_status = str(evidence.get("proof_status", "candidate-not-proof"))

        for cover in cover_row.get("no_point_covers", []):
            complexity = quartic_complexity(str(cover["quartic"]))
            rows.append(
                {
                    "A": int(cover_row["A"]),
                    "B": int(cover_row["B"]),
                    "curve": str(cover_row["curve"]),
                    "cover_index": int(cover["index"]),
                    "quartic": str(cover["quartic"]),
                    **complexity,
                    "selmer_gap": int(cover_row["selmer_gap"]),
                    "bsd_status": bsd_status,
                    "bsd_analytic_rank": bsd_analytic_rank,
                    "has_bsd_conditional_rank0": has_bsd_conditional_rank0,
                    "proof_status": proof_status,
                }
            )

    rows.sort(
        key=lambda row: (
            0 if row["has_bsd_conditional_rank0"] else 1,
            int(row["coefficient_height"]),
            int(row["term_count"]),
            int(row["A"]) + int(row["B"]),
            str(row["curve"]),
            int(row["cover_index"]),
        )
    )
    for priority, row in enumerate(rows, start=1):
        row["priority"] = priority

    return {
        "candidate_cover_total": len(rows),
        "rows": rows,
        "top_targets": [
            {
                "A": int(row["A"]),
                "B": int(row["B"]),
                "curve": str(row["curve"]),
                "cover_index": int(row["cover_index"]),
            }
            for row in rows[:10]
        ],
        "boundary": (
            "This is a prioritization table for explicit Sha[2] candidates. "
            "It ranks follow-up targets; it does not prove that any cover has "
            "no rational point."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cover-summary", type=Path, required=True)
    parser.add_argument("--evidence-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = prioritize_residual_covers(
        cover_summary=load_json(args.cover_summary),
        evidence_audit=load_json(args.evidence_audit),
    )
    write_json(args.out, result)
    print(f"wrote residual cover priorities to {args.out}")
    print(f"candidate_cover_total={result['candidate_cover_total']}")
    if result["top_targets"]:
        print(f"top_target={result['top_targets'][0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
