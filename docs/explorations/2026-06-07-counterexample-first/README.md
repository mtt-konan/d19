# d19 Counterexample-First Exploration

Date: 2026-06-07

Scope: counterexample-first exploration for the d19 / Harborth direction. This run tried to find exact full-plane GEN-CLOSURE hits first, then ranked near-misses and proof leads. It did not try to turn finite no-hit scans into a proof.

## Executive Summary

本轮没有找到 GEN-CLOSURE 闭合命中，也没有找到完整 Harborth 反例。

最强的负结果是 full-space 精确扫描：

| Bound | Domain | Multi-N pairs | Exact GEN-CLOSURE survivors checked | Closures |
|---:|---|---:|---:|---:|
| 10,000 | coprime + non-coprime | 17,748 | 866 | 0 |
| 100,000 | coprime + non-coprime | 324,925 | 19,219 | 0 |
| 1,000,000 | coprime + non-coprime | 4,951,985 | 332,373 | 0 |

普通话说：我们没有只盯互素 pair，也没有用旧的 `N1+N2=A+B`。这次扫描覆盖了非互素空间，并且最后一步使用 full-plane GEN-CLOSURE：

```text
{N1 + N2, |N1 - N2|} intersects {A + B, |A - B|}
```

最重要的 near-miss 是：

```text
(A,B) = (15960, 61776), gcd=24, D_g=1
N = [4950, 10368, 20007, 49280, 95095]
|95095 - 49280| = 45815
|A - B| = 45816
delta = 1
```

这不是反例，因为差了 1。但它很有价值：它落在 `D_g=1` 的弱层，既没有被 gcd-aware divisibility 筛杀，也没有被 full-plane modular sieve 杀掉。

## Produced Artifacts

Documents:

- `search-log.md`: commands, bounds, metadata, and reproducibility notes.
- `candidates.md`: exact hit / candidate status.
- `near-misses.md`: ranked near-miss table and high-k observations.
- `filter-breakers.md`: samples that break unsafe shortcuts.
- `negative-evidence.md`: what the scans rule out and do not rule out.
- `proof-leads.md`: candidate proof or construction routes.
- `subagent-notes/gcd-strata-search.md`: gcd-strata slice report.
- `subagent-notes/constructive-families.md`: reverse/constructive closure-first search.
- `subagent-notes/filter-breakers.md`: broader filter-breaker slice report.
- `subagent-notes/partner-graph-full-plane-recheck.md`: partner graph full-plane recheck.

Machine-readable data:

- `results/counterexample_first/2026-06-07/full_scan_max10000.json`
- `results/counterexample_first/2026-06-07/full_scan_max100000.json`
- `results/counterexample_first/2026-06-07/full_scan_max1000000.json`
- `results/counterexample_first/2026-06-07/near_misses_max100000.json`
- `results/counterexample_first/2026-06-07/gcd-strata-search.json`
- `results/counterexample_first/2026-06-07/filter_breakers_controller.json`
- `results/counterexample_first/2026-06-07/constructive-families.json`
- `results/counterexample_first/2026-06-07/filter-breakers.json`
- `results/counterexample_first/2026-06-07/partner-graph-full-plane-recheck.json`

Each result file records date, command, commit, bound, scope, closure predicate, and whether concordant `N` enumeration was exact or bounded.

## Current Best Leads

1. Prove or explain the `D_g=1` layer. In this data, `D_g=1` is the dominant hard zone, and it corresponds to `12 | gcd(A,B)`.
2. Attack the delta-1 example `(15960,61776)` as a local model. It misses the full-plane difference relation by exactly one.
3. Study the constructive gap-1 family `(A,B,N1,N2)=(60,84,63,80)`: all four square checks hold, but `N1+N2=A+B-1`.
4. Study why high `k` does not help enough. The highest `k` examples at `max_hyp=100000` still fail closure, often after modular obstruction.
5. Re-run partner graph scans with full-plane delta, because old `G_M` / island data is sum-only.

## Completion Status

Phase 1-3 are materially complete for this first pass:

- baseline tests passed;
- exact hit search reached `max_hyp=1,000,000`;
- near-miss data exists at `max_hyp=100,000`;
- boundary/filter-breaker samples exist;
- constructive closure-first search exists and produced gap-1 families;
- partner graph old-result semantics were rechecked and downgraded where needed;
- reduced/coprime and full-space scope are separated;
- no full-plane conclusion uses old sum-only closure.

Remaining optional slices may still add more side evidence, but the controller findings already satisfy the core counterexample-first pass.

## Follow-Up

The first recommended next step has now been run in:

```text
docs/explorations/2026-06-07-next-step-hard-layer/
```

It confirms `D_g=1` is exactly the `12 | gcd(A,B)` hard layer in the positive search domain, dissects the gap-1 models, and upgrades the old partner graph `G_M @ max_value=1M` evidence from sum-only to full-plane GEN-CLOSURE:

```text
338,225 vertices
5,071,562 full-plane relation rows
0 full-plane hits
global min delta = 1
```
