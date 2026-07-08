# AA Neg Kernel Odd-Prime Formal Lifts

## Question

Can the remaining odd-prime formal-lift branches for
`rank-zero-selmer-AA-kernel-neg-2sqrt-q` be closed?

## Result

Yes. The odd-prime input is now:

```text
ell | L                 full image
ell | T                 local image contained in {1, -1}
ell | T^2 + 4*L^2       local image for x: {1}
```

普通话说：这个 kernel 在 `L` 的奇素数处完全放开；在 `T` 的奇素数处只允许
`1` 和 `-1` 两类；在 `T^2+4L^2` 的奇素数处只允许平方类。

## Proof Shape

For `ell | L`, write

```text
e  = v(L) >= 1
s  = 16*T^2
a2 = s + 32*L^2
a4 = 256*L^4
Q(x) = x^2 + a2*x + a4.
```

Here `a2` is a square unit and `a4` is a square of valuation `4e`. The
valuation split shows the ramified classes occur for `0 < v(x) < 4e`, and
the two unit classes occur by a finite-field residue lift when `-1` is
square and by a node-neighborhood lift `x=-16*T^2+c*L^2` when `-1` is not
square. Hence the local image is full.

For `ell | T`, use

```text
x^2 + a2*x + a4 = (x + 16*L^2)^2 + 16*T^2*x.
```

If `x + 16*L^2` is a unit, the quadratic factor is a square and `x` is
square. If not, `x` has the squareclass of `-16*L^2`, i.e. `-1`.

The `ell | T^2 + 4*L^2` case was already proved in the package transcript:
the local image is `{1}`.

## Boundary

This closes only the odd-prime formal-lift part of this package. It does not
prove the dyadic condition, the global Selmer bound, rank zero, or any
lambda-family exclusion.
