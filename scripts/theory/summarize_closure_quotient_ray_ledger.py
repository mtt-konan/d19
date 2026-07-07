#!/usr/bin/env python3
"""Summarize closure-quotient evidence by primitive A:B rays."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This ledger reorganizes existing closure-quotient evidence by primitive "
    "A:B rays and c_+/c_- classes. It does not add new no-point certificates "
    "and does not prove any lambda-family exclusion."
)

LAMBDA_MAINLINE = (
    "Treat closure quotient as a local certificate tool. The next main line is "
    "lambda=A/B family structure: rank-zero, root-number, and 2-cover mechanisms "
    "that exclude whole primitive ratio classes, with remaining cases accepted "
    "only through reviewable no-point certificates."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def _primitive_ray(A: int, B: int) -> tuple[int, int, int]:
    gcd = math.gcd(A, B)
    return A // gcd, B // gcd, gcd


def _c_ratio(A: int, B: int) -> Fraction | None:
    c_minus = abs(A - B)
    if c_minus == 0:
        return None
    return Fraction(A + B, c_minus)


def _row_rank_counts(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        curve = str(row.get("curve", ""))
        if row.get("status") == "ok":
            key = f"{row.get('rank_lower')}/{row.get('rank_upper')}"
        else:
            key = str(row.get("status", "unknown"))
        counts[curve][key] += 1
    return {
        curve: dict(sorted(curve_counts.items()))
        for curve, curve_counts in sorted(counts.items())
    }


def _strict_pairs(rank_summary: dict[str, Any]) -> dict[tuple[int, int], list[str]]:
    return {
        (int(row["A"]), int(row["B"])): [
            str(curve) for curve in row.get("certifying_curves", [])
        ]
        for row in rank_summary.get("strict_excluded_pairs", [])
    }


def _residual_pairs(
    residual_cover_summary: dict[str, Any],
) -> dict[tuple[int, int], list[dict[str, Any]]]:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in residual_cover_summary.get("no_point_cover_rows", []):
        key = (int(row["A"]), int(row["B"]))
        grouped[key].append(
            {
                "curve": str(row["curve"]),
                "evidence_level": str(row.get("evidence_level", "")),
                "no_point_cover_indices": [
                    int(index) for index in row.get("no_point_cover_indices", [])
                ],
                "selmer_gap": int(row.get("selmer_gap", 0)),
            }
        )
    return dict(grouped)


def _pair_status(
    *,
    pair: tuple[int, int],
    strict_pairs: dict[tuple[int, int], list[str]],
    residual_pairs: dict[tuple[int, int], list[dict[str, Any]]],
) -> str:
    if pair in strict_pairs:
        return "strict-local-tool-excludes-observed-pair"
    if pair in residual_pairs:
        return "residual-candidate-not-proof"
    return "observed-not-closed-by-local-tool"


def _coverage_status(status_counts: Counter[str], pair_count: int) -> str:
    strict_count = status_counts["strict-local-tool-excludes-observed-pair"]
    residual_count = status_counts["residual-candidate-not-proof"]
    if strict_count == pair_count:
        return "all-observed-pairs-strict"
    if strict_count:
        return "some-observed-pairs-strict"
    if residual_count:
        return "residual-candidate-open"
    return "observed-open"


def summarize_ray_ledger(
    *,
    rank_rows: list[dict[str, Any]],
    rank_summary: dict[str, Any],
    residual_cover_summary: dict[str, Any],
) -> dict[str, Any]:
    rows_by_pair: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rank_rows:
        rows_by_pair[(int(row["A"]), int(row["B"]))].append(row)

    strict = _strict_pairs(rank_summary)
    residual = _residual_pairs(residual_cover_summary)
    pair_rows: list[dict[str, Any]] = []
    rays: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    classes: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    c_minus_zero_pair_count = 0

    for A, B in sorted(rows_by_pair):
        primitive_A, primitive_B, scale = _primitive_ray(A, B)
        c_plus = A + B
        c_minus = abs(A - B)
        ratio = _c_ratio(A, B)
        if ratio is None:
            c_ratio = "undefined"
            class_key = (primitive_A, primitive_B)
            c_minus_zero_pair_count += 1
        else:
            c_ratio = _fraction_text(ratio)
            class_key = tuple(sorted((primitive_A, primitive_B)))
        pair = (A, B)
        status = _pair_status(pair=pair, strict_pairs=strict, residual_pairs=residual)
        row = {
            "A": A,
            "B": B,
            "scale": scale,
            "primitive_A": primitive_A,
            "primitive_B": primitive_B,
            "lambda": _fraction_text(Fraction(primitive_A, primitive_B)),
            "c_plus": c_plus,
            "c_minus": c_minus,
            "c_ratio": c_ratio,
            "c_ratio_class": f"{class_key[0]}:{class_key[1]}",
            "status": status,
            "certifying_curves": strict.get(pair, []),
            "residual_cover_rows": residual.get(pair, []),
            "rank_counts_by_curve": _row_rank_counts(rows_by_pair[pair]),
        }
        pair_rows.append(row)
        rays[(primitive_A, primitive_B)].append(row)
        classes[class_key].append(row)

    ray_rows: list[dict[str, Any]] = []
    for (primitive_A, primitive_B), pairs in sorted(rays.items()):
        status_counts = Counter(str(pair["status"]) for pair in pairs)
        c_ratio = str(pairs[0]["c_ratio"])
        reciprocal = [primitive_B, primitive_A]
        ray_rows.append(
            {
                "primitive_A": primitive_A,
                "primitive_B": primitive_B,
                "lambda": _fraction_text(Fraction(primitive_A, primitive_B)),
                "reciprocal_ray": reciprocal,
                "c_plus_unit": primitive_A + primitive_B,
                "c_minus_unit": abs(primitive_A - primitive_B),
                "c_ratio": c_ratio,
                "scale_count": len(pairs),
                "scales": [int(pair["scale"]) for pair in pairs],
                "pair_count": len(pairs),
                "status_counts": dict(sorted(status_counts.items())),
                "coverage_status": _coverage_status(status_counts, len(pairs)),
                "observed_pairs": [[int(pair["A"]), int(pair["B"])] for pair in pairs],
            }
        )

    class_rows: list[dict[str, Any]] = []
    for (small, large), pairs in sorted(classes.items()):
        observed = sorted({(int(pair["primitive_A"]), int(pair["primitive_B"])) for pair in pairs})
        status_counts = Counter(str(pair["status"]) for pair in pairs)
        if small == large:
            c_ratio = "undefined"
            possible_oriented_rays = [[small, large]]
        else:
            c_ratio = _fraction_text(Fraction(small + large, large - small))
            possible_oriented_rays = [[small, large], [large, small]]
        class_rows.append(
            {
                "class": f"{small}:{large}",
                "unordered_primitive_ray": [small, large],
                "possible_oriented_rays": possible_oriented_rays,
                "observed_oriented_rays": [[a, b] for a, b in observed],
                "orientation_lost_by_c_ratio": small != large,
                "c_ratio": c_ratio,
                "pair_count": len(pairs),
                "status_counts": dict(sorted(status_counts.items())),
                "coverage_status": _coverage_status(status_counts, len(pairs)),
            }
        )

    pair_status_counts = Counter(str(row["status"]) for row in pair_rows)
    ray_status_counts = Counter(str(row["coverage_status"]) for row in ray_rows)
    class_status_counts = Counter(str(row["coverage_status"]) for row in class_rows)
    return {
        "status": "ok",
        "ready": True,
        "pair_count": len(pair_rows),
        "rank_row_count": len(rank_rows),
        "primitive_ray_count": len(ray_rows),
        "c_ratio_class_count": len(class_rows),
        "c_minus_zero_pair_count": c_minus_zero_pair_count,
        "pair_status_counts": dict(sorted(pair_status_counts.items())),
        "ray_coverage_status_counts": dict(sorted(ray_status_counts.items())),
        "c_ratio_class_coverage_status_counts": dict(
            sorted(class_status_counts.items())
        ),
        "strict_pair_count": pair_status_counts[
            "strict-local-tool-excludes-observed-pair"
        ],
        "strict_ray_count": sum(
            1
            for row in ray_rows
            if row["coverage_status"]
            in {"all-observed-pairs-strict", "some-observed-pairs-strict"}
        ),
        "strict_c_ratio_class_count": sum(
            1
            for row in class_rows
            if row["coverage_status"]
            in {"all-observed-pairs-strict", "some-observed-pairs-strict"}
        ),
        "residual_candidate_pair_count": pair_status_counts[
            "residual-candidate-not-proof"
        ],
        "lambda_mainline": LAMBDA_MAINLINE,
        "coverage_interpretation": (
            "c_+/c_- identifies the unordered primitive ratio class {A:B, B:A}. "
            "It is useful as a ray ledger key, but it is not by itself a "
            "lambda-family exclusion theorem."
        ),
        "pair_rows": pair_rows,
        "ray_rows": ray_rows,
        "c_ratio_class_rows": class_rows,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank-jsonl", type=Path, action="append", required=True)
    parser.add_argument("--rank-summary", type=Path, required=True)
    parser.add_argument("--residual-cover-summary", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ledger = summarize_ray_ledger(
        rank_rows=load_jsonl(args.rank_jsonl),
        rank_summary=load_json(args.rank_summary),
        residual_cover_summary=load_json(args.residual_cover_summary),
    )
    write_json(args.out, ledger)
    print(f"wrote closure quotient ray ledger to {args.out}")
    print(f"status={ledger['status']}")
    print(f"pair_count={ledger['pair_count']}")
    print(f"primitive_ray_count={ledger['primitive_ray_count']}")
    print(f"c_ratio_class_count={ledger['c_ratio_class_count']}")
    print(f"strict_c_ratio_class_count={ledger['strict_c_ratio_class_count']}")
    if args.strict and ledger["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
