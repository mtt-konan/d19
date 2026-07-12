# M2 Pure v_ell Even Common-Valuation Leading Character

## Question

What replaces the `wl558` unit-place character when an odd prime dividing
`ell-1` also divides `R`, but its common valuation is positive and even, so it
does not occur in the canonical squarefree class `r`?

## Normalize The Even Common Power

Let

```text
e=v_p(ell-1),
k=v_p(R),
d=min(e,k)=2*h>0.
```

At a common prime, `p` does not divide `QD`, so `v_p(E)=e`. Since `d` is even,
`p` does not divide `r`. The equation

```text
Z=F+i*E=r*Gamma^2
```

shows that `p^h` divides `Gamma`. Divide by `p^(2h)` and put

```text
E_d=E/p^d,
R_d=R/p^d,
F_d=F/p^d=R_d-E_d.
```

Then

```text
Z_d=F_d+i*E_d
```

is a unit square times `r` in `F_p[i]`.

## Inert Primes

If `p ≡ 3 (mod 4)`, `F_p[i]=F_(p^2)`. An element of this field is a square
exactly when its norm is a square in `F_p`. Here

```text
Norm(Z_d/r)=(W/(p^d*r))^2,
```

so the condition is automatic. Thus even common valuations at inert primes
add no new obstruction.

## Split Primes

Let `p ≡ 1 (mod 4)` and choose `j in F_p` with `j^2=-1`. The two components
of `Z_d/r` have product equal to the square norm above, so it is enough to
require either component to be a square:

```text
Legendre((F_d+j*E_d)/r,p)=1.
```

This has three explicit valuation cases.

### Case e < k

Here `R_d=0 (mod p)` and

```text
Z_d/r = (E_d/r)*(-1+i).
```

Writing `L_e=(ell-1)/p^e`, the square factors in
`E_d=4*L_e*Q^2*D^2` disappear from the character. Hence

```text
Legendre(L_e*(-1+j)/r,p)=1.
```

### Case k < e

Here `E_d=0 (mod p)` and `F_d=R_d`, so

```text
Legendre((R/p^k)/r,p)=1.
```

### Case e = k

Both leading terms are units. With

```text
L_e=(ell-1)/p^e,
lambda=(R/p^e)/(4*L_e*Q^2*D^2) (mod p),
```

the condition is

```text
Legendre(L_e*(lambda-1+j)/r,p)=1.
```

Again the omitted factor `4Q^2D^2` is a square.

## Exact Completion Of The Place Classification

Together, `wl558` and `wl559` cover every odd `p|ell-1` not occurring in
`r`: valuation zero and positive even common valuation. Odd common valuation
is exactly the case `p|r`; `wl549`-`wl554` determine its support membership,
but its normalized leading character still has to be extracted.

The next task is to add that odd-common leading character and then assemble
the simultaneous split-prime equations, whose right-hand class couples the
different prime divisors of `ell-1`.

## Boundary

This does not solve the character system, prove that any valuation case occurs
globally, solve a surviving orientation, handle the nontrivial real-unit
class, prove `wl535`, or enter M3.
