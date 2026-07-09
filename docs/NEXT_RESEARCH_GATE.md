# Next Research Gate

This page is the handoff for the next agent. It says what to do next, and just
as importantly, what not to re-open.

## Current Position

The latest committed route reaches `wl490`. The current workspace may also
contain `wl491`, `wl492`, `wl493`, `wl494`, `wl495`, `wl496`, `wl497`,
`wl498`, `wl499`, `wl500`, `wl501`, `wl502`, `wl503`, `wl504`, `wl505`,
`wl506`, `wl507`, `wl508`, `wl509`, `wl510`, `wl511`, `wl512`, `wl513`,
`wl514`, `wl515`, `wl516`, `wl517`, `wl518`, `wl519`, `wl520`, and `wl521`: `wl491` defines the reusable filter contract,
`wl492` selects the
route after that filter has no unfiltered known ambient `C_d` point left to
process, `wl493` builds the existing-diagnostic candidate queue, `wl494`
refreshes the sampled `M_tail` diagnostics on a bounded primitive AA/BB grid,
`wl495` routes those refreshed supports through ambient `C_d` solubility before
applying `wl491` only where a global point is established, `wl496` resolves the
two remaining `wl495` deferred `v_5` ledgers for their common
`L=4,T=5,d=(5,1,5)` cover, `wl497` selects the post-`wl496` next gate without
executing it, and `wl498` structures that next `M_tail` extension without
refreshing a grid or computing new supports. `wl499` executes exactly the
finite primitive shell `max(A,B)=5`, records two active `u_5` `M_tail`
diagnostic supports, and stops before ambient `C_d` solubility or `wl491`.
`wl500` routes exactly those two `u_5` supports through ambient `C_d`
solubility, closes their common `L=5,T=8,d=(5,5,1)` cover as globally not
soluble, and therefore does not apply `wl491`. `wl501` selects the post-`wl500`
next gate as executing the next finite `M_tail` shell from the existing `wl498`
plan, but does not execute it. `wl502` executes exactly that shell at
`max(A,B)=6`, finds all eight primitive AA/BB samples full rank in the current
`M_tail` diagnostics, records empty support queues, and stops before ambient
`C_d` solubility or `wl491`. `wl503` selects the post-`wl502` next gate as
executing the next finite `M_tail` shell from the existing `wl498` plan at
`max(A,B)=7`, but does not execute it. `wl504` executes exactly that shell at
`max(A,B)=7`, records 12 active shell-7 `M_tail` diagnostic supports and two
processed `u_3` exclusions, and stops before ambient `C_d` solubility or
`wl491`.
`wl505` routes exactly those 12 active shell-7 supports through ambient
`C_d` solubility first, records eight exact integral ambient points as
globally soluble but not AA+BB-admissible after `wl491`, leaves four ambient
global-solubility ledgers genuinely deferred, and does not re-open the two
pure `u_3` processed exclusions.
`wl506` resolves exactly those four deferred shell-7 ledgers: two `w_5`
ledgers are ambient globally not soluble, and two `u_7 + w_37` ledgers are
ambient globally soluble but not AA+BB-admissible after `wl491`. `wl507`
selects the post-`wl506` next gate as executing the next finite `M_tail` shell
from the existing `wl498` plan at `max(A,B)=8`, but does not execute it.
`wl508` executes exactly that shell at `max(A,B)=8`, records no active new
kernel supports and two processed pure `u_3` exclusions, and stops before
ambient `C_d` solubility or `wl491`. `wl509` selects the post-`wl508` next
gate as executing the next finite `M_tail` shell from the existing `wl498`
plan at `max(A,B)=9`, but does not execute it. `wl510` executes exactly that
shell at `max(A,B)=9`, records eight active new kernel supports and no
duplicate / processed support outputs, and stops before ambient `C_d`
solubility or `wl491`. `wl511` routes exactly those eight active shell-9
supports through ambient `C_d` solubility first: four exact integral ambient
points route through `wl491` as globally soluble but not AA+BB-admissible, and
four covers remain genuinely deferred ambient-solubility ledgers. `wl512`
classifies exactly those four deferred shell-9 ledgers: the two `v_13`
entries are ambient globally not soluble for their common
`L=4,T=13,d=(13,1,13)` cover, and the two `u_7` entries remain explicit
deferred ledgers for their common `L=7,T=16,d=(7,7,1)` cover. `wl513`
selects the next narrow gate as targeted resolution of that remaining shared
`u_7` ambient `C_d` cover, but does not enter it. `wl514` enters exactly that
selected gate, resolves the shared `u_7` cover by a mod-17 Mordell-Weil-sieve
no-lift certificate as ambient globally not soluble, and stops before the
post-`wl514` route choice. `wl515` observes that all shell-9 ambient `C_d`
deferred ledgers have now been classified, preserves the four `wl511`
globally soluble but not AA+BB-admissible ledgers, the two `wl512` `v_13`
refutations, and the two `wl514` `u_7` refutations, and selects the next
narrow gate as executing the next finite `M_tail` shell from the existing
`wl498` plan at `max(A,B)=10`, but does not execute shell 10. `wl516`
executes exactly that shell at `max(A,B)=10`, records 10 active new kernel
supports and no duplicate / processed support outputs, and stops before
ambient `C_d` solubility or `wl491`. `wl517` routes exactly those 10 active
shell-10 supports through ambient `C_d` solubility first: eight exact integral
ambient points route through `wl491` as globally soluble but not
AA+BB-admissible, and two covers remain genuinely deferred ambient-solubility
ledgers. `wl518` aggregates the `wl491`-`wl517` ledgers by support family and
cover family, identifies the only genuinely deferred cover family as the shared
shell-10 `u_5` cover `L=10,T=19,d=(5,5,1)`, records the `u_5` theorem-candidate
pattern as not a theorem, and selects targeted resolution of that shared cover
as the next narrow gate without entering it. `wl519` enters exactly that
selected gate, records an exact rational ambient `C_d` point on the shared
shell-10 `u_5` cover, applies `wl491` to the two mirror entries, and routes
both as globally soluble but not AA+BB-admissible; it does not make the
post-`wl519` route choice. `wl520` observes that the only `wl518` deferred
cover family is now classified, compares support-family synthesis, shell 11,
proof-level generalization / local-row work, and final-candidate selection,
and selects support/cover-family synthesis after `wl519` as the next narrow
gate without entering it. `wl521` enters exactly that selected synthesis,
re-aggregates the `wl491`-`wl519` ledgers after the shared shell-10 `u_5`
cover has been classified, records no genuinely deferred cover families and no
AA+BB-admissible cover families, preserves the finite `u_5` mixed
refuted/not-admissible history only as a theorem-candidate pattern, and selects
only a later finite shell extension at `max(A,B)=11` from the existing `wl498`
plan without executing shell 11.

The corrected line is no longer the old package-`x` / `S~` bridge. The current
line is the complete `d`-coordinate route:

```text
D0 complete d-container
  -> D1 relevant places
  -> D2 local C_d rows
  -> D3 torsion baseline
  -> D4 M_tail rank obstruction
  -> u_3 ambient C_d point audit
  -> AA+BB admissibility gate
  -> M_tail candidate queue routing
  -> existing M_tail candidate queue audit
  -> bounded M_tail diagnostic refresh
  -> refreshed support ambient C_d / wl491 route audit
  -> deferred v_5 ambient C_d ledger resolution
  -> post-wl496 route choice
  -> structured M_tail diagnostic extension plan
  -> finite shell-5 M_tail diagnostic extension
  -> active u_5 ambient C_d solubility route
  -> post-wl500 route choice
  -> finite shell-6 M_tail diagnostic extension
  -> post-wl502 empty-shell route choice
  -> finite shell-7 M_tail diagnostic extension
  -> active shell-7 M_tail support ambient route
  -> four shell-7 ambient C_d solubility ledgers deferred
  -> four shell-7 deferred ambient C_d ledgers resolved
  -> post-wl506 route choice
  -> finite shell-8 M_tail diagnostic extension
  -> post-wl508 empty-shell route choice
  -> finite shell-9 M_tail diagnostic extension
  -> active shell-9 M_tail support ambient route
  -> four shell-9 ambient C_d solubility ledgers deferred
  -> two shell-9 v_13 ledgers refuted; two shell-9 u_7 ledgers still deferred
  -> post-wl512 route choice selects targeted u_7 cover resolution
  -> remaining shell-9 u_7 cover refuted by no-lift certificate
  -> post-wl514 route choice selects finite shell-10 M_tail extension
  -> finite shell-10 M_tail diagnostic extension
  -> active shell-10 M_tail support ambient route
  -> two shell-10 ambient C_d solubility ledgers deferred
  -> wl491-wl517 support/cover family synthesis
  -> shared shell-10 u_5 deferred cover resolution selected but not entered
  -> shared shell-10 u_5 cover globally soluble but not AA+BB-admissible
  -> post-wl519 route choice selects post-classification family synthesis
  -> post-wl519 support/cover family synthesis
  -> later finite shell extension at max(A,B)=11 selected but not entered
```

The important outcome is:

```text
AA, A=3, B=1, d=(3,3,1)
```

has a global ambient `C_d` point. That point pulls back to the `AA` quotient
with:

```text
N = 4
M = 0
```

but it fails the `BB` common-source closure condition because:

```text
(N^2+B^2)(M^2+B^2) = 17
```

which is not a rational square. So this point is neither a current obstruction
candidate nor an AA+BB-admissible point. It lives only in the diagnostic ledger:

```text
ambient globally soluble but not AA+BB-admissible
```

## Current Narrow Gate

If `wl521` is present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

The `wl491`-`wl519` ledgers have been re-aggregated after the shared shell-10
`u_5` cover was classified. The final candidate-ledger snapshot has 43 entries,
13 support families, 22 cover families, 10 refuted entries, 29 globally soluble
but not AA+BB-admissible entries, 4 already-closed entries, no genuinely
deferred entries, and no AA+BB-admissible entries. The only reusable pattern
preserved by `wl521` is finite diagnostic `u_5` cover history:

```text
support = u_5
d = (5, 5, 1)
L=5,T=8   refuted
L=10,T=11 globally soluble but not AA+BB-admissible
L=10,T=19 globally soluble but not AA+BB-admissible
```

This is not a theorem and does not isolate a named proof-level local row,
Hilbert row, or Selmer-layer gap. `wl521` therefore selects only the later
finite-shell extension from the existing `wl498` plan:

```text
max(A,B) = 11
```

It has not been executed. Do not run shell 11 unless that is the explicit next
task. Do not re-open the two `wl519` not-admissible ledgers, shell-9 ledgers,
or previous refuted covers. Do not compute new supports, test new ambient
`C_d` solubility, apply `wl491` to a new point, select a final obstruction
candidate, pivot to proof-level generalization, run broad rank/Selmer
diagnostics, or claim rank zero, a Selmer upper bound, uniform `M_tail` full
rank, or family exclusion.

If `wl520` is present, the current handoff is:

```text
synthesize_support_and_cover_families_after_wl519_not_entered_here
```

The only `wl518` genuinely deferred cover family has been classified by
`wl519`: the shared shell-10 `u_5` cover `L=10,T=19,d=(5,5,1)` is ambient
globally soluble, but both mirror entries fail `wl491` and remain diagnostic
not-admissible ledgers. `wl520` selected the next narrow gate as a
post-classification support-family / cover-family synthesis over `wl491`-
`wl519`, aimed only at preserving reusable theorem-candidate patterns.

Do not enter that synthesis unless it is the explicit next task. Do not
re-open the two `wl519` not-admissible ledgers, shell-9 ledgers, or previous
refuted covers. Do not execute shell 11, run broad rank/Selmer diagnostics,
pivot to proof-level generalization / local-row work, select a final
obstruction candidate, or claim rank zero, a Selmer upper bound, uniform
`M_tail` full rank, or family exclusion.

If `wl519` is present, the current handoff is:

```text
post_wl519_route_choice_not_entered_here
```

The only genuinely deferred `wl518` cover family has now been classified. The
shared shell-10 `u_5` cover

```text
L = 10
T = 19
d = (5, 5, 1)
```

has the exact rational ambient `C_d` point:

```text
X = 1260642/121
u_minus_p = 504/11
u_pos_2sqrt_q = 464/11
u_neg_2sqrt_q = 1202/11
```

This proves ambient global solubility for that one cover, not a Selmer bound
or family theorem. After `wl491`, both mirror entries are globally soluble but
not AA+BB-admissible:

```text
AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
```

Do not re-open the two `wl519` not-admissible ledgers, do not execute shell
11, do not pivot to proof-level generalization, do not select a final
obstruction candidate, and do not claim rank zero, a Selmer upper bound,
uniform `M_tail` full rank, or family exclusion unless that is the explicit
next task.

If `wl518` is present, the current handoff is:

```text
resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover_not_entered_here
```

The `wl491`-`wl517` ledgers have already been aggregated by support family and
cover family. The only genuinely deferred cover family is:

```text
support = u_5
L = 10
T = 19
d = (5, 5, 1)

AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
```

The `u_5` pattern is only theorem-candidate information: shell-5
`L=5,T=8,d=(5,5,1)` is refuted, shell-10 `L=10,T=11,d=(5,5,1)` is globally
soluble but not AA+BB-admissible, and shell-10 `L=10,T=19,d=(5,5,1)` remains
deferred. Do not treat this pattern as a family theorem. Do not execute shell
11, do not resolve the two shell-10 deferred covers unless that is the explicit
next task, do not run broad rank/Selmer diagnostics, do not select a final
obstruction candidate, do not pivot to proof-level generalization before this
cover is classified, and do not claim Selmer progress.

If `wl517` is present, the current handoff is:

```text
shell10_deferred_ambient_C_d_global_solubility_ledgers_not_entered_here
```

The 10 active shell-10 supports have already been routed through ambient
`C_d` solubility. Eight are globally soluble but not AA+BB-admissible after
`wl491`, and two are still deferred ambient-solubility ledgers:

```text
AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
```

Do not re-open the eight not-admissible ledgers or any closed shell-9 ledger.
Do not execute shell 11, select a final candidate, prove local rows, run broad
rank/Selmer diagnostics, treat the two deferred shell-10 covers as globally
not soluble without an explicit certificate, or treat shell-10 output as
Selmer progress.

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

After `wl514`, all shell-9 ambient `C_d` deferred ledgers have been
classified: four shell-9 supports from `wl511` are globally soluble but not
AA+BB-admissible, the two `wl512` `v_13` ledgers are ambient globally not
soluble, and the two remaining `wl514` `u_7` ledgers are ambient globally not
soluble. `wl515` makes only the route choice and selects the next finite
primitive shell:

```text
max(A,B) = 10
```

It has not been executed. Do not run shell 10 unless that is the explicit next
task. Do not re-open any closed shell-9 ledger, do not apply `wl491` to a
refuted cover, do not pivot to proof-level row work without a named proof gap,
do not select a final obstruction candidate, do not run broad rank/Selmer
diagnostics, do not claim uniform `M_tail` full rank, and do not treat finite
shell diagnostics as theorem-level Selmer progress.

If `wl514` is present but `wl515` is not present, the current handoff is:

```text
post_wl514_route_choice_not_entered_here
```

`wl514` entered only the `wl513` selected gate. It resolves the remaining
shared shell-9 `u_7` ambient `C_d` cover:

```text
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
L = 7
T = 16
d = (7, 7, 1)
V^2 = (X + 120)(X - 904)(X + 904)
```

by an exhaustive no-lift certificate. The certificate uses the single
instantiated Mordell-Weil description `E(Q)=<G>+E(Q)[2]` with
`G=(1032,16896)` and a mod-17 sieve: the full rational reduction image has
empty intersection with the mod-17 reductions satisfying the three
`d=(7,7,1)` cover squareclass conditions, and the point at infinity is blocked
because `7` is not a square modulo `17`. Therefore both remaining `u_7`
ledgers route to `ambient globally not soluble`.

Because no ambient global point is established, `wl491` is not applied. The
post-`wl514` route choice is not made here. Do not execute shell 10, re-open
the `wl512` `v_13` refutations, re-open the `wl511` globally soluble but not
AA+BB-admissible shell-9 ledgers, apply `wl491`, select a final obstruction
candidate, prove new local/Hilbert rows outside this one cover certificate,
run broad rank/Selmer diagnostics, claim a uniform `M_tail` theorem, claim
rank zero or a complete Selmer upper bound, or advance to any next roadmap
step unless that is the explicit next task.

If `wl513` is present, the current handoff is:

```text
resolve_remaining_shell9_u7_ambient_C_d_global_solubility_ledgers_not_entered_here
```

`wl513` is a route-choice audit only. It uses `wl512` as input, preserves the
two shell-9 `v_13` refuted ledgers, the four shell-9 globally soluble but not
AA+BB-admissible ledgers from `wl511`, and every closed ledger through `wl512`.
It selects the next narrow gate as targeted resolution of the remaining shared
shell-9 `u_7` ambient `C_d` cover:

```text
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
L = 7
T = 16
d = (7, 7, 1)
V^2 = (X + 120)(X - 904)(X + 904)
```

That selected gate is not entered here. The future gate must resolve this
single shared cover by either an exact ambient `C_d` point or an exhaustive
no-lift certificate; only after ambient global solubility is established may
`wl491` be applied. Do not execute shell 10, re-open closed shell-9 ledgers,
select a final obstruction candidate, prove local rows, run broad rank/Selmer
diagnostics, claim a uniform `M_tail` theorem, treat these two `u_7` ledgers as
globally soluble or globally not soluble without an explicit certificate, or
advance to `wl514`.

If `wl512` is present but `wl513` is not present, the current handoff is:

```text
shell9_u7_ambient_C_d_global_solubility_ledgers_still_deferred_not_entered_here
```

The four `wl511` deferred shell-9 ledgers have been classified without
re-opening the four shell-9 globally soluble but not AA+BB-admissible ledgers
or any closed ledger through `wl511`. The two `v_13` ledgers are ambient
globally not soluble for their shared `L=4,T=13,d=(13,1,13)` cover. The only
still-deferred shell-9 ambient ledgers are:

```text
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

They share the `L=7,T=16,d=(7,7,1)` cover. `wl512` records no exact ambient
`C_d` point and no exhaustive no-lift certificate for this cover, so it remains
genuinely deferred. Do not execute shell 10, select a final obstruction
candidate, prove local rows, run broad rank/Selmer diagnostics, claim a uniform
`M_tail` theorem, treat these two `u_7` ledgers as globally soluble or globally
not soluble without an explicit certificate, or advance to `wl513`.

If `wl511` is present but `wl512` is not present, the current handoff is:

```text
shell9_deferred_ambient_C_d_global_solubility_ledgers_not_entered_here
```

The eight active shell-9 supports have already been routed through ambient
`C_d` solubility: four are globally soluble but not AA+BB-admissible after
`wl491`, and four are still deferred ambient-solubility ledgers. Do not re-open
the four not-admissible ledgers or any closed ledger through `wl510`. The only
unresolved shell-9 ambient ledgers are:

```text
AA_A4_B9_v_13_m_tail_shell9_candidate
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B4_v_13_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

Do not execute shell 10, select a final obstruction candidate, prove local
rows, run broad rank/Selmer diagnostics, claim a uniform `M_tail` theorem, or
treat the four deferred ledgers as globally not soluble without an explicit
certificate.

If `wl510` is present but `wl511` is not present, the current handoff is:

```text
route_active_shell9_m_tail_support_through_ambient_C_d_solubility_then_wl491_filter_not_entered_here
```

The shell-9 finite `M_tail` diagnostic has been executed with:

```text
shell_bound = 9
sample_count = 24
full_rank_sample_count = 16
kernel_sample_count = 8
kernel_support_entry_count = 8
active_new_support_entry_count = 8
excluded_duplicate_or_processed_support_entry_count = 0
unique_active_supports = u_3, u_7, v_13, v_5, w_53
```

The active shell-9 diagnostic supports are:

```text
AA_A4_B9_v_13_m_tail_shell9_candidate
AA_A7_B9_u_7_m_tail_shell9_candidate
AA_A9_B1_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate
AA_A9_B4_v_13_m_tail_shell9_candidate
BB_A1_B9_u_3_plus_v_5_plus_w_53_m_tail_shell9_candidate
BB_A4_B9_v_13_m_tail_shell9_candidate
BB_A9_B4_v_13_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

They are `M_tail` diagnostic supports only: not ambient global `C_d` points,
not AA+BB-admissible points, and not final obstruction candidates. Do not
re-open closed ledgers through `wl509`. Do not route these shell-9 supports
through ambient `C_d` solubility unless that is the explicit next task. Do not
apply `wl491`, select a final obstruction candidate, prove local rows, run
broad rank/Selmer diagnostics, claim a uniform `M_tail` theorem, or advance to
the selected next route.

If `wl509` is present but `wl510` is not present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

The post-`wl508` route choice has been made with:

```text
completed_finite_shell_bound_after_wl508 = 8
shell8_sample_count_from_wl508 = 16
shell8_full_rank_sample_count_from_wl508 = 14
shell8_kernel_sample_count_from_wl508 = 2
shell8_kernel_support_entry_count_from_wl508 = 2
shell8_active_new_support_entry_count_from_wl508 = 0
shell8_excluded_duplicate_or_processed_support_entry_count_from_wl508 = 2
active_candidate_count_after_wl508 = 0
```

The selected next narrow gate is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan
```

with:

```text
entered_here = false
uses_existing_wl498_plan = true
shell_bound_to_execute_later = 9
preserve_wl498_duplicate_support_guard = true
new_shell_or_grid_refreshed_here = false
m_tail_diagnostics_extended_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_here = false
candidate_selected_here = false
```

Do not re-open the shell-8 pure `u_3` processed exclusions, shell-7 ledgers,
bounded `v_5` ledgers, shell-5 `u_5` ledgers, shell-6 empty diagnostic output,
or the old `u_3` ambient ledger. Do not run shell 9 unless that is the explicit
next task. Do not invent an ambient `C_d` solubility task for shell 8, do not
apply `wl491`, do not select a final obstruction candidate, do not prove local
rows, do not run broad rank/Selmer diagnostics, do not claim a uniform
`M_tail` theorem, and do not advance to the selected next gate.

If `wl508` is present but `wl509` is not present, the current handoff is:

```text
post_wl508_empty_shell_route_choice_not_entered_here
```

The shell-8 finite `M_tail` diagnostic has been executed with:

```text
shell_bound = 8
sample_count = 16
full_rank_sample_count = 14
kernel_sample_count = 2
kernel_support_entry_count = 2
active_new_support_entry_count = 0
excluded_duplicate_or_processed_support_entry_count = 2
unique_active_supports = []
```

The two kernel outputs are pure `u_3` processed-support repeats:

```text
AA_A3_B8_u_3_m_tail_shell8_candidate
BB_A8_B3_u_3_m_tail_shell8_candidate
```

They are not active candidates. Do not re-open shell-7 ledgers, the shell-8
processed exclusions, bounded `v_5` ledgers, shell-5 `u_5` ledgers, or the
old `u_3` ambient ledger. Do not invent an ambient `C_d` solubility task for
shell 8, do not apply `wl491`, do not select a final obstruction candidate,
do not prove local rows, do not run broad rank/Selmer diagnostics, do not
claim a uniform `M_tail` theorem, and do not advance to `wl509`.

If `wl507` is present but `wl508` is not present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

The post-`wl506` route choice has been made with:

```text
completed_finite_shell_bound_after_wl506 = 7
shell7_deferred_entry_count_from_wl506 = 4
shell7_deferred_entries_resolved_by_wl506 = 4
shell7_ambient_global_solubility_refuted_count_from_wl506 = 2
shell7_globally_soluble_not_admissible_count_from_wl506 = 2
shell7_ambient_global_solubility_still_deferred_count_after_wl506 = 0
shell7_wl491_filter_applied_count_from_wl506 = 2
aa_bb_admissible_count_after_wl506 = 0
active_candidate_count_after_wl506 = 0
```

The selected next narrow gate is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan
```

with:

```text
entered_here = false
uses_existing_wl498_plan = true
shell_bound_to_execute_later = 8
preserve_wl498_duplicate_support_guard = true
new_shell_or_grid_refreshed_here = false
m_tail_diagnostics_extended_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_here = false
```

Do not re-open the eight `wl505` globally soluble but not-admissible shell-7
ledgers, the two pure `u_3` processed exclusions, the two `wl506` refuted
`w_5` ledgers, or the two `wl506` globally soluble but not-admissible
`u_7+w_37` ledgers. Do not run shell 8 unless that is the explicit next task.
Do not test new ambient `C_d` solubility, apply `wl491` to new points, select
a final obstruction candidate, prove local rows, run broad rank/Selmer
diagnostics, claim a uniform `M_tail` theorem, or advance to `wl508`.

If `wl506` is present but `wl507` is not present, the current handoff is:

```text
post_wl506_route_choice_not_entered_here
```

The four `wl505` deferred shell-7 ambient ledgers have been resolved with:

```text
wl505_deferred_entry_count = 4
explicitly_classified_entry_count = 4
ambient_globally_soluble_count = 2
ambient_global_solubility_refuted_count = 2
ambient_global_solubility_still_deferred_count = 0
wl491_filter_applied_count = 2
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 2
aa_bb_filter_not_applied_count = 2
```

The refuted ledgers are:

```text
AA_A4_B7_w_5_m_tail_shell7_candidate
BB_A7_B4_w_5_m_tail_shell7_candidate
```

for their shared `L=4,T=11,d=(1,5,5)` cover. The globally soluble but
not AA+BB-admissible ledgers are:

```text
AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate
BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate
```

for their shared `L=7,T=10,d=(7,259,37)` cover. `wl506` does not re-open the
eight shell-7 globally soluble but not-admissible ledgers from `wl505`, does
not re-open the two pure `u_3` processed exclusions, does not select a final
obstruction candidate, prove a local row, run broad rank/Selmer diagnostics,
claim a uniform `M_tail` theorem, or advance to `wl507`.

If `wl505` is present but `wl506` is not present, the current handoff is:

```text
shell7_deferred_ambient_C_d_global_solubility_ledgers_not_entered_here
```

The active shell-7 route audit has been executed with:

```text
active_shell7_support_entry_count = 12
processed_exclusions_reopened_count = 0
ambient_globally_soluble_count = 8
ambient_global_solubility_refuted_count = 0
ambient_global_solubility_deferred_count = 4
wl491_filter_applied_count = 8
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 8
aa_bb_filter_deferred_count = 4
```

The four still-deferred shell-7 ambient ledgers are:

```text
AA_A4_B7_w_5_m_tail_shell7_candidate
AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate
BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate
BB_A7_B4_w_5_m_tail_shell7_candidate
```

The two pure `u_3` processed exclusions remain not re-opened:

```text
AA_A6_B7_u_3_m_tail_shell7_candidate
BB_A7_B6_u_3_m_tail_shell7_candidate
```

The eight established ambient global points all route through `wl491` as:

```text
globally_soluble_but_not_aa_bb_admissible_ledger
```

`wl505` does not select a final obstruction candidate, prove a local row, run
broad rank/Selmer diagnostics, claim a uniform `M_tail` theorem, or advance to
`wl506`. The remaining gap, not entered by `wl505`, is to resolve the four
deferred shell-7 ambient `C_d` global-solubility ledgers if the route continues.

If `wl504` is present but `wl505` is not present, the current handoff is:

```text
route_active_m_tail_support_through_ambient_C_d_solubility_then_wl491_filter_not_entered_here
```

The shell-7 diagnostic extension has been executed with:

```text
shell_bound = 7
sample_count = 24
full_rank_sample_count = 12
kernel_sample_count = 12
kernel_support_entry_count = 14
active_new_support_entry_count = 12
excluded_duplicate_or_processed_support_entry_count = 2
unique_active_supports = [u_3, u_7, v_13, v_5, w_17, w_37, w_5]
```

The only processed outputs are the pure `u_3` support-family entries:

```text
AA_A6_B7_u_3_m_tail_shell7_candidate
BB_A7_B6_u_3_m_tail_shell7_candidate
```

The active shell-7 outputs are still only `M_tail` diagnostic supports. They
are not ambient global `C_d` points, not AA+BB-admissible points, and not final
obstruction candidates. The next work, if any, is to route the active shell-7
support queue through ambient `C_d` global solubility first, then apply `wl491`
only where ambient global solubility is proved. Do not enter that route unless
it is the explicit next task.

If `wl503` is present but `wl504` is not present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

The selected next finite shell is:

```text
max(A,B) = 7
```

This must use the existing `wl498` finite-shell plan and duplicate-support
guard. It must not re-open `u_3`, bounded `v_5`, shell-5 `u_5`, or shell-6
empty diagnostic ledgers; any new support must still route through ambient
`C_d` global solubility before `wl491`. Do not execute shell 7 unless that is
the explicit next task.

If `wl502` is present but `wl503` is not present, the current handoff is:

```text
post_wl502_empty_shell_route_choice_not_entered_here
```

The shell-6 diagnostic extension has been executed with:

```text
shell_bound = 6
sample_count = 8
full_rank_sample_count = 8
kernel_sample_count = 0
active_new_support_entry_count = 0
excluded_duplicate_or_processed_support_entry_count = 0
unique_active_supports = []
```

It used the `wl498` duplicate-support guard and the `wl501` closed-ledger
exclusions:

```text
u_3_processed_or_deprioritized_after_wl493_wl491
bounded_v_5_entries_disposed_by_wl495_wl496
shell5_u_5_entries_refuted_by_wl500
```

It did not test ambient `C_d` solubility, did not apply `wl491`, did not select
a final obstruction candidate, did not prove a new local row, and did not
advance to `wl503`. The next work should be a route-choice step after this
empty shell output, not a retroactive solubility/admissibility audit for shell 6.

If `wl501` is present but `wl502` is not present, the current handoff is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan_not_entered_here
```

The selected next finite shell is:

```text
max(A,B) = 6
```

This must use the existing `wl498` finite-shell plan and duplicate-support
guard. It must not re-open `u_3`, bounded `v_5`, or shell-5 `u_5` ledgers; any
new support must still route through ambient `C_d` global solubility before
`wl491`.

If `wl500` is present but `wl501` is not present, the current handoff is:

```text
post_wl500_route_choice_not_entered_here
```

The two active `wl499` `u_5` supports have been routed as:

```text
ambient_c_d_global_solubility_status = globally_not_soluble
aa_bb_admissibility_status = not_applied_ambient_global_solubility_refuted
ledger_route = ambient_c_d_global_solubility_refuted_ledger
```

The next work must not re-open those two ledgers or treat them as admissible /
not-admissible ambient global points. A later route-choice step may decide the
next narrow gate, but `wl500` itself does not enter `wl501`.

If `wl499` is present but `wl500` is not present, the current handoff is:

```text
route_active_m_tail_support_through_ambient_C_d_solubility_then_wl491_filter
```

It has not been entered here. The two active shell-5 diagnostic supports are
`AA_A5_B3_u_5_m_tail_shell5_candidate` and
`BB_A3_B5_u_5_m_tail_shell5_candidate`; both must first become ambient global
`C_d` points before `wl491` can be applied.

If `wl498` is present but `wl499` is not present, the current handoff is:

```text
execute_finite_M_tail_diagnostic_extension_from_wl498_plan
```

It has been structured but not executed. The chronological gate trail below is
kept so the next agent can see why `u_3` and the bounded refreshed `v_5`
ledgers must not be re-opened, and why the next finite shell must use the
`wl498` duplicate-support guard.

If `wl497` is present but `wl498` is not present, the current handoff is:

```text
structure_next_M_tail_diagnostic_extension
```

It has been selected but not executed.

The `wl492` gate is:

```text
build_candidate_queue_from_existing_M_tail_diagnostics
```

If `wl491` is not present, the next work should define this reusable filter.
If `wl491` is present, future work must use the filter before recording any
ambient global `C_d` point as AA+BB-admissible.

Minimum expected output:

- a precise input schema for an ambient `C_d` point;
- the pullback data needed to recover candidate `N, M`;
- the AA and BB square tests;
- degeneracy handling, especially `M=0` and midpoint cases;
- a result ledger that separates `admissible`, `not_admissible`, and
  `missing_pullback_data`;
- tests covering the `u_3` point from `wl489`.

`wl491` implements this contract as:

```text
classify_ambient_c_d_point_for_aa_bb_admissibility
```

and classifies the known `u_3` point as:

```text
output_class = not_admissible
ledger_route = globally_soluble_but_not_aa_bb_admissible_ledger
```

If `wl492` is present, the filter has been applied to the only currently known
ambient point in the route input. There are no unfiltered already-known ambient
`C_d` point ledgers left in that input:

```text
admissible_point_count = 0
not_admissible_point_count = 1
unfiltered_already_known_ambient_c_d_point_count = 0
```

The next work should build, not yet execute, an ordered queue from existing
`M_tail` diagnostics:

```text
wl481_sample_matrices_kernel_diagnostics
wl482_classified_u3_support_as_already_disposed
wl491_classify_ambient_c_d_point_for_aa_bb_admissibility
```

If `wl493` is present, that queue has been built. The queue audit finds:

```text
kernel_support_entry_count_from_wl481 = 1
active_unprocessed_candidate_count = 0
deprioritized_or_excluded_candidate_count = 1
```

The single existing support is `u_3`. It is retained only as a processed /
deprioritized queue entry because it is already:

```text
ambient_c_d_global_solubility_status = globally_soluble
aa_bb_admissibility_status = not_admissible
ledger_route = globally_soluble_but_not_aa_bb_admissible_ledger
```

The next narrow gate after `wl493` is therefore:

```text
extend_or_refresh_M_tail_diagnostics
```

Any new support from that refreshed diagnostic layer must still follow:

```text
M_tail support
  -> ambient C_d solubility
  -> wl491 AA+BB admissibility filter
  -> admissible / not_admissible ledger routing
```

If `wl494` is present, the bounded refresh has been run with:

```text
side in {AA, BB}, 1 <= A,B <= 4, gcd(A,B)=1
sample_count = 22
active_new_support_entry_count = 6
processed_or_excluded_u3_entry_count = 2
unique_active_supports = v_5
```

Those `v_5` entries are active diagnostic outputs only. `wl494` does not prove
ambient `C_d` solubility, does not apply the wl491 admissibility filter to a
new candidate, and does not select a final obstruction candidate.

The next narrow action after `wl494`, not entered by `wl494`, is:

```text
route_refreshed_support_through_ambient_C_d_solubility_then_wl491_filter
```

If `wl495` is present, that route audit has been run without selecting a final
candidate:

```text
active_refreshed_support_entry_count = 6
ambient_globally_soluble_count = 4
ambient_global_solubility_deferred_count = 2
wl491_filter_applied_count = 4
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 4
```

The four exact ambient global `C_d` points are routed by `wl491` as:

```text
globally_soluble_but_not_aa_bb_admissible_ledger
```

The remaining two active refreshed entries are explicitly retained as:

```text
AA_A4_B1_v_5_m_tail_refresh_candidate
BB_A1_B4_v_5_m_tail_refresh_candidate
```

with:

```text
ambient_c_d_global_solubility_status = global_solubility_deferred
aa_bb_admissibility_status = not_applied_ambient_global_solubility_unproved
ledger_route = ambient_c_d_solubility_deferred_ledger
```

The next gap after `wl495`, not entered by `wl495`, is to resolve those two
ambient `C_d` global-solubility deferred ledgers. Do not treat them as
refuted, admissible, or selected obstruction candidates.

If `wl496` is present, the two `wl495` deferred ledgers have been resolved:

```text
wl495_deferred_entry_count = 2
explicitly_classified_entry_count = 2
ambient_global_solubility_refuted_count = 2
ambient_global_solubility_still_deferred_count = 0
wl491_filter_applied_count = 0
aa_bb_admissible_count = 0
```

The common cover is:

```text
L = 4
T = 5
d = (5,1,5)
```

Both entries route to:

```text
ambient_c_d_global_solubility_status = globally_not_soluble
aa_bb_admissibility_status = not_applied_ambient_global_solubility_refuted
ledger_route = ambient_c_d_global_solubility_refuted_ledger
```

The `wl491` filter is not applied to these two entries because ambient
global solubility is refuted. `wl496` deliberately does not select a final
obstruction candidate.

If `wl497` is present, the route choice after those disposals has been made:

```text
u3_active_unprocessed_candidate_count_after_wl493 = 0
u3_processed_or_deprioritized_count_after_wl493 = 1
bounded_v5_active_support_entry_count_from_wl494 = 6
bounded_v5_routed_not_admissible_count_from_wl495 = 4
bounded_v5_refuted_ambient_count_from_wl496 = 2
bounded_v5_still_deferred_count_after_wl496 = 0
aa_bb_admissible_count_after_wl496 = 0
active_candidate_count_after_wl496 = 0
```

The selected next narrow gate is:

```text
structure_next_M_tail_diagnostic_extension
```

with:

```text
entered_here = false
new_grid_refreshed_here = false
m_tail_diagnostics_extended_here = false
candidate_selected_here = false
advance_to_wl498 = false
```

The next agent should structure, not yet blindly run, a non-duplicating
`M_tail` diagnostic extension that carries forward the disposed `u_3` and
bounded `v_5` route state.

If `wl498` is present, that structure has been built:

```text
extension_unit = finite_primitive_shell
side in {AA, BB}
A, B positive integers
gcd(A,B) = 1
shell_axis = max(A,B)
prior_completed_shell_bound = 4
allowed_future_shells = finite shells with max(A,B) > 4
```

The `wl498` exclusion ledger has:

```text
u_3 support family = exclude_or_deprioritize_without_reentering
bounded wl494-wl496 v_5 route keys = excluded disposed entries
```

The future duplicate-support guard key is:

```text
source_quotient, A, B, L, T, candidate_support
```

Any genuinely new support from a later finite `M_tail` extension must still
follow:

```text
M_tail support
  -> ambient C_d global solubility
  -> wl491 AA+BB admissibility filter
  -> admissible / not_admissible / refuted ledger
```

`wl498` itself has:

```text
new_grid_refreshed_here = false
m_tail_diagnostics_extended_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
candidate_selected_here = false
advance_to_wl499 = false
```

If `wl499` is present, the finite primitive shell has been executed with:

```text
shell_bound = 5
sample_count = 16
full_rank_sample_count = 14
kernel_sample_count = 2
active_new_support_entry_count = 2
excluded_duplicate_or_processed_support_entry_count = 0
unique_active_supports = u_5
```

The active `M_tail` diagnostic outputs are:

```text
AA_A5_B3_u_5_m_tail_shell5_candidate
BB_A3_B5_u_5_m_tail_shell5_candidate
```

`wl499` has:

```text
m_tail_diagnostics_extended_here = true
new_supports_computed_here = true
new_c_d_solubility_tested_here = false
wl491_filter_applied_here = false
candidate_selected_here = false
advance_to_wl500 = false
```

These are not ambient points yet and not AA+BB-admissible points.

If `wl500` is present, those two active shell-5 entries have been routed
through the required ambient `C_d` solubility gate. Both entries share:

```text
L = 5
T = 8
d = (5,5,1)
```

with cover equations:

```text
X + 72 = 5*u_minus_p^2
X - 328 = 5*u_pos_2sqrt_q^2
X + 328 = u_neg_2sqrt_q^2
```

The targeted single-cover Mordell-Weil torsion-lift certificate records:

```text
V^2 = (X + 72)(X - 328)(X + 328)
rank = 0
torsion points = O, (-328,0), (-72,0), (328,0)
```

and no listed torsion point lifts to the `d=(5,5,1)` cover. Therefore:

```text
active_u5_support_entry_count = 2
ambient_globally_soluble_count = 0
ambient_global_solubility_refuted_count = 2
ambient_global_solubility_still_deferred_count = 0
wl491_filter_applied_count = 0
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 0
```

`wl500` has:

```text
route_audit_built_here = true
all_active_u5_entries_classified_here = true
candidate_selected_here = false
new_local_row_proved_here = false
broad_rank_or_selmer_diagnostics_run = false
advance_to_wl501 = false
```

The `wl491` filter is not applied because ambient global solubility is refuted.

If `wl501` is present, the post-`wl500` route choice has been made:

```text
shell5_active_u5_support_entry_count_from_wl500 = 2
shell5_ambient_global_solubility_refuted_count_from_wl500 = 2
shell5_ambient_global_solubility_still_deferred_count_after_wl500 = 0
shell5_wl491_filter_applied_count_from_wl500 = 0
aa_bb_admissible_count_after_wl500 = 0
active_candidate_count_after_wl500 = 0
completed_finite_shell_bound_after_wl500 = 5
```

The selected next narrow gate is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan
```

with:

```text
entered_here = false
uses_existing_wl498_plan = true
shell_bound_to_execute_later = 6
new_shell_or_grid_refreshed_here = false
m_tail_diagnostics_extended_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_here = false
advance_to_wl502 = false
```

The route-impact-summary option was deferred as documentation only, and broad
theorem-level local row work was deferred until a new `M_tail` gap or support
requires it.

If `wl502` is present, that selected shell has been executed:

```text
shell_bound = 6
sample_count = 8
full_rank_sample_count = 8
kernel_sample_count = 0
kernel_support_entry_count = 0
active_new_support_entry_count = 0
excluded_duplicate_or_processed_support_entry_count = 0
```

The only emitted queue outputs are:

```text
active_new_kernel_supports = []
excluded_duplicate_or_processed_supports = []
```

`wl502` remains an `M_tail` diagnostic audit only. It does not prove uniform
full rank, does not test any ambient `C_d` cover, does not apply `wl491`, does
not select a final candidate, and does not advance to `wl503`.

If `wl503` is present, the post-`wl502` empty-shell route choice has been made:

```text
completed_finite_shell_bound_after_wl502 = 6
shell6_sample_count_from_wl502 = 8
shell6_full_rank_sample_count_from_wl502 = 8
shell6_kernel_sample_count_from_wl502 = 0
shell6_active_new_support_entry_count_from_wl502 = 0
shell6_excluded_duplicate_or_processed_support_entry_count_from_wl502 = 0
active_candidate_count_after_wl502 = 0
```

The selected next narrow gate is:

```text
execute_next_finite_M_tail_shell_from_wl498_plan
```

with:

```text
entered_here = false
uses_existing_wl498_plan = true
shell_bound_to_execute_later = 7
preserve_wl498_duplicate_support_guard = true
new_shell_or_grid_refreshed_here = false
m_tail_diagnostics_extended_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_here = false
advance_to_wl504 = false
```

`wl503` is still route selection only. It does not execute shell 7, test
ambient `C_d` solubility, apply `wl491`, prove local rows, or claim uniform
`M_tail` full rank.

If `wl504` is present, that selected shell has been executed:

```text
shell_bound = 7
sample_count = 24
full_rank_sample_count = 12
kernel_sample_count = 12
kernel_support_entry_count = 14
active_new_support_entry_count = 12
excluded_duplicate_or_processed_support_entry_count = 2
```

The active outputs are `M_tail` diagnostic supports only. The two excluded
outputs are pure `u_3` support-family repeats. `wl504` does not test any
ambient `C_d` cover, does not apply `wl491`, does not select a final candidate,
does not prove a local row, and does not advance to `wl505`.

## What Not To Do Next

Do not immediately pick another `M_tail` kernel candidate before defining the
admissibility filter. That would repeat the same point-specific check and blur
ambient solubility with AA+BB admissibility.

If the filter is already defined, do not bypass it when testing the next
candidate. The next candidate must first become an ambient global `C_d` point,
then pass this filter before it can matter for AA+BB.

If `wl492` is present, do not skip straight to an unscoped new candidate. First
build the candidate queue from existing `M_tail` diagnostics, with `u_3`
excluded or deprioritized as already globally soluble but not AA+BB-admissible.

If `wl493` is present, do not re-enter `u_3` through the active queue. The
existing `wl481` queue is empty after filter-aware routing; refresh the
`M_tail` diagnostics before attempting another support.

If `wl494` is present, do not treat the refreshed `v_5` support entries as
ambient points, admissible AA+BB points, or obstruction candidates. They are
only refreshed `M_tail` kernel supports until the ambient `C_d` solubility gate
and then the wl491 admissibility filter have both been run.

If `wl495` is present, do not reprocess the four already-routed exact global
ambient points as active candidates; they are globally soluble but
not AA+BB-admissible. Also do not silently drop the two deferred `v_5` entries
or apply the wl491 filter to them before proving an ambient global `C_d` point.

If `wl496` is present, do not re-open the two `wl495` deferred `v_5` ledgers as
active deferred work. They are classified as ambient globally not soluble for
their shared `L=4,T=5,d=(5,1,5)` cover. Also do not cite `wl496` as a final
obstruction candidate, a new local row, or a Selmer theorem.

If `wl497` is present, do not treat `structure_next_M_tail_diagnostic_extension`
as already executed. It is only the selected next gate. Do not refresh a new
grid, prove a local row, test a new `C_d` solubility ledger, or select a final
candidate unless that is the explicit next task.

If `wl498` is present, do not treat the extension plan as an executed
diagnostic refresh. The next executable step must declare a finite primitive
shell with `max(A,B) > 4`, apply the route-key duplicate guard, and stop after
building the `M_tail` support queue. It must not test ambient `C_d` solubility
or apply `wl491` inside the `M_tail` extension.

If `wl499` is present, do not treat the two active `u_5` supports as ambient
global `C_d` points, AA+BB-admissible points, final obstruction candidates, or
Selmer progress. They are only `M_tail` diagnostic supports until routed
through ambient `C_d` solubility and then `wl491` where appropriate.

If `wl500` is present, do not re-open the two `wl499` active `u_5` ledgers as
active or deferred ambient-solubility work. They are classified as ambient
globally not soluble for their shared `L=5,T=8,d=(5,5,1)` cover. Also do not
cite `wl500` as an admissible point, a final obstruction candidate, a new local
row, or a Selmer theorem.

If `wl501` is present, do not treat
`execute_next_finite_M_tail_shell_from_wl498_plan` as already executed. It is
only the selected next gate. Do not refresh or execute a new shell/grid, compute
new supports, test new `C_d` solubility, apply `wl491` to a new point, select a
final obstruction candidate, or advance to `wl502` unless that is the explicit
next task.

If `wl502` is present, do not invent an ambient `C_d` route for shell 6: there
are no active shell-6 supports to route. Also do not treat the all-full-rank
shell-6 diagnostic as a uniform `M_tail` full-rank theorem or as a Selmer
upper-bound proof. The next step, if any, is a separate post-`wl502` route
choice, not `wl503` entered by `wl502`.

If `wl503` is present, do not treat shell 7 as already executed. It is only the
selected next gate. Do not refresh or execute a new shell/grid, compute new
supports, test ambient `C_d` solubility, apply `wl491` to a new point, select a
final obstruction candidate, prove a local row, or advance to `wl504` unless
that is the explicit next task.

If `wl504` is present, do not treat its active shell-7 diagnostic supports as
ambient global `C_d` points, AA+BB-admissible points, final obstruction
candidates, or Selmer progress. They must first be routed through ambient
`C_d` global solubility, then through `wl491` only where a global point is
proved. Do not re-open the two pure `u_3` excluded outputs.

If `wl505` is present, do not re-open the eight shell-7 entries already routed
as globally soluble but not AA+BB-admissible, and do not re-open the two pure
`u_3` processed exclusions. The four unresolved shell-7 entries are deferred
ambient `C_d` global-solubility ledgers, not refuted covers, not admissible
points, not final obstruction candidates, and not Selmer progress.

If `wl506` is present, do not re-open any of the 12 `wl505` active shell-7
route entries or the two pure `u_3` processed exclusions. The two `w_5`
deferred ledgers have been refuted as ambient globally not soluble, and the
two `u_7 + w_37` deferred ledgers have been routed through `wl491` as globally
soluble but not AA+BB-admissible. `wl506` is still not a final obstruction
candidate, local-row proof, Selmer upper bound, or family theorem.

If `wl507` is present, do not treat shell 8 as already executed. It is only
the selected next gate. Do not re-open shell-7 route ledgers, compute new
supports, test ambient `C_d` solubility, apply `wl491` to a new point, select
a final obstruction candidate, prove a local row, or advance to `wl508` unless
that is the explicit next task.

If `wl508` is present, do not invent an ambient `C_d` route for shell 8: there
are no active shell-8 supports to route. Also do not treat the 14 full-rank
samples, or the absence of active shell-8 supports, as a uniform `M_tail`
full-rank theorem or as a Selmer upper-bound proof. The next step, if any, is
a separate post-`wl508` route choice, not `wl509` entered by `wl508`.

If `wl509` is present but `wl510` is not present, do not treat shell 9 as
already executed. It is only the selected next gate. Do not re-open shell-8
processed `u_3` exclusions, invent a shell-8 ambient `C_d` route, compute new
supports, test ambient `C_d` solubility, apply `wl491` to a new point, select
a final obstruction candidate, prove a local row, or advance to shell 9 unless
that is the explicit next task.

If `wl510` is present but `wl511` is not present, do not treat active shell-9 `M_tail` supports as
ambient global `C_d` points, AA+BB-admissible points, final obstruction
candidates, local-row proofs, uniform `M_tail` full-rank evidence, or Selmer
theorem progress. Their next route, if explicitly entered, starts with
ambient `C_d` global solubility, not `wl491`.

If `wl511` is present but `wl512` is not present, do not re-open the four
shell-9 entries already routed as globally soluble but not AA+BB-admissible,
and do not treat the four deferred shell-9 ambient `C_d` ledgers as refuted.
They remain unresolved global-solubility ledgers, not final obstruction
candidates or theorem progress. Do not execute shell 10 unless that is the
explicit next task.

If `wl512` is present but `wl513` is not present, do not re-open the two
shell-9 `v_13` ledgers refuted there, the four shell-9 globally soluble but
not AA+BB-admissible ledgers from `wl511`, or any closed ledger through
`wl511`. The two shell-9 `u_7` ledgers remain genuinely deferred ambient
`C_d` global-solubility ledgers, not final obstruction candidates or theorem
progress. Do not execute shell 10, choose a candidate, or advance to `wl513`
unless that is the explicit next task.

If `wl513` is present but `wl514` is not present, do not treat the selected
remaining `u_7` cover resolution gate as entered. The shared
`L=7,T=16,d=(7,7,1)` cover is still unresolved until a later explicit
certificate records either an exact ambient `C_d` point or an exhaustive
no-lift result. Do not execute shell 10, re-open the `wl512` `v_13`
refutations, re-open the `wl511` not-admissible shell-9 ledgers, apply
`wl491`, prove local rows, select a final candidate, or advance to `wl514`
unless that is the explicit next task.

If `wl514` is present but `wl515` is not present, do not treat the
post-`wl514` route choice as made. The shared shell-9 `u_7` cover has been
refuted as ambient globally not soluble by the mod-17 no-lift certificate, so
`wl491` is not applied to it. Do not execute shell 10, re-open closed shell-9
ledgers, select a final candidate, prove new local rows outside this one
certificate, run broad rank/Selmer diagnostics, or advance beyond `wl514`
unless that is the explicit next task.

If `wl515` is present but `wl516` is not present, shell 10 is only the selected
next gate. Do not execute it unless that is the explicit next task. Do not
re-open any closed shell-9 ledger, apply `wl491` to a refuted cover, pivot to
proof-level row work without a named proof gap, select a final candidate, claim
uniform `M_tail` full rank, or treat finite shell diagnostics as theorem-level
Selmer progress.

If `wl516` is present, shell 10 has already been executed only as a finite
`M_tail` diagnostic extension. Do not treat its 10 active supports as ambient
global `C_d` points, AA+BB-admissible points, final obstruction candidates,
local-row proofs, uniform `M_tail` full-rank evidence, or Selmer theorem
progress. Their next route, if explicitly entered, starts with ambient `C_d`
global solubility, not `wl491`.

If `wl517` is present, those 10 active shell-10 supports have already been
routed through ambient `C_d` global solubility first. Do not re-open the eight
globally soluble but not AA+BB-admissible ledgers, do not treat the two
deferred shell-10 covers as globally not soluble without an explicit
certificate, do not execute shell 11, and do not select a final candidate or
claim Selmer progress.

If `wl518` is present, do not treat the support-family synthesis as a
certificate. It only reorganizes existing `wl491`-`wl517` ledgers by support
family and cover family, identifies the shared shell-10 `u_5`
`L=10,T=19,d=(5,5,1)` cover as the sole genuinely deferred cover family, and
selects targeted resolution of that cover as the next narrow gate. Do not
execute shell 11, resolve that cover, pivot to proof-level generalization, or
claim a family theorem unless that is the explicit next task.

If `wl519` is present, the shared shell-10 `u_5` cover has already been
resolved as ambient globally soluble by an exact rational `C_d` point, and the
two mirror entries have already failed `wl491`. Do not re-open those
not-admissible ledgers, do not execute shell 11, and do not treat the exact
point as a final obstruction candidate or as Selmer progress.

If `wl520` is present, post-`wl519` route choice has already selected
support-family / cover-family synthesis after `wl519` as the next narrow gate.
Do not treat that synthesis as entered, do not re-open `wl519` not-admissible
ledgers, shell-9 ledgers, or previous refuted covers, and do not skip straight
to shell 11, proof-level generalization, final-candidate selection, or Selmer
claims.

Do not add a new local/Hilbert row just to kill `u_3`. `wl483` found no
justified row, and `wl486` found a global point anyway.

Do not treat the `u_3` global point as a Sha-style obstruction candidate. It is
globally soluble.

Do not treat the `u_3` point as evidence for an AA+BB solution. It fails the
BB common-source square test.

## Claim Boundary

The following remain unproved:

- uniform full rank of `M_tail`;
- complete Selmer upper bound;
- `dim Sel_2(E_L/Q)=2`;
- rank zero;
- `Sha[2]=0`;
- family exclusion;
- Harborth global theorem.

The `wl493` queue is useful because it prevents re-processing `u_3` as if it
were still active. It is not, by itself, a Selmer theorem.

The `wl494` refresh is useful because it exposes new diagnostic supports beyond
`u_3` in a bounded sample grid. It is not a local-row proof, a solubility proof,
an admissibility proof, or a Selmer theorem.

The `wl495` route audit is useful because it routes every refreshed `v_5`
entry explicitly and prevents the four globally soluble but not-admissible
entries from being mistaken for AA+BB points. It still leaves two ambient
global-solubility ledgers deferred and is not a Selmer theorem.

The `wl496` resolution is useful because it closes those two deferred ledgers
as ambient globally not soluble for the shared `L=4,T=5,d=(5,1,5)` cover. It is
not a new local-row proof, not an admissible-point proof, not a final
obstruction candidate, and not a Selmer theorem.

The `wl497` route choice is useful because it prevents re-opening disposed
`u_3` or bounded `v_5` ledgers and identifies the next controllable gate at the
`M_tail` diagnostic layer. It is not itself a diagnostic extension, local-row
proof, solubility test, obstruction candidate, or Selmer theorem.

The `wl498` plan is useful because it fixes the allowed finite-shell axes,
exclusion ledger, duplicate-support guard, future output schema, and routing
contract for the next `M_tail` diagnostic extension. It is not itself a grid
refresh, support computation, solubility test, obstruction candidate, or Selmer
theorem.

The `wl499` finite shell is useful because it executes the first declared
post-`wl498` primitive shell and exposes two active `u_5` `M_tail` diagnostic
supports without reopening `u_3` or bounded `v_5`. It is not a solubility test,
not an admissibility proof, not a candidate selection, and not a Selmer theorem.

The `wl500` route audit is useful because it closes those two active `u_5`
ledgers as ambient globally not soluble for the shared `L=5,T=8,d=(5,5,1)`
cover and prevents them from being mistaken for AA+BB-admissible points. It is
not a new local-row proof, not an admissible-point proof, not a final
obstruction candidate, and not a Selmer theorem.

The `wl501` route choice is useful because it prevents re-opening `u_3`,
bounded `v_5`, or shell-5 `u_5` ledgers and identifies the next controllable
gate as the next finite `M_tail` shell from the existing `wl498` plan. It is
not itself a diagnostic extension, local-row proof, solubility test,
obstruction candidate, or Selmer theorem.

The `wl502` diagnostic extension is useful because it executes the selected
shell-6 finite primitive `M_tail` shell and records that the queue is empty
under the current row ledger. It is not a uniform `M_tail` full-rank theorem,
not an ambient `C_d` solubility audit, not an admissibility-filter result, not
a final obstruction candidate, and not a Selmer theorem.

The `wl503` route choice is useful because it prevents an empty shell from
being mistaken for either an ambient-solubility task or a uniform rank theorem,
and identifies the next controllable gate as the next finite `M_tail` shell
from the existing `wl498` plan. It is not itself a diagnostic extension,
local-row proof, solubility test, obstruction candidate, or Selmer theorem.

The `wl504` diagnostic extension is useful because it executes the selected
shell-7 finite primitive `M_tail` shell and records a concrete active support
queue while preserving the closed-ledger exclusions. It is not an ambient
`C_d` solubility audit, not an admissibility-filter result, not a local-row
proof, not a final obstruction candidate, and not a Selmer theorem.

The `wl505` route audit is useful because it routes exactly the 12 active
shell-7 `M_tail` supports through ambient `C_d` solubility before applying
`wl491`: eight have exact integral ambient witnesses and are not
AA+BB-admissible, while four remain deferred. It is not a refutation of those
four deferred covers, not an admissible-point proof, not a final obstruction
candidate, not a local-row proof, and not a Selmer theorem.

The `wl506` resolution is useful because it closes the four `wl505` deferred
ambient ledgers: two as ambient globally not soluble and two as globally
soluble but not AA+BB-admissible after `wl491`. It is not an admissible-point
proof, not a final obstruction candidate, not a local-row proof, and not a
Selmer theorem.

The `wl507` route choice is useful because it prevents re-opening disposed
shell-7 ledgers and identifies the next controllable gate as the next finite
`M_tail` shell from the existing `wl498` plan. It is not itself a diagnostic
extension, local-row proof, solubility test, obstruction candidate, or Selmer
theorem.

The `wl508` diagnostic extension is useful because it executes the selected
shell-8 finite primitive `M_tail` shell and records that no active support
queue remains after the pure `u_3` processed-support exclusions are applied.
It is not a uniform `M_tail` full-rank theorem, not an ambient `C_d`
solubility audit, not an admissibility-filter result, not a final obstruction
candidate, and not a Selmer theorem.

The `wl509` route choice is useful because it prevents re-opening the shell-8
processed `u_3` exclusions or converting an empty active shell into an ambient
route, and identifies the next controllable gate as the next finite `M_tail`
shell from the existing `wl498` plan. It is not itself a diagnostic extension,
local-row proof, solubility test, obstruction candidate, or Selmer theorem.

The `wl510` diagnostic extension is useful because it executes the selected
shell-9 finite primitive `M_tail` shell and records eight active diagnostic
supports while preserving all closed ledgers through `wl509`. It is not an
ambient `C_d` solubility audit, not an admissibility-filter result, not a final
obstruction candidate, not a local-row proof, and not a Selmer theorem.

The `wl511` route audit is useful because it routes exactly those eight
shell-9 supports through ambient `C_d` solubility before `wl491`: four exact
ambient points are filtered to globally soluble but not AA+BB-admissible, and
four covers remain genuinely deferred. It is not a final obstruction
candidate, not a local-row proof, not shell 10, and not a Selmer theorem.

The `wl512` deferred-ledger audit is useful because it classifies exactly those
four deferred shell-9 ledgers without re-opening closed shell-9 ledgers: the
two `v_13` ledgers are refuted by a targeted single-cover certificate, while
the two `u_7` ledgers remain explicitly deferred. It is not shell 10, not a
candidate-selection step, not a local-row proof, and not a Selmer theorem.

The `wl513` route-choice audit is useful because it stops the route from
widening to shell 10 while a concrete shell-9 ambient `C_d` gap remains. It
selects targeted resolution of the shared `u_7` cover as the next narrow gate,
but does not enter that gate and does not prove solubility, admissibility,
local rows, or Selmer progress.

The `wl514` ledger-resolution audit is useful because it resolves exactly that
shared shell-9 `u_7` cover by a single-cover no-lift certificate: the
Mordell-Weil image modulo 17 has empty intersection with all mod-17 cover-lift
reductions. It is not a post-resolution route choice, not shell 10, not an
admissibility-filter result, and not a Selmer theorem.

The `wl515` route-choice audit is useful because it records that all shell-9
deferred ambient `C_d` ledgers are classified, rejects a proof-level pivot
without a named proof gap, and selects the existing `wl498` finite-shell route
at `max(A,B)=10` as the next narrow gate. It does not execute shell 10, re-open
closed ledgers, apply `wl491`, select a final candidate, or prove Selmer
progress.

The `wl516` finite-shell audit is useful because it executes only the declared
shell-10 diagnostic extension, preserves every closed ledger through `wl515`,
and records the active/duplicate/processed support queues. It does not route
those supports through ambient `C_d`, apply `wl491`, select a final candidate,
or prove Selmer progress.

The `wl517` route audit is useful because it routes exactly those 10 active
shell-10 supports through ambient `C_d` solubility before applying `wl491`:
eight have exact integral ambient witnesses and are not AA+BB-admissible, and
two remain genuine deferred ambient-solubility ledgers. It does not execute
shell 11, select a final candidate, prove a local row, or prove Selmer
progress.

The `wl518` synthesis audit is useful because it reorganizes the existing
`wl491`-`wl517` route ledgers by support and cover family instead of worklog
order. It records one genuinely deferred cover family, the shared shell-10
`u_5` `L=10,T=19,d=(5,5,1)` cover, and selects targeted resolution of that
cover as the next narrow gate. It does not resolve the cover, execute shell 11,
select a final candidate, or prove Selmer progress.

The `wl519` cover-resolution audit is useful because it enters exactly that
selected shared shell-10 `u_5` gate, gives an exact rational ambient `C_d`
point, and then applies `wl491`: both mirror entries are globally soluble but
not AA+BB-admissible. It does not execute shell 11, make the post-`wl519` route
choice, select a final candidate, or prove Selmer progress.

The `wl520` route-choice audit is useful because it observes that the only
`wl518` deferred cover has now been classified and compares the four tempting
next moves: post-classification support/cover-family synthesis, shell 11,
proof-level generalization / local-row work, and final-candidate selection. It
selects the synthesis gate, but does not enter it, execute shell 11, select a
candidate, or prove Selmer progress.

## Source Trail

Read these in order:

1. `docs/work-logs/470-aa-bb-route-pivot-after-h2-audit.md`
2. `docs/work-logs/471-aa-bb-complete-d-container-definition.md`
3. `docs/work-logs/480-aa-bb-d4-uniform-matrix-rank-bound-audit.md`
4. `docs/work-logs/483-aa-bb-local-hilbert-row-decision-gate.md`
5. `docs/work-logs/486-aa-bb-local-solubility-gate.md`
6. `docs/work-logs/489-aa-bb-closure-pullback-common-source-constraints-for-global-c-d-point.md`
7. `docs/work-logs/490-aa-bb-route-impact-after-wl489-admissibility-failure.md`
8. `docs/work-logs/491-aa-bb-ambient-c-d-to-aa-bb-admissibility-filter.md`
9. `docs/work-logs/492-aa-bb-route-selection-after-admissibility-filter.md`
10. `docs/work-logs/493-aa-bb-candidate-queue-from-existing-m-tail-diagnostics.md`
11. `docs/work-logs/494-aa-bb-extend-or-refresh-m-tail-diagnostics.md`
12. `docs/work-logs/495-aa-bb-route-refreshed-support-through-ambient-c-d-solubility-then-wl491-filter.md`
13. `docs/work-logs/496-resolve-wl495-deferred-v5-ambient-c-d-global-solubility-ledgers.md`
14. `docs/work-logs/497-post-wl496-route-choice-audit.md`
15. `docs/work-logs/498-structure-next-m-tail-diagnostic-extension-plan.md`
16. `docs/work-logs/499-execute-finite-m-tail-diagnostic-extension-from-wl498-plan.md`
17. `docs/work-logs/500-route-active-u5-m-tail-supports-through-ambient-c-d-solubility-then-wl491-filter.md`
18. `docs/work-logs/501-post-wl500-route-choice-audit.md`
19. `docs/work-logs/502-execute-next-finite-m-tail-shell-from-wl498-plan.md`
20. `docs/work-logs/503-post-wl502-empty-shell-route-choice-audit.md`
21. `docs/work-logs/504-execute-next-finite-m-tail-shell-from-wl498-plan.md`
22. `docs/work-logs/505-route-active-shell7-m-tail-supports-through-ambient-c-d-solubility-then-wl491-filter.md`
23. `docs/work-logs/506-resolve-shell7-deferred-ambient-c-d-global-solubility-ledgers.md`
24. `docs/work-logs/507-post-wl506-route-choice-audit.md`
25. `docs/work-logs/508-execute-next-finite-m-tail-shell-from-wl498-plan.md`
26. `docs/work-logs/509-post-wl508-empty-shell-route-choice-audit.md`
27. `docs/work-logs/510-execute-next-finite-m-tail-shell-from-wl498-plan.md`
28. `docs/work-logs/511-route-active-shell9-m-tail-supports-through-ambient-c-d-solubility-then-wl491-filter.md`
29. `docs/work-logs/512-resolve-shell9-deferred-ambient-c-d-global-solubility-ledgers.md`
30. `docs/work-logs/513-post-wl512-route-choice-audit.md`
31. `docs/work-logs/514-resolve-remaining-shell9-u7-ambient-c-d-global-solubility-ledger.md`
32. `docs/work-logs/515-post-wl514-route-choice-audit.md`
33. `docs/work-logs/516-execute-next-finite-m-tail-shell-from-wl498-plan.md`
34. `docs/work-logs/517-route-active-shell10-m-tail-supports-through-ambient-c-d-solubility-then-wl491-filter.md`
35. `docs/work-logs/518-support-family-synthesis-after-wl517.md`
36. `docs/work-logs/519-resolve-shared-shell10-u5-ambient-c-d-global-solubility-cover.md`
37. `docs/work-logs/520-post-wl519-route-choice-audit.md`
