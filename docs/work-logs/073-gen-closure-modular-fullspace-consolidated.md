# wl073-wl104 - GEN-CLOSURE, modular filters, and full-space scans consolidated

## Summary

This replaces the old wl073-wl104 worklogs, including the duplicate wl094 pair.

普通话说：这一段做了两件大事。第一，试图从 k=2 / mod-`p^2`
方向证明，最后撞墙。第二，纠正了闭合关系：`N1+N2=A+B` 只是正方形内部，
全平面要用 GEN-CLOSURE 四关系。这个纠正是主线资产。

## What This Block Established

- Dual closure and `N`-side modular filters were implemented and tested.
- Path A tried to prove a `k=2 => rank >= 2` style theorem.
- The attempted A1/A2 Gaussian proof was later found invalid for composite
  cases; keep wl084's correction, not wl083's overclaim.
- Path B tried to promote mod-`p^2` patterns into a uniform obstruction.
- CRT and survivor audits showed that pure local mod-`p^2` filtering leaves a
  persistent positive residue set; the route was closed as a proof strategy.
- D-scaling and K-hub tools reproduced and extended high-`k` examples.
- Cycle linear relations and K-hub identities were explained as
  Mordell-Weil/2-divisibility structure, not as a killing obstruction.
- Peschmann-style sieves and Heegner-height deciders were judged redundant or
  insufficient for the remaining global proof gap.
- GEN-CLOSURE was derived:

```text
{N1 + N2, |N1 - N2|} intersects {A + B, |A - B|}
```

- Production closure checks were upgraded from sum-only to the four full-plane
  relations.
- The coprime-leg mod-12 theorem was proved:

```text
gcd(A,B)=1 and N^2+A^2, N^2+B^2 squares  =>  12 | N
```

- The gcd-aware/non-coprime scans showed why coprime reduction misses a real
  half-space.

## Main Numbers To Keep

```text
sum-only multi-N scan to max_hyp=7M found 0 closure hits
GEN-CLOSURE full-plane check to max_hyp=2000 found 0 hits
coprime mod-12 validation covered >1.16M concordant N values
non-coprime full-space scan reached max_hyp=1M
```

## What Survived As Mainline

- GEN-CLOSURE is the right closure language.
- The inside-square/sum-only logs are historical and must not be read as a
  full-plane proof.
- Coprime `12 | N` is a real theorem and explains much of the modular filter.
- Non-coprime/gcd scaling is a genuine gap, not bookkeeping.

## Boundary

This block still does not prove Harborth. It fixes the closure target and
closes several tempting false routes.
