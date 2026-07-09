# Agent Guide

This repository is a research notebook plus executable audit tools for the
rational-distance-to-square problem. Future agents should optimize for object
clarity, not for making the story sound more complete than it is.

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

The current handoff is route selection after the ambient `C_d` admissibility
layer. If `wl491` is present, the reusable filter has been defined and must be
used before any ambient `C_d` point enters an admissible ledger:

```text
classify_ambient_c_d_point_for_aa_bb_admissibility
```

If `wl492` is present, the known `u_3` ambient point has already been routed as
`not_admissible`, and the next gate is:

```text
build_candidate_queue_from_existing_M_tail_diagnostics
```

If `wl493` is present, that queue has been built from the existing `wl481`
finite `M_tail` diagnostics. The only existing kernel support in that input is
`u_3`, and it is recorded only as processed / deprioritized because it is
globally soluble but not AA+BB-admissible. The next gate is:

```text
extend_or_refresh_M_tail_diagnostics
```

If `wl522` is present, the current handoff is:

```text
try_common_source_square_obstruction_lemma_candidate_not_entered_here
```

`wl522` used `wl521` as the latest state and compressed the `wl491`-`wl521`
ledgers into a stable support-family / cover-family taxonomy by
classification and failure mode. The taxonomy has 43 final candidate-ledger
entries, 13 support families, 22 cover families, 5 ambient-globally-not-soluble
cover families, 15 globally soluble but not AA+BB-admissible cover families,
2 processed / duplicate cover families, no genuinely deferred cover families,
and no AA+BB-admissible cover families. The one named theorem-candidate pattern
isolated here is:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

It has not been proved and no proof-level work was entered. Do not execute
shell 11, compute new supports, test new ambient `C_d` solubility, apply
`wl491` to a new point, select a final obstruction candidate, run broad
rank/Selmer diagnostics, or claim Selmer/family progress. Do not treat the 15
not-admissible cover families as a theorem; the next explicit task, if chosen,
is only to try proving the named common-source square obstruction lemma.

If `wl521` is present but `wl522` is not present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

The post-`wl519` support/cover-family synthesis has been entered and stopped.
`wl521` re-aggregated the `wl491`-`wl519` ledgers, found no genuinely deferred
cover family and no AA+BB-admissible cover family, preserved the fully
classified `u_5` `d=(5,5,1)` mixed refuted/not-admissible history only as a
theorem-candidate pattern, and selected only the later finite shell extension:

```text
max(A,B) = 11
```

It has not been executed. Do not run shell 11 unless that is the explicit next
task. Do not re-open the two `wl519` not-admissible ledgers, shell-9 ledgers,
or previous refuted covers. Do not compute new supports, test new ambient
`C_d` solubility, apply `wl491` to a new point, select a final obstruction
candidate, pivot to proof-level generalization, run broad rank/Selmer
diagnostics, or claim Selmer/family progress.

If `wl520` is present but `wl521` is not present, the current handoff is:

```text
synthesize_support_and_cover_families_after_wl519_not_entered_here
```

The shared shell-10 `u_5` cover selected by `wl518` has been classified by
`wl519`, and `wl520` has selected post-classification support/cover-family
synthesis as the next narrow gate. That synthesis has not been entered.

Do not re-open the two `wl519` not-admissible ledgers, shell-9 ledgers, or
previous refuted covers. Do not execute shell 11, pivot to proof-level
generalization / local-row work, select a final obstruction candidate, run
broad rank/Selmer diagnostics, enter the selected synthesis, or claim
Selmer/family progress unless that is the explicit next task.

If `wl519` is present but `wl520` is not present, the current handoff is:

```text
post_wl519_route_choice_not_entered_here
```

The shared shell-10 `u_5` cover selected by `wl518` has been resolved by an
exact rational ambient `C_d` point:

```text
L = 10
T = 19
d = (5, 5, 1)
X = 1260642/121
u_minus_p = 504/11
u_pos_2sqrt_q = 464/11
u_neg_2sqrt_q = 1202/11
```

Both mirror ledgers have already been routed through `wl491` as globally
soluble but not AA+BB-admissible:

```text
AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
```

Do not re-open those ledgers, execute shell 11, pivot to proof-level
generalization, select a final obstruction candidate, run broad rank/Selmer
diagnostics, or claim Selmer/family progress unless that is the explicit next
task.

If `wl518` is present, the current handoff is:

```text
resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover_not_entered_here
```

The `wl491`-`wl517` ledgers have been aggregated by support family and cover
family. The only genuinely deferred cover family is the shared shell-10 `u_5`
cover:

```text
AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
L = 10
T = 19
d = (5, 5, 1)
```

This is only a theorem-candidate pattern, not a theorem: shell-5
`L=5,T=8,d=(5,5,1)` is refuted, shell-10 `L=10,T=11,d=(5,5,1)` is globally
soluble but not AA+BB-admissible, and shell-10 `L=10,T=19,d=(5,5,1)` remains
deferred. Do not execute shell 11, resolve this cover, pivot to proof-level
generalization, select a final candidate, run broad rank/Selmer diagnostics,
or claim Selmer/family progress unless that is the explicit next task.

If `wl517` is present but `wl518` is not present, the current handoff is:

```text
support_family_synthesis_after_wl517_not_entered_here
```

The 10 active shell-10 supports have already been routed through ambient
`C_d` solubility. Eight are globally soluble but not AA+BB-admissible after
`wl491`, and two are still deferred ambient-solubility ledgers:

```text
AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
```

Do not execute shell 11, do not resolve the two shell-10 deferred covers, do
not run broad rank/Selmer diagnostics, do not select a final obstruction
candidate, and do not treat shell-10 output as Selmer progress.

If `wl516` is present, the current handoff is:

```text
route_active_shell10_m_tail_support_through_ambient_C_d_solubility_then_wl491_filter_not_entered_here
```

Shell 10 has been executed as a finite `M_tail` diagnostic extension from the
existing `wl498` plan. It produced 10 active diagnostic supports and no
duplicate / processed support outputs:

```text
AA_A3_B10_u_3_plus_v_13_m_tail_shell10_candidate
AA_A7_B10_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate
AA_A10_B1_u_5_m_tail_shell10_candidate
AA_A10_B7_v_17_plus_w_13_m_tail_shell10_candidate
AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A1_B10_u_5_m_tail_shell10_candidate
BB_A7_B10_v_17_plus_w_13_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
BB_A10_B3_u_3_plus_v_13_m_tail_shell10_candidate
BB_A10_B7_u_7_plus_v_17_plus_w_5_m_tail_shell10_candidate
```

These are not ambient global `C_d` points, not AA+BB-admissible points, and
not final obstruction candidates. Do not route them through ambient `C_d`
solubility unless that is the explicit next task. Do not apply `wl491`, select
a final candidate, prove local rows, run broad rank/Selmer diagnostics, claim
uniform `M_tail` full rank, or treat shell-10 output as Selmer progress.

If `wl515` is present but `wl516` is not present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

All shell-9 ambient `C_d` deferred ledgers have now been classified: the four
`wl511` globally soluble but not AA+BB-admissible ledgers remain closed, the
two `wl512` `v_13` ledgers are refuted, and the two `wl514` `u_7` ledgers are
refuted. `wl515` selected the next finite shell:

```text
max(A,B) = 10
```

It has not been executed. Do not run shell 10 unless that is the explicit next
task. Do not re-open any closed shell-9 ledger, apply `wl491` to a refuted
cover, pivot to proof-level row work without a named proof gap, select a final
candidate, run broad rank/Selmer diagnostics, claim uniform `M_tail` full rank,
or treat shell diagnostics as theorem-level Selmer progress.

If `wl514` is present but `wl515` is not present, the current handoff is:

```text
post_wl514_route_choice_not_entered_here
```

`wl514` entered only the `wl513` selected gate and resolved the remaining
shared shell-9 `u_7` ambient `C_d` cover `L=7,T=16,d=(7,7,1)` by a mod-17
Mordell-Weil-sieve no-lift certificate. Both remaining `u_7` ledgers are now
ambient globally not soluble, so `wl491` was not applied. Do not execute shell
10, re-open the `wl512` `v_13` refutations, re-open the `wl511` not-admissible
shell-9 ledgers, apply `wl491`, select a final candidate, prove new local rows
outside this one certificate, run broad rank/Selmer diagnostics, or advance to
the next route unless that is the explicit task.

If `wl513` is present but `wl514` is not present, the current handoff is:

```text
resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers_not_entered_here
```

`wl513` selected targeted resolution of the remaining shared shell-9 `u_7`
ambient `C_d` cover as the next narrow gate, but did not enter it. The
remaining ledgers are:

```text
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

They share the `L=7,T=16,d=(7,7,1)` cover. Do not execute shell 10, re-open
the two `v_13` ledgers refuted by `wl512`, re-open the four shell-9 globally
soluble but not AA+BB-admissible ledgers from `wl511`, apply `wl491`, select a
final candidate, prove local rows, run broad rank/Selmer diagnostics, treat
these two `u_7` ledgers as globally soluble or globally not soluble without an
explicit certificate, or treat shell-9 output as Selmer progress.

If `wl512` is present but `wl513` is not present, the current handoff is:

```text
shell9_u7_ambient_C_d_global_solubility_ledgers_still_deferred_not_entered_here
```

The four `wl511` deferred shell-9 ledgers have been classified by `wl512`
without re-opening the four shell-9 globally soluble but not AA+BB-admissible
ledgers or any closed ledger through `wl511`. The two `v_13` ledgers are
ambient globally not soluble for their shared `L=4,T=13,d=(13,1,13)` cover.
The only still-deferred shell-9 ambient ledgers are:

```text
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

They share the `L=7,T=16,d=(7,7,1)` cover. Do not execute shell 10, select a
final candidate, prove local rows, run broad rank/Selmer diagnostics, treat
these two `u_7` ledgers as globally soluble or globally not soluble without an
explicit certificate, or treat shell-9 output as Selmer progress.

If `wl511` is present but `wl512` is not present, the current handoff is:

```text
shell9_deferred_ambient_C_d_global_solubility_ledgers_not_entered_here
```

The eight active shell-9 supports have already been routed through ambient
`C_d` solubility. Four are globally soluble but not AA+BB-admissible after
`wl491`, and four are still deferred ambient-solubility ledgers:

```text
AA_A4_B9_v_13_m_tail_shell9_candidate
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B4_v_13_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

Do not re-open the four not-admissible ledgers or any closed ledger through
`wl510`. Do not execute shell 10, select a final candidate, prove local rows,
run broad rank/Selmer diagnostics, treat deferred shell-9 covers as globally
not soluble without an explicit certificate, or treat shell-9 output as Selmer
progress.

If `wl510` is present but `wl511` is not present, the current handoff is:

```text
route_active_shell9_m_tail_support_through_ambient_C_d_solubility_then_wl491_filter_not_entered_here
```

Shell 9 has been executed as a finite `M_tail` diagnostic extension. It
produced eight active diagnostic supports and no duplicate / processed support
outputs. These are not ambient global `C_d` points, not AA+BB-admissible
points, and not final obstruction candidates. Do not route them through
ambient `C_d` solubility unless that is the explicit next task. Do not apply
`wl491`, select a final candidate, prove local rows, run broad rank/Selmer
diagnostics, or treat shell-9 output as Selmer progress.

If `wl509` is present but `wl510` is not present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

The post-`wl508` empty-active-shell route choice has been made. Shell 8
produced no active support and two pure `u_3` processed exclusions; these are
closed for the current route. The selected next finite shell is:

```text
max(A,B) = 9
```

It has not been executed. Do not run shell 9 unless that is the explicit next
task. Do not re-open shell-8 processed exclusions, invent a shell-8 ambient
`C_d` solubility task, apply `wl491`, select a final obstruction candidate,
prove local rows, run broad rank/Selmer diagnostics, or treat the shell-8
full-rank sample count or empty active queue as a uniform theorem.

If `wl508` is present but `wl509` is not present, the current handoff is:

```text
post_wl508_empty_shell_route_choice_not_entered_here
```

The shell-8 finite `M_tail` diagnostic has been executed. It produced no
active support and two pure `u_3` processed exclusions:

```text
AA_A3_B8_u_3_m_tail_shell8_candidate
BB_A8_B3_u_3_m_tail_shell8_candidate
```

Do not invent an ambient `C_d` solubility task for shell 8, do not apply
`wl491`, do not select a final obstruction candidate, do not prove local rows,
do not run broad rank/Selmer diagnostics, do not treat the shell-8 full-rank
sample count as a uniform theorem, and do not advance to `wl509`.

If `wl507` is present but `wl508` is not present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

The shell-7 active/deferred route is fully disposed: the eight `wl505`
globally soluble but not-admissible ledgers, the two pure `u_3` processed
exclusions, the two `wl506` refuted `w_5` ledgers, and the two `wl506`
globally soluble but not-admissible `u_7+w_37` ledgers are all closed for the
current route. The selected next finite shell is:

```text
max(A,B) = 8
```

It has not been executed. Do not run shell 8 unless that is the explicit next
task. Do not re-open shell-7 ledgers, test new ambient `C_d` solubility, apply
`wl491`, select a final obstruction candidate, prove local rows, run broad
rank/Selmer diagnostics, or treat this as Selmer progress.

If `wl506` is present but `wl507` is not present, the current handoff is:

```text
post_wl506_route_choice_not_entered_here
```

The four `wl505` deferred shell-7 ambient `C_d` global-solubility ledgers have
been resolved. The two `w_5` ledgers are ambient globally not soluble for their
shared `L=4,T=11,d=(1,5,5)` cover. The two `u_7 + w_37` ledgers are ambient
globally soluble for their shared `L=7,T=10,d=(7,259,37)` cover, but both fail
the `wl491` AA+BB admissibility filter and remain diagnostic not-admissible
ledgers. Do not re-open the eight `wl505` globally soluble but not-admissible
ledgers, the two pure `u_3` processed exclusions, or these four resolved
ledgers. Do not select a final obstruction candidate, prove local rows, run
broad rank/Selmer diagnostics, or treat this as Selmer progress unless that is
the explicit next task.

If `wl505` is present but `wl506` is not present, the current handoff is:

```text
shell7_deferred_ambient_C_d_global_solubility_ledgers_not_entered_here
```

The 12 active shell-7 supports have already been routed through ambient `C_d`
solubility: eight are globally soluble but not AA+BB-admissible after `wl491`,
and four are still deferred ambient-solubility ledgers. Do not re-open the
eight not-admissible ledgers or the two pure `u_3` processed exclusions. The
only unresolved shell-7 ambient ledgers are:

```text
AA_A4_B7_w_5_m_tail_shell7_candidate
AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate
BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate
BB_A7_B4_w_5_m_tail_shell7_candidate
```

If `wl504` is present and `wl505` is not present, the current handoff is:

```text
route_active_m_tail_support_through_ambient_C_d_solubility_then_wl491_filter_not_entered_here
```

The shell-7 finite `M_tail` diagnostic has been executed. It produced 12
active diagnostic supports and two pure `u_3` processed exclusions. These are
not ambient global `C_d` points, not AA+BB-admissible points, and not final
obstruction candidates. Do not route them through ambient `C_d` solubility
unless that is the explicit next task. Do not apply `wl491`, select a final
candidate, prove a local row, or treat shell-7 output as Selmer progress.

If `wl503` is present but `wl504` is not present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

The selected next finite shell is:

```text
max(A,B) = 7
```

It has not been executed. Do not run shell 7 unless that is the explicit next
task. Do not invent an ambient `C_d` solubility task for shell 6, do not apply
`wl491`, do not select a final obstruction candidate, and do not treat the
shell-6 full-rank sample as a uniform theorem.

If `wl502` is present but `wl503` is not present, the current handoff is:

```text
post_wl502_empty_shell_route_choice_not_entered_here
```

The route is:

```text
complete d-coordinate C_d ledger
  -> parameter-dependent M_tail
  -> ambient C_d global points
  -> AA+BB common-source admissibility filter (wl491)
  -> filter-aware M_tail candidate queue (wl492)
  -> processed/deprioritized u_3 queue entry (wl493)
  -> structured finite-shell plan (wl498)
  -> shell-5 u_5 diagnostics and ambient refutation (wl499-wl500)
  -> shell-6 empty M_tail diagnostic output (wl502)
  -> post-wl502 empty-shell route choice (wl503)
  -> shell-7 finite M_tail shell diagnostic output (wl504)
  -> active shell-7 support ambient route not entered
  -> active shell-7 support ambient route output (wl505)
  -> shell-7 deferred ambient C_d ledger resolution (wl506)
  -> post-wl506 route choice (wl507)
  -> finite shell-8 M_tail diagnostic extension (wl508)
  -> post-wl508 empty-shell route choice (wl509)
  -> finite shell-9 M_tail diagnostic extension (wl510)
  -> active shell-9 M_tail support ambient route output (wl511)
  -> four shell-9 ambient C_d solubility ledgers deferred
  -> two shell-9 v_13 ledgers refuted and two shell-9 u_7 ledgers still deferred (wl512)
  -> post-wl512 route choice selects targeted u_7 cover resolution (wl513)
  -> remaining shell-9 u_7 cover refuted by no-lift certificate (wl514)
  -> post-wl514 route choice selects shell-10 finite M_tail extension (wl515)
  -> finite shell-10 M_tail diagnostic extension (wl516)
```

If `wl502` is present, shell `max(A,B)=6` has already been executed as an
`M_tail` diagnostic extension. It produced no active support and no duplicate /
processed support output. Do not invent an ambient `C_d` solubility task for
shell 6, do not apply `wl491`, do not select a final obstruction candidate, and
do not treat the shell-6 full-rank sample as a uniform theorem.

Do not go back to the old package-`x` / `S~` bridge as if it were a complete
Selmer object. `S~` was a pseudo-container; it is not the theorem-level
`Sel_2(E_L/Q)`.

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

Counts are not proof progress by themselves. More packages, samples, candidates,
or JSON rows are progress only if they shrink a stated theorem gap or produce a
strict certificate.

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

Do not edit old worklogs except for clear typo/index maintenance. Add a new
worklog for a new research move.

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
