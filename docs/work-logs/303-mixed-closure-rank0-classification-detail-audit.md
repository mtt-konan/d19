# wl303 - rank-0 certificate classification detail audit

日期：2026-07-07

## 一句话结论

`AA/BB rank=0` certificate audit 现在不只看汇总布尔字段，还逐条检查
`affine_preimage_classifications`。

普通话说：以前是“证书说所有点都是 midpoint”；现在会真的看每个回拉点明细，确认它是 midpoint、
且不是 full-closed square。

## 更新脚本

```text
scripts/theory/audit_mixed_closure_rank0_certificates.py
tests/test_mixed_closure_rank0_certificate_audit.py
scripts/theory/audit_closure_quotient_paper_claims.py
tests/test_closure_quotient_paper_claim_audit.py
```

新增检查：

```text
classification-count-mismatch
classification-not-midpoint
classification-full-closed-square
```

也新增统计：

```text
classification_detail_rows
classification_detail_point_count
```

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

JSON 中新增关键字段：

```text
classification_detail_rows=275
classification_detail_point_count=550
affine_preimage_counts={'2': 275}
```

解释：

```text
275 条 rank-0 AA/BB certificate 都有 affine preimage 明细；
每条有 2 个 affine preimage；
合计 550 个明细点逐点通过 midpoint / non-full-closed 检查。
```

## 接入 paper claim gate

`audit_closure_quotient_paper_claims.py` 现在检查：

```text
classification_detail_rows=275
classification_detail_point_count=550
```

真实运行仍然：

```text
mismatches=0
```

## 边界

这个加固仍然只审计 stored certificate：

```text
它不重新证明 rank。
它不解决 residual 2-cover 无点。
它不把 bounded search 变成证明。
```

它的作用是让 rank-0 torsion 回拉的 only-midpoint 结论更可审计，减少“汇总字段错了但明细没查”
这种风险。

## 验证

```bash
uv run pytest \
  tests/test_mixed_closure_rank0_certificate_audit.py \
  tests/test_closure_quotient_paper_claim_audit.py \
  -q

uv run ruff check \
  scripts/theory/audit_mixed_closure_rank0_certificates.py \
  scripts/theory/audit_closure_quotient_paper_claims.py \
  tests/test_mixed_closure_rank0_certificate_audit.py \
  tests/test_closure_quotient_paper_claim_audit.py
```

结果：

```text
7 passed
All checks passed!
```
