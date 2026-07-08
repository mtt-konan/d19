# AA Square-Root Kernels Kill d-Prime Local Classes

## Question

After `AA / kernel_minus_p` gave full image at odd primes dividing

```text
d = T^2 + 4*L^2,
```

do the other two `AA` kernels provide local restrictions at those same primes?

## Result

Yes. For both square-root kernels, the `d`-prime local image for the tracked
descent coordinate `x` is trivial:

```text
rank-zero-selmer-AA-kernel-pos-2sqrt-q: x-class {1}
rank-zero-selmer-AA-kernel-neg-2sqrt-q: x-class {1}
```

普通话说：`minus_p` 这个 kernel 在 `d` 的奇素数处管不住，但另外两个 square-root
kernel 在同一类素数处能管住。它们是接住这些潜在自由生成元的最小结构候选。

## Proof Shape

For `kernel_pos_2sqrt_q`, write

```text
d  = T^2 + 4*L^2
a2 = -8*(T^2 + 8*L^2)
a4 = 16*T^4
r  = -4*T^2
```

and use

```text
x^2 + a2*x + a4 = (x - r)^2 - 16*d*x.
```

At `ell | d`, the residue of `r` is `16*L^2`, a square unit.

For `kernel_neg_2sqrt_q`, write

```text
d  = T^2 + 4*L^2
a2 = 16*(T^2 + 2*L^2)
a4 = 256*L^4
r  = 16*L^2
```

and use

```text
x^2 + a2*x + a4 = (x - r)^2 + 16*d*x.
```

In both cases, if `x-r` is a unit then the quadratic factor is a square by
odd-prime square lifting. If `x-r` is not a unit, then `x` is congruent to
the square unit `r`. Hence every non-kernel local point has trivial `x`
squareclass.

## Boundary

This proves only these two package-specific odd-prime formal-lift subclaims.
It does not prove the dyadic condition, the global Selmer bound, rank zero,
or any lambda-family exclusion.
