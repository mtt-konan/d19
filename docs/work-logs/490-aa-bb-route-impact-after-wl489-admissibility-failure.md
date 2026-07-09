# AA+BB Route Impact After wl489 Admissibility Failure

## Question

Using `wl489` as input, what changes after the explicit `u_3` / `d=(3,3,1)`
global `C_d` point is proved to fail the AA+BB common-source constraints?

This is a routing audit only. It updates the point ledgers and chooses the next
narrow route. It does not define the next filter or test another candidate.

## Input From wl489

`wl489` proved, only for the explicit `AA, A=3, B=1` point:

```text
candidate_id = AA_A3_B1_u_3_complete_d_candidate
d = (3, 3, 1)
X = 152
Y = 1536
```

The point is a genuine ambient global `C_d` point and pulls back to the `AA`
closure quotient:

```text
N = 4
M = 0
quartic_y = 15
```

But the same common-source variables fail on the `BB` side:

```text
(N^2+B^2)*(M^2+B^2) = 17
```

which is not a rational square. Thus `wl489` has status:

```text
proved_fails_for_this_explicit_point
```

## Ledger Update

`wl490` records that the explicit point is killed by AA+BB common-source
constraints, so it must be removed from both ledgers that would otherwise make
it look route-active:

```text
remove_from_current_obstruction_candidate_ledger = true
remove_from_admissible_point_ledger = true
```

After `wl490`:

```text
current_obstruction_candidate_ledger_after_wl490 = []
admissible_point_ledger_after_wl490 = []
```

The point is retained only in the separate diagnostic ledger:

```text
globally_soluble_but_not_aa_bb_admissible_ledger =
  AA_A3_B1_u_3_complete_d_candidate, d=(3,3,1)
```

This avoids both mistakes:

- treating a globally soluble ambient `C_d` point as an obstruction candidate,
- treating a globally soluble ambient `C_d` point as an AA+BB-admissible point.

## Route Choice

The selected next narrow gate is:

```text
define_reusable_ambient_C_d_to_AA_BB_admissibility_filter
```

with:

```text
entered_here = false
```

The reason is that `wl489` killed the first ambient global `C_d` point by
AA+BB common-source constraints. Before returning to `M_tail` / kernel
classification for another candidate, the route needs a reusable filter that
every later ambient `C_d` point must pass before entering the admissible-point
ledger.

## Deferred Option

Returning to `M_tail` / kernel classification for another candidate remains
allowed later, but `wl490` defers it. Choosing another candidate before a
reusable admissibility filter would repeat the `wl489` point-specific check and
blur the distinction between ambient solubility and AA+BB admissibility.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl490_route_impact_after_wl489_admissibility_failure.json
```

with:

```text
status = ok
work_log = wl490
input_work_log = wl489
ledger_update.remove_from_current_obstruction_candidate_ledger = true
ledger_update.remove_from_admissible_point_ledger = true
selected_next_gate.gate =
  define_reusable_ambient_C_d_to_AA_BB_admissibility_filter
selected_next_gate.entered_here = false
routing_audit_only = true
point_level_admissibility_decided_here = false
new_m_tail_or_kernel_candidate_selected_here = false
admissibility_filter_defined_here = false
broad_rank_or_selmer_diagnostics_run = false
single_curve_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
advance_to_wl491 = false
```

## Boundary

This work-log stops after `wl490`. It does not prove:

- that every ambient `C_d` point fails AA+BB admissibility,
- a reusable ambient-`C_d`-to-AA+BB admissibility filter,
- a new `M_tail` row or full-rank theorem,
- a new `M_tail` / kernel candidate,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
