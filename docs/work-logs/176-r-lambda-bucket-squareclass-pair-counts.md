# wl176 — `R_lambda` bucket squareclass-pair counts

日期：2026-06-09

## 1. 本轮目标

wl175 已经能统计：

```text
centerline / reciprocal / residual
```

但还不能直接回答：

```text
每个桶里的 (u,v) 长什么样？
```

本轮给 summary 增加：

```text
squareclass_pair_counts_by_bucket
```

普通话说：

```text
不只数桶，
还数每个桶里具体坏法。
```

---

## 2. 新字段

`ProductSquareBucketSummary` 新增：

```text
squareclass_pair_counts_by_bucket
```

结构：

```text
{
  bucket: {
    (u,v): count
  }
}
```

其中：

```text
u = squareclass pair 的第一边
v = squareclass pair 的第二边
```

---

## 3. 当前诊断结果

输入仍是：

```text
lambda = 1..15
max_denominator = 20
extra_conditions = 已知 residual guard
```

总桶：

```text
bucket_counts = {
  centerline: 230,
  reciprocal: 40,
  residual: 1,
}
```

pair 分布摘录：

```text
centerline:
  (2,2)     20
  (5,13)    20
  (10,34)   20
  (17,65)   20
  (26,106)  20
  ...

reciprocal:
  (2,2)     40

residual:
  (29,29)    1
```

普通话说：

```text
centerline 桶有很多不同坏法；
reciprocal 桶在这个池里集中到 (2,2)；
residual guard 是 (29,29)。
```

---

## 4. 边界

可以说：

```text
当前诊断池里 residual 的已知样本是 (29,29)。
```

不能说：

```text
所有 residual 都是 (29,29)。
所有 residual 都是 (u,u)。
residual 桶没有 true_member_pair 已经被证明。
```

普通话说：

```text
这只是把已知坏法记清楚，
不是把所有坏法证明完。
```

---

## 5. 下一步

现在可以更有目标地扩大 residual 来源：

```text
1. 生成更多有理 lambda residual guard。
2. 统计 residual 的 (u,v)。
3. 看 residual 是否总是非平凡 pair。
4. 特别找 residual 中是否出现 (1,1) 或 true_member_pair=True。
```

如果 residual 总是：

```text
(u,v) != (1,1)
```

那就支持下一条证明路线：

```text
residual bucket => not true R_lambda member pair
```

普通话总结：

```text
第三桶现在不是黑箱了。
至少工具能告诉我们第三桶坏成什么 squareclass。
```

---

## 6. 验证

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
