# AA+BB Route Selection After Admissibility Filter

## Question

Using `wl491` as input, what is the next narrow route after the reusable
ambient `C_d` to AA+BB admissibility filter exists and the known `u_3` sample
has been classified as:

```text
output_class = not_admissible
```

This is a routing audit only. It decides between:

- first applying the filter to already-known ambient `C_d` point ledgers,
- returning directly to `M_tail` / kernel candidate discovery,
- building a candidate queue from existing `M_tail` diagnostics.

It does not build that queue or select a new candidate.

## Input From wl491

`wl491` defines:

```text
classify_ambient_c_d_point_for_aa_bb_admissibility
```

and applies it to the only known ambient global `C_d` point currently carried
by this route:

```text
candidate_id = AA_A3_B1_u_3_complete_d_candidate
d = (3, 3, 1)
```

The filter returns:

```text
output_class = not_admissible
ledger_route = globally_soluble_but_not_aa_bb_admissible_ledger
blocking_reasons = BB_common_source_product_not_square, M_not_positive
```

Therefore the current filtered ambient ledger has:

```text
admissible_point_count = 0
not_admissible_point_count = 1
unfiltered_already_known_ambient_c_d_point_count = 0
```

## Route Options

The option:

```text
first_apply_filter_to_already_known_ambient_C_d_point_ledgers
```

is already exhausted for the current inputs. The only known ambient point in
`wl491` is `u_3`, and it is already routed as `not_admissible`.

The option:

```text
return_directly_to_M_tail_kernel_candidate_discovery
```

is deferred. Direct discovery is allowed later, but after one killed ambient
point the next controllable unit should be an ordered queue from existing
`M_tail` diagnostics rather than an unscoped new pick.

The selected next narrow gate is:

```text
build_candidate_queue_from_existing_M_tail_diagnostics
```

with:

```text
entered_here = false
candidate_queue_built_here = false
candidate_selected_here = false
```

The next gate should use:

```text
wl481_sample_matrices_kernel_diagnostics
wl482_classified_u3_support_as_already_disposed
wl491_classify_ambient_c_d_point_for_aa_bb_admissibility
```

and answer:

```text
Which existing M_tail kernel diagnostics should be queued next,
with u_3 excluded or deprioritized as already globally soluble
but not AA+BB-admissible?
```

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl492_route_selection_after_admissibility_filter.json
```

with:

```text
status = ok
work_log = wl492
input_work_log = wl491
known_ambient_filter_status.admissible_point_count = 0
known_ambient_filter_status.not_admissible_point_count = 1
known_ambient_filter_status.unfiltered_already_known_ambient_c_d_point_count = 0
selected_next_gate.gate =
  build_candidate_queue_from_existing_M_tail_diagnostics
selected_next_gate.entered_here = false
candidate_queue_built_here = false
new_m_tail_or_kernel_candidate_selected_here = false
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
advance_to_wl493 = false
```

## Boundary

This work-log stops after `wl492`. It does not prove:

- that every ambient `C_d` point fails AA+BB admissibility,
- a new local row or full-rank theorem,
- a new `M_tail` / kernel candidate,
- a candidate queue,
- ambient solubility for any new `C_d` class,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
