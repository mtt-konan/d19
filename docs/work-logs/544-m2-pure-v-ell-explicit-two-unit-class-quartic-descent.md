# M2 Pure v_ell Explicit Two-Unit-Class Quartic Descent

## Question

Can the abstract element equation from `wl543` be converted into a finite,
explicit system that still remembers the Gaussian square, the `G_ell` square,
and real positivity?

## Unit-Class Coordinates

Choose one representative of each totally positive unit squareclass:

```text
epsilon = (r+s*sqrt(ell))/2,
r^2-ell*s^2=4,
r>|s|*sqrt(ell).
```

There is one such class when a norm-`-1` unit exists and at most two otherwise.
Write

```text
beta=(u+v*sqrt(ell))/2,
u ≡ v (mod 2).
```

Define the integral quadratic forms

```text
N = u^2-ell*v^2,
F = s*(u^2+ell*v^2)+2*r*u*v,
H = r*(u^2+ell*v^2)+2*ell*s*u*v.
```

Expanding `alpha=epsilon*beta^2` gives

```text
alpha=(H+F*sqrt(ell))/8.
```

Comparing with `alpha=(C+Q*sqrt(ell))/2` yields `H=4C`, `F=4Q`, and

```text
N=4*sigma*D, sigma in {+1,-1}.
```

The unit norm identity gives the automatic conic identity

```text
H^2-ell*F^2=4*N^2.
```

## Explicit Quartic System

Put

```text
J_ell(F,N)
  = F^8 +(16-8ell)F^6*N^2
    +(32ell^2-96ell+72)F^4*N^4
    +(32ell-64)F^2*N^6 +16N^8.
```

Every rational `wl535` candidate gives a choice of at most two unit classes
and integers `u,v,Z,W` satisfying

```text
u ≡ v (mod 2),
N != 0,
Z^2 = ell*N^2-F^2,
W^2 = J_ell(F,N),
ell*F^4+4*F^2*N^2-4*ell*N^4 > 0.
```

Conversely, any such solution for a totally positive norm-one unit
representative reconstructs

```text
q = F/N,
a = Z/N,
c = H/N,
V = W/N^4.
```

The automatic identity for `H` proves `c^2=ell*q^2+4`; the `Z` equation proves
`a^2=ell-q^2`; the `W` equation proves `V^2=G_ell(q^2)`; and the displayed
strict inequality is exactly the original positivity predicate after
multiplication by `N^4>0`.

Thus this is an exact reformulation, not merely a necessary condition.

## Trivial Unit Class

When `epsilon=1`, take `r=2,s=0`. Then

```text
F=4*u*v,
H=2*(u^2+ell*v^2),
N=u^2-ell*v^2.
```

The Gaussian equation becomes the explicit quartic

```text
Z^2 = ell*(u^2-ell*v^2)^2-16*u^2*v^2.
```

If the negative Pell equation is soluble, this single branch is the whole
real-quadratic descent. Otherwise the same formulas above give exactly one
additional branch using a fundamental totally positive unit representative.

## Exact Boundary

The `wl535` problem is now a union of at most two explicit integer quartic
systems in `(u,v)`, each carrying one square equation `Z`, one degree-eight
homogeneous square equation `W`, and the exact positivity inequality. The
unbounded denominator-prime support and ordinary ideal class group no longer
appear.

This does not solve either branch, produce a rational point, prove a family
exclusion, establish theorem-level Selmer/rank/`Sha`, or enter M3. The next
gate must attack one of these explicit branches or prove that this descent
does not reduce the remaining arithmetic enough.
