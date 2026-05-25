# Results Directory

This directory contains generated artifacts. Not every file is equally important.

## Authoritative artifacts

### Multi-concordant ground truth
- `multi_concordant_N_max10000.jsonl`
- Coverage: all reduced coprime pairs `1 <= A < B <= 10000`
- Meaning: one JSON line per pair with `n_concordant >= 2`
- Record count: 854
- Use this file as the ground-truth comparison set for any future fast multi-N heuristic.

### Proof workflow state
- `proof_status.db`
- Meaning: SQLite state for proof-status workflow

## Extended fast-scan outputs

These are produced by `scripts/fast_multi_concordant_scan.py` (pivot-on-N).
At `max_hyp=10000` they are byte-equivalent to the ground truth (verified by
`scripts/validate_fast_multi_n.py`). At larger scales they are not yet
independently audited but were spot-checked against the slow
`factor_search` for representative pairs.

- `multi_concordant_N_max20000_fast.jsonl` — 1848 multi-N pairs, max k=4
- `multi_concordant_N_max50000_fast.jsonl` — 4968 multi-N pairs, max k=4

## Regenerate curated catalog

```bash
uv run python scripts/build_results_catalog.py
```

## Regenerate fast scans

```bash
uv run python scripts/fast_multi_concordant_scan.py --max-hyp 20000
uv run python scripts/fast_multi_concordant_scan.py --max-hyp 50000
```

## Validate fast scanner against ground truth

```bash
uv run python scripts/validate_fast_multi_n.py --max-hyp 10000
```
