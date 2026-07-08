# AA Minus-P Formal-Lift Reviewable Proof

## Question

Can the odd-prime `formal_lift_compatibility` segment for

```text
rank-zero-selmer-AA-kernel-minus-p
```

be frozen as a reviewable proof package, including the corrected
zero-double-root branch at primes dividing `T^2 + 4*L^2`?

## Result

Yes. For the package model

```text
E: y^2 = x^3 + (32*L^2 - 8*T^2)*x^2 + 16*(T^2 + 4*L^2)^2*x
```

with primitive `A:B`, `L=A`, `T=A+B`, the odd-prime formal-lift conclusions
are:

```text
ell | L                 every non-kernel point has trivial x-class
ell | T                 every non-kernel point has x-class in {1, -1}
ell | T^2 + 4*L^2       full image in Q_ell*/Q_ell*2
```

普通话说：这份文稿把 `AA / kernel_minus_p` 的 odd-prime
`formal_lift_compatibility` 固定成可逐行检查的 proof。特别是最后一条不再沿用
早先的 naive `{1}` 想象，而是明确改成“full image”。

## Setup

Fix an odd prime `ell`, let `K` be a finite extension of `Q_ell`, let `O` be
its valuation ring, `pi` a uniformizer, and `v` the normalized valuation.
Write

```text
a2 = 32*L^2 - 8*T^2
a4 = 16*(T^2 + 4*L^2)^2
Q(x) = x^2 + a2*x + a4,
```

so the curve equation is

```text
y^2 = x * Q(x).
```

The tracked descent coordinate is the squareclass of `x` for points with
`x != 0`.

We repeatedly use the usual odd-prime square-lifting criterion:

1. a unit with non-zero square residue is a square in `K*`;
2. an element congruent to `1 mod pi` is a square in `K*`.

## Theorem

For the package `rank-zero-selmer-AA-kernel-minus-p`, the odd-prime
formal-lift compatibility statements above hold.

## Proof

### 1. Case `ell | L`

Because `A:B` is primitive and `L=A`, the element `T=A+B` is an `ell`-adic
unit. Put

```text
r = 4*(T^2 + 4*L^2).
```

Then `r` is a unit with square residue `4*T^2`, and

```text
Q(x) = (x - r)^2 + 64*L^2*x.
```

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then the quadratic factor is congruent to the non-zero
square `(x-r)^2` modulo `pi`, hence is a square in `K*`. The curve equation
then forces `x` to be a square.

If `x-r` is not a unit, then `x` has the same residue as `r`, whose residue is
a non-zero square. So `x` is again a square in `K*`.

Therefore every non-kernel local point has trivial tracked squareclass when
`ell | L`.

### 2. Case `ell | T`

Here primitiveness gives that `L` is an `ell`-adic unit. The reduction shape is

```text
x*(x + 16*L^2)^2.
```

The quadratic factor satisfies

```text
Q(x) = (x + 16*L^2)^2 - 8*T^2*(x - 16*L^2 - 2*T^2).
```

Let `P=(x,y)` be a local point with `x != 0`.

If `x + 16*L^2` is a unit, then `Q(x)` has non-zero square residue modulo
`pi`, hence is a square in `K*`. The curve equation forces `x` to be a square.

If `x + 16*L^2` is not a unit, then `x` has the same residue as `-16*L^2`.
Because `16*L^2` is a square unit, the squareclass of `x` is the class of
`-1`.

Thus every non-kernel local point has tracked squareclass in

```text
{1, -1}.
```

### 3. Case `ell | T^2 + 4*L^2`

This is the zero-double-root branch. The naive candidates "`x` always square"
and "`x + 64*L^2` always square" are both false; the corrected local image is
full.

Write

```text
d  = T^2 + 4*L^2
s  = 64*L^2
a2 = s - 8*d
a4 = 16*d^2.
```

Then `v(d) >= 1`, `s` is a square unit, `a2` is a square unit because

```text
a2/s == 1 mod pi,
```

and `a4` is a square.

We show that all four odd-prime squareclasses occur.

First, the trivial class occurs by taking

```text
x = pi^(2*N)*u
```

with `N > v(d)` and `u` a square unit. Then

```text
Q(x) = a4 * (1 + a2*x/a4 + x^2/a4),
```

where the parenthesized factor is `1 mod pi`, hence a square. Since both `x`
and `a4` are squares, the right-hand side of the curve equation is a square.

Second, both ramified classes occur by taking

```text
x = pi*u
```

with `u` a unit. Then

```text
Q(x) = a2*pi*u * (1 + pi*u/a2 + 16*d^2/(a2*pi*u)),
```

and the parenthesized factor is again a square. Because `a2` is a square unit,
the squareclass of `x*Q(x)` is trivial for either choice of unit class of `u`.
Choosing `u` square or nonsquare realizes the two ramified classes.

It remains to realize the nonsquare unit class. Reduce modulo `ell`. Because
`T^2 + 4*L^2 == 0 mod ell` and `L` is a unit, `-1` is a square in the residue
field. For the square unit `s`, there exists `x0 in k*` such that `x0` is
nonsquare and `x0 + s` is a non-zero square. After scaling `s` to `1`, this is
the standard character count

```text
#{t in k*, t != 1 : chi(t)=1 and chi(t-1)=-1} = (#k - 1)/4.
```

Lift such an `x0` to a unit `x in O*`. Modulo `pi`,

```text
x * Q(x) == x0^2 * (x0 + s),
```

which has non-zero square residue. Hence the right-hand side of the curve
equation is a square in `K*`, so this lifted point realizes the nonsquare unit
class.

All four squareclasses occur. Therefore

```text
{ squareclasses of x(P) : P in E(Q_ell), x(P) != 0 } = Q_ell*/Q_ell*2
```

when `ell | T^2 + 4*L^2`.

## Conclusion

The odd-prime `formal_lift_compatibility` segment of
`rank-zero-selmer-AA-kernel-minus-p` is now written as a single reviewable
proof package:

```text
ell | L                 local image for x: {1}
ell | T                 local image for x: {1, -1}
ell | T^2 + 4*L^2       full image
```

In ordinary language: the first two odd-prime branches are restrictive, but
the zero-double-root branch is not restrictive at all on the original descent
coordinate `x`.

## Boundary

This note does not prove the full Selmer package. It does not address:

- the prime `2`,
- the corrected global Selmer dimension bound,
- the rank-zero conclusion,
- any family-level exclusion theorem.

It also does not change any audit count from `0` to `1`. This is a
review-ready proof write-up for one package segment only.
