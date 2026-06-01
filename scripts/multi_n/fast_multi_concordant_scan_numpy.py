#!/usr/bin/env python3
"""Numpy sort-and-group pivot-on-N multi-concordant-N scan (scales to max_hyp=5e6+).

`fast_multi_concordant_pairs` stores relations in Python dicts; at max_hyp=2e6
that is ~5.3 GiB to hold what is fundamentally ~0.6 GB of raw (n, a) data, and
the box OOMs at 2e6. This variant stores the (n, a) relation stream in **numpy
arrays** and groups by two in-place sorts instead of two dicts.

Memory design (why it fits ~10-12M in 8 GiB)
--------------------------------------------
Stage 1 sorts the relations by N with ``argsort(kind="quicksort")`` (introsort:
no O(n) stable-merge scratch buffer) and reorders both arrays, then keeps the
multi-element bucket boundaries as **numpy int arrays** (never ``.tolist()`` —
millions of Python ints are ~0.3 GB at 5e6).

Stage 2: for each N-bucket emit every coprime not-both-even A-pair ``(ai, aj)``
as ``pkey = ai*(max_hyp+1) + aj`` into a growable int64 buffer, optionally
**sharded by ``ai % shards``** to bound that buffer (the bucket walk is cheap to
repeat); sort the buffer and count run lengths — a pkey occurring k>=2 times is
a pair sharing k distinct concordant N.

Output aggregates match `fast_multi_concordant_scan.py` exactly (verified at
1e6 = 111,090 and 2e6 = 226,120).

Three orthogonal speed/RAM optimizations (each falls back gracefully):

* ``--shards K`` splits pair-emit by ``ai % K`` to bound the pair buffer
  (5M: 5.92 -> 3.86 GiB at K=4).
* Cython kernel ``_concordant_gen`` (built via ``_build_gen.py``) runs the SPF
  sieve + divisor enumeration *and* the per-bucket pair emission in C, writing
  straight into numpy arrays (5M total 270s -> 76s). The ``.so`` is platform
  specific and not committed; without it the scanner uses the pure-Python path.
* ``--workers W`` (``scan_numpy_parallel``) generates+sorts once, publishes the
  sorted relations via ``multiprocessing.shared_memory``, and runs W ai-shards
  of emit+dedup in parallel processes (5M 76s -> 56s on 2 cores).
"""

from __future__ import annotations

import argparse
import resource
import sys
import time
from collections import defaultdict
from math import gcd
from pathlib import Path
from typing import cast

import numpy as np

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

_CHUNK = 1 << 22  # 4.19M relations per numpy chunk


def _collect_relations(max_hyp: int, use_cython: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Return (n[], a[]) of every concordant (A, N) with 2<=A<=max_hyp.

    Uses the compiled Cython kernel ``_concordant_gen`` when available (the SPF
    sieve + per-A divisor enumeration + emission run in C, ~80x faster than the
    pure-Python generator); otherwise streams ``iter_concordant_a_n`` into
    chunked numpy arrays.
    """
    if use_cython:
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            import _concordant_gen  # type: ignore[import-not-found]

            return _concordant_gen.generate(max_hyp)
        except ImportError:
            pass

    from rational_distance.concordant.fast_multi_n import iter_concordant_a_n

    n_chunks: list[np.ndarray] = []
    a_chunks: list[np.ndarray] = []
    buf_n = np.empty(_CHUNK, dtype=np.int64)
    buf_a = np.empty(_CHUNK, dtype=np.int32)
    i = 0
    for a, n in iter_concordant_a_n(max_hyp):
        buf_n[i] = n
        buf_a[i] = a
        i += 1
        if i == _CHUNK:
            n_chunks.append(buf_n)
            a_chunks.append(buf_a)
            buf_n = np.empty(_CHUNK, dtype=np.int64)
            buf_a = np.empty(_CHUNK, dtype=np.int32)
            i = 0
    n_chunks.append(buf_n[:i].copy())
    a_chunks.append(buf_a[:i].copy())
    del buf_n, buf_a
    n_arr = np.concatenate(n_chunks)
    a_arr = np.concatenate(a_chunks)
    return n_arr, a_arr


def _grouped(max_hyp: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Sort relations by N; return (n_sorted, a_sorted, bucket_starts, bucket_ends)
    where only multi-element (>=2) buckets are kept, as numpy int arrays."""
    n_arr, a_arr = _collect_relations(max_hyp)

    # quicksort (introsort) avoids the O(n) scratch buffer a stable mergesort
    # needs; grouping does not require a stable order.
    order = np.argsort(n_arr, kind="quicksort")
    n_arr = n_arr[order]
    a_arr = a_arr[order]
    del order

    change = np.flatnonzero(np.diff(n_arr)) + 1
    starts = np.concatenate(([0], change))
    ends = np.concatenate((change, [n_arr.shape[0]]))
    del change
    keep = (ends - starts) >= 2
    ms = starts[keep]
    me = ends[keep]
    del starts, ends, keep
    return n_arr, a_arr, ms, me


def _emit_shard_py(
    n_arr: np.ndarray,
    a_arr: np.ndarray,
    ms: np.ndarray,
    me: np.ndarray,
    factor: int,
    shard: int,
    shards: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Pure-Python fallback for the Cython ``emit_pairs`` kernel."""
    nbuckets = ms.shape[0]
    cap = 1 << 20
    pkeys = np.empty(cap, dtype=np.int64)
    nns = np.empty(cap, dtype=np.int64)
    cnt = 0
    for bi in range(nbuckets):
        s = int(ms[bi])
        e = int(me[bi])
        bucket = sorted(a_arr[s:e].tolist())
        nval = int(n_arr[s])
        m = len(bucket)
        for i in range(m):
            ai = bucket[i]
            if shards > 1 and (ai % shards) != shard:
                continue
            ai_odd = ai & 1
            for j in range(i + 1, m):
                aj = bucket[j]
                if not ai_odd and not (aj & 1):
                    continue
                if gcd(ai, aj) != 1:
                    continue
                if cnt == cap:
                    cap <<= 1
                    pkeys.resize(cap, refcheck=False)
                    nns.resize(cap, refcheck=False)
                pkeys[cnt] = ai * factor + aj
                nns[cnt] = nval
                cnt += 1
    return pkeys[:cnt], nns[:cnt]


def scan_numpy(max_hyp: int, shards: int = 1) -> dict[tuple[int, int], list[int]]:
    n_arr, a_arr, ms, me = _grouped(max_hyp)
    factor = max_hyp + 1

    cy = None
    maxbucket = 0
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import _concordant_gen as cy  # type: ignore[import-not-found,no-redef]

        maxbucket = int((me - ms).max()) if ms.shape[0] else 0
    except ImportError:
        cy = None

    result: dict[tuple[int, int], list[int]] = {}

    for shard in range(shards):
        if cy is not None:
            pk, nn = cy.emit_pairs(n_arr, a_arr, ms, me, factor, maxbucket, shard, shards)
        else:
            pk, nn = _emit_shard_py(n_arr, a_arr, ms, me, factor, shard, shards)
        if shard == shards - 1:
            # relations no longer needed; free before the (memory-heavy) pair sort
            del n_arr, a_arr, ms, me
        if pk.shape[0] == 0:
            continue
        korder = np.argsort(pk, kind="quicksort")
        pk = pk[korder]
        nn = nn[korder]
        del korder
        uniq, first_idx, counts = np.unique(pk, return_index=True, return_counts=True)
        mm = counts >= 2
        for pkey, idx, c in zip(
            uniq[mm].tolist(), first_idx[mm].tolist(), counts[mm].tolist(), strict=True
        ):
            a = pkey // factor
            b = pkey % factor
            result[(a, b)] = sorted(nn[idx : idx + c].tolist())
        del pk, nn, uniq, first_idx, counts, mm

    return result


def _dedup_shard(pk: np.ndarray, nn: np.ndarray, factor: int) -> dict[tuple[int, int], list[int]]:
    """Sort one shard's (pkey, N) buffer and collect the k>=2 multi-N pairs."""
    out: dict[tuple[int, int], list[int]] = {}
    if pk.shape[0] == 0:
        return out
    korder = np.argsort(pk, kind="quicksort")
    pk = pk[korder]
    nn = nn[korder]
    del korder
    uniq, first_idx, counts = np.unique(pk, return_index=True, return_counts=True)
    mm = counts >= 2
    for pkey, idx, c in zip(
        uniq[mm].tolist(), first_idx[mm].tolist(), counts[mm].tolist(), strict=True
    ):
        out[(pkey // factor, pkey % factor)] = sorted(nn[idx : idx + c].tolist())
    return out


def _parallel_worker(args: tuple) -> dict[tuple[int, int], list[int]]:
    """Worker (spawn-safe): attach the shared sorted-relation arrays, run the
    Cython emit for one ai-shard, then sort+dedup that shard locally and return
    its (small) pair->N dict. Shards partition by ai, so dicts never collide."""
    from multiprocessing import shared_memory

    (shard, nshards, factor, maxbucket, n_name, a_name, ms_name, me_name, nlen, mlen) = args
    sys.path.insert(0, str(Path(__file__).parent))
    import _concordant_gen as cy  # type: ignore[import-not-found]

    shn = shared_memory.SharedMemory(name=n_name)
    sha = shared_memory.SharedMemory(name=a_name)
    shms = shared_memory.SharedMemory(name=ms_name)
    shme = shared_memory.SharedMemory(name=me_name)
    try:
        n_arr = np.ndarray((nlen,), dtype=np.int64, buffer=shn.buf)
        a_arr = np.ndarray((nlen,), dtype=np.int32, buffer=sha.buf)
        ms = np.ndarray((mlen,), dtype=np.int64, buffer=shms.buf)
        me = np.ndarray((mlen,), dtype=np.int64, buffer=shme.buf)
        pk, nn = cy.emit_pairs(n_arr, a_arr, ms, me, factor, maxbucket, shard, nshards)
        del n_arr, a_arr, ms, me
        return _dedup_shard(pk, nn, factor)
    finally:
        shn.close()
        sha.close()
        shms.close()
        shme.close()


def scan_numpy_parallel(max_hyp: int, workers: int) -> dict[tuple[int, int], list[int]]:
    """Step-3 parallel driver: generate+sort relations once (serial), publish
    them in shared memory, then run ``workers`` ai-shards of emit+dedup in
    parallel processes. Falls back to serial ``scan_numpy`` if Cython missing."""
    import multiprocessing as mp
    from multiprocessing import shared_memory

    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import _concordant_gen  # type: ignore[import-not-found]  # noqa: F401
    except ImportError:
        return scan_numpy(max_hyp, shards=workers)

    n_arr, a_arr, ms, me = _grouped(max_hyp)
    factor = max_hyp + 1
    maxbucket = int((me - ms).max()) if ms.shape[0] else 0
    nlen = int(n_arr.shape[0])
    mlen = int(ms.shape[0])

    blocks = []

    def _publish(arr: np.ndarray) -> str:
        shm = shared_memory.SharedMemory(create=True, size=max(arr.nbytes, 1))
        view = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf)
        view[:] = arr
        blocks.append(shm)
        return shm.name

    # publish + pool inside the try so a failure partway through _publish (e.g.
    # /dev/shm full) still unlinks the blocks already created in the finally.
    result: dict[tuple[int, int], list[int]] = {}
    try:
        n_name = _publish(n_arr)
        a_name = _publish(a_arr)
        ms_name = _publish(ms)
        me_name = _publish(me)
        # parent's private copies no longer needed; workers read shared memory
        del n_arr, a_arr, ms, me

        args = [
            (r, workers, factor, maxbucket, n_name, a_name, ms_name, me_name, nlen, mlen)
            for r in range(workers)
        ]
        ctx = mp.get_context("spawn")
        with ctx.Pool(workers) as pool:
            for d in pool.map(_parallel_worker, args):
                result.update(d)
    finally:
        for shm in blocks:
            shm.close()
            shm.unlink()
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Numpy sort-and-group pivot-on-N scan")
    _ = parser.add_argument("--max-hyp", type=int, default=5000000)
    _ = parser.add_argument(
        "--shards", type=int, default=1, help="split pair-emit by ai%%shards to bound RAM"
    )
    _ = parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="parallel processes over ai-shards (step 3); >1 overrides --shards",
    )
    _ = parser.add_argument("--out", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    max_hyp = cast(int, args.max_hyp)
    shards = cast(int, args.shards)
    workers = cast(int, args.workers)

    t0 = time.perf_counter()
    if workers > 1:
        pairs = scan_numpy_parallel(max_hyp, workers=workers)
    else:
        pairs = scan_numpy(max_hyp, shards=shards)
    elapsed = time.perf_counter() - t0
    peak_gib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**2
    child_gib = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024**2

    k_hist: dict[int, int] = defaultdict(int)
    n_closure = 0
    closure_examples: list[tuple[int, int, list[int]]] = []
    for (a, b), ns in pairs.items():
        k_hist[len(ns)] += 1
        target = a + b
        ns_set = set(ns)
        if any((target - x) != x and (target - x) in ns_set and target - x > 0 for x in ns):
            n_closure += 1
            if len(closure_examples) < 10:
                closure_examples.append((a, b, ns))

    print(f"max_hyp={max_hyp} shards={shards}")
    print(f"multi-N pairs: {len(pairs)}")
    print(f"k histogram: {dict(sorted(k_hist.items()))}")
    print(f"closure pairs (N1+N2=A+B): {n_closure}")
    if closure_examples:
        print(f"closure examples: {closure_examples}")
    if workers > 1:
        print(
            f"elapsed: {elapsed:.2f}s  peak RSS parent: {peak_gib:.2f} GiB  "
            f"largest child: {child_gib:.2f} GiB  workers: {workers}"
        )
    else:
        print(f"elapsed: {elapsed:.2f}s  peak RSS: {peak_gib:.2f} GiB")

    out_path = cast("Path | None", args.out)
    if out_path is not None:
        import json

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as fh:
            for (a, b), ns in sorted(pairs.items()):
                _ = fh.write(
                    json.dumps(
                        {
                            "A": a,
                            "B": b,
                            "n_concordant": len(ns),
                            "concordant_N": ns,
                            "A_plus_B": a + b,
                        }
                    )
                    + "\n"
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
