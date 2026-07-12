# M2 Pure v_ell Source-Square Multiquadratic Cover Genus

## Question

What exact curve is defined by the simultaneous factored square predicates in
`wl570`, and does it have an exceptional lower-genus branch?

## Positive Linear Factors

Keep `X,tau` in the exact `wl570` open rectangle and put

```text
delta=tau^2+2*tau-1,
a=X*(tau+2)-2,
b=2*tau-X*(2*tau-1),
c=X+2*tau+4,
d=tau*(X+4)-2.
```

Then `delta>0`, `X>1`, and the two source squares are

```text
p^2=a*b/(2*X*delta),
s^2=c*d/(2*delta).
```

The `wl570` sign analysis gives `a,b,c,d>0` on every candidate.

## Product Elliptic Curve

Since `X=q^2`, simultaneous source squares imply

```text
Y^2=a*b*c*d,
Y=2*q*delta*p*s.
```

Homogenize the four factors as linear forms in `[X:Z]`. Their six pairwise
determinants, up to the displayed signs, are

```text
det(a,b)= 2*(tau^2+1),
det(a,c)= 2*(tau^2+4*tau+5),
det(a,d)= 4*delta,
det(b,c)=-4*delta,
det(b,d)=-2*(5*tau^2-4*tau+1),
det(c,d)=-2*(tau^2+1).
```

For `tau>sqrt(2)-1`, every factor on the right is nonzero; in particular

```text
5*tau^2-4*tau+1=5*(tau-2/5)^2+1/5>0.
```

Thus the four projective branch points are distinct. This includes
`tau=1/2`: there `b=Z` is the point at infinity and `d=X/2` is the point
zero, still distinct from the roots of `a` and `c`.

Therefore the smooth projective completion of

```text
Y^2=a*b*c*d
```

is genus one for every admissible rational `tau`. Each branch point is
rational, so the curve has rational points and is an elliptic curve with full
rational `2`-torsion. This is an auxiliary curve family, not a Selmer group.

## Exact Full Cover

Over `Q(X)`, the complete `wl570` source-square conditions adjoin square roots
of the three squareclasses

```text
u_1=X,
u_2=a*b/(2*X*delta),
u_3=c*d/(2*delta).
```

The product curve records `u_1*u_2*u_3` square. Conversely, on the locus
`X=q^2`, the product curve together with `u_2` square forces `u_3` square,
because

```text
u_2*u_3=Y^2/(4*X*delta^2).
```

All factors are nonzero in the open rectangle, so this converse loses no
branch.

For `tau!=1/2`, the parity supports of `u_1,u_2,u_3` lie over

```text
{0,infinity},
{a,b,0,infinity},
{c,d},
```

respectively. The determinant calculation makes these six points distinct,
and the three squareclasses are independent. The resulting degree-eight
multiquadratic cover has six inertia-two branch points. Riemann-Hurwitz gives

```text
2*g-2=8*(-2)+6*4=8,
g=5.
```

## Exceptional tau=1/2 Branch

At `tau=1/2`, the parity supports become

```text
u_1: {0,infinity},
u_2: {a,0},
u_3: {c,0}.
```

They remain independent, but the union has only four branch points. Hence

```text
2*g-2=8*(-2)+4*4=0,
g=1.
```

The `wl570` formulas simplify exactly to

```text
ell=X+5-4/X,
p^2=5-4/X,
s^2=X*(X+5).
```

Since `X=q^2`, the last square is equivalent to `X+5` being a rational
square. Thus `tau=1/2` is a genuine exceptional elliptic subproblem, while
every other admissible `tau` lies on the genus-five cover.

## Next Exact Gate

The next gate may attack only the exceptional branch

```text
q^2=X,
p^2=5-4/X,
r^2=X+5,
ell=X+5-4/X prime congruent 1 mod 4,
```

or prove a uniform obstruction on the generic genus-five cover. Finite point
counts or broad rank diagnostics are not accepted.

## Boundary

This classifies the exact auxiliary curve and its unique genus drop. It does
not determine rational points on either cover, prove the exceptional branch
empty, prove `wl535`, identify theorem-level Selmer, or enter M3.
