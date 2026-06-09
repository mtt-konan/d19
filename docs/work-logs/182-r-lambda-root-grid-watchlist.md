# wl182 — `R_lambda` root-grid residual watchlist

日期：2026-06-09

## 1. 本轮目标

wl181 有了 root-grid residual summary：

```text
可以统计 residual 数量和 squareclass pair 分布。
```

本轮再加一个更直接的报警器：

```text
sum_ab_root_grid_residual_watchlist(...)
```

普通话说：

```text
统计表负责看全局分布；
watchlist 负责把最危险的候选直接拎出来。
```

---

## 2. 新 helper

新增：

```text
sum_ab_root_grid_residual_watchlist(
    max_numerator,
    max_denominator,
    extra_conditions=(),
)
```

默认抓两类东西：

```text
1. true_member_pair = True
2. member_squareclass_pair = (1,1)
```

普通话说：

```text
第一类是真正过了四个单项平方检查。
第二类是 squareclass 层面最危险，
因为它看起来已经没有非平凡 squareclass 障碍。
```

---

## 3. 小边界结果

输入：

```text
max_numerator = 26
max_denominator = 23
```

结果：

```text
watchlist = ()
```

这说明：

```text
这个小边界里的已知 residual：
lambda = 535/161
roots = (14/23, 26/7)
pair = (29,29)
```

没有触发最高危险报警。

---

## 4. 测试 guard

测试里额外注入一个 toy true condition：

```text
lambda = 1
roots = (3/4, 4/3)
member_squareclass_pair = (1,1)
true_member_pair = True
```

watchlist 必须返回它。

普通话说：

```text
报警器不能只是“这次没响”；
还要证明真有危险信号进来时它会响。
```

---

## 5. 可以说 / 不能说

可以说：

```text
root-grid 现在能直接监控 true residual 或 pair=(1,1) residual。
小边界 (26,23) 没触发 watchlist。
```

不能说：

```text
pair=(1,1) 不可能。
true residual 不存在。
有理比例主定理已经证明。
```

因为这仍然是有限诊断。

---

## 6. 下一步

更自然的下一步：

```text
1. 扩大 root-grid 边界时先看 watchlist。
2. 若 watchlist 非空，优先审查该候选是否是真危险。
3. 若长期为空，再把 residual 方程改写成 squareclass obstruction。
```

普通话总结：

```text
这轮给下一批搜索装了刹车灯。
灯不亮不是证明；
但灯一亮就要立刻停车看。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_root_grid_residual_watchlist_flags_true_or_trivial_pairs -q
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
