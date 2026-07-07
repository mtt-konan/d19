# mwrank Frontier Rank Probe

## Question

Can Sage's bundled `mwrank` close the first rank-zero escalation target
`(1625,5643) AA` after same-level Sage rank-method attempts have failed?

## Commands

Default `mwrank` probe:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/probe_mwrank_mixed_closure_rank.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_mwrank_rank_probe.json \
  --sage sage \
  --timeout 30 \
  --strict
```

Higher-bound short probe:

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/probe_mwrank_mixed_closure_rank.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_mwrank_b20_x30_t60_probe.json \
  --sage sage \
  --timeout 60 \
  --mwrank-arg=-q \
  --mwrank-arg=-v \
  --mwrank-arg=0 \
  --mwrank-arg=-b \
  --mwrank-arg=20 \
  --mwrank-arg=-x \
  --mwrank-arg=30
```

## Output

Default probe:

```text
status=ok
proof_status=open-rank-bounds-not-proof
rank_bounds=[0,2]
rank_zero_proof_candidate=False
```

Higher-bound short probe:

```text
status=timeout
proof_status=timeout-not-proof
rank_zero_proof_candidate=False
```

Ledger after adding both mwrank probes:

```text
attempt_count=19
target_count_with_attempts=8
attempt_status_counts={'open-rank-bounds-not-proof': 1, 'rank-method-open-not-proof': 8, 'rank-method-timeout-not-proof': 8, 'timeout-not-proof': 2}
strict_certificate_ready_count=0
```

## Boundary

This is not a proof. The default `mwrank` run leaves rank bounds open at
`0 <= rank <= 2`; the higher-bound short run times out. Neither result proves
rank zero and neither certifies any residual cover has no rational point.
