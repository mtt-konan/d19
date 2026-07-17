# Berry C_1 Q3b Exact Dyadic Local Image

## Outcome

`exact_local_image_span`

The frozen eight-coordinate basis of `H_varpi` has the exact local fake image

```text
I_varpi = span_F2 {
  01110110,
  01111000,
  00001100,
  00011000
}.
```

The first vector is the previously accepted `D_i` class from Q3a3.  The other
three are independently certified local divisor classes constructed below.
The four vectors have rank `4`; Q3a3 proves `dim_F2 I_varpi=4`, so this span
is the whole local image, not only a lower bound.

Using the exact supported-image annihilator rows from the frozen Q3b
assembly,

```text
00000100,
00101010,
```

gives

```text
W_supported intersect I_varpi
  = span_F2 {01111000, 01100010},
```

where

```text
01111000 = D_lambda,
01100010 = D_i + D_{3+i} + D_{5+i}.
```

Hence the exact intersection dimension is `2`.  The known class `D_i` is
outside `W_supported` because the first annihilator row evaluates to `1`.

## Local Points

Let `K_varpi=Q_2(i)`.  For

```text
d = a+i in {1+i, 3+i, 5+i},
M_d = K_varpi(z),  z^2=d,
```

the absolute polynomial of `z` is

```text
z^4 - 2*a*z^2 + (a^2+1).
```

Each `d` has `2`-adic norm valuation `1`, so this is the totally ramified
degree-four local field with normalized ramification index `e=4`.  The exact
square-lifting fact used by the verifier is

```text
U_{2e+1}=U_9 subset M_d^{*2}.
```

The table uses ascending powers of `z`.

| class | `t=t_0+t_1 z` | square witness `w` | `v_z(w), v_z(g_6(t))` | `v_z(w^2-g_6(t))` |
| --- | --- | --- | --- | --- |
| `D_lambda` | `-3-2z+2z^2` | `-16z+32z^2-8z^3` | `15, 30` | `infinity` |
| `D_{3+i}` | `-7-8z+2z^2+2z^3` | `240+56z+104z^2+240z^3` | `13, 26` | `53` |
| `D_{5+i}` | `1-10z+2z^3` | `16+832z+80z^2+1792z^3` | `16, 32` | `56` |

For `D_{3+i}` and `D_{5+i}`, the exact remainder coefficients of
`w^2-g_6(t)` are respectively

```text
(-3588096, -385024, 1712128, 393216),
(-912670720, -7372800, 268222464, 3047424).
```

The resulting error-over-square valuations are `53-2*13=27` and
`56-2*16=24`, both at least `9`.  Thus the displayed approximate witnesses
give exact local square roots by the `U_9` lemma.  For `D_lambda` the
remainder is exactly zero.  In all three cases `t_1 != 0` and `g_6(t) != 0`,
so the two conjugate finite points are distinct and no infinity or branch
point is being used implicitly.

Let `sigma` be the nontrivial automorphism of `M_d/K_varpi`, and let
`P_d=(t,y)` be the exact point obtained from the square lift.  Define

```text
D_d = [P_d + sigma(P_d) - P_+ - P_-] in J(K_varpi).
```

The leading coefficient of `g_6` is `1`, so the infinity normalization has no
extra squareclass.  The fake evaluation representative is therefore the
exact quadratic norm

```text
u_d(theta) = (theta-t)(theta-sigma(t))
            = theta^2 - 2*t_0*theta + (t_0^2-d*t_1^2).
```

The producer constructs this element in the fixed absolute degree-12 field;
the verifier independently reconstructs its power-basis coordinates and
converts them to the frozen maximal-order basis before using any local
quotient data.

## Exact Localization

The two frozen maximal-order primes above `2` have absolute ramification
indices `4` and `8`, and the Q3a2 primary quotient bases have dimensions `6`
and `10` including their valuation bits.  The exact local squareclass vectors
of `u_d(theta)` in those bases are:

| class | `P_1` vector | `P_2` vector | concatenated product vector |
| --- | --- | --- | --- |
| `D_lambda` | `011010` | `0101000110` | `0110100101000110` |
| `D_{3+i}` | `011000` | `0000011000` | `0110000000011000` |
| `D_{5+i}` | `000010` | `0000110000` | `0000100000110000` |

For each row, the producer stores integral maximal-order numerator and
denominator coordinates satisfying the exact identity

```text
numerator * uniformizer^v = denominator * u_d(theta)
```

when `v>=0` (and the equivalent multiplied identity for `v<0`).  Both
numerator and denominator reduce to units modulo the prime.  The verifier
independently converts each frozen Q3a2 uniformizer from the absolute power
basis to the maximal-order basis and requires exact equality with the local
witness before accepting the reported valuation.  It then
recomputes the primary-quotient inverse by the exact exponent
`2^(2e+1)-1`, checks the quotient residue, and then checks the frozen unit
squareclass coordinate map.  This is exact localization evidence, not a
finite-precision factor display.

The quotient-coordinate map sends each concatenated vector into the frozen
12-dimensional `F_varpi`; the four frozen norm rows vanish.  Applying the
frozen eight-row `H_varpi` kernel basis and its exact coordinate extractor
gives

```text
D_lambda  -> 01111000,
D_{3+i}   -> 00001100,
D_{5+i}   -> 00011000.
```

The accepted Q3a3 class supplies

```text
D_i       -> 01110110.
```

For an explicit independence check, the minor on H-coordinate columns
`(2,4,5,7)` (one-based) is

```text
1101
1110
0010
0110
```

with determinant `1` over `F_2`.  Thus the four local classes are independent.

## Brauer Boundary

This result uses the accepted Q3a3 commutative descent square only for actual
Jacobian divisor classes and their fake evaluations.  It does not identify
`H^1(K_varpi,Q)` with the fake quotient: the Brauer cokernel in the sequence
`1 -> mu_2 -> R -> Q -> 1` remains a separate object, exactly as required by
Q3a3.  No true Selmer, rank, saturation, Q3c-Q4, `i`-twist, other Berry row,
`wl597`, D2, D5, or M3 conclusion is made.

## Artifacts And Validation

The exact producer, serialized payload, verifier, and focused test are:

```text
scripts/theory/berry_sextic_q3b_local_image.sage
docs/codex/tasks/berry-sextic-genus2-classification-20260715/q3b-local-image-payload.json
scripts/theory/berry_sextic_q3b_local_image.py
tests/test_berry_sextic_q3b_local_image.py
```

Reproduction uses the frozen Q3a2 environment directories:

```text
DOT_SAGE=/private/tmp/d19-sage \
SAGE_TMP_DIR=/private/tmp/d19-sage-tmp \
HOME=/private/tmp/d19-sage-home \
TMPDIR=/private/tmp/d19-sage-tmp \
sage -python scripts/theory/berry_sextic_q3b_local_image.sage
python3 scripts/theory/berry_sextic_q3b_local_image.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/test_berry_sextic_q3b_local_image.py -n 1
```
