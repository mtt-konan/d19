# Multi-Concordant N Strategy

This document records the role of multi-`N` after the closure quotient pivot.

## Core Idea

For fixed `(A,B)`, a concordant value `N` satisfies:

```text
N^2 + A^2 is square
N^2 + B^2 is square
```

A possible Harborth configuration needs at least two such values and must pass
GEN-CLOSURE:

```text
{N1+N2, |N1-N2|} intersects {A+B, |A-B|}
```

## Current Status

Multi-`N` scanning is no longer the main proof route. It is useful for:

- producing examples;
- testing closure predicates;
- feeding residual datasets;
- checking whether new certificates agree with finite search.

The main proof attempt now works at the quotient/family level:

```text
N plus closure leg M
  -> AA/BB closure quotient
  -> rank-zero certificate
  -> lambda=A/B family theorem attempt
```

## Important Correction

Old multi-`N` notes often centered `N1+N2=A+B`. That is only the inside-square
case. Use GEN-CLOSURE for current full-plane statements.

## Relationship To Closure Quotients

Multi-`N` enumerates possible `N` values first.

Closure quotient puts `N` and the closure leg `M` into the same curve first.
That is why `AA/BB rank=0 + torsion pullback` can exclude some candidates
without treating the whole problem as more pair counting.

## Reading

- [CLOSURE_QUOTIENT_MAINLINE.md](../CLOSURE_QUOTIENT_MAINLINE.md)
- [EXPLORATION_MAP.md](./EXPLORATION_MAP.md)
- [work-logs/README.md](../work-logs/README.md)
