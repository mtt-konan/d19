# Q3a2 Exact Dyadic Diagonal And Norm Matrices

## Outcome

`exact_dyadic_diagonal_norm_and_localization_matrices`

The two exact primes of the absolute degree-12 field above `2` give local
degrees `4` and `8`, hence the two relative factors over
`K_varpi=Q_2(i)` have degrees `2` and `4`.  Working in the maximal order, the
certificate computes squareclasses from the exact primary quotients

```text
O/P_1^9,  O/P_2^17.
```

The exponent `2e+1` is the standard exact dyadic cutoff for
`E^*/E^{*2}`.  Thus the finite quotient enumeration is an exact local-field
squareclass computation, not a stabilization heuristic or bounded search for
points.

## Coordinate Spaces

The product basis is ordered as

```text
P_1 uniformizer, five P_1 unit classes,
P_2 uniformizer, nine P_2 unit classes.
```

This gives

```text
W_varpi = E_2^*/E_2^{*2} x E_4^*/E_4^{*2},
dim W_varpi = 6+10 = 16.
```

The base-field basis is

```text
lambda=1+i, i, 3, 1+2i.
```

Its exact restriction matrix `B_varpi` has rank `4`.  Therefore the diagonal
map is injective; in particular, the earlier degree-only ambiguity is resolved
without testing an embedding `E_2 subset E_4`:

```text
dim B_varpi = 4,
dim F_varpi = dim(W_varpi/B_varpi) = 12.
```

In the product basis, the rows of `B_varpi` are

```text
0000
1111
1011
0000
1000
1000
0000
1110
0010
0000
1000
1000
0000
1000
1000
0000
```

Columns follow the displayed base-field basis.

## Product Norm

The exact product-norm matrix `N_varpi: W_varpi -> K_varpi^*/K_varpi^{*2}`
has rows

```text
1000001000000000
0000001000000000
0001110000100010
1000111000011100
```

in the base-field coordinate order `lambda,i,3,1+2i`.  It satisfies

```text
rank N_varpi = 4,
N_varpi * B_varpi = 0.
```

The induced map on `F_varpi` also has rank `4`, so its exact norm kernel is

```text
H_varpi = ker(F_varpi -> K_varpi^*/K_varpi^{*2}),
dim H_varpi = 12-4 = 8.
```

The payload contains a 12-coordinate quotient presentation, the induced
`4 x 12` norm matrix, eight independent kernel rows, and their sixteen-
coordinate lifts.

## Exact Norm Separation

For a basis element in one local factor, the producer uses an exact global
CRT idempotent which is `1` at the selected dyadic prime and `0` at the other
to lambda-adic precision `8`.  It checks, in normalized prime valuations, that
the patched element differs from the selected local element and from `1` at
the other factor by at least the respective `2e+1` square cutoffs.  Its exact
relative determinant therefore has the same two local norm squareclasses.
This supplies each column of `N_varpi` without a finite-precision factorization.

## Global Localization

All sixteen conservative global S-unit basis elements from Q2b are evaluated
in the same two primary-quotient bases.  The resulting `16 x 16` localization
matrix has rank `16`.  Its product with `N_varpi` equals the independently
computed Q2c global norm matrix exactly.  After quotienting by `B_varpi`, the
fake localization matrix has rank `12`.

The complete matrices, maximal-order basis, ideal HNFs, unit-square witnesses,
CRT determinants, quotient coordinates, and kernel lifts are serialized in
`q3a2-dyadic-matrices-payload.json`.  The standalone Python verifier rebuilds
all finite quotient squareclass cosets and checks every displayed matrix and
rank without a p-adic factorization backend.

## Boundary

Q3a2 is complete for the diagonal map, product norm, exact `F_varpi` and
`H_varpi`, and the sixteen global ambient localization columns.  This does not
compute the local Jacobian fake image `I_varpi`, does not decide
`D_inf in 2J(K_varpi)`, and does not determine the fake-map kernel.  Those are
the separate Q3a3 obligation.  No Selmer, rank, point-set, or Berry
classification conclusion follows from these dimensions alone.

## Reproduction

```text
DOT_SAGE=/private/tmp/d19-sage sage -python scripts/theory/berry_sextic_q3a_dyadic_matrices.sage
python3 scripts/theory/berry_sextic_q3a_dyadic_matrices.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q tests/test_berry_sextic_q3a_dyadic_matrices.py -n 1
```
