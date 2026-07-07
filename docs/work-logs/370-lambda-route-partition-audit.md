# Lambda Route Partition Audit

## Question

Do the current rank-zero, root-number, and 2-cover ledgers cover every primitive
`lambda=A/B` class exactly once?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_lambda_route_partition.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --rank-zero-candidates results/closure_quotient_rank_zero_family_candidates.json \
  --root-number-triage results/closure_quotient_root_number_lambda_triage.json \
  --two-cover-frontier results/closure_quotient_two_cover_lambda_frontier.json \
  --out results/closure_quotient_lambda_route_partition_audit.json \
  --strict
```

## Output

```text
status=ok
lambda_class_count=356
rank_zero_class_count=200
root_number_class_count=148
two_cover_class_count=8
covered_class_count=356
missing_classes=[]
overlap_classes=[]
unexpected_classes=[]
family_exclusion_proved_count=0
```

## Interpretation

普通话说：现在 356 个本原比例类已经完整分到三条后续路线里：

- 200 个：rank-zero family generalization；
- 148 个：root-number / rank-structure triage；
- 8 个：2-cover/Selmer 或可审阅 no-point certificate。

没有丢类、没有重复类、没有跑出 ray ledger 之外的类。这个 audit 只检查路线分桶是否自洽，
不证明任何比例类已经整族排除。

## Boundary

This is a route partition audit. It proves no lambda-family exclusion theorem.
