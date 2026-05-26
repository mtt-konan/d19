#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.parallel import ParallelConfig
from scripts.partner_full_bfs import _compute_ns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "results" / "multi_concordant_N_max2000_fast.jsonl",
    )
    _ = parser.add_argument("--pairs", type=int, default=160)
    _ = parser.add_argument("--batch-size", type=int, default=16)
    _ = parser.add_argument("--workers", type=int, default=4)
    _ = parser.add_argument("--chunksize", type=int, default=16)
    _ = parser.add_argument("--trials", type=int, default=3)
    return parser.parse_args()


def load_pairs(path: Path, n_pairs: int) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            pairs.append((int(row["A"]), int(row["B"])))
            if len(pairs) >= n_pairs:
                break
    if not pairs:
        raise SystemExit(f"no pairs found in {path}")
    return pairs


def make_batches(pairs: list[tuple[int, int]], batch_size: int) -> list[list[tuple[int, int]]]:
    return [pairs[i:i + batch_size] for i in range(0, len(pairs), batch_size)]


def bench_cfg_map(cfg: ParallelConfig, batches: list[list[tuple[int, int]]]) -> tuple[float, int]:
    t0 = time.perf_counter()
    total_ns = 0
    for batch in batches:
        results = cfg.map(_compute_ns, batch)
        total_ns += sum(len(ns) for _, ns in results)
    return time.perf_counter() - t0, total_ns


def bench_executor(cfg: ParallelConfig, batches: list[list[tuple[int, int]]]) -> tuple[float, int]:
    t0 = time.perf_counter()
    total_ns = 0
    with cfg.executor() as executor:
        for batch in batches:
            results = executor.map(_compute_ns, batch)
            total_ns += sum(len(ns) for _, ns in results)
    return time.perf_counter() - t0, total_ns


def main() -> int:
    args = parse_args()
    pairs = load_pairs(args.data, args.pairs)
    batches = make_batches(pairs, args.batch_size)
    cfg = ParallelConfig(workers=args.workers, chunksize=args.chunksize)

    print(
        f"data={args.data.name} pairs={len(pairs)} batches={len(batches)} "
        f"batch_size={args.batch_size} workers={args.workers} chunksize={args.chunksize}"
    )

    warmup_dt, warmup_total = bench_cfg_map(cfg, batches[:1])
    print(f"warmup cfg.map: {warmup_dt:.3f}s total_ns={warmup_total}")

    cfg_times: list[float] = []
    executor_times: list[float] = []
    expected_total: int | None = None

    for trial in range(1, args.trials + 1):
        cfg_dt, cfg_total = bench_cfg_map(cfg, batches)
        executor_dt, executor_total = bench_executor(cfg, batches)
        if expected_total is None:
            expected_total = cfg_total
        if cfg_total != executor_total or cfg_total != expected_total:
            raise SystemExit(
                f"mismatched totals: cfg={cfg_total}, executor={executor_total}, expected={expected_total}"
            )
        cfg_times.append(cfg_dt)
        executor_times.append(executor_dt)
        print(
            f"trial {trial}: cfg.map={cfg_dt:.3f}s executor={executor_dt:.3f}s "
            f"speedup=x{cfg_dt / executor_dt:.2f}"
        )

    cfg_mean = statistics.mean(cfg_times)
    executor_mean = statistics.mean(executor_times)
    print()
    print(f"cfg.map mean:  {cfg_mean:.3f}s  runs={[round(x, 3) for x in cfg_times]}")
    print(f"executor mean: {executor_mean:.3f}s  runs={[round(x, 3) for x in executor_times]}")
    print(f"speedup mean:  x{cfg_mean / executor_mean:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
