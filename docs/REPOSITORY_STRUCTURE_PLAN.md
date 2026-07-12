# Repository Structure Improvement Plan

## Purpose

Reduce navigation cost without disturbing the mathematical evidence chain or
turning repository cleanup into a second research project.

This is a gradual organization pass, not a mass rewrite. Existing worklogs,
scripts, tests, references, and Git history remain authoritative until each
small migration batch has been checked.

## Current Diagnosis

The repository size is manageable, but three large flat namespaces make it
hard to browse:

- `docs/work-logs/`
- `scripts/theory/`
- `tests/`

The naming problem is a symptom of that layout. File names currently repeat
the project, route, object layer, worklog number, action, and conclusion. The
result is precise but difficult to scan. The more important issue is that
small experiments often create a worklog, script, and test as three new
top-level files.

## Constraints

- Do not reorganize files while the current research batch is still changing.
- Do not mix mathematical changes with path-only cleanup in one commit.
- Do not delete proof history merely because a consolidated worklog exists.
- Do not alter theorem strength, object labels, or no-claim boundaries during
  structural cleanup.
- Do not introduce CI checks or hard file-name length rules.
- Use shorter names as a practical convention for files touched or created by
  this improvement.
- Avoid a large one-shot rename of historical scripts and tests.

## Target Shape

Keep the structure shallow and organized by research route:

```text
docs/
  work-logs/
    README.md
    consolidated/
    archive/

scripts/
  theory/
    aa_bb/

tests/
  theory/
    aa_bb/
```

The exact directories should be created only when the first checked migration
batch is ready. Empty scaffolding is unnecessary.

New AA+BB files should prefer compact names such as:

```text
docs/work-logs/541-v-ell-valuation-obstruction.md
scripts/theory/aa_bb/wl541_valuation_obstruction.py
tests/theory/aa_bb/test_wl541_valuation_obstruction.py
```

The file body, worklog title, and index carry the full mathematical statement.
The path only needs to identify the route and checkpoint.

## Execution Phases

### Phase 0: Wait for a coherent research checkpoint

The ongoing agent owns the current research batch. Before any move or rename:

1. Let that agent finish its current proof obligation.
2. Inspect the resulting worklogs, scripts, tests, and route documents.
3. Run the tests appropriate to that batch.
4. Commit the research checkpoint separately if it is coherent.

If the batch is incomplete, leave it untouched and postpone organization.

### Phase 1: Build a reference inventory

Before moving anything, identify:

- Markdown links to candidate files.
- Python imports or subprocess references to script paths.
- Tests that derive module paths from file names.
- README, project-status, glossary, memory, and worklog-index references.
- Generated artifacts whose metadata records a script path.

Produce a small migration manifest containing old path, proposed path, and
known references. This phase is read-only.

### Phase 2: Improve worklog navigation

Start with documentation because it has the lowest runtime risk:

1. Keep `docs/work-logs/README.md` as the human entry point.
2. Separate consolidated phase summaries from detailed historical logs.
3. Move only a range that already has a trustworthy consolidated summary.
4. Update all links in the same change.
5. Preserve original WL numbers and Git history with `git mv`.

The first candidate is the `wl491-wl522` range because it already has a
consolidated taxonomy worklog. Verify the consolidated file is sufficient
before moving any detailed logs.

### Phase 3: Consolidate the current symbolic-family episode

After the current M2 investigation reaches a real checkpoint, add one summary
for the episode beginning at `wl530`. The summary should state:

- the original proposition;
- exact reductions that remain valid;
- local residue classes already excluded;
- methods proved exhausted;
- the one remaining arithmetic statement;
- the next proof gate and forbidden conclusions.

Do not consolidate at an arbitrary WL number while the result is still
changing. The ending number is determined by the mathematical checkpoint.

### Phase 4: Introduce route directories for new code

Once the active batch is committed:

1. Put new AA+BB audit scripts under `scripts/theory/aa_bb/`.
2. Put their tests under `tests/theory/aa_bb/`.
3. Confirm package imports and root-path calculations in a focused test.
4. Update `scripts/README.md` with one route-level entry rather than listing
   every experimental filename.

Historical files stay where they are unless moving a small coherent group
clearly improves navigation.

### Phase 5: Reduce file creation per microstep

Use one WL for one proof obligation, not automatically for one computation.
Several coordinate changes, residue checks, or failed tactics may remain in
the same worklog and audit script when they answer the same question.

Create a new WL when at least one of these occurs:

- a new proposition is entered;
- an exact lemma or exclusion certificate is proved;
- a counterexample kills the current route;
- the remaining gap changes materially;
- a research gate is closed and another is explicitly entered.

This is a judgment guideline, not an automated rule.

### Phase 6: Optional historical cleanup

Only after the new layout has worked for several research steps, consider
moving additional historical script/test groups. Each batch must be small,
path-only, reference-complete, tested, and independently revertible.

Stop historical cleanup when further moves no longer make the current route
easier to understand.

## Checkpoint Policy

Use checkpoints at semantic boundaries:

1. Current research batch completed and verified.
2. Worklog navigation cleanup completed.
3. Current symbolic-family episode consolidated.
4. New AA+BB script/test layout proven by its first real task.

Do not commit files that another agent is actively changing. Before each
checkpoint, inspect `git status` and the diff again so concurrently produced
research is not accidentally included in a structural commit.

## Validation

For each migration batch:

- verify every old-path reference has been updated or intentionally retained;
- run focused tests for moved scripts and tests;
- run the full test suite when Python paths change;
- run `git diff --check`;
- confirm project-status and next-gate documents still point to the same
  mathematical checkpoint;
- confirm no theorem claim changed in a path-only commit.

## Completion Criteria

This improvement is complete when:

- the current route is discoverable from the main documentation without
  browsing hundreds of files;
- consolidated and historical worklogs have visibly different roles;
- new AA+BB scripts and tests use a route-specific location and concise names;
- micro-experiments no longer require three new top-level files by default;
- old evidence remains reachable and all tests pass;
- further cleanup would mostly create churn rather than improve navigation.
