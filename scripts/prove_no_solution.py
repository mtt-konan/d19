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
import json
import os
import sys
import time
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


def _reset_sqlite_db(db_path: Path) -> None:
    for path in (
        db_path,
        db_path.with_name(db_path.name + "-wal"),
        db_path.with_name(db_path.name + "-shm"),
    ):
        if path.exists():
            path.unlink()


def _configure_pari_runtime() -> None:
    os.environ.setdefault("PARI_MT_ENGINE", "single")


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
        "--progress-every",
        type=int,
        default=0,
        help="Print a plain progress line every N processed pairs (0 = disabled).",
    )
    # 导入公共并行工具获取默认 worker 数
    from rational_distance.parallel import default_workers
    _default_workers = default_workers()

    parser.add_argument(
        "--workers",
        type=int,
        default=_default_workers,
        help=(
            f"Number of parallel worker processes for batch runs. "
            f"Default: {_default_workers} (auto = CPU count). Use --workers 1 for "
            f"sequential execution. When > 1, uses multiprocessing + "
            f"batched commits (see --commit-every) for large speedups. "
            f"Incompatible with --rerun-terminal."
        ),
    )
    parser.add_argument(
        "--serial",
        action="store_true",
        help="Run in serial mode (equivalent to --workers 1).",
    )
    parser.add_argument(
        "--commit-every",
        type=int,
        default=1000,
        help=(
            "When --workers > 1: commit the SQLite transaction every N "
            "pairs (default: 1000). Larger values reduce commit overhead "
            "at the cost of less frequent persistence checkpoints."
        ),
    )
    parser.add_argument(
        "--moduli",
        type=str,
        default="standard",
        choices=["minimal", "balanced", "standard", "extended"],
        help=(
            "模数档位：minimal(2个,最快), balanced(5个), "
            "standard(14个,默认), extended(23个,最慢但最强)。"
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="清空旧数据库，从头重跑（不做增量跳过）。",
    )
    parser.add_argument(
        "--fast-core",
        action="store_true",
        help="快速核心筛模式：全量只跑核心筛，不写全量审计；只对疑难对写完整 proof_status。",
    )
    parser.add_argument(
        "--fast-core-only",
        action="store_true",
        help="--fast-core: stop after core sieve summary; do not audit survivors with PARI.",
    )
    parser.add_argument(
        "--pair-chunk-size",
        type=int,
        default=50_000,
        help="--fast-core 每个 worker 任务包含的 pair 数量。",
    )
    parser.add_argument(
        "--fast-summary-json",
        type=Path,
        default=None,
        help="--fast-core: write aggregate summary and survivors to this JSON file.",
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
    _configure_pari_runtime()

    if args.fast_core_only and not args.fast_core:
        raise SystemExit("--fast-core-only requires --fast-core")

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

    from rational_distance.concordant.pairs import generate_ab_pairs, iter_ab_pairs
    from rational_distance.proof_status import fast_core, schema, workflow
    from rational_distance.proof_status.methods import set_moduli_preset, get_current_moduli

    # 设置模数档位
    set_moduli_preset(args.moduli)

    # --force: 删除旧库重建
    if args.force:
        _reset_sqlite_db(db_path)

    conn = schema.connect_db(db_path)
    schema.init_schema(conn)

    # 处理 --serial 参数
    workers = 1 if args.serial else args.workers

    pair_label = "1"
    if args.pair:
        pairs = [_parse_pair(args.pair)]
    elif args.max_hyp:
        if args.max_hyp <= 0:
            raise SystemExit("--max-hyp must be positive")
        if workers > 1:
            pairs = generate_ab_pairs(args.max_hyp)
            pair_label = f"{len(pairs)} (materialized from max_hyp={args.max_hyp})"
        else:
            pairs = iter_ab_pairs(args.max_hyp)
            pair_label = f"streaming (max_hyp={args.max_hyp})"
    else:
        raise SystemExit("must specify one of --pair, --max-hyp or --report")

    config = workflow.WorkflowConfig(rerun_terminal=args.rerun_terminal)

    if workers > 1 and args.rerun_terminal:
        raise SystemExit(
            "--workers > 1 is not compatible with --rerun-terminal "
            "(parallel path only processes pairs not yet terminal)."
        )

    counts: dict[str, int] = {}
    started = time.perf_counter()
    processed = 0

    def _emit_progress(force: bool = False) -> None:
        if args.progress_every <= 0:
            return
        if not force and processed % args.progress_every != 0:
            return
        elapsed = time.perf_counter() - started
        rate = processed / elapsed if elapsed > 0 else 0.0
        print(
            f"[progress] done={processed} no_solution={counts.get('no_solution', 0)} hard_case={counts.get('hard_case', 0)} solution_found={counts.get('solution_found', 0)} elapsed={elapsed:.1f}s rate={rate:.1f}/s",
            flush=True,
        )

    def _on_result(result) -> None:
        nonlocal processed
        processed += 1
        counts[result.final_status] = counts.get(result.final_status, 0) + 1
        if args.print_each:
            from rational_distance.proof_status.types import PairProofStatus

            synthetic = PairProofStatus(
                A=result.A,
                B=result.B,
                status=result.final_status,
                method=result.final_method,
                rank_lower=result.rank_lower,
                rank_upper=result.rank_upper,
                concordant_n_count=result.concordant_n_count,
                chain_compatible_count=result.chain_compatible_count,
                notes=result.final_notes,
                updated_at="",
            )
            _print_pair_status(synthetic)
        _emit_progress()

    print("=" * 72)
    print(f"Proof-status workflow — DB: {db_path}")
    print(f"  mode:             {'fast-core' if args.fast_core else 'full-audit'}")
    print(f"  pairs to process: {pair_label}")
    print(f"  rerun_terminal:   {args.rerun_terminal}")
    print(f"  workers:          {workers}")
    print(f"  moduli:           {args.moduli} ({len(get_current_moduli())} 个)")
    if workers > 1:
        print(f"  commit_every:     {args.commit_every}")
    if args.heegner_multiple_bound is not None:
        print(f"  heegner |n|<=:    {args.heegner_multiple_bound}")
    if args.heegner_height_bound is not None:
        print(f"  heegner height<=: {args.heegner_height_bound}")
    print("=" * 72)

    if args.fast_core:
        if not args.max_hyp:
            raise SystemExit("--fast-core requires --max-hyp")
        if args.fast_core_only and not args.fast_summary_json:
            raise SystemExit("--fast-core-only requires --fast-summary-json")
        if workers <= 1:
            raise SystemExit("--fast-core requires --workers > 1")
        if args.pair_chunk_size <= 0:
            raise SystemExit("--pair-chunk-size must be positive")

        print(
            f"[phase] fast-core start pairs={len(pairs)} workers={workers} "
            f"chunk_size={args.pair_chunk_size}",
            flush=True,
        )
        core_started = time.perf_counter()
        core_result = fast_core.run_fast_core(
            pairs,
            workers=workers,
            pair_chunk_size=args.pair_chunk_size,
            pool_chunksize=1,
            on_chunk=None,
        )
        core_elapsed = time.perf_counter() - core_started
        counts["no_solution"] = counts.get("no_solution", 0) + core_result.no_solution
        if args.fast_summary_json is not None:
            args.fast_summary_json.parent.mkdir(parents=True, exist_ok=True)
            args.fast_summary_json.write_text(
                json.dumps(
                    {
                        "checked": core_result.checked,
                        "no_solution": core_result.no_solution,
                        "survivor_count": len(core_result.survivors),
                        "survivors": [list(pair) for pair in core_result.survivors],
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            )
        print(
            f"[phase] fast-core done checked={core_result.checked} "
            f"no_solution={core_result.no_solution} "
            f"survivors={len(core_result.survivors)} elapsed={core_elapsed:.1f}s",
            flush=True,
        )
        if args.fast_core_only:
            print("[phase] fast-core-only: survivor audit skipped", flush=True)
        else:

            print(f"[phase] survivor audit start pairs={len(core_result.survivors)}", flush=True)
            audit_started = time.perf_counter()
            workflow.process_pairs_parallel(
                conn,
                core_result.survivors,
                workers=workers,
                commit_every=args.commit_every,
                skip_terminal=False,
                on_result=_on_result,
            )
            audit_elapsed = time.perf_counter() - audit_started
            print(f"[phase] survivor audit done elapsed={audit_elapsed:.1f}s", flush=True)

    elif workers > 1:
        workflow.process_pairs_parallel(
            conn,
            pairs,
            workers=workers,
            commit_every=args.commit_every,
            skip_terminal=not args.rerun_terminal,
            on_result=_on_result,
        )
    else:

        def _on_pair(status) -> None:
            nonlocal processed
            processed += 1
            counts[status.status] = counts.get(status.status, 0) + 1
            if args.print_each:
                _print_pair_status(status)
            _emit_progress()

        workflow.process_pairs(conn, pairs, config=config, on_pair=_on_pair)

    _emit_progress(force=True)

    print()
    print("Summary of this run:")
    for status_name in ("no_solution", "solution_found", "hard_case", "unknown"):
        print(f"  {status_name:<18} {counts.get(status_name, 0):>8}")
    print()
    _print_status_report(db_path)


if __name__ == "__main__":
    main()
