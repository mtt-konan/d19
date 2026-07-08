# BB Neg Kernel Formal-Lift Reviewable Proof

## Question

Can one `BB` Selmer package get a real reviewable
`formal_lift_compatibility` segment, instead of only inheriting the general
transport note?

This note does that for the odd-prime segment of

```text
rank-zero-selmer-BB-kernel-neg-2sqrt-q.
```

## Result

Yes. For the package model

```text
E: y^2 = x^3 + 16*(T^2 + 2*L^2)*x^2 + 256*L^4*x
```

with primitive `A:B`, `L=B`, and `T=A+B`, the odd-prime formal-lift
conclusions are:

```text
ell | L                 full image in K*/K*2
ell | T                 every non-kernel point has x-class in {1, -1}
ell | T^2 + 4*L^2       every non-kernel point has trivial x-class
```

In ordinary language: this proves exactly one package segment. It covers odd
primes only. It does not cover the prime `2`, the global Selmer bound, rank
zero, or any lambda-family exclusion.

## Setup

Fix an odd prime `ell`. Let `K` be a finite extension of `Q_ell`, let `O` be
its valuation ring, let `pi` be a uniformizer, and write `v` for the normalized
valuation. Put

```text
a2 = 16*(T^2 + 2*L^2)
a4 = 256*L^4
Q(x) = x^2 + a2*x + a4,
```

so the curve equation is

```text
y^2 = x * Q(x).
```

The descent coordinate tracked here is the squareclass of `x` for points with
`x != 0`.

We use two standard odd-prime lifting facts.

1. A unit with non-zero square residue is a square in `K*`.
2. An element congruent to `1 mod pi` is a square in `K*`.

Because this is the `BB` package, `L=B`. Since `A:B` is primitive, an odd prime
dividing `L` does not divide `T=A+B`; an odd prime dividing `T` does not divide
`L`; and an odd prime dividing `T^2 + 4*L^2` divides neither `T` nor `L`.

## Theorem

For `rank-zero-selmer-BB-kernel-neg-2sqrt-q`, the odd-prime
`formal_lift_compatibility` statements above hold.

## Proof

### 1. Case `ell | L`

Here `T` is an `ell`-adic unit. Set

```text
e  = v(L) >= 1
s  = 16*T^2
a2 = s + 32*L^2
a4 = 256*L^4.
```

Then `s` is a square unit. Also `a2` is a square unit, because

```text
a2/s == 1 mod pi.
```

Finally, `a4` is a square and has valuation `4e`.

Let `P=(x,y)` be a local point with `x != 0`, and write `m=v(x)`.

If `m < 0`, then

```text
Q(x) = x^2 * (1 + a2/x + a4/x^2).
```

The two correction terms have positive valuation, so the parenthesized factor
is `1 mod pi`, hence a square. Thus `Q(x)` has the same squareclass as `x^2`,
and `y^2 = x*Q(x)` forces `x` to be a square.

If `0 < m < 4e`, then

```text
Q(x) = a2*x * (1 + x/a2 + a4/(a2*x)).
```

Again the parenthesized factor is a square. Since `a2` is a square unit,
`x*Q(x)` is a square for every such `x`. Taking

```text
x = pi*u
```

with `u` square or nonsquare realizes the two odd-valuation squareclasses.

If `m > 4e`, then

```text
Q(x) = a4 * (1 + a2*x/a4 + x^2/a4).
```

The parenthesized factor is a square, and `a4` is a square, so the equation
again forces `x` to be a square.

The boundary valuations `m=0` and `m=4e` only give unit squareclasses. The
trivial unit class occurs by taking `x` with sufficiently large negative even
valuation.

It remains to realize a nonsquare unit class.

If `-1` is a square in the residue field, choose a residue `u in k*` such that
`u` is nonsquare and `u+1` is a non-zero square. The standard two-character
count gives such a residue:

```text
#{u in k*, u != -1 : chi(u)=-1 and chi(u+1)=1} = (#k - 1)/4.
```

Lift it to a unit `x in O*`. Modulo `pi`, the right-hand side satisfies

```text
x * Q(x) == x^2 * (x + s),
```

with non-zero square residue. Hence a local point exists with `x` in the
nonsquare unit class.

If `-1` is not a square in the residue field, then `-s` is a nonsquare unit.
Choose a non-zero square residue `t` with `t != 32`, and choose `c in O*` with

```text
c == t - 32 mod pi.
```

Set

```text
x = -s + c*L^2.
```

Then `x` has the same residue as `-s`, so `x` is a nonsquare unit. Writing
`delta = c*L^2`, expand:

```text
Q(-s + delta)
  = delta^2 - s*delta + 32*L^2*delta - 32*s*L^2 + 256*L^4.
```

After dividing by `L^2` and reducing modulo `pi`,

```text
Q(x)/L^2 == -s*(c+32) mod pi.
```

Since `L^2` is a square and `c+32` has square residue, `Q(x)` has the same
nonsquare unit squareclass as `x`. Therefore `x*Q(x)` is a square.

So, when `ell | L`, all four odd-prime squareclasses occur:

```text
{ squareclasses of x(P) : P in E(K), x(P) != 0 } = K*/K*2.
```

### 2. Case `ell | T`

Here `L` is an `ell`-adic unit. Put

```text
r = -16*L^2.
```

The quadratic factor has the identity

```text
Q(x) = (x - r)^2 + 16*T^2*x.
```

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then `16*T^2*x` is divisible by `pi`, so `Q(x)` has the
same non-zero square residue as `(x-r)^2`. Hence `Q(x)` is a square in `K*`,
and `y^2 = x*Q(x)` forces `x` to be a square.

If `x-r` is not a unit, then `x` has the same residue as `r=-16*L^2`. Since
`16*L^2` is a square unit, the squareclass of `x` is the class of `-1`.

Therefore every non-kernel local point has

```text
x-class in {1, -1}.
```

This is an upper bound on the local image. It is not a claim that both classes
must always occur.

### 3. Case `ell | T^2 + 4*L^2`

Write

```text
d = T^2 + 4*L^2
r = 16*L^2.
```

In this case both `L` and `T` are units, and `r` is a square unit. The
quadratic factor satisfies

```text
Q(x) = (x - r)^2 + 16*d*x.
```

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then `16*d*x` is divisible by `pi`, so `Q(x)` is congruent
to the non-zero square `(x-r)^2` modulo `pi`. Thus `Q(x)` is a square in `K*`,
and the curve equation forces `x` to be a square.

If `x-r` is not a unit, then `x` has the same residue as the square unit `r`,
so `x` is again a square in `K*`.

Therefore every non-kernel local point has trivial tracked squareclass when
`ell | T^2 + 4*L^2`.

## Conclusion

The odd-prime `formal_lift_compatibility` segment of
`rank-zero-selmer-BB-kernel-neg-2sqrt-q` is now written as a reviewable proof
package:

```text
ell | B                 full image
ell | A+B               contained in {1, -1}
ell | (A+B)^2 + 4*B^2   contained in {1}
```

This is the `BB` version of the symbolic `L`-proof. The point of writing it
here is practical: this package can now be reviewed directly, without asking a
reader to infer every detail from the family-level transport note.

## Boundary

This note does not prove the full Selmer package. It does not address:

- the prime `2`,
- the global Selmer dimension bound,
- the rank-zero conclusion,
- any family-level exclusion theorem.

It also does not promote the package to a complete transcript. It records one
review-ready odd-prime segment only.
