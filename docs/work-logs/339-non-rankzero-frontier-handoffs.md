# Non-Rank-Zero Frontier Handoffs

Date: 2026-07-07

## Question

Can the two non-rank-zero residual frontier targets be packaged for external
proof work at the same quality level as the rank-zero frontier handoffs?

These targets are not rank-zero proof targets. One needs visible rank-one
separation from the residual `Sha[2]` class; the other needs deeper descent or an
independent `Sha[2]` obstruction.

## Scope

The two packaged targets are:

```text
priority_008_209_5355_BB_covers_5_4_3
priority_011_1449_12155_BB_covers_5_6_3_4
```

For each target, the handoff directory contains:

```text
<name>.json
<name>.sage
<name>.magma
<name>_map_verify.json
<name>_local_witnesses.json
<name>_sage_probe.json
```

## Commands

The handoffs were exported from the existing priority and `ell2cover` data using
the same `build_handoff` and `write_handoff_files` helpers as the CLI exporter.

Each handoff then ran:

```bash
DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_verify_mixed_closure_handoff_maps.py \
  --handoff results/mixed_closure_residual_handoffs/<name>.json \
  --out results/mixed_closure_residual_handoffs/<name>_map_verify.json \
  --timeout 60 \
  --strict

DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_probe_mixed_closure_local_witnesses.py \
  --handoff results/mixed_closure_residual_handoffs/<name>.json \
  --out results/mixed_closure_residual_handoffs/<name>_local_witnesses.json \
  --timeout 60 \
  --search-bound 300 \
  --max-denominator-power 3 \
  --strict

DOT_SAGE=/private/tmp/d19-dot-sage \
UV_CACHE_DIR=/private/tmp/d19-uv-cache \
uv run python scripts/theory/sage_probe_mixed_closure_handoff.py \
  --handoff results/mixed_closure_residual_handoffs/<name>.json \
  --out results/mixed_closure_residual_handoffs/<name>_sage_probe.json \
  --timeout 60 \
  --point-search-bound 100
```

## Result

```text
priority_008_209_5355_BB_covers_5_4_3:
  strict_proof_status = open
  map_verified = True
  local_bad_primes_witnessed = True
  rank_bounds = [1, 3]
  rank_proof_status = runtime-error
  selmer_rank = 5
  torsion_two_dimension = 2
  cover_point_counts = [0, 0, 0]

priority_011_1449_12155_BB_covers_5_6_3_4:
  strict_proof_status = open
  map_verified = True
  local_bad_primes_witnessed = True
  rank_bounds = [0, 4]
  rank_proof_status = runtime-error
  selmer_rank = 6
  torsion_two_dimension = 2
  cover_point_counts = [0, 0, 0, 0]
```

Both have BSD diagnostic status `timeout`.

## Boundary

This handoff work does not prove a no-point result. It only packages the two
remaining non-rank-zero frontier targets for stricter follow-up. The rank-one
target still needs a visible generator or a separation argument. The even-gap4
target still needs deeper descent or an independent `Sha[2]` obstruction.
