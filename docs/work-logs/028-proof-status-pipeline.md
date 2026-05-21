# 028-proof-status-pipeline

## Summary

Added a brand-new pipeline that **mathematically proves** non-existence of full
chain solutions for reduced `(A, B)` pairs, accumulating verdicts into a
SQLite database. This is the first time the project produces statements of
the form *"this pair has been proven to have no chain solution"* rather than
*"this pair was not found to have a chain solution within the search range"*.

The new entry point is:

```bash
uv run python scripts/prove_no_solution.py --max-hyp 100 --db .cache/proofs.sqlite3
uv run python scripts/prove_no_solution.py --pair 7,45 --db .cache/proofs.sqlite3
uv run python scripts/prove_no_solution.py --db .cache/proofs.sqlite3 --report
```

For each reduced pair the workflow runs a pipeline of judgement methods,
records every attempt, and stops at the first terminal outcome
(`no_solution` / `solution_found`). The materialised verdict is stored in
`pair_proof_status`; the full attempt log is stored in `pair_method_attempts`.

## What Was Added

- New package: `src/rational_distance/proof_status/`
  - `types.py` — `PairProofStatus`, `MethodResult`, status / outcome literals
  - `schema.py` — SQLite schema, DAO, `connect_db` / `init_schema`
  - `methods.py` — six judgement methods (see below)
  - `workflow.py` — pipeline orchestration, incremental re-entry
- New CLI script: `scripts/prove_no_solution.py`
- New tests: `tests/test_proof_status.py` (18 tests)
- New theory doc: `docs/THEORY_DIRECTIONS_ADVANCED.md`
  (advanced directions: Heegner / L-functions / Chabauty / Brauer–Manin /
  Second descent / K3 surfaces)
- Doc updates:
  - `docs/DIRECTIONS.md` reading order + file table
  - `docs/PROJECT_STATUS.md` new §8 on long-term directions
  - `docs/THEORY_DIRECTIONS.md` pointer to ADVANCED at the top
  - `docs/IMPLEMENTATION.md` new maintenance zone `proof_status`
  - `docs/CURRENT_FINDINGS.md` clarification about `mod1680` not overlapping
    with `safe_sieve`
  - `README.md` quick-start examples

## Methods Implemented

Six methods, called in order. Stops at the first terminal verdict.

| # | Method | Mathematical content | Status |
|---|---|---|---|
| 1 | `safe_sieve` | 2-adic necessary conditions on reduced pairs (A, B both odd, (A+B) % 4 == 0) | ✅ rigorous, PARI-free |
| 2 | `factor_concordant` | enumerate all concordant N via `B² - A² = (h4-h3)(h4+h3)` factor pairs, then test full-chain closure | ✅ rigorous, PARI-free |
| 3 | `rank_zero` | PARI `ellrank` on `E: Y² = X(X+A²)(X+B²)`; if upper bound is 0 ⇒ only torsion ⇒ no concordant N | ✅ rigorous, requires PARI |
| 4 | `heegner` | Heegner point construction (方向五) | 🟡 stub, always returns `skipped` |
| 5 | `chabauty` | Chabauty / Quadratic Chabauty (方向七) | 🟡 stub |
| 6 | `brauer_manin` | Brauer–Manin obstruction (方向八) | 🟡 stub |

The three stubs are deliberately kept as named methods so that future
implementations only need to swap out the function body; no schema change is
required.

## SQLite Schema

`proof_meta` — schema version marker (rejects mismatched versions instead of
migrating, mirrors `chain_db.py`).

`pair_proof_status` — one row per `(A, B)`:

- `status` ∈ {`unknown`, `no_solution`, `solution_found`, `hard_case`}
- `method` — which method produced the verdict
- `rank_lower`, `rank_upper` — from PARI when available
- `concordant_n_count`, `chain_compatible_count` — from `factor_concordant`
- `notes`, `updated_at`

`pair_method_attempts` — append-only audit log:

- one row per `(A, B, method)` attempt
- includes outcome, JSON details, elapsed time

## Workflow Semantics

- Pipeline stops at the first method that returns `no_solution` or
  `solution_found`. Subsequent methods are not attempted for that pair.
- Pairs already terminal are skipped on subsequent runs unless
  `--rerun-terminal` is passed.
- `hard_case` pairs are *not* terminal — re-running will re-attempt them, so
  that adding a new method (e.g. replacing the Heegner stub with a real
  implementation) automatically upgrades existing hard cases.

## Smoke Test Result (max_hyp = 100)

```
Total reduced pairs:        254
├── no_solution (proven):   238   (93.7%)
│   ├── safe_sieve:         231
│   └── factor_concordant:    7
└── hard_case:               16   (6.3%)
```

All 16 hard cases survived `safe_sieve` and `factor_concordant`, and PARI
reported exact rank (`lower == upper`): 10 are rank 1, 6 are rank 2.

This is exactly where the advanced directions take over: Heegner point
construction can in principle decide every rank-1 pair, second descent and
Chabauty can handle the rank-2 group.

## Bug Fixed Mid-Implementation

The first version of `_aggregate_details` in `workflow.py` reset previously
accumulated `rank_lower` / `concordant_n_count` to None when a later method
(e.g. the Heegner stub) did not produce that key.

Root cause: `_coerce_int(value=None, default=existing)` returned `None`
instead of `existing`. The fix:

- `_coerce_int(None, default)` now returns `default` (treats None as "absent")
- `_aggregate_details` now takes the running accumulators as keyword arguments,
  not as part of the stale `existing` record

After the fix the `pair_proof_status` summary correctly shows
`rank=[1,1]`, `concordant_n_count=1`, `chain_compatible_count=0` for each
hard case, instead of all-`NULL`.

## Why Direction 6 (L-function derivatives) Was Reclassified

The original `THEORY_DIRECTIONS_ADVANCED.md` listed direction 6 as a "rank
discrimination pre-filter" for direction 5. But the smoke test shows PARI's
`ellrank` already gives exact rank for every hard case in this range. So
direction 6 in its original framing is redundant; it has been downgraded to
"expected payoff: low" and re-scoped to canonical height estimation via
Gross–Zagier.

## What This Pipeline Does **Not** Yet Do

- It does not implement Heegner point construction, Chabauty, or
  Brauer–Manin. Those are stubs.
- It does not try to scale to `max_hyp = 1000+` yet — that needs the
  caller to be patient with PARI throughput, not pipeline changes.

## Takeaway

The project for the first time has a **growable, append-only proof database**.
Every new advanced method only needs to:

1. Replace a stub in `methods.py`
2. Run `prove_no_solution.py --rerun-terminal=False` (default)
3. Hard cases get re-evaluated; new `proven_no_solution` rows accumulate

This is the natural unit of progress going forward.
