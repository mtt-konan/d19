# Resolve Remaining Shell-9 u_7 Ambient C_d Global-Solubility Ledger

## Question

Using `wl513` as input, can the remaining shared shell-9 `u_7` ambient
`C_d` cover at `L=7,T=16,d=(7,7,1)` be resolved by an exact ambient point or
an exhaustive no-lift certificate?

This enters only the selected `wl513` gate. It does not execute shell 10, does
not re-open the `wl512` `v_13` refutations, does not re-open the `wl511`
globally soluble but not AA+BB-admissible shell-9 ledgers, does not make the
post-`wl514` route choice, does not select a final obstruction candidate, does
not apply `wl491`, and does not run broad rank/Selmer diagnostics.

## Inputs

The input is:

```text
wl513 post-wl512 route choice audit
```

The touched object layer is:

```text
ambient complete d-coordinate C_d global solubility for one shared cover
```

not the old package-`x` / `S~` pseudo-container, not a new `M_tail`
diagnostic extension, not AA+BB admissibility, and not theorem-level
`Sel_2(E_L/Q)`.

The only two ledgers resolved here are:

```text
AA_A7_B9_u_7_m_tail_shell9_candidate
BB_A9_B7_u_7_m_tail_shell9_candidate
```

They share the cover:

```text
L = 7
T = 16
d = (7, 7, 1)
X + 120 = 7*u_minus_p^2
X - 904 = 7*u_pos_2sqrt_q^2
X + 904 = u_neg_2sqrt_q^2
```

The associated elliptic curve is:

```text
V^2 = (X + 120)(X - 904)(X + 904)
    = X^3 + 120*X^2 - 817216*X - 98065920
```

## Certificate

The single-curve Mordell-Weil certificate used for this cover records:

```text
rank = 1
G = (1032,16896)
E(Q)[2] = {O, (-904,0), (-120,0), (904,0)}
E(Q) = <G> + E(Q)[2]
```

This is a certificate for the one instantiated ambient curve only. It is not a
family rank theorem and is not theorem-level Selmer progress.

Modulo `17`, the curve has good reduction:

```text
y^2 = (x + 1)(x - 3)(x + 3)
G mod 17 = (12,15)
order(G mod 17) = 6
```

The full rational reduction image from `<G> + E(Q)[2]` has 12 points:

```text
O,
(0,5), (0,12),
(1,1), (1,16),
(3,0),
(8,6), (8,11),
(12,2), (12,15),
(14,0),
(16,0)
```

The `d=(7,7,1)` cover lift conditions modulo `17` require:

```text
(x + 120)/7, (x - 904)/7, x + 904
```

to be squares or zero in `F_17`. The reductions on the elliptic curve satisfying
those three local lift conditions are:

```text
(6,6), (6,11),
(10,7), (10,10),
(13,8), (13,9)
```

The intersection with the rational reduction image is empty. The point at
infinity is also blocked because `7` is not a square modulo `17`.

Therefore the shared instantiated ambient `C_d` cover has no rational point.
Both `u_7` ledgers route to:

```text
ambient globally not soluble
```

Because ambient global solubility is refuted, the `wl491` AA+BB admissibility
filter is not applied.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl514_resolve_remaining_shell9_u7_ambient_c_d_global_solubility_ledger.json
```

with:

```text
status = ok
work_log = wl514
input_work_log = wl513
wl513_remaining_deferred_candidate_count = 2
shared_cover_count_resolved_here = 1
classified_candidate_entry_count = 2
ambient_globally_soluble_count = 0
ambient_global_solubility_refuted_count = 2
exhaustive_no_lift_certificate_count = 1
wl491_filter_applied_count = 0
aa_bb_admissible_count = 0
aa_bb_filter_not_applied_count = 2
shell10_executed_here = false
post_wl514_route_choice_made_here = false
candidate_selected_here = false
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
advance_to_wl515 = false
```

## Boundary

This work-log stops after `wl514`. It proves only a targeted single-cover
ambient non-solubility result for the shared shell-9 `u_7` cover. It does not
prove:

- AA+BB admissibility for any shell-9 support;
- a final obstruction candidate;
- a new local/Hilbert row outside this one no-lift certificate;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The selected `wl513` gate is now resolved. The next route choice after all
shell-9 deferred ambient `C_d` ledgers have been classified is not made here.
