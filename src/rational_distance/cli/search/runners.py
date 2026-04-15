"""CLI run orchestration for the search entrypoint."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from .output import (
    _NearMissTopK,
    _print_chain_fast_profile,
    _print_four_vertex,
    _print_summary,
    _print_table,
    _save_json,
    _size_estimate,
)


def _resolve_parametric_limits(args: argparse.Namespace) -> None:
    """Resolve the effective parametric limits for the CLI.

    `--scale` is a shorthand default. Explicit `--max-*` flags keep
    priority so callers can override one field without restating all of them.
    """
    default_max_m = 80
    default_max_k_num = 640
    default_max_k_den = 320

    if args.scale is not None:
        if args.max_m is None:
            args.max_m = args.scale
        if args.max_k_den is None:
            args.max_k_den = 4 * args.scale
        if args.max_k_num is None:
            args.max_k_num = 8 * args.scale

    if args.max_m is None:
        args.max_m = default_max_m
    if args.max_k_num is None:
        args.max_k_num = default_max_k_num
    if args.max_k_den is None:
        args.max_k_den = default_max_k_den


def _run_parametric(args: argparse.Namespace) -> None:
    from rational_distance.backend import _try_torch, detect_backend
    from rational_distance.search import (
        brute_force_search,
        dedup_by_symmetry,
        merge_results,
        parametric_search_fast,
    )
    from rational_distance.search_gpu import parametric_search_gpu

    _resolve_parametric_limits(args)

    use_cpu = args.backend == "numpy"
    xp = None
    backend_name = ""

    if use_cpu:
        backend_name = "numpy (CPU, multiprocessing)"
    elif args.backend == "cupy":
        import cupy as cp

        xp = cp
        backend_name = "forced:cupy"
    elif args.backend == "torch":
        xp = _try_torch()
        if xp is None:
            print("ERROR: PyTorch ROCm/CUDA not available.", file=sys.stderr)
            sys.exit(1)
        backend_name = "forced:torch"
    else:
        xp, backend_name, _ = detect_backend()

    est = _size_estimate(args.max_m, args.max_k_num, args.max_k_den)
    print("=" * 72)
    print("Rational distance search [parametric] — A(0,0) B(1,0) C(1,1) D(0,1)")
    print(f"  backend  : {backend_name}")
    print(
        f"  max_m={args.max_m}, max_k={args.max_k_num}/{args.max_k_den}, "
        f"min_rational={args.min_rational}"
    )
    print(f"  search space ≈ {est} (triple x k combinations)")
    if args.inside:
        print("  Filter: inside unit square only (0<x<1, 0<y<1)")
    if args.brute_den:
        print(f"  + brute-force denominator ≤ {args.brute_den}")
    print("=" * 72)

    dedup_sym = not args.no_dedup_symmetry
    t0 = time.perf_counter()

    if use_cpu:
        results = parametric_search_fast(
            max_m=args.max_m,
            max_k_num=args.max_k_num,
            max_k_den=args.max_k_den,
            min_rational=args.min_rational,
            workers=args.workers,
            progress=not args.no_progress,
            inside_only=args.inside,
        )
        if args.brute_den:
            bf = list(brute_force_search(max_den=args.brute_den, min_rational=args.min_rational))
            results = list(merge_results(iter(results), iter(bf)))
        backend_used = backend_name
    else:
        results, backend_used = parametric_search_gpu(
            max_m=args.max_m,
            max_k_num=args.max_k_num,
            max_k_den=args.max_k_den,
            min_rational=args.min_rational,
            progress=not args.no_progress,
            xp=xp,
            inside_only=args.inside,
        )
        if args.brute_den:
            bf = list(brute_force_search(max_den=args.brute_den, min_rational=args.min_rational))
            results = list(merge_results(iter(results), iter(bf)))

    raw_count = len(results)
    if dedup_sym:
        results = dedup_by_symmetry(results)

    elapsed = time.perf_counter() - t0
    count_by_n = _print_summary(results, elapsed, deduped_from=raw_count if dedup_sym else None)
    _print_table(results, args.top)
    _print_four_vertex(results)

    if args.out:
        params = {
            "max_m": args.max_m,
            "max_k_num": args.max_k_num,
            "max_k_den": args.max_k_den,
            "min_rational": args.min_rational,
            "backend": args.backend,
            "workers": args.workers,
            "inside": args.inside,
            "brute_den": args.brute_den,
            "no_dedup_symmetry": args.no_dedup_symmetry,
        }
        _save_json(
            args.out, "parametric", params, elapsed, results, count_by_n, backend=backend_used
        )


def _run_ec(args: argparse.Namespace) -> None:
    from rational_distance.backend import _try_torch, detect_backend
    from rational_distance.ec_db import ECSearchStore
    from rational_distance.search_ec import ec_search

    xp = None
    backend_name = "numpy (CPU)"
    if args.backend == "numpy":
        pass
    elif args.backend == "cupy":
        import cupy as cp

        xp = cp
        backend_name = "forced:cupy"
    elif args.backend == "torch":
        xp = _try_torch()
        if xp is None:
            print("ERROR: PyTorch ROCm/CUDA not available.", file=sys.stderr)
            sys.exit(1)
        backend_name = "forced:torch"
    elif args.backend == "auto":
        xp_auto, backend_name, _ = detect_backend()
        import numpy as _np

        xp = None if xp_auto is _np else xp_auto
        backend_name = backend_name if xp is not None else "numpy (CPU)"

    if args.resume and not args.db:
        print("ERROR: --resume requires --db PATH.", file=sys.stderr)
        sys.exit(2)

    params = {
        "max_m": args.max_m,
        "max_k_num": args.max_k_num,
        "max_k_den": args.max_k_den,
        "max_steps": args.max_steps,
        "min_rational": args.min_rational,
        "inside": args.inside,
    }
    store = ECSearchStore(args.db, params, backend_name, resume=args.resume) if args.db else None

    print("=" * 72)
    print("Rational distance search [ec] — A(0,0) B(1,0) C(1,1) D(0,1)")
    print(f"  backend  : {backend_name}")
    print(f"  max_m={args.max_m}, seed range k_num≤{args.max_k_num}, k_den≤{args.max_k_den}")
    print(f"  max_steps={args.max_steps}, min_rational={args.min_rational}, inside={args.inside}")
    if store is not None:
        mode = "resume" if args.resume else "record"
        print(f"  db       : {args.db}  (run_id={store.run_id}, mode={mode})")
    print("=" * 72)

    t0 = time.perf_counter()
    try:
        results = ec_search(
            max_m=args.max_m,
            max_k_num=args.max_k_num,
            max_k_den=args.max_k_den,
            max_steps=args.max_steps,
            min_rational=args.min_rational,
            inside_only=args.inside,
            progress=not args.no_progress,
            xp=xp,
            store=store,
        )
        elapsed = time.perf_counter() - t0
        if store is not None:
            store.finish(elapsed)
    finally:
        if store is not None:
            store.close()

    count_by_n = _print_summary(results, elapsed)
    _print_table(results, args.top)
    _print_four_vertex(results)

    if args.out:
        _save_json(args.out, "ec", params, elapsed, results, count_by_n)


def _run_chain(args: argparse.Namespace) -> None:
    from rational_distance.search_chain import find_chains, results_to_json

    print("=" * 72)
    print("Pythagorean 4-cycle search — rectangle / unit-square problem")
    print(f"  max_val={args.max_val}, require_square={args.require_square}")
    print("=" * 72)

    t0 = time.perf_counter()
    results = find_chains(
        max_val=args.max_val,
        require_square=args.require_square,
        canonical=True,
        progress=not args.no_progress,
    )
    elapsed = time.perf_counter() - t0

    n_sq = sum(1 for result in results if result.square_ok)
    print(f"\nFound {len(results)} canonical 4-cycles in {elapsed:.1f}s")
    print(f"  {n_sq} satisfy unit-square constraint (a+c == b+d)")
    print(f"  {len(results) - n_sq} are rectangle-only solutions")

    top = args.top if args.top > 0 else len(results)
    if results:
        print()
        for result in results[:top]:
            print(str(result))
            print()
        if len(results) > top:
            print(f"  ... {len(results) - top} more rows suppressed (use --top 0 to show all)")

    if args.out:
        data = results_to_json(results, args.max_val, args.require_square, elapsed)
        with open(args.out, "w") as handle:
            json.dump(data, handle, indent=2)
        print(f"\nResults saved to {args.out}")


def _run_chain_fast(args: argparse.Namespace) -> None:
    from rational_distance.search_chain import results_to_json
    from rational_distance.search_chain_fast import (
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
    bucket_stats_enabled = bool(getattr(args, "bucket_stats", False))
    safe_pair_sieve_enabled = bool(getattr(args, "safe_pair_sieve", False))
    if bucket_stats_enabled and not getattr(args, "db", None):
        raise SystemExit("--bucket-stats requires --db so the aggregated rows can be persisted.")
    if safe_pair_sieve_enabled and backend != "python":
        raise SystemExit(
            "--safe-pair-sieve currently supports only backend=python. "
            "Use --backend python or disable the experimental sieve."
        )
    run_params = {
        "backend": backend,
        "backend_requested": backend_requested,
        "bucket_stats": bucket_stats_enabled,
        "max_hyp": args.max_hyp,
        "mod_sieve": bool(getattr(args, "mod_sieve", False)),
        "near_miss": bool(getattr(args, "near_miss", False)),
        "near_miss_limit": near_miss_limit,
        "profile": bool(getattr(args, "profile", False)),
        "safe_pair_sieve": safe_pair_sieve_enabled,
        "workers": args.workers,
    }
    near_miss_store = _NearMissTopK(near_miss_limit)
    triples: list[tuple[int, int, int]] | None = None
    time_generate_triples_s = 0.0
    triples_source = "generated"
    db_write_s = 0.0

    if getattr(args, "db", None):
        from rational_distance.chain_db import (
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
        from rational_distance.chain_db import checkpoint_t1

        def chunk_complete_callback(last_t1_index: int) -> None:
            checkpoint_t1(db_conn, run_id, last_t1_index)

    print("=" * 72)
    print("Pythagorean 4-cycle fast search — O(n²) primitive-triple-pair method")
    print(
        f"  max_hyp={args.max_hyp}  backend={backend}"
        f"  workers={args.workers}  safe_pair_sieve={safe_pair_sieve_enabled}"
        f"  mod_sieve={bool(getattr(args, 'mod_sieve', False))}"
        f"  bucket_stats={bucket_stats_enabled}"
        f"  start_t1={start_t1}  triples_source={triples_source}"
    )
    print("=" * 72)

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
        safe_pair_sieve=safe_pair_sieve_enabled,
        mod_sieve=bool(getattr(args, "mod_sieve", False)),
        bucket_stats=bucket_stats_enabled,
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
        from rational_distance.chain_db import (
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
        if bucket_stats_enabled and execution.bucket_stats:
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
        if bucket_stats_enabled:
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


def _run_concordant(args: argparse.Namespace) -> None:
    from rational_distance.concordant import (
        diagnose_pair,
        generate_ab_pairs,
    )

    def _candidate_payload(candidate) -> dict[str, object]:
        return {
            "n": candidate.n,
            "source": candidate.source,
            "b": candidate.b,
            "b_in_concordant_set": candidate.b_in_concordant_set,
            "b_source": candidate.b_source,
            "c1_ok": candidate.c1_ok,
            "c2_ok": candidate.c2_ok,
            "chain_ok": candidate.chain_ok,
            "c1_nearest_square_delta": candidate.c1_nearest_square_delta,
            "c2_nearest_square_delta": candidate.c2_nearest_square_delta,
            "combined_delta": candidate.combined_delta,
        }

    def _pair_report(diagnostics, *, deep: int) -> dict[str, object]:
        result = diagnostics.result
        return {
            "mode": "pair",
            "A": result.A,
            "B": result.B,
            "ec_bound": result.ec_bound,
            "deep": deep,
            "rank": result.rank,
            "rank_bounds": list(result.rank_bounds),
            "generators": [list(generator) for generator in result.generators],
            "raw_square_x": result.raw_square_x,
            "concordant_n": result.concordant_n,
            "deep_extra_n": diagnostics.deep_extra_n,
            "all_concordant_n": diagnostics.all_concordant_n,
            "mirror_hit_n": diagnostics.mirror_hit_n,
            "chain_compatible": diagnostics.chain_compatible,
            "best_candidate": (
                _candidate_payload(diagnostics.best_candidate)
                if diagnostics.best_candidate is not None
                else None
            ),
            "candidates": [_candidate_payload(candidate) for candidate in diagnostics.candidates],
        }

    def _batch_pair_summary(diagnostics) -> dict[str, object]:
        result = diagnostics.result
        best_candidate = diagnostics.best_candidate
        return {
            "A": result.A,
            "B": result.B,
            "rank": result.rank,
            "rank_bounds": list(result.rank_bounds),
            "concordant_n": result.concordant_n,
            "all_concordant_n": diagnostics.all_concordant_n,
            "chain_compatible": diagnostics.chain_compatible,
            "raw_square_x": result.raw_square_x,
            "mirror_hit_n": diagnostics.mirror_hit_n,
            "mirror_hit_count": len(diagnostics.mirror_hit_n),
            "best_candidate": (
                _candidate_payload(best_candidate) if best_candidate is not None else None
            ),
            "min_combined_delta": (
                best_candidate.combined_delta if best_candidate is not None else None
            ),
            "best_b": best_candidate.b if best_candidate is not None else None,
        }

    print("=" * 72)
    print("Elliptic curve concordant-form analysis")

    if args.pair:
        parts = args.pair.split(",")
        if len(parts) != 2:
            print("Error: --pair must be A,B (e.g. --pair 264,420)")
            return
        A, B = int(parts[0].strip()), int(parts[1].strip())
        print(f"  pair=({A}, {B})  ec_bound={args.ec_bound}  deep={args.deep}")
        print("=" * 72)

        t0 = time.perf_counter()
        diagnostics = diagnose_pair(A, B, ec_bound=args.ec_bound, deep=args.deep)
        result = diagnostics.result
        print(f"\n{result.summary()}")
        if args.deep > 0:
            print(f"\nDeep search (depth={args.deep})...")
        print("\nChain compatibility diagnostics")
        print(f"  deep_extra_n: {diagnostics.deep_extra_n if diagnostics.deep_extra_n else 'none'}")
        print(f"  all_concordant_n: {diagnostics.all_concordant_n}")
        print(f"  mirror_hit_n: {diagnostics.mirror_hit_n if diagnostics.mirror_hit_n else 'none'}")
        if diagnostics.best_candidate is None:
            print("  best_candidate: none")
        else:
            candidate = diagnostics.best_candidate
            print(
                "  best_candidate: "
                f"N={candidate.n} source={candidate.source} b={candidate.b} "
                f"chain_ok={candidate.chain_ok} combined_delta={candidate.combined_delta}"
            )
        if diagnostics.candidates:
            print("  candidates:")
            for candidate in diagnostics.candidates:
                print(
                    "    "
                    f"N={candidate.n} source={candidate.source} b={candidate.b} "
                    f"b_in_concordant_set={candidate.b_in_concordant_set} "
                    f"C1={candidate.c1_ok}(delta={candidate.c1_nearest_square_delta}) "
                    f"C2={candidate.c2_ok}(delta={candidate.c2_nearest_square_delta}) "
                    f"combined_delta={candidate.combined_delta}"
                )
        else:
            print("  candidates: none")

        elapsed = time.perf_counter() - t0
        if args.out:
            with open(args.out, "w") as handle:
                json.dump(_pair_report(diagnostics, deep=args.deep), handle, indent=2)
            print(f"\nReport saved to {args.out}")
        print(f"\nCompleted in {elapsed:.1f}s")

    else:
        print(f"  max_hyp={args.max_hyp}  ec_bound={args.ec_bound}")
        print("=" * 72)

        t0 = time.perf_counter()
        pairs = generate_ab_pairs(args.max_hyp)
        print(f"Generated {len(pairs)} primitive (A,B) pairs")

        results = []
        rank_counts: dict[int, int] = {}
        n_with_concordant = 0
        n_with_chain = 0
        n_with_mirror_hit = 0

        iterator = enumerate(pairs)
        if not args.no_progress:
            from tqdm import tqdm

            iterator = tqdm(list(iterator), desc="EC analysis", leave=False)

        import cypari2

        pari = cypari2.Pari()
        pari.allocatemem(64 * 1024 * 1024)

        for _idx, (A, B) in iterator:
            try:
                diagnostics = diagnose_pair(A, B, ec_bound=args.ec_bound, pari=pari)
                results.append(diagnostics)

                result = diagnostics.result
                rank = result.rank
                rank_counts[rank] = rank_counts.get(rank, 0) + 1
                if result.has_concordant:
                    n_with_concordant += 1
                if result.has_chain_solution:
                    n_with_chain += 1
                    print(f"\n*** CHAIN SOLUTION: {result.summary()} ***")
                if diagnostics.mirror_hit_n:
                    n_with_mirror_hit += 1
            except Exception as exc:
                print(f"\n  Error on ({A},{B}): {exc}")

        elapsed = time.perf_counter() - t0

        print(f"\n{'─' * 72}")
        print(f"Analysed {len(results)} pairs in {elapsed:.1f}s")
        print("\nRank distribution:")
        for rank in sorted(rank_counts):
            print(f"  rank={rank}: {rank_counts[rank]} pairs")
        print(f"\nPairs with concordant N: {n_with_concordant}/{len(results)}")
        print(f"Pairs with chain-compatible N: {n_with_chain}/{len(results)}")
        print(f"Pairs with mirror hits: {n_with_mirror_hit}/{len(results)}")

        if n_with_chain > 0:
            print("\n*** HARBORTH SOLUTIONS EXIST! ***")

        top = args.top if args.top > 0 else len(results)
        conc_results = [diagnostics for diagnostics in results if diagnostics.result.has_concordant]
        if conc_results:
            print(f"\nPairs with concordant N (showing up to {top}):")
            conc_results.sort(
                key=lambda diagnostics: (
                    0 if diagnostics.result.has_chain_solution else 1,
                    diagnostics.best_candidate.combined_delta
                    if diagnostics.best_candidate is not None
                    else float("inf"),
                    diagnostics.result.A,
                    diagnostics.result.B,
                )
            )
            for diagnostics in conc_results[:top]:
                result = diagnostics.result
                best = diagnostics.best_candidate
                print(
                    f"  (A={result.A}, B={result.B}): rank={result.rank} "
                    f"concordant_n={result.concordant_n} "
                    f"mirror_hit_n={diagnostics.mirror_hit_n or 'none'} "
                    f"best_b={best.b if best is not None else 'none'} "
                    f"min_combined_delta={best.combined_delta if best is not None else 'none'}"
                )
                print()

        if args.out:
            report = {
                "max_hyp": args.max_hyp,
                "ec_bound": args.ec_bound,
                "n_pairs": len(results),
                "elapsed_s": round(elapsed, 2),
                "rank_distribution": rank_counts,
                "n_with_concordant": n_with_concordant,
                "n_with_chain_compatible": n_with_chain,
                "n_with_mirror_hit": n_with_mirror_hit,
                "pairs": [
                    _batch_pair_summary(diagnostics)
                    for diagnostics in results
                ],
            }
            with open(args.out, "w") as handle:
                json.dump(report, handle, indent=2)
            print(f"\nReport saved to {args.out}")


RUNNERS = {
    "chain": _run_chain,
    "chain-fast": _run_chain_fast,
    "concordant": _run_concordant,
    "ec": _run_ec,
    "parametric": _run_parametric,
}


__all__ = [
    "RUNNERS",
    "_resolve_parametric_limits",
    "_run_chain",
    "_run_chain_fast",
    "_run_concordant",
    "_run_ec",
    "_run_parametric",
]
