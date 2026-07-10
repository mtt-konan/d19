# Function-Field Squareclass Proof-Data Scope

## Question

Entering the `wl526` selected gate, do the named `wl522` globally soluble but
not AA+BB-admissible cover families already have the minimum function-field
proof data needed for a later uniform squareclass proof attempt?

This is a proof-data scoping audit only. It works at the
cover-family function-field proof-data layer. It does not prove the uniform
lemma, build a function-field engine, execute shell 11, compute new `M_tail`
supports, test new ambient `C_d` solubility, apply `wl491` to a new point, run
broad rank/Selmer diagnostics, use the old package-`x` / `S~` bridge, name a
theorem-level Selmer row, select a final obstruction candidate, or claim
theorem-level progress.

## Input

`wl526` selected only the later gate:

```text
gather_minimal_function_field_squareclass_proof_data_for_named_cover_families
```

It did not enter that gate. `wl527` uses `wl526` as immediate input and uses
the `wl522` taxonomy only as the finite inventory of named cover families:

- 15 globally soluble but not AA+BB-admissible cover families.
- 29 entries in those families.
- No AA+BB-admissible cover families.
- No genuinely deferred cover families.

## Inventory Result

The audit inventories, for each of the 15 named cover families, exactly the
minimum later-proof data requested by `wl526`:

- cover-family model availability;
- rational source-side maps;
- candidate `N,M` function-field elements;
- opposite-side product squareclass or divisor-parity certificate target;
- exceptional specialization / positivity-separation checklist.

The named cover families are:

```text
support=u_3|L=3|T=4|d=(?,?,?)
support=u_3+v_13|L=3|T=13|d=(39,3,13)
support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85)
support=u_3+v_5+w_53|L=9|T=10|d=(15,159,265)
support=u_5|L=10|T=11|d=(5,5,1)
support=u_5|L=10|T=19|d=(5,5,1)
support=u_7|L=7|T=9|d=(7,7,1)
support=u_7+v_13+w_5|L=7|T=13|d=(91,35,65)
support=u_7+v_17+w_5|L=7|T=17|d=(119,35,85)
support=u_7+w_37|L=7|T=10|d=(7,259,37)
support=v_13|L=6|T=13|d=(13,1,13)
support=v_13|L=9|T=13|d=(13,1,13)
support=v_17+w_13|L=10|T=17|d=(17,13,221)
support=v_5|L=1|T=5|d=(5,1,5)
support=v_5|L=2|T=5|d=(5,1,5)
```

Fourteen rows have a label plus `L,T,d` vector data. The original
`support=u_3|L=3|T=4|d=(?,?,?)` row has only the family label and `L,T`; its
explicit `d` vector is not present in the `wl522` taxonomy row. None of the 15
rows has an explicit cover-family equation, function-field coordinates,
rational source-side maps, `N,M` as function-field elements, or a proved
opposite-side squareclass/divisor-parity certificate.

The opposite-side target is only a formula target at this stage:

```text
AA source target: (N^2 + B^2)(M^2 + B^2)
BB source target: (N^2 + A^2)(M^2 + A^2)
```

That target is not a certificate. A later proof attempt would still need to
state this as an element of the relevant cover-family function field and prove
non-squareness, or prove an equivalent divisor-parity squareclass obstruction
that survives specialization.

## Decision

The current data is not ready for a later uniform squareclass proof attempt.

```text
ready_cover_family_count = 0
not_ready_cover_family_count = 15
exact_missing_data_class =
  uniform_function_field_model_maps_and_squareclass_certificate
```

The exact missing data classes are:

- explicit cover-family function-field model;
- rational source-side maps on the family;
- `N,M` as function-field elements;
- opposite-side product squareclass or divisor-parity certificate;
- exceptional specialization and positivity separation.

For one row, the scoping audit also records the narrower missing class:

```text
explicit_d_vector_for_family_label
```

This is not a mathematical refutation of the possible uniform lemma. It only
says the current `wl522` / `wl526` data is insufficient for a later proof
attempt without first supplying the missing function-field objects.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.json
```

with:

```text
status = ok
work_log = wl527
immediate_input_work_log = wl526
object_layer = cover_family_function_field_proof_data_scoping
selected_gate_entered_here = true
function_field_proof_data_scoped_here = true
scope_summary.named_cover_family_count = 15
scope_summary.named_entry_count = 29
scope_summary.ready_for_later_uniform_squareclass_proof_attempt = false
scope_summary.ready_cover_family_count = 0
scope_summary.not_ready_cover_family_count = 15
scope_summary.exact_missing_data_class =
  uniform_function_field_model_maps_and_squareclass_certificate
function_field_models_built_here = false
function_field_engine_built_here = false
function_field_squareclass_certificate_proved_here = false
uniform_cover_family_lemma_proved_here = false
shell11_executed_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
wl491_filter_applied_to_new_point_here = false
final_obstruction_candidate_selected_here = false
rank_zero_claimed = false
complete_selmer_upper_bound_proved = false
advance_to_next_roadmap_step = false
stop_after_current_task = true
```

## Boundary

This work-log stops after `wl527`. It does not prove:

- a uniform cover-family squareclass obstruction;
- function-field nonsquareness of any opposite-side product;
- a new local/Hilbert row;
- a new `M_tail` row or uniform `M_tail` full rank;
- ambient solubility for any new `C_d` class;
- AA+BB admissibility for any new point or support;
- a final obstruction candidate;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

No next roadmap step is entered here. A later proof attempt would first need
the missing function-field model/map/squareclass-certificate data named above.
