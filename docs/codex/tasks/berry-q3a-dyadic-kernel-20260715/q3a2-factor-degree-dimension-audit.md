# Q3a2 Dyadic Factor-Degree Dimension Audit

## Outcome

`q3a2_degree_only_dimensions`

Assume the certified relative factor degrees at `varpi` mean that `g6` is
separable over

```text
K = K_varpi = Q_2(i)
```

and factors as two irreducibles of degrees `2` and `4`.  Set

```text
E_2 = K[t]/(g_2),  E_4 = K[t]/(g_4),
A = A_varpi ~= E_2 x E_4.
```

No factor coefficients, p-adic factorization, Sage, or Magma are used below.
The factor degrees force `dim W_varpi=16`, but they do not select one value
for `dim F_varpi` or `dim H_varpi`.  The exact alternatives are controlled by
whether the quadratic factor field embeds in the quartic factor field.

## Local Squareclass Facts

For every finite extension `E/Q_2`, the standard dyadic local-field formula is

```text
dim_F2 E^*/E^{*2} = [E:Q_2] + 2.
```

Since `[K:Q_2]=2`, this gives

```text
dim_F2 K^*/K^{*2} = 4,
dim_F2 E_2^*/E_2^{*2} = 2*2 + 2 = 6,
dim_F2 E_4^*/E_4^{*2} = 2*4 + 2 = 10.
```

Therefore

```text
W_varpi = A^*/A^{*2}
         ~= (E_2^*/E_2^{*2}) x (E_4^*/E_4^{*2}),
dim_F2 W_varpi = 6 + 10 = 16.
```

This is a local algebra squareclass dimension.  It is not the dimension of
the 16-column global S-unit coordinate space, and it gives no localization
columns.

## Norm-Restriction Lemma

For a finite separable extension `E/K`, write

```text
V_K = K^*/K^{*2},  V_E = E^*/E^{*2},
R_E = ker(V_K -> V_E),
U_E = im(N_{E/K}: V_E -> V_K).
```

The quadratic Hilbert pairings on `V_K` and `V_E` are nondegenerate.  Norm-
restriction compatibility gives, for `x in E^*` and `a in K^*`,

```text
(N_{E/K}(x), a)_K = (x, a)_E.
```

Consequently,

```text
U_E^perp = R_E,
rank_F2(U_E) = 4 - dim_F2(R_E).
```

Indeed, a squareclass `[a]` lies in `U_E^perp` exactly when
`(x,a)_E=1` for every `[x] in V_E`; nondegeneracy then says that `[a]` is a
square in `E`, which is exactly `[a] in R_E`.

The restriction kernel has the intrinsic field interpretation

```text
R_E = { [a] in V_K : K(sqrt(a)) is contained in E }.
```

Thus its dimension records the quadratic subfields of `E/K`; it is not
determined by the degree alone.

## The Two Factor Norm Ranks

The degree-2 factor is itself a quadratic extension.  If
`E_2=K(sqrt(d_2))`, then

```text
R_2 = <[d_2]>,  dim R_2 = 1,
rank_F2(U_2) = 3.
```

This rank is forced without knowing `d_2`.

For the degree-4 factor, let

```text
d_4 = dim_F2 R_4.
```

The degree only gives `d_4 in {0,1,2}`:

```text
d_4 = 0  iff E_4 has no quadratic subfield,
d_4 = 1  iff E_4 has exactly one quadratic subfield,
d_4 = 2  iff E_4/K is biquadratic.
```

The norm-image rank is therefore exactly

```text
rank_F2(U_4) = 4 - d_4 in {4,3,2},
```

but `[E_4:K]=4` alone does not determine which of these three ranks occurs.
Selecting one requires exact quadratic-subfield/squareclass information about
the quartic factor, which is coefficient data not supplied by the degree
partition.

## Constant Quotient

Let `B_varpi` be the diagonal image of `V_K` in `W_varpi`.  Its kernel is

```text
ker(V_K -> W_varpi) = R_2 intersect R_4.
```

Since `R_2` has dimension one, put

```text
d = dim_F2(R_2 intersect R_4) in {0,1}.
```

Equivalently, `d=1` exactly when `E_2` embeds into `E_4`; otherwise `d=0`.
Hence

```text
dim_F2 B_varpi = 4 - d,
dim_F2 F_varpi = dim W_varpi - dim B_varpi = 12 + d.
```

In particular:

```text
E_2 not contained in E_4:  dim B_varpi = 4, dim F_varpi = 12;
E_2 contained in E_4:      dim B_varpi = 3, dim F_varpi = 13.
```

The relative degrees `[2,4]` do not decide this containment.  The fact that
the two factors are different local factors of the same global algebra does
not, by itself, prevent the corresponding local fields from having this
embedding relation.

## Norm Kernel of the Fake Quotient

The product norm on `W_varpi` is

```text
N_A(x_2,x_4) = N_{E_2/K}(x_2) N_{E_4/K}(x_4),
```

so its image is `U_2 + U_4` in the four-dimensional space `V_K`.  The total
degree is six, hence a diagonal constant `a in K^*` has norm `a^6`, a square.
Thus `B_varpi` lies in the norm kernel and the norm descends to

```text
Nbar_varpi: F_varpi -> V_K.
```

Using the norm-restriction lemma,

```text
(U_2 + U_4)^perp = R_2 intersect R_4,
rank_F2(Nbar_varpi) = rank_F2(U_2 + U_4) = 4 - d.
```

Therefore

```text
dim_F2 H_varpi
  = dim_F2 F_varpi - rank_F2(Nbar_varpi)
  = (12 + d) - (4 - d)
  = 8 + 2*d.
```

The exact degree-only alternatives are consequently

```text
E_2 not contained in E_4:  dim F_varpi = 12, dim H_varpi = 8;
E_2 contained in E_4:      dim F_varpi = 13, dim H_varpi = 10.
```

The degree-4 factor's individual norm rank remains `2`, `3`, or `4` as
described above.  Its rank does not by itself determine the total norm rank:
the total rank is `4` when `R_2` and `R_4` are disjoint, and `3` when they
share the quadratic class defining `E_2`.

## Boundary

The accepted source dimension is

```text
dim_F2 J(K_varpi)/2J(K_varpi) = 5.
```

For the fake evaluation map `delta_varpi`, this yields only

```text
dim im(delta_varpi) <= 5,
dim ker(delta_varpi) + dim im(delta_varpi) = 5.
```

It does not imply `dim im(delta_varpi)=5`, does not choose a basis of
`H_varpi`, and does not determine any of the 16 localization columns.  Those
require the actual embeddings of the global S-unit generators into the two
local factor squareclass groups, together with a chosen local coordinate
basis.  The status of `D_inf` modulo `2J(K_varpi)` is unchanged by this
dimension audit.

This report is limited to Q3a2.  It makes no Q3b, Q3a3, Q4, Selmer, rank, or
Berry-classification claim.
