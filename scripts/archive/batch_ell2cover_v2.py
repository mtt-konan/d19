#!/usr/bin/env python3
"""Resumable, timeout-safe ell2cover scanner for the sha2>=2 hard_case subset.

Reads ``results/sha2_scan_hard_cases.jsonl`` (produced by
``batch_sha2_scan_v2.py``), filters to pairs with ``sha2_lower >= 2``, and
fans out one subprocess per pair to ``ell2cover_worker.py``. Parent enforces
a hard timeout (default 60s) so a pathological ell2cover call cannot block
the whole sweep.

Results stream into JSONL with per-line flush. Reruns skip pairs that
already appear in the output, so the scan is fully resumable.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
WORKER = ROOT / "scripts" / "ell2cover_worker.py"


def load_done(out_path: Path) -> set[tuple[int, int]]:
    if not out_path.exists():
        return set()
    done: set[tuple[int, int]] = set()
    with open(out_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "A" in row and "B" in row:
                done.add((int(row["A"]), int(row["B"])))
    return done


def load_sha2_pairs(jsonl_path: Path, min_sha2: int) -> list[tuple[int, int, int]]:
    """Return (A, B, sha2_lower) for pairs with sha2_lower >= min_sha2."""
    pairs: list[tuple[int, int, int]] = []
    with open(jsonl_path, encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            s_lo = row.get("sha2_lower")
            if isinstance(s_lo, int) and s_lo >= min_sha2:
                pairs.append((int(row["A"]), int(row["B"]), s_lo))
    pairs.sort()
    return pairs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--sha2-jsonl",
        default="results/sha2_scan_hard_cases.jsonl",
        help="Input JSONL from batch_sha2_scan_v2 (default: %(default)s)",
    )
    ap.add_argument(
        "--out",
        default="results/ell2cover_sha2_cases.jsonl",
        help="Output JSONL path (default: %(default)s)",
    )
    ap.add_argument("--min-sha2", type=int, default=2)
    ap.add_argument(
        "--height", type=int, default=10000,
        help="hyperellratpoints naive height bound (default: 10000)",
    )
    ap.add_argument(
        "--timeout", type=float, default=60.0,
        help="Hard per-pair wall-clock cap in seconds (default: 60)",
    )
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--progress-every", type=int, default=20)
    args = ap.parse_args()

    sha2_path = Path(args.sha2_jsonl)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not sha2_path.exists():
        print(f"ERROR: {sha2_path} not found. Run batch_sha2_scan_v2.py first.")
        return 1

    all_pairs = load_sha2_pairs(sha2_path, args.min_sha2)
    if args.limit:
        all_pairs = all_pairs[: args.limit]
    done = load_done(out_path)
    todo = [(a, b, s) for a, b, s in all_pairs if (a, b) not in done]

    print(f"sha2 pairs (>= {args.min_sha2}): {len(all_pairs)}  "
          f"done: {len(done)}  todo: {len(todo)}")
    print(f"h={args.height}  timeout={args.timeout}s  out={out_path}")
    print()

    if not todo:
        print("Nothing to do.")
        return 0

    n_timeout = 0
    n_error = 0
    n_with_obstruction = 0  # at least one cover without rational point
    n_all_have_pt = 0
    cover_count_hist: dict[int, int] = {}
    obstr_count_hist: dict[int, int] = {}
    t_start = time.perf_counter()

    fh = open(out_path, "a", encoding="utf-8")
    try:
        for idx, (A, B, s_lo) in enumerate(todo, 1):
            cmd = ["uv", "run", "--quiet", "python", str(WORKER),
                   str(A), str(B), str(args.height)]
            t0 = time.perf_counter()
            try:
                proc = subprocess.run(
                    cmd, cwd=str(ROOT),
                    capture_output=True, text=True,
                    timeout=args.timeout,
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    out = json.loads(proc.stdout.strip().splitlines()[-1])
                    out.setdefault("sha2_lower_input", s_lo)
                else:
                    out = {
                        "A": A, "B": B, "sha2_lower_input": s_lo,
                        "error": f"returncode={proc.returncode}: "
                                 f"{proc.stderr[:200]}",
                        "time_total_s": round(time.perf_counter() - t0, 3),
                    }
                    n_error += 1
            except subprocess.TimeoutExpired:
                out = {
                    "A": A, "B": B, "sha2_lower_input": s_lo,
                    "error": "TIMEOUT",
                    "time_total_s": round(time.perf_counter() - t0, 3),
                }
                n_timeout += 1

            fh.write(json.dumps(out) + "\n")
            fh.flush()

            n_cov = out.get("n_covers")
            n_no_pt = out.get("n_without_pt")
            if isinstance(n_cov, int):
                cover_count_hist[n_cov] = cover_count_hist.get(n_cov, 0) + 1
            if isinstance(n_no_pt, int):
                obstr_count_hist[n_no_pt] = obstr_count_hist.get(n_no_pt, 0) + 1
                if n_no_pt > 0:
                    n_with_obstruction += 1
                else:
                    n_all_have_pt += 1

            if idx % args.progress_every == 0 or idx == len(todo):
                elapsed = time.perf_counter() - t_start
                rate = idx / elapsed
                eta = (len(todo) - idx) / rate if rate > 0 else float("inf")
                print(
                    f"[{idx:>4}/{len(todo)}] {elapsed:>5.0f}s  "
                    f"{rate:>5.2f}/s  ETA {eta:>5.0f}s  "
                    f"obstr: {n_with_obstruction}  all_pt: {n_all_have_pt}  "
                    f"timeout: {n_timeout}  err: {n_error}",
                    flush=True,
                )
    finally:
        fh.close()

    elapsed = time.perf_counter() - t_start
    print()
    print("=" * 72)
    print(f"Done. {len(todo)} pairs in {elapsed:.0f}s.")
    print(f"  with >=1 cover-without-pt (Sha[2] candidate): {n_with_obstruction}")
    print(f"  all covers have a rat pt (h<={args.height}):  {n_all_have_pt}")
    print(f"  TIMEOUT: {n_timeout}")
    print(f"  ERROR:   {n_error}")
    print(f"  n_covers distribution:")
    for k in sorted(cover_count_hist):
        print(f"    n_covers={k:>2}: {cover_count_hist[k]:>4}")
    print(f"  n_without_pt distribution:")
    for k in sorted(obstr_count_hist):
        print(f"    n_without_pt={k:>2}: {obstr_count_hist[k]:>4}")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
