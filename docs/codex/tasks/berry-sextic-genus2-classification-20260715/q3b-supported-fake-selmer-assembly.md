# Berry C_1 Q3b Supported Fake-Selmer Assembly

## Outcome

`supported_dyadic_coordinate_blocker`

The exact Q2c matrices, complete odd local image, and frozen Q3a2 dyadic
localization assemble to a six-dimensional supported quotient candidate.  Its
dyadic image is an explicit six-dimensional subspace of the frozen
eight-dimensional `H_varpi`, and the map is injective on this quotient.

Q3a3 supplies only

```text
dim_F2 I_varpi = 4,
delta_varpi(D_i) = 01110110.
```

It does not supply a coordinate basis or an exact coordinate characterization
of `I_varpi`.  The known class `01110110` is not in the supported dyadic image,
so the supported fake-Selmer intersection cannot be computed from its
dimension.  The remaining issue is a coordinate blocker in `H_varpi`, not an
arithmetic or software blocker.

## Global Candidate

Use the ambient order

```text
zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_10.
```

On the global norm kernel, the accepted odd image is

```text
I_pi = span{0110,0010}
```

in the Q2a order `(h_varpi,h_nu,h_r,h_u)`.  Therefore the complete odd local
condition is equivalent to the two equations `h_varpi=0` and `h_u=0`.  In the
ambient coordinates this gives the exact six-row matrix

```text
M_3b =
  0000000100000000
  0000001100000000
  0000000011001000
  0000000000110101
  0000000011000000
  0000000010000010
```

The first four rows are `M_norm`; the last two are the first and fourth rows
of `M_loc_H`.  Its rank is `6`, so

```text
S_{N,pi} = ker(M_3b),
dim S_{N,pi} = 16-6 = 10.
```

One exact basis, written as 16-bit ambient vectors, is

```text
1000000000000000  = zeta4
0100000000000000  = epsilon_1
0010000000000000  = epsilon_2
0001000000000000  = epsilon_3
0000100000000000  = epsilon_4
0000010000000000  = epsilon_5
0000000000110000  = S_prime_5+S_prime_6
0000000000100100  = S_prime_5+S_prime_8
0000000011000010  = S_prime_3+S_prime_4+S_prime_9
0000000000100001  = S_prime_5+S_prime_10.
```

The four supported constant columns are

```text
1000000000000000  = i
0101110000000000  = lambda
0101010011000010  = pi
1101100000110101  = bar_pi.
```

They have rank `4`, lie in `S_{N,pi}`, and vanish in both fake localizations.
Extending these four columns inside `S_{N,pi}` gives the supported quotient

```text
S_{N,pi}/C_S,
dim_F2(S_{N,pi}/C_S)=10-4=6.
```

An exact quotient basis, represented by ambient lifts, is

```text
q_1 = [epsilon_1]
q_2 = [epsilon_2]
q_3 = [epsilon_3]
q_4 = [epsilon_4]
q_5 = [S_prime_5+S_prime_6]
q_6 = [S_prime_5+S_prime_8].
```

Their odd `H_pi` coordinates are respectively

```text
0110, 0110, 0110, 0100, 0110, 0110,
```

so each lies in the complete odd local image.  Here `0100` is
`beta_12+beta_r`; no odd-local condition has been dropped.

## Dyadic Localization

Apply the frozen Q3a2 quotient map to the sixteen-column dyadic localization
and then express the result in the frozen eight-row `H_varpi` basis.  In the
quotient basis `(q_1,...,q_6)`, the exact map has matrix

```text
M_{dyad,H} =
  010110
  011010
  001101
  100000
  101001
  000000
  100100
  011100.
```

The four frozen dyadic norm rows vanish on every column.  The four supported
constants map to zero before taking these six quotient columns.  The matrix
has rank `6`, hence its quotient kernel is zero and its image

```text
W_supported = loc_varpi(S_{N,pi}/C_S) subset H_varpi
```

has dimension `6`.  An exact image basis is

```text
00011010
11000001
01101001
10100011
11000000
00101000.
```

The same subspace can be recorded by its two independent annihilator rows in
the frozen `H_varpi` coordinates:

```text
00000100,
00101010.
```

Thus

```text
W_supported = {h in H_varpi:
  h_6=0,
  h_3+h_5+h_7=0}.
```

This is a coordinate description of the supported global image, not of the
local Jacobian image.

## Remaining Membership

The accepted Q3a3 exact-sequence calculation proves `dim I_varpi=4`, but it
does not give four coordinate vectors in `H_varpi`.  No local Tate-pairing
matrix, Brauer-compatible coordinate map, or equivalent descent basis is
present in the accepted inputs.  The Q3a3 exact sequence controls the kernel
dimension; it does not determine which four-dimensional subspace of
`H_varpi` is `I_varpi`.

The one accepted class is

```text
h_i = 01110110 in I_varpi.
```

Its two coordinates modulo `W_supported` are

```text
(h_6, h_3+h_5+h_7) = (1,0),
```

so `h_i` is not in `W_supported`.  Consequently the only exact conclusion
available from the dimensions and this class is

```text
2 <= dim_F2(W_supported intersect I_varpi) <= 3.
```

The lower bound is `6+4-8`; the strict upper bound follows from the known
class outside `W_supported`.  Equivalently, the unresolved projection
`I_varpi -> H_varpi/W_supported` has rank `1` or `2`; deciding whether a local
image class has second quotient coordinate `1` distinguishes intersection
dimension `3` from `2`.  A basis of `W_supported intersect I_varpi` still
requires the missing local coordinate characterization, so no fake Selmer
intersection or true Selmer group is claimed here.

The smallest exact pending object is therefore

```text
W_supported intersect I_varpi
  = {h in I_varpi: h_6=0 and h_3+h_5+h_7=0},
```

with the explicit six-dimensional basis above and the unresolved local-image
membership condition.  This task does not compute a true Selmer group, a
rank, saturation, Q3c-Q4, the `i`-twist, another Berry row, or any `wl597`
artifact.

## Validation

```text
python3 scripts/theory/berry_sextic_q3b_assembly.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/test_berry_sextic_q3b_assembly.py -n 1
```

The verifier also re-runs the accepted Q2c, Q3a2, Q3a3 exact-class, and Q3a3
fake-kernel certificates before accepting this assembly.
