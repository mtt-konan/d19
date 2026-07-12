# M2 Pure v_ell Source-Square Genus-One Torsor And Square-X Fiber Product

## Question

After `wl582` exhausts the `Q(i)` elliptic quotient, can the two individual
source-square conditions be retained on a lower-genus object while keeping the
square-`X` condition visibly independent?

Yes. The two source squares, after absorbing the known square root `q` into
the first one, define a genus-one torsor over `Q`. The complete generic
genus-five cover is exactly its fiber product with `q^2=X`.

## Input

Keep

```text
delta=tau^2+2*tau-1,
a=X*(tau+2)-2,
b=2*tau-X*(2*tau-1),
c=X+2*tau+4,
d=tau*(X+4)-2.
```

An exact `wl570` candidate satisfies

```text
q^2=X,
p^2=a*b/(2*X*delta),
s^2=c*d/(2*delta).
```

On the live generic locus,

```text
sqrt(2)-1<tau<1,
tau!=1/2,
delta>0,
X>1,
a,b,c,d>0.
```

## Source-Square Torsor

Define

```text
T_tau:
U^2=a*b/(2*delta),
V^2=c*d/(2*delta).
```

Every exact candidate maps to `T_tau(Q)` by

```text
U=q*p,
V=s.
```

Conversely, if `(X,U,V)` is a rational point on `T_tau` and `q in Q` has
`q^2=X` with `q!=0`, then

```text
p=U/q,
s=V
```

reconstructs both exact `wl570` source squares.

## Genus And Product Elliptic Curve

Over the `X`-line, the first quadratic extension branches at

```text
root(a), root(b),
```

and the second branches at

```text
root(c), root(d).
```

For admissible `tau!=1/2`, `wl571` proves these four points are distinct.
The two squareclasses are independent, so `T_tau` is a connected degree-four
`(Z/2)^2` cover. Each branch point has two points above it with ramification
index two. Riemann-Hurwitz gives

```text
2*g(T_tau)-2=4*(-2)+4*2=0,
g(T_tau)=1.
```

Multiplication gives the map

```text
T_tau -> E_tau^prod,
(X,U,V) -> (X,Y=2*delta*U*V),

E_tau^prod: Y^2=a*b*c*d.
```

The target is the product elliptic curve from `wl571`. The map has degree two.
Since both smooth projective curves have genus one, Riemann-Hurwitz proves it
is unramified. Without a rational point on `T_tau`, call this an etale
degree-two genus-one cover, not automatically a rational 2-isogeny.

## Exact Fiber Product

The full generic source-square cover is exactly

```text
T_tau x_{P^1_X} {q^2=X}.
```

The forward and converse formulas are

```text
(q,p,s) -> (X=q^2,U=q*p,V=s),
(X,U,V,q) -> (q,p=U/q,s=V).
```

No denominator is lost on the candidate locus because `X>1`.

For `tau!=1/2`, the branch supports of the three independent squareclasses
are

```text
X:                 {0,infinity},
a*b/(2*delta):     {root(a),root(b)},
c*d/(2*delta):     {root(c),root(d)}.
```

They are six distinct points. The degree-eight fiber product therefore has

```text
2*g-2=8*(-2)+6*4=8,
g=5,
```

recovering the exact generic genus-five cover of `wl571`.

## Square-X Is Not Automatic

At `X=0`, the four linear factors are

```text
-2, 2*tau, 2*tau+4, 4*tau-2.
```

At infinity their leading coefficients are

```text
tau+2, -(2*tau-1), 1, tau.
```

All are nonzero for the live interval with `tau!=1/2`. Hence `T_tau` is
unramified above both `0` and infinity. On its smooth projective completion,
the function `X` has four simple zeros and four simple poles over the
algebraic closure. Its divisor is not even, so `X` is not a square in
`Qbar(T_tau)`.

Therefore adjoining `q^2=X` is a genuinely connected quadratic pullback. In
contrast to the automatic lift in `wl582`, square `X` remains an independent
arithmetic condition here.

## Exceptional tau=1/2

At the already excluded value `tau=1/2`, the torsor becomes

```text
U^2=5*X-4,
V^2=X*(X+5).
```

It is again genus one, but its branch support is

```text
{4/5,infinity,0,-5}.
```

Adding `q^2=X` recovers the exceptional genus-one full cover from `wl571`,
not the generic genus-five curve. `wl572` already proves that this branch
cannot have an integral prime parameter, so it is not reopened here.

## Exact New Failure Point

For every live candidate, the point `(X,U,V)` must lie on `T_tau(Q)` and
satisfy simultaneously

```text
X is a positive rational square in the exact wl570 interval,
ell=L(X,tau) is an odd prime congruent to 1 mod 4.
```

This is strictly stronger than the product elliptic quotient because
`T_tau` retains the two individual source-square lifts. It is strictly smaller
than the genus-five cover because the independent square-`X` pullback has not
yet been imposed.

## Next Exact Gate

Analyze rational points on `T_tau` with square `X` and the exact prime formula,
or prove an obstruction to the etale degree-two lift over the product elliptic
curve. Unrestricted product-curve points, unrestricted torsor ranks, finite
counts, or another quotient that forgets square `X` are not enough.

## Boundary

This proves an exact genus-one torsor and fiber-product decomposition. It does
not prove `T_tau(Q)` empty, classify its square-`X` points, solve `wl535`,
prove family exclusion or a Selmer upper bound, or enter M3.
