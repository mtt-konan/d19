# AA+BB u_3 Obstruction Route Entry Audit

## Question

Using `wl483` as input, what is the explicit obstruction-candidate datum for
the `AA, A=3, B=1` complete `d`-coordinate tail support

```text
u_3
```

and which obstruction workflow gate should be entered next?

This is a routing audit only. It does not prove the obstruction.

## Candidate Datum

`WL484_u3_obstruction_route_entry_audit` records the candidate

```text
AA_A3_B1_u_3_complete_d_candidate
```

for

```text
E_L: Y^2=(X+p)*(X^2-4*q).
```

The sample parameters are:

```text
side = AA
A = 3
B = 1
L = 3
T = 4
sqrt_q = 52
p = 40
q = 2704
primitive = true
```

The complete `d`-coordinate order is:

```text
d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q
```

The support and `d`-vector are:

```text
support = u_3
d = (3, 3, 1)
```

equivalently

```text
d_minus_p       = 3
d_pos_2sqrt_q   = 3
d_neg_2sqrt_q   = 1
```

The relevant places remain exactly:

```text
infinity, 2, 3, 13
```

## M_tail Rescue Status

The `M_tail` full-rank rescue path is closed for now:

```text
M_tail_full_rank_rescue_closed_for_now
```

The reason is narrow. `wl483` found no currently justified additional
local/Hilbert row at `infinity`, `2`, `3`, or `13` that kills `u_3`. Therefore
`wl484` does not add another row to `wl481`, does not change the `wl482`
classification, and enters obstruction handling instead.

## Chosen Gate

The selected next workflow gate is:

```text
explicit_C_d_cover_local_global_solubility
```

This gate is chosen because the `u_3` datum is already explicit in complete
`d`-coordinates, and the row-rescue path has been closed by `wl483`. The next
narrow controllable question is whether the concrete `C_d` cover for
`d=(3,3,1)` is locally soluble at the recorded places and globally soluble or
obstructed.

The other candidate gates are deferred:

- `Cassels_Tate_or_second_descent`: defer until the explicit `C_d` cover is
  certified as the relevant locally soluble Selmer-class representative or
  obstruction.
- `L_value_or_analytic_rank_route`: defer because analytic-rank evidence would
  not by itself be the minimal certificate for this concrete `d`-cover routing
  question.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl484_u3_obstruction_route_entry_audit.json
```

with:

```text
status = ok
work_log = wl484
input_work_log = wl483
obstruction_candidate_datum.id = AA_A3_B1_u_3_complete_d_candidate
obstruction_candidate_datum.support = [u_3]
obstruction_candidate_datum.d_vector_pattern = (3,3,1)
m_tail_full_rank_rescue_status.decision = M_tail_full_rank_rescue_closed_for_now
next_obstruction_workflow_gate.selected_gate = explicit_C_d_cover_local_global_solubility
routing_audit_only = true
obstruction_proved_here = false
explicit_c_d_cover_solved_here = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
```

## Boundary

This work-log stops after entering the obstruction workflow. It does not prove:

- local solubility or local insolubility of the `d=(3,3,1)` cover,
- global solubility or global insolubility of that cover,
- a Cassels-Tate or second-descent obstruction,
- an analytic-rank or L-value theorem,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
