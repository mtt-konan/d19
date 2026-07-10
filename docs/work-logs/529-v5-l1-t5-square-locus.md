# v_5 L=1 T=5 Square-Locus Audit

## Question

For the already selected `wl528` prototype

```text
support=v_5|L=1|T=5|d=(5,1,5)
```

represented in `wl495` by

```text
AA_A1_B4_v_5_m_tail_refresh_candidate
BB_A4_B1_v_5_m_tail_refresh_candidate
```

can the remaining `wl528` specialization gap be closed for this one family by
an exact analysis of the square-locus

```text
s^2 = (N^2+16)(M^2+16)
```

under the required nonexceptional positivity condition

```text
|t| < 5
```

with

```text
t = y*(r^2+20)/(4*r*(r^2-20))
N = (5+t)/2
M = (5-t)/2
```

This work touches only the single `wl528` prototype square-locus layer. It does
not execute shell 11, compute new supports, touch another cover family, test
new ambient `C_d` solubility, run broad rank/Selmer diagnostics, use the old
package-`x` / `S~` bridge, or claim theorem-level progress.

## Exact Identity

For the opposite leg-4 product

```text
P = (N^2+16)(M^2+16)
```

the centered-even parameter gives the exact identity

```text
16P = (t^2+39)^2 + 6400
```

equivalently

```text
U^2 = t^4 + 78*t^2 + 7921
```

with

```text
U = 4s.
```

So the rational square-specialization problem reduces to the genus-one quartic

```text
D: U^2 = t^4 + 78*t^2 + 7921.
```

This quartic is squarefree, hence smooth of genus one.

## Over The wl528 Quartic

`wl528` gives

```text
y^2 = 5*r^4 - 264*r^2 + 2000.
```

Clearing denominators in the `t`-map gives

```text
16*r^2*(r^2-20)^2*t^2 = (r^2+20)^2*(5*r^4-264*r^2+2000).
```

Thus any rational square specialization on the prototype quartic must map to a
rational point on `D`.

## Elliptic Quotient

The square-locus quartic has the smooth intersection-of-quadrics model

```text
V*Z = T^2 + 39*Z^2
U^2 = V^2 + 6400*Z^2
```

and admits a degree-two map to the elliptic curve

```text
E: Y^2 = X^3 + 78*X^2 + 7921*X
```

by

```text
X = t^2
Y = t*U.
```

The `wl529` script checks this map symbolically.

The elliptic curve is a quotient used to classify rational points; the map is
not claimed to be a birational equivalence. A rational point on `D` maps to a
rational point on `E` whose `X`-coordinate is the square `t^2`.

## Rational Points

The `wl529` script then uses a single-curve Sage certificate for `E`:

```text
rank(E(Q)) = 0
E(Q)_tors ~= Z/4Z
E(Q) = {O, (0,0), (89,1424), (89,-1424)}.
```

Any rational point on `D` maps to `E(Q)` with

```text
X = t^2
```

a rational square. Among the finite rational points on `E(Q)`, the only square
`X`-value is

```text
X = 0.
```

Therefore the affine rational points on `D` are exactly

```text
(t,U) = (0,89), (0,-89).
```

This is the pointwise part that `wl528` did not supply. Divisor parity only
proves that the function-field element is generically nonsquare. By itself it
cannot rule out every rational specialization landing on a square value.

## No Lift To The Prototype Quartic

To finish the one-family square-locus audit, `wl529` checks whether

```text
t = 0
```

has a rational preimage on the `wl528` quartic. Writing `x = r^2`, the cleared
denominator relation becomes

```text
5*x^2 - 264*x + 2000 = 0.
```

The script computes its discriminant as

```text
29696 = 2^10 * 29
```

which is not a rational square. Hence `t=0` has no rational lift to the
prototype quartic. The discriminant, its factorization, and the substitution
`x=r^2` are executable certificate checks rather than recorded booleans.

So there is no rational point on the selected `wl528` prototype with

```text
|t| < 5
```

for which `(N^2+16)(M^2+16)` is a rational square.

## What Is Proved Here

For this one selected prototype only:

- `wl528` still supplies the generic function-field nonsquare certificate.
- `wl529` closes the remaining specialization gap in the required positivity
  domain by a genus-one rational-point certificate.
- Every rational point on the prototype quartic satisfying the nonexceptional
  centered-even positivity condition `|t|<5` has opposite-side product
  nonsquare.
- Therefore this prototype has no nonexceptional rational point that is both
  positivity-compatible and opposite-side square-compatible.

## What Remains Unproved

This does **not** prove:

- a divisor-parity certificate on the prototype;
- a uniform cover-family theorem;
- any statement for another cover family;
- a theorem-level Selmer upper bound;
- rank zero;
- `Sha[2]=0`;
- family exclusion.

The one-family square-locus question is closed here. The wider uniform theorem
is outside this stop condition.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.json
```

with:

```text
status = ok
work_log = wl529
object_layer = single_cover_family_square_specialization_locus
square_locus_constructed_here = true
divisor_parity_only_proves_generic_nonsquareness = true
genus_one_rational_point_certificate_proved_here = true
nonexceptional_positive_square_specialization_absent = true
one_family_positive_square_obstruction_proved_here = true
uniform_cover_family_obstruction_proved_here = false
advance_to_next_cover_family = false
advance_to_next_roadmap_step = false
stop_after_current_task = true
```

## Boundary

This work-log stops after this one `v_5|L=1|T=5|d=(5,1,5)` square-locus
analysis. It does not advance to another family or roadmap step.
