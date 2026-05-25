#!/usr/bin/env python3
"""Lookup a pair in the authoritative max_hyp=10000 multi-N dataset."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lookup a pair in multi_concordant_N_max10000.jsonl"
    )
    _ = parser.add_argument("A", type=int)
    _ = parser.add_argument("B", type=int)
    _ = parser.add_argument(
        "--dataset",
        type=Path,
        default=ROOT / "results" / "multi_concordant_N_max10000.jsonl",
    )
    return parser.parse_args()


def main() -> int:
    from rational_distance.results.multi_concordant import lookup_multi_concordant_pair

    args = parse_args()
    A = cast(int, args.A)
    B = cast(int, args.B)
    dataset = cast(Path, args.dataset)
    row = lookup_multi_concordant_pair(A, B, dataset_path=dataset)
    if row is None:
        print("not found")
        return 1
    print(json.dumps(row.__dict__, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
