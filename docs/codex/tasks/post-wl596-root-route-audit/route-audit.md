# Post-wl596 Root Route Audit

Status: complete.

Base commit:

```text
7c13919
```

This is a route-selection audit, not a proof attempt. It does not create
`wl597`, modify frozen worklogs or scripts, run searches, add a model, or run
local-prime, rank, or Selmer computations.

## Outcome

```text
no_current_route_without_new_external_input
```

No existing route has both a theorem-strength obligation and a new independent
input available in the repository. The correct current decision is to pause,
not to select Selmer by default and not to rename an exhausted route.

## Root Problem

The original problem is whether a rational point in the plane can have
rational distances to all four vertices of a unit square. After common scaling,
D4 reduction, and the exact full-plane closure translation, the nontrivial
object is represented by positive rational or primitive integer data

```text
N_i^2+A^2 = S_i^2,
N_i^2+B^2 = T_i^2,       i=1,2,
{N1+N2, |N1-N2|} intersects {A+B, |A-B|}.
```

The two target branches, the two ordered difference orientations, positivity,
the midpoint, and all source lifts are part of the proposition. The equivalent
interior chain language is

```text
a^2+b^2, b^2+c^2, c^2+d^2, d^2+a^2 are squares,
a+c=b+d,
```

with the full-plane GEN-CLOSURE correction retained rather than silently using
the inside-square sum branch.

## Route Table

| Route | Object layer and exact proposition | New independent input required | Strongest evidence and boundary | Decision, theorem potential, prerequisites |
| --- | --- | --- | --- | --- |
| Strict counterexample | Original `P in Q^2`, or a primitive chain satisfying every square and GEN-CLOSURE equation. Obligation: exhibit one exact valid tuple and reconstruct the rational point. | A concrete tuple with exact square certificates, positivity, nondegeneracy, denominators, and all four distances. | `README.md` and the chain-fast baseline report no found example; bounded scans are finite evidence. The ambient `u_3` point from `wl487` is not admissible after `wl489`. | **Not ready, not killed.** Decisive potential, but no candidate exists. Prerequisite is an exact tuple, not another search report. |
| Quotient / theorem-level Selmer | Ratio ray `lambda=A/B`, closure quotients `AA/BB`, and complete `C_d` data. Obligation: a uniform `Sel_2(E_L/Q)` upper bound at the visible torsion baseline for both `A+B` and `|A-B|`, then torsion pullback and midpoint exclusion. | A uniform full-rank theorem for the parameter-dependent residual matrix `M_tail`, or a global obstruction that eliminates every residual complete-`d` cover while preserving AA+BB admissibility. | `wl469` refutes the old package-`x` equivalence. `wl471-wl479` then build the complete `d`-coordinate container, relevant-place support, odd/dyadic local rows, overlap rows, and torsion baseline. `wl480` reduces the remaining theorem to `M_tail_uniform_full_rank_missing`; `wl483-wl490` find no new local row and show the selected `u_3` cover is globally soluble while its point fails common-source admissibility. `wl491-wl522` classify the finite residual taxonomy but do not promote it to a family theorem. | **Paused: exact global matrix/obstruction theorem missing, not route-dead.** High theorem potential, but the local/formal-lift construction is not the current gap and should not be repeated. Prerequisite is a new uniform invariant controlling `M_tail` or all residual complete-`d` covers. |
| Relative Picard / HRL | Full individual four-radical cover and the realized class `[H_RL(P)]`. Obligation: prove fixed finite parameter-uniform support or produce a realized unbounded-support family. | A non-tautological parameter-uniform relative 2-descent class with forced parity across both branches, `p=2`, denominators, boundaries, and all four lifts. | `wl594` gives genus-three/genus-five geometry; `wl595` kills only the natural closure-product Kummer/split-prime/denominator mechanism; `wl596` reduces HRL to `q_1*q_2`; the post-wl596 audit exhausts involution, factorization, and reciprocity candidates. | **Paused: specific mechanisms route-dead, overall route not impossible.** High potential, but no new class or invariant. Prerequisite is external/new arithmetic input beyond the audited candidates. |
| Direct divisor-pair / integral-point | Primitive `q_i,d_i` with `q_i d_i=Delta_bar`, `F(q_i)` square, and one of six closure equations. Obligation: classify `sqf(q_1 q_2)` uniformly or prove a uniform integral-point/divisor-pair theorem. | A genuine global theorem on closure-compatible divisor pairs, such as an integral-point, Thue/Runge, or other arithmetic classification that removes a degree of freedom. | `wl596` is an exact converse and complete primewise/gcd/dyadic reduction. The post-wl596 global audit proves its three declared global candidates add no information. | **Paused: exact blocker remains.** High potential, but no available theorem. Prerequisite is a new global result, not a coordinate rewrite or local table. |
| Higher-genus / global Diophantine | The genus-five individual AA/BB lift, fixed-parameter genus-seventeen cover, or a parameterized surface. Obligation: uniformly exclude the restricted rational image, or give a uniform Brauer-Manin/Chabauty/integral-point obstruction preserving all lifts. | A family-level global method with rank, sections, divisor, or Brauer data strong enough to retain positive square `x`, positivity, both `T` branches, and the full lift. | `wl530-wl585` shows the elliptic quotient forgets square lifts and restores the original problem; Peschmann leaves a residual descent class and lists Brauer-Manin as future work. | **Untried but not ready.** Potentially decisive, but it requires external theorem/data absent from the repository. No current exact gate can be selected. |
| Finite shell / `M_tail` diagnostics | Bounded primitive shells and complete `C_d` ledgers. Obligation: certify a chosen finite shell has no admissible point. | Only a bounded-scope authorization and execution; it cannot supply a theorem over all ratios without a new bridge. | `wl491-wl522` processed shells and separated ambient solubility from AA+BB admissibility; shell 11 was only a planned diagnostic. Counts and empty queues are explicitly not proof. | **Finite diagnostic only.** No family-theorem potential at the current object layer. Prerequisite is an explicit finite-scope request; it is not a current root route. |
| Historical `R_lambda` / reciprocal route | `R_lambda={r: r^2+1 and r^2+lambda^2 are squares}` with full-plane closure. Obligation: prove the four-branch implication `r,s in R_lambda and closure => rs=lambda`. | A new global reciprocity or Diophantine theorem beyond product-square, q-adic, and dyadic reductions. | `wl162` closes the centerline through Yang Ji; `wl203-wl293` records the failed full-plane reciprocal/q-adic route and locally soluble residuals. | **Proved route-death for the attempted local/product mechanisms; residual theorem paused.** No novelty or prerequisite currently available. |
| Ambient `C_d` obstruction | Fixed complete `d`-coordinate covers. Obligation: prove a cover is locally soluble but globally pointless, then prove it is the relevant AA+BB class uniformly. | A strict global obstruction plus a reusable AA+BB lift theorem, not an ambient elliptic point. | `wl486-wl490` show the `u_3` cover has a global point and that point fails the BB common-source square; `wl483` found no new local/Hilbert row. | **Closed as a current obstruction candidate; diagnostic route remains.** It cannot be promoted without new cover-specific or family-level input. |

## Evidence Links

- Root status and theorem boundary: [`PROJECT_STATUS.md`](../../../PROJECT_STATUS.md),
  [`OPEN_DIRECTIONS.md`](../../../OPEN_DIRECTIONS.md), and
  [`CLOSURE_QUOTIENT_MAINLINE.md`](../../../CLOSURE_QUOTIENT_MAINLINE.md).
- Original problem and algebraic translation: [`README.md`](../../../../README.md)
  and [`MATH.md`](../../../MATH.md).
- Historical route consolidation: [`028`](../../../work-logs/028-proof-status-ec-foundation-consolidated.md),
  [`073`](../../../work-logs/073-gen-closure-modular-fullspace-consolidated.md),
  [`162`](../../../work-logs/162-r-lambda-centerline-consolidated.md),
  [`203`](../../../work-logs/203-wl218-full-plane-reciprocal-consolidated.md),
  and [`363`](../../../work-logs/363-lambda-mainline-consolidated.md).
- Current AA+BB and Selmer boundaries: [`386`](../../../work-logs/386-rank-zero-selmer-package-consolidated.md),
  [`468`](../../../work-logs/468-aa-bb-theorem-candidate-bridge-audit.md),
  [`470`](../../../work-logs/470-aa-bb-route-pivot-after-h2-audit.md),
  [`471`](../../../work-logs/471-aa-bb-complete-d-container-definition.md),
  [`480`](../../../work-logs/480-aa-bb-d4-uniform-matrix-rank-bound-audit.md),
  [`483`](../../../work-logs/483-aa-bb-local-hilbert-row-decision-gate.md),
  [`490`](../../../work-logs/490-aa-bb-route-impact-after-wl489-admissibility-failure.md),
  [`491-522`](../../../work-logs/491-522-aa-bb-admissibility-taxonomy-consolidated.md),
  and [`523-529`](../../../work-logs/523-529-common-source-function-field-squareclass-consolidated.md).
- Frozen and downstream certificates: [`530-585`](../../../work-logs/530-585-pure-v-ell-m1-m2-consolidated-checkpoint.md),
  [`wl595`](../../../work-logs/595-universal-closure-product-g4-route-death.md),
  [`wl596`](../../../work-logs/596-universal-four-factor-hrl-q0-divisor-allocation-blocker.md),
  and the [post-wl596 invariant audit](../wl596-global-invariant-candidate-audit/global-invariant-candidate-audit.md).
- Complete `C_d` boundary: [`wl483`](../../../work-logs/483-aa-bb-local-hilbert-row-decision-gate.md),
  [`wl487`](../../../work-logs/487-aa-bb-route-impact-of-global-point.md),
  [`wl489`](../../../work-logs/489-aa-bb-closure-pullback-common-source-constraints-for-global-c-d-point.md),
  and [`wl490`](../../../work-logs/490-aa-bb-route-impact-after-wl489-admissibility-failure.md).

## Boundary Classification

The following are proved route-deaths for their stated mechanisms, not claims
that the original theorem is solved:

- pure modular and standalone local-prime filtering;
- the old package-`x` / `S~` bridge to complete Selmer;
- the fixed-representative factor-twist local-image promotion;
- the universal closure-product Kummer/split-prime/denominator mechanism;
- the elliptic quotient subroute when its lost square lifts are not restored;
- the three post-wl596 HRL candidates: involution, source factorization, and
  bare reciprocity/product formula.

The following remain pauses with named missing input:

- family-level complete Selmer bound;
- a new HRL invariant or exact divisor-pair theorem;
- a family-level higher-genus global obstruction;
- an exact strict counterexample tuple.

Finite shell, `M_tail`, bounded rank, bounded point search, root-number data,
and literature analogies remain diagnostics or context only. They are not
silently promoted to route selection.

## Missing Inputs Required To Reopen

At least one of these new inputs is required before a theorem-strength route
can be selected:

1. An exact rational counterexample satisfying all four distance squares and
   the full-plane closure, with a reproducible reconstruction certificate.
2. A new uniform theorem forcing full rank of `M_tail`, or a global obstruction
   for every residual complete-`d` cover that also preserves the AA+BB lift;
   the complete local rows and torsion baseline already exist and must not be
   rebuilt as if they were the missing input.
3. A new non-tautological relative Picard/HRL class or a theorem classifying
   the exact closure-compatible `q_1*q_2` divisor pairs.
4. A uniform higher-genus/global theorem, such as a proved Brauer-Manin,
   Chabauty, or integral-point obstruction that retains the restricted image.

None is present in the current repository, and no current route can be
honestly selected without one.

## Literature And Cache Coverage

The index and notes were read from
[`docs/literature/README.md`](../../../literature/README.md), its timeline,
and all available notes. The current checkout has no actual PDF or extracted
text file under `docs/literature/pdfs/`; it contains only the cache README and
`.gitignore`. Therefore the route audit uses the checked-in notes and does not
claim fresh PDF verification.

- Peschmann's Theorems 5.4 and 6.2, in
  [`peschmann-2604-09328.md`](../../../literature/notes/peschmann-2604-09328.md),
  provide partial Kummer/2-descent obstructions for a different genus-three
  Euler-brick setup and explicitly leave a residual descent class. They support
  the boundary distinction, not a d19 theorem.
- Knaf-Selder-Spindler's quadrics-to-elliptic and point-finding algorithms, in
  [`knaf-selder-spindler.md`](../../../literature/notes/knaf-selder-spindler.md),
  apply to finding points on the related elliptic family, not to a uniform
  no-point or complete Selmer theorem for the restricted d19 image.
- Ono's concordant-form results, in
  [`ono-1996-concordant.md`](../../../literature/notes/ono-1996-concordant.md),
  show why positive rank produces primitive concordant solutions, but d19 adds
  the fixed `y=1` / square-`X` slice and closure, so positive rank is not enough.
- Halbeisen-Hungerbuhler Theorems 2 and 8, in
  [`halbeisen-hungerbuhler-2021.md`](../../../literature/notes/halbeisen-hungerbuhler-2021.md),
  concern pythapotent multiplicative pairings, not the shared-source closure.
- Chang's 2024 note records that the relevant five-point rational-distance
  question remains wide open. Bremner-Guy's full text is explicitly not
  available in the archive, so it cannot supply an unverified route theorem.

## Decision

No route is selected. The project should remain at the post-wl596 boundary until
one of the listed external inputs appears. In particular, the next action is
not another Selmer package, HRL rewrite, fixed family, local table, finite
shell, or numbered worklog.
