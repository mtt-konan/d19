# M2 Pure v_ell Odd-Prime Side Transport Under Rotation

## Question

For an odd prime in the canonical class `k=sqf(2*Delta)`, how does the
`wl575` rotation transport its side between the two source-factor pairs?

## Parameter-Prime Units

Let `p` be an odd prime with `p|k`. Then `v_p(Delta)` is odd, so `p|Delta`.
By `wl573`,

```text
gcd(Delta,m*n)=1,
a^2|4*m*n,
b^2|m*n.
```

Consequently

```text
p does not divide a*b*m*n.
```

Indeed `p` cannot divide `m*n`; if it divided `a` or `b`, either support
divisibility would force it back into `m*n`.

Thus `t=m/n mod p` is defined and satisfies

```text
t^2+2*t-1=0 mod p.
```

Its discriminant is `8`, so

```text
Legendre(2,p)=1,
p congruent 1 or 7 mod 8.
```

This is a uniform necessary condition on every odd prime in `k`.

## Regular Determinant Case

Assume

```text
p does not divide R1*R2.
```

Since `A*B=k*U^2`, exactly one of `A,B` vanishes modulo `p`: at least one does,
and both cannot because `gcd(A,B)|R1`. Likewise exactly one of `C,D` vanishes.

The rotation is invertible modulo `p`. If `p|A`, then `B` is a unit and

```text
R1*C=-2*K*B,
R1*D= P*B.
```

Therefore exactly one of `P,K` vanishes:

```text
p|K => p|C,
p|P => p|D.
```

If `p|B`, the other two equations give

```text
p|K => p|D,
p|P => p|C.
```

Because `gcd(P,K)` has no odd factor, the alternatives are exclusive. Thus:

- `p|K` transports the same side, `A->C` and `B->D`;
- `p|P` transports the crossed side, `A->D` and `B->C`.

The fact that one of `P,K` must vanish is not assumed: it follows because one
of `C,D` must vanish while the displayed coefficients and `R1*B` or `R1*A`
are units.

## Singular R1 Case

Assume `p|R1`. By `wl575`, `p` does not divide `R2`, `P`, or `K`. Since
`p|A*B`, at least one of `A,B` vanishes. Reducing the forward rotation shows
that either one forces the other:

```text
p|A and p|B.
```

On the other hand, exactly one of `C,D` vanishes because
`gcd(C,D)|R2` and `p|C*D`.

The normalized first-pair allocation is therefore not visible modulo `p`.
Writing `e_A=v_p(A)`, `e_B=v_p(B)`, their sum is odd, so after removing the
common valuation `min(e_A,e_B)`, the side carrying `p` is exactly the side
with larger valuation. Determining it requires higher `p`-adic data.

## Singular R2 Case

If `p|R2`, the inverse rotation gives the exact analogue:

```text
p|C and p|D,
```

while exactly one of `A,B` vanishes modulo `p`. The normalized second-pair
side is the coordinate with larger valuation and is again invisible at the
residue level.

## Exact Failure Point

All regular odd primes in `k` now have deterministic side transport governed
by `p|P` versus `p|K`. The only unresolved odd-prime allocations are singular
determinant primes:

```text
p|gcd(k,R1) or p|gcd(k,R2).
```

Since `gcd(R1,R2)` has no odd factor, these two sets are disjoint. The next
gate must compute the first nonzero normalized rotation at such a prime; no
new residue-only allocation table can resolve it.

## Boundary

This proves regular side transport and isolates the exact higher-valuation
failure point. It does not resolve singular sides, solve the generic cover,
prove `wl535`, identify theorem-level Selmer, or enter M3.
