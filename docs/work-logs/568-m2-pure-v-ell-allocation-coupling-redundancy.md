# M2 Pure v_ell Allocation-Coupling Redundancy

## Question

Does coupling the `wl567` affine allocation space to the `wl563` scale,
real-coordinate, selected orientation, and cone produce a new obstruction?

## Scale Is Exactly The Product Coordinate

Keep

```text
E=4*(ell-1)*Q^2*D^2,
2*(ell-1)/r=kappa*h^2,
a=g*alpha*M^2,
b=g*beta*N^2,
alpha*beta=kappa.
```

Then

```text
2*r*a*b=2*r*g^2*kappa*M^2*N^2
```

equals `E` if and only if

```text
(g*M*N)^2=(h*Q*D)^2.
```

All factors on the left are positive, so this is equivalent to the `wl563`
scale equation

```text
g*M*N=h*abs(Q*D).
```

Thus scale is not an additional condition after the imaginary-coordinate
equality; it is that equality with the known squareclass cancelled.

## Cone Is Exactly The Original Positivity

Put

```text
F=Q^4+(8-4*ell)*Q^2*D^2-4*D^4.
```

The original strict inequality is identically

```text
ell*Q^4+4*Q^2*D^2-4*ell*D^4
  = ell*F+(ell-1)*E.
```

After substituting the two Gaussian coordinates, its right side is

```text
r*g^2 * (
  ell*(alpha^2*M^4-beta^2*N^4)
  +2*(ell-1)*kappa*M^2*N^2
).
```

Because `r*g^2>0`, the `wl563` cone is equivalent to the original positivity.
It cannot independently cut down a candidate once the coordinate equalities
and original inequality are retained.

## The Affine Rows Are Automatic On An Actual Factorization

Let

```text
H=alpha^2*M^4-beta^2*N^4.
```

For every unresolved split prime `q|kappa`, reducing this actual `H` modulo
`q` gives exactly the two `wl566` formulas according as `q|alpha` or
`q|beta`. The algebra in `wl567` combines those two formulas into

```text
Delta_q*x_q + sum_(t!=q) A_qt*x_t = z_q+a_q.
```

Consequently, if `z_q` is computed from the same actual `H`, every row holds
identically. Gaussian elimination is useful only when the right-hand signs
are supplied independently. Here they depend on the unknown `M,N` in `H`, so
the affine system does not add an independent obstruction to the global
integer equations.

The converse is deliberately not claimed: a bit vector satisfying the affine
rows need not produce integers `M,N`, the real-coordinate equality, or a
rational `wl535` point.

## Exact Collapse Back To The Norm Square

Set

```text
A=alpha*M^2,
B=beta*N^2.
```

The two Gaussian coordinate equalities imply the signed ratio branch

```text
2*F*A*B=E*(A^2-B^2).
```

For positive rational `A,B`, define

```text
C=E*(A^2+B^2)/(2*A*B)
```

Then the signed ratio branch implies

```text
C^2=F^2+E^2.
```

The exact reverse statement has two ordered branches:

```text
C^2-F^2-E^2
 = (E*(A^2-B^2)-2*F*A*B)
   *(E*(A^2-B^2)+2*F*A*B)/(4*A^2*B^2).
```

Thus a norm square recovers the signed ratio equation only after the correct
ordering/sign branch is retained. The actual Gaussian factorization supplies
that branch; an affine allocation vector alone does not. Consequently the
complementary allocation plus real/product coordinates is a factorization of
the original Gaussian norm-square condition, not a new independent
obstruction.

## Smaller Exact Missing Lemma

On the trivial real-unit branch, all allocation-only refinements are now
exhausted. The remaining exact lemma is the selected-orientation norm-square
intersection:

- use `Q=+/-R_pi(x,y)` when `ell=5 mod 8`;
- use `Q=+/-B_pi(x,y)` with `v_2(Q)>=3` when `ell=1 mod 8`;
- retain the primitive real-quadratic double-descent equation from `wl546`;
- prove that `F^2+E^2` cannot be a square under the strict inequality, or
  produce a strict point.

This is strictly narrower than the two-orientation system in `wl546`, but it
is not solved here. A next proof gate must attack this orientation/norm
intersection directly. It must not return to allocation matrices, standalone
local tables, or standalone dyadic refinements.

## Boundary

This proves an exact failure point for the `wl563`-`wl567` allocation route.
It does not solve the selected orientation/norm intersection, handle the
nontrivial real-unit class, prove `wl535`, identify a Selmer group, or enter
M3.
