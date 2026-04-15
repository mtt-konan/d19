# 027-concordant-safe-pair-sieve

## Summary

Replaced the failed pair-level `mod1680` runtime experiment with a real
experimental safe pre-sieve for `concordant --max-hyp`.

The new switch is:

- `uv run python scripts/search.py concordant --safe-pair-sieve ...`

It is based on a stronger 2-adic necessary condition for the **full 4-chain**
on the current reduced `(A,B)` batch pairs:

- `A` odd
- `B` odd
- `(A + B) % 4 == 0`

This sieve is:

- mathematically safe for the current reduced batch input
- extremely cheap to compute
- strong enough to remove most pairs before `ellratpoints`

## Why `026` Was Removed From Runtime

Worklog `026` showed that the previous pair-level local-solvability `mod1680`
idea was a vacuous sieve.

Reason:

- it asked whether some `N (mod m)` exists so that `N^2 + A^2` and `N^2 + B^2`
  both look square modulo `m`
- but `N ≡ 0 (mod m)` always works
- so every `(A,B)` passes

That experiment is still kept as a negative result:

- `docs/work-logs/026-concordant-local-sieve-mod1680.md`

But it is no longer kept as a runtime feature.

## What Was Added

- New module:
  - `src/rational_distance/concordant/safe_pair_sieve.py`
- New CLI flag on `concordant`:
  - `--safe-pair-sieve`
- Updated concordant profile fields:
  - `safe_pair_sieve_enabled`
  - `n_pairs_after_safe_pair_sieve`
  - `n_pairs_rejected_by_safe_pair_sieve`
  - `n_pairs_rejected_mixed_parity`
  - `n_pairs_rejected_mod4`
  - `time_safe_pair_sieve_s`
- Batch JSON now makes the distinction explicit:
  - `n_pairs` = raw generated pair count
  - `n_pairs_analyzed` = pairs actually sent into PARI
  - `safe_pair_sieve_enabled` = whether the experimental sieve was used

`--pair` intentionally does not support `--safe-pair-sieve`.

## Important Semantic Difference

This new sieve is **not** trying to preserve the old “full concordant view”.

Instead:

- default `concordant --max-hyp` still shows the full concordant landscape
- `--safe-pair-sieve` switches to a full-chain-directed batch mode

So it is expected that:

- `n_with_concordant` can drop when the sieve is enabled
- because many half-solutions are being filtered out on purpose

What should stay unchanged is the chain-solution story:

- if a real full-chain candidate survived before, it should still survive now

In the measured runs below, chain-compatible hits stayed at `0` in both modes.

## Benchmarks

Commands run:

```bash
uv run python scripts/search.py concordant --max-hyp 1000 --ec-bound 100000 --no-progress --profile
uv run python scripts/search.py concordant --max-hyp 1000 --ec-bound 100000 --no-progress --profile --safe-pair-sieve

uv run python scripts/search.py concordant --max-hyp 2000 --ec-bound 100000 --no-progress --profile
uv run python scripts/search.py concordant --max-hyp 2000 --ec-bound 100000 --no-progress --profile --safe-pair-sieve
```

Results:

| `max_hyp` | mode | raw pairs | analyzed pairs | rejected | mixed parity | mod-4 reject | `time_safe_pair_sieve_s` | `time_find_concordant_s` | wall time | `n_with_concordant` | `n_with_chain_compatible` |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1000 | baseline | 24197 | 24197 | 0 | 0 | 0 | 0.000s | 23.777s | 23.9s | 686 | 0 |
| 1000 | `--safe-pair-sieve` | 24197 | 2120 | 22077 | 20032 | 2045 | 0.002s | 1.995s | 2.0s | 115 | 0 |
| 2000 | baseline | 99311 | 99311 | 0 | 0 | 0 | 0.000s | 96.432s | 96.9s | 891 | 0 |
| 2000 | `--safe-pair-sieve` | 99311 | 8220 | 91091 | 82996 | 8095 | 0.010s | 7.671s | 7.8s | 152 | 0 |

## Interpretation

The result is much stronger than the failed `026` experiment:

- the new sieve removes about `91%` of batch pairs
- the sieve itself costs almost nothing
- `ellratpoints` time drops by about the same order of magnitude
- wall time also drops sharply because PARI was the dominant cost

In plain terms:

- this filter is finally attacking the expensive part of `concordant`
- not by making PARI faster
- but by sending PARI far fewer pairs

## Takeaway

For the `concordant` line, the first useful pre-sieve is not pair-level
`mod1680`; it is the stronger 2-adic full-chain necessary condition on reduced
batch pairs.

Current position after this work:

- keep default `concordant` for full concordant observation
- keep `--safe-pair-sieve` as an experimental full-chain-directed fast path
- continue using the surviving sifted pairs as input for the next round of
  deeper mathematical analysis
