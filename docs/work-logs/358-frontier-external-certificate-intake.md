# Frontier External Certificate Intake

## Question

Can the external no-point certificate intake be extended from the first
residual target to the whole residual frontier?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_external_cover_certificate_frontier_intake.py \
  --frontier-handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --certificate-dir results/mixed_closure_external_certificates \
  --out results/mixed_closure_external_cover_certificate_frontier_intake.json \
  --template-index-out results/mixed_closure_external_cover_certificate_template_index.json \
  --strict
```

## Output

```text
status=ok
target_count=10
cover_count=23
certificate_package_ready_count=0
strict_promotion_ready_count=0
```

## Interpretation

普通话说：现在所有 residual frontier 目标都有统一的外部证书入口了。它覆盖
10 个目标、23 个 cover。当前还没有任何外部 no-point 证书包，所以没有新的严格提升。

这个审计做三件事：

- 按 `mixed_closure_frontier_handoff_audit.json` 固定需要外部处理的目标清单；
- 对每个目标约定证书包路径，例如
  `external_certificates/<handoff-name>_certificate.json`；
- 复用单目标 intake 规则，检查证书包是否覆盖全部 cover、是否有 transcript、
  是否只声称 `no-rational-points` 这种可审阅结果。

即使某个证书包字段齐全，它也只会进入 `certificate_package_ready=True`。它不会自动
变成证明；还需要数学审阅 transcript。

## Boundary

This is a frontier-wide external evidence intake gate, not a mathematical
verifier. It prevents missing or partial external evidence from being promoted.
