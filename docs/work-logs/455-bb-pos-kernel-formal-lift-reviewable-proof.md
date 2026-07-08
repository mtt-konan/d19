# BB Pos Kernel Formal-Lift Reviewable Proof

## Question

Can a second `BB` Selmer package get a direct reviewable
`formal_lift_compatibility` segment, without claiming the whole `BB` family is
done?

This note does that for the odd-prime segment of

```text
rank-zero-selmer-BB-kernel-pos-2sqrt-q.
```

## Result

Yes. For the package model

```text
E: y^2 = x^3 - 8*(T^2 + 8*L^2)*x^2 + 16*T^4*x
```

with primitive `A:B`, `L=B`, and `T=A+B`, the odd-prime formal-lift
conclusions are:

```text
ell | L                 every non-kernel point has trivial x-class
ell | T                 unit classes if -1 nonsquare; full image if -1 square
ell | T^2 + 4*L^2       every non-kernel point has trivial x-class
```

In ordinary language: this is one proof segment for one package. It covers odd
primes only. It does not prove the dyadic condition, the global Selmer bound,
rank zero, or any lambda-family exclusion.

## Setup

Fix an odd prime `ell`. Let `K` be a finite extension of `Q_ell`, let `O` be
its valuation ring, let `pi` be a uniformizer, and write `v` for the normalized
valuation. Put

```text
a2 = -8*(T^2 + 8*L^2)
a4 = 16*T^4
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

Because this is the `BB` package, `L=B`. Since `A:B` is primitive, the three
odd-prime branches `ell | L`, `ell | T`, and `ell | T^2 + 4*L^2` have the same
coprime-support properties as in the symbolic `L` proof.

## Theorem

For `rank-zero-selmer-BB-kernel-pos-2sqrt-q`, the odd-prime
`formal_lift_compatibility` statements above hold.

## Proof

### 1. Case `ell | L`

Here `T` is an `ell`-adic unit. Put

```text
r = 4*T^2.
```

Then `r` is a square unit, and the quadratic factor satisfies

```text
Q(x) = (x - r)^2 - 64*L^2*x.
```

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then `64*L^2*x` is divisible by `pi`, so `Q(x)` is
congruent to the non-zero square `(x-r)^2` modulo the maximal ideal. Hence
`Q(x)` is a square in `K*`, and the curve equation forces `x` to be a square.

If `x-r` is not a unit, then `x` has the same residue as the square unit `r`,
so `x` is itself a square in `K*`.

Therefore every non-kernel local point has trivial tracked squareclass when
`ell | L`.

### 2. Case `ell | T`

Here `L` is an `ell`-adic unit. Set

```text
e  = v(T) >= 1
s  = 64*L^2
a2 = -s - 8*T^2
a4 = 16*T^4
Q(x) = x^2 + a2*x + a4.
```

The element `s` is a square unit, `v(a2)=0`, and the unit squareclass of `a2`
is the squareclass of `-1`.

Let `P=(x,y)` be a local point with `x != 0`, and put `m=v(x)`.

If `m < 0`, then

```text
Q(x) = x^2 * (1 + a2/x + a4/x^2).
```

The parenthesized factor is `1 mod pi`, hence a square, so the curve equation
forces `x` to be a square.

If `m = 0`, then `x` is a unit, so only the two unit classes can occur.

If `0 < m < 4e`, then

```text
Q(x) = a2*x * (1 + x/a2 + a4/(a2*x)).
```

Again the parenthesized factor is a square. Therefore `x*Q(x)` has the
squareclass of `a2`. Such a point can exist only when `a2` is a square,
equivalently when `-1` is a square in `K`.

If `m = 4e`, then `x` has even valuation, so its squareclass is a unit class.
If `m > 4e`, then

```text
Q(x) = a4 * (1 + a2*x/a4 + x^2/a4),
```

with the parenthesized factor a square. Since `a4` is a square, the curve
equation again forces `x` to be a square.

These valuation ranges give the upper bound:

- if `-1` is not a square, only unit classes can occur;
- if `-1` is a square, ramified classes are also allowed.

It remains to realize the allowed classes.

The trivial class occurs by taking `x` with sufficiently large negative even
valuation.

A nonsquare unit class occurs by the standard finite-field character count:
for the residue field `k` and square unit `s`, there exists `x0 in k*` with
`x0` nonsquare and `x0-s` a non-zero square. After scaling `s` to `1`, the
number of such residues is

```text
(#k - chi(-1))/4,
```

which is positive for every odd residue field. Lifting such an `x0` gives

```text
x * Q(x) == x0^2 * (x0 - s) mod pi,
```

a non-zero square residue, hence a local point with `x` in a nonsquare unit
class.

Finally, when `-1` is a square, the element `a2` is a square unit. Then taking

```text
x = pi*u
```

with `u` square or nonsquare realizes the two ramified classes through the
range `0 < v(x) < 4e`.

So the `ell | T` branch has:

```text
if -1 is not a square:  the two unit classes
if -1 is a square:      all four squareclasses.
```

### 3. Case `ell | T^2 + 4*L^2`

Write

```text
d  = T^2 + 4*L^2
r  = -4*T^2.
```

Then `ell | d`, both `L` and `T` are units, and

```text
Q(x) = (x - r)^2 - 16*d*x.
```

Because `d == 0 mod pi`, the residue of `r` is `16*L^2`, a non-zero square.

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then the quadratic factor is congruent to the non-zero
square `(x-r)^2` modulo the maximal ideal. Hence `Q(x)` is a square in `K*`,
and the curve equation forces `x` to be a square.

If `x-r` is not a unit, then `x` has the same residue as `r`. Since `r` has
non-zero square residue, `x` is again a square in `K*`.

Therefore every non-kernel local point has trivial tracked squareclass when
`ell | T^2 + 4*L^2`.

## Conclusion

The odd-prime `formal_lift_compatibility` segment of
`rank-zero-selmer-BB-kernel-pos-2sqrt-q` is now written as a reviewable proof
package:

```text
ell | B                 local image for x: {1}
ell | A+B               unit classes if -1 nonsquare; full image if -1 square
ell | (A+B)^2 + 4*B^2   local image for x: {1}
```

This is the second `BB` package-level odd-prime formal-lift segment. It moves
`BB` from `1/3` to `2/3` at this narrow proof-layer only.

## Boundary

This note does not prove the full Selmer package. It does not address:

- the prime `2`,
- the global Selmer dimension bound,
- the rank-zero conclusion,
- any family-level exclusion theorem.

It also does not promote the package to a complete transcript. It records one
review-ready odd-prime segment only.
