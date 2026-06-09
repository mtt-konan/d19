# wl177 — `R_lambda` slope-to-product bucket helper

日期：2026-06-09

## 1. 本轮目标

wl176 的下一步是：

```text
扩大 residual guard 来源。
```

本轮先做一个小 helper：

```text
sum_ab_product_square_condition_from_slopes(x, y)
```

普通话说：

```text
给两个 scaled slopes，
直接生成 sum=A+B 的 product-square 账本。
```

---

## 2. 新 helper

新增：

```text
sum_ab_product_square_condition_from_slopes(slope1, slope2)
```

它复用：

```text
sum_ab_point_from_slopes(...)
```

流程：

```text
x = r/lambda
y = s/lambda
lambda = 1 / (x+y-1)
r = lambda*x
s = lambda*y
```

然后返回：

```text
closure_product_square_conditions(lambda, lambda+1, rs, sum=A+B)
```

如果：

```text
x+y <= 1
```

则没有 sum=A+B 点，返回：

```text
None
```

---

## 3. 已知 residual guard 可以复现

已知样本：

```text
lambda = 535/161
r = 14/23
s = 26/7
```

对应 scaled slopes：

```text
x = r/lambda
y = s/lambda
```

用新 helper 可以复现：

```text
lambda_ratio = 535/161
roots = (14/23, 26/7)
product_square_bucket = residual
member_squareclass_pair = (29,29)
```

普通话说：

```text
这条 residual 不再只能手写。
至少可以从 scaled slope 坐标复原。
```

---

## 4. 小扫描边界

尝试：

```text
slopes = pythagorean_leg_ratios(30)
用所有 slope pair 生成 condition
筛 product_square_bucket = residual
```

结果：

```text
slopes = 372
residuals = 0
```

这说明：

```text
Pythagorean slope 小池没有自动给出 residual。
```

不能说：

```text
residual 不存在。
```

因为已知 residual guard 已经存在。

普通话说：

```text
这个 helper 能复原 residual，
但还没解决“怎么批量生成 residual 来源”。
```

---

## 5. 当前判断

可以说：

```text
从 arbitrary scaled slope pair 到 product bucket 的入口已经有了。
```

不能说：

```text
已经有 residual 批量生成算法。
Pythagorean slope 池没扫到 residual 就说明 residual 稀少或不存在。
```

---

## 6. 下一步

下一步更合理的是回看 wl119：

```text
residual guard 是如何被构造出来的？
```

也就是追：

```text
lambda=535/161, r=14/23, s=26/7
```

背后的参数，而不是盲扫 Pythagorean slopes。

如果能找到参数化来源，就可以：

```text
批量生成 residual guard
统计 residual (u,v)
检查是否出现 true_member_pair
```

普通话总结：

```text
这轮只是打通入口。
真正要找的是 residual 的生成机制。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_slope_pair_translates_to_rational_ratio_membership -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
32 passed
396 passed, 2 warnings
```
