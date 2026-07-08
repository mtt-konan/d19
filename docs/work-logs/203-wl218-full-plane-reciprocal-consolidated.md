# wl203-wl293 - wl218 full-plane reciprocal route consolidated

## Summary

This replaces the old wl203-wl293 worklogs.

普通话说：这一段是一次很长的证明尝试：想把 `R_lambda` 的全平面闭合问题
压成 reciprocal / product / valuation / q-adic / 2-adic 矛盾。最终没有证明成功。
它留下的是精确命题、失败边界和后续入口，不是 theorem。

## What This Block Established

- Yang Ji fixed-`n` prime-pair coverage was tabulated for fixed-ratio context.
- D4-invariant and closure-first near-miss templates were equationized.
- Shared-variable/shared-role buckets helped choose examples, but did not give
  a proof route.
- wl218 defined the full-plane `R_lambda` closure classifier.
- The full-plane target has four branches:

```text
r + s   = lambda + 1
r + s   = |lambda - 1|
|r - s| = lambda + 1
|r - s| = |lambda - 1|
```

- The intended theorem remained:

```text
r,s in R_lambda and one full-plane closure branch holds  =>  rs=lambda
```

- The first branch `r+s=lambda+1` was reduced through many shadow models:
  squareclass ratio, `z=u-1/u`, Gaussian ratios, slope quadratics, dual slopes,
  bridge cycles, and q-adic norm ledgers.
- Several apparent shortcuts were ruled out:
  single-prime residue obstruction, naive 3-adic lift, exact local branch
  killing, p+lambda shadow, and standalone 2-adic cleanup.
- The final q-adic/2-adic residuals looked locally soluble in the sampled
  models, so this route did not close.

## Closeout State

The route closed with this honest status:

```text
full-plane reciprocal theorem = open
sum=A+B branch = open
q-adic bridge residual = open
centerline-style trivial tubes = separated but not enough
local residue data = boundary evidence, not contradiction
```

## What Was Dropped

Dropped from the human worklog set:

- dozens of helper-ledger logs;
- repeated q-adic sample tables;
- incremental factorization notes;
- boundary probes that only renamed the same residual channel.

Kept here:

- the exact four-branch statement;
- the product-layer identity;
- the fact that the attempted reciprocal proof did not close;
- the warning that `sum=A+B` is only one branch.

## Boundary

This consolidation is a closeout of a failed proof attempt. It should not be
used as evidence that the theorem is false; it says only that this route did not
find the missing global obstruction.
