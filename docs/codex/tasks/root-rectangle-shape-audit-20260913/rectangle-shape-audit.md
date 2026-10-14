# Rectangle Shape Versus The Square Local Obstruction

Updated: 2026-09-13

## Outcome

The [previous 5-adic obstruction](../root-structural-exploration-20260912/rotation-local-audit.md)
does **not** single out exact equal sides. For every rational side ratio
`t` with `t=1 or -1 mod 5`, the full rectangle rotation model has a `Q_5`
point with nonzero side if and only if the rotation coefficients are
5-adic integers. Thus precisely the same local classification holds on an
entire 5-adic neighborhood of the square, including infinitely many unequal
rectangles. This is a proved scope limitation, not a refutation of the
previous theorem.

Outside this shape class there are strict rational examples: the `24 x 7`
rectangle and point `(12,16)` have distances `20,15,15,20` in the paired
order below. Their rotation is `(24/25,7/25)`, whose denominator contains 5.
The `24 x 25` rectangle with the same point has the same distances and puts
the point in the interior. All four distances and both sides are rational.

Exact equality removes a mixed term in the full equation. That identity
locates the equal-side condition but supplies no additional global
restriction by itself. No claim of literature novelty is made.

## Full Rectangle Equation

Let the side lengths be nonzero rationals `L,M`, positive for the geometric
interpretation. Use signed rational distances to the ordered vertices:

```text
a : (0,0)       b : (L,M)
c : (0,M)       d : (L,0)
R=a^2+b^2=c^2+d^2,
q=a^2-b^2,      r=c^2-d^2.
```

Every rectangle satisfies the equal-norm identity. Its remaining exact
compatibility equation is

```text
F_rect = M^2*(q+r)^2 + L^2*(q-r)^2
         -8*L^2*M^2*R +4*L^2*M^2*(L^2+M^2) = 0.
```

The inverse geometry is

```text
x=L/2+(q+r)/(4*L),
y=M/2+(q-r)/(4*M).
```

For `(0,0)` and `(L,M)`, multiplying the squared-distance residual by
`16*L^2*M^2` gives exactly `F_rect`. For the other two vertices it gives
`F_rect+8*L^2*M^2*(a^2+b^2-c^2-d^2)`. Hence the equal-norm and rectangle
equations reconstruct **each** required square, over any characteristic-zero
field. Over the rationals, absolute values of the signed variables are the
geometric distances. No interior restriction is imposed.

## Where Equality Enters

Expanding the same equation gives

```text
(L^2+M^2)*(q^2+r^2) +2*(M^2-L^2)*q*r
 -8*L^2*M^2*R +4*L^2*M^2*(L^2+M^2) = 0.
```

The mixed-term coefficient vanishes exactly at `L^2=M^2`. For positive
sides that means a square. But the term also vanishes when `q*r=0`, even
with unequal sides; these symmetry branches are not discarded.

For a dimensionless view put

```text
T=(L^2+M^2)/2,
epsilon=(L^2-M^2)/(L^2+M^2).
```

For rational nonzero sides the denominator is nonzero, and the equation is

```text
q^2+r^2-2*epsilon*q*r = 4*T*(1-epsilon^2)*(R-T).
```

This is an equivalent rewrite only. The side lifts remain
`L^2=T*(1+epsilon)` and `M^2=T*(1-epsilon)`, both rational squares.
Also `1-epsilon^2=(2*L*M/(L^2+M^2))^2`; these are not free parameters.
In local reduction where `L^2+M^2=0 mod 5`, division by that sum is not
allowed modulo 5: use the undivided equation instead.

## Fixed Shape And Projective Boundary

Fix `t=M/L != 0` and write `L=w, M=t*w`. On `w != 0`, dividing the sixth
degree equation by `w^2` gives the homogeneous quartic

```text
G_t = t^2*(q+r)^2+(q-r)^2
      -8*t^2*R*w^2+4*t^2*(1+t^2)*w^4 = 0.
```

For a fixed rational rotation, also retain
`c=C*a-S*b, d=S*a+C*b, C^2+S^2=1`. Every original rectangle point maps to
this quartic. Keeping `G_t` at `w=0` retains the boundary of this model,
without the extraneous whole component introduced by the factor `w^2`.
No boundary point is claimed to be a nondegenerate rectangle.

If `F_square=q^2+r^2-4*R*w^2+4*w^4`, then

```text
G_t = 2*t^2*F_square
      +(t^2-1)*(4*t^2*w^4-(q-r)^2).
```

This exact identity separates the equal-side equation from its shape
correction. Vanishing of the correction alone is not a new obstruction.

## Uniform Local Comparison

Assume `t` is a 5-adic unit and `t^2=1 mod 5`. Then
`G_t=2*F_square mod 5` for **every** distance tuple and side coordinate.

Necessity: Normalize any nonzero full-model `Q_5` point in all five
coordinates `(a,b,c,d,w)`. If their common norm `R` were divisible by 5,
the equal-norm relations and `G_t=0` would force

```text
a^4+c^4+w^4=0 mod 5.
```

Each fourth power is 0 or 1. All five coordinates would then be divisible
by 5, contradicting normalization. Thus `R` is a unit, and the recovered
rotation `C=(a*c+b*d)/R, S=(a*d-b*c)/R` is integral. This excludes primitive
rotation denominators containing 5, including all projective boundary
points, not just an integral affine chart.

Sufficiency: For integral `C,S`, the norm-one residues are exactly
`(1,0),(-1,0),(0,1),(0,-1)`. At the seed `(a,b,w)=(0,2,1)` we have

```text
G_t=0 mod 5,  dG_t/db=96=1 mod 5.
```

The simple-root Hensel lemma proves exact local solubility with `w=1` for
every such rotation and every such `t`. As in the earlier audit, for
nontrivial rotations one can choose a sufficiently small nonzero `a` in
`5*Z_5` and obtain nonzero distance variables and nonzero `q,r,q-r,q+r`.
This is local solubility, not a rational-point assertion.

Consequently, the completed criterion on this shape domain is again

```text
G_t has a Q_5 point with w != 0  <=>  C,S in Z_5
                               <=>  5 does not divide primitive H.
```

For example every `t_n=1+5/n`, with positive integer `n` prime to 5,
is an unequal positive rational side ratio with this same criterion, and
`t_n` approaches 1 in the ordinary real topology. No finite limit argument
is used to infer a square solution or exclusion.

## Exact Contrast Outside This Domain

For `L=24`, point `(12,16)`, and either `M=7` or `M=25`, the ordered
distances are

```text
(a,b,c,d)=(20,15,15,20),
R=625, q=175, r=-175,
C=(a*c+b*d)/R=24/25,
S=(a*d-b*c)/R=7/25.
```

Indeed `C^2+S^2=1`, `C*a-S*b=15`, and `S*a+C*b=20`.
For `M=7` the point is outside the rectangle; for `M=25` it is inside.
In both cases it lies on the vertical symmetry line. No claim is made
that these examples are generic off-axis points, and the comparison does
not require that claim.

After rational scaling to `L=1`, the point is `(1/2,2/3)`, the ordered
distances are `(5/6,5/8,5/8,5/6)`, and the two heights are `7/24` and
`25/24`. The first height is 3 modulo 5, so its square is -1 modulo 5;
the second has 5-adic valuation 2 and is not a unit. Neither satisfies
the hypothesis of the uniform local comparison above.

For `t^2=-1 mod 5` and `R=0 mod 5`, the undivided closure reduces instead
to `a^2*c^2=0 mod 5`, not an anisotropic three-term fourth-power sum.
This permits the primitive residues of the `24 x 7` witness. A finite
residue alone would not prove existence; here all four rational distances
provide the full exact lift.

No complete local classification for `t=2,-2 mod 5` or nonunit `t` is
claimed. These exact witnesses suffice to show that the obstruction is
shape-dependent but is not specific to equal sides.

## Shape Is Not The Whole Arithmetic Problem

Keeping this particular ordered distance tuple fixed, a square side would
have to satisfy, with `V=w^2`,

```text
V^2-625*V+61250/4=0,
V=(625 +/- 25*sqrt(527))/2.
```

Both roots are positive, but neither is rational since `527=17*31` is not
a square. The reverse map gives real equal-sided configurations carrying
these same rational distances, but their sides are irrational. Rescaling
to the unit square makes the nonzero distances irrational. This is a
fixed-tuple observation, not a statement about all square configurations.

Thus the target is not equal-sided Euclidean geometry alone: it is equal
sides **together with rational metric scale**. Rationality is preserved by
rational similarity factors, not arbitrary real similarity factors. This
is a basic distinction clarified by the comparison, not a newly invented
theory or an exclusion proof for the surviving class.

## Status And Verification

The deliverables are a reversible rectangle model, a proved extension and
scope limitation of the previous local theorem, and two strict rational
rectangle witnesses. The disappearing mixed term is an exact structural
identity, not an independent obstruction. No new numbered checkpoint,
database sweep, new-prime table, or broad parameter search is used.

The [task-local tests](test_rectangle_shape_audit.py) check all four reverse
lifts, side normalization, the shape and deformation identities, the
complete finite residue lemma, all eight shape/rotation residue Hensel
seeds, both geometric examples, and the fixed-tuple square discriminant.

Verification completed: 21 task-local checks and all 14 previous local
rotation checks passed; targeted Ruff passed. The executable check is:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -n 0 docs/codex/tasks/root-rectangle-shape-audit-20260913/test_rectangle_shape_audit.py docs/codex/tasks/root-structural-exploration-20260912/test_rotation_local_audit.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check docs/codex/tasks/root-rectangle-shape-audit-20260913/test_rectangle_shape_audit.py
```

The remaining conceptual question is what additional **global rational**
compatibility, if any, is special to the exact equal-side fiber after all
side and distance square lifts are retained. This task does not supply that
obstruction and does not authorize a new search merely by naming it.
