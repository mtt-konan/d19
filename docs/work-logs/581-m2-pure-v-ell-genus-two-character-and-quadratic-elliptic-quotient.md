# M2 Pure v_ell Genus-Two Character And Quadratic Elliptic Quotient

## Question

After `wl580` proves that descent bookkeeping is exhausted, does the generic
genus-five source-square cover have a genuinely lower-genus quotient that
retains a strict necessary condition for an exact `wl535` candidate?

This work answers only that question. It constructs a genus-two character
quotient over `Q` and its degree-two elliptic quotient over `Q(i)`. It does not
classify the rational points of either quotient and does not prove `wl535`.

## Input

Keep the `wl570` notation

```text
delta=tau^2+2*tau-1,
a=X*(tau+2)-2,
b=2*tau-X*(2*tau-1),
c=X+2*tau+4,
d=tau*(X+4)-2.
```

On an exact candidate,

```text
X=q^2,
p^2=a*b/(2*X*delta),
s^2=c*d/(2*delta),
sqrt(2)-1<tau<1,
tau!=1/2.
```

The last exclusion is the rigorous `wl572` result. All six branch points used
below are therefore distinct by the determinant calculation in `wl571`.

## Genus-Two Character Quotient

Multiplying the two source-square equations gives

```text
p^2*s^2=a*b*c*d/(4*X*delta^2).
```

Hence every exact candidate maps to

```text
C_tau: Z^2=X*a*b*c*d,
Z=2*X*delta*p*s.
```

For rational admissible `tau!=1/2`, the branch locus of the hyperelliptic
projection is

```text
{0, root(a), root(b), root(c), root(d), infinity}.
```

These are six distinct points, so the smooth projective completion of
`C_tau` has genus two. This is the character quotient belonging to the
squareclass product `u_2*u_3` in `wl571`; it is strictly lower-genus than the
degree-eight genus-five full cover. The map is only forward: a rational point
on `C_tau` need not make the two source factors square separately.

## Reciprocal Symmetry

The base involution

```text
T(X)=-4/X
```

exchanges the four linear factors in pairs:

```text
a(T)=-2*c/X,   c(T)= 2*a/X,
b(T)= 2*d/X,   d(T)=-2*b/X.
```

For `H=X*a*b*c*d`, this gives

```text
H(T)/H(X)=-64/X^6.
```

Thus the base involution does not lift over `Q`, but it does lift over
`K=Q(i)` as

```text
j(X,Z)=(-4/X, 8*i*Z/X^3).
```

Direct substitution gives `j^2=1`.

## Elliptic Quotient Over Q(i)

The following functions are invariant under `j`:

```text
S=X-4/X,
Y=Z*(X-2*i)/X^2.
```

They satisfy the cubic equation

```text
E_tau:
Y^2=-(S-4*i)
     *((tau+2)*S+2*tau^2+8*tau+6)
     *((2*tau^2-tau)*S+6*tau^2-8*tau+2).
```

The discriminant of the cubic right side is

```text
256*(tau-i)^2*(tau+i)^2
   *((1-2*i)*tau+i)^4
   *(tau+2+i)^4
   *(tau^2+2*tau-1)^2.
```

It is nonzero for rational `sqrt(2)-1<tau<1`. Therefore `E_tau` is a smooth
genus-one curve with its point at infinity, hence an elliptic curve over
`Q(i)`. Generically `X` satisfies

```text
X^2-S*X-4=0,
```

so `K(C_tau)/K(E_tau)` has degree two. This proves that the displayed map is
the elliptic quotient by `j`, not merely a substitution identity.

## Exact Forward Obstruction

Every exact `wl535` candidate therefore produces an affine point on
`E_tau(Q(i))` with all of the following extra restrictions:

```text
tau is rational and sqrt(2)-1<tau<1,
S is rational,
S^2+16=(X+4/X)^2 is a nonzero rational square,
the positive root of X^2-S*X-4=0 is the original rational square X,
Y!=0,
ell=L(X,tau) is the original odd prime congruent to 1 mod 4,
and the exact wl570 interval holds.
```

The condition `Y!=0` follows because `X,a,b,c,d,delta,p,s` are all nonzero
on the open candidate locus. Consequently the visible two-torsion points of
the cubic are never candidate images.

This is a strict forward obstruction: proving that the restricted image locus
above is empty would prove the `wl535` proposition. An unrestricted statement
that `E_tau(Q(i))` is nonempty is useless because the point at infinity and
the three rational two-torsion points are always present.

## Next Exact Gate

Analyze only the restricted affine image locus on `E_tau`, including the
quadratic lift `S^2+16` and the prime-parameter condition. A valid next result
must be a rational-point obstruction, a strict exact candidate, or a further
quotient/descent that genuinely constrains this restricted locus. Unrelated
rank tables, finite point counts, and renewed allocation bookkeeping are not
progress.

## Boundary

This work proves a genus-two character quotient and its quadratic elliptic
quotient over `Q(i)`. It does not prove either quotient has no admissible
point, does not solve `wl535`, does not prove family exclusion or a Selmer
upper bound, and does not enter M3.
