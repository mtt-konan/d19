# rank-zero-selmer-AA-kernel-pos-2sqrt-q

Status: open

## Scope

- family_pattern = AA
- kernel = kernel_pos_2sqrt_q
- candidate_class_count = 82
- model_count = 82

## Symbolic Model

- T = A+B
- L role = A for AA, B for BB; AA+BB requires both sides to close
- kernel_root = 2*sqrt_q
- target_a2 = -8*(T^2 + 8*L^2)
- target_a4 = 16*T^4

## Required Transcript

- statement
- isogeny_setup
- local_squareclass_conditions
- selmer_bound_argument
- rank_zero_conclusion
- review_notes

## Partial Transcript: formal_lift_compatibility

### Subclaim: odd prime `ell | L`

- package: `rank-zero-selmer-AA-kernel-pos-2sqrt-q`
- local case: odd prime `ell | L`
- assumptions: `A:B` is primitive, `L=A`, `T=A+B`; hence `T` is an
  `ell`-adic unit in this case
- target model:

```text
y^2 = x^3 - 8*(T^2 + 8*L^2)*x^2 + 16*T^4*x
```

The mod-`ell` reduction shape is

```text
x*(x - 4*T^2)^2.
```

The tracked squareclass is the squareclass of `x` away from the kernel point
`x=0`.

### Claim

For every odd-prime local field `K` with valuation above such an `ell`, every
`K`-point on the displayed model with `x != 0` has `x` in the trivial class
of `K*/K*2`.

### Proof

Write

```text
a2 = -8*(T^2 + 8*L^2)
a4 = 16*T^4
r  = 4*T^2.
```

Since `ell | L` and `A:B` is primitive, `T` is an `ell`-adic unit. Hence
`r` is a square unit. The quadratic factor satisfies the exact identity

```text
x^2 + a2*x + a4 = (x - r)^2 - 64*L^2*x.
```

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then the quadratic factor is congruent to `(x-r)^2`
modulo the maximal ideal, hence is a square in `K*` by the odd-prime
square-lifting criterion. Since

```text
y^2 = x * (x^2 + a2*x + a4),
```

the element `x` is also a square.

If `x-r` is not a unit, then `x` has the same non-zero residue as the square
unit `r`, so `x` is a square in `K*`.

Thus every non-kernel local point has trivial tracked squareclass. This
proves the `ell | L` formal-lift subclaim for
`rank-zero-selmer-AA-kernel-pos-2sqrt-q`.

### Subclaim: odd prime `ell | T`

- package: `rank-zero-selmer-AA-kernel-pos-2sqrt-q`
- local case: odd prime `ell | T`
- assumptions: `A:B` is primitive, `L=A`, `T=A+B`; hence `L` is an
  `ell`-adic unit in this case
- target model:

```text
y^2 = x^3 - 8*(T^2 + 8*L^2)*x^2 + 16*T^4*x
```

The mod-`ell` reduction shape is

```text
x^2*(x - 64*L^2).
```

This is the zero-double-root tangent-minus-one case. The tracked
squareclass is the squareclass of `x` away from the kernel point `x=0`.

### Claim

Let `K` be an odd-prime local field above such an `ell`, and let `pi` be a
uniformizer. The local image is:

```text
if -1 is not a square in K:  the two unit classes {1, epsilon}
if -1 is a square in K:      all four classes {1, epsilon, pi, epsilon*pi}
```

where `epsilon` is any fixed nonsquare unit. Equivalently, when `-1` is not
a square, no ramified class occurs; when `-1` is a square, the formal lift
imposes no squareclass restriction.

### Proof

Write

```text
e  = v(T) >= 1
s  = 64*L^2
a2 = -8*(T^2 + 8*L^2) = -s - 8*T^2
a4 = 16*T^4
Q(x) = x^2 + a2*x + a4.
```

Here `s` is a square unit, `v(a2)=0`, and the unit squareclass of `a2` is
the squareclass of `-1`.

Let `P=(x,y)` be a local point with `x != 0`, and set `m=v(x)`. The curve
equation is

```text
y^2 = x * Q(x).
```

First suppose `m < 0`. Then

```text
Q(x) = x^2 * (1 + a2/x + a4/x^2),
```

and the parenthesized factor is congruent to `1` modulo the maximal ideal,
hence is a square. Thus `x*Q(x)` has the same squareclass as `x^3`, so the
existence of `y` forces `x` itself to be a square.

If `m = 0`, then `x` is a unit, so its squareclass is one of the two unit
classes.

If `0 < m < 4*e`, then

```text
Q(x) = a2*x * (1 + x/a2 + a4/(a2*x)),
```

and the parenthesized factor is again congruent to `1`, hence is a square.
Therefore `x*Q(x)` has squareclass `a2*x^2`, i.e. the squareclass of `a2`.
Such a point can exist only when `a2` is a square, equivalently when `-1`
is a square in `K`.

If `m = 4*e`, then `x` has even valuation, so its squareclass is a unit
class. If `m > 4*e`, then

```text
Q(x) = a4 * (1 + a2*x/a4 + x^2/a4),
```

with the parenthesized factor a square; since `a4` is a square, the curve
equation forces `x` to be a square.

These valuation cases prove the upper bound: if `-1` is not a square, only
unit classes can occur; if `-1` is a square, all four classes are allowed by
the valuation argument.

It remains to see that the allowed classes really occur. The trivial class
occurs by taking `x` of sufficiently large negative even valuation, so that
the first case applies with `x` already a square. A nonsquare unit class
occurs by the finite-field fact that for the residue field `k` and square
unit `s`, there is `x0 in k*` with `x0` nonsquare and `x0-s` a non-zero
square. After scaling `s` to `1`, the number of such residues is

```text
(#k - chi(-1))/4,
```

so it is positive for every odd residue field. Lifting such an `x0` makes

```text
x * Q(x) == x0^2 * (x0 - s) mod ell,
```

a non-zero square residue. Finally, when `-1` is a square, `a2` is a square
unit, and taking

```text
x = pi*u
```

with `u` square or nonsquare realizes the two ramified classes by the
`0 < m < 4*e` case.

This proves the `ell | T` zero-double-root formal-lift subclaim for
`rank-zero-selmer-AA-kernel-pos-2sqrt-q`.

### Subclaim: odd prime `ell | T^2 + 4*L^2`

This records the local subclaim needed after the `AA / kernel_minus_p`
package showed full image at the same primes.

- package: `rank-zero-selmer-AA-kernel-pos-2sqrt-q`
- local case: odd prime `ell | T^2 + 4*L^2`
- assumptions: `A:B` is primitive, `L=A`, `T=A+B`; hence `L` and `T` are
  `ell`-adic units in this case
- target model:

```text
y^2 = x^3 - 8*(T^2 + 8*L^2)*x^2 + 16*T^4*x
```

The mod-`ell` reduction shape is

```text
x*(x - 16*L^2)^2.
```

Equivalently, since `T^2 + 4*L^2 == 0 mod ell`, the double root is the
square unit

```text
r = -4*T^2 == 16*L^2 mod ell.
```

The tracked squareclass is the squareclass of `x` away from the kernel point
`x=0`.

### Claim

For every odd-prime local field `K` with valuation above such an `ell`, every
`K`-point on the displayed model with `x != 0` has `x` in the trivial class
of `K*/K*2`.

In ordinary terms: the `T^2 + 4*L^2` primes that were free for
`kernel_minus_p` are locally killed by this `kernel_pos_2sqrt_q` descent
coordinate.

### Proof

Write

```text
d  = T^2 + 4*L^2
a2 = -8*(T^2 + 8*L^2)
a4 = 16*T^4
r  = -4*T^2.
```

Then `ell | d`, `L` and `T` are units, and

```text
x^2 + a2*x + a4 = (x - r)^2 - 16*d*x.
```

Because `d == 0 mod ell`, the residue of `r` is `16*L^2`, a non-zero square.

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then the identity shows that the quadratic factor
`x^2 + a2*x + a4` is congruent to `(x-r)^2` modulo the maximal ideal.
Since `ell` is odd, it is a square in `K*`. The curve equation

```text
y^2 = x * (x^2 + a2*x + a4)
```

then forces `x` to be a square.

If `x-r` is not a unit, then `x` has the same residue as `r`. Since `r` has
non-zero square residue, the odd-prime unit square criterion says `x` is a
square in `K*`.

These two cases cover every non-kernel local point. Therefore the
`ell | T^2 + 4*L^2` formal lift has local image `{1}` for
`rank-zero-selmer-AA-kernel-pos-2sqrt-q`.

### Odd-prime summary

The odd-prime formal-lift input for this package is now:

```text
ell | L                 local image for x: {1}
ell | T                 unit classes if -1 nonsquare; full image if -1 square
ell | T^2 + 4*L^2       local image for x: {1}
```

This closes the odd-prime formal-lift part of the package transcript. It
does not by itself prove the dyadic local condition or the global Selmer
dimension bound.

### Remaining Gaps

This does not prove the whole package. The following parts remain open:

- the `ell=2` local condition
- the global Selmer dimension bound
- the rank-zero conclusion
- any `lambda`-family exclusion

## Boundary

transcript_status = missing

No Selmer rank upper bound is proved by this file. No rank-zero theorem or lambda-family exclusion is claimed here.
