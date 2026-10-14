# Research entry archive record

- Date: 2026-09-12
- Status: complete
- Scope: The user-approved documentation and task-entry archive, not a new mathematical result.
- Base HEAD: 486fd607fa658b10ed0fb06e69895daf46c02d6d
- Git boundary: No commit, tag, stash, reset, staging, or changes to existing mathematical artifacts are part of this task.

## Pre-edit baseline

The local [pre-edit archive](../../../../outputs/research-entry-archive-20260912/pre-edit.tar.gz)
contains 19 files: every pre-existing dirty/untracked nonignored file plus all
11 pre-existing entry documents selected for editing. It includes the original
1020-line guide and the already present wl597 worklog, script, test, and worker
records. It was captured after creating this maintenance anchor but before
changing any pre-existing file; this anchor itself is excluded.

Archive SHA-256:

```text
ce0dde454f0f4fde3563225401e74c48ccdcd9e39433b4ad31711f76f23aec65
```

The same local directory holds manifest.json, working-tree.patch, staged.patch,
and status.txt. The manifest fingerprints 892 pre-existing nonignored files.
Ignored runtime data and outputs were neither copied nor modified. The bundle
is local and ignored by Git under the existing outputs/ rule; do not treat a
commit or tag alone as preserving the pre-existing uncommitted state.

## Outcome

- AGENTS.md was reduced from 1020 to 131 lines, with historical route commands
  removed from default loading and proof guards preserved.
- PROJECT_STATUS.md owns mathematical status; current-context.md and the
  selected task anchor own activity. Other navigation pages point to them.
- [RESEARCH_ROUTES.md](../../../archive/RESEARCH_ROUTES.md) distinguishes
  completed local results, paused global gaps, scoped failures, and diagnostics.
- The [new exploration entry](../root-structural-exploration-20260912/active-task.md)
  awaits selection. It is not a new proof route or a running research task.
- Other task anchors, including the independently active Berry branch, stay
  byte-for-byte unchanged. No wl598 or new mathematical certificate is created.

## Verification

- All 19 archived members were extracted to a separate temporary directory
  and matched their pre-edit SHA-256 fingerprints; the bundle hash matched.
- All 881 pre-existing files outside the 11 entry documents retained their
  content hashes and modes. This includes the uncommitted wl597 artifacts,
  existing scripts, tests, data/certificates, derivations, and other task anchors.
- The closure architecture body from Core Object through the section before
  Reading Route is byte-for-byte unchanged. The delegation command and script
  command examples are unchanged; README commands differ only in comments.
- All 176 local link destinations in edited/new documents exist. Incoming
  references to the renamed legacy headings were checked; no matches remained.
- The context-memory-index root validator returned zero errors and warnings.
- Stale default wl521/wl596 handoff and priority-queue wording was removed from
  the entry set. Historical evidence still identifies each scoped conclusion.
- HEAD and the Git index are unchanged; git diff --check passed.
- Only 11 existing Markdown entry files and four new Markdown records are in
  this task's change set. verification.json in the local baseline directory
  records the preservation and link-check results.

Mathematical tests, Ruff, research searches, and proof computations were not
run: no mathematical implementation was changed. These checks verify the
documentation archive, not a new review of the mathematics.

## Restoration boundary

Restore only a selected entry file from the pre-edit bundle after inspecting
any subsequent user changes. Extract to a separate temporary directory first;
do not extract the whole bundle over the live tree or use Git reset/checkout.
The bundle contains pre-existing wl597 work, not files created by this archive
task. The original mathematical artifacts remain in place.
