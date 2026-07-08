# wl053-wl072 - partner graph and fast-core infrastructure consolidated

## Summary

This replaces the old wl053-wl072 worklogs.

普通话说：这一段把 multi-`N` 数据组织成 partner graph / `G_M`，同时把
`proof_status` 跑法工程化。它的价值主要是结构地图和速度；它没有把高 `k`、
大连通分量或 partner cycle 转成全局障碍。

## What This Block Established

- Old top-level modules were archived or stubbed.
- Partner pairs and `K_n` hubs were identified as the graph form of
  multi-concordant-`N` structure.
- `K_n` shared-partner structure was connected to the count of concordant
  `N` values.
- Direct non-coprime scans showed that reducing to coprime `(A,B)` is not
  automatically WLOG for the full problem.
- Partner BFS found a giant component plus small isolated components in the
  finite window.
- Cycle/rank-deficit experiments showed that cycles mostly express
  Mordell-Weil linear dependence, not a new obstruction.
- Large `G_M` closure scans found no counterexample in range, but the early
  predicate was still sum-only.
- Shared parallel infrastructure, AB-sieve ordering, fast-core mode, and
  PARI single-thread safeguards were added.
- Generator-first candidate generation was benchmarked but did not replace the
  main route.

## Main Numbers To Keep

```text
full G_M finite scan vertices = 338225
full G_M finite scan closure hits = 0
giant component size in the 1M scan = 309689 vertices
observed finite graph was about 99.6% tree-like
PARI internal multithreading was disabled for reliable survivor audits
```

## Boundary

The graph work gave excellent diagnostics, but did not prove that all infinite
components behave like the finite window.

The later GEN-CLOSURE correction also matters: early "closure = 0" graph logs
mainly checked the inside-square sum relation, not all four full-plane
relations.
