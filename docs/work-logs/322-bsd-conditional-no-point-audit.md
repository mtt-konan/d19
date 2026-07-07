# BSD-Conditional No-Point Audit

Date: 2026-07-07

## Question

After the rank-0 torsion-preimage audit, identify which residual `AA/BB` covers have both:

- a `rank0-sha2-gap2` Selmer/Sha[2] gap row,
- BSD-conditional analytic-rank-zero evidence, and
- no torsion preimage under the verified cover map.

This is meant to separate the strongest conditional candidates from the still-open residual covers.

## Commands

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_mixed_closure_bsd_conditional_no_point_audit.py -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/audit_mixed_closure_bsd_conditional_no_points.py \
  tests/test_mixed_closure_bsd_conditional_no_point_audit.py

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/audit_mixed_closure_bsd_conditional_no_points.py \
  --selmer-gap-ledger results/mixed_closure_residual_selmer_gap_ledger.json \
  --rank0-torsion-preimage-audit results/mixed_closure_rank0_sha2_torsion_preimage_audit.json \
  --out results/mixed_closure_bsd_conditional_no_point_audit.json \
  --strict
```

## Result

The audit found 4 BSD-conditional no-point candidates among the 20 `rank0-sha2-gap2` residual covers:

| A | B | curve | cover |
|---:|---:|:---:|---:|
| 115 | 297 | AA | 3 |
| 115 | 297 | AA | 4 |
| 575 | 4641 | AA | 4 |
| 575 | 4641 | AA | 3 |

The audit keeps:

- `bsd_conditional_no_point_cover_count = 4`
- `rank0_sha2_gap2_cover_count = 20`
- `strict_no_point_cover_count = 0`
- `candidate_not_proof = true`

## Boundary

This is conditional evidence, not an unconditional proof. In plain terms: these 4 covers are the best current candidates because two independent checks point the same way, but the argument still depends on BSD-style rank evidence. They cannot be counted with the rank-zero torsion certificates.
