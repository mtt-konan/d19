# Agent Guide

This repository is a research notebook plus executable audit tools for the
rational-distance-to-square problem. Optimize for object clarity, not for
making the story sound more complete than it is.

## Start Here

Read these files before changing research direction:

1. `docs/PROJECT_STATUS.md`
2. `docs/NEXT_RESEARCH_GATE.md`
3. `docs/OPEN_DIRECTIONS.md`
4. `docs/CLOSURE_QUOTIENT_MAINLINE.md`
5. `docs/work-logs/README.md`

For script names and entry points, read `scripts/README.md`. For terminology,
read `docs/GLOSSARY.md`.

## Current Research Gate

The current handoff is:

```text
wl529_v5_l1_t5_square_locus_complete_stop
```

`wl529` is the current completed one-family square-locus checkpoint. It uses
the `wl528` prototype and still touches only:

```text
support=v_5|L=1|T=5|d=(5,1,5)
```

represented by `AA_A1_B4_v_5_m_tail_refresh_candidate` and
`BB_A4_B1_v_5_m_tail_refresh_candidate` in `wl495`.

The `wl522` taxonomy remains the finite input snapshot:

- 43 final candidate-ledger entries.
- 13 support families.
- 22 cover families.
- 5 ambient-globally-not-soluble cover families.
- 15 globally soluble but not AA+BB-admissible cover families.
- 2 processed / duplicate cover families.
- No genuinely deferred cover families.
- No AA+BB-admissible cover families.

The only named theorem-candidate pattern isolated by `wl522` was:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

`wl523` proves only the point-level form from existing `wl491` machinery. It
does not prove a uniform cover-family theorem. `wl525` proves only that the
finite taxonomy cannot be promoted to that theorem from the current inputs.
`wl526` then compares four routes and selects only a later gate:

```text
gather_minimal_function_field_squareclass_proof_data_for_named_cover_families
```

`wl527` enters that scoping gate and inventories the minimum function-field
proof data for the named cover families: model inventory, source-side maps,
candidate `N,M` function-field elements, opposite-side product
squareclass/divisor-parity target, and exceptional specialization / positivity
separation. It finds:

```text
ready_cover_family_count = 0
not_ready_cover_family_count = 15
exact_missing_data_class =
  uniform_function_field_model_maps_and_squareclass_certificate
```

No next roadmap step is entered in `wl527`.

`wl528` then supplies the first explicitly selected single-family
function-field prototype. It reconstructs the chart

```text
Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))
```

derives rational maps to

```text
t = y*(r^2+20)/(4*r*(r^2-20))
N = (5+t)/2
M = (5-t)/2
```

and proves the opposite leg-4 product

```text
(N^2+16)(M^2+16)
```

is nonsquare in this prototype function field by a checked smooth
nonexceptional rational specialization:

```text
r = 10, y = 160, t = 6, N = 11/2, M = -1/2
(N^2+16)(M^2+16) = 12025/16
```

which is not a rational square.

`wl529` analyzes the remaining pointwise square-specialization locus

```text
U^2 = t^4 + 78*t^2 + 7921
```

through the degree-two map `X=t^2, Y=tU` to
`Y^2=X^3+78X^2+7921X`. A rigorous rank-zero and torsion computation on this
elliptic quotient leaves only `t=0`; an executable discriminant certificate
then proves that `t=0` has no rational lift to the `wl528` quartic. Thus the
one-family positivity-domain square-locus question is closed.

This is not a uniform cover-family theorem and not a Selmer/rank/Sha/family
exclusion claim. Do not advance to another cover family from `wl529` without a
new explicit user selection.

## Do Not Reopen

Unless the user explicitly asks for one of these, do not:

- execute shell 11;
- compute new supports;
- test new ambient `C_d` solubility;
- apply `wl491` to a new point;
- select a final obstruction candidate;
- run broad rank/Selmer diagnostics;
- treat the 15 not-admissible cover families as a theorem;
- claim that `wl523`, `wl525`, `wl526`, `wl527`, `wl528`, or `wl529` proves a
  uniform cover-family obstruction;
- build additional function-field models or prove the uniform lemma unless
  that gate is explicitly entered.
- treat `wl527` proof-data scoping as a ready proof attempt.
- treat `wl528` as more than one checked single-prototype nonsquare
  certificate.
- treat `wl529` as more than one closed one-family positivity-domain
  square-locus audit.

The old package-`x` / `S~` bridge is not a theorem-level Selmer object. Do not
route new evidence back into that ledger as if it proved a Selmer upper bound.

## Object Boundaries

Keep these layers separate in every explanation, worklog, and script result:

- `single_curve_full_2_selmer`: diagnostics for one elliptic curve.
- `S~`: old AA+BB common-source pseudo-container; useful history, not a final
  Selmer upper-bound object.
- complete `d`-coordinate `C_d` ledger: current local-solubility framework.
- `M_tail`: parameter-dependent residual `F2` matrix, not uniformly full rank.
- AA+BB admissibility: common-source closure constraints after an ambient
  `C_d` point is found.
- theorem-level `Sel_2(E_L/Q)`: only this can support a rank-zero theorem.

## Hard No-Claim Rules

Do not claim any of the following unless the work proves a complete Selmer
upper bound:

- `rank(E_L)=0` as a family theorem;
- `dim Sel_2(E_L/Q)=2`;
- `Sha(E_L)[2]=0`;
- family exclusion;
- Harborth global theorem.

Counts are not proof progress by themselves. More packages, samples,
candidates, or JSON rows are progress only if they shrink a stated theorem gap
or produce a strict certificate.

## Worklog Pattern

New research steps should usually have all three pieces:

- `docs/work-logs/<number>-<slug>.md`
- `scripts/theory/audit_<slug>.py`
- `tests/test_<slug>.py`

Each worklog should answer:

- What exact question is being audited?
- Which earlier worklog is the input?
- Which object layer is being touched?
- What is proved, what is only sampled, and what remains unproved?
- Which forbidden theorem claims remain false?
- What is the next narrow gate, and whether it is entered here.

Do not edit old worklogs except for clear typo/index maintenance. For route
state after `wl529`, keep the full handoff in `docs/NEXT_RESEARCH_GATE.md`
short and point readers to the relevant worklog.

## Verification

Use `uv` with a temp cache outside the repo:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest <focused tests>
```

For broad hygiene:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest
uv run ruff check .
```

The generated JSON artifacts under `results/` are ignored by default. Do not
force-add them unless the user explicitly asks for a result artifact to become
tracked source material.

## When To Create A Skill

Do not create a reusable skill while the math route is still moving. First keep
the workflow in `AGENTS.md` and `docs/NEXT_RESEARCH_GATE.md`. Extract a skill
only after the same gate pattern has been repeated enough times that the input
objects, forbidden claims, test command, and output schema are stable.
