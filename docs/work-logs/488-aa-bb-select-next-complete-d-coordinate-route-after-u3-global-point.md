# AA+BB Select Next Complete d-Coordinate Route After u_3 Global Point

## Question

Using `wl487` as input, what is the next narrow AA+BB complete
`d`-coordinate route after the `u_3` candidate

```text
d = (3, 3, 1)
```

was represented by a global point that is not in the visible rational
two-torsion baseline?

This is a routing audit only. It does not enter the selected next gate.

## Input from wl487

`wl487` recorded that the `AA, A=3, B=1` candidate

```text
AA_A3_B1_u_3_complete_d_candidate
```

is globally soluble on the explicit `C_d` cover. The induced point on

```text
E_L: Y^2=(X+p)*(X^2-4*q)
```

has complete `d`-coordinate squareclass

```text
(3, 3, 1)
```

and is classified only as

```text
non_torsion_candidate_not_visible_two_torsion_baseline
```

This is not a full Mordell-Weil torsion computation and not a rank computation.

## What the Point Changes

The point changes the route ledger in exactly these ways:

```text
remove_u3_from_current_global_obstruction_candidate_ledger
record_u3_as_globally_soluble_complete_d_coordinate_class_for_this_sample
promote_the_next_question_from_local_obstruction_to_AA_BB_admissibility
```

It does not change:

```text
M_tail_uniform_full_rank_missing_remains_unproved
no_new_local_or_hilbert_row_is_added
visible_torsion_baseline_is_not_enlarged_here
no_complete_selmer_upper_bound_or_rank_zero_conclusion_is_proved
```

So `wl488` does not reopen the `M_tail` full-rank rescue path and does not
promote the global point to a family theorem.

## Route Choice

The selected next narrow gate is:

```text
AA_BB_closure_pullback_common_source_constraints_for_global_C_d_point
```

with:

```text
entered_here = false
```

The reason is first-principles route control: the failed `u_3` obstruction
attempt produced a global non-baseline `C_d` point. Before testing another
candidate, the next controllable question is whether such a point is admissible
for the AA+BB common source and closure/pullback constraints, or whether it is
only an ambient point on `E_L`.

## Deferred Options

`wl488` defers choosing another `M_tail` or kernel candidate because `wl487`
found no new row and did not reopen the uniform full-rank route.

`wl488` also defers another minimal complete `C_d` obstruction test. Such tests
remain allowed later, but they should come after the route separates globally
soluble `C_d` classes that are AA+BB-admissible from classes that only live on
the ambient elliptic curve.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl488_select_next_complete_d_coordinate_route_after_u3_global_point.json
```

with:

```text
status = ok
work_log = wl488
input_work_log = wl487
u3_global_point_impact.point_classification =
  non_torsion_candidate_not_visible_two_torsion_baseline
route_options.inspect_AA_BB_closure_pullback_common_source_constraints.decision =
  selected_next_narrow_gate
selected_next_gate.gate =
  AA_BB_closure_pullback_common_source_constraints_for_global_C_d_point
selected_next_gate.entered_here = false
routing_audit_only = true
broad_rank_or_selmer_diagnostics_run = false
single_curve_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
package_x_s_tilde_bridge_used = false
```

## Boundary

This work-log stops after selecting the next route gate. It does not prove:

- that the global point satisfies or fails the AA+BB closure/pullback/common
  source constraints,
- a new `M_tail` row or full-rank theorem,
- another complete `C_d` obstruction,
- a full Mordell-Weil torsion classification,
- Mordell-Weil rank,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
