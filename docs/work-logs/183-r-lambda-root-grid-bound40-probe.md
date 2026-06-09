# wl183 — `R_lambda` root-grid bound-40 probe

日期：2026-06-09

## 1. 本轮目标

wl182 加了 watchlist：

```text
true_member_pair = True
或 member_squareclass_pair = (1,1)
```

本轮用它做一个适度扩大的有限探针。

普通话说：

```text
不只是看 residual 有多少，
还要看有没有最高危险信号亮灯。
```

---

## 2. 探针设置

跑了三个 root-grid 边界：

```text
bound = 30
bound = 35
bound = 40
```

每次使用：

```text
max_numerator = bound
max_denominator = bound
```

统计：

```text
residual_count
true_count
watchlist_count
top member_squareclass_pair
```

---

## 3. 结果

```text
bound = 30
residual_count = 1
true_count = 0
watchlist_count = 0
top_pairs = [((29,29), 1)]

bound = 35
residual_count = 1
true_count = 0
watchlist_count = 0
top_pairs = [((29,29), 1)]

bound = 40
residual_count = 1
true_count = 0
watchlist_count = 0
top_pairs = [((29,29), 1)]
```

唯一 residual 还是：

```text
lambda = 535/161
roots = (14/23, 26/7)
member_squareclass_pair = (29,29)
true_member_pair = False
```

---

## 4. 普通话解释

到这个边界为止：

```text
没有看到新的 residual。
没有看到 true residual。
没有看到 pair=(1,1) 的最高危险 residual。
```

这个现象说明：

```text
root-grid residual 不是小高度里随便乱冒的一大片。
目前唯一看到的 residual 仍卡在非平凡 squareclass 29 上。
```

---

## 5. 可以说 / 不能说

可以说：

```text
root-grid 到 bound=40 的有限探针没有触发 watchlist。
已知 residual 的障碍仍是 pair=(29,29)。
```

不能说：

```text
residual 只有这一个。
pair=(1,1) 不可能。
true residual 不存在。
有理比例主定理已经证明。
```

因为：

```text
这是有限网格，
不是覆盖所有有理数的证明。
```

---

## 6. 对下一步的影响

继续盲目扩大边界可以做，
但理论收益可能不高。

更有价值的下一步是：

```text
把 residual 条件写成 squareclass 方程：

r+s = lambda+1
(r^2+1)(s^2+1) 是平方
(r^2+lambda^2)(s^2+lambda^2) 是平方
但 r^2+1, s^2+1, r^2+lambda^2, s^2+lambda^2
并不各自都是平方。
```

普通话说：

```text
现在该问的不是“再扫大一点会不会有”，
而是“为什么唯一看到的假阳性会卡在同一个非平凡平方类上”。
```

---

## 7. 验证

本轮没有改代码。

已跑探针：

```text
PYTHONPATH=src uv run python - <<'PY'
from collections import Counter
from rational_distance.concordant.rational_ratio import (
    sum_ab_product_square_residuals_from_root_grid,
    sum_ab_root_grid_residual_watchlist,
)

for bound in (30, 35, 40):
    residuals = sum_ab_product_square_residuals_from_root_grid(
        max_numerator=bound,
        max_denominator=bound,
    )
    watchlist = sum_ab_root_grid_residual_watchlist(
        max_numerator=bound,
        max_denominator=bound,
    )
    pair_counts = Counter(item.member_squareclass_pair for item in residuals)
    true_count = sum(item.true_member_pair for item in residuals)
    print(bound, len(residuals), true_count, len(watchlist), pair_counts.most_common(10))
PY
```

结果：

```text
bound 30: residual_count=1, true_count=0, watchlist_count=0
bound 35: residual_count=1, true_count=0, watchlist_count=0
bound 40: residual_count=1, true_count=0, watchlist_count=0
```
