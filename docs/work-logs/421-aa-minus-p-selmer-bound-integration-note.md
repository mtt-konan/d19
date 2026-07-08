# AA Minus-P Selmer-Bound Integration Note

## Question

How should the new full-image result at primes

```text
ell | T^2 + 4*L^2
```

be counted in the `rank-zero-selmer-AA-kernel-minus-p` Selmer bound argument?

## Result

It must be counted as no local restriction.

The odd-prime local image input for this package is now:

```text
ell | L                 local image for x: {1}
ell | T                 local image for x: {1, -1}
ell | T^2 + 4*L^2       local image for x: full Q_ell*/Q_ell*2
```

普通话说：`T^2 + 4L^2` 的奇素数不会帮这个 kernel 降维。它们不是“只允许 trivial”，而是
四种局部平方类都允许。

## Consequence

The old route cannot prove a uniform `global_selmer_dimension_bound` for this
package by promoting the reduction-level zero-double-root `{trivial}`
candidate. Any global Selmer candidate can still carry independent odd
valuation at primes dividing `T^2 + 4*L^2`, unless another argument removes
those generators.

So the next real proof step is not another local lift in this package. It is
one of:

- combine this kernel with another independent kernel or family-level
  argument;
- prove a separate global relation killing the `T^2 + 4*L^2` generators;
- route these lambda classes through root-number or 2-cover exclusions.

## Boundary

This does not prove a Selmer rank upper bound, rank zero, or family exclusion.
It corrects the input to the still-open global Selmer dimension bound.
