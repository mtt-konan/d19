# 023 - chain-fast mod sieve experiment

## Summary

Added an experimental `--mod-sieve` flag to `chain-fast`.

- New module: `chain_fast/mod_sieve.py`
- Fixed moduli: `16, 3, 5, 7`
- Scope: only pre-filter `C3` candidates
- Added profile fields for `after_c3_mod` and `time_mod_sieve_c3_s`

## Result

The sieve is mathematically correct and preserves the result set, but it is not
yet a speed win.

Measured with the Python backend:

- `max_hyp=5000`: candidate count drops sharply, wall time roughly unchanged
- `max_hyp=50000`: `C3` checks drop from `62.5M` to `21.7M`, but wall time gets slower
- `max_hyp=100000, workers=8`: `C3` checks drop from `250.0M` to `86.8M`, but wall time still gets slower

## Conclusion

Keep `--mod-sieve` as an experimental switch only.

The experiment shows that:

- reducing exact `isqrt(C3)` calls is not enough by itself
- the extra modulo / lookup work in Python is also expensive
- future work should focus on either cheaper sieve mechanics or earlier
  structural pruning before the main pair loop
