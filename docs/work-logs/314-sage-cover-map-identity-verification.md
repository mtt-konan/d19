# wl314 - Sage cover map identity verification

日期：2026-07-07

## 一句话结论

priority top-4 residual cover 的 cover-to-elliptic maps 现在用 Sage 做了恒等式验证。

普通话说：以前 handoff 里保存了 PARI 给出的 map。现在我们进一步检查：把这个 map 代进
目标椭圆曲线方程，利用 cover 方程 `y^2=f(x)` 化简后，残差确实为 0。

## 新增脚本

```text
scripts/theory/sage_verify_mixed_closure_handoff_maps.py
tests/test_sage_verify_mixed_closure_handoff_maps.py
```

验证方式：

```text
cover: y^2 = f(x)
map: (x,y) -> (X(x,y), Y(x,y))
elliptic equation: Y^2 + a1XY + a3Y = X^3 + a2X^2 + a4X + a6
```

脚本在 Sage 里计算残差，然后用 `y^2=f(x)` 把残差化成：

```text
A(x) + y B(x)
```

只有 `A(x)=0` 且 `B(x)=0` 时，才记录：

```text
identity_verified = true
```

## 真实运行

第一组：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_verify_mixed_closure_handoff_maps.py \
  --handoff results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4.json \
  --out results/mixed_closure_residual_handoffs/priority_001_115_297_AA_covers_3_4_map_verify.json \
  --timeout 60 \
  --strict
```

输出：

```text
status=ok
all_verified=True
```

第二组：

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/sage_verify_mixed_closure_handoff_maps.py \
  --handoff results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3.json \
  --out results/mixed_closure_residual_handoffs/priority_003_575_4641_AA_covers_4_3_map_verify.json \
  --timeout 60 \
  --strict
```

输出：

```text
status=ok
all_verified=True
```

关键 JSON：

```text
priority_001 covers 3,4: identity_verified=true, residual_even_degree=-1, residual_odd_degree=-1
priority_003 covers 4,3: identity_verified=true, residual_even_degree=-1, residual_odd_degree=-1
```

然后 priority handoff audit 用 `--require-map-verifications` 重新跑：

```text
ready=True
groups_checked=2
map_verify_status_counts.ok=2
violations=[]
```

## 边界

这仍然不是 residual cover 无点证明。

它证明的是一件较小但重要的事：

```text
当前 handoff 里的 rational map 确实把这四个 cover 映到对应 elliptic curve。
```

它不证明：

```text
cover 没有有理点；
Selmer gap 一定来自已证明的 Sha[2] 元素；
BSD 条件诊断可以替代严格 rank 证书。
```

## 验证

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest \
  tests/test_sage_verify_mixed_closure_handoff_maps.py \
  -q

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/sage_verify_mixed_closure_handoff_maps.py \
  tests/test_sage_verify_mixed_closure_handoff_maps.py
```

结果：

```text
4 passed
All checks passed!
```
