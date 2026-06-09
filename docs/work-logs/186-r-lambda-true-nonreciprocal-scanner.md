# wl186 — `R_lambda` true-nonreciprocal scanner

日期：2026-06-09

## 1. 本轮目标

wl185 把主证明目标压缩成：

```text
排除 branch = true-nonreciprocal
```

本轮补一个有限 scanner：

```text
scan_sum_ab_true_closure_relations(...)
```

普通话说：

```text
以后不是泛泛扫“闭合对”，
而是直接问有没有最危险的真非镜像闭合对。
```

---

## 2. 新 helper

新增：

```text
scan_sum_ab_true_closure_relations(
    lambda_ratios,
    max_numerator,
    max_denominator,
    branches=None,
)
```

它做的事：

```text
1. 枚举有限有理 root pool。
2. 对每个 lambda，令 target=lambda+1。
3. 枚举 r，并用 s=target-r 强制 sum=A+B closure。
4. 要求 s 也在同一个有限 root pool。
5. 调 sum_ab_true_closure_relation 做分支分类。
6. 可用 branches 只保留指定分支。
```

普通话说：

```text
它不是证明器，
只是把危险分支从有限池里捞出来。
```

---

## 3. 测试例子

对：

```text
lambda = 7
root pool = 正整数 1..7
```

sum=A+B 闭合对是：

```text
(1,7) -> false-reciprocal
(2,6) -> false-residual
(3,5) -> false-residual
(4,4) -> false-centerline
```

普通话说：

```text
闭合对很多，
但没有一个是真 R_lambda 成员对。
```

---

## 4. 小探针

跑了两个有限池：

```text
lambda = integers 1..12
root pool = positive_rational_ratios(12,12)
```

结果：

```text
lambda_count = 12
relation_count = 111
branch_counts = {
  false-centerline: 11,
  false-reciprocal: 11,
  false-residual: 89,
}
true_nonreciprocal_count = 0
```

另一个：

```text
lambda = positive_rational_ratios(6,6)
root pool = positive_rational_ratios(12,12)
```

结果：

```text
lambda_count = 23
relation_count = 230
branch_counts = {
  false-centerline: 23,
  false-reciprocal: 22,
  false-residual: 185,
}
true_nonreciprocal_count = 0
```

---

## 5. 可以说 / 不能说

可以说：

```text
这两个小有限池没有看到 true-nonreciprocal。
scanner 现在可以专门监控 true-nonreciprocal。
```

不能说：

```text
true-nonreciprocal 不存在。
有理比例主定理已经证明。
所有 lambda 都已经覆盖。
```

因为：

```text
lambda pool 和 root pool 都是有限的。
```

---

## 6. 对主证明的意义

这轮没有证明。

但它把实验入口和理论目标对齐了：

```text
如果 scanner 找到 true-nonreciprocal，
那就是最高优先级候选。

如果长期找不到，
下一步就不该只加边界，
而应该从 r,s ∈ R_lambda 和 r+s=lambda+1 推导矛盾。
```

普通话说：

```text
有限扫描现在只负责报警，
真正要推进还得开始代数证明。
```

---

## 7. 下一步

更理论的下一步：

```text
1. 参数化 r ∈ R_lambda：
   r^2+1 = square
   r^2+lambda^2 = square

2. 同时参数化 s ∈ R_lambda。

3. 加入 r+s=lambda+1。

4. 尝试推出 impossible 或 rs=lambda。
```

普通话总结：

```text
现在 scanner 已经能看住“鬼”。
接下来该研究为什么这只鬼应该不存在。
```

---

## 8. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_scan_sum_ab_true_closure_relations_monitors_nonreciprocal_branch -q
```

结果：

```text
1 passed
```

小探针命令：

```text
PYTHONPATH=src uv run python - <<'PY'
from collections import Counter
from fractions import Fraction
from rational_distance.concordant.rational_ratio import (
    scan_sum_ab_true_closure_relations,
    positive_rational_ratios,
)

lambda_sets = {
    'integers-1-12': tuple(Fraction(i) for i in range(1, 13)),
    'rationals-6x6': positive_rational_ratios(6, 6),
}
for name, lambdas in lambda_sets.items():
    relations = scan_sum_ab_true_closure_relations(
        lambda_ratios=lambdas,
        max_numerator=12,
        max_denominator=12,
    )
    branch_counts = Counter(item.branch for item in relations)
    dangerous = tuple(item for item in relations if item.branch == 'true-nonreciprocal')
    print(name, len(lambdas), len(relations), branch_counts, len(dangerous))
PY
```

后续还需要跑：

```text
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
