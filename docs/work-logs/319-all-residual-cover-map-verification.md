# wl319 - all residual cover map verification

日期：2026-07-07

## 一句话结论

27 个 residual no-point cover 的 rational map identity 现在全部用 Sage 验证过。

普通话说：这些 cover 不是孤零零的四次曲线；它们确实通过存下来的有理映射落到对应的
Weierstrass 椭圆曲线上。这个检查仍然不是“无有理点证明”，但它把后续 Selmer/Sha[2]
讨论的输入对象钉牢了。

## 更新脚本

```text
scripts/theory/sage_verify_mixed_closure_residual_cover_maps.py
tests/test_sage_verify_mixed_closure_residual_cover_maps.py
scripts/theory/summarize_closure_quotient_partial_result.py
tests/test_summarize_closure_quotient_partial_result.py
scripts/theory/audit_closure_quotient_partial_artifacts.py
tests/test_closure_quotient_partial_artifacts.py
```

## 真实运行

命令：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_verify_mixed_closure_residual_cover_maps.py \
  --covers results/pari_ell2cover_mixed_aabb_h100000.jsonl \
  --cover-summary results/mixed_closure_aabb_residual_cover_summary.json \
  --out results/mixed_closure_residual_cover_map_verify.json \
  --timeout 120 \
  --strict
```

输出：

```text
wrote residual cover map verification to results/mixed_closure_residual_cover_map_verify.json
status=ok
target_cover_count=27
all_verified=True
```

## 当前 gate 数字

```text
group_count = 12
target_cover_count = 27
verified_cover_count = 27
failed_cover_count = 0
all_verified = true
```

## 接入 partial summary

`summarize_closure_quotient_partial_result.py` 新增输入：

```text
--residual-cover-map-verify results/mixed_closure_residual_cover_map_verify.json
```

summary 现在输出：

```text
residual_cover_map_status.ready = true
residual_cover_map_status.target_cover_count = 27
residual_cover_map_status.verified_cover_count = 27
residual_cover_map_status.failed_cover_count = 0
```

## 边界

这个 gate 只验证存储的 cover-to-elliptic rational maps 满足对应椭圆曲线方程。
它不证明 residual cover 没有有理点，也不把 bounded search 升级成证明。

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_sage_verify_mixed_closure_residual_cover_maps.py \
  tests/test_summarize_closure_quotient_partial_result.py \
  tests/test_closure_quotient_partial_artifacts.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/sage_verify_mixed_closure_residual_cover_maps.py \
  tests/test_sage_verify_mixed_closure_residual_cover_maps.py \
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
