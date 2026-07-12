# M2 Pure v_ell All Odd k-Primes Transport Same-Side

## Question

Do the singular determinant cases isolated in `wl576` actually occur after
the global divisibility `Delta|K` from `wl573` is imposed?

## Every Odd k-Prime Divides K

Keep

```text
k=sqf(2*Delta),
K=a^4+4*a^2*b^2-4*b^4.
```

If an odd prime `p` divides `k`, then `v_p(Delta)` is odd and in particular

```text
p divides Delta.
```

But `wl573` proves the integer divisibility

```text
Delta divides K.
```

Therefore every odd `p|k` satisfies

```text
p|K.
```

## Determinants Are Automatically Regular

`wl575` proves that `gcd(P,K)` has no odd prime factor. Hence

```text
p does not divide P.
```

Reducing the norm identity

```text
P^2+4*K^2=R1*R2
```

modulo `p` gives

```text
R1*R2=P^2 != 0 mod p.
```

Thus

```text
p does not divide R1*R2.
```

The singular cases `p|R1` and `p|R2` from `wl576` are structurally possible
for the rotation alone but impossible on an actual candidate satisfying the
global parameter equation.

## Uniform Same-Side Transport

Every odd `p|k` is therefore in the regular `p|K` case of `wl576`. Its side
transport is uniformly

```text
A-side -> C-side,
B-side -> D-side.
```

Equivalently, in the complementary splits of `wl574`,

```text
p|alpha iff p|gamma,
p|beta  iff p|delta_0.
```

Hence the odd parts of the two allocations agree exactly:

```text
odd(alpha)=odd(gamma),
odd(beta)=odd(delta_0).
```

No odd crossed allocation and no odd higher-valuation ambiguity survives.

## The Remaining Factor 2

Primitive `m,n` give

```text
v_2(Delta)=0  if m,n have opposite parity,
v_2(Delta)=1  if m,n are both odd.
```

Since `k` is the squarefree kernel of `2*Delta`,

```text
2|k  iff m,n have opposite parity.
```

Thus the two complementary allocations can differ, if at all, only in the
side assigned to `2`. When `m,n` are both odd, `k` is odd and the two
allocations are already identical.

## Next Exact Gate

Determine the side of `2` in both source-factor pairs when `m,n` have opposite
parity. This is not a return to standalone dyadic analysis: it is the sole
remaining comparison after every odd prime has been transported globally.

## Boundary

This removes all odd singular/crossed cases and proves odd allocation equality.
It does not compare the dyadic side, solve the generic cover, prove `wl535`,
identify theorem-level Selmer, or enter M3.
