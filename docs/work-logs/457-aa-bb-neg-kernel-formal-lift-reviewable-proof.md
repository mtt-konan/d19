# AA+BB Neg Kernel Formal-Lift Reviewable Proof

## Question

Can the first `AA+BB` package get a reviewable odd-prime
`formal_lift_compatibility` segment without pretending that the whole
rank-zero proof is done?

This note does that for

```text
rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q.
```

## Result

Yes. For the `kernel_neg_2sqrt_q` package, the one-sided formal-lift proofs
give:

```text
AA side, L=A:
  odd valuation can only come from primes dividing A

BB side, L=B:
  odd valuation can only come from primes dividing B
```

Since `A:B` is primitive, no odd prime divides both `A` and `B`. Therefore the
`AA+BB` common-source requirement forces:

```text
kernel_neg_2sqrt_q: no odd-prime valuation support.
```

In ordinary language: this is the first `AA+BB` package-level odd-prime
formal-lift segment. It says the odd-prime part is killed for this kernel. It
does not decide the prime `2`, unit/sign classes, the global Selmer bound,
rank zero, or any lambda-family exclusion.

## Setup

For the one-sided packages, the shared target model is

```text
E_L: y^2 = x^3 + 16*(T^2 + 2*L^2)*x^2 + 256*L^4*x,
T = A+B.
```

The `AA` side uses `L=A`. The `BB` side uses `L=B`. The `AA+BB` package means
that the same common-source object must pass both one-sided formal-lift
constraints.

The relevant one-sided reviewable proofs are:

```text
AA / kernel_neg_2sqrt_q: docs/work-logs/431-aa-neg-kernel-formal-lift-reviewable-proof.md
BB / kernel_neg_2sqrt_q: docs/work-logs/454-bb-neg-kernel-formal-lift-reviewable-proof.md
```

Both proofs have the same odd-prime local image pattern:

```text
ell | L                 full image
ell | T                 contained in {1, -1}
ell | T^2 + 4*L^2       contained in {1}
```

Only the `ell | L` branch can contribute odd valuation. The branches
`{1, -1}` and `{1}` are unit classes, so they have even valuation.

## Theorem

For `rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q`, the odd-prime
formal-lift compatibility segment has no odd-prime valuation support.

## Proof

Let `ell` be an odd prime. Suppose an `AA+BB` common-source class has odd
valuation at `ell` in the `kernel_neg_2sqrt_q` coordinate.

On the `AA` side, the one-sided formal-lift proof says odd valuation is
possible only in the branch

```text
ell | A.
```

Indeed, when `ell | T`, the local class is contained in `{1, -1}`, and when
`ell | T^2 + 4*A^2`, it is contained in `{1}`. Both have even valuation.

On the `BB` side, the same formal-lift proof with `L=B` says odd valuation is
possible only in the branch

```text
ell | B.
```

Again, the `ell | T` and `ell | T^2 + 4*B^2` branches contribute only unit
classes and therefore even valuation.

Thus the same odd valuation could survive the `AA+BB` common-source condition
only if

```text
ell | A
and
ell | B.
```

But `A:B` is primitive, so `gcd(A,B)=1`. No odd prime can divide both.

Therefore no odd prime can contribute odd valuation to the
`kernel_neg_2sqrt_q` coordinate in the `AA+BB` package.

## Conclusion

The odd-prime `formal_lift_compatibility` segment of
`rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q` is now written as a reviewable
package proof:

```text
kernel_neg_2sqrt_q: no odd-prime valuation support.
```

This is stronger than either one-sided package at the odd-valuation level,
because the only one-sided full-image branches are disjoint after imposing
`gcd(A,B)=1`.

## Boundary

This note does not prove the full Selmer package. It does not address:

- the prime `2`,
- unit/sign classes,
- the global Selmer dimension bound,
- the rank-zero conclusion,
- any family-level exclusion theorem.

It also does not promote the package to a complete transcript. It records one
review-ready odd-prime segment only.
