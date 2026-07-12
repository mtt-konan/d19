# Repository Structure Migration Manifest

## Status

```text
inventory_status = complete
migration_status = batch_a_complete_active_research_deferred
active_research_task = m2-wl535-q-root-square-quartic-resolution
latest_observed_worklog = wl541
```

This manifest records the reference inventory required before repository
structure changes. It does not authorize moving files while the active
research task is changing them.

## Executed

Batch A was completed while explicitly excluding the active `wl530+` research
files:

- moved the 32 detailed `wl491-wl522` worklogs into
  `docs/work-logs/archive/`;
- kept the consolidated `491-522` worklog at its existing path;
- updated direct links in `docs/GLOSSARY.md` and
  `docs/NEXT_RESEARCH_GATE.md`;
- updated the root and archive worklog indexes;
- left all research statements unchanged.

The current symbolic-family consolidation and first new short-name script/test
pair remain deferred because the active task is still producing new exact
steps. They are not required to finish this non-conflicting migration batch.

## First Documentation Batch

Candidate range:

```text
wl491-wl522
```

Reason:

- The range already has a consolidated source of truth:
  `docs/work-logs/491-522-aa-bb-admissibility-taxonomy-consolidated.md`.
- All 32 detailed worklogs are still present directly under
  `docs/work-logs/`.
- Moving the details to `docs/work-logs/archive/` reduces the active flat
  namespace without changing executable code.

Proposed operation after the research checkpoint:

```text
docs/work-logs/491-*.md ... docs/work-logs/522-*.md
  -> docs/work-logs/archive/

docs/work-logs/491-522-aa-bb-admissibility-taxonomy-consolidated.md
  -> keep at docs/work-logs/ for the first batch
```

Keeping the consolidated file in place makes the first migration smaller and
avoids changing the current handoff path at the same time as the archive move.
It can move to a future `consolidated/` directory in a separate batch.

## Known Direct References

The following detailed worklogs have explicit Markdown links outside the
worklog index and therefore require link updates when archived:

| Worklog | Referencing file |
| --- | --- |
| `wl493` | `docs/GLOSSARY.md` |
| `wl496` | `docs/GLOSSARY.md` |
| `wl502` | `docs/GLOSSARY.md` |
| `wl503` | `docs/GLOSSARY.md` |
| `wl504` | `docs/GLOSSARY.md` |
| `wl506` | `docs/GLOSSARY.md` |
| `wl507` | `docs/GLOSSARY.md` |
| `wl508` | `docs/GLOSSARY.md` |
| `wl509` | `docs/GLOSSARY.md` |
| `wl510` | `docs/GLOSSARY.md` |
| `wl511` | `docs/GLOSSARY.md` |
| `wl512` | `docs/GLOSSARY.md` |
| `wl513` | `docs/GLOSSARY.md` |
| `wl514` | `docs/GLOSSARY.md` |
| `wl515` | `docs/GLOSSARY.md` |
| `wl521` | `docs/GLOSSARY.md` |
| `wl522` | `docs/NEXT_RESEARCH_GATE.md` |

Some detailed worklogs also name one another. Those relative references must
be checked after the files move, even when both source and target move into
the same archive directory.

The consolidated file is referenced by `scripts/README.md`; its path remains
unchanged in the first batch.

## Executable Coupling

No tracked result metadata was found that records a `wl491-wl522`
`scripts/theory/` path.

The tests for this route commonly execute scripts by constructing an exact
path under `scripts/theory/`, for example:

```python
ROOT / "scripts/theory/" / "audit_...wlNNN_....py"
```

Consequences:

- Moving scripts requires changing their matching tests in the same commit.
- Moving tests into `tests/theory/aa_bb/` changes the meaning of expressions
  such as `Path(__file__).parent.parent`.
- Script and test directory migration must not be combined with the first
  documentation-only archive batch.
- The first new script placed under `scripts/theory/aa_bb/` must establish and
  test the correct project-root calculation before historical files move.

Pytest is configured with:

```text
testpaths = ["tests"]
```

Nested test directories are discoverable, but root-path calculations inside
individual tests still need explicit adjustment.

## Current Symbolic-Family Batch

The episode beginning at `wl530` is not ready for consolidation. At inventory
time:

- the active task remains open;
- `wl540` is the latest observed exact reduction;
- the next step is analysis of the nonzero unit squareclass branch and the
  conditional Hensel-root branch;
- the active-task file explicitly forbids committing the research batch.

Therefore no ending WL number is assigned to the future consolidated summary.
Do not use `530-540` as a final range merely because those files currently
exist.

## Migration Batches

### Batch A: Archive detailed wl491-wl522 worklogs

Scope:

- move the 32 detailed worklogs with `git mv`;
- update direct links in `docs/GLOSSARY.md` and
  `docs/NEXT_RESEARCH_GATE.md`;
- update references between moved worklogs where necessary;
- update `docs/work-logs/README.md` to distinguish active, consolidated, and
  archived material.

Validation:

- no old detailed path remains in tracked Markdown;
- every moved file is reachable from the worklog index or consolidated file;
- `git diff --check` passes;
- no mathematical statement changes.

### Batch B: Consolidate the wl530+ episode

Start only when the active proof obligation reaches a semantic checkpoint.
Determine the ending WL from the completed mathematics, then add one compact
handoff summary. This batch changes documentation only and does not archive
the fresh detailed evidence immediately.

### Batch C: Prove the new script/test layout

Use the first new post-checkpoint AA+BB task:

```text
scripts/theory/aa_bb/wlNNN_<short-topic>.py
tests/theory/aa_bb/test_wlNNN_<short-topic>.py
```

Update `scripts/README.md` at route level and run focused plus full tests. Do
not move historical scripts in this batch.

### Batch D: Optional historical code moves

After Batch C has demonstrated stable imports and root handling, select one
small coherent historical range. Move its scripts and tests together, update
exact path references, and stop if the navigation benefit is marginal.

## Pre-Migration Recheck

Because another agent is active, repeat these checks immediately before Batch
A:

```text
git status --short --branch
docs/codex/active-task.md status and stop condition
latest worklog number
all references to wl491-wl522 file names
```

If research files are still changing, continue to wait. Structural commits
must never absorb unfinished research changes.
