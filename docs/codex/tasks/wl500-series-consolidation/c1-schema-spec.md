# C1 A0/B0 Schema Specification

## Verdict

```text
worker_outcome_line_present = false
controller_accepted_outcome = a0_b0_schema_ready
implementation_started = false
```

The Worker omitted the requested final token but supplied a complete field,
consumer, provenance, parity, and negative-test specification. The Controller
accepts it with two simplifications:

1. no new `jsonschema` dependency;
2. no separate JSON Schema files. One Python loader validates explicit keys,
   types, versions, cross-file invariants, and `additionalProperties=false`
   semantics using the standard library.

## Canonical Files

```text
data/theory/aa_bb/wl500/a0-ledger.v1.json
data/theory/aa_bb/wl500/a0-witnesses.v1.json
data/theory/aa_bb/wl500/a0-taxonomy.v1.json
data/theory/aa_bb/wl500/a0-inventory.v1.json
data/theory/aa_bb/wl500/b0-prototype-rows.v1.json
data/theory/aa_bb/wl500/manifest.v1.json
scripts/theory/aa_bb/consolidation_inputs.py
tests/theory/aa_bb/test_consolidation_inputs.py
```

All data objects carry `schema_version: 1` and deterministic key ordering.
Arrays use canonical semantic keys, never legacy `route_rank`.

## A0 Projections

### Ledger

Source: `wl521.final_candidate_ledgers`, exactly 43 rows.

```text
candidate_id
support_family
cover_family
sample: A, B, L, T, side
cover_summary: L, T, d_vector
classification
ambient_c_d_global_solubility_status
ledger_route
source_work_log
```

### Witnesses

Source: the eight globally soluble rows of
`wl505.routed_active_shell7_supports`.

```text
candidate_id
candidate_support
sample: A, B, L, T, primitive, side, sqrt_q
parameters: p, q, sqrt_q
d_vector
point_on_cover: X, u_minus_p, u_pos_2sqrt_q, u_neg_2sqrt_q
point_on_E_L: X, Y
```

The loader recomputes root coordinates, the three cover equations,
`q=sqrt_q^2`, and the `Y` product. It does not store trusted equation booleans.

The eight IDs are:

```text
AA_A3_B7_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate
AA_A6_B7_v_13_m_tail_shell7_candidate
AA_A7_B2_u_7_m_tail_shell7_candidate
AA_A7_B6_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate
BB_A2_B7_u_7_m_tail_shell7_candidate
BB_A6_B7_u_7_plus_v_13_plus_w_5_m_tail_shell7_candidate
BB_A7_B3_u_3_plus_v_5_plus_w_17_m_tail_shell7_candidate
BB_A7_B6_v_13_m_tail_shell7_candidate
```

`wl586` currently consumes the pure `AA_A7_B2...` and mixed `AA_A3_B7...`
rows, but all eight remain part of the exact finite `wl505` evidence.

### Taxonomy

Source: `wl522.support_cover_taxonomy`, exactly 22 rows.

```text
support_family
cover_family
classification
failure_mode
ambient_c_d_global_solubility_status
lemma_candidate_status
candidate_ids
entry_count
work_logs
cover_summary
blocking_reasons
```

### Inventory

Source: `wl527.cover_family_proof_data_inventory`, exactly 15 rows. Preserve
the object-level source-side map targets, model availability, rational maps,
candidate function-field elements, opposite-side target, exceptional-branch
checklist, and missing-data classes. Recompute all summary counts.

## B0 Projection

Source: exactly two rows selected from `wl495.routed_refreshed_supports`:

```text
AA_A1_B4_v_5_m_tail_refresh_candidate
BB_A4_B1_v_5_m_tail_refresh_candidate
```

Fields:

```text
candidate_id
candidate_support
sample
complete_d_cover: parameters, d_vector, root_values
ambient_witness: point_on_cover, point_on_E_L
routing: ambient_status, admissibility_status, ledger_route, blocking_reasons
```

## Manifest And Provenance

The single manifest binds all five data files and records:

```text
schema_version
materialization_kind
baseline_commit
source_worklog
source_worklog_path
source_script_path
source_test_paths
source_result_path
source_selector
source_payload_sha256
source_payload_size
canonical_projection_sha256
consumer_paths
```

Hashes identify source and projection bytes; they do not prove mathematics.
Coordinates, equations, set/cardinality invariants, and worklogs remain the
auditable evidence. The implementation records the actual stable source commit
at materialization time rather than hard-coding the current dirty-worktree
HEAD.

## Loader And Materializer

```python
materialize_a0(source_results_dir, baseline_commit, output_dir)
materialize_b0(source_results_dir, baseline_commit, output_dir)
load_a0(path)
load_b0(path)
```

Only explicit `materialize_*` commands may read ignored `results/`. Loaders
never glob or fall back to `results/`.

Compatibility views are generated only at consumer boundaries:

```text
a0.to_wl522_view()
a0.to_wl527_view()
a0.to_wl586_inputs()
b0.to_wl528_view()
```

Any legacy `status/ready` values are derived after structural validation and
are never canonical stored facts.

## Invariants And Negative Tests

- Exact cardinalities `43/22/15/8/2`.
- Unique candidate IDs; taxonomy candidate union equals all 43 ledger IDs.
- `entry_count == len(candidate_ids)`.
- Cover classification counts `5/15/2`; entry counts `10/29/4`.
- Inventory families equal the 15 not-admissible taxonomy families.
- Witness cover equations and elliptic coordinates recompute exactly.
- B0 rows are the complete AA/BB pair for `v_5,L=1,T=5,d=(5,1,5)`.
- Missing/duplicate rows, unknown fields, altered coordinates, wrong hashes,
  missing provenance, selector drift, or a deferred witness fail closed.
- A stored `ready`, `status`, proof flag, route rank, or synthetic fixture fails
  schema validation.
- Failure never triggers an ignored-results fallback.

## Fields Not Promoted

Do not store `ready`, `status`, `violations`, `lemma_id`, proof/claim flags,
`advance_to_*`, route order/rank, cached summaries, full cached filter payloads,
free-form evidence strings, `wl529` rank proof status, or `wl586` synthetic
fixtures. A2 route outputs such as selected-next-gate and lemma patterns are not
A0 input.

## First Implementation Slice

Add only the five data files, manifest, loader/materializer, and focused tests.
Keep and do not modify `wl495`, `wl505`, `wl522`, `wl527`, `wl528`, `wl529`,
and `wl586`. Do not delete ignored payloads or switch consumers. Validate
source selectors, schema invariants, old/new semantic projections, and
fail-closed behavior before entering A1/B1.
