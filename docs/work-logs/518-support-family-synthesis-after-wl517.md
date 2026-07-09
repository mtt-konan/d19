# Support Family Synthesis After wl517

## Question

Using `wl517` as the immediate input, what does the AA+BB route look like if
the existing `wl491`-`wl517` ledgers are aggregated by support family and cover
family instead of by worklog order?

This is a synthesis audit only. It does not execute shell 11, does not resolve
the two shell-10 deferred covers, does not run broad rank or Selmer
diagnostics, does not select a final obstruction candidate, and does not enter
a proof-level generalization task.

## Inputs

The input ledger interval is:

```text
wl491, wl492, wl493, wl494, wl495, wl496, wl497, wl498, wl499,
wl500, wl501, wl502, wl503, wl504, wl505, wl506, wl507, wl508,
wl509, wl510, wl511, wl512, wl513, wl514, wl515, wl516, wl517
```

The touched object layers are:

```text
M_tail diagnostic support ledgers
complete d-coordinate ambient C_d cover ledgers
wl491 AA+BB admissibility-filter output ledgers
```

This is not the old package-`x` / `S~` pseudo-container and not a
theorem-level `Sel_2(E_L/Q)` upper-bound argument.

## Family Synthesis

The final candidate-ledger snapshot through `wl517` has:

```text
final_candidate_ledger_entry_count = 43
support_family_count = 13
cover_family_count = 22
refuted_entry_count = 10
globally_soluble_but_not_aa_bb_admissible_entry_count = 27
genuinely_deferred_entry_count = 2
already_closed_entry_count = 4
aa_bb_admissible_entry_count = 0
```

The only genuinely deferred cover family is:

```text
support = u_5
L = 10
T = 19
d = (5, 5, 1)

AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
```

The support-family pattern worth preserving is not a theorem. It is only a
candidate pattern:

```text
u_5 support family:
  shell-5 L=5,T=8,d=(5,5,1) cover = refuted
  shell-10 L=10,T=11,d=(5,5,1) mirror cover = globally soluble but not AA+BB-admissible
  shell-10 L=10,T=19,d=(5,5,1) mirror cover = genuinely deferred
```

This pattern says where the next narrow audit should focus. It does not prove
a family exclusion, a Selmer bound, or rank zero.

## Route Choice

The selected next narrow gate is:

```text
resolve_shared_shell10_u5_ambient_C_d_global_solubility_cover
```

with:

```text
candidate_ids =
  AA_A10_B9_u_5_m_tail_shell10_candidate
  BB_A9_B10_u_5_m_tail_shell10_candidate

shared_cover = L=10,T=19,d=(5,5,1)
allowed_future_certificates =
  exact_ambient_C_d_global_point
  exhaustive_no_lift_certificate
```

The alternative proof-level generalization task is deferred until this
remaining shared shell-10 cover is classified.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl518_support_family_synthesis_after_wl517.json
```

with:

```text
status = ok
work_log = wl518
input_work_log = wl517
support_family_synthesis_built_here = true
new_c_d_solubility_tested_here = false
resolved_shell10_deferred_covers_here = false
shell11_executed_here = false
candidate_selected_here = false
advance_to_wl519 = false
```

## Boundary

This work-log stops after `wl518`. It does not prove:

- ambient global solubility or insolubility for the shared shell-10 `u_5`
  cover;
- AA+BB admissibility for any shell-10 support;
- a final obstruction candidate;
- a new local/Hilbert row;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The next gap is to resolve the shared shell-10 `u_5` ambient `C_d` cover. That
gate is selected here but not entered.
