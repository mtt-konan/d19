# wl189 — `R_lambda` centerline unit-leg parameterization

日期：2026-06-09

## 1. 本轮目标

wl188 把 centerline 写成两个平方条件：

```text
center^2 + 1         是平方
center^2 + lambda^2  是平方
```

本轮先吃掉第一个条件：

```text
center^2 + 1 是平方
```

普通话说：

```text
先让中心点到单位边自动成为勾股距离，
再看到 lambda 边的距离还剩什么障碍。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_from_unit_leg_param(parameter)
```

返回：

```text
SumAbCenterlineUnitLegParam
```

记录：

```text
parameter
center
lambda_ratio
unit_hypotenuse
equations
remaining_squareclass
true_member
```

---

## 3. 参数化

用标准有理勾股参数：

```text
center = 2t / (1 - t^2)
h       = (1 + t^2) / (1 - t^2)
```

那么自动有：

```text
center^2 + 1 = h^2
```

centerline 还要求：

```text
center = (lambda+1)/2
```

所以：

```text
lambda = 2center - 1
```

普通话说：

```text
一个参数 t 决定 center，
center 又决定 lambda。
第一条平方条件被自动满足，
剩下只看第二条。
```

---

## 4. 剩余方程

剩下要检查：

```text
center^2 + lambda^2 是平方
```

其中：

```text
center = 2t / (1 - t^2)
lambda = 4t / (1 - t^2) - 1
```

普通话说：

```text
centerline 真点问题被压成：
找一个有理 t，让这个剩余表达式也是平方。
```

---

## 5. 样本

输入：

```text
t = 3/5
```

得到：

```text
center = 15/8
lambda = 11/4
unit_hypotenuse = 17/8
unit_value = 289/64
lambda_value = 709/64
remaining_squareclass = 709
true_member = False
```

普通话说：

```text
第一条已经过了：
15/8, 1, 17/8 是勾股。

但第二条剩下 709/64，
709 不是平方类 1，
所以中心线真点没有出现。
```

---

## 6. 可以说 / 不能说

可以说：

```text
centerline 的 unit-leg 条件已经可以用一个有理参数自动满足。
centerline 真点问题剩下 lambda-leg 条件。
```

不能说：

```text
centerline 已经全局排除。
剩余方程不可能有有理解。
有理比例主定理已经证明。
```

因为：

```text
本轮只是参数化第一条件，
还没有证明剩余方程无解。
```

---

## 7. 下一步

下一步可以对剩余方程做两件事：

```text
1. 展开成 t 的有理平方方程，寻找模障碍。
2. 换参数 u/v，把它变成整数四次方程，看是否有递降结构。
```

普通话总结：

```text
中心线现在只剩一只脚卡住。
如果能证明这只脚永远过不了，
centerline 分支就可以真正关掉。
```

---

## 8. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_unit_leg_param_reduces_to_lambda_leg_check -q
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
