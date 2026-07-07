# All Rank-Zero Frontier Handoffs

Date: 2026-07-07

## Question

Can all 8 rank-zero residual frontier targets be packaged for external rank or
cover-level proof work?

The short Sage rank-retry route has already ended in timeouts. This work packages
the target cover quartics, stored maps, local-witness diagnostics, and bounded
Sage probes for all rank-zero frontier targets. It does not prove that any cover
has no rational point.

## Scope

The 8 packaged rank-zero frontier targets are:

```text
priority_005_1625_5643_AA_covers_4_3
priority_006_567_3757_BB_covers_4_3
priority_009_5075_17901_AA_covers_4_3
priority_012_8075_8613_AA_covers_4_3
priority_013_391_9009_BB_covers_4_3
priority_017_209_21735_BB_covers_3_4
priority_024_5083_12825_BB_covers_3_4
priority_025_5301_38675_BB_covers_4_3
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

The remaining 7 handoffs after `priority_005` were exported from the existing
priority and `ell2cover` data using the same `build_handoff` and
`write_handoff_files` helpers as the CLI exporter.

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

All 8 handoffs have:

```text
strict_proof_status = open
map_verified = True
local_bad_primes_witnessed = True
rank_bounds = [0, 2]
rank_proof_status = runtime-error
cover_point_counts = [0, 0]
```

The BSD diagnostic statuses are:

```text
pari-error: priority_005_1625_5643_AA_covers_4_3
pari-error: priority_006_567_3757_BB_covers_4_3
timeout:    the other 6 rank-zero frontier handoffs
```

## Boundary

This is stronger packaging, not a stronger theorem. Map verification proves that
the stored rational maps are internally consistent. Local witnesses show the
expected local solubility. Bounded Sage probes and bounded point searches are not
no-point certificates.

The strict partial result remains unchanged: only the already certified rank-zero
`AA/BB` torsion pullback rows are paper-ready.
