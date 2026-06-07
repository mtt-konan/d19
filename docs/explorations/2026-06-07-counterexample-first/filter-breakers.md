# Filter-Breaker Samples

These are not Harborth counterexamples. They are samples that break tempting but unsafe shortcuts.

Machine-readable data:

```text
results/counterexample_first/2026-06-07/filter_breakers_controller.json
```

## Samples

| Sample | What it breaks | Exact status |
|---|---|---|
| `(75,495)` | Coprime-only `safe_sieve` would reject as `odd_odd_wrong_mod4`, but `gcd(A,B)=15`, `D_g=4`, `gcd_aware_kills=False`, and full-plane modular sieve does not kill it. | `N=[100,308]`, no GEN-CLOSURE, closest delta `12`. |
| `(51,975)` | Another non-coprime pair where coprime-only safe classification is not a valid proof reason. | `N=[140,1300]`, no GEN-CLOSURE; full-plane mod sieve kills at `25`. |
| `(11339,37765)` | Old sum-only modular closure kills at `361`, but full-plane modular closure does not kill. | `N=[3480,222300]`, no GEN-CLOSURE. |
| `(10207,78793)` | Old sum-only closure and full-plane closure disagree. | `N=[13224,882876]`, no GEN-CLOSURE; also killed by gcd-aware logic. |
| `(264,420)` | Default bounded `concordant` CLI undercounts `N`; exact factor/divisor path finds more. | exact `N=[77,315,352,1440]`, no GEN-CLOSURE, closest delta `17`. |
| `(15960,61776)` | Near-counterexample in the weak `D_g=1` layer. | exact `N=[4950,10368,20007,49280,95095]`, delta `1`. |
| `(3960,6300)` | High-k stage-3 survivor at small bound. | exact `N=[1470,5280,6615,7616,16170]`, delta `4`. |

## Plain-Language Takeaway

These examples are warning signs for future proof attempts:

- Do not run the coprime-only safe rule on arbitrary non-coprime pairs.
- Do not use sum-only closure as a full-plane obstruction.
- Do not use bounded CLI output as an exhaustive `N` list.
- Do not assume high `k` automatically pushes a pair into closure.
