# wl321 - rank0 torsion preimage audit

日期：2026-07-07

## 一句话结论

20 个 `rank0-sha2-gap2` cover 现在都有条件性的 torsion-preimage 审计。

普通话说：如果对应椭圆曲线真的 rank 0，那么有理点只能落到 torsion 点。我们检查了这些
cover 到椭圆曲线的映射，20 个 cover 都没有有理无穷点、没有有理 branch point，也没有
有限 torsion 点的有理 preimage。

## 更新脚本

```text
scripts/theory/sage_audit_mixed_closure_rank0_torsion_preimages.py
tests/test_sage_audit_mixed_closure_rank0_torsion_preimages.py
scripts/theory/summarize_closure_quotient_partial_result.py
tests/test_summarize_closure_quotient_partial_result.py
scripts/theory/audit_closure_quotient_partial_artifacts.py
tests/test_closure_quotient_partial_artifacts.py
```

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_audit_mixed_closure_rank0_torsion_preimages.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --selmer-gap-ledger results/mixed_closure_residual_selmer_gap_ledger.json \
  --out results/mixed_closure_rank0_sha2_torsion_preimage_audit.json \
  --timeout 180 \
  --strict
```

输出：

```text
wrote rank-zero torsion preimage audit to results/mixed_closure_rank0_sha2_torsion_preimage_audit.json
status=ok
target_cover_count=20
all_no_torsion_preimages=True
```

## 当前 gate 数字

```text
target_cover_count = 20
no_torsion_preimage_count = 20
failed_cover_count = 0
all_no_torsion_preimages = true
```

## 接入 partial summary

`summarize_closure_quotient_partial_result.py` 新增输入：

```text
--rank0-torsion-preimage-audit results/mixed_closure_rank0_sha2_torsion_preimage_audit.json
```

summary 现在输出：

```text
rank0_torsion_preimage_status.ready = true
rank0_torsion_preimage_status.target_cover_count = 20
rank0_torsion_preimage_status.no_torsion_preimage_count = 20
rank0_torsion_preimage_status.failed_cover_count = 0
rank0_torsion_preimage_status.conditional_on_rank_zero = true
```

## 边界

这是条件性审计，不是无条件无点证明。

准确说，它证明的是：对这 20 个 cover，如果对应椭圆曲线的有理点群只有 torsion，
那么这些 cover 没有有理点。它没有证明这些椭圆曲线 rank 0；当前 rank 仍是
`[0,2]` 的 Selmer/Sha[2] 缺口。

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_sage_audit_mixed_closure_rank0_torsion_preimages.py \
  tests/test_summarize_closure_quotient_partial_result.py \
  tests/test_closure_quotient_partial_artifacts.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/sage_audit_mixed_closure_rank0_torsion_preimages.py \
  tests/test_sage_audit_mixed_closure_rank0_torsion_preimages.py \
  scripts/theory/summarize_closure_quotient_partial_result.py \
  tests/test_summarize_closure_quotient_partial_result.py \
  scripts/theory/audit_closure_quotient_partial_artifacts.py \
  tests/test_closure_quotient_partial_artifacts.py
```

结果：

```text
8 passed
All checks passed!
```
