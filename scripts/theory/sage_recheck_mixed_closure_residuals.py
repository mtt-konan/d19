#!/usr/bin/env python3
"""Recheck mixed-closure residual rank bounds with Sage/eclib.

The input is the JSON summary produced by
``summarize_mixed_closure_results.py``.  This script only attacks the
``uncertain_rank_rows`` slice: rows where PARI reported a rank interval such as
``0/2`` or ``1/3``.  Each row is run in a separate Sage subprocess so a hard
curve can time out without blocking the whole batch.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections.abc import Callable
from pathlib import Path
from time import perf_counter
from typing import Any

Run = Callable[..., subprocess.CompletedProcess[str]]
Clock = Callable[[], float]
CurveTarget = tuple[int, int, str]

MARKER = "SAGE_RECHECK_JSON "


def _tail_lines(text: str | bytes, *, limit: int = 20) -> list[str]:
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    lines = text.splitlines()
    return lines[-limit:]


def _sage_program(model: list[int], second_limits: list[int]) -> str:
    return f"""
import json
from sage.all import EllipticCurve

model = {json.dumps(model)}
second_limits = {json.dumps(second_limits)}


def emit(payload):
    print({MARKER!r} + json.dumps(payload, separators=(",", ":")), flush=True)


E = EllipticCurve(model)
bounds = E.rank_bounds()
emit({{"phase": "initial", "rank_bounds": [int(bounds[0]), int(bounds[1])]}})

for second_limit in second_limits:
    # configured two_descent(second_limit={second_limits[0] if second_limits else "none"})
    E.two_descent(second_limit=second_limit)
    bounds = E.rank_bounds()
    emit(
        {{
            "phase": "two_descent",
            "second_limit": int(second_limit),
            "rank_bounds": [int(bounds[0]), int(bounds[1])],
        }}
    )
"""


def _parse_marker_rows(stdout: str) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        if line.startswith(MARKER):
            parsed.append(json.loads(line[len(MARKER) :]))
    return parsed


def parse_curve_target(raw: str) -> CurveTarget:
    parts = [part.strip() for part in raw.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("target must be A,B,CURVE")
    try:
        a_value = int(parts[0])
        b_value = int(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("target A and B must be integers") from exc

    curve = parts[2].upper()
    if curve not in {"AA", "AB", "BA", "BB"}:
        raise argparse.ArgumentTypeError("target curve must be one of AA, AB, BA, BB")
    return a_value, b_value, curve


def filter_uncertain_rows(
    rows: list[dict[str, Any]],
    *,
    curves: list[str] | None = None,
    targets: list[CurveTarget] | None = None,
) -> list[dict[str, Any]]:
    allowed_curves = {curve.upper() for curve in curves or []}
    allowed_targets = set(targets or [])

    filtered: list[dict[str, Any]] = []
    for row in rows:
        row_key = (int(row["A"]), int(row["B"]), str(row["curve"]).upper())
        if allowed_curves and row_key[2] not in allowed_curves:
            continue
        if allowed_targets and row_key not in allowed_targets:
            continue
        filtered.append(row)
    return filtered


def _result_from_completed(
    row: dict[str, Any],
    completed: subprocess.CompletedProcess[str],
) -> dict[str, Any]:
    markers = _parse_marker_rows(completed.stdout)
    initial_rank_bounds = None
    limits: list[dict[str, Any]] = []
    final_rank_bounds = None

    for marker in markers:
        phase = marker.get("phase")
        if phase == "initial":
            initial_rank_bounds = marker.get("rank_bounds")
            final_rank_bounds = marker.get("rank_bounds")
        elif phase == "two_descent":
            limits.append(
                {
                    "second_limit": marker["second_limit"],
                    "rank_bounds": marker["rank_bounds"],
                }
            )
            final_rank_bounds = marker.get("rank_bounds")

    status = "ok" if completed.returncode == 0 else "sage-error"
    return {
        "A": int(row["A"]),
        "B": int(row["B"]),
        "curve": str(row["curve"]),
        "input_rank": str(row["rank"]),
        "model": row["model"],
        "status": status,
        "returncode": completed.returncode,
        "initial_rank_bounds": initial_rank_bounds,
        "final_rank_bounds": final_rank_bounds,
        "limits": limits,
        "stdout_tail": _tail_lines(completed.stdout),
        "stderr_tail": _tail_lines(completed.stderr),
    }


def recheck_rows(
    rows: list[dict[str, Any]],
    *,
    sage_executable: str,
    second_limits: list[int],
    timeout_seconds: int,
    run: Run = subprocess.run,
    clock: Clock = perf_counter,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in rows:
        model = [int(value) for value in row["model"]]
        cmd = [
            sage_executable,
            "-python",
            "-c",
            _sage_program(model, second_limits),
        ]
        started_at = clock()
        try:
            completed = run(
                cmd,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            results.append(
                {
                    "A": int(row["A"]),
                    "B": int(row["B"]),
                    "curve": str(row["curve"]),
                    "input_rank": str(row["rank"]),
                    "model": row["model"],
                    "status": "timeout",
                    "timeout_seconds": timeout_seconds,
                    "elapsed_seconds": round(clock() - started_at, 6),
                    "stdout_tail": _tail_lines(exc.stdout or ""),
                    "stderr_tail": _tail_lines(exc.stderr or ""),
                }
            )
            continue

        result = _result_from_completed(row, completed)
        result["elapsed_seconds"] = round(clock() - started_at, 6)
        results.append(result)
    return results


def load_uncertain_rows(summary_path: Path, *, limit: int | None = None) -> list[dict[str, Any]]:
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(summary["uncertain_rank_rows"])
    if limit is not None:
        rows = rows[:limit]
    return rows


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
    parser.add_argument("--sage", default="sage", help="Sage executable.")
    parser.add_argument(
        "--second-limit",
        type=int,
        action="append",
        dest="second_limits",
        default=[],
        help="Sage two_descent(second_limit=N). Repeat to run several limits.",
    )
    parser.add_argument("--timeout", type=int, default=300, help="Seconds per curve.")
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
    args = parse_args()
    second_limits = args.second_limits or [13]
    rows = load_uncertain_rows(args.summary)
    rows = filter_uncertain_rows(rows, curves=args.curve, targets=args.target)
    if args.limit is not None:
        rows = rows[: args.limit]
    results: list[dict[str, Any]] = []

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for index, row in enumerate(rows, start=1):
            result = recheck_rows(
                [row],
                sage_executable=args.sage,
                second_limits=second_limits,
                timeout_seconds=args.timeout,
            )[0]
            results.append(result)
            handle.write(json.dumps(result, ensure_ascii=True) + "\n")
            handle.flush()

            bounds = result.get("final_rank_bounds")
            if isinstance(bounds, list) and len(bounds) == 2:
                final_rank = f"{bounds[0]}/{bounds[1]}"
            else:
                final_rank = "missing"
            print(
                f"[{index}/{len(rows)}] "
                f"({result['A']},{result['B']}) {result['curve']} "
                f"status={result['status']} final={final_rank} "
                f"elapsed={result['elapsed_seconds']}s",
                flush=True,
            )

    status_counts: dict[str, int] = {}
    final_rank_counts: dict[str, int] = {}
    for result in results:
        status = str(result["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
        bounds = result.get("final_rank_bounds")
        if isinstance(bounds, list) and len(bounds) == 2:
            key = f"{bounds[0]}/{bounds[1]}"
            final_rank_counts[key] = final_rank_counts.get(key, 0) + 1

    print(f"wrote {len(results)} Sage recheck rows to {args.out}")
    print(f"status_counts={dict(sorted(status_counts.items()))}")
    if final_rank_counts:
        print(f"final_rank_counts={dict(sorted(final_rank_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
