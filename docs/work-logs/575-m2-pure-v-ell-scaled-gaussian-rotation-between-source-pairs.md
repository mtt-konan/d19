# M2 Pure v_ell Scaled Gaussian Rotation Between Source Pairs

## Question

What exact relation compares the two complementary `k`-allocations from
`wl574`?

## Four Coefficient Forms

Put

```text
P =a^4+4*b^4,
K =a^4+4*a^2*b^2-4*b^4,
R1=5*a^4-8*a^2*b^2+4*b^4,
R2=a^4+8*a^2*b^2+20*b^4.
```

Here `K>0` is the same homogeneous positivity form used in `wl573`, while
`R1,R2>0` are the two gcd-support determinants from `wl574`.

## Forward Rotation

Direct elimination of the primitive variables `(m,n)` gives

```text
R1*C=P*A-2*K*B,
R1*D=2*K*A+P*B.
```

Equivalently, in Gaussian notation,

```text
R1*(C+i*D)=(P+2*i*K)*(A+i*B).
```

Thus the second source pair is not an independent allocation of `k`; it is a
scaled rotation of the first pair.

## Inverse Rotation And Norm

The inverse identities are

```text
R2*A=P*C+2*K*D,
R2*B=-2*K*C+P*D.
```

They follow from the exact norm identity

```text
P^2+4*K^2=R1*R2.
```

Taking Gaussian norms also gives

```text
R1*(C^2+D^2)=R2*(A^2+B^2).
```

All four identities are integral and retain every common factor; no division
by a possibly vanishing residue class is hidden.

## Exact Primitive GCDs

For `gcd(a,b)=1`,

```text
gcd(P,K)=1  if a is odd,
gcd(P,K)=4  if a is even.
```

Indeed the resultant of `P,K`, viewed as quadratics in `a^2`, is
`128*b^8`, so no odd common prime is possible. Their visible `2`-adic
valuations are both zero when `a` is odd and both exactly two when `a` is
even (then `b` is odd).

Similarly,

```text
gcd(R1,R2)=1  if a is odd,
gcd(R1,R2)=4  if a is even.
```

The corresponding resultant is

```text
2^11*3^2*b^8.
```

Only the odd prime `3` needs separate checking. If `3|a` or `3|b`, direct
reduction of one of `R1,R2` is nonzero; if `3` divides neither, then
`a^2=b^2=1 mod 3` and `R1=1 mod 3`. Hence `3` cannot divide both. The same
visible parity calculation gives the exact dyadic gcd above.

## Primewise Coupling

At every odd prime `q`, the coefficient pair `(P,2K)` is primitive. Also an
odd `q` cannot divide both `R1` and `R2`. Therefore:

- if `q` divides neither `R1` nor `R2`, the rotation is invertible modulo
  `q` and directly transports the `A,B` allocation to `C,D`;
- if `q|R1`, then `q` does not divide `R2`, and the forward equations reduce
  to the single rank-one relation forced by
  `P^2+4*K^2=0 mod q`;
- the case `q|R2` is the exact inverse analogue.

This is a complete structural comparison, but it does not force the two
complementary allocations to agree or disagree uniformly.

## Next Exact Gate

For odd `q|k=sqf(2*Delta)`, classify the transported side choice under this
rotation in the three exact cases `q` divides neither determinant, `q|R1`, or
`q|R2`. A new allocation table detached from the rotation is forbidden.

## Boundary

This proves the comparison map and its primitive support, not a contradiction.
It does not solve the generic cover, prove `wl535`, identify theorem-level
Selmer, or enter M3.
