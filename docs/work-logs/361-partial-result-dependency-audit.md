# Partial Result Dependency Audit

## Question

Can every major final-summary status be traced back to an explicit result file?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_partial_dependencies.py \
  --summary results/closure_quotient_partial_result_summary.json \
  --artifact-audit results/closure_quotient_partial_artifact_audit.json \
  --root . \
  --out results/closure_quotient_partial_dependency_audit.json \
  --strict
```

## Output

```text
status=ok
dependency_count=8
missing_summary_statuses=0
```

## Interpretation

普通话说：这个审计检查最终 summary 里的关键状态是否都有明确的上游 result 文件。
它不验证数学，只防止 final summary 变成“孤立的一份绿灯文件”。

当前 dependency map 覆盖：

- strict certificate；
- residual priority/status；
- open frontier；
- frontier strictification；
- external certificate frontier intake；
- paper structure；
- artifact status。

## Boundary

This is a dependency-map audit. It verifies file traceability, not mathematical
truth.
