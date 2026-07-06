#!/usr/bin/env python3
"""Rank the four closure-aware genus-one quotients for selected pairs.

This is the first concrete experiment suggested by ``tmp.txt``: stop ranking
only the old concordant curve, and also rank the quotients that contain both
``N`` and the closed leg ``M = A + B - N``. With ``--pullback-height``, certified
rank-0 quotients also get a bounded ``hyperellratpoints`` pullback on the
original quartic.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.mixed_closure_curves import (  # noqa: E402
    _ensure_pari,
    classify_quartic_point,
    closure_quotient_polynomials,
    enumerate_quartic_points,
    rank_mixed_closure_curves,
)


def _parse_pair(raw: str) -> tuple[int, int]:
    parts = raw.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("pair must be A,B")
    try:
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError("pair must contain integers") from exc


def _load_pairs_jsonl(path: Path, limit: int | None) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                continue
            row = json.loads(line)
            pairs.append((int(row["A"]), int(row["B"])))
            if limit is not None and len(pairs) >= limit:
                break
    return pairs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair", action="append", type=_parse_pair, default=[])
    parser.add_argument("--pairs-jsonl", type=Path, default=None)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--effort", type=int, default=1)
    parser.add_argument(
        "--pullback-height",
        type=int,
        default=0,
        help=(
            "For certified rank-0 quotients, enumerate affine points on the original "
            "quartic up to this PARI naive height and classify their N values."
        ),
    )
    parser.add_argument(
        "--no-pari",
        action="store_true",
        help="Only emit quartic equations; mark rank rows as pari-unavailable.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pairs: list[tuple[int, int]] = list(args.pair)
    if args.pairs_jsonl is not None:
        pairs.extend(_load_pairs_jsonl(args.pairs_jsonl, args.limit))
    if args.limit is not None:
        pairs = pairs[: args.limit]
    if not pairs:
        print("ERROR: provide --pair or --pairs-jsonl", file=sys.stderr)
        return 2

    pari = None if args.no_pari else _ensure_pari()
    rows = rank_mixed_closure_curves(
        pairs,
        pari=pari,
        effort=args.effort,
        pari_available=not args.no_pari,
    )

    if args.pullback_height > 0 and not args.no_pari:
        curves = {
            (curve.A, curve.B, curve.name): curve
            for pair in pairs
            for curve in closure_quotient_polynomials(*pair)
        }
        for row in rows:
            if (
                row.get("status") == "ok"
                and row.get("rank_lower") == 0
                and row.get("rank_upper") == 0
            ):
                curve = curves[(int(row["A"]), int(row["B"]), str(row["curve"]))]
                points = enumerate_quartic_points(
                    curve,
                    height=args.pullback_height,
                    pari=pari,
                )
                row["point_count"] = len(points)
                row["point_classifications"] = [
                    classify_quartic_point(curve, point) for point in points
                ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")

    status_counts: dict[str, int] = {}
    rank_counts: dict[str, int] = {}
    for row in rows:
        status = str(row["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
        if status == "ok":
            key = f"{row['rank_lower']}/{row['rank_upper']}"
            rank_counts[key] = rank_counts.get(key, 0) + 1

    print(f"wrote {len(rows)} rows for {len(pairs)} pairs to {args.out}")
    print(f"status_counts={dict(sorted(status_counts.items()))}")
    if rank_counts:
        print(f"rank_counts={dict(sorted(rank_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
