# External Cover Certificate Intake

## Question

If a future Magma / Mordell-Weil sieve / specialized descent run produces a
cover-level certificate, how do we keep it from being mixed up with search
evidence?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_external_cover_certificate_intake.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_external_cover_certificate_intake.json \
  --template-out results/priority_005_1625_5643_AA_external_cover_certificate_template.json \
  --strict
```

## Output

```text
status=ok
certificate_package_ready=False
strict_promotion_ready=False
```

## Interpretation

普通话说：现在还没有外部 no-point 证书包，所以这个 residual 目标没有变成证明。
脚本同时生成了一个证书包模板，未来外部工具必须至少填清楚：

- 目标 `(A,B,curve)`；
- transcript 文件路径；
- 每个目标 cover 的证书类型；
- 每个目标 cover 的结果必须是 `no-rational-points`；
- 对应的命令标签，方便回看 transcript。

即使这些字段齐全，脚本也只会说 `certificate_package_ready=True`。它不会自己说
数学已经证明，因为 transcript 里的 descent / sieve 论证仍需要人工或形式化工具审阅。

## Boundary

This is an intake gate, not a mathematical verifier. It prevents incomplete
external evidence from being promoted, but it does not certify a no-point claim
by itself.
