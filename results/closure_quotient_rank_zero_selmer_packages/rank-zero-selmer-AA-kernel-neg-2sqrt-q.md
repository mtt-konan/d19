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

### Remaining Gaps

This does not prove the whole package. The following parts remain open:

- the other odd-prime formal-lift cases for this package
- the `ell=2` local condition
- the global Selmer dimension bound
- the rank-zero conclusion
- any `lambda`-family exclusion

## Boundary

transcript_status = missing

No Selmer rank upper bound is proved by this file. No rank-zero theorem or lambda-family exclusion is claimed here.
