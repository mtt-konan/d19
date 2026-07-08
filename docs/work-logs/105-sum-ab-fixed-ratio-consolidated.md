# wl105-wl161 - fixed-ratio and sum=A+B branch consolidated

## Summary

This replaces the old wl105-wl161 worklogs.

普通话说：这一段是在 closure-first / fixed-ratio / `sum=A+B` 语言里找一个
可证的代数切片。它产出了一批模型、缓存和诊断，但主结论是负面的：这些
squareclass、Möbius、Euclid、shared-leg 和 residue 层没有闭合成证明。

## What This Block Established

- Closure-first near-miss data were organized by D4 symmetry and coordinate
  branches.
- Fixed integer ratio `A=kB` was upgraded to rational ratio `lambda=A/B`.
- The same reciprocal orbit cannot by itself give closure.
- Cross-orbit closure becomes a fixed-line / elliptic-curve level problem.
- `sum=A+B` was translated through slope, product, Möbius, Euclid, and
  squareclass coordinates.
- The weak product model was shown to have false positives and cannot replace
  the four individual square conditions.
- Coprime/stale-result guards were added so old sum-only outputs would not be
  mistaken for current proof status.
- Mixed-orientation mod 8/24 notes closed only small sub-branches.
- Same-orientation/shared-leg/factor-pair routes kept producing structured
  near-misses rather than a contradiction.
- Descending-family graphs and squareclass families were useful diagnostics,
  not a descent proof.

## What Was Dropped

Dropped from the human worklog set:

- one-log-per-helper additions;
- fixed-sample equation printouts;
- residue table churn;
- repeated "new field/new helper" notes;
- near-miss taxonomies that did not feed the current lambda/Selmer mainline.

## Boundary

No fixed-ratio theorem was proved here. The useful material was later absorbed
into the `R_lambda` language and then superseded by the closure quotient /
rank-zero Selmer mainline.
