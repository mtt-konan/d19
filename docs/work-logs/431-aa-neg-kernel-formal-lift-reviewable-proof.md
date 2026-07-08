# AA Neg Kernel Formal-Lift Reviewable Proof

## Question

Can we take one of the still-open transcript segments for a single rank-zero
Selmer package and write it as a reviewable proof, without pretending that the
whole package is done?

This note does that for the odd-prime `formal_lift_compatibility` segment of

```text
rank-zero-selmer-AA-kernel-neg-2sqrt-q.
```

## Result

Yes. For the package model

```text
E: y^2 = x^3 + 16*(T^2 + 2*L^2)*x^2 + 256*L^4*x
```

with primitive `A:B`, `L=A`, `T=A+B`, the odd-prime formal-lift conclusions
are:

```text
ell | L                 full image in K*/K*2
ell | T                 every non-kernel point has x-class in {1, -1}
ell | T^2 + 4*L^2       every non-kernel point has trivial x-class
```

普通话说：这份文稿只做一件事: 把这个 package 的 odd-prime
`formal_lift_compatibility` 写成能逐行检查的证明。它还没有处理 `ell=2`、global
Selmer bound、rank zero，也不会把任何 audit 计数改成“已完成”。

## Setup

Fix an odd prime `ell`, let `K` be a finite extension of `Q_ell`, let `O` be
its valuation ring, `pi` a uniformizer, and `v` the normalized valuation.
Write

```text
a2 = 16*(T^2 + 2*L^2)
a4 = 256*L^4
Q(x) = x^2 + a2*x + a4,
```

so the curve equation is

```text
y^2 = x * Q(x).
```

The tracked descent coordinate is the squareclass of `x` for points with
`x != 0`.

Two local facts will be used repeatedly.

1. If `u in O*` has non-zero square residue, then `u` is a square in `K*`.
2. If `w in K*` satisfies `w == 1 mod pi`, then `w` is a square in `K*`.

Both are the usual odd-prime square-lifting criterion.

## Theorem

For the package `rank-zero-selmer-AA-kernel-neg-2sqrt-q`, the odd-prime
formal-lift compatibility statements above hold.

## Proof

### 1. Case `ell | L`

Because `A:B` is primitive and `L=A`, the element `T=A+B` is an `ell`-adic
unit. Set

```text
e  = v(L) >= 1
s  = 16*T^2
a2 = s + 32*L^2
a4 = 256*L^4.
```

Then `s` is a square unit. Also `a2` is a square unit because

```text
a2/s == 1 mod pi,
```

and `v(32*L^2/s) > 0`, so `a2/s` is congruent to `1`. Finally `a4` is a
square of valuation `4e`.

Let `P=(x,y)` be a `K`-point with `x != 0`, and write `m=v(x)`.

If `m < 0`, then

```text
Q(x) = x^2 * (1 + a2/x + a4/x^2).
```

Since `v(a2)=0`, `v(a4)=4e`, and `m<0`, both `a2/x` and `a4/x^2` have
positive valuation. So the parenthesized factor is `1 mod pi`, hence a
square. Therefore `Q(x)` has the same squareclass as `x^2`, and the equation
`y^2 = x*Q(x)` forces `x` itself to be a square.

If `0 < m < 4e`, then

```text
Q(x) = a2*x * (1 + x/a2 + a4/(a2*x)).
```

Again the parenthesized factor is `1 mod pi`, hence a square. Because `a2` is
a square unit, `x*Q(x)` is a square for every such `x`. In particular, taking

```text
x = pi*u
```

with `u` square or nonsquare realizes the two odd-valuation squareclasses.

If `m > 4e`, then

```text
Q(x) = a4 * (1 + a2*x/a4 + x^2/a4).
```

Now `v(a2*x/a4)=m-4e>0` and `v(x^2/a4)=2m-4e>0`, so the parenthesized factor
is again `1 mod pi` and therefore a square. Since `a4` is a square, the curve
equation again forces `x` to be a square.

The boundary cases `m=0` and `m=4e` have even valuation, so they can only
contribute unit squareclasses.

It remains to show that both unit classes do occur.

The trivial squareclass occurs by taking `x` with sufficiently large negative
even valuation; then the `m < 0` analysis applies and `x` is already a square.

For the nonsquare unit class there are two subcases.

First suppose `-1` is a square in the residue field. Because `s` is a square
unit, it is enough to find `u in k*` such that `u` is nonsquare and `u+1` is a
non-zero square. This is the standard two-character count

```text
#{u in k*, u != -1 : chi(u)=-1 and chi(u+1)=1} = (#k - 1)/4.
```

which is positive because `-1` square implies `#k == 1 mod 4`, hence `#k >=
5`. Choose such a residue `x0` and lift it to a unit `x in O*`. Modulo `pi`,

```text
x * Q(x) == x0^2 * (x0 + s),
```

which has non-zero square residue. Hence `x*Q(x)` is a square in `K*`, so
there is a local point with `x` in the nonsquare unit class.

Now suppose `-1` is not a square in the residue field. Then `-s` is in the
nonsquare unit class. Choose any non-zero square residue `t` with `t != 32`,
and let `c in O*` satisfy

```text
c == t - 32 mod pi.
```

Then `c+32` has square residue `t`. Set

```text
x = -s + c*L^2.
```

Because `v(L) >= 1`, this `x` has the same residue as `-s`, so `x` is a
nonsquare unit. Writing `delta = c*L^2`, a direct expansion gives

```text
Q(-s + delta)
  = delta^2 - s*delta + 32*L^2*delta - 32*s*L^2 + 256*L^4.
```

Dividing by `L^2` and reducing modulo `pi` yields

```text
Q(x)/L^2 == -s*(c+32) mod pi.
```

Since `L^2` is a square and `c+32` has square residue, the squareclass of
`Q(x)` is again the squareclass of `-s`. Therefore `x` and `Q(x)` have the
same nonsquare unit class, so

```text
x * Q(x)
```

is a square in `K*`. This produces a local point in the nonsquare unit class.

We have now realized both unit classes and both ramified classes. Therefore

```text
{ squareclasses of x(P) : P in E(K), x(P) != 0 } = K*/K*2
```

when `ell | L`.

### 2. Case `ell | T`

Here primitiveness gives that `L` is an `ell`-adic unit. Put

```text
r = -16*L^2.
```

Then a direct identity gives

```text
Q(x) = (x - r)^2 + 16*T^2*x.
```

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then the term `16*T^2*x` is divisible by `pi`, so

```text
Q(x) == (x-r)^2 mod pi.
```

The residue is a non-zero square, hence `Q(x)` is a square in `K*`. The curve
equation then forces `x` to be a square.

If `x-r` is not a unit, then `x` has the same residue as `r=-16*L^2`. Since
`16*L^2` is a square unit, `x` has squareclass `-1`.

So every non-kernel local point satisfies

```text
x-class in {1, -1}.
```

This is the formal-lift compatibility statement needed for the package. It is
an upper bound, not a proof that both classes always occur.

### 3. Case `ell | T^2 + 4*L^2`

Write

```text
d = T^2 + 4*L^2
r = 16*L^2.
```

Since `A:B` is primitive, both `L` and `T` are units in this case, and `r` is
a square unit. Another direct identity gives

```text
Q(x) = (x - r)^2 + 16*d*x.
```

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then `16*d*x` is divisible by `pi`, so `Q(x)` is
congruent to the non-zero square `(x-r)^2` modulo `pi`. Hence `Q(x)` is a
square in `K*`, and the curve equation forces `x` to be a square.

If `x-r` is not a unit, then `x` has the same residue as the square unit `r`,
so `x` is itself a square in `K*`.

Therefore every non-kernel local point has trivial tracked squareclass when
`ell | T^2 + 4*L^2`.

This is exactly the package claim that the `d`-prime branch contributes only
the trivial class.

## Conclusion

The odd-prime `formal_lift_compatibility` segment of
`rank-zero-selmer-AA-kernel-neg-2sqrt-q` is now written as a single
reviewable proof package:

```text
ell | L                 full image
ell | T                 contained in {1, -1}
ell | T^2 + 4*L^2       contained in {1}
```

In ordinary language: at odd primes over `L`, this kernel imposes no
squareclass restriction; at odd primes over `T`, it only allows the trivial
class or the class of `-1`; and at odd primes over `T^2 + 4*L^2`, it forces
the squareclass to be trivial.

## Boundary

This note does not prove the full Selmer package. It does not address:

- the prime `2`,
- the global Selmer dimension bound,
- the rank-zero conclusion,
- any family-level exclusion theorem.

It also does not change any audit count from `0` to `1`. This is a
review-ready proof write-up for one package segment only.
