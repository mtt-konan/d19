# 026-concordant-local-sieve-mod1680

## Summary

Implemented an experimental `--local-sieve` for `concordant --max-hyp`, using
moduli `16, 3, 5, 7` with combined modulus `1680`.

The intended idea was:

- reject `(A,B)` pairs before `ellratpoints`
- only keep pairs that are locally solvable modulo `1680`
- reduce the dominant `time_find_concordant_s` cost

The implementation is correct, but the experiment produced an important
negative result:

- this v1 local-solvability condition is vacuous
- it rejects **zero** pairs
- therefore it does not reduce PARI work

## What Was Added

- New module: `src/rational_distance/concordant/local_sieve.py`
- New CLI flag:
  - `uv run python scripts/search.py concordant --local-sieve ...`
- New profile fields:
  - `local_sieve_enabled`
  - `local_sieve_moduli`
  - `local_sieve_combined_modulus`
  - `n_pairs_after_local_sieve`
  - `n_pairs_rejected_by_local_sieve`
  - `time_local_sieve_s`
- Batch JSON now distinguishes:
  - `n_pairs` = raw generated pair count
  - `n_pairs_analyzed` = pairs actually sent into analysis

`--pair` intentionally does not support `--local-sieve`.

## Why It Rejects Nothing

The v1 condition checks whether there exists some residue class `N (mod m)` such
that:

- `N^2 + A^2` is a square residue mod `m`
- `N^2 + B^2` is a square residue mod `m`

But `N ≡ 0 (mod m)` always works:

- `N^2 + A^2 ≡ A^2`
- `N^2 + B^2 ≡ B^2`

and both `A^2` and `B^2` are automatically square residues.

So for this exact pair-level condition:

- every `(A,B)` is locally solvable
- the `1680 x 1680` lookup table is all `True`
- the sieve is mathematically safe, but useless

This is different from `chain-fast`'s `mod1680`:

- `chain-fast` filters specific expressions like `A^2 + N^2`
- `concordant` v1 tried to filter whole `(A,B)` pairs
- the latter collapses because `N ≡ 0` is always an allowed witness

## Benchmarks

Commands run:

```bash
uv run python scripts/search.py concordant --max-hyp 1000 --ec-bound 100000 --no-progress --profile
uv run python scripts/search.py concordant --max-hyp 1000 --ec-bound 100000 --no-progress --profile --local-sieve

uv run python scripts/search.py concordant --max-hyp 2000 --ec-bound 100000 --no-progress --profile
uv run python scripts/search.py concordant --max-hyp 2000 --ec-bound 100000 --no-progress --profile --local-sieve
```

Results:

| max_hyp | mode | wall time | after_local_sieve | rejected | time_local_sieve_s | time_find_concordant_s |
|---|---|---:|---:|---:|---:|---:|
| 1000 | baseline | 23.1s | 24197 | 0 | 0.000s | 22.937s |
| 1000 | `--local-sieve` | 23.9s | 24197 | 0 | 0.003s | 23.750s |
| 2000 | baseline | 97.2s | 99311 | 0 | 0.000s | 96.756s |
| 2000 | `--local-sieve` | 94.4s | 99311 | 0 | 0.014s | 93.847s |

Interpretation:

- no pairs were removed
- result sets were unchanged
- timing differences are just run-to-run noise
- this experiment does **not** provide a useful speedup path

## Takeaway

This rules out one tempting but too-weak idea:

- pair-level “there exists some `N mod 1680`” local solvability is not enough

If `concordant` wants a useful safe pre-sieve, it needs a stronger necessary
condition than this one, or it needs to move back to a different structure
entirely, such as:

- deeper arithmetic constraints on `(A,B)`
- a nontrivial local condition that does not admit `N ≡ 0` as a universal witness
- parallelism, since `ellratpoints` remains the real bottleneck
