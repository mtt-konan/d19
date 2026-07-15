# Berry C_1 Segmented Free Magma Route Audit

## Outcome

free_magma_global_stage_timeout

This is a tool-feasibility outcome, not an arithmetic blocker. The public
University of Sydney Calculator returned Magma 2.29-8, constructed the
selected JacHyp over K=Q(i), and exposed TwoSelmerGroup and TwoCoverDescent.
The earlier exact global descent request reached
BERRY_TWO_SELMER_V1_START and was terminated by the hard 60-second limit.
That request is not rerun here. The four new staged requests were submitted
once in this run but DNS was unavailable before the service was reached. That
transport result is recorded separately and is not promoted to an arithmetic
claim.

The segmented route is designed and independently audited, but not accepted
as segmented_free_magma_route_ready from this run. In particular, neither an
individual global stage nor cross-request Magma serialization was observed.
No full Selmer, rank, or local Kummer image is reported.

| request | observed result | boundary |
|---|---|---|
| capability probe | Magma 2.29-8, 0.03 seconds | exact capability only |
| earlier full global call | warning after START at 60 seconds | service timeout |
| four new staged requests | DNS transport error before service | no arithmetic result |

## Exact Global Data

The selected polynomial is

~~~
g6(t)=t^6+(-2-2*i)t^5+(-35-8*i)t^4+(-52-28*i)t^3
      +(19-40*i)t^2+(6+14*i)t-1.
~~~

Local Sage proof.all(True) checks give

~~~
L=Q(i)[theta]/(g6),  [L:Q(i)]=6,  [L:Q]=12,
f12(x)=x^12-4*x^11-62*x^10+68*x^9+1647*x^8+4184*x^7
       +2716*x^6-376*x^5+623*x^4-788*x^3+194*x^2-12*x+1,
Disc(MaximalOrder(L))=5019340374016.
~~~

The exact class group is trivial and the exact unit invariants are

~~~
Cl(L)=1,
U(L)=C4 x Z^5.
~~~

For the displayed genus-2 models the support over Q(i) is

~~~
S_model={(1+i),(94*i-169)}.
~~~

The complete relative prime decomposition has these stable slots:

| slot | base prime | (e,f) | local factor label |
|---:|---|---|---|
| 1 | 1+i | (2,1) | degree 2 |
| 2 | 1+i | (4,1) | degree 4 |
| 3 | 94*i-169 | (1,1) | x+3615 |
| 4 | 94*i-169 | (1,1) | x+9390 |
| 5 | 94*i-169 | (2,1) | ramified x+25652 branch |
| 6 | 94*i-169 | (1,2) | x^2+6501*x+25179 |

The degree sums are 2+4=6 and 1+1+2+2=6. Independently, the absolute
order decompositions over rational 2 and 37397 are

~~~
2:      (e,f)=(4,1),(8,1),
37397:  (1,1),(2,1),(1,1),(1,1),(1,1),(1,1),(1,2),(1,3).
~~~

The conjugate support prime -94*i-169 contributes four additional relative
slots (1,1),(1,1),(1,1),(1,3). Thus the model S-unit group has

~~~
U_S = C4 x Z^11,   U_S/U_S^2 ~= (F_2)^12.
~~~

with basis zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_6.
The conservative Berry-closed support has C4 x Z^15 and squareclass dimension
16. Triviality of the class group makes each support ideal principal, so
these six (or ten) prime generators, together with the unit basis, are an
exact S-unit squareclass basis. The only torsion relation is zeta4^4=1;
the serialized relation row is [4,0,...,0].

## Local Targets

The new local probe asks Magma only for Factorization(ChangeRing(g6,K_v)).
The strict target is supplied independently by the local compact-group
formula

~~~
dim_F2 J(K_v)/2J(K_v)
 = [K_v:Q_2]*g + dim_F2 J(K_v)[2]       (v above 2),
 = dim_F2 J(K_v)[2]                     (residue characteristic odd).
~~~

At varpi=(1+i), the absolute order data gives local relative factor degrees
[2,4]. The two even branch orbits give one invariant even branch partition
modulo the all-branch relation, hence dim J(K_varpi)[2]=1. Since
[K_varpi:Q_2]=2 and g=2, the strict target is

~~~
dim J(K_varpi)/2J(K_varpi)=4+1=5.
~~~

At pi=(94*i-169), the local factor degrees are [1,1,2,2]. The invariant
even branch partitions have dimension 4-1-1=2, so

~~~
dim J(K_pi)/2J(K_pi)=2.
~~~

The two quadratic twists have the same branch algebra and the same rational
2-torsion dimensions. These are target dimensions, not computed local
images. The prior exact proof C_i(K_varpi)=emptyset is a separate cover
statement and is not used as a Jacobian Kummer computation.

## Serialization Audit

The proposed cross-request payload is

~~~
schema=berry-c1-magma-segmented-v1
absolute defining polynomial f12
maximal-order discriminant
fixed support ideal_number 1..6 (or 1..10 conservatively)
relative e,f,norm and local-factor label
ideal-generator coordinates relative to an explicitly emitted maximal-order
basis, and S-unit coordinates in the fixed absolute-field power basis
unit generator coordinates, unit and S-unit invariants
relation matrix with the single torsion row [4,0,...,0].
~~~

No Magma map, ideal object, or abstract-group handle may be persisted. The
task Python certificate round-trips a proposed six-slot model payload and a
ten-slot conservative payload, checks degree sums and Sage-coordinate lengths,
and preserves task-local slot numbers. This is a schema check, not a Magma
rebuild certificate. Sage and Magma need not choose the same maximal-order
basis. The Stage 4 .m probe currently reconstructs only the field, maximal
order, discriminant, and scalar metadata; it does not yet reconstruct the
support ideals or generators from Stage 1/2 output. That cross-request step
remains part of the feasibility gate.

## Probe Inventory

- berry_sextic_magma_field_order.m: relative/absolute field, maximal order,
  discriminant, and rational support decomposition.
- berry_sextic_magma_sunits.m: class group, unit group, conservative S-unit
  basis, and relation sequence.
- berry_sextic_magma_local.m: the two local factorizations and theorem
  targets only.
- berry_sextic_magma_rebuild.m: field/scalar reconstruction prototype without
  transient Magma handles; support-ideal reconstruction remains unverified.
- scripts/theory/berry_sextic_magma_segmented.py: exact certificate and
  serialization parser.
- scripts/theory/berry_sextic_magma_segmented.sage: independent proof-enabled
  field, order, support, and odd-local-factor checks.
- tests/test_berry_sextic_magma_segmented.py: focused proof-data tests.

## Boundary And Next Obligation

The observed 60-second failure is a public-service limit. The current DNS
failure is transport only. Neither is evidence that the class group, units,
S-unit basis, or local Kummer images are arithmetically impossible. Restore
Calculator transport and run the four probes separately. Stage 1/2 must emit
an explicit Magma maximal-order basis, support ideals, generators, and
relations; a fresh request must reconstruct and verify those objects. Only
after those bounded requests succeed should the two local Kummer images and
the global C_1 descent be attempted.

## Files And Validation

- docs/codex/tasks/berry-sextic-genus2-classification-20260715/active-task.md
- this report
- scripts/theory/berry_sextic_magma_field_order.m
- scripts/theory/berry_sextic_magma_sunits.m
- scripts/theory/berry_sextic_magma_local.m
- scripts/theory/berry_sextic_magma_rebuild.m
- scripts/theory/berry_sextic_magma_segmented.py
- scripts/theory/berry_sextic_magma_segmented.sage
- tests/test_berry_sextic_magma_segmented.py

Focused validation:

~~~
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q tests/test_berry_sextic_magma_segmented.py -n 1
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff format scripts/theory/berry_sextic_magma_segmented.py tests/test_berry_sextic_magma_segmented.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check scripts/theory/berry_sextic_magma_segmented.py tests/test_berry_sextic_magma_segmented.py
git diff --check
~~~

The focused Berry/Magma suite passes with `14 passed`. The full repository
suite passes with `1403 passed in 51.99s`. The existing wl587-wl596 artifacts
and earlier Berry reports are untouched.
