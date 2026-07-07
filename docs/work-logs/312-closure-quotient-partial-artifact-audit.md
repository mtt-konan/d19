# wl312 - closure quotient partial artifact audit

日期：2026-07-07

## 一句话结论

closure quotient partial result 现在多了一个 artifact audit。

普通话说：它不判断数学对不对，只检查这套 partial-result 证据包有没有缺文件。
如果某个脚本、测试、结果文件、论文草稿或 worklog 不见了，`--strict` 会失败。

## 新增脚本

```text
scripts/theory/audit_closure_quotient_partial_artifacts.py
tests/test_closure_quotient_partial_artifacts.py
```

默认检查的类别：

```text
script
test
doc
worklog
result
```

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/audit_closure_quotient_partial_artifacts.py \
  --out results/closure_quotient_partial_artifact_audit.json \
  --strict
```

当前期望输出：

```text
ready=True
required_file_count=111
missing_files=[]
```

这个结果也接进了 partial-result summary：

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
  --rank0-torsion-preimage-audit results/mixed_closure_rank0_sha2_torsion_preimage_audit.json \
  --bsd-conditional-no-point-audit results/mixed_closure_bsd_conditional_no_point_audit.json \
  --residual-open-frontier-audit results/mixed_closure_residual_open_frontier_audit.json \
  --artifact-audit results/closure_quotient_partial_artifact_audit.json \
  --out results/closure_quotient_partial_result_summary.json \
  --strict
```

输出：

```text
ready_for_partial_result=True
blocking_issues=[]
artifact_status.ready=True
artifact_status.required_file_count=111
artifact_status.missing_file_count=0
```

## 边界

这个 audit 只回答一个很机械的问题：

```text
这套 partial-result 说明依赖的材料是否都在仓库/工作区里。
```

它不回答：

```text
rank 结论是否新证明；
residual 2-cover 是否严格无点；
Sha[2] candidate 是否已经变成证明；
Harborth 猜想是否证明。
```

所以它只能作为“证据包完整性 gate”，不能作为数学证明 gate。

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_closure_quotient_partial_artifacts.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/audit_closure_quotient_partial_artifacts.py \
  tests/test_closure_quotient_partial_artifacts.py
```

结果：

```text
6 passed
All checks passed!
```
