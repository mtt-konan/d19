# wl298 - mixed closure rank-0 certificate audit

日期：2026-07-06

## 一句话结论

`AA/BB rank=0` torsion 回拉主结论现在有单独审计脚本。真实两批数据审计结果：

```text
275 个 AA/BB rank-0 证书全部 certified
275 个全部排除 full-closed square
275 个全部 only-midpoint
violations = 0
```

普通话说：这不是只看 summary 里的几个数字，而是把每条 rank-0 证书逐条检查了一遍。

## 新增脚本

```text
scripts/theory/audit_mixed_closure_rank0_certificates.py
tests/test_mixed_closure_rank0_certificate_audit.py
```

审计范围很窄：

```text
AA/BB rows with exact rank 0/0 only
```

它不重新证明 rank。它只审计已经写入 JSONL 的 `rank0_torsion_certificate`：

- certificate 是否存在且 `status=certified`；
- 是否 `certifies_no_full_closed_square=true`；
- 是否 `all_affine_preimages_are_midpoints=true`；
- affine preimage 数量分布；
- pair 级 strict exclusion 数量；
- 若有例外，列出 `(A,B,curve,reason)`。

## 真实运行

命令：

```bash
uv run python scripts/theory/audit_mixed_closure_rank0_certificates.py \
  --input results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --input results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/mixed_closure_rank0_certificate_audit.json \
  --strict
```

输出：

```text
wrote rank0 certificate audit for 1536 rows to results/mixed_closure_rank0_certificate_audit.json
rank0_aabb_rows=275 certified_rows=275 strict_no_full_closed_rows=275 only_midpoint_rows=275 violations=0
```

这里的 `1536` 是：

```text
320 hard cases * 4 quotients + 64 residual pairs * 4 quotients
```

## 对 partial result 的意义

这一步把主结论的机器证据分成两层：

```text
rank_mixed_closure_curves.py
  生成 rank/certificate JSONL

audit_mixed_closure_rank0_certificates.py --strict
  逐条审计 stored certificates 是否满足 paper 需要的结论
```

因此论文草稿里可以更清楚地写：

```text
在当前两批数据中，所有 275 条 AA/BB rank-0 torsion-pullback 证书均通过审计；
每条只有两个 affine preimage，且都是 midpoint；没有任何 full-closed square preimage。
```

边界也必须保留：

```text
audit 脚本不重新证明 rank。
rank 0 仍依赖前置 PARI rank 认证和 certificate 生成过程。
```

## 验证

```bash
uv run pytest tests/test_mixed_closure_rank0_certificate_audit.py -q
uv run ruff check \
  scripts/theory/audit_mixed_closure_rank0_certificates.py \
  tests/test_mixed_closure_rank0_certificate_audit.py
```

结果：

```text
3 passed
All checks passed!
```
