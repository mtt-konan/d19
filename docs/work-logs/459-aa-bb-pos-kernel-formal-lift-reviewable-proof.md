# AA+BB Pos Kernel Formal-Lift Reviewable Proof

## Question

Can the remaining `AA+BB` package get a reviewable odd-prime
`formal_lift_compatibility` segment without claiming a full Selmer bound?

This note does that for

```text
rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q.
```

## Result

Yes. For the `kernel_pos_2sqrt_q` package, the one-sided formal-lift proofs
give the same odd-valuation source on both sides:

```text
AA side, L=A:
  odd valuation can only come from primes ell | T where -1 is a square

BB side, L=B:
  odd valuation can only come from primes ell | T where -1 is a square
```

where `T=A+B`. Over `Q_ell`, the condition that `-1` is a square is exactly
`ell == 1 mod 4`. Therefore the `AA+BB` common-source requirement forces:

```text
kernel_pos_2sqrt_q: odd-prime valuation support only from ell | T, ell == 1 mod 4.
```

In ordinary language: unlike the other two `AA+BB` kernels, this one is not
killed at every odd prime. The only remaining odd-prime tail is the already
known `T` tail at primes `1 mod 4`. This still does not decide the prime `2`,
unit/sign classes, the global Selmer bound, rank zero, or any lambda-family
exclusion.

## Setup

For the one-sided packages, the shared target model is

```text
E_L: y^2 = x^3 - 8*(T^2 + 8*L^2)*x^2 + 16*T^4*x,
T = A+B.
```

The `AA` side uses `L=A`. The `BB` side uses `L=B`. The relevant one-sided
reviewable proofs are:

```text
AA / kernel_pos_2sqrt_q: docs/work-logs/449-aa-pos-kernel-formal-lift-reviewable-proof.md
BB / kernel_pos_2sqrt_q: docs/work-logs/455-bb-pos-kernel-formal-lift-reviewable-proof.md
```

Both proofs have the same odd-prime local image pattern:

```text
ell | L                 contained in {1}
ell | T                 unit classes if -1 nonsquare; full image if -1 square
ell | T^2 + 4*L^2       contained in {1}
```

Only the `ell | T` branch can contribute odd valuation, and even there it can
contribute odd valuation only when `-1` is a square locally.

## Lemma

Let `ell` be an odd prime and let `T=A+B` with `gcd(A,B)=1`.

If an odd valuation can occur in either one-sided `kernel_pos_2sqrt_q`
formal-lift condition, then

```text
ell | T
and
-1 is a square in Q_ell.
```

Equivalently, over the rational local field,

```text
ell | T
and
ell == 1 mod 4.
```

## Proof Of Lemma

The one-sided formal-lift proof for `L=A` says:

```text
ell | A                 local image is contained in {1}
ell | T                 unit classes if -1 nonsquare; full image if -1 square
ell | T^2 + 4*A^2       local image is contained in {1}
```

The classes in `{1}` have even valuation. The `ell | T` branch has only unit
classes when `-1` is nonsquare, so it also has no odd valuation in that case.
Thus an odd valuation on the `AA` side can occur only if `ell | T` and `-1`
is a square in `Q_ell`.

The same argument with `L=B` applies to the `BB` side:

```text
ell | B                 local image is contained in {1}
ell | T                 unit classes if -1 nonsquare; full image if -1 square
ell | T^2 + 4*B^2       local image is contained in {1}
```

Again, the only possible odd-valuation branch is `ell | T` with `-1` square.

For odd rational primes, the standard criterion gives

```text
-1 is a square in Q_ell  if and only if  ell == 1 mod 4.
```

This proves the lemma.

## Theorem

For `rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q`, the odd-prime
`formal_lift_compatibility` segment has odd-prime valuation support only at
primes

```text
ell | T
ell == 1 mod 4.
```

## Proof

Let `ell` be an odd prime. Suppose an `AA+BB` common-source class has odd
valuation at `ell` in the `kernel_pos_2sqrt_q` coordinate.

Because it is an `AA+BB` common-source class, the same coordinate must satisfy
both one-sided formal-lift constraints: the `AA` constraint with `L=A`, and
the `BB` constraint with `L=B`.

By the lemma, the `AA` constraint allows odd valuation only when

```text
ell | T
and
ell == 1 mod 4.
```

The `BB` constraint gives the same necessary condition. Therefore any
odd-prime valuation support surviving the `AA+BB` common-source condition is
contained in the set of primes `ell | T` with `ell == 1 mod 4`.

This is exactly the claimed support bound.

## Conclusion

The odd-prime `formal_lift_compatibility` segment of
`rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q` is now written as a reviewable
package proof:

```text
kernel_pos_2sqrt_q: odd-prime valuation support only from ell | T, ell == 1 mod 4.
```

Together with `wl457` and `wl458`, this completes the narrow odd-prime
formal-lift coverage for the three `AA+BB` kernels:

```text
kernel_neg_2sqrt_q    no odd-prime valuation support
kernel_minus_p        no odd-prime valuation support
kernel_pos_2sqrt_q    support only from ell | T, ell == 1 mod 4
```

## Boundary

This note does not prove the full Selmer package. It does not address:

- the prime `2`,
- unit/sign classes,
- the global Selmer dimension bound,
- the rank-zero conclusion,
- any family-level exclusion theorem.

It also does not promote the package to a complete transcript. It records one
review-ready odd-prime segment only.
