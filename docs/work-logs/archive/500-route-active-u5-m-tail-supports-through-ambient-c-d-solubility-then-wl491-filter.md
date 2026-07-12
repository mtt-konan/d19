# Route Active u_5 M_tail Supports Through Ambient C_d Solubility Then wl491 Filter

## Question

Using `wl499` as input, how do the two active shell-5 `u_5` `M_tail`
diagnostic supports route after the required ambient `C_d` global-solubility
gate, and should the `wl491` AA+BB admissibility filter be applied?

The two entries are exactly:

```text
AA_A5_B3_u_5_m_tail_shell5_candidate
BB_A3_B5_u_5_m_tail_shell5_candidate
```

This work-log touches only:

```text
wl499 active M_tail support entries
complete d-coordinate C_d cover
ambient C_d global solubility
AA+BB admissibility gate routing
```

It does not touch the old package-`x` / `S~` pseudo-container and does not
claim anything about theorem-level `Sel_2(E_L/Q)`.

## Inputs

The input is:

```text
wl491 reusable ambient C_d to AA+BB admissibility filter
wl499 active_new_kernel_supports
```

Only entries already classified by `wl499` as:

```text
ambient_c_d_global_solubility_status = not_tested_here
aa_bb_admissibility_status = not_applied_here
ledger_route = m_tail_shell_support_pending_ambient_C_d_solubility
```

are eligible. The two target entries are kept explicitly and in order.

## Certificate

Both `u_5` entries instantiate the same complete `d`-cover data:

```text
L = 5
T = 8
d = (5,5,1)
```

The cover equations are:

```text
X + 72 = 5*u_minus_p^2
X - 328 = 5*u_pos_2sqrt_q^2
X + 328 = u_neg_2sqrt_q^2
```

Their product maps any rational cover point to the single elliptic curve:

```text
V^2 = (X + 72)(X - 328)(X + 328)
    = X^3 + 72*X^2 - 107584*X - 7746048
```

with:

```text
V = 5*u_minus_p*u_pos_2sqrt_q*u_neg_2sqrt_q
```

The targeted single-curve Mordell-Weil certificate recorded here is:

```text
rank = 0
torsion points = O, (-328,0), (-72,0), (328,0)
```

This is only a certificate for this instantiated auxiliary curve. It is not a
family rank-zero theorem, not a Selmer upper bound, and not a family exclusion.

None of the listed torsion points lifts to the `d=(5,5,1)` cover:

```text
O:       infinity would require 5*u_minus_p^2 = 5*u_pos_2sqrt_q^2
         = u_neg_2sqrt_q^2, forcing 5 to be a rational square.
(-328): X + 72 = -256 = 5*u_minus_p^2, impossible over Q.
(-72):  X - 328 = -400 = 5*u_pos_2sqrt_q^2, impossible over Q.
(328):  X + 72 = 400 = 5*u_minus_p^2, so 80 would be a square,
         impossible over Q.
```

Therefore this instantiated ambient `C_d` cover has no rational point.

## Route Result

Both active `u_5` entries are explicitly classified:

```text
active_u5_support_entry_count = 2
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
results/closure_quotient_rank_zero_aa_bb_wl500_route_active_u5_m_tail_supports_through_ambient_c_d_solubility_then_wl491_filter.json
```

with:

```text
status = ok
work_log = wl500
input_work_logs = wl491, wl499
route_audit_built_here = true
all_active_u5_entries_classified_here = true
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
advance_to_wl501 = false
```

## Boundary

This work-log stops after `wl500`. It does not prove:

- a new `M_tail` row;
- a new local/Hilbert row;
- an AA+BB-admissible active `u_5` point;
- a final obstruction candidate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero as a family theorem;
- `Sha[2]=0`;
- any family exclusion theorem.

The two active `wl499` `u_5` ledgers are no longer active deferred ambient
solubility gaps. No post-`wl500` route choice is entered here.
