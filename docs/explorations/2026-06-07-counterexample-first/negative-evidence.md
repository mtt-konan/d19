# Negative Evidence

## What Was Ruled Out

Within the scanned bounds, no full-plane GEN-CLOSURE hit exists among exact multi-N pairs:

| Bound | Ruled out |
|---:|---|
| 10,000 | every full-space multi-N pair with `A<B<=10000` |
| 100,000 | every full-space multi-N pair with `A<B<=100000` |
| 1,000,000 | every full-space multi-N pair with `A<B<=1000000` |

The statement above is finite and scoped. It is not a proof of Harborth's conjecture.

## Why This Is Stronger Than Old No-Hit Statements

This pass avoided the two biggest pitfalls from the theory audit:

- It included non-coprime `(A,B)` pairs. Reduced/coprime is not treated as WLOG.
- It used full-plane GEN-CLOSURE. The old sum-only relation was not used for full-plane claims.

The exact hit pipeline was:

```text
multi-N pair generation
gcd_aware_kills
find_killer_modulus(..., full_plane=True)
exact concordant N list
exact GEN-CLOSURE check
```

## What Was Not Ruled Out

This pass does not rule out:

- a counterexample with `A` or `B` above `1,000,000`;
- a proof-relevant infinite family that starts beyond the scanned bounds;
- a bug in the Cython generator or exact divisor enumeration;
- a full Harborth proof requiring rational-point geometry outside this integer scan framing;
- closure patterns that require a constructive generator rather than blind bounded enumeration.

## Residual Hard Core

At `max_hyp=1,000,000`, the pipeline still had `332,373` exact stage-3 survivors. They were not closures, but they also were not killed by the current sound prefilters.

The dominant survivor gcd values were:

```text
12, 60, 24, 120, 36, 48, 180, 240, 72, 84
```

Plain-language interpretation: the current filters are very good at clearing easy cases, but a large hard core remains. That hard core is mostly where `gcd(A,B)` is divisible by `12`.

## Partner Graph Caveat

The partner graph recheck found that old `G_M` and island artifacts are useful but narrower than the current target:

- old `full_gm_closure_scan.py` checked `N_i + N_j = A+B`;
- old full-`G_M` delta data measured only `(A+B)-(N_i+N_j)`;
- old island `closure_hits_total=0` is also sum-only.

A bounded full-plane recheck over 2,293 representative partner vertices found no hit and minimum full-plane delta `1`, but it did not exhaust all 338,225 old `G_M @ max_value=1M` vertices.
