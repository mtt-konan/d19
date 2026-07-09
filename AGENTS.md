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
try_common_source_square_obstruction_lemma_candidate_not_entered_here
```

`wl522` is the current checkpoint. It compresses the `wl491`-`wl521` ledgers
into a support-family / cover-family taxonomy by classification and failure
mode:

- 43 final candidate-ledger entries.
- 13 support families.
- 22 cover families.
- 5 ambient-globally-not-soluble cover families.
- 15 globally soluble but not AA+BB-admissible cover families.
- 2 processed / duplicate cover families.
- No genuinely deferred cover families.
- No AA+BB-admissible cover families.

The only named theorem-candidate pattern isolated by this checkpoint is:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

It has not been proved, and no proof-level work was entered. The next explicit
task, if chosen, is only to try proving that named common-source square
obstruction lemma.

## Do Not Reopen

Unless the user explicitly asks for one of these, do not:

- execute shell 11;
- compute new supports;
- test new ambient `C_d` solubility;
- apply `wl491` to a new point;
- select a final obstruction candidate;
- run broad rank/Selmer diagnostics;
- treat the 15 not-admissible cover families as a theorem.

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
state after `wl522`, keep the full handoff in `docs/NEXT_RESEARCH_GATE.md`
short and point readers to the relevant consolidated worklog.

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
