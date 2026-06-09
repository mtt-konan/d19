# wl181 — `R_lambda` root-grid residual summary

日期：2026-06-09

## 1. 本轮目标

wl180 有了 root-grid residual generator：

```text
先枚举 r,s，
再由 lambda = r+s-1 反推长宽比。
```

本轮补一个统计层：

```text
sum_ab_root_grid_residual_summary(...)
```

普通话说：

```text
不是只把 residual 一条条吐出来，
而是顺手统计它们坏在哪类 squareclass 上。
```

---

## 2. 新 helper

新增：

```text
sum_ab_root_grid_residual_summary(
    max_numerator,
    max_denominator,
)
```

返回复用已有结构：

```text
ProductSquareBucketSummary
```

里面有：

```text
bucket_counts
true_member_counts
squareclass_pair_counts_by_bucket
examples_by_bucket
```

普通话说：

```text
同一套仪表盘，
现在既能看 lambda-grid，
也能看 root-grid。
```

---

## 3. 小边界测试

输入：

```text
max_numerator = 26
max_denominator = 23
```

结果：

```text
bucket_counts = {"residual": 1}
true_member_counts = {}
squareclass_pair_counts_by_bucket = {"residual": {(29,29): 1}}
example lambda = 535/161
example roots = (14/23, 26/7)
```

普通话说：

```text
在这个很小的 root-grid 边界里，
唯一 residual 还是那个老熟人，
而且它不是 R_lambda 真点。
```

---

## 4. 对主方向的意义

主目标仍然是：

```text
若 r,s ∈ R_lambda 且 full-plane closure，
是否必须 s = lambda/r？
```

这轮没有证明。

但它把下一步的实验问题变清楚：

```text
residual 桶里，
member_squareclass_pair 是否总是非平凡？
如果出现 pair=(1,1)，那就是理论方向的最高危险信号。
```

普通话说：

```text
我们不是在找“有多少假人”，
而是在看有没有假人拿到了真身份证。
```

---

## 5. 可以说 / 不能说

可以说：

```text
root-grid 现在有了 squareclass 分布统计入口。
小边界 (26,23) 内没有 true residual。
```

不能说：

```text
residual 永远不是真点。
有理比例主定理已经证明。
pair=(1,1) 不可能出现。
```

因为这仍然是有限网格。

---

## 6. 下一步

更自然的下一步：

```text
1. 扩大 root-grid 边界，收集 residual pair 分布。
2. 专门监控 pair=(1,1)。
3. 如果始终只见非平凡 pair，尝试把 residual 条件改写成 squareclass 方程。
```

普通话总结：

```text
这轮不是证明，
而是给证明方向装了一个更好的报警器。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_root_grid_residual_summary_counts_squareclass_pairs -q
```

结果：

```text
1 passed
```

后续还需要跑：

```text
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
