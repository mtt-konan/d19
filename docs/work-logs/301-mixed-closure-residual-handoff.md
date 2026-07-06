# wl301 - mixed closure residual strict-proof handoff

日期：2026-07-07

## 一句话结论

`(115,297) AA` 的 cover `3,4` 现在有固定 handoff 包：JSON + Sage + Magma 草案。

普通话说：后面要攻严格无点证明时，不用再从多个结果文件里找对象；目标 cover、covering map、
BSD 条件诊断和证明边界都打包好了。

## 新增脚本

```text
scripts/theory/export_mixed_closure_residual_handoff.py
tests/test_mixed_closure_residual_handoff.py
```

输入：

```text
results/pari_ell2cover_mixed_115_297_AA_h100000_with_maps.jsonl
results/pari_bsd_mixed_115_297_AA.jsonl
```

命令：

```bash
uv run python scripts/theory/export_mixed_closure_residual_handoff.py \
  --covers results/pari_ell2cover_mixed_115_297_AA_h100000_with_maps.jsonl \
  --bsd results/pari_bsd_mixed_115_297_AA.jsonl \
  --target 115,297,AA \
  --cover-index 3 \
  --cover-index 4 \
  --out-dir results/mixed_closure_residual_handoffs \
  --name 115_297_AA_covers_3_4
```

输出：

```text
results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.json
results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.sage
results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.magma
```

## 目标 cover

```text
cover 3:
y^2 = 41*x^4 + 10812*x^3 + 27981*x^2 - 54060*x + 1025

cover 4:
y^2 = -19*x^4 + 1848*x^3 + 182394*x^2 - 1062600*x - 6281875
```

打包进去的证据：

```text
ellrank = [0,2]
local_solubility_source = PARI ell2cover returns everywhere locally soluble 2-covers
bounded_search_evidence = hyperellratpoints found no points on target covers
analytic_rank = 0
evidence_level = bsd-conditional-diagnostic
strict_proof_status = open
```

边界：

```text
handoff 不是证明。
bounded search 不是无点证明。
BSD diagnostic 不是无条件 rank 证书。
Magma 文件不是已验证 transcript。
```

## 本地验证

Sage handoff 文件已跑通：

```bash
/usr/local/bin/sage results/mixed_closure_residual_handoffs/115_297_AA_covers_3_4.sage
```

输出：

```text
cover 3: Hyperelliptic Curve over Rational Field defined by y^2 = 41*x^4 + ...
cover 4: Hyperelliptic Curve over Rational Field defined by y^2 = -19*x^4 + ...
```

本地没有 `magma`：

```text
command -v magma
```

没有返回可执行文件。因此 `.magma` 只能作为外部严格证明的起点。

## 下一步

最直接的后续任务：

```text
拿 115_297_AA_covers_3_4.magma 去有 Magma 的环境跑 Mordell-Weil sieve /
genus-one proof，并保存 transcript。
```

如果跑通，才可以把 `strict_proof_status=open` 升级成严格证书。

## 验证

```bash
uv run pytest tests/test_mixed_closure_residual_handoff.py -q
uv run ruff check \
  scripts/theory/export_mixed_closure_residual_handoff.py \
  tests/test_mixed_closure_residual_handoff.py
```

结果：

```text
4 passed
All checks passed!
```
