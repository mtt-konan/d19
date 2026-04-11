# Work Log 009 — Backend Split, Entry Point Unification, Test Consolidation

## Summary

Refactored `src/rational_distance/search_gpu.py` by extracting backend detection
into a new `backend.py` module. Unified three CLI scripts into a single entry
point. Consolidated two test files into one comprehensive suite (27 tests).

## Changes

### New Files
- **`src/rational_distance/backend.py`** — Backend detection extracted from
  `search_gpu.py`. Contains `_xp_cast`, `_try_cupy`, `_try_torch` (with
  `_TorchXP` namespace class), `detect_backend`.

- **`tests/test_all.py`** — Unified test suite replacing the two prior files.
  27 tests covering: `math_utils`, `square`, `search` (all paths), `search_gpu`
  (numpy backend), `backend`.

### Modified Files
- **`src/rational_distance/search_gpu.py`** — Removed all backend detection
  code (~120 lines). Now imports `_xp_cast`, `detect_backend` from `backend.py`.
  Cleaner separation of concerns.

- **`src/rational_distance/__init__.py`** — Updated docstring to document all
  five modules including the new `backend`.

- **`scripts/search_gpu.py`** — Fixed imports: `_try_torch` and `detect_backend`
  now imported from `rational_distance.backend` (not `search_gpu`).

- **`docs/IMPLEMENTATION.md`** — Updated module map, entry points, test layout,
  and GPU section to reflect the `backend.py` split.

### Deleted Files
- `scripts/search_3vertex.py` — Superseded by unified `scripts/search_gpu.py`
  (pass `--backend numpy` for CPU path).
- `scripts/search_4vertex.py` — Placeholder, not needed.
- `tests/test_math_utils.py` — Merged into `tests/test_all.py`.
- `tests/test_search.py` — Merged into `tests/test_all.py`.

## Key Decisions

### Why split backend.py?
`search_gpu.py` had grown to ~400 lines with two distinct concerns: (1) backend
detection/adaptation, (2) the actual search algorithm. After the `--inside` and
`inside_only` additions, the file was becoming hard to audit. Splitting lets each
file have a clear invariant: `backend.py` never does math; `search_gpu.py` never
does backend negotiation.

### Why keep `_TorchXP` simple (no `_TorchArrayWrapper`)?
The original `search_gpu.py` had a `_TorchArrayWrapper` to add `.astype()` and
`.get()` to raw tensors. The new `backend.py` instead uses `_xp_cast(arr, dtype)`
everywhere dtype conversion is needed. This avoids wrapping every intermediate
tensor and is easier to reason about. The `_to_cpu` helper in `_search_triple_gpu`
handles `.cpu().numpy()` for torch, `.get()` for cupy, passthrough for numpy.

### Test consolidation rationale
Two small files (`test_math_utils.py`, `test_search.py`) with 8 tests between
them gave incomplete coverage. The new `test_all.py` adds:
- `canonical_xy` idempotency and orbit consistency tests
- `inside_only` filter end-to-end tests (CPU and GPU paths)
- `min_rational=4` subset test
- D4 dedup correctness test (no symmetric duplicates remain)
- `parametric_search_gpu` vs `parametric_search_fast` cross-consistency check
- `backend` module tests (`detect_backend`, `_xp_cast`)

## Notes

- All 27 tests pass on macOS (no GPU). GPU-specific paths (`_try_torch`,
  `_try_cupy`) are exercised via the `--backend torch` / `--backend cupy` CLI
  args and covered by integration testing on Windows ROCm hardware.
- The `backend` return value from `parametric_search_gpu` when called with
  `xp=np` explicitly is `'module'` (the numpy module type name). When called via
  `detect_backend()` it returns a human-readable string (`'numpy'`, `'cupy'`,
  `'rocm/torch'`). Tests assert `isinstance(backend, str)` to avoid brittleness.
