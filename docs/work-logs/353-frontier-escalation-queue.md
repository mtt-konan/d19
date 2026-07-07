# Frontier Escalation Queue

## Question

After all same-level rank-method target hopping and 600-second rank-zero long
rechecks failed to produce a strict certificate, what is the next proof-work
queue?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_mixed_closure_frontier_escalation_queue.py \
  --strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --attempt-audit results/mixed_closure_frontier_strictification_attempt_audit.json \
  --next-action-audit results/mixed_closure_frontier_next_action_audit.json \
  --out results/mixed_closure_frontier_escalation_queue.json \
  --strict
```

## Output

```text
status=ok
target_count=10
cover_count=23
rank_zero_target_count=8
rank_zero_rank_method_target_hopping_exhausted=True
strict_certificate_ready_count=0
route_counts={
  'even-gap4-deeper-descent-or-cover-descent': 1,
  'rank-one-generator-sha2-separation-or-cover-descent': 1,
  'rank-zero-external-rank-proof-or-cover-descent': 8,
}
```

## Interpretation

普通话说：这一步把后续证明工作排清楚。8 个 rank-zero 目标已经不能再靠同级
Sage rank-method target hopping 推进；需要外部严格 rank proof，或者逐 cover 的
no-point certificate。剩下两个 non-rankzero 目标分别需要 rank-one/Sha[2] 分离和
even-gap4 的 deeper descent 或独立 Sha[2] 障碍。

## Boundary

This queue is not a proof. It only records which strict evidence would be enough
to promote each residual target. Timeouts, open rank bounds, local witnesses,
map verification, and bounded point searches remain non-proof evidence.
