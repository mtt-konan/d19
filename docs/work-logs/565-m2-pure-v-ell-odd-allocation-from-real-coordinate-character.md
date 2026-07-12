# M2 Pure v_ell Odd Allocation From The Real-Coordinate Character

## Question

Can an odd prime factor of `kappa` be assigned to `alpha` or `beta` using the
quartic real-coordinate equation from `wl563`?

## Normalized Real Unit

Keep

```text
F/r=g^2*(alpha^2*M^4-beta^2*N^4),
alpha*beta=kappa,
gcd(alpha*M,beta*N)=1.
```

Let `q` be an odd prime dividing `kappa`. It divides exactly one of
`alpha,beta`, and the bracket

```text
H=alpha^2*M^4-beta^2*N^4
```

is a `q`-adic unit. Hence

```text
v_q(F/r)=2*v_q(g)
```

is even. Define the canonical leading unit

```text
U_q=(F/r)/q^v_q(F/r) (mod q).
```

Removing the square `(g/q^v_q(g))^2` does not change its quadratic character,
so `Legendre(U_q,q)=Legendre(H,q)`.

## Allocation Character

If `q|alpha`, then

```text
H ≡ -(beta*N^2)^2 (mod q),
Legendre(U_q,q)=Legendre(-1,q).
```

If `q|beta`, then

```text
H ≡ (alpha*M^2)^2 (mod q),
Legendre(U_q,q)=1.
```

Thus the exact allocation rule is

```text
Legendre(U_q,q)=Legendre(-1,q)^[q|alpha].
```

## Consequences By Splitting Type

For `q ≡ 3 (mod 4)`, `-1` is a nonsquare, so the allocation is unique:

```text
Legendre(U_q,q)=-1 => q|alpha,
Legendre(U_q,q)=+1 => q|beta.
```

For `q ≡ 1 (mod 4)`, both possible allocations require

```text
Legendre(U_q,q)=+1.
```

A nonsquare `U_q` therefore excludes the entire complementary split, while a
square `U_q` leaves the side of `q` unresolved at quadratic-character level.

## Strict Reduction And Failure Point

Every inert odd factor of `kappa` is assigned canonically by the real
coordinate. Split odd factors satisfy a strict square-unit test but retain a
binary allocation choice. Together with `wl564`, all dyadic and inert factors
are assigned; only split primes `1 mod 4` can remain undecided.

The next gate must use quartic residue information, the selected orientation,
or the scale equation to constrain those split-prime choices, or record the
resulting finite split-prime allocation systems as the exact unresolved
global lemma.

## Boundary

This does not prove that a candidate leading unit has either character, solve
a split-prime allocation, solve the quartic system, handle the nontrivial
real-unit class, prove `wl535`, or enter M3.
