#!/usr/bin/env python3
"""Collect cheap Sage diagnostics for mixed-closure residual rank rows."""

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

MARKER = "SAGE_DIAG_JSON "


def _tail_lines(text: str | bytes, *, limit: int = 20) -> list[str]:
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    return text.splitlines()[-limit:]


def _sage_program(model: list[int], analytic_rank_algorithms: list[str]) -> str:
    return f"""
import json
from sage.all import EllipticCurve

model = {json.dumps(model)}
analytic_rank_algorithms = {json.dumps(analytic_rank_algorithms)}


def torsion_two_dimension(invariants):
    return sum(1 for value in invariants if int(value) % 2 == 0)


E = EllipticCurve(model)
torsion = E.torsion_subgroup()
invariants = [int(value) for value in torsion.invariants()]
bounds = E.rank_bounds()
payload = {{
    "rank_bounds": [int(bounds[0]), int(bounds[1])],
    "selmer_rank_pari": int(E.selmer_rank()),
    "selmer_rank_mwrank": int(E.selmer_rank(algorithm="mwrank")),
    "torsion_order": int(E.torsion_order()),
    "torsion_invariants": invariants,
    "torsion_two_dimension": int(torsion_two_dimension(invariants)),
    "root_number": int(E.root_number()),
    "conductor": int(E.conductor()),
}}
for algorithm in analytic_rank_algorithms:
    payload["analytic_rank_" + algorithm] = int(E.analytic_rank(algorithm=algorithm))
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
    result["status"] = "ok" if completed.returncode == 0 else "sage-error"

    marker = _parse_marker(completed.stdout)
    if marker is not None:
        result.update(marker)
        result["rank_plus_sha2_dimension"] = (
            int(marker["selmer_rank_pari"]) - int(marker["torsion_two_dimension"])
        )

    result["stdout_tail"] = _tail_lines(completed.stdout)
    result["stderr_tail"] = _tail_lines(completed.stderr)
    return result


def diagnose_rows(
    rows: list[dict[str, Any]],
    *,
    sage_executable: str,
    timeout_seconds: int,
    run: Run = subprocess.run,
    analytic_rank_algorithms: list[str] | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    analytic_rank_algorithms = analytic_rank_algorithms or []
    for row in rows:
        cmd = [
            sage_executable,
            "-python",
            "-c",
            _sage_program(
                [int(value) for value in row["model"]],
                analytic_rank_algorithms,
            ),
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
    parser.add_argument("--sage", default="sage", help="Sage executable.")
    parser.add_argument("--timeout", type=int, default=120, help="Seconds per curve.")
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
    parser.add_argument(
        "--analytic-rank",
        action="append",
        choices=["pari", "sympow", "rubinstein", "zero_sum"],
        default=[],
        help=(
            "Also ask Sage for probable analytic_rank(algorithm=...). "
            "This is evidence, not a strict rank certificate."
        ),
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
                sage_executable=args.sage,
                timeout_seconds=args.timeout,
                analytic_rank_algorithms=args.analytic_rank,
            )[0]
            results.append(result)
            handle.write(json.dumps(result, ensure_ascii=True) + "\n")
            handle.flush()
            print(
                f"[{index}/{len(rows)}] "
                f"({result['A']},{result['B']}) {result['curve']} "
                f"status={result['status']}",
                flush=True,
            )

    status_counts: dict[str, int] = {}
    selmer_counts: dict[str, int] = {}
    for result in results:
        status = str(result["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
        if "selmer_rank_pari" in result:
            key = str(result["selmer_rank_pari"])
            selmer_counts[key] = selmer_counts.get(key, 0) + 1

    print(f"wrote {len(results)} Sage diagnostic rows to {args.out}")
    print(f"status_counts={dict(sorted(status_counts.items()))}")
    if selmer_counts:
        print(f"selmer_rank_counts={dict(sorted(selmer_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
