#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.candidate_generators import (  # noqa: E402
    CandidateGeneratorResult,
    run_generator_benchmark,
    run_named_generator_benchmark,
)

GENERATOR_NAMES = ("all_coprime", "safe_coprime", "multi_n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark direct integer-domain candidate generators"
    )
    _ = parser.add_argument("--max-hyp", type=int, default=2000)
    _ = parser.add_argument(
        "--only",
        choices=GENERATOR_NAMES,
        default=None,
        help="Run only one generator",
    )
    _ = parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Write benchmark rows as JSON",
    )
    return parser.parse_args()


def _format_table(rows: tuple[CandidateGeneratorResult, ...]) -> str:
    lines = [
        "name          max_hyp      pairs  elapsed_s  carries_N  min_k  max_k",
        "------------  -------  ---------  ---------  ---------  -----  -----",
    ]
    for row in rows:
        min_k = "-" if row.min_n_count is None else str(row.min_n_count)
        max_k = "-" if row.max_n_count is None else str(row.max_n_count)
        line = "".join(
            (
                f"{row.name:<12}  ",
                f"{row.max_hyp:>7}  ",
                f"{row.pair_count:>9}  ",
                f"{row.elapsed_s:>9.3f}  ",
                f"{row.carries_concordant_n!s:>9}  ",
                f"{min_k:>5}  ",
                f"{max_k:>5}",
            )
        )
        lines.append(line)
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    max_hyp = cast(int, args.max_hyp)
    only = cast(str | None, args.only)
    json_out = cast(Path | None, args.json_out)

    rows = (
        (run_named_generator_benchmark(only, max_hyp),)
        if only is not None
        else run_generator_benchmark(max_hyp)
    )
    print(_format_table(rows))

    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        _ = json_out.write_text(
            json.dumps([row.to_json_dict() for row in rows], indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"json: {json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
