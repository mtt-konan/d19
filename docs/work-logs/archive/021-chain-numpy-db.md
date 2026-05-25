# Work Log 021 — Chain-Fast: numpy Acceleration + SQLite Persistence

## Summary

Added numpy vectorisation to `search_chain_fast.py` and implemented SQLite
persistence (`chain_db.py`) with full CLI integration. All 101 tests pass.

---

## Changes

### `src/rational_distance/search_chain_fast.py`

- New `_numpy_inner(i, triples, s_arr, t_arr, results, seen, near_miss_callback)`
  — vectorised inner T2 loop using numpy int64 arrays.
- Updated `find_chains_fast` signature: added `backend`, `start_t1`,
  `near_miss_callback` parameters (fully backward-compatible).
- `backend="auto"` (default): uses numpy when available and `max_hyp ≤ 36000`.
- Overflow guard: `_NUMPY_MAX_HYP = 36000` — derived from sq3/sq4 ≤ 5H⁴ must
  fit in int64 (< 2⁶³−1 ≈ 9.22e18); safe threshold is H ≤ 36 853.
- Float sqrt prefilter with exact ±1 correction (c3e | c3p1 | c3m1) for each
  of C3 and C4; exact `isqrt` verification for every actual hit.
- `near_miss_callback` fires in both numpy and python paths for C3-pass/C4-fail
  pairs, passing corrected h4c (not raw h4f).
- `start_t1` enables resume: outer loop begins at T1 index `start_t1`.

### `src/rational_distance/chain_db.py` (new, ~210 lines)

SQLite persistence layer for chain-fast runs.

**Tables:**

| Table | Purpose |
|-------|---------|
| `chain_runs` | One row per run: parameters, status, timing, progress |
| `chain_solutions` | Discovered solutions (empty until conjecture resolved) |
| `chain_near_misses` | C3-pass/C4-fail pairs for proximity analysis |

**API:**

- `connect_db(path)` — open/create DB, enable WAL + FK
- `init_schema(conn)` — create tables if absent
- `start_run(conn, max_hyp, backend, n_triples)` → `run_id`
- `resume_run(conn, max_hyp)` → `(run_id, last_t1_index)` | `None`
- `checkpoint_t1(conn, run_id, t1_index, near_miss_count)`
- `record_solution(conn, run_id, result)` — `INSERT OR IGNORE` (dedup)
- `record_near_miss(conn, run_id, a, b_val, c, d, ...)` — computes deficits
- `finish_run(conn, run_id, found_count, elapsed)`
- `get_near_misses(conn, run_id, limit)` → sorted by sq4_deficit ASC
- `get_run(conn, run_id)` → dict | None

### `scripts/search.py`

Updated `_run_chain_fast` and added argparse options:

| Flag | Default | Effect |
|------|---------|--------|
| `--backend {auto,numpy,python}` | `auto` | Select vectorisation backend |
| `--db PATH` | None | Enable SQLite persistence |
| `--resume` | False | Resume last incomplete run in `--db` |
| `--near-miss` | False | Log C3-pass/C4-fail pairs to `--db` |

Example:

```bash
uv run python scripts/search.py chain-fast \
    --max-hyp 20000 --backend numpy --db results/chain.db --near-miss
```

### `tests/test_all.py`

- Added `import pytest` to module-level imports.
- `TestChainFastNumpy` (6 tests): numpy==python output, auto-backend, forced
  numpy, overflow guard raises ValueError, near-miss count parity, start_t1
  returns subset.
- `TestChainDB` (5 tests): schema creation, start/finish run, solution dedup,
  checkpoint+resume, near-miss deficit calculation.

---

## Performance (Apple Silicon, max_hyp = 20 000)

| Backend | Time |
|---------|------|
| Python  | ~8 s |
| numpy   | ~2 s |

Speedup ~4× at this scale. At larger `max_hyp` the batch size grows linearly
so the numpy advantage improves further.

---

## Design decisions

**Overflow threshold 36 000 (not 45 000):** N = s2r·(s1−t1) + A can be as
large as ~2H², so sq3 ≤ H⁴ + 4H⁴ = 5H⁴. The safe bound is
H ≤ ((2⁶³−1)/5)^¼ ≈ 36 853; we use 36 000 for conservatism.

**±1 correction instead of pure round:** float64 sqrt is accurate to ≈ 0.5 ULP
in the result, so for sq3 ≤ 5·36000⁴ ≈ 8.4e18, the rounding error in sqrt is
< 1. Checking h, h±1 covers all cases without any exact integer sqrt in the
hot path; exact `isqrt` is reserved for the handful of actual hits.

**Corrected h4c in near_miss_callback:** rubber-duck review caught that passing
the raw `h4f` (before ±1 correction) would make proximity deficits off by 1.
The callback now always receives the closest integer root.
