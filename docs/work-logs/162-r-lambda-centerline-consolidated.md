# wl162-wl202 - R_lambda and centerline branch consolidated

## Summary

This replaces the old wl162-wl202 worklogs.

普通话说：这一段把 fixed-ratio 工作正式搬到 `R_lambda`，并把 centerline
情形接到 Yang Ji 的已知定理。主线进账是：中心线不用再反复研究；它是已关闭
的特殊分支。非中心 residual 分支仍开放。

## What This Block Established

- `R_lambda` became the ratio-level object:

```text
R_lambda = { r > 0 rational : r^2+1 and r^2+lambda^2 are squares }
```

- Product-square conditions were separated from true membership in `R_lambda`.
- Centerline, reciprocal, and residual buckets were made explicit.
- Product-square / squareclass-pair ledgers explained several false-positive
  patterns.
- Root-grid and small-height rational pools found residual examples for
  diagnostics, not proofs.
- True closure branches were distinguished from shadow/product conditions.
- The centerline branch was translated across geometries:

```text
N1=N2
a+b=2n
|a-b|=2n
r=s=(lambda+1)/2
```

- The centerline branch was closed by reference to Yang Ji, Theorem 2 plus the
  full-plane remark.

## Main Status

```text
centerline branch = closed by known theorem and local translation
reciprocal/product-square ledgers = useful diagnostics
residual non-center branch = open
full R_lambda theorem = not proved
```

## Boundary

This block did not reprove Yang Ji's Fermat descent inside the repository. It
only records the citation and the coordinate translation needed for d19.

It also did not close fixed ratio `lambda != 1` or the full-plane closure
problem.
