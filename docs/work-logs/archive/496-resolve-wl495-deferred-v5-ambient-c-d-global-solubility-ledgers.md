# Resolve Wl495 Deferred v_5 Ambient C_d Global-Solubility Ledgers

## Question

Using `wl495` as input, can the two deferred refreshed `v_5` ambient
`C_d` global-solubility ledgers be classified without selecting a final
obstruction candidate or advancing the route?

The two entries are:

```text
AA_A4_B1_v_5_m_tail_refresh_candidate
BB_A1_B4_v_5_m_tail_refresh_candidate
```

They have the same instantiated complete `d`-cover data:

```text
L = 4
T = 5
d = (5,1,5)
```

This work-log touches only:

```text
wl495 deferred route ledgers
complete d-coordinate C_d cover
ambient C_d global solubility
AA+BB admissibility gate routing
```

It does not touch the old package-`x` / `S~` pseudo-container and does not
claim anything about theorem-level `Sel_2(E_L/Q)`.

## Inputs

The input is:

```text
wl495 routed_refreshed_supports
```

Only entries already classified by `wl495` as:

```text
ambient_c_d_global_solubility_status = global_solubility_deferred
aa_bb_admissibility_status = not_applied_ambient_global_solubility_unproved
ledger_route = ambient_c_d_solubility_deferred_ledger
```

are eligible. The two target entries are kept explicitly and in order.

## Certificate

For `L=4,T=5,d=(5,1,5)`, the cover equations are:

```text
X + 78 = 5*u_minus_p^2
X - 178 = u_pos_2sqrt_q^2
X + 178 = 5*u_neg_2sqrt_q^2
```

Their product maps any rational cover point to the single elliptic curve:

```text
V^2 = (X + 78)(X - 178)(X + 178)
    = X^3 + 78*X^2 - 31684*X - 2471352
```

with:

```text
V = 5*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q
```

The targeted single-curve Mordell-Weil certificate recorded here is:

```text
rank = 0
torsion points = O, (-178,0), (-78,0), (178,0)
```

This is only a certificate for this instantiated auxiliary curve. It is not a
family rank-zero theorem, not a Selmer upper bound, and not a family exclusion.

None of the listed torsion points lifts to the `d=(5,1,5)` cover:

```text
O:       infinity would require 5*u_minus_p^2 = u_pos_2sqrt_q^2
         with 5 a rational square, impossible.
(-178): X - 178 = -356 = u_pos_2sqrt_q^2, impossible over Q.
(-78):  X - 178 = -256 = u_pos_2sqrt_q^2, impossible over Q.
(178):  X + 78 = 256 = 5*u_minus_p^2, so 256/5 would be a square, impossible.
```

Therefore this instantiated ambient `C_d` cover has no rational point.

## Route Result

Both deferred entries are explicitly classified:

```text
wl495_deferred_entry_count = 2
explicitly_classified_entry_count = 2
ambient_globally_soluble_count = 0
ambient_global_solubility_refuted_count = 2
ambient_global_solubility_still_deferred_count = 0
wl491_filter_applied_count = 0
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 0
aa_bb_filter_not_applied_count = 2
```

Both entries route to:

```text
ambient_c_d_global_solubility_status = globally_not_soluble
aa_bb_admissibility_status = not_applied_ambient_global_solubility_refuted
ledger_route = ambient_c_d_global_solubility_refuted_ledger
```

The `wl491` filter is not applied, because there is no ambient global
`C_d` point to filter.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl496_resolve_wl495_deferred_v5_ambient_c_d_global_solubility_ledgers.json
```

with:

```text
status = ok
work_log = wl496
input_work_log = wl495
resolved_wl495_deferred_ledgers_here = true
all_wl495_deferred_entries_resolved_here = true
candidate_selected_here = false
new_m_tail_row_proved_here = false
new_local_row_proved_here = false
broad_rank_or_selmer_diagnostics_run = false
family_rank_or_selmer_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
advance_to_wl497 = false
```

## Boundary

This work-log stops after `wl496`. It does not prove:

- a new `M_tail` row;
- a new local/Hilbert row;
- an AA+BB-admissible refreshed point;
- a final obstruction candidate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero as a family theorem;
- `Sha[2]=0`;
- any family exclusion theorem.

The two `wl495` deferred ledgers are no longer active deferred ambient
solubility gaps. The next route choice is deliberately not selected here.
