# wl304 - mixed closure residual evidence audit

日期：2026-07-07

## 一句话结论

`AA/BB` residual 的证据现在有一个跨文件审计 gate。

普通话说：以前 `12` 条 residual 的信息分散在 rank summary、Sage Selmer、PARI
`ell2cover`、BSD 诊断几份文件里；现在脚本会检查这些文件是否讲的是同一批对象，
并确认 no-point cover 仍然只叫候选，不会被误写成证明。

## 新增脚本

```text
scripts/theory/audit_mixed_closure_residual_evidence.py
tests/test_mixed_closure_residual_evidence_audit.py
```

审计内容：

```text
rank summary 中的 AA/BB uncertain rows 是否都有对应 Sage/PARI/BSD 行；
Sage pari / mwrank Selmer rank 是否一致；
rank_plus_sha2_dimension 是否等于 selmer_rank_pari - torsion_two_dimension；
PARI ell2cover 的 cover_count 是否对齐 selmer_rank_pari；
covers_without_points 是否对齐 selmer gap；
每条 residual 是否保留 proof_status = candidate-not-proof。
```

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/audit_mixed_closure_residual_evidence.py \
  --rank-summary results/mixed_closure_rank_summary.json \
  --diagnostics results/sage_mixed_closure_aabb_selmer_diagnostics.jsonl \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --bsd results/pari_bsd_mixed_aabb_t10.jsonl \
  --out results/mixed_closure_aabb_residual_evidence_audit.json \
  --strict
```

输出：

```text
wrote mixed closure residual evidence audit to results/mixed_closure_aabb_residual_evidence_audit.json
target_rows=12
candidate_cover_total=27
violations=0
```

关键 JSON 字段：

```text
diagnostic_status_counts = {"ok": 12}
cover_status_counts = {"ok": 12}
bsd_status_counts = {"ok": 2, "pari-error": 2, "timeout": 8}
selmer_backend_alignment_counts = {"match": 12}
rank_plus_sha2_alignment_counts = {"match": 12}
cover_count_selmer_alignment_counts = {"match": 12}
no_point_selmer_gap_alignment_counts = {"match": 12}
candidate_rows = 12
candidate_cover_total = 27
bsd_conditional_rank0_rows = 2
violations = []
```

## 接入 paper claim gate

`audit_closure_quotient_paper_claims.py` 现在可接收：

```text
--residual-evidence-audit results/mixed_closure_aabb_residual_evidence_audit.json
```

新增检查：

```text
residual_evidence_target_rows = 12
residual_evidence_candidate_cover_total = 27
residual_evidence_violations = 0
```

真实运行仍然：

```text
mismatches=0
```

## 边界

这个审计不证明 cover 无有理点。

它证明的是：

```text
当前 stored result files 彼此一致；
12 条 AA/BB residual 都已经压成 explicit Sha[2] candidate；
27 个 no-point cover 仍然只是 bounded-search no-point candidate；
论文口径没有把候选误升格成严格证明。
```

下一步真正的数学缺口仍然是：对某个代表性 cover，例如 `(115,297) AA` 的第 `3,4`
个 cover，给出严格无有理点证书，或者把它解释成可引用的 Cassels-Tate /
Brauer-Manin / Mordell-Weil sieve 结论。

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_mixed_closure_residual_evidence_audit.py \
  tests/test_closure_quotient_paper_claim_audit.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/audit_mixed_closure_residual_evidence.py \
  scripts/theory/audit_closure_quotient_paper_claims.py \
  tests/test_mixed_closure_residual_evidence_audit.py \
  tests/test_closure_quotient_paper_claim_audit.py
```

结果：

```text
8 passed
All checks passed!
```
