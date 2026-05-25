# Work Log 014 — EC Persistence, Resume, and Analysis

## Summary

This change adds an explicit SQLite-backed workflow for `scripts/search.py ec`.

The goal is not to speed up a first run. The goal is to make EC runs:

- resumable
- traceable
- analyzable without re-running search

The persisted chain now records:

- run metadata
- per-triple progress
- seeds
- quartic curve nodes
- parent-child edges from tangent / secant expansion
- candidate point outcomes
- final deduplicated points

## What Changed

### New persistence module

Added `src/rational_distance/ec_db.py`.

It manages:

- schema creation
- run matching for `--resume`
- loading already-found points
- per-triple commits
- point-level D4 continuity across resumed sessions

### New analysis module and CLI

Added:

- `src/rational_distance/ec_analysis.py`
- `scripts/analyze_ec_db.py`

The analysis layer can summarize a stored run, optionally filter by:

- run id
- triple `(p,q,r)`
- seed id
- region (`all`, `inside`, `outside`)

It also reuses the existing `scripts/visualize.py` HTML generator instead of
building a second visualization stack.

### EC search provenance

`search_ec.py` now has a database-aware path that records:

- seed records
- seed branches `(t, ±E)`
- orbit nodes
- tangent / secant edges
- candidate statuses such as:
  - `accepted`
  - `d4_duplicate`
  - `k_duplicate`
  - `side_filtered`
  - `inside_filtered`
  - `insufficient_rational`
  - `non_positive_k`
  - `infinite_k`

The default no-database EC path is still supported.

### CLI changes

`scripts/search.py ec` now accepts:

- `--db PATH`
- `--resume`

Without `--db`, the command behaves as before.

## Verification

Added tests covering:

- DB-backed EC run matches the plain EC result set
- `--resume` reuses the same run id
- known seed `(8,15,17, k=357/740)` is persisted
- provenance edges are stored with the expected parent counts
- analysis script emits JSON and HTML
- inside/outside analysis splits are consistent
