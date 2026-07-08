# rank-zero-selmer-AA-kernel-neg-2sqrt-q

Status: open

## Scope

- family_pattern = AA
- kernel = kernel_neg_2sqrt_q
- candidate_class_count = 82
- model_count = 82

## Symbolic Model

- T = A+B
- L role = A for AA, B for BB; AA+BB requires both sides to close
- kernel_root = -2*sqrt_q
- target_a2 = 16*(T^2 + 2*L^2)
- target_a4 = 256*L^4

## Required Transcript

- statement
- isogeny_setup
- local_squareclass_conditions
- selmer_bound_argument
- rank_zero_conclusion
- review_notes

## Partial Transcript: formal_lift_compatibility

### Subclaim: odd prime `ell | L`

- package: `rank-zero-selmer-AA-kernel-neg-2sqrt-q`
- local case: odd prime `ell | L`
- assumptions: `A:B` is primitive, `L=A`, `T=A+B`; hence `T` is an
  `ell`-adic unit in this case
- target model:

```text
y^2 = x^3 + 16*(T^2 + 2*L^2)*x^2 + 256*L^4*x
```

The mod-`ell` reduction shape is

```text
x^2*(x + 16*T^2).
```

This is the zero-double-root tangent-one case. The tracked squareclass is
the squareclass of `x` away from the kernel point `x=0`.

### Claim

For every odd-prime local field `K` with valuation above such an `ell`,

```text
{ squareclasses of x(P) : P in E(K), x(P) != 0 } = K*/K*2.
```

Thus this branch imposes no local squareclass restriction.

### Proof

Write `pi` for a uniformizer and set

```text
e  = v(L) >= 1
s  = 16*T^2
a2 = 16*(T^2 + 2*L^2) = s + 32*L^2
a4 = 256*L^4
Q(x) = x^2 + a2*x + a4.
```

Here `s` and `a2` are square units, and `a4` is a square with valuation
`4*e`.

Let `P=(x,y)` be a local point with `x != 0`, and put `m=v(x)`.

If `m < 0`, then

```text
Q(x) = x^2 * (1 + a2/x + a4/x^2),
```

where the parenthesized factor is congruent to `1`, hence a square. The
curve equation then forces `x` to be a square.

If `0 < m < 4*e`, then

```text
Q(x) = a2*x * (1 + x/a2 + a4/(a2*x)).
```

The parenthesized factor is again a square, and `a2` is a square unit.
Therefore `x*Q(x)` is automatically a square for every squareclass of such
an `x`. Taking `x=pi*u`, with `u` square or nonsquare, realizes the two
ramified squareclasses.

If `m > 4*e`, then

```text
Q(x) = a4 * (1 + a2*x/a4 + x^2/a4),
```

so the curve equation forces `x` to be a square. The boundary case
`m=4*e` has even valuation and therefore gives only unit classes.

The two unit classes occur as follows. The trivial class occurs by choosing
`x` with sufficiently large negative even valuation.

For a nonsquare unit class, first suppose `-1` is a square in the residue
field. Since `s` is a square unit, there exists `x0 in k*` with `x0`
nonsquare and `x0+s` a non-zero square; after scaling `s` to `1`, the number
of such residues is

```text
(#k - 1)/4,
```

which is positive because `#k` is odd and `-1` square implies `#k >= 5`.
Lifting such an `x0` gives

```text
x * Q(x) == x0^2 * (x0 + s) mod ell,
```

a non-zero square residue, so Hensel square-lifting gives a local point with
`x` in a nonsquare unit class.

Now suppose `-1` is not a square in the residue field. Then the class of
`-s` is the nonsquare unit class. Take

```text
x = -s + c*L^2
```

with `c` an integral unit chosen so that `c+32` has non-zero square residue.
Then `x` has the nonsquare unit class. Writing `delta=c*L^2`, the expansion

```text
Q(-s + delta)
  = delta^2 - s*delta + 32*L^2*delta - 32*s*L^2 + 256*L^4
```

gives

```text
Q(x)/L^2 == -s*(c+32) mod ell.
```

Hence

```text
x*Q(x) == (-s) * L^2 * (-s)*(c+32) mod squares,
```

which is a square. This realizes the nonsquare unit class also when `-1` is
not a square.

All four squareclasses occur. This proves the `ell | L` formal-lift subclaim
for `rank-zero-selmer-AA-kernel-neg-2sqrt-q`.

### Subclaim: odd prime `ell | T`

- package: `rank-zero-selmer-AA-kernel-neg-2sqrt-q`
- local case: odd prime `ell | T`
- assumptions: `A:B` is primitive, `L=A`, `T=A+B`; hence `L` is an
  `ell`-adic unit in this case
- target model:

```text
y^2 = x^3 + 16*(T^2 + 2*L^2)*x^2 + 256*L^4*x
```

The mod-`ell` reduction shape is

```text
x*(x + 16*L^2)^2.
```

The tracked squareclass is the squareclass of `x` away from the kernel point
`x=0`.

### Claim

For every odd-prime local field `K` with valuation above such an `ell`, every
`K`-point on the displayed model with `x != 0` has squareclass in
`{1, -1}`.

### Proof

Write

```text
a2 = 16*(T^2 + 2*L^2)
a4 = 256*L^4
r  = -16*L^2.
```

The quadratic factor satisfies

```text
x^2 + a2*x + a4 = (x - r)^2 + 16*T^2*x.
```

If `x-r` is a unit, then the quadratic factor has non-zero square residue,
so it is a square in `K*`. The curve equation then forces `x` to be a
square.

If `x-r` is not a unit, then `x` has the same residue as `r=-16*L^2`, so
the squareclass of `x` is the class of `-1`.

Thus every non-kernel local point has tracked squareclass in `{1, -1}`. This
proves the `ell | T` formal-lift compatibility subclaim for
`rank-zero-selmer-AA-kernel-neg-2sqrt-q`.

### Subclaim: odd prime `ell | T^2 + 4*L^2`

This records the matching local subclaim for the other `AA` square-root
kernel.

- package: `rank-zero-selmer-AA-kernel-neg-2sqrt-q`
- local case: odd prime `ell | T^2 + 4*L^2`
- assumptions: `A:B` is primitive, `L=A`, `T=A+B`; hence `L` and `T` are
  `ell`-adic units in this case
- target model:

```text
y^2 = x^3 + 16*(T^2 + 2*L^2)*x^2 + 256*L^4*x
```

The mod-`ell` reduction shape is

```text
x*(x - 16*L^2)^2.
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
d  = T^2 + 4*L^2
a2 = 16*(T^2 + 2*L^2)
a4 = 256*L^4
r  = 16*L^2.
```

Then `ell | d`, `L` and `T` are units, and

```text
x^2 + a2*x + a4 = (x - r)^2 + 16*d*x.
```

The element `r=16*L^2` is a square unit.

Let `P=(x,y)` be a local point with `x != 0`.

If `x-r` is a unit, then the quadratic factor `x^2 + a2*x + a4` is congruent
to `(x-r)^2` modulo the maximal ideal. Since `ell` is odd, it is a square in
`K*`. From

```text
y^2 = x * (x^2 + a2*x + a4),
```

the class of `x` is trivial.

If `x-r` is not a unit, then `x` has the same residue as the square unit
`r`, so `x` itself is a square in `K*`.

Thus every non-kernel local point has trivial tracked squareclass. This
proves the `ell | T^2 + 4*L^2` formal-lift subclaim for
`rank-zero-selmer-AA-kernel-neg-2sqrt-q`.

### Odd-prime summary

The odd-prime formal-lift input for this package is now:

```text
ell | L                 full image
ell | T                 local image contained in {1, -1}
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
