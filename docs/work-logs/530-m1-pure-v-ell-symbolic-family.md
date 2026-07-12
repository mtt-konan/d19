# M1 Pure v_ell Symbolic Family

## Question

For the infinite pure family

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell)
```

with `ell` an odd prime, can the exact symbolic complete-`d` formulas, one
rational function-field chart, the centered-even `t,N,M` maps, the
opposite-side square product, and the resulting square-specialization elliptic
family all be derived and verified so that specializing `ell=5` recovers
`wl528` and `wl529` exactly?

This touches only the symbolic cover-family / function-field derivation layer
for this one infinite support family. It does not enter M2, does not classify
the rational points of the general square-locus elliptic fibers, does not prove
a uniform cover-family obstruction, and does not claim theorem-level Selmer,
rank, `Sha[2]`, or family-exclusion progress.

## Input

Immediate checked inputs:

```text
wl528  first explicit v_5 L=1 T=5 function-field prototype
wl529  closed v_5 square-locus audit
```

Structural symbolic input already established elsewhere:

```text
p = 8*L^2 - 2*T^2
sqrt_q = T^2 + 4*L^2
```

Here `L=1`, `T=ell`, so:

```text
p = 8 - 2*ell^2
sqrt_q = ell^2 + 4
q = (ell^2 + 4)^2.
```

The touched object layer remains:

```text
complete d-coordinate C_d cover
-> symbolic function-field chart
-> centered-even N,M maps
-> opposite-side square-specialization family
```

not old package-`x` / `S~`, not point classification on every fiber, and not
the theorem-level `Sel_2(E_L/Q)` object.

## Complete-d Family

For `d=(ell,1,ell)`, the complete-`d` cover equations are:

```text
X - (2*ell^2 - 8) = ell*u_minus_p^2
X - (2*ell^2 + 8) = u_pos_2sqrt_q^2
X + (2*ell^2 + 8) = ell*u_neg_2sqrt_q^2
```

Hence:

```text
ell*u_minus_p^2 - u_pos_2sqrt_q^2 = 16
u_minus_p^2 - u_neg_2sqrt_q^2 = -4*ell.
```

The second relation gives:

```text
u_neg_2sqrt_q^2 - u_minus_p^2 = 4*ell.
```

On the chart

```text
r = u_neg_2sqrt_q + u_minus_p
```

with exceptional denominators

```text
r != 0
r^2 != 4*ell
```

one gets:

```text
u_minus_p = (r^2 - 4*ell)/(2*r)
u_neg_2sqrt_q = (r^2 + 4*ell)/(2*r).
```

Writing

```text
y = 2*r*u_pos_2sqrt_q
```

and substituting into `ell*u_minus_p^2 - u_pos_2sqrt_q^2 = 16` yields the exact
quartic chart:

```text
Q(ell)(r,y)/(y^2 - (ell*r^4 - 8*(ell^2+8)*r^2 + 16*ell^3)).
```

So the symbolic cover maps are:

```text
u_minus_p = (r^2 - 4*ell)/(2*r)
u_pos_2sqrt_q = y/(2*r)
u_neg_2sqrt_q = (r^2 + 4*ell)/(2*r)
X = 2*ell^2 - 8 + ell*((r^2 - 4*ell)/(2*r))^2
Y = ell*y*(r^4 - 16*ell^2)/(8*r^3).
```

The quartic discriminant is:

```text
disc_r(ell*r^4 - 8*(ell^2+8)*r^2 + 16*ell^3) = 2^28*ell^4*(ell^2+4)^2.
```

So for every odd prime `ell`, this quartic model is smooth.

## Centered-Even Maps

Using the centered-even pullback:

```text
t = Y/(2*(X+p))
N = (T+t)/2
M = (T-t)/2
```

with `T=ell`, the symbolic formulas become:

```text
t = y*(r^2 + 4*ell)/(4*r*(r^2 - 4*ell))
N = (ell+t)/2
M = (ell-t)/2.
```

The positivity condition for the source side is exactly:

```text
N > 0 and M > 0  <=>  |t| < ell
```

because `ell>0`.

Since the source leg is `L=1`, the source-side square identity remains:

```text
(N^2+1)(M^2+1) = (z/4)^2
```

with `z = X/2 - t^2`.

## Opposite-Side Product

For the pure `v_ell` family, the opposite leg is:

```text
ell - 1.
```

So the opposite-side product is:

```text
(N^2+(ell-1)^2)(M^2+(ell-1)^2).
```

Substituting `N=(ell+t)/2`, `M=(ell-t)/2` gives the exact closed identity:

```text
16*(N^2+(ell-1)^2)(M^2+(ell-1)^2)
  = (t^2 + 5*ell^2 - 8*ell + 4)^2 - 4*ell^2*t^2.
```

Equivalently:

```text
(N^2+(ell-1)^2)(M^2+(ell-1)^2)
  = ((t^2 + 5*ell^2 - 8*ell + 4)^2 - 4*ell^2*t^2)/16.
```

## Square-Specialization Family

If the opposite-side product is a rational square, writing `U=4*s` gives the
symbolic square-locus quartic:

```text
U^2 = t^4 + (6*ell^2 - 16*ell + 8)*t^2 + (5*ell^2 - 8*ell + 4)^2.
```

The quartic discriminant is:

```text
2^16*ell^4*(ell-1)^4*(5*ell^2 - 8*ell + 4)^2.
```

Since `ell` is an odd prime and `5*ell^2 - 8*ell + 4` has discriminant `-16`,
this is nonzero for every odd prime `ell`. Hence the square-locus quartic is
smooth for every odd prime `ell`.

The degree-two elliptic quotient family is:

```text
Y^2 = X^3 + (6*ell^2 - 16*ell + 8)*X^2 + (5*ell^2 - 8*ell + 4)^2*X
```

via

```text
X = t^2
Y = t*U.
```

The discriminant of its cubic right-hand side is:

```text
-64*ell^2*(ell-1)^2*(5*ell^2 - 8*ell + 4)^4
```

which is also nonzero for every odd prime `ell`, so the displayed Weierstrass
model is nonsingular. This is the cubic polynomial discriminant, not the
normalized Weierstrass discriminant.

This is the exact symbolic elliptic family required for M1. No rational-point
classification of this family is attempted here.

## Exact ell=5 Recovery

Specializing `ell=5` recovers `wl528` and `wl529` exactly:

```text
y^2 = 5*r^4 - 264*r^2 + 2000
t = y*(r^2+20)/(4*r*(r^2-20))
N = (5+t)/2
M = (5-t)/2
(N^2+16)(M^2+16)
U^2 = t^4 + 78*t^2 + 7921
Y^2 = X^3 + 78*X^2 + 7921*X.
```

The SymPy audit checks this specialization exactly rather than by pattern
matching.

## Certificate

The executable certificate is:

```text
scripts/theory/audit_closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family.py
tests/test_closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family.py
```

The audit verifies:

```text
- all symbolic cover / map / product identities in the function field;
- the square-locus quartic identity;
- the degree-two elliptic quotient identity;
- the quartic discriminant and elliptic right-hand-side cubic discriminant;
- exact specialization to the wl528/wl529 `ell=5` checkpoint.
```

Default result artifact:

```text
results/closure_quotient_rank_zero_aa_bb_wl530_m1_pure_v_ell_symbolic_family.json
```

with:

```text
status = ok
work_log = wl530
symbolic_complete_d_family_derived_here = true
function_field_chart_derived_here = true
rational_n_m_maps_derived_here = true
opposite_side_square_product_derived_here = true
square_specialization_elliptic_family_derived_here = true
exact_ell_5_recovery_verified_here = true
uniform_cover_family_obstruction_proved_here = false
m2_entered_here = false
stop_after_m1 = true.
```

## What Is Proved Here

For every odd prime `ell`, at the symbolic M1 derivation level only:

- the exact pure-`v_ell` complete-`d` family formulas for `L=1,T=ell,d=(ell,1,ell)`;
- one exact rational function-field chart and its exceptional denominators;
- the centered-even `t,N,M` pullback formulas;
- the exact opposite-side product formula;
- the exact square-locus quartic and degree-two elliptic quotient family;
- exact recovery of the `ell=5` formulas from `wl528` and `wl529`.

## What Remains Unproved

This does **not** prove:

- that the opposite-side product is nonsquare for every rational specialization
  in the general family;
- rational-point classifications for the symbolic elliptic family;
- the M2 family-level square-locus obstruction;
- a uniform cover-family theorem;
- a divisor-parity or specialization-survival theorem for all odd primes;
- a complete Selmer upper bound;
- `rank(E_L)=0` as a family theorem;
- `Sha(E_L)[2]=0`;
- family exclusion.

## Next Gate

The next narrow gate would be:

```text
M2_general_pure_v_ell_square_locus_analysis
```

meaning a family-level analysis of the rational square-specialization locus or
the first exact obstruction to such an analysis.

That gate is **not** entered here.
