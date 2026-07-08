# Partner Graph Theory

This document is now a compact historical summary. Partner graph work is not
the current proof mainline.

## Dictionary

```text
concordant N for (A,B):
  N^2 + A^2 and N^2 + B^2 are squares

multi-N pair:
  (A,B) has at least two concordant N values

partner pair:
  if N_i,N_j are concordant for (A,B), then (N_i,N_j) is a partner pair

partner graph G_M:
  vertices are multi-N pairs; edges connect a pair to its partner pairs
```

## Main Identity

The partner identity is elementary:

```text
N_i,N_j concordant for (A,B)
  => A,B concordant for (N_i,N_j)
```

So partner graph structure is a symmetric repackaging of the same four
Pythagorean square conditions.

## What The Route Taught

- Multi-N pairs are real and common enough to matter.
- `K_n` hubs are just high-multiplicity multi-N pairs in graph language.
- Cycles mostly reflect Mordell-Weil linear dependence and 2-divisibility.
- High `k` did not produce a closure obstruction.
- Partner graph scans gave strong finite evidence but no theorem.

## Boundary

Do not use partner graph results as a proof of Harborth. They are historical
diagnostics and sample generators.

Current proof work has moved to closure quotient / `lambda` / rank-zero Selmer.
