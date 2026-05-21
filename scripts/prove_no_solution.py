"""Incrementally prove non-existence of full-chain solutions for (A, B) pairs.

Each reduced ``(A, B)`` pair is run through a pipeline of judgement methods
(see ``rational_distance.proof_status.methods``). The strongest conclusion
reached for each pair is materialised into a SQLite database and every
attempt is logged for audit.

Typical usage
-------------

  # Process all reduced pairs up to max_hyp = 500 and write to .cache/proofs.sqlite3
  uv run python scripts/prove_no_solution.py --max-hyp 500 \
      --db .cache/proofs.sqlite3

  # Process a single pair
  uv run python scripts/prove_no_solution.py --pair 264,420 \
      --db .cache/proofs.sqlite3

  # Just print the current status histogram
  uv run python scripts/prove_no_solution.py --db .cache/proofs.sqlite3 --report

  # Re-run all methods even for pairs already classified as terminal
  uv run python scripts/prove_no_solution.py --max-hyp 500 \
      --db .cache/proofs.sqlite3 --rerun-terminal

  # Make the direction-five Heegner/height diagnostic scan deeper
  uv run python scripts/prove_no_solution.py --pair 7,45 \
      --db .cache/proofs.sqlite3 --heegner-multiple-bound 30
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def _parse_pair(spec: str) -> tuple[int, int]:
    parts = spec.split(",")
    if len(parts) != 2:
        raise SystemExit(f"--pair expects 'A,B' (got {spec!r})")
    try:
        a, b = int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise SystemExit(f"--pair: both values must be integers (got {spec!r})") from exc
    if a <= 0 or b <= 0:
        raise SystemExit(f"--pair: both A and B must be positive (got {spec!r})")
    if a > b:
        a, b = b, a
    return a, b


def _print_status_report(db_path: Path) -> None:
    from rational_distance.proof_status import schema

    conn = schema.connect_db(db_path)
    schema.init_schema(conn)
    status_hist = schema.status_counts(conn)
    method_hist = schema.method_outcome_counts(conn)

    total = sum(status_hist.values())
    print("=" * 72)
    print(f"Proof status report — {db_path}")
    print("=" * 72)
    print(f"Total pairs in DB: {total}")
    if total == 0:
        print("  (no pairs processed yet)")
        return

    print("\nStatus histogram:")
    for status in ("no_solution", "solution_found", "hard_case", "unknown"):
        count = status_hist.get(status, 0)
        ratio = count / total if total else 0.0
        print(f"  {status:<18} {count:>8}  ({ratio:6.2%})")

    print("\nMethod-outcome breakdown (across all attempts):")
    if not method_hist:
        print("  (no attempts recorded)")
        return
    method_names = sorted({key[0] for key in method_hist})
    outcome_names = sorted({key[1] for key in method_hist})
    header = "  method".ljust(24) + "".join(f"{name:>14}" for name in outcome_names)
    print(header)
    for method in method_names:
        row = f"  {method:<22}"
        for outcome in outcome_names:
            row += f"{method_hist.get((method, outcome), 0):>14}"
        print(row)


def _print_pair_status(status) -> None:
    from rational_distance.proof_status.types import PairProofStatus

    assert isinstance(status, PairProofStatus)
    bits = [f"(A={status.A}, B={status.B})", f"status={status.status}"]
    if status.method:
        bits.append(f"via={status.method}")
    if status.rank_lower is not None or status.rank_upper is not None:
        bits.append(f"rank=[{status.rank_lower},{status.rank_upper}]")
    if status.concordant_n_count is not None:
        bits.append(f"concordant_n={status.concordant_n_count}")
    if status.chain_compatible_count is not None:
        bits.append(f"chain_ok={status.chain_compatible_count}")
    print("  ".join(bits))
    if status.notes:
        print(f"    notes: {status.notes}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db",
        required=True,
        help="SQLite database for persisted proof status (created if absent).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--pair",
        type=str,
        default=None,
        help="Process a single 'A,B' pair instead of a batch.",
    )
    group.add_argument(
        "--max-hyp",
        type=int,
        default=None,
        help="Process all reduced (A,B) pairs derived from primitive Pythagorean "
        "triples with hypotenuse <= max-hyp.",
    )
    group.add_argument(
        "--report",
        action="store_true",
        help="Skip processing; only print the current status histogram.",
    )

    parser.add_argument(
        "--rerun-terminal",
        action="store_true",
        help="Re-run methods even for pairs already classified as terminal.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Suppress per-pair progress output.",
    )
    parser.add_argument(
        "--print-each",
        action="store_true",
        help="Print the materialised status line for each processed pair.",
    )
    parser.add_argument(
        "--heegner-multiple-bound",
        type=int,
        default=None,
        help=(
            "Direction-five diagnostic depth: scan nG+T for |n| <= this bound "
            "(default from RD_HEEGNER_MULTIPLE_BOUND or 12)."
        ),
    )
    parser.add_argument(
        "--heegner-height-bound",
        type=float,
        default=None,
        help=(
            "Optional canonical-height cap for the Heegner/height diagnostic scan. "
            "This only limits the scan; it is not treated as a no-solution proof."
        ),
    )
    args = parser.parse_args()

    if args.heegner_multiple_bound is not None:
        if args.heegner_multiple_bound < 0:
            raise SystemExit("--heegner-multiple-bound must be non-negative")
        os.environ["RD_HEEGNER_MULTIPLE_BOUND"] = str(args.heegner_multiple_bound)
    if args.heegner_height_bound is not None:
        if args.heegner_height_bound < 0:
            raise SystemExit("--heegner-height-bound must be non-negative")
        os.environ["RD_HEEGNER_HEIGHT_BOUND"] = str(args.heegner_height_bound)

    db_path = Path(args.db)

    if args.report:
        _print_status_report(db_path)
        return

    from rational_distance.concordant.pairs import generate_ab_pairs
    from rational_distance.proof_status import schema, workflow

    conn = schema.connect_db(db_path)
    schema.init_schema(conn)

    if args.pair:
        pairs: list[tuple[int, int]] = [_parse_pair(args.pair)]
    elif args.max_hyp:
        if args.max_hyp <= 0:
            raise SystemExit("--max-hyp must be positive")
        pairs = generate_ab_pairs(max_hyp=args.max_hyp)
    else:
        raise SystemExit("must specify one of --pair, --max-hyp or --report")

    config = workflow.WorkflowConfig(rerun_terminal=args.rerun_terminal)

    progress = None
    if not args.no_progress and len(pairs) > 1:
        try:
            from tqdm import tqdm

            progress = tqdm(total=len(pairs), desc="proof_status", leave=False)
        except ImportError:
            progress = None

    print("=" * 72)
    print(f"Proof-status workflow — DB: {db_path}")
    print(f"  pairs to process: {len(pairs)}")
    print(f"  rerun_terminal:   {args.rerun_terminal}")
    if args.heegner_multiple_bound is not None:
        print(f"  heegner |n|<=:    {args.heegner_multiple_bound}")
    if args.heegner_height_bound is not None:
        print(f"  heegner height<=: {args.heegner_height_bound}")
    print("=" * 72)

    counts: dict[str, int] = {}

    def _on_pair(status) -> None:
        counts[status.status] = counts.get(status.status, 0) + 1
        if args.print_each:
            _print_pair_status(status)
        if progress is not None:
            progress.update(1)
            progress.set_postfix(
                no_sol=counts.get("no_solution", 0),
                hard=counts.get("hard_case", 0),
                sol=counts.get("solution_found", 0),
            )

    workflow.process_pairs(conn, pairs, config=config, on_pair=_on_pair)

    if progress is not None:
        progress.close()

    print()
    print("Summary of this run:")
    for status_name in ("no_solution", "solution_found", "hard_case", "unknown"):
        print(f"  {status_name:<18} {counts.get(status_name, 0):>8}")
    print()
    _print_status_report(db_path)


if __name__ == "__main__":
    main()
