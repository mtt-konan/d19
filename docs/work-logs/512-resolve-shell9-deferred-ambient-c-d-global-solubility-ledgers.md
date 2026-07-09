# Resolve Shell-9 Deferred Ambient C_d Global-Solubility Ledgers

## Question

Using `wl511` as input, what can be recorded for exactly the four deferred
shell-9 ambient `C_d` global-solubility ledgers?

This is a deferred-ledger audit only. It does not re-open the four shell-9
globally soluble but not AA+BB-admissible ledgers from `wl511`, does not
re-open any closed ledger through `wl511`, does not execute shell 10, does not
select a final obstruction candidate, does not prove local rows, does not run
broad rank/Selmer diagnostics, and does not advance to the next route.

## Inputs

The input is:

```text
wl491 reusable ambient C_d to AA+BB admissibility filter
wl511 active shell-9 M_tail support ambient route output
```

The touched object layers are:

```text
ambient complete d-coordinate C_d solubility
AA+BB admissibility filter policy after ambient solubility is established
M_tail diagnostic support route bookkeeping
```

not the old package-`x` / `S~` pseudo-container and not theorem-level
`Sel_2(E_L/Q)`.

## Target Deferred Ledgers

The classified deferred ledgers are exactly:

```text
AA_A4_B9_v_13_m_tail_shell9_candidate
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B4_v_13_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

The four globally soluble but not AA+BB-admissible shell-9 ledgers from `wl511`
are preserved and not re-opened.

## Route Output

The two `v_13` entries share the cover:

```text
L = 4
T = 13
d = (13, 1, 13)
X - 210 = 13*u_minus_p^2
X - 466 = u_pos_2sqrt_q^2
X + 466 = 13*u_neg_2sqrt_q^2
```

Their ambient elliptic curve model is:

```text
V^2 = (X - 210)(X - 466)(X + 466)
    = X^3 - 210*X^2 - 217156*X + 45602760
```

The targeted Mordell-Weil certificate records rank `0` and torsion points:

```text
O, (-466,0), (210,0), (466,0)
```

None lifts to the `d=(13,1,13)` cover. Therefore the two `v_13` ledgers route
to:

```text
ambient globally not soluble
```

The two `u_7` entries share the cover:

```text
L = 7
T = 16
d = (7, 7, 1)
X + 120 = 7*u_minus_p^2
X - 904 = 7*u_pos_2sqrt_q^2
X + 904 = u_neg_2sqrt_q^2
```

Their ambient elliptic curve model is:

```text
V^2 = (X + 120)(X - 904)(X + 904)
    = X^3 + 120*X^2 - 817216*X - 98065920
```

This model has a recorded single-curve rank-one status with generator
`G=(1032,16896)`, but `wl512` records no exact cover point and no exhaustive
Mordell-Weil sieve / no-lift certificate. The bounded multiple probe is route
information only and is not a global insolubility proof. Therefore these two
ledgers remain:

```text
ambient C_d global-solubility deferred
```

No `wl512` entry is AA+BB-admissible. The `wl491` filter is not applied here
because no `wl512` entry has ambient `C_d` global solubility established.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl512_resolve_shell9_deferred_ambient_c_d_global_solubility_ledgers.json
```

with:

```text
status = ok
work_log = wl512
input_work_logs = wl491, wl511
wl511_deferred_entry_count = 4
explicitly_classified_entry_count = 4
ambient_globally_soluble_count = 0
ambient_global_solubility_refuted_count = 2
ambient_global_solubility_still_deferred_count = 2
wl491_filter_applied_count = 0
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 0
candidate_selected_here = false
new_m_tail_row_proved_here = false
new_local_row_proved_here = false
broad_rank_or_selmer_diagnostics_run = false
family_rank_or_selmer_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
uniform_m_tail_full_rank_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
shell10_executed_here = false
advance_to_wl513 = false
```

## Boundary

This work-log stops after `wl512`. It proves only a targeted single-cover
ambient non-solubility result for the shared `v_13` shell-9 cover. It does not
prove:

- ambient global solubility or non-solubility for the two `u_7` shell-9 covers;
- AA+BB admissibility for any shell-9 support;
- a final obstruction candidate;
- a new local/Hilbert row;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The remaining gap is the two `u_7` shell-9 ambient `C_d` global-solubility
deferred ledgers. The next roadmap step is not entered here.
