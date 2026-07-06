# wl308 - priority queue paper claim gate

日期：2026-07-07

## 一句话结论

priority queue 的关键数字现在进入 paper-level claim gate。

普通话说：论文/主线文档里写的 `27` 个候选 cover、top target 是 `(115,297) AA cover 3`、
top-4 都有 BSD 条件 rank 0，现在会被脚本检查，不再只是文档里的手写数字。

## 更新脚本

```text
scripts/theory/audit_closure_quotient_paper_claims.py
tests/test_closure_quotient_paper_claim_audit.py
```

新增输入：

```text
--priority-summary results/mixed_closure_aabb_residual_cover_priorities.json
```

新增 claim values：

```text
priority_candidate_cover_total
priority_top_a
priority_top_b
priority_top_cover_index
priority_top_curve_is_aa
priority_top4_bsd_rank0_rows
```

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/audit_closure_quotient_paper_claims.py \
  --rank-summary results/mixed_closure_rank_summary.json \
  --rank0-audit results/mixed_closure_rank0_certificate_audit.json \
  --cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --residual-evidence-audit results/mixed_closure_aabb_residual_evidence_audit.json \
  --priority-summary results/mixed_closure_aabb_residual_cover_priorities.json \
  --identity-audit results/mixed_closure_even_model_identity_audit.json \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --out results/closure_quotient_paper_claim_audit.json \
  --expect rank0_torsion_certificates=275 \
  --expect strict_excluded_pair_count=220 \
  --expect rank0_aabb_rows=275 \
  --expect classification_detail_rows=275 \
  --expect classification_detail_point_count=550 \
  --expect cover_rows=12 \
  --expect cover_selmer_matches=12 \
  --expect residual_evidence_target_rows=12 \
  --expect residual_evidence_candidate_cover_total=27 \
  --expect residual_evidence_violations=0 \
  --expect priority_candidate_cover_total=27 \
  --expect priority_top_a=115 \
  --expect priority_top_b=297 \
  --expect priority_top_cover_index=3 \
  --expect priority_top4_bsd_rank0_rows=4 \
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

这个 gate 不产生数学证明。

它只证明 stored result files 和文档里的数值声明一致，包括：

```text
rank-0 AA/BB only-midpoint 证书数量；
residual evidence audit 数字；
priority queue 的 top target 与候选 cover 数量；
BSD 条件诊断数量。
```

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_closure_quotient_paper_claim_audit.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/audit_closure_quotient_paper_claims.py \
  tests/test_closure_quotient_paper_claim_audit.py
```

结果：

```text
4 passed
All checks passed!
```
