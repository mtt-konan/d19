# wl309 - residual language overclaim audit

日期：2026-07-07

## 一句话结论

residual 相关文档现在有措辞审计，防止把数值证据写成证明。

普通话说：脚本不会验证数学，但会抓几类危险表达，比如“bounded search 证明无点”、
“BSD diagnostic 是严格证书”。这补的是论文级 partial result 最容易出错的一层：措辞边界。

## 新增脚本

```text
scripts/theory/audit_mixed_closure_residual_language.py
tests/test_mixed_closure_residual_language_audit.py
```

当前拦截：

```text
bounded-search-proof-overclaim
bsd-strict-certificate-overclaim
```

当前检查的边界词：

```text
candidate-not-proof
Sha[2] ... candidate
bounded search ... not a proof / does not prove
BSD ... not a strict rank certificate
```

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/audit_mixed_closure_residual_language.py \
  --path docs/CLOSURE_QUOTIENT_MAINLINE.md \
  --path docs/paper/CLOSURE_QUOTIENT_PARTIAL_RESULT.md \
  --path docs/work-logs/304-mixed-closure-residual-evidence-audit.md \
  --path docs/work-logs/305-sage-residual-handoff-probe.md \
  --path docs/work-logs/306-mixed-residual-cover-priority-queue.md \
  --path docs/work-logs/307-priority-handoff-export-and-second-sage-probe.md \
  --path docs/work-logs/308-priority-queue-paper-claim-gate.md \
  --out results/mixed_closure_residual_language_audit.json \
  --strict
```

输出：

```text
wrote mixed closure residual language audit to results/mixed_closure_residual_language_audit.json
files=7
violations=0
required_boundary_hits={
  'candidate_not_proof': 2,
  'sha2_candidate': 5,
  'bounded_search_not_proof': 1,
  'bsd_not_strict_certificate': 1
}
```

## 边界

这个审计不证明任何数学结论。

它只防止这几类错误：

```text
把 hyperellratpoints 有界无点写成无点证明；
把 BSD 条件诊断写成无条件 rank 证书；
把 Sha[2] candidate 写成已证明的 Sha[2] 元素；
把 priority queue 写成证明结果。
```

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_mixed_closure_residual_language_audit.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/audit_mixed_closure_residual_language.py \
  tests/test_mixed_closure_residual_language_audit.py
```

结果：

```text
4 passed
All checks passed!
```
