"""EC CLI runner."""

from __future__ import annotations

import argparse
import sys
import time

from .output import _print_four_vertex, _print_summary, _print_table, _save_json


def _run_ec(args: argparse.Namespace) -> None:
    from rational_distance.backend import _try_torch, detect_backend
    from rational_distance._legacy.ec_db import ECSearchStore
    from rational_distance._legacy.search_ec import ec_search

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


__all__ = ["_run_ec"]
