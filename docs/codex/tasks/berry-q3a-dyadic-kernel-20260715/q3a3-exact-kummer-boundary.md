# Q3a3 Exact Dyadic Kummer Boundary

## Outcome

`q3a3_exact_setup_and_one_certified_class`

This worker pass does not complete the dyadic fake Kummer image and does not
decide whether `D_inf` is in `2J(K_varpi)`. It records one exact local
Kummer class, the exact divisor/function normalization needed for the missing
classes, and the first missing certificate. The missing result is not being
promoted to an arithmetic blocker.

## Frozen Target Coordinates

Keep the Q3a2 product basis, in the exact order

```text
factor_1_uniformizer, factor_1_unit_1,...,factor_1_unit_5,
factor_2_uniformizer, factor_2_unit_1,...,factor_2_unit_9.
```

The product space has dimension `16`, the diagonal quotient has dimension
`12`, and the norm-kernel target `H_varpi` has dimension `8`. The quotient
coordinate matrix and the eight-row kernel basis are exactly the frozen
fields `quotient_coordinate_matrix_rows` and
`norm_kernel_basis_quotient_rows` in
`q3a2-dyadic-matrices-payload.json`. No replacement basis or normalization
is introduced here.

## Exact Divisor Evaluation Setup

Write `lambda=1+i`, `K_varpi=Q_2(i)`, and use the reciprocal chart

```text
x=1/t,  z=v/t^3,  z^2=g6_star(x)=x^6*g6(1/x).
```

The two infinity points are the distinct points `P_+=(0,1)` and
`P_-=(0,-1)` in this chart. If `Q=(x_Q,z_Q)` is in the `P_+` chart, then
the tangent-normalized fake evaluation of `Q-P_+` is

```text
[1-x_Q*theta] in F_varpi.
```

Indeed the finite-chart expression is `[t(Q)-theta]`, and multiplication by
the diagonal constant `x_Q` gives the displayed reciprocal-chart expression.
For a degree-two divisor whose two reciprocal coordinates have elementary
symmetric functions `s` and `p`, the exact evaluation is

```text
[1-s*theta+p*theta^2].
```

Thus a `K_varpi`-rational quadratic Mumford divisor can be certified by
`u(X)=X^2-sX+p`, a linear `v(X)`, and the exact congruence
`v(X)^2 = g6_star(X) mod u(X)`; its fake class is the displayed element.
This is the formal divisor route that still has to be completed.

For a finite monic factor `h` of `g6`, with `k=g6/h`, the factor-zero
normalization is

```text
beta_h|_{K_varpi[theta]/(h)} = k(theta)^(-1),
beta_h|_{K_varpi[theta]/(k)} = h(theta).
```

At a root of `h`, this follows from `(t-root)/v -> 1/g6'(root)` and
`h'(root)/g6'(root)=1/k(root)`. At both infinity points all monic factors
have leading value `1`. These formulas retain the factor-zero, tangent, and
both-infinity branches; they are not replaced by naive evaluation at a zero
factor.

The even-degree kernel relation remains only

```text
div(t-theta)=2*W_theta-P_+-P_-,
delta_varpi(D_inf)=[1]=0,
D_inf=[P_+-P_-].
```

It does not say that the source class of `D_inf` is zero.

## One Exact Local Class

There is an exact `K_varpi`-point `P_i=(i,v_i)` with `v_i^2=g6(i)`. The
exact identity is

```text
g6(i)=(i-1)^6*(11+12*i)
       =(i-1)^6*(-1)*(1-12*lambda).
```

Since `v_varpi(12*lambda)=5` and `1+varpi^5*O_varpi` consists of squares in
`Q_2(i)`, the square root exists by the exact dyadic Hensel lemma. One may
write `v_i=i*(i-1)^3*s` with `s^2=1-12*lambda`.

For `D_i=[P_i-P_+]`, the exact function evaluation is `[i-theta]`. Running
the frozen Q3a2 primary-quotient arithmetic on this element gives, in the
frozen product basis,

```text
delta_varpi(D_i) before the constant quotient
    = (0,1,1,1,0,0,0,1,0,1,0,1,1,0,1,0),
```

and after the Q3a2 quotient map,

```text
F_varpi coordinates = (0,0,1,1,1,0,1,1,0,1,1,0).
```

In the frozen eight-row `H_varpi` basis this is

```text
delta_varpi(D_i) = (0,1,1,1,0,1,1,0).
```

The norm rows vanish exactly. Consequently this is a certified nonzero
element of the local fake image and proves only

```text
dim_F2(I_varpi) >= 1,
dim_F2(kappa_varpi) <= 4.
```

It is not a complete image basis.

The exact computation is durable in `q3a3-exact-class-payload.json`. Its
Sage producer reconstructs the two primary quotients, evaluates `i-theta`,
and records the local unit residues. The standalone Python verifier rebuilds
both squareclass cosets, applies the frozen quotient and norm matrices, and
checks the displayed `H_varpi` vector.

## Exact Dimension Boundary

The accepted source dimension is

```text
dim_F2 J(K_varpi)/2J(K_varpi)=5.
```

The only dimension identity currently justified is

```text
dim_F2(kappa_varpi)+dim_F2(I_varpi)=5.
```

The Q3a2 values `dim(F_varpi)=12` and `dim(H_varpi)=8` are target dimensions,
not image dimensions. The single class above does not determine the other
four source directions.

## First Missing Certificate

The first missing exact certificate is one of the following local objects:

1. Four further `K_varpi`-rational divisor classes, each given by an exact
   Mumford/Cantor or formal-group certificate and an eight-coordinate image
   vector, followed by the exact rank of the resulting image matrix; or
2. A complete formal-group filtration calculation for `J(K_varpi)` whose
   four non-torsion source coordinates are mapped through the two accepted
   primary quotients `O/P_1^9` and `O/P_2^17`.

The separate `D_inf` obligation needs an exact half-divisor certificate
`2E=D_inf` in local Mumford/Cantor arithmetic, or an exact obstruction to
such a half. Until that is supplied, the contribution of `D_inf` to
`kappa_varpi` is unresolved:

```text
D_inf in 2J(K_varpi)       -> its source class is zero;
D_inf not in 2J(K_varpi)   -> it contributes a nonzero kernel class.
```

No bounded residue enumeration, apparent p-adic stabilization, finite-
precision factorization, or source-dimension inference is used as a
substitute for either certificate.
