# M2 Pure v_ell Q(i) Elliptic Rational-Locus Descent Equivalence

## Question

Does the `wl581` elliptic quotient over `Q(i)` impose an independent
quadratic-lift obstruction on the rational locus, or does its equation already
reconstruct the genus-two rational point?

The second alternative holds. Away from the visible branch points, the
`S in Q` locus on the elliptic quotient is exactly equivalent to the rational
locus of the genus-two character quotient. Thus an unrestricted elliptic
rank or point calculation cannot shrink the current proof gap.

## Input

Keep the `wl581` notation and put

```text
L_1=(tau+2)*S+2*tau^2+8*tau+6,
L_2=(2*tau^2-tau)*S+6*tau^2-8*tau+2,
L=L_1*L_2.
```

The elliptic quotient over `K=Q(i)` is

```text
E_tau: Y^2=(-S+4*i)*L.
```

The genus-two character quotient over `Q` is

```text
C_tau: Z^2=X*a*b*c*d.
```

Throughout the exact candidate interval, `tau` is rational,
`sqrt(2)-1<tau<1`, and `tau!=1/2`.

## Split The Elliptic Equation

Let an affine point of `E_tau(K)` have

```text
S in Q,
Y=A+i*B,
A,B in Q.
```

Comparing real and imaginary parts gives exactly

```text
A^2-B^2=-S*L,
2*A*B=4*L.
```

If `Y!=0` and the point is not two-torsion, then `L!=0`, so `A*B!=0`.
Eliminating `L` gives

```text
S*A*B=2*(B^2-A^2).
```

Define

```text
X=-2*A/B,
Z=A*X.
```

Then

```text
X-4/X=S,
Y=Z*(X-2*i)/X^2.
```

In particular,

```text
S^2+16=(X+4/X)^2
```

is automatically a rational square. It is not an additional obstruction on
this locus.

Using the exact `wl581` quotient identity

```text
(-S+4*i)*L
 =a*b*c*d*(X-2*i)^2/X^3
```

and cancelling the nonzero factor `(X-2*i)^2` gives

```text
Z^2=X*a*b*c*d.
```

Thus `(X,Z)` is a rational point on `C_tau`.

## Exact Inverse

Conversely, let `(X,Z)` be a rational nonbranch point on `C_tau`, so
`X*Z*a*b*c*d!=0`. Define

```text
S=X-4/X,
Y=Z*(X-2*i)/X^2.
```

Then `wl581` proves `(S,Y)` lies on `E_tau(K)`. Writing `Y=A+iB` gives

```text
A=Z/X,
B=-2*Z/X^2,
```

and the reconstruction above returns

```text
-2*A/B=X,
A*X=Z.
```

Therefore the two maps are mutually inverse between

```text
C_tau(Q) nonbranch affine points
```

and

```text
{(S,Y) in E_tau(Q(i)):
   S in Q,
   Y!=0,
   L_1*L_2!=0}.
```

There is no hidden second rational lift. The other root of
`X^2-S*X-4=0` is `-4/X`; under the `wl581` involution its `Z` coordinate is
multiplied by `i`, so it is not the second rational point on the nonbranch
locus.

## Branch Audit

The two rational roots `L_1=0` and `L_2=0` are precisely the images of the
rational branch-point pairs

```text
{root(a),root(c)},
{root(b),root(d)}.
```

In each pair the two `X` values have product `-4` and sum equal to the
corresponding `S` root. The third two-torsion root is `S=4*i`, which is not in
the `S in Q` locus. Candidate points have all four factors positive and hence
never meet these branches.

## Exact Consequence

The `wl581` elliptic quotient is a valid geometric quotient, but its
field-of-definition restriction restores exactly the genus-two rational
locus. Therefore none of the following can be counted as a smaller proof gate:

```text
S^2+16 square by itself,
unrestricted E_tau(Q(i)) point existence,
unrestricted E_tau(Q(i)) rank or torsion,
the visible two-torsion points.
```

For an exact candidate, the reconstructed coordinate is

```text
X=-2*Re(Y)/Im(Y),
```

and the still-independent conditions are that this `X` is a positive rational
square in the exact interval, both source factors are individually rational
squares, and `ell=L(X,tau)` is the required odd prime.

## Next Exact Gate

Attack a condition not absorbed by the rational-locus equivalence: the
square-`X` pullback, one individual source-square lift over the genus-two
character quotient, or the prime-parameter condition. Do not compute
unrestricted elliptic ranks or present the automatic quadratic lift as a new
obstruction.

## Boundary

This is an exact descent-equivalence and route-exhaustion certificate for the
`wl581` elliptic quotient. It does not classify the remaining restricted
points, solve `wl535`, prove family exclusion or a Selmer upper bound, or
enter M3.
