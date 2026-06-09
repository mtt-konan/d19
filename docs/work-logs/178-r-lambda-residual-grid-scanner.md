# wl178 — `R_lambda` residual grid scanner

日期：2026-06-09

## 1. 本轮目标

wl177 说：

```text
需要扩大 residual guard 来源。
```

本轮新增一个更直接的有限网格 scanner：

```text
sum_ab_product_square_residuals_from_grid(...)
```

普通话说：

```text
不再只靠手写 residual guard。
给定一批 lambda，
工具枚举 r，
自动找 residual 桶。
```

---

## 2. 新 helper

新增：

```text
sum_ab_product_square_residuals_from_grid(
    lambda_ratios,
    max_denominator,
)
```

它只处理：

```text
sum=A+B
target = lambda + 1
s = target - r
r = numerator / denominator
denominator <= max_denominator
```

筛选：

```text
product_square_bucket == residual
```

返回：

```text
tuple[ClosureProductSquareConditions, ...]
```

---

## 3. 回归测试

输入：

```text
lambda_ratios = (535/161,)
max_denominator = 23
```

应该找回：

```text
lambda = 535/161
roots = (14/23, 26/7)
bucket = residual
pair = (29,29)
```

普通话说：

```text
已知 residual guard 现在可以由网格 scanner 自动找回。
```

---

## 4. 小实验

输入：

```text
lambda = 535/161, 7, 1, 3/2, 12/13
max_denominator = 40
```

结果：

```text
count = 1
lambda = 535/161
roots = (14/23, 26/7)
pair = (29,29)
true = False
```

可以说：

```text
这个小实验只找回已知 residual，
没有发现 true_member_pair。
```

不能说：

```text
只有这一个 residual。
residual 桶没有真点已经证明。
```

---

## 5. 和 slope scanner 的关系

wl177 里：

```text
pythagorean_leg_ratios(30)
```

没有扫出 residual。

本轮说明：

```text
用 lambda/r 网格可以找回 residual。
```

普通话说：

```text
residual 的来源更像弱 p 模型的有理网格，
不一定来自小 Pythagorean slope 池。
```

---

## 6. 下一步

下一步可以有目的地扩大：

```text
lambda_ratios = 有理数小高度池
max_denominator = 逐步增加
```

但必须记录：

```text
这是有限搜索。
只用于找 residual 形态，
不能当证明。
```

重点统计：

```text
residual count
residual true_member_pair count
residual member_squareclass_pair distribution
```

普通话总结：

```text
第三桶现在有了自动寻找入口。
下一步是看第三桶是不是总坏在非平凡 squareclass 上。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_product_square_bucket_summary_keeps_residual_guard -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
32 passed
396 passed, 2 warnings
```
