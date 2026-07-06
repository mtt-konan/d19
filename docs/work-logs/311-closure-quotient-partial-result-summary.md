# wl311 - closure quotient partial result summary

日期：2026-07-07

## 一句话结论

closure quotient partial result 现在有一个总摘要 gate。

普通话说：以前要分别看 claim audit、language audit、priority queue。现在有一个 summary
脚本，把这些结果合成一句机器可读状态：这套 partial-result 证据包是否自洽。

## 新增脚本

```text
scripts/theory/summarize_closure_quotient_partial_result.py
tests/test_summarize_closure_quotient_partial_result.py
```

输入：

```text
results/closure_quotient_paper_claim_audit.json
results/mixed_closure_residual_language_audit.json
results/mixed_closure_aabb_residual_cover_priorities.json
results/mixed_closure_priority_handoff_audit_top4.json
results/mixed_closure_aabb_residual_local_witnesses.json
results/closure_quotient_partial_artifact_audit.json
```

输出：

```text
ready_for_partial_result
blocking_issues
strict_certificate
residual_status
language_status
priority_handoff_status
residual_local_witness_status
artifact_status
boundary
```

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/summarize_closure_quotient_partial_result.py \
  --claim-audit results/closure_quotient_paper_claim_audit.json \
  --language-audit results/mixed_closure_residual_language_audit.json \
  --priority-summary results/mixed_closure_aabb_residual_cover_priorities.json \
  --priority-handoff-audit results/mixed_closure_priority_handoff_audit_top4.json \
  --residual-local-witnesses results/mixed_closure_aabb_residual_local_witnesses.json \
  --selmer-gap-ledger results/mixed_closure_residual_selmer_gap_ledger.json \
  --residual-cover-map-verify results/mixed_closure_residual_cover_map_verify.json \
  --artifact-audit results/closure_quotient_partial_artifact_audit.json \
  --out results/closure_quotient_partial_result_summary.json \
  --strict
```

输出：

```text
wrote closure quotient partial-result summary to results/closure_quotient_partial_result_summary.json
ready_for_partial_result=True
blocking_issues=[]
```

关键 JSON：

```text
strict_certificate.rank0_torsion_certificates = 275
strict_certificate.strict_excluded_pair_count = 220
residual_status.candidate_cover_total = 27
residual_status.top_target = (115,297) AA cover 3
residual_status.bsd_analytic_rank0_rows = 2
residual_status.proof_status = candidate-not-proof
language_status.files = 7
language_status.violations = 0
priority_handoff_status.ready = True
priority_handoff_status.groups_checked = 2
priority_handoff_status.target_cover_count = 4
priority_handoff_status.map_verified_groups = 2
priority_handoff_status.local_witnessed_groups = 2
residual_local_witness_status.candidate_cover_total = 27
residual_local_witness_status.bad_prime_check_total = 251
residual_local_witness_status.unresolved_bad_prime_total = 0
residual_selmer_gap_status.candidate_cover_total = 27
residual_selmer_gap_status.rows_with_ok_diagnostics = 27
residual_selmer_gap_status.rank0_sha2_gap2_cover_total = 20
residual_selmer_gap_status.gap_type_counts = {'even-rank-sha2-gap4-open': 4, 'rank0-sha2-gap2': 20, 'rank1-sha2-gap2-open': 3}
residual_cover_map_status.target_cover_count = 27
residual_cover_map_status.verified_cover_count = 27
residual_cover_map_status.failed_cover_count = 0
artifact_status.ready = True
artifact_status.required_file_count = 99
artifact_status.missing_file_count = 0
```

## 边界

`ready_for_partial_result=True` 的含义很窄：

```text
stored result files 自洽；
论文数字 gate 无 mismatch；
措辞 gate 无 overclaim；
priority queue 有 top target；
priority handoff/probe/map/local audit ready；
27 个 residual candidate covers 的 bad-prime local witness audit 无 unresolved；
artifact audit 无 missing file。
```

它不表示：

```text
residual 2-cover 已经严格无点；
Sha[2] candidate 已经变成已证明的 Sha[2] 元素；
Harborth 猜想已证明。
```

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_summarize_closure_quotient_partial_result.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/summarize_closure_quotient_partial_result.py \
  tests/test_summarize_closure_quotient_partial_result.py
```

结果：

```text
4 passed
All checks passed!
```
