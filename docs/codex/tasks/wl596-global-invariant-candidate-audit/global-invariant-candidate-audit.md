# Global Invariant Candidate Audit

Status: complete.

Base commit:

```text
9d817e1
```

The audit starts from the exact realized HRL evaluation in `wl596` and uses
only its strict positive divisor-pair system. It does not add a numbered
checkpoint, alter `wl587`-`wl596`, run a prime table, or use formal twists,
rank, Selmer, D2, D5, or M3.

## Outcome

```text
global_invariant_candidate_space_exhausted
```

HRL should pause. None of the three declared candidate classes removes an
exact degree of freedom from the closure-compatible divisor-pair set. This is
not a finite-support theorem and not an infinite-support family.

## Exact Object

For primitive positive `Abar>Bbar`, put

```text
s=Abar+Bbar,  r=Abar-Bbar,  Delta_bar=s*r,
F(q)=((q^2-s^2)*(q^2-r^2))/(4*q^2).
```

The quantified set is the set of pairs `(q_1,q_2)` with

```text
q_i | Delta_bar, q_i>0, q_i>=s,
q_i = Delta_bar/q_i (mod 2), F(q_i)=U_i^2,
```

where `U_i` are nonnegative integers and one of

```text
U1+U2=s, U1+U2=r,
U1-U2=s, U2-U1=s, U1-U2=r, U2-U1=r
```

holds. The exact class remains

```text
[H_RL]=[epsilon1*epsilon2*q1*q2*Delta_bar^e],
e=1 iff the two relative lift signs differ.
```

This retains the `T=A+B` and physical `T=|A-B|` branches, positive square
`x=t^2`, real sum and ordered-difference intervals, all four radical lifts,
primitive denominators, shared gcds, `p=2`, and every `wl596` midpoint,
endpoint, factor-zero, infinity, collision, and denominator chart.

## 1. Involution

Let `I(q)=Delta_bar/q`. Direct cancellation gives

```text
F(I(q))=F(q),  I(I(q))=q.
```

Hence all six closure equations, which depend on a lift only through `U_i`,
are unchanged if a formal source root is reflected and the same nonnegative
`U_i` is chosen. This creates no new closure coupling. The product changes as
follows:

```text
q1*q2 -> Delta_bar*q2/q1       under I(q1),
q1*q2 -> Delta_bar*q1/q2       under I(q2),
q1*q2 -> Delta_bar^2/(q1*q2)   under both,
```

so the single-reflection ratio is `[Delta_bar]` and the double-reflection
ratio is square. More importantly, the reflection is not an involution of the
strict positive domain: if `q>=s` and `s>r>0`, then

```text
0 < I(q) <= Delta_bar/s = r < s
```

with equality only at `q=s`. Thus an interior divisor point leaves the
domain. `q=s` maps to the `q=r` factor-zero/source-sign boundary with `U=0`;
`q=0` and infinity are the exchanged projective charts, not finite positive
source points. The midpoint and both real `T` branches therefore gain no new
invariant. Degrees of freedom removed: `0`.

## 2. Integer And Ideal Factorization

For each individual lift the proposed factorization is exactly

```text
4*U^2*q^2=(q-s)(q+s)(q-r)(q+r).
```

It is equivalent, for nonzero `q`, to `F(q)=U^2`, which already defines the
source-square divisor system. The useful split identity is likewise only

```text
(q^2-Delta_bar-2*U*q)*(q^2-Delta_bar+2*U*q)
  = q^2*(s-r)^2.
```

In `Z`, the class group is trivial. Any ideal allocation is therefore the
prime-valuation equality already present in `wl596`, including the exact
equal-valuation cancellation rows and `v_2(4)`. The six pairwise gcd bounds
are deterministic difference bounds:

```text
gcd(q-s,q+s) | 2*s,
gcd(q-r,q+r) | 2*r,
gcd(q-s,q-r), gcd(q+s,q+r) | s-r=2*Bbar,
gcd(q-s,q+r), gcd(q+s,q-r) | s+r=2*Abar.
```

Also `gcd(q,q-s)|s` and `gcd(q,q-r)|r`. These bounds do not couple `q_1`
and `q_2`; the existing shared gcds remain explicit. A Gaussian norm does
not repair this: the tempting expression has

```text
Norm_Z[i](q^2-Delta_bar+2*i*U*q)
  =(q^2-Delta_bar)^2+4*U^2*q^2,
```

which is not `q^2*(s-r)^2`. The valid identity is a split difference of
squares over `Z`, so no Gaussian ideal descent is justified without adding a
new equation. Degrees of freedom removed: `0`.

## 3. Reciprocity And Product Formula

Write `a=q_1*q_2` and `b_p=v_p(a) mod 2` for `p|Delta_bar`. For every
`c in Q^*`, Hilbert reciprocity says

```text
product_v (a,c)_v=1.
```

At an odd prime, with `a=p^alpha*u`, `c=p^beta*v` and `u,v` units,

```text
(a,c)_p=(-1)^((p-1)*alpha*beta/2)*(u/p)^beta*(v/p)^alpha.
```

The bit `b_p` gives only `alpha mod 2`; when `beta` is odd the unit character
`(u/p)` remains. At `p=2`, with odd `u,v`, the exact term is

```text
(a,c)_2=(-1)^(eps(u)*eps(v)+alpha*omega(v)+beta*omega(u)),
eps(w)=(w-1)/2 mod 2, omega(w)=(w^2-1)/8 mod 2.
```

It cannot be dropped: the exact unit and cancellation branches in `wl596`
remain. The real place is retained as well; here `a>0`, so its Hilbert term is
evaluated from that sign rather than silently omitted.

Consequently the product formula, with all local unit, dyadic, and
archimedean terms retained, is an identity for the same exact integer `a`; it
does not cut the divisor-pair set. Replacing those terms by a function of the
bits alone is unjustified: the `wl596` normalized `Q_7` witness already has
the same source-square and closure values with both unbalanced allocation
bits. Any further evaluation would be a new exact global theorem, not a
consequence of the declared product formula. Degrees of freedom removed: `0`.

## Literature Boundary

The archive index is [`docs/literature/README.md`](../../../literature/README.md).
Only the following results are used as applicability boundaries:

- Peschmann, *Quartic reductions and elliptic obstructions for perfect Euler
  bricks*, Theorems 5.4 and 6.2, as summarized in
  [`peschmann-2604-09328.md`](../../../literature/notes/peschmann-2604-09328.md),
  gives Kummer/2-descent obstructions for a different genus-3-to-elliptic
  setup and explicitly leaves a residual descent class. It does not compute
  this `q_i|Delta_bar` divisor-pair system or supply the missing reciprocity
  evaluation.
- Knaf-Selder-Spindler, the homogeneous-space algorithm summarized in
  [`knaf-selder-spindler.md`](../../../literature/notes/knaf-selder-spindler.md),
  gives a point-finding transformation for intersections of quadrics. It is
  not a global invariant or a rank theorem for the individual four-lift
  cover, so it does not remove a divisor-pair degree of freedom here.
- Ono's Main Theorems 1-3, summarized in
  [`ono-1996-concordant.md`](../../../literature/notes/ono-1996-concordant.md),
  concern primitive concordant solutions and elliptic torsion/twist families.
  They do not impose the fixed common source, positive square `x`, or the four
  individual lifts, so they are not evidence for a `q_1*q_2` invariant.
- Halbeisen-Hungerbuhler's Theorems 2 and 8, summarized in
  [`halbeisen-hungerbuhler-2021.md`](../../../literature/notes/halbeisen-hungerbuhler-2021.md),
  identify pythapotent conditions with positive rank for a related elliptic
  family. Their multiplicative pairing condition is different from the fixed
  common-source closure here, so the equivalence supplies no divisor-pair
  relation.

## Decision

The executable certificate is
[`global_invariant_candidate_audit.py`](../../../../scripts/theory/aa_bb/global_invariant_candidate_audit.py)
with focused tests in
[`test_global_invariant_candidate_audit.py`](../../../../tests/theory/aa_bb/test_global_invariant_candidate_audit.py).
The three declared classes add no independent information. HRL should pause;
reopening requires a genuinely new global invariant on the exact
closure-compatible positive divisor pairs, not another rewrite, local table,
or formal twist family.
