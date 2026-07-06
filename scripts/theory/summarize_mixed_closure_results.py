#!/usr/bin/env python3
"""Summarize mixed closure quotient rank/certificate JSONL results."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts: Counter[str] = Counter()
    rank_counts: Counter[str] = Counter()
    rank_counts_by_curve: dict[str, Counter[str]] = defaultdict(Counter)
    affine_preimage_counts: Counter[str] = Counter()
    uncertain_rank_rows: list[dict[str, Any]] = []
    strict_excluded_pairs: dict[tuple[int, int], set[str]] = defaultdict(set)
    rank0_torsion_certificates = 0
    certified_no_full_closed_square = 0
    certified_all_midpoint = 0

    for row in rows:
        status = str(row.get("status", "missing"))
        status_counts[status] += 1

        curve = str(row.get("curve", "missing"))
        if status == "ok":
            rank = f"{row['rank_lower']}/{row['rank_upper']}"
            rank_counts[rank] += 1
            rank_counts_by_curve[curve][rank] += 1
            if row["rank_lower"] != row["rank_upper"]:
                uncertain_rank_rows.append(
                    {
                        "A": int(row["A"]),
                        "B": int(row["B"]),
                        "curve": curve,
                        "rank": rank,
                    }
                )

        certificate = row.get("rank0_torsion_certificate")
        if isinstance(certificate, dict) and certificate.get("status") == "certified":
            rank0_torsion_certificates += 1
            affine_preimage_counts[str(certificate["affine_preimage_count"])] += 1
            if certificate.get("certifies_no_full_closed_square"):
                certified_no_full_closed_square += 1
                strict_excluded_pairs[(int(row["A"]), int(row["B"]))].add(curve)
            if certificate.get("all_affine_preimages_are_midpoints"):
                certified_all_midpoint += 1

    strict_excluded_pair_rows = [
        {
            "A": pair[0],
            "B": pair[1],
            "certifying_curves": sorted(curves),
        }
        for pair, curves in sorted(strict_excluded_pairs.items())
    ]

    return {
        "rows": len(rows),
        "status_counts": dict(sorted(status_counts.items())),
        "rank_counts": dict(sorted(rank_counts.items())),
        "rank_counts_by_curve": {
            curve: dict(sorted(counts.items()))
            for curve, counts in sorted(rank_counts_by_curve.items())
        },
        "rank0_torsion_certificates": rank0_torsion_certificates,
        "certified_no_full_closed_square": certified_no_full_closed_square,
        "certified_all_midpoint": certified_all_midpoint,
        "affine_preimage_counts": dict(sorted(affine_preimage_counts.items())),
        "strict_excluded_pair_count": len(strict_excluded_pair_rows),
        "strict_excluded_pairs": strict_excluded_pair_rows,
        "uncertain_rank_rows": uncertain_rank_rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        action="append",
        required=True,
        help="Mixed closure rank JSONL file. Repeat to merge datasets.",
    )
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows: list[dict[str, Any]] = []
    for path in args.input:
        rows.extend(_load_jsonl(path))

    summary = summarize_rows(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote summary for {summary['rows']} rows to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
