# M2 Pure v_ell Prime-Coupled Source Elliptic And Final Norm Intersection

## Question

After `wl583`, does the source-square genus-one torsor retain a new
independent obstruction once the exact prime parameter equation
`ell=L(X,tau)` is imposed, or does it reduce pointwise to the original two
source squares?

It reduces exactly to a fixed-`ell` source genus-one curve. The final
norm-ratio equation remains an independent quadratic lift whose discriminant
is `G_ell(X)`. Therefore unrestricted torsor or 2-isogeny analysis cannot
resolve the active gate.

## Pointwise Prime Coupling

Keep the `wl570` factors and the `wl583` variables

```text
U^2=a*b/(2*delta),
V^2=c*d/(2*delta).
```

On the parameter locus

```text
ell=L(X,tau),
```

the exact `wl570` factorizations give

```text
U^2=X*(ell-X),
V^2=ell*X+4.
```

In particular,

```text
V^2-U^2=X^2+4.
```

Thus every candidate maps to the fixed-parameter curve

```text
H_ell:
U^2=X*(ell-X),
V^2=ell*X+4.
```

This statement is pointwise: for fixed independent `tau`, the whole
`wl583` torsor is not being identified with `H_ell`. The identification holds
exactly on the incidence locus `ell=L(X,tau)`.

## Source Genus-One Curve

Over the `X`-line, the two squareclasses defining `H_ell` have branch
supports

```text
X*(ell-X): {0,ell},
ell*X+4:   {-4/ell,infinity}.
```

For positive `ell`, these are four distinct points. The connected degree-four
biquadratic cover therefore has

```text
2*g(H_ell)-2=4*(-2)+4*2=0,
g(H_ell)=1.
```

It has the rational boundary points

```text
(X,U,V)=(0,0,+2),
(X,U,V)=(0,0,-2),
```

so its smooth projective completion is an elliptic curve over `Q`. These
points lie outside the exact candidate interval `X>1`; they prove only that
unrestricted global solubility of `H_ell` is automatic.

## Square-X Cover

Adjoining `q^2=X` to `H_ell` reconstructs

```text
p=U/q,
c=V,
q^2+p^2=ell,
c^2=ell*q^2+4.
```

The three squareclasses over `Q(X)` are

```text
X,
X*(ell-X),
ell*X+4.
```

Their parity supports are independent and their union is the same four-point
set

```text
{0,ell,-4/ell,infinity}.
```

The resulting degree-eight cover again has genus one:

```text
2*g-2=8*(-2)+4*4=0.
```

Equivalently, `q^2=X` is an unramified connected degree-two cover of
`H_ell`. It is the exact genus-one curve of the first two `wl535` square
conditions, not the final `wl535` curve.

## Final Norm-Ratio Lift

Put

```text
F=X^2+(8-4*ell)*X-4,
E=4*(ell-1)*X.
```

Clearing `ell=L(X,tau)` gives exactly

```text
E*tau^2-2*F*tau-E=0.
```

Its discriminant is

```text
4*(F^2+E^2)=4*G_ell(X).
```

Hence, away from `E=0`, a rational `tau` exists if and only if
`G_ell(X)` is a rational square. The two roots are

```text
tau=(F+C)/E,
tau=(F-C)/E,
C^2=G_ell(X).
```

`wl569` proves that an exact positive candidate selects only the first root
and imposes the exact interval `rho_ell<tau<1`.

The exceptional denominator `E=0` means `X=0` or `ell=1`. The active scope
has odd prime `ell>=5` and `X>1`, so no candidate branch is lost.

## Exact Equivalence

The active `wl535` proposition is now equivalently the nonexistence of a
rational point on the square-`X` genus-one source cover satisfying
simultaneously

```text
X>sigma_ell,
C^2=G_ell(X),
tau=(F+C)/E lies in (rho_ell,1).
```

The prime condition remains `ell` an odd prime congruent to `1 mod 4`.
Conversely these data reconstruct `p,c,tau` and hence all four exact `wl535`
conditions by `wl570`.

## Route Exhaustion

This proves that the following are not independent progress routes:

```text
unrestricted H_ell(Q) solubility,
unrestricted rank or torsion of H_ell,
unrestricted wl583 torsor solubility after forgetting ell=L(X,tau),
the identity V^2-U^2=X^2+4 by itself.
```

The live arithmetic intersection is specifically:

```text
square-X source genus-one point
AND final norm-ratio discriminant square
AND selected real interval
AND prime ell.
```

## Next Exact Gate

Attack the final norm-ratio square on the square-`X` source genus-one curve,
with the selected root and prime parameter retained. A quotient or rank
calculation that forgets any of these conditions is not a smaller exact gate.

## Boundary

This is a prime-coupling and route-exhaustion certificate. It does not solve
the final intersection, prove `wl535`, classify a rank family, prove family
exclusion or a Selmer upper bound, or enter M3.
