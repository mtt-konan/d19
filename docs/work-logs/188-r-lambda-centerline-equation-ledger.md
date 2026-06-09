# wl188 — `R_lambda` centerline equation ledger

日期：2026-06-09

## 1. 本轮目标

wl187 关闭了：

```text
sum=A+B reciprocal / mirror 分支。
```

本轮整理另一个低维分支：

```text
sum=A+B centerline
```

普通话说：

```text
镜像门已经关了；
中心线门还没全局证明关上，
但我们可以把门锁长什么样写清楚。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_equations(lambda_ratio)
```

返回：

```text
SumAbCenterlineEquations
```

记录：

```text
center
unit_value
lambda_value
unit_is_square
lambda_is_square
unit_squareclass
lambda_squareclass
true_member
obstruction
```

---

## 3. 中心线方程

sum=A+B centerline 是：

```text
r = s
r+s = lambda+1
```

所以：

```text
r = s = (lambda+1)/2
```

要成为真 `R_lambda` 点，需要同时满足：

```text
((lambda+1)/2)^2 + 1         是有理平方
((lambda+1)/2)^2 + lambda^2  是有理平方
```

普通话说：

```text
中心线不是一个二维问题了，
它被压成 lambda 这一维上的两个平方条件。
```

---

## 4. 样本 1：lambda=3

```text
center = 2
unit_value = 5
lambda_value = 13
unit_is_square = False
lambda_is_square = False
unit_squareclass = 5
lambda_squareclass = 13
true_member = False
obstruction = both-legs
```

普通话说：

```text
两边距离都不是勾股平方。
```

---

## 5. 样本 2：lambda=15

```text
center = 8
unit_value = 65
lambda_value = 289
unit_is_square = False
lambda_is_square = True
unit_squareclass = 65
lambda_squareclass = 1
true_member = False
obstruction = unit-leg
```

普通话说：

```text
到 lambda 那边过了，
但到单位边还是坏，
所以仍不是真点。
```

---

## 6. 可以说 / 不能说

可以说：

```text
centerline 分支已被整理成两个明确平方方程。
lambda=3、lambda=15 样本的坏法可精确解释。
```

不能说：

```text
centerline 对所有 lambda 都不可能。
true-centerline 已经全局排除。
有理比例主定理已经证明。
```

因为：

```text
本轮只是 equation ledger，
不是递降证明或完整模证明。
```

---

## 7. 对主目标的意义

目前 sum=A+B 的低维分支状态：

```text
reciprocal / mirror:
  已有小证明关闭，强迫 roots=(1,lambda)，点 1 失败。

centerline:
  已压成两个平方方程，但尚未全局证明关闭。

true-nonreciprocal:
  仍是主危险分支。
```

普通话说：

```text
中心线不是最乱的部分，
但也还不是已经拿下的部分。
它更像固定比例线 A=kB 路线的样板。
```

---

## 8. 下一步

两条自然路线：

```text
1. 用 Yang Ji / 固定线方法攻 centerline 方程：
   ((lambda+1)/2)^2 + 1 = square
   ((lambda+1)/2)^2 + lambda^2 = square

2. 继续主线，直接攻 true-nonreciprocal：
   r,s ∈ R_lambda
   r+s=lambda+1
   r != s
   rs != lambda
```

普通话总结：

```text
这轮把中心线门牌挂好了。
下一步可以选择砸这扇门，
也可以先去砸真正危险的非镜像门。
```

---

## 9. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_equations_expose_two_square_conditions -q
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
