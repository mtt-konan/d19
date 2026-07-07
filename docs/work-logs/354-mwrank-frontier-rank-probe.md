# mwrank Frontier Rank Probe

## Question

Can Sage's bundled `mwrank` close any rank-zero escalation target after
same-level Sage rank-method attempts have failed?

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

The same default command was then run for the remaining seven rank-zero
frontier handoffs:

```text
results/mixed_closure_residual_handoffs/priority_006_567_3757_BB_covers_4_3.json
results/mixed_closure_residual_handoffs/priority_009_5075_17901_AA_covers_4_3.json
results/mixed_closure_residual_handoffs/priority_012_8075_8613_AA_covers_4_3.json
results/mixed_closure_residual_handoffs/priority_013_391_9009_BB_covers_4_3.json
results/mixed_closure_residual_handoffs/priority_017_209_21735_BB_covers_3_4.json
results/mixed_closure_residual_handoffs/priority_024_5083_12825_BB_covers_3_4.json
results/mixed_closure_residual_handoffs/priority_025_5301_38675_BB_covers_4_3.json
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
default_mwrank_target_count=8
open-rank-bounds-not-proof=7
timeout-not-proof=1
rank_zero_proof_candidate_count=0
```

Higher-bound short probe:

```text
status=timeout
proof_status=timeout-not-proof
rank_zero_proof_candidate=False
```

Ledger after adding both mwrank probes:

```text
attempt_count=26
target_count_with_attempts=8
attempt_status_counts={'open-rank-bounds-not-proof': 7, 'rank-method-open-not-proof': 8, 'rank-method-timeout-not-proof': 8, 'timeout-not-proof': 3}
strict_certificate_ready_count=0
```

## Boundary

This is not a proof. Seven default `mwrank` runs leave rank bounds open at
`0 <= rank <= 2`; one default run times out at 30 seconds; the higher-bound
short run on the first target also times out. None of these results proves rank
zero and none certifies any residual cover has no rational point.
