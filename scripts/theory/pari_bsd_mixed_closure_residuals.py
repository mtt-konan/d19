#!/usr/bin/env python3
"""Collect BSD-conditional PARI diagnostics for mixed-closure residual rows."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_recheck_mixed_closure_residuals import (  # noqa: E402
    filter_uncertain_rows,
    load_uncertain_rows,
    parse_curve_target,
)

Run = Callable[..., subprocess.CompletedProcess[str]]

MARKER = "PARI_BSD_JSON "


def _tail_lines(text: str | bytes, *, limit: int = 20) -> list[str]:
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    return text.splitlines()[-limit:]


def _pari_program(model: list[int], stack_bytes: int) -> str:
    return f"""
import json
from cypari2 import Pari

pari = Pari()
pari.allocatemem({stack_bytes})
E = pari.ellinit({json.dumps(model)})
rank = pari.ellrank(E, 1)
analytic = pari.ellanalyticrank(E)
payload = {{
    "root_number": int(pari.ellrootno(E)),
    "ellrank_lower": int(rank[0]),
    "ellrank_upper": int(rank[1]),
    "ellrank_sha2_lower": int(rank[2]) if len(rank) > 2 else None,
    "analytic_rank": int(analytic[0]),
    "analytic_leading_value": str(analytic[1]),
    "bsd_factor": str(pari.ellbsd(E)),
}}
print({MARKER!r} + json.dumps(payload, separators=(",", ":")), flush=True)
"""


def _parse_marker(stdout: str) -> dict[str, Any] | None:
    for line in stdout.splitlines():
        if line.startswith(MARKER):
            return json.loads(line[len(MARKER) :])
    return None


def _base_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "A": int(row["A"]),
        "B": int(row["B"]),
        "curve": str(row["curve"]),
        "input_rank": str(row["rank"]),
        "model": row["model"],
    }


def _result_from_completed(
    row: dict[str, Any],
    completed: subprocess.CompletedProcess[str],
) -> dict[str, Any]:
    result = _base_row(row)
    result["status"] = "ok" if completed.returncode == 0 else "pari-error"

    marker = _parse_marker(completed.stdout)
    if marker is not None:
        result.update(marker)
        result["evidence_level"] = "bsd-conditional-diagnostic"
    else:
        result["evidence_level"] = "no-bsd-diagnostic"

    result["stdout_tail"] = _tail_lines(completed.stdout)
    result["stderr_tail"] = _tail_lines(completed.stderr)
    return result


def diagnose_rows(
    rows: list[dict[str, Any]],
    *,
    python_executable: str,
    timeout_seconds: int,
    stack_bytes: int,
    run: Run = subprocess.run,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in rows:
        cmd = [
            python_executable,
            "-c",
            _pari_program([int(value) for value in row["model"]], stack_bytes),
        ]
        try:
            completed = run(
                cmd,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            result = _base_row(row)
            result.update(
                {
                    "status": "timeout",
                    "timeout_seconds": timeout_seconds,
                    "evidence_level": "no-bsd-diagnostic",
                    "stdout_tail": _tail_lines(exc.stdout or ""),
                    "stderr_tail": _tail_lines(exc.stderr or ""),
                }
            )
            results.append(result)
            continue

        results.append(_result_from_completed(row, completed))
    return results


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
    parser.add_argument("--python", default=sys.executable, help="Python with cypari2.")
    parser.add_argument("--timeout", type=int, default=30, help="Seconds per curve.")
    parser.add_argument(
        "--stack-bytes",
        type=int,
        default=268435456,
        help="PARI stack bytes for each child process.",
    )
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
    rows = load_uncertain_rows(args.summary)
    rows = filter_uncertain_rows(rows, curves=args.curve, targets=args.target)
    if args.limit is not None:
        rows = rows[: args.limit]

    results: list[dict[str, Any]] = []
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for index, row in enumerate(rows, start=1):
            result = diagnose_rows(
                [row],
                python_executable=args.python,
                timeout_seconds=args.timeout,
                stack_bytes=args.stack_bytes,
            )[0]
            results.append(result)
            handle.write(json.dumps(result, ensure_ascii=True) + "\n")
            handle.flush()
            print(
                f"[{index}/{len(rows)}] "
                f"({result['A']},{result['B']}) {result['curve']} "
                f"status={result['status']} analytic_rank="
                f"{result.get('analytic_rank', 'missing')}",
                flush=True,
            )

    status_counts: dict[str, int] = {}
    analytic_rank_counts: dict[str, int] = {}
    for result in results:
        status = str(result["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
        if "analytic_rank" in result:
            key = str(result["analytic_rank"])
            analytic_rank_counts[key] = analytic_rank_counts.get(key, 0) + 1

    print(f"wrote {len(results)} BSD diagnostic rows to {args.out}")
    print(f"status_counts={dict(sorted(status_counts.items()))}")
    if analytic_rank_counts:
        print(f"analytic_rank_counts={dict(sorted(analytic_rank_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
