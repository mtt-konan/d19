# Lambda Mainline Audit

## Question

Does the closure quotient package now enforce the new mainline: primitive
`lambda=A/B` structure first, no single-pair certificate counting as main
progress?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_lambda_mainline.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --lambda-frontier results/closure_quotient_lambda_frontier.json \
  --route-partition results/closure_quotient_lambda_route_partition_audit.json \
  --two-cover-frontier results/closure_quotient_two_cover_lambda_frontier.json \
  --out results/closure_quotient_lambda_mainline_audit.json \
  --strict
```

## Output

```text
status=ok
lambda_class_count=356
covered_class_count=356
violations=[]
```

Checks:

```text
ray_ledger_has_c_minus=True
route_partition_complete=True
search_count_rejected_as_progress=True
two_cover_requires_strict_evidence=True
family_exclusion_claim_count_zero=True
```

Route counts:

```text
rank-zero-family-generalization=200
root-number-rank-structure-triage=148
two-cover-or-reviewable-no-point-certificate=8
```

## Interpretation

普通话说：这个总 gate 把当前方向锁住：

- ray ledger 已经补 `c_- = |A-B|` 和 `c_+/c_-`；
- 356 个本原比例类完整分桶；
- 搜索数量增长明确不是主进展；
- 剩余 2-cover 类只接受整族 Selmer/2-cover 障碍或可审阅 no-point 证书；
- 当前没有任何比例类被误标成已经整族排除。

## Boundary

This audit checks mainline organization and evidence boundaries. It proves no
lambda-family exclusion theorem.
