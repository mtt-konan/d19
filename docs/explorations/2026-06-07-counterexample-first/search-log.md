# Search Log

## Metadata

| Field | Value |
|---|---|
| Date | 2026-06-07 |
| Commit | `3a44a6f08a8d9e7af40e4d77c39882af26ea42fe` |
| Scope | full-space coprime + non-coprime `(A,B)` with `A < B <= max_hyp` |
| Counterexample predicate | full-plane GEN-CLOSURE |
| Concordant `N` enumeration | exact divisor enumeration; no `N` upper bound |
| Main data dir | `results/counterexample_first/2026-06-07/` |

## Baseline

| Command | Outcome |
|---|---|
| `git status --short --branch` | branch `main...origin/main`; worktree has untracked audit/exploration docs |
| `git rev-parse HEAD` | `3a44a6f08a8d9e7af40e4d77c39882af26ea42fe` |
| `uv run pytest -q` | `335 passed, 2 warnings` |

The first attempt to run `scripts/multi_n/noncoprime_full_scan_fast.py` failed because the local Cython module `_concordant_gen` was not built. Root cause was environmental, not mathematical: the project expects a machine-local `.so`.

Build command:

```bash
uv run python scripts/multi_n/_build_gen.py build_ext --inplace
```

After building, the fast full-space scanner reproduced the expected small-bound behavior.

## Exact GEN-CLOSURE Scans

All scans used:

```text
gcd_aware_kills -> chain_closure_mod_sieve(full_plane=True) -> exact GEN-CLOSURE
```

| Bound | Command | Multi-N pairs | D_g killed | Full-plane mod killed | Exact survivors | Closures |
|---:|---|---:|---:|---:|---:|---:|
| 10,000 | `PYTHONPATH=src uv run python scripts/multi_n/noncoprime_full_scan_fast.py --max-hyp 10000 --workers 1` | 17,748 | 11,318 | 5,564 | 866 | 0 |
| 100,000 | `PYTHONPATH=src uv run python scripts/multi_n/noncoprime_full_scan_fast.py --max-hyp 100000 --workers 4` | 324,925 | 200,707 | 104,999 | 19,219 | 0 |
| 1,000,000 | `PYTHONPATH=src uv run python scripts/multi_n/noncoprime_full_scan_fast.py --max-hyp 1000000 --workers 6` | 4,951,985 | 3,001,807 | 1,617,805 | 332,373 | 0 |

The default scanner writes to `results/multi_n/full_scan_max*.json`; those incidental outputs were restored after wrapping this run's outputs under `results/counterexample_first/2026-06-07/`.

## Near-Miss Collection

Command:

```bash
PYTHONPATH=src uv run python - <<'PY'
# controller near-miss collector
# uses scripts/multi_n/_concordant_gen.emit_pairs(..., coprime_only=False)
# writes results/counterexample_first/2026-06-07/near_misses_max100000.json
PY
```

Bound:

```text
max_hyp = 100000
```

For each pair with at least two exact concordant `N`, the collector computed:

```text
delta = min(
  |N_i + N_j - (A+B)|,
  |N_i + N_j - |A-B||,
  ||N_i - N_j| - (A+B)|,
  ||N_i - N_j| - |A-B||
)
```

Results:

| Stage | Count | Min delta |
|---|---:|---:|
| `stage1_Dg_killed` | 200,707 | 1 |
| `stage2_full_plane_mod_killed` | 104,999 | 1 |
| `stage3_exact_gen_survivor` | 19,219 | 1 |

The important near-miss list is the `stage3_exact_gen_survivor` list, because these pairs survived both sound prefilters and were decided only by exact GEN-CLOSURE.

## Subagent Slices

| Slice | Status | Output |
|---|---|---|
| `gcd-strata-search` | completed | `subagent-notes/gcd-strata-search.md`, `results/counterexample_first/2026-06-07/gcd-strata-search.json` |
| `constructive-families` | completed | `subagent-notes/constructive-families.md`, `results/counterexample_first/2026-06-07/constructive-families.json` |
| `filter-breakers` | completed by subagent and controller | `subagent-notes/filter-breakers.md`, `filter-breakers.md`, `results/counterexample_first/2026-06-07/filter-breakers.json`, `results/counterexample_first/2026-06-07/filter_breakers_controller.json` |
| `partner-graph-full-plane-recheck` | completed | `subagent-notes/partner-graph-full-plane-recheck.md`, `results/counterexample_first/2026-06-07/partner-graph-full-plane-recheck.json` |

## Filter-Breaker Probe

Command:

```bash
PYTHONPATH=src uv run python - <<'PY'
# selected exact diagnostic samples
# writes results/counterexample_first/2026-06-07/filter_breakers_controller.json
PY
```

This was a selected-sample probe, not an exhaustive scan. It collected examples where unsafe shortcuts diverge from exact or full-plane logic.

## Constructive-Families Probe

Subagent output:

```text
docs/explorations/2026-06-07-counterexample-first/subagent-notes/constructive-families.md
results/counterexample_first/2026-06-07/constructive-families.json
```

The reverse search found no true hit, but did find gap-1 families where all four square checks are exact and only the final linear closure misses.

Example:

```text
(A,B,N1,N2) = (60,84,63,80)
63^2 + 60^2 = 87^2
63^2 + 84^2 = 105^2
80^2 + 60^2 = 100^2
80^2 + 84^2 = 116^2
N1 + N2 = 143
A + B = 144
```

## Partner Graph Recheck

Subagent output:

```text
docs/explorations/2026-06-07-counterexample-first/subagent-notes/partner-graph-full-plane-recheck.md
results/counterexample_first/2026-06-07/partner-graph-full-plane-recheck.json
```

Main result: old `G_M` and island no-hit/delta artifacts are sum-only/inside-square evidence, not full-plane GEN-CLOSURE evidence. A bounded full-plane recheck of 2,293 representative partner vertices found 0 hits and minimum full-plane delta 1.
