# M2 Pure v_ell Common-Allocation Mobius Magnitude Curve

## Question

After `wl578` removes every allocation choice, what exact curve remains for
the square magnitudes under the scaled rotation?

## Ratio Coordinates

Keep the identical complementary split

```text
alpha*beta=k
```

and put

```text
lambda=beta/alpha>0,
z=B/A=lambda*u^2,
u=s1/r1>0,

w=D/C=lambda*v^2,
v=s2/r2>0.
```

The first rotation coordinate gives

```text
C/A=(P-2*K*z)/R1.
```

Since `A,C,R1>0`, every candidate has the strict denominator condition

```text
0<z<P/(2*K).
```

Dividing the second rotation coordinate by the first gives the exact Mobius
map

```text
w=(2*K+P*z)/(P-2*K*z).
```

## Biquadratic Magnitude Curve

Substituting the common squareclasses `z=lambda*u^2` and
`w=lambda*v^2` gives

```text
lambda*v^2*(P-2*K*lambda*u^2)
 =2*K+P*lambda*u^2.
```

Equivalently,

```text
v^2=(2*K+P*lambda*u^2)
    /(lambda*(P-2*K*lambda*u^2)),
```

with the exact positive interval

```text
0<u^2<P/(2*K*lambda).
```

## Strict Magnitude Ordering

For every positive `z` in the allowed interval,

```text
w-z=2*K*(1+z^2)/(P-2*K*z)>0.
```

Since `z=lambda*u^2`, `w=lambda*v^2`, and all quantities are positive,

```text
v>u.
```

Thus the second source pair has a strictly larger normalized square ratio.

## Smooth Genus-One Curve

As a double cover of the `u`-line, the right side has zeros at

```text
u^2=-2*K/(P*lambda)
```

and poles at

```text
u^2=P/(2*K*lambda).
```

Because `P,K,lambda>0`, these give four distinct branch points over the
algebraic closure. A zero could coincide with a pole only if

```text
P^2+4*K^2=0,
```

which is impossible over `Q` and also contradicted by
`P^2+4*K^2=R1*R2>0`. Therefore the smooth projective completion has genus one
for every admissible coefficient triple. It need not have a rational point
without the candidate; call it a genus-one torsor, not automatically an
elliptic curve.

## Forward And Projective Converse

Every exact candidate gives a positive rational point `(u,v)` on the displayed
curve.

Conversely, a positive rational point in the strict interval reconstructs the
projective magnitude ratios

```text
z=lambda*u^2,
w=lambda*v^2,
mu=C/A=(P-2*K*z)/R1>0.
```

Choosing positive rational `A`, then `B=z*A`, `C=mu*A`, and `D=w*C`,
reconstructs the two rotation equations. Clearing denominators, and separately
scaling the square representatives, gives positive integer magnitudes of the
abstract common-allocation system.

This converse does not reconstruct the original primitive linear forms
`A,B,C,D` from a common `(m,n)`, nor their exact gcd normalizations. Those
arithmetic constraints remain additional.

## Next Exact Gate

The allocation route has reduced the magnitude question to this explicit
genus-one torsor plus the original linear-form/gcd constraints. The next gate
must use those arithmetic constraints to restrict rational points on the
torsor. Computing unrelated ranks or reintroducing allocation variables is
forbidden.

## Boundary

This proves a smooth genus-one magnitude reduction and strict ordering, not
solubility or insolubility. It does not solve the generic cover, prove
`wl535`, identify theorem-level Selmer, or enter M3.
