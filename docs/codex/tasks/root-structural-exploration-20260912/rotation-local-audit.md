# Complete Rotation Lift: The 5-Adic Criterion

Updated: 2026-09-13

## Question And Result

The user selected direct local testing of the second square lift, rather
than database sampling. The input is the
[Hadamard/rotation reduction](hadamard-rotation-audit.md), initially at
`(C,S)=(3/5,4/5)`.

For **every** rational pair `C,S` with `C^2+S^2=1`, the complete homogeneous
rotation quartic has a `Q_5` point with nonzero side if and only if
`C,S` belong to `Z_5`. Equivalently, writing

```text
C=P/H, S=Q/H, gcd(P,Q,H)=1, H>0, P^2+Q^2=H^2,
```

the local criterion is `5 does not divide H`. If `5 divides H`, even the
projective quartic has no `Q_5` point, including at infinity.

This proves exclusion of an infinite parameter class, not global exclusion
of the original problem. It does not establish novelty in the literature.
The remaining rotations all pass this particular local test.

## Full Model And Reverse Lift

Use signed distance variables and a side coordinate `w`:

```text
c=C*a-S*b, d=S*a+C*b,
R=a^2+b^2=c^2+d^2,
q=a^2-b^2, r=c^2-d^2,
F=q^2+r^2-4*R*w^2+4*w^4=0.
```

These are homogeneous equations; distances and side scale together.
For `w != 0` the reverse map is

```text
x=1/2+(q+r)/(4*w^2),
y=1/2+(q-r)/(4*w^2).
```

The squared distances to `(0,0),(1,1),(0,1),(1,0)` are respectively
`(a/w)^2,(b/w)^2,(c/w)^2,(d/w)^2`. Substitution proves each of the four
identities individually. Over `Q`, take absolute values for geometric
distances. No restriction to the interior or to positive `a,b,c,d` is used.

This homogeneous model avoids division by `a`, `G`, or an affine distance
scale. It therefore retains the exceptional charts of the preceding
`m=b/a, Z=a^2` description.

## Primitive Norm Lemma

Let `(a,b,c,d,w)` be any nonzero `Q_5` solution of the full equal-norm and
closure equations. Normalize all five coordinates to `Z_5` so that at
least one is a unit. Then `R=a^2+b^2` is a unit.

Proof: If `R=0 mod 5`, the equal-norm equations give
`b^2=-a^2` and `d^2=-c^2` modulo 5. Consequently

```text
q^2=4*a^4, r^2=4*c^4,
F=4*(a^4+c^4+w^4) mod 5.
```

Every fourth power modulo 5 is 0 or 1. Three such residues can sum to zero
only when all three vanish. Thus `a,c,w` are divisible by 5; so are `b,d`.
This contradicts the normalization. The proof also covers `w=0`, zero
distances, axes, and symmetric positions. In particular `R` cannot be zero
in `Q_5` on any nonzero full-model point.

## Necessity And Sufficiency

For a full point, recover its rotation without losing a square lift:

```text
C=(a*c+b*d)/R, S=(a*d-b*c)/R.
```

The primitive norm lemma makes the denominator a unit and both numerators
integral. Thus `C,S` must be in `Z_5`, proving necessity for all projective
points. For primitive rational `P,Q,H`, this is equivalent to `5 not | H`:
if `5 | H`, the primitive Pythagorean relation forces both `P,Q` to be units
modulo 5.

Conversely, if `C,S` are in `Z_5`, their norm-one residues are exactly
`(1,0),(-1,0),(0,1),(0,-1)`. In all four cases

```text
F(a,b,1) = 2*(a^2-b^2)^2-4*(a^2+b^2)+4 mod 5.
```

At `(a,b)=(0,2)`, `F=0 mod 5` and `dF/db=48=3 mod 5`. The simple-root
Hensel lemma gives an exact `Q_5` solution with `w=1`, proving sufficiency.
This is an infinite-precision existence proof, not survival at a finite
list of moduli.

The local witness is not a rational or real solution. Zero-distance seeds
are not essential for non-D4 rotations: after a signed permutation of
`c,d`, take `C` a unit and `v_5(S)=k>=1`, then fix `a=5^(k+1)` and lift
`b=2 mod 5`. All four distance variables are nonzero. Here `c` has valuation
`k`, `d,b` are units, and `q,r,q-r,q+r` are nonzero. Thus the surviving
local points need not be exceptional axis, diagonal, or midpoint points.

## The Selected Rotation

At `(C,S)=(3/5,4/5)`, set

```text
B=(3*a-4*b)^2-(4*a+3*b)^2,
625*F=625*(a^2-b^2)^2+B^2
      -2500*(a^2+b^2)*w^2+2500*w^4.
```

The primitive integer quartic is

```text
P=(625/2)*F
 =337*a^4+336*a^3*b+478*a^2*b^2-336*a*b^3+337*b^4
  -1250*(a^2+b^2)*w^2+1250*w^4.
```

An invertible change over `Q_5`, `b=2*a+5*t`, gives
`c=-a-4*t, d=2*a+3*t`. After removing the scalar 625, the integral quartic
`J=P(a,2*a+5*t,w)/625` satisfies

```text
J = 2*(a^4+(a-t)^4+w^4) mod 5.
```

The coordinate change is invertible over `Q_5` even though its determinant
is not a 5-adic unit. Normalize **the new** coordinates before reduction.
The Fermat congruence has no primitive solution, so this excludes all
`Q_5` points of this fiber, including rational denominators and `w=0`.

In contrast the same fiber has a `Q_2` point. Holding `a=1,b=3`, use `w=12`
as a seed for the **correct** polynomial `P`:

```text
P(1,3,12)=24143872,       v_2=11,
dP/dw(1,3,12)=8340000,   v_2=5.
```

Since `11 > 2*5`, strong Hensel gives a root with
`v_2(w-12)>=6`, hence `v_2(w)=2` and `w != 0`. All four distance numerators
are nonzero there. This rules out a 2-adic exclusion for this selected
fiber; it does not affect the proved 5-adic exclusion.

## Earlier Projection Witness

The earlier rational projection at `m=-169/505` is preserved. Its two scale
candidates are

```text
Z1=6375625/1819808, Z2=6375625/5269842.
```

Both have `v_5=4`, but the units after division by `5^4` are respectively
2 and 3 modulo 5, neither a quadratic residue. Thus neither scale is even
a square in `Q_5`. The earlier failure is explained by the uniform local
theorem, not merely two unrelated integer factorizations.

## What The Structure Explains

At a prime dividing the rotation denominator, a primitive rational rotation
forces the common norm toward zero modulo that prime. The full square-side
condition then forces a three-term fourth-power congruence. At 5 this
congruence is anisotropic and closes the second lift.

For an odd prime `p | H`, the same necessary congruence is
`a^4+c^4+w^4=0 mod p`. It is not automatically obstructive at other primes:
`1^4+2^4+4^4=0 mod 13`. Nor does a finite-field Fermat point by itself
establish a full lift at that prime.

Rotations such as `(5/13,12/13)` survive the complete 5-adic test, despite
being non-D4. Therefore 5-adic integrality is a real restriction on a
parameter, not proof that only finitely many rotations remain. No assertion
about other local fields, rational points, ranks, Selmer groups, or a
local-to-global obstruction for the surviving class follows.

## Verification And Corrections

The task-local [exact tests](test_rotation_local_audit.py) verify the four
reverse lifts symbolically, the coefficient normalization, the invertible
5-adic coordinate change, the full finite residue lemma, every integral
rotation residue's simple Hensel seed, the earlier scale residues, and the
2-adic Hensel inequalities using an exact derivative.

Earlier scratch modular probes in this conversation used `-250` instead of
`-2500` in `625*F`; all their modular survival claims are discarded. Their
central finite difference was not an exact quartic derivative and was not
a Hensel proof. Neither error was in the preserved projection witness.

Verification completed: all 14 exact pytest checks passed; targeted Ruff
passed. Run the checks with:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -n 0 docs/codex/tasks/root-structural-exploration-20260912/test_rotation_local_audit.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check docs/codex/tasks/root-structural-exploration-20260912/test_rotation_local_audit.py
```

This selected local audit is complete. Further work requires a specific
question about the surviving class; repeating 5-adic tests on more rotations
cannot strengthen the criterion just proved. No database sampling, broad
parameter search, or new numbered checkpoint was used for this conclusion.
