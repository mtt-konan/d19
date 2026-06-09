# wl179 — `R_lambda` small-height rational pool

日期：2026-06-09

## 1. 本轮目标

wl178 有了 residual grid scanner。

本轮补一个有理比例小高度池：

```text
positive_rational_ratios(max_numerator, max_denominator)
```

普通话说：

```text
以后可以系统生成一批小有理 lambda，
不用手写 lambda 列表。
```

---

## 2. 新 helper

新增：

```text
positive_rational_ratios(max_numerator, max_denominator)
```

例子：

```text
positive_rational_ratios(3,3)
```

返回：

```text
1/3, 1/2, 2/3, 1, 3/2, 2, 3
```

它只是：

```text
枚举 numerator / denominator
用 Fraction 自动约分
去重
排序
```

---

## 3. 小高度 residual 扫描

输入：

```text
lambda_ratios = positive_rational_ratios(20,20)
max_denominator = 20
```

结果：

```text
lambda_count = 255
residual_count = 0
true_count = 0
```

普通话说：

```text
小高度有理 lambda 池里，
这次没有扫到 residual。
```

---

## 4. 边界

不能说：

```text
有理 residual 不存在。
```

因为已知 residual guard：

```text
lambda = 535/161
```

它的 numerator/denominator 都超过 20。

所以本轮结果只能说明：

```text
height <= 20 的这个小池没看到 residual。
```

普通话说：

```text
小池没鱼，
不代表海里没鱼。
```

---

## 5. 当前判断

`positive_rational_ratios` 的价值是：

```text
给 residual scanner 一个稳定输入。
```

但 residual 来源可能不是低高度均匀分布。

已知 guard 的高度：

```text
lambda = 535/161
```

提示下一步不能只做小高度盲扫。

---

## 6. 下一步

更合理的方向：

```text
1. 回到 wl119，追 lambda=535/161 的构造来源。
2. 找到 residual 参数化或生成模式。
3. 再用 positive_rational_ratios 做 sanity scan。
```

普通话总结：

```text
有理池工具有了，
但 residual 更像有结构地产生，
不是随便小高度就冒出来。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_pythagorean_leg_ratios_generate_bounded_slope_pool -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
32 passed
396 passed, 2 warnings
```
