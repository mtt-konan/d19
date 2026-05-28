"""Chain CLI runner."""

from __future__ import annotations

import argparse
import json
import time

_RESULT_FLUSH_SIZE = 1000
_CHECKPOINT_INTERVAL = 250


def _largest_result_by_max_side(results):
    if not results:
        return None
    return max(
        results,
        key=lambda result: (
            max(result.a, result.b, result.c, result.d),
            result.a + result.b + result.c + result.d,
            (result.a + result.c) * (result.b + result.d),
            result.a,
            result.b,
            result.c,
            result.d,
        ),
    )


def _resolve_result_mode(args: argparse.Namespace) -> str:
    return "diagonal_sign" if getattr(args, "diagonal_sign_sieve", False) else "default"


def _experimental_count_before(
    args: argparse.Namespace,
    results,
    search_stats,
    *,
    result_mode: str,
    result_state=None,
    default_mode_available: bool = False,
    count_cached_results=None,
    conn=None,
) -> int:
    if not getattr(args, "diagonal_sign_sieve", False):
        return len(results)

    if conn is not None and count_cached_results is not None and default_mode_available:
        return count_cached_results(
            conn,
            args.max_val,
            result_mode="default",
            require_square=args.require_square,
        )

    if result_state is not None and int(result_state["results_max_val"]) == args.max_val:
        field = "pre_filter_square_count" if args.require_square else "pre_filter_count"
        return int(result_state[field])

    fallback = len(results) + int(search_stats.diagonal_sign_filtered)
    if args.require_square:
        return max(fallback, int(search_stats.pre_diagonal_square_results))
    return max(fallback, int(search_stats.pre_diagonal_results))


def _run_chain(args: argparse.Namespace) -> None:
    from rational_distance._legacy.search_chain import (
        ChainSearchStats,
        _iter_pythagorean_pairs,
        build_adjacency_from_rows,
        find_chains,
        iter_chain_results,
        results_to_json,
    )

    if getattr(args, "resume", False) and not getattr(args, "db", None):
        raise SystemExit("--resume requires --db")

    result_mode = _resolve_result_mode(args)

    print("=" * 72)
    print("Pythagorean 4-cycle search — rectangle / unit-square problem")
    print(
        f"  max_val={args.max_val}, require_square={args.require_square}, result_mode={result_mode}"
    )
    if getattr(args, "db", None):
        print(f"  db={args.db}  resume={bool(getattr(args, 'resume', False))}")
    print("=" * 72)

    t0 = time.perf_counter()
    results = []
    largest_result = None
    cache_state_after = None
    result_state_after = None
    default_mode_available = False
    search_stats = ChainSearchStats()
    conn = None
    cached_result_counter = None

    if not getattr(args, "db", None):
        results = find_chains(
            max_val=args.max_val,
            require_square=args.require_square,
            diagonal_sign_sieve=getattr(args, "diagonal_sign_sieve", False),
            canonical=True,
            progress=not args.no_progress,
            stats=search_stats,
        )
        largest_result = _largest_result_by_max_side(results)
    else:
        from rational_distance._legacy.chain_cache_db import (
            RESULT_MODE_DEFAULT,
            checkpoint_run,
            connect_db,
            count_cached_results,
            finish_run,
            get_adjacency_max_val,
            get_cache_state,
            get_result_state,
            get_resumable_run,
            init_schema,
            insert_adjacency_rows,
            insert_results,
            load_cached_adjacency_rows,
            load_cached_results,
            start_run,
            update_adjacency_max_val,
            update_result_state,
        )
        cached_result_counter = count_cached_results

        conn = connect_db(args.db)
        init_schema(conn)

        cached_adj_max = get_adjacency_max_val(conn)
        result_state_before = get_result_state(conn, result_mode=result_mode)
        cached_results_max = int(result_state_before["results_max_val"])

        default_result_state = get_result_state(conn, result_mode=RESULT_MODE_DEFAULT)
        default_mode_available = int(default_result_state["results_max_val"]) >= args.max_val

        run_id: int | None = None
        resumable_run = None
        if getattr(args, "resume", False):
            resumable_run = get_resumable_run(
                conn,
                requested_max_val=args.max_val,
                result_mode=result_mode,
            )
            if resumable_run is not None:
                run_id = int(resumable_run["id"])
                resume_a = int(resumable_run["last_completed_a"]) + 1
                print(f"Resuming chain cache run {run_id} from a={resume_a} (mode={result_mode})")
            else:
                print("No resumable chain cache run found; starting a fresh cached run.")

        if run_id is None:
            run_id = start_run(
                conn,
                requested_max_val=args.max_val,
                result_mode=result_mode,
                require_square=args.require_square,
                starting_adjacency_max_val=cached_adj_max,
                starting_results_max_val=cached_results_max,
            )

        build_adjacency_s = 0.0
        load_adjacency_s = 0.0
        search_cycles_s = 0.0
        query_results_s = 0.0
        new_adjacency_edges = 0
        new_results = 0 if resumable_run is None else int(resumable_run["new_results"])

        if resumable_run is not None:
            search_stats.pre_diagonal_results = int(resumable_run["pre_filter_count"])
            search_stats.pre_diagonal_square_results = int(
                resumable_run["pre_filter_square_count"]
            )
            search_stats.diagonal_sign_filtered = int(resumable_run["diagonal_sign_filtered"])
            search_stats.emitted_results = int(resumable_run["new_results"])

        if cached_adj_max < args.max_val:
            build_started = time.perf_counter()
            row_buffer: list[tuple[int, int, int]] = []

            def _flush_adjacency_rows() -> None:
                nonlocal new_adjacency_edges
                if not row_buffer:
                    return
                new_adjacency_edges += insert_adjacency_rows(conn, row_buffer)
                row_buffer.clear()

            if cached_adj_max == 0:
                ranges = [
                    (
                        1,
                        args.max_val,
                        1,
                        args.max_val,
                        "Building Pythagorean pairs",
                    )
                ]
            else:
                ranges = [
                    (
                        1,
                        cached_adj_max,
                        cached_adj_max + 1,
                        args.max_val,
                        "Extending adjacency (old rows x new cols)",
                    ),
                    (
                        cached_adj_max + 1,
                        args.max_val,
                        1,
                        args.max_val,
                        "Extending adjacency (new rows x full cols)",
                    ),
                ]

            for start_a, stop_a, b_start, b_stop, desc in ranges:
                for row in _iter_pythagorean_pairs(
                    start_a,
                    stop_a,
                    b_start,
                    b_stop,
                    progress=not args.no_progress,
                    desc=desc,
                ):
                    row_buffer.append(row)
                    if len(row_buffer) >= 50000:
                        _flush_adjacency_rows()
                _flush_adjacency_rows()

            update_adjacency_max_val(conn, args.max_val)
            build_adjacency_s = time.perf_counter() - build_started
            cached_adj_max = args.max_val

        if cached_results_max < args.max_val:
            if resumable_run is None:
                start_a = cached_results_max + 1
            else:
                start_a = int(resumable_run["last_completed_a"]) + 1

            if start_a <= args.max_val:
                load_started = time.perf_counter()
                rows = load_cached_adjacency_rows(conn, args.max_val)
                adj, hyp = build_adjacency_from_rows(args.max_val, iter(rows))
                load_adjacency_s = time.perf_counter() - load_started

                result_buffer = []
                checkpoint_state = {"last_a": start_a - 1}

                def _flush_results() -> None:
                    nonlocal new_results
                    if not result_buffer:
                        return
                    new_results += insert_results(
                        conn,
                        result_mode=result_mode,
                        results=result_buffer,
                    )
                    result_buffer.clear()

                def _on_result(result) -> None:
                    result_buffer.append(result)
                    if len(result_buffer) >= _RESULT_FLUSH_SIZE:
                        _flush_results()

                def _checkpoint(a: int) -> None:
                    checkpoint_run(
                        conn,
                        run_id,
                        a,
                        new_results=new_results,
                        pre_filter_count=search_stats.pre_diagonal_results,
                        pre_filter_square_count=search_stats.pre_diagonal_square_results,
                        diagonal_sign_filtered=search_stats.diagonal_sign_filtered,
                    )

                def _on_outer_complete(a: int) -> None:
                    checkpoint_state["last_a"] = a
                    if a % _CHECKPOINT_INTERVAL == 0 or a == args.max_val:
                        _flush_results()
                        _checkpoint(a)

                search_started = time.perf_counter()
                iter_chain_results(
                    adj,
                    hyp,
                    max_val=args.max_val,
                    require_square=False,
                    diagonal_sign_sieve=getattr(args, "diagonal_sign_sieve", False),
                    canonical=True,
                    progress=not args.no_progress,
                    start_a=start_a,
                    stats=search_stats,
                    result_callback=_on_result,
                    outer_complete_callback=_on_outer_complete,
                )
                _flush_results()
                _checkpoint(checkpoint_state["last_a"])
                search_cycles_s = time.perf_counter() - search_started

            total_result_count = count_cached_results(
                conn,
                args.max_val,
                result_mode=result_mode,
                require_square=False,
            )
            total_square_count = count_cached_results(
                conn,
                args.max_val,
                result_mode=result_mode,
                require_square=True,
            )
            update_result_state(
                conn,
                result_mode=result_mode,
                results_max_val=args.max_val,
                result_count=total_result_count,
                square_result_count=total_square_count,
                pre_filter_count=int(result_state_before["pre_filter_count"])
                + int(search_stats.pre_diagonal_results),
                pre_filter_square_count=int(result_state_before["pre_filter_square_count"])
                + int(search_stats.pre_diagonal_square_results),
            )
            cached_results_max = args.max_val

        query_started = time.perf_counter()
        results = load_cached_results(
            conn,
            args.max_val,
            result_mode=result_mode,
            require_square=args.require_square,
        )
        largest_result = _largest_result_by_max_side(results)
        query_results_s = time.perf_counter() - query_started
        cache_state_after = get_cache_state(conn, result_mode=result_mode)
        result_state_after = get_result_state(conn, result_mode=result_mode)
        default_result_state = get_result_state(conn, result_mode=RESULT_MODE_DEFAULT)
        default_mode_available = int(default_result_state["results_max_val"]) >= args.max_val

        finish_run(
            conn,
            run_id,
            elapsed_s=time.perf_counter() - t0,
            new_adjacency_edges=new_adjacency_edges,
            new_results=new_results,
            pre_filter_count=search_stats.pre_diagonal_results,
            pre_filter_square_count=search_stats.pre_diagonal_square_results,
            diagonal_sign_filtered=search_stats.diagonal_sign_filtered,
            build_adjacency_s=build_adjacency_s,
            load_adjacency_s=load_adjacency_s,
            search_cycles_s=search_cycles_s,
            query_results_s=query_results_s,
        )
    elapsed = time.perf_counter() - t0

    total_before_experimental = _experimental_count_before(
        args,
        results,
        search_stats,
        result_mode=result_mode,
        result_state=result_state_after,
        default_mode_available=default_mode_available,
        count_cached_results=cached_result_counter,
        conn=conn,
    )
    diagonal_sign_filtered = (
        total_before_experimental - len(results)
        if getattr(args, "diagonal_sign_sieve", False)
        else 0
    )

    if conn is not None:
        conn.close()

    largest_result = _largest_result_by_max_side(results)

    n_sq = sum(1 for result in results if result.square_ok)
    print(f"\nFound {len(results)} canonical 4-cycles in {elapsed:.1f}s")
    print(f"  {n_sq} satisfy unit-square constraint (a+c == b+d)")
    print(f"  {len(results) - n_sq} are rectangle-only solutions")
    if getattr(args, "diagonal_sign_sieve", False):
        print(
            "  experimental diagonal_sign_sieve: "
            f"kept {len(results)}/{total_before_experimental}, filtered {diagonal_sign_filtered}"
        )
    if cache_state_after is not None:
        print(
            "  cache high-water: "
            f"result_mode={result_mode}  adjacency_max_val={cache_state_after[0]}  "
            f"results_max_val={cache_state_after[1]}"
        )
    if largest_result is not None:
        max_side = max(largest_result.a, largest_result.b, largest_result.c, largest_result.d)
        rect_w, rect_h = largest_result.rectangle
        print(
            "  largest by max side: "
            f"({largest_result.a},{largest_result.b},{largest_result.c},{largest_result.d}) "
            f"max_side={max_side} rect={rect_w}×{rect_h}"
        )

    top = args.top if args.top > 0 else len(results)
    if results:
        print()
        for result in results[:top]:
            print(str(result))
            print()
        if len(results) > top:
            print(f"  ... {len(results) - top} more rows suppressed (use --top 0 to show all)")

    if args.out:
        data = results_to_json(
            results,
            args.max_val,
            args.require_square,
            elapsed,
            experimental_filters={
                "diagonal_sign_sieve": bool(getattr(args, "diagonal_sign_sieve", False)),
                "count_before_filters": total_before_experimental,
                "count_filtered_out": diagonal_sign_filtered,
            }
            if getattr(args, "diagonal_sign_sieve", False)
            else None,
        )
        with open(args.out, "w") as handle:
            json.dump(data, handle, indent=2)
        print(f"\nResults saved to {args.out}")


__all__ = ["_run_chain"]
