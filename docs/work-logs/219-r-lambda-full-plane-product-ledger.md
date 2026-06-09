# wl219 — `R_lambda` full-plane product ledger

日期：2026-06-09

## 1. 本轮目标

wl218 已经把 full-plane closure 从 sum-only 升级成四关系分类器。

本轮继续把危险分支接到 product 方程账本：

```text
r,s in R_lambda
full-plane closure holds
p = rs
```

普通话说：

```text
上一轮知道“坏东西”叫什么。
这轮把坏东西放到方程桌面上。
```

## 2. 新增 helper

新增：

```text
full_plane_closure_product_ledger(lambda_ratio, r, s, relation)
full_plane_closure_product_summary(...)
```

返回：

```text
FullPlaneClosureProductLedger
FullPlaneClosureProductSummary
```

ledger 连接两层账本：

```text
classification = full_plane_true_closure_relation(...)
conditions     = closure_product_square_conditions(...)
```

并记录：

```text
target
product = rs
product_equals_lambda
danger_branch
```

其中：

```text
danger_branch = classification.branch == "true-nonreciprocal"
```

## 3. 一个重要 guard

`full_plane_closure_product_ledger` 只接受已经闭合的 pair。

如果：

```text
classification.closes_relation == False
```

会直接拒绝。

原因是 product ledger 使用 relation 的 target 来恢复 roots。
如果原 pair 根本不闭合，那么：

```text
target, p=rs
```

恢复出来的 roots 就不是原来的 `r,s`。

普通话说：

```text
没闭合的 pair 不能拿来做闭合方程账本。
不然是在给另一个点记账。
```

## 4. 方程边界

已有 `closure_product_square_conditions` 给出统一公式。

设：

```text
p = rs
T = closure target
```

sum 型 closure：

```text
D = T^2 - 4p
```

diff 型 closure：

```text
D = T^2 + 4p
```

乘积层必要条件：

```text
A_p = p^2 + eps*2p + T^2 + 1
B_p = p^2 + eps*2lambda^2*p + lambda^2*T^2 + lambda^4
```

其中：

```text
eps = -1  对应 sum closure
eps = +1  对应 diff closure
```

并且恒有：

```text
B_p - lambda^2 A_p = (lambda^2 - 1)(lambda^2 - p^2)
```

提醒：

```text
A_p, B_p 是平方
```

只是乘积层必要条件，不等于：

```text
r,s 都在 R_lambda。
```

## 5. 小池诊断

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from fractions import Fraction
from rational_distance.concordant.rational_ratio import full_plane_closure_product_summary

summary = full_plane_closure_product_summary(
    lambda_ratios=(Fraction(1), Fraction(7)),
    max_numerator=10,
    max_denominator=10,
    include_centerline=True,
)
print(summary)
PY
```

结果：

```text
total_relations = 48
branch_counts = {
  'false-centerline': 3,
  'false-reciprocal': 2,
  'false-residual': 43,
}
product_bucket_counts = {
  ('diff=A+B', 'none'): 17,
  ('diff=|A-B|', 'none'): 3,
  ('diff=|A-B|', 'reciprocal'): 1,
  ('sum=A+B', 'centerline'): 2,
  ('sum=A+B', 'none'): 18,
  ('sum=A+B', 'reciprocal'): 1,
  ('sum=|A-B|', 'centerline'): 1,
  ('sum=|A-B|', 'none'): 5,
}
danger_count = 0
```

普通话说：

```text
这个小池里没有 true-nonreciprocal。
而且大部分 closure pair 连 product-square 必要条件都不过。
```

但这仍然只是有限诊断。

## 6. 对下一步的影响

现在主线可以从一句话：

```text
证明 full-plane closure 强迫 p=lambda
```

变成更具体的四关系方程问题：

```text
relation fixed
T fixed as lambda+1 or |lambda-1|
D square
four member squares true
p != lambda
```

下一步可以做：

```text
1. 对四种 relation 分别写 p != lambda 的 symbolic obstruction target。
2. 优先看 product_bucket != none 但 true_member_pair=False 的样本，因为它们最像“假阳性机制”。
3. 不再只扩大有限扫描；要寻找 squareclass、局部模条件或曲线降维。
```

普通话总结：

```text
这轮把坏分支从“分类标签”推进成“方程账本”。
还没证明它不存在，
但后面已经知道要在哪一层下手。
```

## 7. 验证

```bash
uv run pytest tests/test_rational_ratio.py -q
```

```text
49 passed
```

```bash
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

```text
All checks passed
```
