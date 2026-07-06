#!/usr/bin/env python3
"""Probe PARI ell2cover quartics for mixed-closure residual rows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Protocol

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_recheck_mixed_closure_residuals import (  # noqa: E402
    filter_uncertain_rows,
    load_uncertain_rows,
    parse_curve_target,
)


class PariLike(Protocol):
    def ellinit(self, model: list[int]) -> Any: ...

    def ellrank(self, curve: Any, effort: int) -> Any: ...

    def ell2cover(self, curve: Any) -> Any: ...

    def hyperellratpoints(self, quartic: Any, height: int) -> Any: ...


def _as_int(value: Any) -> int:
    return int(str(value))


def _points_as_strings(points: Any) -> list[str]:
    return [str(point) for point in points]


def cover_row(
    row: dict[str, Any],
    *,
    pari: PariLike,
    height: int,
    effort: int,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "A": int(row["A"]),
        "B": int(row["B"]),
        "curve": str(row["curve"]),
        "input_rank": str(row["rank"]),
        "model": row["model"],
    }

    try:
        curve = pari.ellinit([int(value) for value in row["model"]])
        rank_result = pari.ellrank(curve, effort)
        covers = pari.ell2cover(curve)
    except Exception as exc:  # pragma: no cover - exercised through CLI failures
        result["status"] = "pari-error"
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result

    result["status"] = "ok"
    result["ellrank"] = {
        "lower": _as_int(rank_result[0]),
        "upper": _as_int(rank_result[1]),
        "sha2_lower": _as_int(rank_result[2]) if len(rank_result) > 2 else None,
    }

    cover_results: list[dict[str, Any]] = []
    for index, cover in enumerate(covers, start=1):
        quartic = cover[0]
        cover_result: dict[str, Any] = {
            "index": index,
            "quartic": str(quartic),
        }
        try:
            points = pari.hyperellratpoints(quartic, height)
        except Exception as exc:  # pragma: no cover - exercised through CLI failures
            cover_result["status"] = "point-search-error"
            cover_result["error"] = f"{type(exc).__name__}: {exc}"
            cover_result["point_count"] = None
            cover_result["points"] = []
        else:
            cover_result["point_count"] = len(points)
            cover_result["points"] = _points_as_strings(points)
        cover_results.append(cover_result)

    result["cover_count"] = len(cover_results)
    result["covers"] = cover_results
    result["covers_without_points"] = sum(
        1 for cover in cover_results if cover.get("point_count") == 0
    )
    return result


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("results/mixed_closure_rank_summary.json"),
        help="Summary JSON containing uncertain_rank_rows.",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--height", type=int, default=100000)
    parser.add_argument("--effort", type=int, default=1)
    parser.add_argument("--limit", type=int, default=None, help="Only run the first N rows.")
    parser.add_argument(
        "--curve",
        action="append",
        choices=["AA", "AB", "BA", "BB"],
        default=[],
        help="Only run residual rows for this curve. Repeat for several curves.",
    )
    parser.add_argument(
        "--target",
        action="append",
        type=parse_curve_target,
        default=[],
        help="Only run one residual row, formatted as A,B,CURVE. Repeat for several rows.",
    )
    return parser.parse_args()


def main() -> int:
    from cypari2 import Pari

    args = parse_args()
    rows = load_uncertain_rows(args.summary)
    rows = filter_uncertain_rows(rows, curves=args.curve, targets=args.target)
    if args.limit is not None:
        rows = rows[: args.limit]

    pari = Pari()
    results: list[dict[str, Any]] = []
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for index, row in enumerate(rows, start=1):
            result = cover_row(row, pari=pari, height=args.height, effort=args.effort)
            results.append(result)
            handle.write(json.dumps(result, ensure_ascii=True) + "\n")
            handle.flush()
            print(
                f"[{index}/{len(rows)}] "
                f"({result['A']},{result['B']}) {result['curve']} "
                f"status={result['status']} covers_without_points="
                f"{result.get('covers_without_points', 'missing')}",
                flush=True,
            )

    status_counts: dict[str, int] = {}
    no_point_counts: dict[str, int] = {}
    for result in results:
        status = str(result["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
        if "covers_without_points" in result:
            key = str(result["covers_without_points"])
            no_point_counts[key] = no_point_counts.get(key, 0) + 1

    print(f"wrote {len(results)} ell2cover rows to {args.out}")
    print(f"status_counts={dict(sorted(status_counts.items()))}")
    if no_point_counts:
        print(f"covers_without_points_counts={dict(sorted(no_point_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
