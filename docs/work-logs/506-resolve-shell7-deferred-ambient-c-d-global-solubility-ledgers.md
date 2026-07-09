# Resolve Shell-7 Deferred Ambient C_d Global-Solubility Ledgers

## Question

Using `wl505` as input, can the four remaining shell-7 ambient `C_d`
global-solubility ledgers be resolved without re-opening the eight shell-7
globally soluble but not AA+BB-admissible ledgers or the two pure `u_3`
processed exclusions?

This work-log touches only:

```text
wl505 deferred shell-7 ambient C_d ledgers
targeted single-cover global-solubility certificates
wl491 AA+BB admissibility filter, only after ambient global solubility is proved
```

It does not touch the old package-`x` / `S~` pseudo-container and does not
claim anything about theorem-level `Sel_2(E_L/Q)`.

## Inputs

The input is:

```text
wl491 reusable ambient C_d to AA+BB admissibility filter
wl505 ambient C_d solubility deferred ledgers
```

Only these four `wl505` entries are eligible:

```text
AA_A4_B7_w_5_m_tail_shell7_candidate
AA_A7_B3_u_7_plus_w_37_m_tail_shell7_candidate
BB_A3_B7_u_7_plus_w_37_m_tail_shell7_candidate
BB_A7_B4_w_5_m_tail_shell7_candidate
```

The eight `wl505` exact ambient points already routed through `wl491` as
not AA+BB-admissible are not re-opened. The two pure `u_3` processed exclusions
also remain not re-opened.

## Resolution Result

The audit resolves all four deferred ledgers:

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

The two `w_5` ledgers share:

```text
L = 4
T = 11
d = (1,5,5)
```

They are routed to:

```text
ambient_c_d_global_solubility_status = globally_not_soluble
aa_bb_admissibility_status = not_applied_ambient_global_solubility_refuted
ledger_route = ambient_c_d_global_solubility_refuted_ledger
```

The certificate is a targeted single-cover Mordell-Weil torsion-lift
refutation for:

```text
V^2 = (X - 114)(X - 370)(X + 370)
```

The two `u_7 + w_37` ledgers share:

```text
L = 7
T = 10
d = (7,259,37)
```

They are globally soluble by an exact cover-lift point induced by:

```text
G = (-304,5376)
T = (-592,0)
P = -49*G + T
```

on the single curve:

```text
V^2 = (X + 192)(X - 592)(X + 592)
```

The exact rational point is large and is recorded in the result JSON. After
ambient global solubility is established, both entries are passed through
`wl491` and route to:

```text
globally_soluble_but_not_aa_bb_admissible_ledger
```

No AA+BB-admissible point is produced.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl506_resolve_shell7_deferred_ambient_c_d_global_solubility_ledgers.json
```

with:

```text
status = ok
work_log = wl506
input_work_logs = wl491, wl505
resolved_wl505_deferred_ledgers_here = true
all_wl505_deferred_entries_resolved_here = true
candidate_selected_here = false
new_m_tail_row_proved_here = false
new_local_row_proved_here = false
broad_rank_or_selmer_diagnostics_run = false
family_rank_or_selmer_diagnostics_run = false
single_curve_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
uniform_m_tail_full_rank_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
advance_to_wl507 = false
```

## Boundary

This work-log stops after `wl506`. It does not prove:

- a new `M_tail` row;
- a new local/Hilbert row;
- an AA+BB-admissible shell-7 point;
- a final obstruction candidate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero as a family theorem;
- `Sha[2]=0`;
- any family exclusion theorem.

The four `wl505` deferred ambient ledgers are no longer unresolved. No
post-`wl506` route choice is entered here.
