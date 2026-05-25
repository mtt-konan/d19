# Work Log 012 — EC Seed Search Vectorization and GPU Support

## Problem

The EC search (`scripts/search.py ec`) was taking ~300 seconds for
`--max-m 60 --max-k-num 800 --max-k-den 1600`, producing only 19 points.
Root cause: `find_seeds_for_triple` used a pure Python double loop
(~1.28 M iterations per triple, 1 474 triples → ~1.9 B iterations total).

By contrast, the parametric search does the same isqrt checks via numpy
vectorization and finishes a comparable range in ~20 s.

## Changes

### `src/rational_distance/search_ec.py`

**New helpers (seed-finding layer):**

- `_build_coprime_arrays(max_k_num, max_k_den)` — builds numpy int64
  arrays of all coprime (a, b) pairs once per `ec_search` call, avoiding
  repeated `gcd` checks in the inner loop.

- `_isqrt_arr(t)` — numpy vectorized perfect-square check identical to
  `_isqrt_vec` in `search.py`; handles float64 rounding via s+1 fallback.

- `_find_seeds_numpy(p, q, r, a_arr, b_arr, inside_only)` — vectorized
  seed finder: filters side-exclusion and inside_only in one pass, checks
  tB for all pairs simultaneously, then checks tD only for tB hits (early
  exit reduces tD work significantly). Returns `(a, b, sB, sD)` int tuples.

- `_find_seeds_gpu(xp, p, q, r, a_dev, b_dev, inside_only)` — GPU seed
  finder (cupy / torch). Computes tB and tD simultaneously on device,
  transfers only the rare hits to CPU, then **recomputes tB/tD from (a, b)
  using Python int arithmetic** for exact isqrt verification. This avoids
  any dependence on potentially overflowed device values.

- `_seeds_raw_to_fractions(raw, r)` — converts `(a, b, sB, sD)` integer
  tuples to `(k, dB, dD)` Fraction triples.

- `_INT64_SAFE_HALF = 2³¹ − 1` — safety bound: numpy path is used only
  when `(max_k_num + max_k_den) * r ≤ _INT64_SAFE_HALF`. Larger r falls
  back to exact Python-int arithmetic.

**Updated `find_seeds_for_triple`:**

- Dispatches to `_find_seeds_numpy` when int64-safe; falls back to the
  original scalar Python loop otherwise.
- Accepts optional `_a_arr`, `_b_arr` keyword arguments so `ec_search`
  can pass pre-built arrays and avoid rebuilding them per triple.

**Updated `ec_search`:**

- New `xp=None` parameter for GPU backend.
- Builds coprime arrays once before the triple loop.
- Routes to `_find_seeds_gpu` when `xp` is a real GPU backend
  (`xp is not None and xp is not np`); uses `find_seeds_for_triple`
  (with pre-built arrays) otherwise.
- Passes pre-built arrays to `find_seeds_for_triple` via `_a_arr`/`_b_arr`.

### `scripts/search.py`

- Added `--backend auto|cupy|torch|numpy` to the `ec` subcommand.
- `_run_ec` resolves the backend and passes `xp` to `ec_search`.

## Benchmark

Same parameters as the original slow run:

| Version | Time | Points |
|---|---|---|
| Before (pure Python) | ~301 s | 19 |
| After (numpy CPU) | ~20 s | 19 |

**15× speedup**, same results.  GPU path available via `--backend torch`
or `--backend cupy` for further acceleration on AMD/NVIDIA hardware.

## Test Suite

All 44 existing tests pass.  Test suite wall-clock time dropped from ~47 s
to ~3 s (same improvement, since tests call `find_seeds_for_triple` directly).

## Search Space Analysis

EC results (`--max-m 60 --max-k-num 800 --max-k-den 1600 --inside`), 19 points:

| Denominator range | Count | % |
|---|---|---|
| ≤ 100 | 2 | 11% |
| 101–1 000 | 3 | 16% |
| 1 001–10 000 | 5 | 26% |
| 10 001–100 000 | 7 | 37% |
| > 100 000 | 2 | 11% |

The large-denominator points come from EC orbit expansion, not from seeds
directly — seeds themselves tend to have small denominators.  Reducing
`max_k_den` would reduce seed coverage but the orbit step still reaches
distant points.
