# 025 - chain-fast safe pair sieve experiment

## Summary

Added an experimental `--safe-pair-sieve` switch for `chain-fast`.

- New module: `chain_fast/safe_pair_sieve.py`
- Scope: python backend only
- Hard conditions only:
  - `(OE, OE)` reject
  - `(EO, EO)` reject
  - for `T1=OE, T2=EO`, require `v2(t1) = v2(s2)`
  - for the same case, after building `N`, require `N % 4 == 0`
- Added profile fields:
  - `safe_pair_sieve_enabled`
  - `n_pairs_after_safe_pair_sieve`
  - `time_safe_pair_sieve_s`

## Result

The filter is mathematically safe and preserves the output set, but it is not a
speed win in the current Python implementation.

Measured runs:

- `max_hyp=5000, workers=1`: pairs drop from `2.51M` to `0.73M`, wall time goes from `0.9s` to `1.7s`
- `max_hyp=50000, workers=1`: pairs drop from `253.4M` to `73.9M`, wall time goes from `88.9s` to `170.0s`
- `max_hyp=100000, workers=8`: pairs drop from `1.01B` to `295.7M`, wall time goes from `81.7s` to `149.2s`

Most importantly, `after_basic_filters` stays exactly the same as baseline in
all three runs. That means the new sieve mostly re-detects pairs that the
existing basic filter was already rejecting cheaply.

## Conclusion

Keep `--safe-pair-sieve` as an experimental switch only.

This round confirms two things:

- the orientation / `v2` math is sound enough to use as hard pruning
- in the current insertion point, the extra Python work costs more than it saves

If this line is revisited later, the next step should be to make the same
information cheaper to evaluate, or to find conditions that reduce
`after_basic_filters`, not just `pairs total`.
