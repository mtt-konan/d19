"""Scan exact fixed-ratio ``A = kB`` concordant-N ratios.

This script uses the exact factor-decomposition path, not residue-only modular
witnesses. It is meant to produce proof leads: for each fixed ``k``, collect
the true ratios ``N/B`` seen up to ``B <= max_b`` and check whether those
ratios already satisfy any full-plane closure relation after dividing by ``B``.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from rational_distance.concordant.fixed_ratio_exact import (
    FixedRatioHit,
    FixedRatioRatioSummary,
    collect_fixed_ratio_ratios,
)


def _fraction_to_str(value) -> str:
    return str(value)


def hit_to_json_dict(hit: FixedRatioHit) -> dict[str, Any]:
    return {
        "r1": _fraction_to_str(hit.r1),
        "r2": _fraction_to_str(hit.r2),
        "relation": hit.relation,
        "centerline": hit.centerline,
    }


def summary_to_json_dict(summary: FixedRatioRatioSummary) -> dict[str, Any]:
    return {
        "k": summary.k,
        "max_b": summary.max_b,
        "ratio_count": summary.ratio_count,
        "ratios": [_fraction_to_str(ratio) for ratio in summary.ratios],
        "b_with_n_count": summary.b_with_n_count,
        "total_n_count": summary.total_n_count,
        "noncenter_hits": [hit_to_json_dict(hit) for hit in summary.noncenter_hits],
        "centerline_hits": [hit_to_json_dict(hit) for hit in summary.centerline_hits],
    }


def scan_fixed_ratios(k_min: int, k_max: int, max_b: int) -> list[FixedRatioRatioSummary]:
    if k_min < 1 or k_max < k_min:
        raise ValueError("expected 1 <= k_min <= k_max")
    if max_b < 1:
        raise ValueError("max_b must be positive")
    return [collect_fixed_ratio_ratios(k, max_b) for k in range(k_min, k_max + 1)]


def write_jsonl(path: Path, rows: Sequence[FixedRatioRatioSummary]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(summary_to_json_dict(row), sort_keys=True) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k-min", type=int, default=1)
    parser.add_argument("--k-max", type=int, default=30)
    parser.add_argument("--max-b", type=int, default=200)
    parser.add_argument("--jsonl-out", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = scan_fixed_ratios(args.k_min, args.k_max, args.max_b)
    if args.jsonl_out is not None:
        write_jsonl(args.jsonl_out, rows)

    for row in rows:
        if row.ratio_count == 0 and not row.noncenter_hits and not row.centerline_hits:
            continue
        payload = summary_to_json_dict(row)
        print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
