# M2 Pure v_ell Split-Prime Global Class Character

## Question

What odd-place condition does the global standard equation

```text
Z=r*(a+i*b)^2
```

impose at a prime dividing `ell-1` but not the common-coordinate gcd?

## Unit Place Setup

Let `p` be an odd prime with

```text
p|ell-1,
p not divide R.
```

Then `p` does not divide the canonical class `r`. Modulo `p`, the standard
element from `wl555` satisfies

```text
E=0,
F=R != 0,
Z/r=F/r in F_p^*.
```

The global square equation says that this rational unit is a square in the
quadratic etale algebra `F_p[i]`.

## Split Versus Inert

If `p ≡ 3 (mod 4)`, the algebra is `F_(p^2)`. Every element of `F_p^*` is a
square in `F_(p^2)^*`, so this place adds no condition.

If `p ≡ 1 (mod 4)`, the algebra is split. A diagonal rational unit is a square
in `F_p x F_p` exactly when it is a square in `F_p`. Therefore every rational
candidate must satisfy the genuinely global character condition

```text
Legendre(F/r,p)=1.
```

The class `r` contains information from the other common primes, so this is a
distinct-place coupling rather than another standalone residue table.

## Explicit q-Coordinate Form

If `p` does not divide `QD`, put

```text
t=Q^2/D^2 (mod p),
f(t)=t^2+4*t-4.
```

Since `D^4` is a square,

```text
Legendre(f(t)/r,p)=1.
```

If `p|Q` or `p|D`, primitivity gives respectively

```text
F ≡ -4*D^4,
F ≡ Q^4.
```

For split `p`, both `-4` and a fourth power are squares, so either boundary
case requires

```text
Legendre(r,p)=1.
```

## Nontriviality

The condition is not automatic from the first two source squares. For
example, modulo `13`,

```text
t=10,
t, 1-t, t+4 are squares,
f(t)=6 is a nonsquare.
```

Thus this residue is allowed by the source-square reductions but is compatible
with the global class equation only when `r` is also a nonsquare modulo `13`.

## Next Exact Gate

For every split unit prime dividing `ell-1`, the canonical class must match the
quadratic character of `F`. The next gate must combine these character
conditions across the prime divisors of `ell-1`, and separately handle primes
where `p|R` with even common valuation. This is the first strict odd
distinct-place condition after `wl557`.

## Boundary

This does not solve the global character system, handle even positive common
valuations, solve either surviving orientation, handle the nontrivial
real-unit class, prove `wl535`, or enter M3.
