"""Chain-fast CLI runner."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from .output import _NearMissTopK, _print_chain_fast_profile


def _resolve_chain_fast_flags(args: argparse.Namespace, backend: str) -> dict[str, bool]:
    flags = {
        "bucket_stats": bool(getattr(args, "bucket_stats", False)),
        "mod_sieve": bool(getattr(args, "mod_sieve", False)),
        "safe_pair_sieve": bool(getattr(args, "safe_pair_sieve", False)),
    }
    if flags["bucket_stats"] and not getattr(args, "db", None):
        raise SystemExit("--bucket-stats requires --db so the aggregated rows can be persisted.")
    if flags["safe_pair_sieve"] and backend != "python":
        raise SystemExit(
            "--safe-pair-sieve currently supports only backend=python. "
            "Use --backend python or disable the experimental sieve."
        )
    return flags


def _build_chain_fast_run_params(
    args: argparse.Namespace, backend: str, near_miss_limit: int, flags: dict[str, bool]
) -> dict[str, object]:
    return {
        "backend": backend,
        "backend_requested": getattr(args, "backend", "auto"),
        "bucket_stats": flags["bucket_stats"],
        "max_hyp": args.max_hyp,
        "mod_sieve": flags["mod_sieve"],
        "near_miss": bool(getattr(args, "near_miss", False)),
        "near_miss_limit": near_miss_limit,
        "profile": bool(getattr(args, "profile", False)),
        "safe_pair_sieve": flags["safe_pair_sieve"],
        "workers": args.workers,
    }


def _print_chain_fast_banner(
    args: argparse.Namespace,
    *,
    backend: str,
    start_t1: int,
    triples_source: str,
    flags: dict[str, bool],
) -> None:
    print("=" * 72)
    print("Pythagorean 4-cycle fast search — O(n²) primitive-triple-pair method")
    print(
        f"  max_hyp={args.max_hyp}  backend={backend}"
        f"  workers={args.workers}  start_t1={start_t1}"
        f"  triples_source={triples_source}"
    )
    enabled_options: list[str] = []
    if getattr(args, "near_miss", False):
        enabled_options.append("near_miss=True")
    if bool(getattr(args, "profile", False)):
        enabled_options.append("profile=True")
    if flags["bucket_stats"]:
        enabled_options.append("bucket_stats=True")
    if enabled_options:
        print("  options: " + "  ".join(enabled_options))
    if flags["safe_pair_sieve"] or flags["mod_sieve"]:
        print(
            "  experimental: "
            f"safe_pair_sieve={flags['safe_pair_sieve']}  mod_sieve={flags['mod_sieve']}"
        )
    print("=" * 72)


def _run_chain_fast(args: argparse.Namespace) -> None:
    from rational_distance._legacy.search_chain import results_to_json
    from rational_distance._legacy.search_chain_fast import (
        build_chain_fast_triples,
        resolve_backend_choice,
        run_chain_fast,
    )

    db_conn = None
    run_id: int | None = None
    start_t1 = 0
    backend_requested = getattr(args, "backend", "auto")
    backend = resolve_backend_choice(args.max_hyp, backend_requested)
    near_miss_limit = int(getattr(args, "near_miss_limit", 100000))
    flags = _resolve_chain_fast_flags(args, backend)
    run_params = _build_chain_fast_run_params(args, backend, near_miss_limit, flags)
    near_miss_store = _NearMissTopK(near_miss_limit)
    triples: list[tuple[int, int, int]] | None = None
    time_generate_triples_s = 0.0
    triples_source = "generated"
    db_write_s = 0.0

    if getattr(args, "db", None):
        from rational_distance._legacy.chain_db import (
            cache_triples,
            connect_db,
            init_schema,
            load_cached_triples,
            record_run_triples,
            resume_run,
            start_run,
        )

        db_conn = connect_db(args.db)
        try:
            init_schema(db_conn)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc

        if getattr(args, "resume", False):
            resumed = resume_run(db_conn, run_params)
            if resumed:
                run_id, last_t1 = resumed
                start_t1 = last_t1 + 1
                print(f"Resuming run {run_id} from T1 index {start_t1}")
            else:
                print("No resumable run found; starting fresh.")

        cached_triples = load_cached_triples(db_conn, args.max_hyp)
        if cached_triples:
            triples = cached_triples
            triples_source = "db-cache"
        else:
            triples_started = time.perf_counter()
            triples = build_chain_fast_triples(args.max_hyp)
            time_generate_triples_s = time.perf_counter() - triples_started
            db_started = time.perf_counter()
            cache_triples(db_conn, args.max_hyp, triples)
            db_write_s += time.perf_counter() - db_started

        if run_id is None:
            db_started = time.perf_counter()
            run_id = start_run(db_conn, run_params, len(triples), triples_source=triples_source)
            record_run_triples(db_conn, run_id, triples)
            db_write_s += time.perf_counter() - db_started

    if triples is None:
        triples_started = time.perf_counter()
        triples = build_chain_fast_triples(args.max_hyp)
        time_generate_triples_s = time.perf_counter() - triples_started

    near_miss_callback = None
    chunk_complete_callback = None
    if getattr(args, "near_miss", False):

        def near_miss_callback(a, b, c, d, c3_ok, c4_ok, sq3, sq4, h3, h4):
            near_miss_store.consider(a, b, c, d, c3_ok, c4_ok, sq3, sq4, h3, h4)

    if db_conn is not None:
        from rational_distance._legacy.chain_db import checkpoint_t1

        def chunk_complete_callback(last_t1_index: int) -> None:
            checkpoint_t1(db_conn, run_id, last_t1_index)

    _print_chain_fast_banner(
        args,
        backend=backend,
        start_t1=start_t1,
        triples_source=triples_source,
        flags=flags,
    )

    t0 = time.perf_counter()
    execution = run_chain_fast(
        max_hyp=args.max_hyp,
        progress=not args.no_progress,
        backend=backend,
        workers=args.workers,
        start_t1=start_t1,
        near_miss_callback=near_miss_callback,
        chunk_complete_callback=chunk_complete_callback,
        triples=triples,
        profile=bool(getattr(args, "profile", False)),
        triples_source=triples_source,
        safe_pair_sieve=flags["safe_pair_sieve"],
        mod_sieve=flags["mod_sieve"],
        bucket_stats=flags["bucket_stats"],
    )
    elapsed = time.perf_counter() - t0
    results = execution.results
    execution.profile.time_db_write_s += db_write_s
    execution.profile.time_generate_triples_s = time_generate_triples_s
    execution.profile.triples_source = triples_source
    execution.profile.near_miss_seen = near_miss_store.seen
    execution.profile.near_miss_saved = near_miss_store.saved
    execution.profile.near_miss_dropped = near_miss_store.dropped

    run_row = None
    if db_conn is not None:
        from rational_distance._legacy.chain_db import (
            finish_run,
            get_bucket_stats,
            get_near_misses,
            get_run,
            record_bucket_stats,
            record_near_misses,
            record_solution,
            update_run_db_size,
        )

        db_started = time.perf_counter()
        for result in results:
            record_solution(db_conn, run_id, result)
        if getattr(args, "near_miss", False) and near_miss_store.saved:
            record_near_misses(db_conn, run_id, near_miss_store.rows())
        if flags["bucket_stats"] and execution.bucket_stats:
            record_bucket_stats(
                db_conn,
                run_id,
                [row.as_dict() for row in execution.bucket_stats],
            )
        execution.profile.time_db_write_s += time.perf_counter() - db_started

        finish_run(db_conn, run_id, elapsed=elapsed, profile=execution.profile)
        db_size = Path(args.db).stat().st_size
        update_run_db_size(db_conn, run_id, db_size)
        execution.profile.db_bytes_after_run = db_size
        run_row = get_run(db_conn, run_id)

        if getattr(args, "near_miss", False) and near_miss_store.saved:
            top_nm = get_near_misses(db_conn, run_id, limit=5)
            print("\nTop near-misses (sq4_deficit, closest first):")
            for near_miss in top_nm:
                print(
                    f"  a={near_miss['a']} b={near_miss['b_val']} "
                    f"c={near_miss['c']} d={near_miss['d']}"
                    f"  sq4_deficit={near_miss['sq4_deficit']}"
                )
        if flags["bucket_stats"]:
            bucket_row_count = len(get_bucket_stats(db_conn, run_id))
            print(f"  persisted bucket rows: {bucket_row_count}")

    print(f"\nFound {len(results)} unit-square 4-cycle solution(s) in {elapsed:.1f}s")
    print(
        "  near-misses seen/saved/dropped: "
        f"{execution.profile.near_miss_seen}/{execution.profile.near_miss_saved}/"
        f"{execution.profile.near_miss_dropped}"
    )
    if db_conn is not None and run_row is not None:
        print(f"  DB run id: {run_id}  last_t1_index={run_row['last_t1_index']}")
    print("  All results satisfy a+c == b+d by construction.")
    if getattr(args, "profile", False):
        _print_chain_fast_profile(execution.profile.as_dict())

    top = args.top if args.top > 0 else len(results)
    if results:
        print()
        for result in results[:top]:
            print(str(result))
            print()
        if len(results) > top:
            print(f"  ... {len(results) - top} more rows suppressed (use --top 0 to show all)")

    if args.out:
        data = results_to_json(results, args.max_hyp, require_square=True, elapsed=elapsed)
        data["profile"] = execution.profile.as_dict()
        with open(args.out, "w") as handle:
            json.dump(data, handle, indent=2)
        print(f"\nResults saved to {args.out}")


__all__ = ["_run_chain_fast"]
