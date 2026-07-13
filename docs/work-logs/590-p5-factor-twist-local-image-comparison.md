# wl590 p=5 Factor-Twist Local Image Comparison

## Scope and result

This worklog resolves only the selected shared `p=5` gate for the frozen
`wl587` pure-`u_7` cover and frozen `wl589` mixed
`u_3+v_5+w_17` cover. The source curves, factor radicands, complete-`d`
coordinates, and AA+BB maps are read-only inputs.

Use the local squareclass basis

```text
Q_5^*/Q_5^*2 = {[1], [u], [5], [5u]},
```

where `u` is any unit whose residue is a nonsquare modulo `5`.

The exact local images are

```text
I_{5,u} = empty set,
I_{5,m} = {[5]}.
```

## Frozen normalization and lift maps

For `wl587`, keep

```text
W^2 = 7*r^4 + 2864*r^2 + 87808,
t = W*(r^2-112)/(4*r*(r^2+112)),
N=(9+t)/2, M=(9-t)/2,
F_plus=(t^2+18*t+97)/4,
F_minus=(t^2-18*t+97)/4.
```

The frozen cleared radicands satisfy exactly, in the source function field,

```text
J_plus  = (2*T_denominator)^2*F_plus,
J_minus = (2*T_denominator)^2*F_minus,
T_denominator = 4*r*(r^2+112).
```

Consequently the normalized factor variables are
`a_plus=s_plus/(2*T_denominator)` and
`a_minus=s_minus/(2*T_denominator)`, and the fixed-cover map is

```text
R = d*a_plus*a_minus,
R^2 = (N^2+4)*(M^2+4).
```

This `R` is the fixed-cover coordinate. It is not the separate cleared
polynomial coordinate denoted `rho` in the D0 chart.

The exact pure AA+BB conditions remain

```text
(N^2+49)*(M^2+49) = (Z/4)^2,
-9 < t < 9,
source leg = 7, opposite leg = 2.
```

For `wl589`, keep

```text
W^2 = 289*r^4 - 408*r^3 + 274*r^2 - 120*r + 25,
t = -17*(17*r^2-20*r+5)*W /
    ((17*r^2-5)*(17*r^2-17*r+5)),
N=(10+t)/2, M=(10-t)/2,
F_plus=(t^2+20*t+296)/4,
F_minus=(t^2-20*t+296)/4.
```

Again the frozen cleared radicands satisfy exactly

```text
J_plus  = (2*T_denominator)^2*F_plus,
J_minus = (2*T_denominator)^2*F_minus,
T_denominator = (17*r^2-5)*(17*r^2-17*r+5).
```

The normalized variables and fixed-cover map are the same, while the exact
mixed AA+BB conditions remain

```text
(N^2+9)*(M^2+9) = (Z/4)^2,
-10 < t < 10,
source leg = 3, opposite leg = 7.
```

The strict certificate checks both identities and retains these maps without
introducing a new model.

## Pure-u_7 exclusion

The source has good reduction at `5`:

```text
f(r) = 2*(r^2-2*r-2)*(r^2+2*r-2) mod 5.
```

Both quadratic factors have nonsquare discriminant modulo `5`, so there is
no source point with `r=0 mod 5`. The infinity equation has leading
squareclass `7=2 mod 5`, also nonsquare. The two possible finite `t` poles
are excluded because `r=0` has no source point and `r^2+112=0` would require
`r^2=3 mod 5`.

The complete affine source residue table has exactly these eight rows. Every
row has five smooth lifts modulo `25`, and the displayed `t mod 25` value is
independent of the lift:

```text
(r,W) mod 5       t mod 25
(1,2)                14
(1,3)                11
(2,1)                14
(2,4)                11
(3,1)                11
(3,4)                14
(4,2)                11
(4,3)                14
```

Write `H_plus=t^2+18*t+97` and
`H_minus=t^2-18*t+97`. Direct congruence gives

```text
t = 11 mod 25:  v_5(H_plus)=0, v_5(H_minus)=1,
t = 14 mod 25:  v_5(H_plus)=1, v_5(H_minus)=0.
```

The denominator `4` is a square unit, so the same valuation pairs hold for
`F_plus,F_minus`. A point on a constant factor twist requires

```text
[F_plus] = [d] = [F_minus]
```

and hence equal valuation parity. The two rows contradict this.

The factor-zero branches are also closed exactly. The primitive resultant of
`W^2-f(r)` and either `J_plus` or `J_minus` has no root modulo `25`; the
factor-zero resultant is disjoint from the pole divisor. Therefore no omitted
factor-zero point can change the valuation argument. Hence

```text
I_{5,u} = empty set.
```

## Mixed-family image

The mixed source has the reduction `-r^2*(r-1)^2 mod 5`. All source strata
are included as follows.

### Regular affine strata

For `r mod 5` in `{2,3,4}`, the exact residue table is

```text
(r,W) mod 5       t mod 25
(2,1)                17
(2,4)                 8
(3,2)                 8
(3,3)                17
(4,1)                17
(4,4)                 8
```

Each row has five smooth lifts modulo `25`.

### The r=5*x chart

For `r=5*x, W=5*y`, use

```text
g(x)=1-24*x+274*x^2-2040*x^3+7225*x^4,
y^2=g(x),
t=-17*(85*x^2-20*x+1)*y /
   ((85*x^2-1)*(85*x^2-17*x+1)).
```

When `x=3 mod 5`,

```text
g(3+5*z) = 15 mod 25,
```

which is not a square modulo `25`; this is the singular source branch and
has no `Q_5` point. The eight remaining `(x,y) mod 5` rows have five lifts
each and give

```text
(x,y) mod 5       t mod 25
(0,1)                17       (0,4)                 8
(1,1)                 8       (1,4)                17
(2,2)                17       (2,3)                 8
(4,2)                 8       (4,3)                17
```

### r=1, poles, and projective boundary

For `r=1+5*x`, `f(r)/5=2 mod 5`; thus this branch has no source point.

The denominator branch `D=17*r^2-5=0` would require
`v_5(r^2)=1`, impossible in `Q_5`. For
`A=17*r^2-17*r+5=0`, reduction gives either `r=1 mod 5` or
`r=5*x` with `x=3 mod 5`; both branches were just excluded. Thus every
`Q_5` pole branch is empty.

The two projective infinity disks are retained. With `z=1/r` and
`v=W/r^2`, they satisfy

```text
v^2=289-408*z+274*z^2-120*z^3+25*z^4,
```

and have `v=2 or 3 mod 5`. Each has five lifts modulo `25`, giving
`t=8 or 17 mod 25`, respectively. The `r=0` points are already included in
the `r=5*x` chart and are not poles after normalization.

Therefore every non-pole mixed source point has

```text
t = 8 or 17 mod 25.
```

### Valuation exclusion outside factor-zero

Put `H_plus=t^2+20*t+296` and
`H_minus=t^2-20*t+296`. For the two possible residue classes,

```text
t = 8 mod 25:
    v_5(F_plus)=1 and F_plus/5 is a square unit;
    v_5(F_minus)>=2.

t = 17 mod 25:
    v_5(F_minus)=1 and F_minus/5 is a square unit;
    v_5(F_plus)>=2.
```

If both factor values have squareclass `[d]`, the high-valuation factor must
have odd valuation. The low factor then forces

```text
v_5(d)=1 and the unit part of d is a square,
```

so `[d]=[5]`. If the high valuation is even, the two parity classes differ
and the twist is impossible.

### Factor-zero branches

Unlike the pure family, the mixed factor-zero branch is locally present. Let
`E(r)` be the primitive resultant of `W^2-f(r)` and `J_plus`. Its exact
reduction is

```text
E(r) = 2*r^8*(r-2)*(r+1)*(r+2)
       *(r^2-2*r-1)*(r^2+2*r-2) mod 5,
E'(2)=1 mod 5.
```

Writing `J_plus=a(r)*W+b(r)`, both `a` and `b` are divisible by `5`, while
`a/5` is a unit at `r=2`. Hensel therefore gives a `Q_5` root of `E`, and
`W=-b/a` gives a source point with `J_plus=0`. The `J_minus` branch follows
from `W -> -W`.

At `F_plus=0`, one has `F_minus=-10*t`; at `F_minus=0`, one has
`F_plus=10*t`. The factor-zero roots have `t=2 or 3 mod 5`, so the nonzero
factor divided by `5` is `1 or 4 mod 5`, a square unit. The zero factor is
represented by `s=0`. Both factor-zero orientations therefore have common
class `[5]`, and they add no other local class.

### Inclusion of [5]

Take the regular source disk with `r=4`. The unique Hensel lift of
`W^2=f(4)` with `W=1 mod 5` has

```text
W = 276 mod 625,
t = 67 mod 625.
```

For `t=67 mod 625`,

```text
H_plus/5^3 = 4 mod 5,
H_minus/5 = 4 mod 5.
```

After dividing by the square unit `4`, both `F_plus/5` and `F_minus/5`
are `Q_5` squares (the extra `5^2` in `F_plus/5` is itself a square).
Hensel lifting of the two square roots gives

```text
J_plus = 5*s_plus^2,
J_minus = 5*s_minus^2.
```

The denominator is a `5`-adic unit at `r=4`, so the exact normalized map
`a_plus=s_plus/(2*T_denominator)`, `a_minus=s_minus/(2*T_denominator)`,
`rho=5*a_plus*a_minus` gives the frozen fixed-cover point. Hence

```text
I_{5,m} = {[5]}.
```

## Named D0 representatives

The exact `Q_5` classes and decisions are:

```text
pure-u_7:
  [1]  : 1, 14681, 107961, 564249                         delete all
  [u]  : 97, 1113, 5817, 1424057                          delete all
  [5]  : 105, 25705, 134345, 1541505                      delete all
  [5u] : 265, 1385, 10185, 149525985                      delete all

mixed-u_3+v_5+w_17:
  [1]  : 21, 29, 629, 383061                             delete
  [u]  : 37, 357, 493, 22533                              delete
  [5u] : 85, 3885, 5365, 51765                            delete
  [5]  : 5, 3045, 66045, 91205                            survive
```

No prime other than `5` was processed. The finite residue tables are complete
congruence strata followed by Hensel arguments; they are not bounded searches
for rational points.

## Verification

```text
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/theory/aa_bb/test_wl590_p5_factor_twist_local_image_comparison.py
3 passed

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/aa_bb/wl590_p5_factor_twist_local_image_comparison.py \
  tests/theory/aa_bb/test_wl590_p5_factor_twist_local_image_comparison.py
All checks passed!

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/aa_bb/wl590_p5_factor_twist_local_image_comparison.py \
  --out /private/tmp/wl590-p5.json --strict
status=ok
work_log=wl590
ready=True
violations=[]
```

This closes the selected shared-`p=5` local-image gate only. It does not
complete D1, enter D2, process another prime, compute ranks or rational
points, reopen `wl535`, or modify `wl587`/`wl589`.
