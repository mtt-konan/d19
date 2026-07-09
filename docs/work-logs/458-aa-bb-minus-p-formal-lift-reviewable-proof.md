# AA+BB Minus-P Formal-Lift Reviewable Proof

## Question

Can the `AA+BB / kernel_minus_p` package get a reviewable odd-prime
`formal_lift_compatibility` segment?

This note does that for

```text
rank-zero-selmer-AA-BB-kernel-minus-p.
```

## Result

Yes. For the `kernel_minus_p` package, the one-sided formal-lift proofs give:

```text
AA side, L=A:
  odd valuation can only come from primes dividing D_A = T^2 + 4*A^2

BB side, L=B:
  odd valuation can only come from primes dividing D_B = T^2 + 4*B^2
```

where `T=A+B`. For primitive `A:B`, no odd prime divides both `D_A` and `D_B`.
Therefore the `AA+BB` common-source requirement forces:

```text
kernel_minus_p: no odd-prime valuation support.
```

In ordinary language: this kills the odd-prime support for the second `AA+BB`
kernel. It still does not decide the prime `2`, unit/sign classes, the global
Selmer bound, rank zero, or any lambda-family exclusion.

## Setup

For the one-sided packages, the shared target model is

```text
E_L: y^2 = x^3 + (32*L^2 - 8*T^2)*x^2 + 16*(T^2 + 4*L^2)^2*x,
T = A+B.
```

The `AA` side uses `L=A`. The `BB` side uses `L=B`. The relevant one-sided
reviewable proofs are:

```text
AA / kernel_minus_p: docs/work-logs/451-aa-minus-p-formal-lift-reviewable-proof.md
BB / kernel_minus_p: docs/work-logs/456-bb-minus-p-formal-lift-reviewable-proof.md
```

Both proofs have the same odd-prime local image pattern:

```text
ell | L                 contained in {1}
ell | T                 contained in {1, -1}
ell | T^2 + 4*L^2       full image
```

Only the `ell | T^2 + 4*L^2` branch can contribute odd valuation. The
branches `{1}` and `{1, -1}` are unit classes, so they have even valuation.

## Lemma

Let

```text
D_A = T^2 + 4*A^2
D_B = T^2 + 4*B^2
T   = A+B
```

with `gcd(A,B)=1`. Then no odd prime divides both `D_A` and `D_B`.

## Proof Of Lemma

Suppose an odd prime `ell` divides both `D_A` and `D_B`. Then it divides their
difference:

```text
D_A - D_B = 4*(A^2 - B^2) = 4*(A-B)*(A+B) = 4*(A-B)*T.
```

Since `ell` is odd, either

```text
ell | T
```

or

```text
ell | A-B.
```

If `ell | T`, then

```text
D_A = T^2 + 4*A^2 == 4*A^2 mod ell.
```

Because `ell | D_A`, this gives `ell | A`. Together with `ell | T=A+B`, it
also gives `ell | B`, contradicting `gcd(A,B)=1`.

If `ell | A-B`, then `B == A mod ell`, so `T=A+B == 2*A mod ell`. Hence

```text
D_A = T^2 + 4*A^2 == (2*A)^2 + 4*A^2 == 8*A^2 mod ell.
```

Again `ell | D_A`, and `ell` is odd, so `ell | A`. Since `B == A mod ell`,
this gives `ell | B`, again contradicting `gcd(A,B)=1`.

Both cases are impossible. Therefore no odd prime divides both `D_A` and
`D_B`.

## Theorem

For `rank-zero-selmer-AA-BB-kernel-minus-p`, the odd-prime
`formal_lift_compatibility` segment has no odd-prime valuation support.

## Proof

Let `ell` be an odd prime. Suppose an `AA+BB` common-source class has odd
valuation at `ell` in the `kernel_minus_p` coordinate.

On the `AA` side, the one-sided formal-lift proof says odd valuation is
possible only in the branch

```text
ell | D_A = T^2 + 4*A^2.
```

On the `BB` side, the same formal-lift proof with `L=B` says odd valuation is
possible only in the branch

```text
ell | D_B = T^2 + 4*B^2.
```

Thus the same odd valuation could survive the `AA+BB` common-source condition
only if `ell` divides both `D_A` and `D_B`. The lemma says this is impossible
for odd `ell`.

Therefore no odd prime can contribute odd valuation to the `kernel_minus_p`
coordinate in the `AA+BB` package.

## Conclusion

The odd-prime `formal_lift_compatibility` segment of
`rank-zero-selmer-AA-BB-kernel-minus-p` is now written as a reviewable package
proof:

```text
kernel_minus_p: no odd-prime valuation support.
```

Together with `wl457`, this means `AA+BB` now has two kernels whose odd-prime
valuation support is killed at the package level. The remaining odd-prime tail
is the known `kernel_pos_2sqrt_q` branch at primes `ell | T` with
`ell == 1 mod 4`.

## Boundary

This note does not prove the full Selmer package. It does not address:

- the prime `2`,
- unit/sign classes,
- the global Selmer dimension bound,
- the rank-zero conclusion,
- any family-level exclusion theorem.

It also does not promote the package to a complete transcript. It records one
review-ready odd-prime segment only.
