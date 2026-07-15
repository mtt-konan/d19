# Q2c Constant, Norm, and Localization Maps

## Outcome

`q2c_exact_maps_and_global_local_lifts`

The committed `q2b-fixed-basis-payload.json` is now consumed as an exact
absolute power-basis field model.  Q2c computes the supported constant
squareclasses, all sixteen relative norms, and the localization map at
`pi=(94*i-169)` in the Q2a local basis.  Both accepted Q2a classes have
global norm-square ambient lifts.

The calculation is pure Python.  It uses the stored multiplication table and
stored field elements, with a six-dimensional relative `K=Q(i)` basis
`1,a,...,a^5`.  The rational change-of-basis determinant is

```text
det[1,a,...,a^5,i,ia,...,ia^5] = -1/2^34.
```

Thus the relative multiplication determinants below are exact determinants
over `K`, not absolute norms or numerical approximations.

## Supported Constants

Use the `K` squareclass basis

```text
[i], [lambda], [pi], [bar_pi],
lambda=1+i, pi=-169+94*i, bar_pi=-169-94*i.
```

Outside these three finite `K` primes the extension is unramified, so a
constant whose class lies in the supported ambient `V_S` has even valuation
outside them.  Hence these four supported constant classes span the exact
constant subspace relevant to Q1.  The ambient column order is

```text
zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_10.
```

`M_const` is displayed by columns, one column per constant:

```text
[i]       = (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
[lambda]  = (0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0)
[pi]      = (0,1,0,1,0,1,0,0,1,1,0,0,0,0,1,0)
[bar_pi]  = (1,1,0,1,1,0,0,0,0,0,1,1,0,1,0,1).
```

These are exact squareclass relations.  For each displayed column `c`, the
script verifies an absolute power-basis vector `w` with

```text
w^2 * product(ambient_basis_j^c_j) = constant.
```

The `i` relation uses `i^2=-1` and `zeta4=-i`.  The other three relations
have exact stored witnesses.  The four columns have rank `4` over `F_2`.
In particular, the earlier ideal-parity skeleton is not being used as a
replacement for the unit correction.

## Relative Norm

The exact norm values, in ambient column order, are:

```text
zeta4      -> -1
epsilon_1  -> -1
epsilon_2  -> -1
epsilon_3  -> -1
epsilon_4  ->  1
epsilon_5  ->  1
S_prime_1  ->  1+i
S_prime_2  -> -1+i = i*(1+i)
S_prime_3  -> -169+94*i = pi
S_prime_4  -> pi
S_prime_5  ->  169+94*i = -bar_pi
S_prime_6  -> -169-94*i = bar_pi
S_prime_7  ->  169-94*i = -pi
S_prime_8  -> bar_pi
S_prime_9  -> 19725-31772*i = pi^2
S_prime_10 -> -346957-7223618*i = bar_pi^3.
```

Because `-1=i^2` in `K`, the norm matrix with rows
`[i],[lambda],[pi],[bar_pi]` is

```text
M_norm =
  0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 1 1 0 0 1 0 0 0
  0 0 0 0 0 0 0 0 0 0 1 1 0 1 0 1
```

The first row has the additional `S_prime_2` bit; written without visual
alignment ambiguity, its nonzero column is `S_prime_2`, while the second row
has nonzero columns `S_prime_1,S_prime_2`.  The exact matrix rank is `4`.

## Odd-pi Localization

The local component order is `(F_1,F_2,E_r,E_u)`.  Before the diagonal
`F_pi^*` quotient, use the eight rows

```text
(a_1,b_1 ; a_2,b_2 ; c,d ; e,f)
```

where the Q2a component bases are

```text
F_1,F_2: [varpi],[nu]
E_r:    [rho],[nu]
E_u:    [varpi],[eta].
```

The exact localization matrix in these rows is

```text
M_loc_flat =
  0000000010000000
  1001001111111100
  0000000001000000
  1110110111101011
  0000000000001000
  1110000000100000
  0000000000000010
  0111110011101010
```

The `M_loc_flat` rows are bit rows in the same sixteen-column order.  The
local norm rows are `a_1+a_2+c` and `b_1+b_2+f`.  On their kernel, the exact
Q2a `H_pi` coordinates are

```text
(h_varpi,h_nu,h_r,h_u)
  = (a_1+a_2, b_1+b_2, d+b_1, e+a_1).
```

Equivalently, the induced four-row matrix on the norm kernel is

```text
M_loc_H =
  0000000011000000
  0111111000010111
  0111001111011100
  0000000010000010.
```

The four rows are only interpreted as `H_pi` coordinates after the two local
norm equations vanish.  `M_loc_flat` is the full local fake-quotient map for
all ambient columns, so no non-norm column is silently called an `H_pi`
class.

The local calculation is exact at the first two `pi`-adic digits.  The
selected `i` residue lifts to `i=1149174404 mod p^2`.  The four monic factors
modulo `p^2` are stored and their product is checked to equal `g6`.  The
ramified factor discriminant satisfies

```text
Disc(F_r)/(2*pi) = 23453 mod p,
15446^2 = 23453 mod p,
```

so Q2a's choice is `[d_r]=[2*pi]` and `[varpi]=[-d_r]=[2*pi]`.  At the
ramified component, the odd valuation column is normalized by
`rho=2*theta+B_r`, giving the exact derivative residue
`alpha'(11745)/2`.  The payload reduction audit finds exactly four zero
components:

```text
S_prime_3: F_1, v_pi(N)=1, v_F1=1
S_prime_4: F_2, v_pi(N)=1, v_F2=1
S_prime_7: E_r, v_pi(N)=1, v_Er=1
S_prime_9: E_u, v_pi(N)=2, v_Eu=1
```

The last line is the required higher `p`-adic normalization: the unramified
quadratic component has residue degree `2`, so its component norm carries the
`pi^2` valuation while the local uniformizer parity is computed from
`v_Eu=2/2`.  Its unit bit is obtained by dividing the exact local norm by
`varpi^2` and reducing the resulting unit, rather than assuming that every
`F_u` zero has first-order valuation.  The first-order `p^2` evaluations agree
with the same normalized unit bits for the three valuation-one columns.

The conversion from `[pi]` to the Q2a `[varpi]` basis is component-specific.
At `F_1,F_2`, `[pi]=[varpi]+[nu]`; in the unramified quadratic component,
`[nu]` is a square, so `[pi]=[varpi]` and the `eta` bit is not toggled.  This
distinction changes only the final `f` bit of `S_prime_9` and restores the
local/global norm identity.  All other columns have valuation zero at their
component.

The local norm rows agree column-by-column with the global `M_norm` after
mapping

```text
[i] -> (0,1), [lambda] -> (0,1), [pi] -> (1,1), [bar_pi] -> (0,1)
```

in the local basis `[varpi],[nu]`.  The supported constants have zero
`H_pi` coordinate, as required by the fake quotient.

## Global Q2a Lifts

Solving the exact system

```text
M_norm * x = 0,
M_loc_H * x = target
```

on the norm kernel gives rank `8` and solution-space dimension `8` for each
target.  In particular, the following canonical representatives verify all
equations exactly:

```text
beta_12 = (0,1,1,0) = loc_pi(epsilon_1),
beta_r  = (0,0,1,0) = loc_pi(epsilon_1 + epsilon_4).
```

The exact relative norms are

```text
N(epsilon_1) = -1 = i^2,
N(epsilon_1*epsilon_4) = -1 = i^2,
```

so both are global norm-square lifts.  The four supported constant columns
lie in the homogeneous solution space and map to zero in the fake quotient;
they are therefore already factored out by the Q1 constant quotient.

## Validation

```text
python3 scripts/theory/berry_sextic_q2c_maps.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/test_berry_sextic_q2c_maps.py -n 1
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/berry_sextic_q2c_maps.py \
  tests/test_berry_sextic_q2c_maps.py
git diff --check
```

## Strict Proof Boundary

Q2c computes only the supported ambient constant quotient, the global norm
map, the odd-`pi` localization map, and the existence of two global ambient
lifts of the two Q2a local classes.  It does not compute or claim a fake
Selmer group, a true Selmer group, a rank, saturation, rational `t` values,
`Q3`-`Q7`, or the Berry classification.  Q2a's local-image completeness is
preserved and is used only as the stated local target.  No Magma request,
`TwoSelmerGroup`, other Berry sextic, or `wl597` is involved.
