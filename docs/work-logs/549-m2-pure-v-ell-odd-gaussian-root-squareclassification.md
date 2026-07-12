# M2 Pure v_ell Odd Gaussian Root-Square Classification

## Question

Which odd rational primes in the refined `wl548` support can actually satisfy
the candidate-dependent `wl547` root condition, once one uses the already
forced fact that `t=Q^2/D^2` is a nonzero square modulo the prime?

## Exact Local Identities

Let `p` be an odd divisor of `ell-1`, with `p` not dividing `QD`, and put

```text
t=Q^2/D^2 (mod p).
```

If a Gaussian prime over `p` divides both `delta` and its conjugate, `wl547`
gives

```text
f(t)=t^2+4t-4=0.
```

This identity implies

```text
1-t=t^2/4,
t+4=4/t.
```

The root is nonzero. Therefore, once `t` is a square, both `1-t` and `t+4`
are automatically squares. At such a common divisor, the reductions of the
first two `wl535` square equations add no condition beyond the requirement
that the root `t` itself be a square.

## Root-Square Classification

The discriminant of `f` is `32`, so roots exist exactly when `(2/p)=1`, or

```text
p ≡ 1 or 7 (mod 8).
```

For its two roots `t_1,t_2`, Vieta gives

```text
t_1*t_2=-4.
```

Hence:

- if `p ≡ 7 (mod 8)`, `-1` is a nonsquare, so exactly one of the two roots is
  a square;
- if `p ≡ 1 (mod 8)`, `-1` is a square, so either both roots are squares or
  neither is.

Thus the safe odd support can be sharpened to

```text
S_ell^root = {
  Gaussian primes over odd p :
  p|ell-1 and f(t)=0 has a nonzero square root t modulo p
}.
```

Every divisor `p ≡ 7 (mod 8)` of `ell-1` survives this root-square test.
For `p ≡ 1 (mod 8)`, membership is the explicit zero-or-two-root condition.

## Exact Failure Point

The `wl547` root condition cannot uniformly eliminate all remaining odd
squareclasses: every `p ≡ 7 (mod 8)` has exactly one square root of `f`, and
that root automatically satisfies the two reduced source-square conditions.
Further progress must use the valuation/class equation together with a fixed
`wl546` orientation or the real positivity inequality; repeating residue
square tests at the common prime is exhausted.

## Boundary

This is a classification of possible common-prime support, not a proof that a
listed Gaussian prime occurs in a global candidate. It does not solve a
Gaussian class equation, use positivity, handle the nontrivial real-unit
class, prove the full `wl535` proposition, or enter M3.
