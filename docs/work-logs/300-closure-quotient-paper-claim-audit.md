# wl300 - closure quotient paper claim audit

日期：2026-07-07

## 一句话结论

新增论文数字一致性检查脚本。当前 partial-result 文档要引用的核心数字已经和结果文件对齐：

```text
mismatches = 0
```

普通话说：以后改数据或改文档前，可以先跑这个 gate，避免把旧数字写进论文草稿。

## 新增脚本

```text
scripts/theory/audit_closure_quotient_paper_claims.py
tests/test_closure_quotient_paper_claim_audit.py
```

它读取：

```text
results/mixed_closure_rank_summary.json
results/mixed_closure_rank0_certificate_audit.json
results/mixed_closure_aabb_residual_cover_summary.json
results/pari_bsd_mixed_aabb_t10.jsonl
```

它输出：

```text
results/closure_quotient_paper_claim_audit.json
```

## 检查内容

当前 gate 检查这些 paper-level 数字：

```text
rank0_torsion_certificates = 275
strict_excluded_pair_count = 220
rank0_aabb_rows = 275
cover_rows = 12
cover_selmer_matches = 12
even_model_identities_verified = 1
bsd_ok_rows = 2
bsd_analytic_rank0_rows = 2
```

这些数字分别来自：

- rank/certificate summary；
- rank-0 certificate audit；
- even-model symbolic identity audit；
- residual 2-cover summary；
- PARI BSD 条件诊断。

## 真实运行

命令：

```bash
uv run python scripts/theory/audit_closure_quotient_paper_claims.py \
  --rank-summary results/mixed_closure_rank_summary.json \
  --rank0-audit results/mixed_closure_rank0_certificate_audit.json \
  --cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --identity-audit results/mixed_closure_even_model_identity_audit.json \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --out results/closure_quotient_paper_claim_audit.json \
  --expect rank0_torsion_certificates=275 \
  --expect strict_excluded_pair_count=220 \
  --expect rank0_aabb_rows=275 \
  --expect cover_rows=12 \
  --expect cover_selmer_matches=12 \
  --expect even_model_identities_verified=1 \
  --expect bsd_ok_rows=2 \
  --expect bsd_analytic_rank0_rows=2 \
  --strict
```

输出：

```text
wrote closure quotient paper claim audit to results/closure_quotient_paper_claim_audit.json
mismatches=0
```

## 边界

这个脚本不产生新数学证书。

它只做一致性检查：

```text
stored result files <-> paper-level numeric claims
```

所以它不能替代：

- `rank_mixed_closure_curves.py` 的 rank/certificate 生成；
- `audit_mixed_closure_rank0_certificates.py` 的 rank-0 stored certificate 审计；
- residual 2-cover 的严格无点证明。

## 验证

```bash
uv run pytest tests/test_closure_quotient_paper_claim_audit.py -q
uv run ruff check \
  scripts/theory/audit_closure_quotient_paper_claims.py \
  tests/test_closure_quotient_paper_claim_audit.py
```

结果：

```text
4 passed
All checks passed!
```
