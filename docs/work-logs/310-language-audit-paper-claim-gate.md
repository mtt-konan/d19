# wl310 - language audit paper claim gate

日期：2026-07-07

## 一句话结论

residual language audit 现在接进了 paper-level claim gate。

普通话说：以后跑论文数字一致性检查时，会同时检查“没有过度声明”和“关键边界句还在”。
这样就不需要靠人记得单独跑措辞审计。

## 更新脚本

```text
scripts/theory/audit_closure_quotient_paper_claims.py
tests/test_closure_quotient_paper_claim_audit.py
```

新增输入：

```text
--language-audit results/mixed_closure_residual_language_audit.json
```

新增 claim values：

```text
language_audit_violations
language_audit_files
language_candidate_not_proof_hits
language_sha2_candidate_hits
language_bounded_search_not_proof_hits
language_bsd_not_strict_certificate_hits
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
  --language-audit results/mixed_closure_residual_language_audit.json \
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
  --expect language_audit_violations=0 \
  --expect language_audit_files=7 \
  --expect language_candidate_not_proof_hits=4 \
  --expect language_sha2_candidate_hits=5 \
  --expect language_bounded_search_not_proof_hits=1 \
  --expect language_bsd_not_strict_certificate_hits=1 \
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

这个 gate 仍然不产生数学证明。

它现在同时检查：

```text
rank-0 torsion 回拉数字；
residual evidence 数字；
priority queue 数字；
language audit 边界；
BSD 条件诊断数字；
代数恒等式审计结果。
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
