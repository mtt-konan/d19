# wl491-wl522 AA+BB Admissibility Taxonomy Consolidated

## Scope

This consolidated worklog is the compact route record for the `wl491`-`wl522`
interval. It replaces the need to read each short gate-selection worklog before
understanding the current handoff.

The interval stays inside the complete `d`-coordinate route:

```text
ambient C_d point
  -> AA+BB common-source admissibility filter (wl491)
  -> M_tail diagnostic queue
  -> finite shell support routing
  -> support/cover taxonomy checkpoint (wl522)
```

It is not the old package-`x` / `S~` bridge, and it is not a theorem-level
`Sel_2(E_L/Q)` upper-bound argument.

## Inputs

The interval starts with `wl491`, which defines the reusable filter:

```text
classify_ambient_c_d_point_for_aa_bb_admissibility
```

That filter must be applied before any ambient `C_d` global point enters an
AA+BB admissible-point ledger. The known `u_3` ambient point is globally
soluble, but it is only diagnostic because it fails the opposite-side
common-source square condition.

The interval then uses `M_tail` diagnostics and finite primitive shells to
produce, route, classify, or close support/cover ledgers through `wl521`.

## Route Summary

The useful route shape is:

```text
wl491  define reusable ambient C_d -> AA+BB admissibility filter
wl492  choose candidate-queue routing after known ambient points are filtered
wl493  build existing-diagnostic queue; active queue is empty
wl494  refresh bounded M_tail diagnostics; v_5 supports appear
wl495  route v_5 supports through ambient solubility and wl491 where allowed
wl496  close remaining v_5 deferred cover as ambient globally not soluble
wl497  choose structured M_tail extension
wl498  define finite shell extension plan and duplicate guard
wl499  execute shell 5 M_tail diagnostic
wl500  close shell 5 u_5 cover as ambient globally not soluble
wl501  choose shell 6
wl502  execute shell 6; active queue empty
wl503  choose shell 7
wl504  execute shell 7; active supports appear
wl505  route shell 7 supports; some not-admissible, some deferred
wl506  resolve shell 7 deferred covers
wl507  choose shell 8
wl508  execute shell 8; active queue empty
wl509  choose shell 9
wl510  execute shell 9; active supports appear
wl511  route shell 9 supports; some not-admissible, some deferred
wl512  resolve v_13 shell 9 covers; u_7 shell 9 remains deferred
wl513  choose targeted u_7 cover resolution
wl514  refute remaining u_7 cover by no-lift certificate
wl515  choose shell 10
wl516  execute shell 10; active supports appear
wl517  route shell 10 supports; two covers remain deferred
wl518  synthesize support/cover families; choose shared u_5 cover resolution
wl519  resolve shared shell-10 u_5 cover as global but not-admissible
wl520  choose post-classification support/cover synthesis
wl521  synthesize final candidate ledger and select only later shell 11
wl522  compress taxonomy and isolate the common-source lemma candidate
```

## Current Taxonomy

`wl522` records:

```text
final_candidate_ledger_entry_count = 43
support_family_count = 13
cover_family_count = 22
ambient_globally_not_soluble_cover_family_count = 5
globally_soluble_but_not_aa_bb_admissible_cover_family_count = 15
processed_or_duplicate_cover_family_count = 2
genuinely_deferred_cover_family_count = 0
aa_bb_admissible_cover_family_count = 0
```

The important separation is:

- `ambient_globally_not_soluble`: the ambient `C_d` cover is refuted, so
  `wl491` is not applicable.
- `common_source_aa_bb_admissibility_failure`: the ambient `C_d` cover is
  globally soluble, but the AA+BB common-source square check fails.
- `processed_or_duplicate_m_tail_support`: finite `M_tail` bookkeeping only.

## Current Lemma Candidate

The only named theorem-candidate isolated by the interval is:

```text
common_source_square_obstruction_for_globally_soluble_not_admissible_cover_families
```

This is only a theorem-candidate. It says what to try next: prove that the
recorded opposite-side AA/BB common-source product-not-square failures form a
reusable admissibility obstruction lemma.

## Boundary

This interval does not prove:

- the common-source square obstruction lemma;
- a new local/Hilbert row;
- uniform `M_tail` full rank;
- ambient solubility for any new `C_d` class after `wl522`;
- AA+BB admissibility for any new support;
- a final obstruction candidate;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The next narrow gate is:

```text
try_common_source_square_obstruction_lemma_candidate_not_entered_here
```

Do not execute shell 11 unless the user explicitly chooses that route.
