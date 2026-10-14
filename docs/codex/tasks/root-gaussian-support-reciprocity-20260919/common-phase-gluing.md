# Common phase and the finite gluing obstruction

This note records the next exact layer after the Gaussian support audit.  It
does not claim a global exclusion.

## Fixed squareclass cover

Put `K=Q(i)`,

```text
u_0=z,       u_1=z-1,       u_2=z-i,       u_3=z-1-i.
```

The norm-square condition on `u_j` is equivalent to

```text
u_j = d_j s_j^2,       d_j in Q^*, s_j in K^*.
```

For a fixed rational squareclass tuple `d=(d_0,d_1,d_2,d_3)`, the full
individual lift is the projective intersection of three quadrics

```text
d_0 s_0^2 - d_1 s_1^2 = h^2,
d_0 s_0^2 - d_2 s_2^2 = i h^2,
d_1 s_1^2 - d_3 s_3^2 = i h^2
```

in `P^4_K`.  The affine chart `h=1` reconstructs `z=d_0s_0^2`.  The fourth
edge equation follows from the displayed three.  A smooth complete
intersection of three quadrics in `P^4` has genus

```text
1 + (2*2*2)/2 * (2+2+2-5) = 5.
```

Thus the genuine object is a genus-five simultaneous-lift curve `C_d`, not
any one of its elliptic quotients.

This should be read as a new presentation of an old object layer, not as a
new genus-five curve theorem.  The project already contains three related but
different genus-five constructions:

* `wl594` uses the `V_4` cover `z_A^2=Q_A(t), z_B^2=Q_B(t)` over the closure
  parameter `t`; it has eight finite branch points and genus five.  It is a
  quotient after fixing the closure data and retains only two source-product
  lifts.
* The Berry sextic pullback is a particular hyperelliptic genus-five curve
  attached to one low-degree rational family on the Kummer surface.
* The present `C_d` is the full `(Z/2)^4` cover of the `z`-line, branched at
  `0,1,i,1+i,infinity`, with the four individual norm lifts retained.

They all have genus five, but equal genus does not make them birational.  The
first and the second are restricted quotient/family curves; the third is the
universal fixed-squareclass individual-lift curve over `Q(i)`.  Conversely,
the older three-root complete `d`-coordinate covers in the AA/BB route are
elliptic torsors after normalization (their naive three-quadric projective
models have singular infinity), so they should not be identified with this
five-branch-point cover merely because the equations look similar.

## Two exact compatibility identities

Let

```text
a = d_0 d_3,  b = d_1 d_2,
A = d_0 d_1,  B = d_2 d_3,
D = a b = A B,  q = 1+i.
```

The multiplicative square identity

```text
u_0 u_3 - u_1 u_2 = -i
```

pulls back to

```text
a (s_0 s_3)^2 - b (s_1 s_2)^2 = -i.
```

Consequently the quaternion class `(D,a*i)_K` is split.  The two conjugate
diagonal conics give `(a,i)_K=(b,i)_K=0`; hence

```text
(a,b)_K = 0,       (D,i)_K = 0.                 (1)
```

There is a second relation which keeps the finer Gaussian prime at `1+i`.
For a conic `d_j x^2-d_k y^2=c`, its split class is
`(d_j d_k,d_j c)_K`.  Summing the four diagonal/cross equations for
`(0,2),(1,3),(0,3),(1,2)` gives, by bilinearity and
`[1-i]=[i]+[1+i]`,

```text
(A,B)_K + (a,i)_K + (D,q)_K = 0.
```

Using `(a,i)_K=0`, every genuine lift therefore satisfies

```text
(A,B)_K = (D,1+i)_K.                             (2)
```

Equation (2) is the first useful relation coupling the two diagonal
factorisations to the dyadic Gaussian prime.  It is a relation between
`d`-dependent classes, not a fixed nonzero Brauer class.  For example, the
abstract squareclass tuple `(d_0,d_1,d_2,d_3)=(1,3,51,1)` makes all six
pair-conic classes split, while both sides of (2) have discriminant the
prime ideals above `17`; so (2) can be nontrivial without being a
contradiction.

## Why the five elliptic quotients miss the obstruction

The multiquadratic cover of the `z`-line has character quotients

```text
Y_J^2 = d_J * product_{j in J}(z-a_j).
```

The four `|J|=3` quotients and the `|J|=4` quotient are elliptic (the latter
has the `j=1728` CM model).  Their Jacobian character dimensions add to the
genus-five dimension.  Hence the positive-genus quotient list is complete,
but the quotient maps retain only product square roots.

Define the phase quotient

```text
P = K^*/(Q^* K^{*2}),   rho_j = class(u_j) in P.
```

An individual rational norm-square lift is exactly `rho_j=0`.  A product
quotient only sees sums of phases.  If all pair products are rational
squareclasses, it forces

```text
rho_0 = rho_1 = rho_2 = rho_3 = rho,
```

while the fourfold product sees `4 rho=0` automatically.  The elliptic
quotients can therefore leave one common phase `rho`; the original problem
requires this residual phase itself to vanish.  This is the finite gluing
problem between the five elliptic quotients.

## Scope boundary

The genus-five model and relations (1)--(2) are exact and preserve all four
individual lifts.  They do not show that `C_d(K)` is empty, nor that every
admissible support tuple has a nonzero phase.  A real next theorem would have
to compute the simultaneous Kummer/2-cover image of `C_d` (equivalently, the
gluing obstruction among the five quotient points) uniformly in the support
tuple.  This is a different target from increasing the modulus at `2` or
checking the five elliptic curves separately.
