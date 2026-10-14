# Agent Guide

This repository is a research notebook plus executable audit tools for the
rational-distance-to-square problem. Optimize for object clarity, not for
making the story sound more complete than it is.

## Read For The Task

The current user request selects the work. Read only the material needed for
that request; a local code or documentation edit does not require restoring
the research context.

| Task | Relevant entry |
| --- | --- |
| Assess a mathematical claim or select a research route | [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) for proved results and gaps; the selected task anchor for its scope. Use [NEXT_RESEARCH_GATE.md](docs/NEXT_RESEARCH_GATE.md) when selecting new research. |
| Resume a selected research task | Read its anchor. Use [current-context.md](docs/codex/current-context.md) or [index.md](docs/codex/index.md) to locate it when needed. |
| Change code | Read the owning module and relevant tests; use the [script index](scripts/README.md) if the entry point is unclear. |
| Edit documentation | Read the target and the sources or links affected by the edit. |
| Reuse an earlier method | Read the relevant [historical route](docs/archive/RESEARCH_ROUTES.md) and its supporting evidence. |

`current-context.md` holds the latest recorded research-entry pointer; each
task anchor owns its detailed status, scope, and next step. A recorded entry
does not authorize resuming it for an unrelated request.

The latest mathematical checkpoint and the currently selected activity are
different facts. Historical "next gate", "must", and "do not create" statements
describe their original task, not a standing instruction to resume it. A
completed or unselected task must not silently take over a new conversation.
Do not discard its proved facts or scoped failure certificates.

For the original equations use [MATH.md](docs/MATH.md); for terminology use
[GLOSSARY.md](docs/GLOSSARY.md). The
[closure architecture](docs/CLOSURE_QUOTIENT_MAINLINE.md),
[worklog index](docs/work-logs/README.md), and
[script index](scripts/README.md) are reference material, not a work queue.

## Proof And Scope Rules

- Separate exact proofs, exploratory computations, conjectures, and unresolved
  obligations. Finite counts or empty bounded searches do not prove a uniform
  exclusion without a proved finite reduction.
- A generic function-field nonsquare need not remain nonsquare at rational
  specializations. A quotient point must satisfy every required individual
  square lift before it becomes an original solution.
- Preserve the full-plane domain. Closure arguments require both sum and
  difference branches, ordered differences, and the relevant real intervals.
  Retain primitive denominators, gcd conditions, p=2, midpoint, endpoint,
  factor-zero, infinity, pole, and collision branches when using those models.
- A new definition, equivalent model, quotient, or extra table is not by itself
  a solved proof obligation. Identify the actual restriction proved or the
  independent obstruction obtained.
- Scope every route-death certificate to the audited mechanism. Paused work is
  not disproved mathematics; an untested method is not automatically forbidden.
- Rank, Selmer, Sha, family-exclusion, and Harborth claims each require a proof
  of the precise conclusion. A Selmer-based argument needs its complete
  Selmer bound; an independent proof need not pass through the Selmer route.
- For an explicit worst-case guarantee, prove that the strategy is sufficient.
  Add a matching lower bound only when the task asks for optimality or
  minimality; otherwise label the guarantee without implying optimality.
- Keep single-curve diagnostics, old package-x / S~, complete d-coordinate C_d
  ledgers, M_tail matrices, AA+BB admissibility, and theorem-level Selmer
  statements distinct. The old package-x / S~ bridge is not a Selmer bound.

An archived checkpoint does not authorize shell 11, new support families,
broad rank/Selmer/Sha/M_tail diagnostics, or entry into D2, D5, M2, or M3.
Those require an explicitly selected scoped task. Reusing an exhausted
mechanism also requires identifying the new input that changes its conclusion.

## Stable Files And Task Recovery

Preserve existing mathematical scripts, tests, certificates, and historical
derivations unless the user requests a scoped change or a verified defect
requires it. Explain the necessity, impact, non-goals, and regression check in
Chinese before touching a stable module. Do not overwrite unrelated worktree
changes or infer that an old task is complete merely from its date.

Use the existing docs/codex memory root; its landing policy remains
ask-by-default. For an authorized separate task, use a unique
docs/codex/tasks/<task-id>/active-task.md and add its pointer to index.md.
Ask before creating or extending a persistent record outside the authorized
task scope. Within an authorized scope, continue the listed edits, local
focused checks, and reversible verification without asking again. A new route,
an out-of-scope file, an external service, a deployment, or a destructive or
irreversible action needs fresh authorization.
Do not edit another agent's anchor. When recovering a selected task, read its
anchor and relevant evidence; use the context/index only to locate what is
needed, without rereading them when the task and evidence are already known.
No task starts just because its archived anchor contains a next step.

For newly authorized anchors, use the [minimal task-anchor template](docs/codex/task-anchor-template.md).
Legacy anchors may retain execution metadata for provenance; do not copy
`ExecutionPolicy`, `Execution protocol skills`, or `Lite Demo role` into a new
anchor unless the field changes a concrete decision.

## Delegation Model Contract

Do not delegate unless the user or the selected task explicitly calls for it.
When delegation is authorized, read the [delegation protocol](docs/codex/delegation-protocol.md)
before invoking it. The protocol owns the exact command, model and reasoning
level, Worker prompt boundary, one-level limit, retry rule, and Controller review.

## Worklogs And Verification

A new numbered checkpoint requires a new accepted mathematical obligation.
Documentation maintenance or a research preference is not a reason to create
one. Follow the short worklog/script/test convention in
[scripts/README.md](scripts/README.md), using the appropriate module owner.
Keep historical filenames and derivations; typo/index maintenance is separate
from mathematical revision.

Each accepted research record states its exact question, inputs, object layer,
proof versus sample status, exceptional branches, remaining gap, and scope of
its conclusion. Do not turn a task-local next step into a global instruction.

For scoped code changes, run focused tests and targeted Ruff first. Use a
temporary uv cache outside the repository:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest <focused tests>
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check <changed Python paths>
```

For an explicitly needed broad check:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check .
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff format --check .
```

Documentation-only work uses link, scope, and diff checks; it does not start
research computations. Generated results are ignored by default. Do not
force-add them or create a reusable research skill while its protocol is still
changing.
