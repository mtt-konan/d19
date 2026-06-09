# wl187 — `R_lambda` sum=A+B reciprocal obstruction

日期：2026-06-09

## 1. 本轮目标

wl185 / wl186 把主风险压到：

```text
branch = true-nonreciprocal
```

本轮关闭另一个容易混淆的分支：

```text
sum=A+B 的 reciprocal / mirror 分支。
```

普通话说：

```text
如果闭合对刚好是镜像对，
它其实会被迫用到点 1；
而点 1 永远不是 R_lambda 真成员。
```

---

## 2. 新 helper

新增：

```text
sum_ab_reciprocal_obstruction(lambda_ratio)
```

返回：

```text
SumAbReciprocalObstruction
```

记录：

```text
roots
forced_unit_root
unit_leg_value
unit_leg_is_square
true_roots
branch_closed
```

---

## 3. 小定理

在 sum=A+B 分支里：

```text
r+s = lambda+1
```

如果再要求 reciprocal/mirror：

```text
rs = lambda
```

那么 r,s 是方程：

```text
t^2 - (lambda+1)t + lambda = 0
```

的两个根。

这个方程分解为：

```text
(t-1)(t-lambda)=0
```

所以：

```text
{r,s} = {1, lambda}
```

普通话说：

```text
sum=A+B 的镜像闭合对没有自由度，
只能是 1 和 lambda。
```

---

## 4. 为什么不是真点

`R_lambda` 成员要求：

```text
r^2 + 1 是有理平方
```

但 forced root 里有：

```text
r = 1
```

于是：

```text
1^2 + 1 = 2
```

而：

```text
2 不是有理平方。
```

所以：

```text
1 不属于 R_lambda。
```

因此：

```text
sum=A+B reciprocal branch 不可能是 true branch。
```

---

## 5. 例子

输入：

```text
lambda = 3/4
```

得到：

```text
roots = (1, 3/4)
forced_unit_root = 1
unit_leg_value = 2
unit_leg_is_square = False
true_roots = ()
branch_closed = True
```

普通话说：

```text
无论 lambda 是多少，
这条分支都会碰到点 1，
所以直接死在 2 不是平方上。
```

---

## 6. 和主目标的关系

主目标是：

```text
若 r,s ∈ R_lambda 且 full-plane closure，
是否必须 s=lambda/r？
```

对 sum=A+B 这条闭合线来说，
如果真的满足：

```text
s=lambda/r
```

那它反而落到：

```text
{r,s} = {1,lambda}
```

然后被本轮小定理排除。

普通话说：

```text
sum=A+B 里，镜像分支不是危险分支；
它是已经关闭的分支。
真正危险的仍然是 true-nonreciprocal。
```

---

## 7. 可以说 / 不能说

可以说：

```text
sum=A+B reciprocal branch 已经有本地小证明排除真成员。
这个结论不是有限扫描。
```

不能说：

```text
true-nonreciprocal 已经排除。
其他 full-plane closure 关系也已经排除。
有理比例主定理已经证明。
```

因为：

```text
本轮只关闭 sum=A+B 的 reciprocal/mirror 分支。
```

---

## 8. 下一步

下一步应该继续攻：

```text
true-nonreciprocal:

r,s ∈ R_lambda
r+s = lambda+1
rs != lambda
```

普通话总结：

```text
镜像门关上了。
现在只剩真正麻烦的非镜像真闭合门。
```

---

## 9. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_reciprocal_orbit_sum_ab_roots_are_not_true_members_for_rational_lambda -q
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
