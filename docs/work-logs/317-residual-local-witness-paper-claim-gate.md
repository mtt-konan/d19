# wl317 - residual local witness paper claim gate

日期：2026-07-07

## 一句话结论

全量 residual local witness 的数字现在进入了 paper-level claim gate。

普通话说：之前 partial summary 会展示“27 个候选 cover 的坏素数都找到了局部点见证”，
但 paper claim audit 还不会硬检查这些数字。现在论文数字 gate 也会检查这一点。

## 更新脚本

```text
scripts/theory/audit_closure_quotient_paper_claims.py
tests/test_closure_quotient_paper_claim_audit.py
```

新增输入：

```text
--residual-local-witnesses results/mixed_closure_aabb_residual_local_witnesses.json
```

新增 claim values：

```text
residual_local_witness_candidate_cover_total
residual_local_witness_bad_prime_check_total
residual_local_witness_unresolved_bad_prime_total
residual_local_witness_all_bad_primes_witnessed
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
  --residual-local-witnesses results/mixed_closure_aabb_residual_local_witnesses.json \
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
  --expect residual_local_witness_candidate_cover_total=27 \
  --expect residual_local_witness_bad_prime_check_total=251 \
  --expect residual_local_witness_unresolved_bad_prime_total=0 \
  --expect residual_local_witness_all_bad_primes_witnessed=1 \
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

## 当前 gate 数字

```text
residual_local_witness_candidate_cover_total = 27
residual_local_witness_bad_prime_check_total = 251
residual_local_witness_unresolved_bad_prime_total = 0
residual_local_witness_all_bad_primes_witnessed = 1
```

## 边界

这个 gate 只说明“全量 residual cover 的局部可解性检查数字和文档说法一致”。
它不是无有理点证明，也不把 bounded search 或 Sha[2] candidate 升级成证明。

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
