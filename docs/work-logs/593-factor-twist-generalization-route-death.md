# wl593 Factor-Twist Generalization Route Death

## Scope

This checkpoint encodes Outcome 3 using only the imported certificates
`wl587`, `wl589`, `wl590`, `wl591`, and `wl592`.  It compares the two frozen D0
representatives and the exact local-image certificates already proved for
them.  It does not create a family-level model or add another local row.

The two D0 source bases are both fixed instances over

```text
Spec(Q)
```

with scopes

```text
support=u_7|L=7|T=9|d=(7,7,1), R^2=P_op only
support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85), R^2=P_op only
```

The executable certificate compares the complete imported parameter,
function-field, factor-function, cleared-factor-equation, and bad-fiber
support fields.  The displayed data already show the dependence:

```text
pure u_7:
  parameters: L=7, T=9, p=230, q=76729, sqrt_q=277,
              d=(7,7,1)
  source: W^2=7*r^4+2864*r^2+87808
  t: W*(r^2-112)/(4*r*(r^2+112))
  F_plus=(t^2+18*t+97)/4
  F_minus=(t^2-18*t+97)/4
  bad-prime support: [2,3,5,7,53,97,277]

mixed u_3+v_5+w_17:
  parameters: L=3, T=10, p=-128, q=18496, sqrt_q=136,
              d=(15,51,85)
  source: W^2=289*r^4-408*r^3+274*r^2-120*r+25
  t: -17*(17*r^2-20*r+5)*W /
     ((17*r^2-5)*(17*r^2-17*r+5))
  F_plus=(t^2+20*t+296)/4
  F_minus=(t^2-20*t+296)/4
  bad-prime support: [2,3,5,7,17,29,37]
```

Thus the coefficient, source, factor, and bad-prime data are not shared
inputs.  The script checks this from the imported certificate payloads rather
than treating the displayed formulas as a new symbolic family.

## Local-image quantifier

For each frozen representative `j`, selected prime `p`, and squareclass
`[d]` in `Q_p^*/Q_p^{*2}`, the exact local image is

```text
I_{p,j} = { [d] : there exists a Q_p-point
  (c,a_plus,a_minus,R) on the already audited complete normalized
  factor-cover charts, with d in Q_p^*, such that

  F_plus(c)  = d*a_plus^2,
  F_minus(c) = d*a_minus^2,
  R          = d*a_plus*a_minus }.
```

The quantifier ranges over the complete local charts already used by
`wl590`-`wl592`: finite source points, denominator-pole charts, projective
infinity charts, factor-zero charts, and the `R=0` boundary.  At a pole the
equalities mean the corresponding normalized valuation statement obtained
from the frozen cleared equations; no new chart is introduced here.  A
factor-zero equality is literal and permits the corresponding `a` to be
zero.

The real positivity interval and the exact AA+BB source-product lift are not
silently inserted into this p-adic quantifier.  They remain global boundaries:

```text
pure u_7:          -9<t<9,
                   (N^2+49)*(M^2+49)=(Z/4)^2,
                   source leg=7, opposite leg=2;

mixed u_3+v_5+w_17:
                   -10<t<10,
                   (N^2+9)*(M^2+9)=(Z/4)^2,
                   source leg=3, opposite leg=7.
```

The fixed-cover coordinate is retained throughout.  In particular, the
normalized roots satisfy

```text
R=d*a_plus*a_minus,
R^2=(N^2+4)*(M^2+4)       for pure u_7,
R^2=(N^2+49)*(M^2+49)     for the mixed representative.
```

## Imported local results

The shared `p=5` certificate gives different images on the two fixed
representatives:

```text
I_{5,u} = empty set,
I_{5,m} = {[5]}.
```

This disagreement is itself fixed-representative evidence.  It is not a
common local exclusion and it supplies no parameterized coefficient lemma.

The mixed chain is also tied to the frozen `wl589` coefficient data:

```text
p=5:  survivors = [5, 3045, 66045, 91205]
p=7:  I_{7,m} = {[1]}, so only 91205 remains;
      its class is [1]
p=17: I_{17,m} = {[u]}, while [91205]=[17u], so 91205 is excluded.
```

`wl591` quantifies only over the complete normalized `Q_7` factor-cover
charts of the frozen mixed source.  `wl592` quantifies only over the complete
integral, negative-valuation, and infinity charts of that same frozen mixed
source over `Q_17`.  Neither certificate proves a pure-family image at those
primes, and neither introduces a family parameter.

## Boundary retention

The executable checks retain the prior exceptional boundaries rather than
replacing them with the regular residue rows:

- `wl590`: all `p=5` valuation and residue strata, poles, projective
  boundaries, factor-zero branches, Hensel inclusion, fixed-cover `R`, and
  frozen AA+BB maps;
- `wl591`: complete affine source strata, both infinity disks, `D/A`
  denominator branches, normalized factor-zero and zero-value branches,
  `R=0`, Hensel inclusion, fixed-cover `R`, positivity, and exact AA+BB lift;
- `wl592`: integral and negative-valuation/infinity strata, `D/A` poles,
  factor-zero and `R=0` branches, zero-value branches, Hensel inclusion,
  fixed-cover `R`, positivity, and exact AA+BB lift.

No individual factor-square condition is added to AA+BB.  The local image is
used only as the necessary local condition for a constant factor twist.

## Outcome 3

The two D0 inputs have different fixed coefficients, source and factor maps,
and bad-prime supports.  Their `p=5` local images disagree.  The later mixed
`p=7,p=17` deletions are a chain for the single frozen `wl589` instance, not a
uniform statement over the cover families.  Therefore the current
fixed-representative factor-twist local-image mechanism cannot be promoted
from these fixed inputs alone; it requires new parameterized family-level
coefficient/local-image input.

This is not a claim that all relative 2-descent is impossible.  It is not a
family exclusion, a Selmer claim, a rank computation, a rational-point
search, D2, or D5 result.  No new family, prime, table, equivalent model, or
quotient is added.

## Strict check

```text
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/theory/aa_bb/test_wl593_factor_twist_generalization_route_death.py

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/aa_bb/wl593_factor_twist_generalization_route_death.py \
  tests/theory/aa_bb/test_wl593_factor_twist_generalization_route_death.py

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/aa_bb/wl593_factor_twist_generalization_route_death.py \
  --strict
```

The strict output is exactly:

```text
status=ok
work_log=wl593
ready=True
accepted_outcome=route_death_certificate
violations=[]
```
