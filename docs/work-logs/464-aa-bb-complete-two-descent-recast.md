# AA+BB Complete 2-Descent Recast

## Question

Can the `wl463` point-level two-primary collapse be recast inside complete
2-descent, so the route is no longer phrased as a separate "Selmer lift"
between three independent isogeny packages?

```text
dim Sel_2(E) = 2
```

And after that recast, does the current evidence already force this bound?

## Result

The right recast is a complete 2-descent problem on the common full rational
2-torsion curve:

```text
E_L: Y^2 = (X-(-p))*(X-(2*sqrt_q))*(X-(-2*sqrt_q))
     = (X+p)*(X^2 - 4*q).
```

In this framing, the product relation and local common-source condition are
not a separate Selmer-lift theorem. They are built into complete 2-descent
Selmer membership: a Selmer element is represented by local points on the same
complete 2-cover at every place.

However, the current evidence still does **not** force `dim Sel_2(E)=2`.
Before building the full complete-cover local matrix, the cheaper next audit is
the pseudo-Selmer container

```text
S~
```

defined by the product relation, the existing odd-prime support bounds, the
dyadic `wl460-wl463` constraints, and the archimedean sign row.

## Full Rational 2-Torsion Model

Use

```text
T = A+B,
p = 8*L^2 - 2*T^2,
sqrt_q = T^2 + 4*L^2,
```

with `L=A` on the `AA` side and `L=B` on the `BB` side. The roots are

```text
e_minus = -p,
e_pos   =  2*sqrt_q,
e_neg   = -2*sqrt_q.
```

Thus

```text
E_L[2](Q) = {O, (e_minus,0), (e_pos,0), (e_neg,0)}
```

and

```text
dim_F2 E_L[2](Q) = 2.
```

Therefore a rank-zero proof by complete 2-descent would need:

```text
dim_F2 Sel_2(E_L) = 2.
```

## Complete 2-Descent Coordinates

For a non-2-torsion point, the complete descent squareclass coordinates are:

```text
d_minus = X - e_minus = X+p
d_pos   = X - e_pos   = X-2*sqrt_q
d_neg   = X - e_neg   = X+2*sqrt_q
```

with product relation

```text
d_minus * d_pos * d_neg = Y^2 = 1 in Q*/Q*2.
```

A candidate complete 2-cover is represented by squareclasses

```text
(d_minus, d_pos, d_neg)
```

satisfying that product relation and the local solubility of

```text
d_minus*u_minus^2 = X+p
d_pos*u_pos^2     = X-2*sqrt_q
d_neg*u_neg^2     = X+2*sqrt_q.
```

Equivalently, the local matrix has to solve the difference equations:

```text
d_minus*u_minus^2 - d_pos*u_pos^2 = p+2*sqrt_q
d_minus*u_minus^2 - d_neg*u_neg^2 = p-2*sqrt_q
d_pos*u_pos^2     - d_neg*u_neg^2 = -4*sqrt_q.
```

## Relation To The Three Isogeny Coordinates

The three package coordinates used in `wl457-wl463` are not the complete
descent coordinates themselves. They are:

```text
x_minus_p      = d_pos*d_neg/d_minus
x_pos_2sqrt_q  = d_minus*d_neg/d_pos
x_neg_2sqrt_q  = d_minus*d_pos/d_neg
```

Their product is the complete-descent product:

```text
x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q
  = d_minus * d_pos * d_neg
  = 1.
```

This explains why the point-level product relation is real. In complete
2-descent it is not an extra lift condition; it is the product row of the
Selmer coordinates.

## Translation Of Existing Inputs

Odd-prime formal-lift inputs:

```text
wl457  kernel_neg_2sqrt_q    no odd-prime valuation support
wl458  kernel_minus_p        no odd-prime valuation support
wl459  kernel_pos_2sqrt_q    support only from ell | T, ell == 1 mod 4
```

Dyadic inputs:

```text
wl460  opposite-mod-4 branch forces x_minus_p in {1}
wl461  same-mod-4 branch has local x_minus_p class 2
wl462  same-mod-4 class 2 is incompatible with the other kernels
wl463  genuine common-source rational points collapse to (1,1,1)
```

In complete 2-descent language, these are useful support inputs for a cheap
upper-bound container. The full local solubility rows for the complete covers
`C_d` should be built only if `S~` still leaves unresolved dimension.

## Audit

The immediate pseudo-Selmer audit gives:

```text
dim_F2 S~ <= 2 + omega_{1 mod 4}(T) + epsilon_sign.
```

Thus the current constraints do **not** force

```text
dim_F2 Sel_2(E_L) = 2.
```

The current symbolic obstruction is the possible `ell | T`, `ell == 1 mod 4`
tail plus a possible archimedean sign bit. If those survive, then the full
`C_d` local matrix or a second-descent / Cassels-Tate style route becomes
necessary.

## Boundary

This note does not prove:

- `dim Sel_2(E)=2`,
- a rank upper bound,
- rank zero,
- any family exclusion.

It recasts the next proof target precisely: first audit the cheap
pseudo-Selmer container `S~`; build the complete 2-descent local matrix only if
that container does not collapse to the torsion baseline.
