# Summary Gate External Certificate Intake

## Question

Is the frontier-wide external certificate intake visible in the final
partial-result summary?

## Change

`summarize_closure_quotient_partial_result.py` now accepts:

```text
--external-certificate-frontier-audit results/mixed_closure_external_cover_certificate_frontier_intake.json
```

and emits:

```text
external_certificate_frontier_status.target_count=10
external_certificate_frontier_status.cover_count=23
external_certificate_frontier_status.certificate_package_ready_count=0
external_certificate_frontier_status.strict_promotion_ready_count=0
external_certificate_frontier_status.proof_status=frontier-external-certificates-missing-not-proof
```

## Interpretation

普通话说：最终 summary 现在不会只说“下一步要外部工具”，而是明确记录外部证书入口
已经覆盖整个 residual frontier。当前 10 个目标、23 个 cover 都还没有外部证书包；
因此没有任何新的严格提升。

这仍然不是证明。它只是让最终 partial-result gate 检查：

- external certificate intake 覆盖的目标数等于 frontier handoff 目标数；
- cover 数等于 open frontier cover 数；
- 没有 strict promotion；
- 没有缺 handoff 或 intake 违规。

## Boundary

This summary gate records external certificate intake coverage. It does not
verify any external no-point transcript.
