# proof_status Fast Mode

`proof_status` fast mode is historical engineering support. It is useful for
bounded scans, not current proof progress.

## Modes

```text
full audit:
  every pair runs the full pipeline and writes SQLite rows

fast-core:
  all pairs run cheap core filters; only survivors get full audit

fast-core-only:
  all pairs run cheap core filters; output summary JSON; no survivor audit
```

## Typical Command

```bash
PARI_MT_ENGINE=single uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_core.db \
  --max-hyp 50000 \
  --workers 6 \
  --fast-core \
  --fast-core-only \
  --force \
  --fast-summary-json /tmp/proof_status_fast_summary.json \
  --no-progress
```

## Interpretation

- Summary counts are finite bounded-scan evidence.
- DB rows may contain only survivors, not every checked pair.
- `PARI_MT_ENGINE=single` plus explicit `default(nbthreads,1)` avoids old PARI
  multi-thread hangs.

## Current Role

Use this only when reproducing old finite scans or generating comparison data.
The current proof route is closure quotient / rank-zero Selmer, not
`proof_status` scaling.
