#!/usr/bin/env python3
"""Resumable, timeout-safe batch sha2 scanner.

For each hard_case (A, B) in proof_status.db, spawn a fresh
``sha2_worker.py`` subprocess running PARI ``ellrank``. The parent
enforces a hard timeout (default 15s) via ``subprocess.run(timeout=...)``
so a single pathological pair cannot block the whole sweep.

Results stream into a JSONL file with per-line flush. Reruns skip
pairs that already appear in the output, so the scan is fully
resumable after Ctrl-C / OOM / process-kill.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
WORKER = ROOT / "scripts" / "sha2_worker.py"


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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default="results/proof_status.db")
    ap.add_argument("--out", default="results/sha2_scan_hard_cases.jsonl")
    ap.add_argument("--effort", type=int, default=1)
    ap.add_argument("--timeout", type=float, default=15.0,
                    help="Hard timeout per pair in seconds (default 15)")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--progress-every", type=int, default=50)
    args = ap.parse_args()

    db_path = Path(args.db)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    query = ("SELECT A, B FROM pair_proof_status WHERE status='hard_case' "
             "ORDER BY A, B")
    if args.limit:
        query += f" LIMIT {args.limit}"
    rows = conn.execute(query).fetchall()
    all_pairs = [(int(r["A"]), int(r["B"])) for r in rows]
    conn.close()

    done = load_done(out_path)
    todo = [p for p in all_pairs if p not in done]
    print(f"Total hard_case: {len(all_pairs)}  done: {len(done)}  todo: {len(todo)}")
    print(f"Effort={args.effort}  timeout={args.timeout}s  out={out_path}")
    print()

    if not todo:
        print("Nothing to do. All pairs already scanned.")
        return 0

    n_sha2_pos = 0
    n_timeout = 0
    n_error = 0
    rank_hist: dict[int, int] = {}
    sha2_hist: dict[int, int] = {}
    t_start = time.perf_counter()

    fh = open(out_path, "a", encoding="utf-8")
    try:
        for idx, (A, B) in enumerate(todo, 1):
            cmd = ["uv", "run", "--quiet", "python", str(WORKER),
                   str(A), str(B), str(args.effort)]
            t0 = time.perf_counter()
            try:
                proc = subprocess.run(
                    cmd,
                    cwd=str(ROOT),
                    capture_output=True,
                    text=True,
                    timeout=args.timeout,
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    out = json.loads(proc.stdout.strip().splitlines()[-1])
                else:
                    out = {
                        "A": A, "B": B,
                        "rank_lower": None, "rank_upper": None,
                        "sha2_lower": None,
                        "error": f"returncode={proc.returncode}: "
                                 f"{proc.stderr[:200]}",
                        "time_s": round(time.perf_counter() - t0, 3),
                    }
                    n_error += 1
            except subprocess.TimeoutExpired:
                out = {
                    "A": A, "B": B,
                    "rank_lower": None, "rank_upper": None,
                    "sha2_lower": None,
                    "error": "TIMEOUT",
                    "time_s": round(time.perf_counter() - t0, 3),
                }
                n_timeout += 1

            fh.write(json.dumps(out) + "\n")
            fh.flush()

            r_lo = out.get("rank_lower")
            s_lo = out.get("sha2_lower")
            if isinstance(r_lo, int):
                rank_hist[r_lo] = rank_hist.get(r_lo, 0) + 1
            if isinstance(s_lo, int):
                sha2_hist[s_lo] = sha2_hist.get(s_lo, 0) + 1
                if s_lo > 0:
                    n_sha2_pos += 1

            if idx % args.progress_every == 0 or idx == len(todo):
                elapsed = time.perf_counter() - t_start
                rate = idx / elapsed
                eta = (len(todo) - idx) / rate if rate > 0 else float("inf")
                print(
                    f"[{idx:>5}/{len(todo)}] {elapsed:>5.0f}s  "
                    f"{rate:>5.2f}/s  ETA {eta:>5.0f}s  "
                    f"sha2>0: {n_sha2_pos}  timeout: {n_timeout}  "
                    f"err: {n_error}",
                    flush=True,
                )
    finally:
        fh.close()

    elapsed = time.perf_counter() - t_start
    print()
    print("=" * 72)
    print(f"Done. {len(todo)} pairs in {elapsed:.0f}s.")
    print(f"  rank_lower distribution:")
    for r in sorted(rank_hist):
        print(f"    rank={r:>2}: {rank_hist[r]:>5}")
    print(f"  sha2_lower distribution:")
    for s in sorted(sha2_hist):
        print(f"    sha2={s:>2}: {sha2_hist[s]:>5}")
    print(f"  TIMEOUT: {n_timeout}")
    print(f"  ERROR:   {n_error}")
    print(f"  sha2>=2: {n_sha2_pos}")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
