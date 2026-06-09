# wl185 — `R_lambda` true closure branch classifier

日期：2026-06-09

## 1. 本轮目标

wl184 把 residual 写成 squareclass 方程：

```text
弱 product-square 只要求成对 squareclass 相同，
真 R_lambda 点要求 squareclass 都是 1。
```

本轮往主定理靠一步：

```text
给 sum=A+B 闭合对做分支分类。
```

普通话说：

```text
不要只说“闭合了”，
要明确它到底是镜像根、中心线、假 residual，
还是最危险的真非镜像根。
```

---

## 2. 新 helper

新增：

```text
sum_ab_true_closure_relation(
    lambda_ratio,
    r,
    s,
)
```

返回：

```text
SumAbTrueClosureRelation
```

记录：

```text
closes_sum_ab
r_true_member
s_true_member
both_true_members
reciprocal_pair
centerline
branch
```

---

## 3. 分支含义

目前分类：

```text
not-sum-ab
false-centerline
true-centerline
false-reciprocal
true-reciprocal
true-nonreciprocal
false-residual
```

其中主证明最怕的是：

```text
true-nonreciprocal
```

普通话说：

```text
这就是“两个点都是真的 R_lambda 点，
也满足 sum=A+B 闭合，
但不是 rs=lambda”的情况。
```

如果要证明主目标：

```text
若 r,s ∈ R_lambda 且 sum=A+B closure，
是否必须 s=lambda/r？
```

那在这个 helper 语言里就是：

```text
排除 true-nonreciprocal。
```

---

## 4. 一个重要修正

之前容易混淆：

```text
lambda = 1
r = 3/4
s = 4/3
```

这是一个 toy true pair：

```text
r,s 都是真 R_lambda 点，
rs=lambda。
```

但它不满足：

```text
r+s=lambda+1
```

因为：

```text
3/4 + 4/3 = 25/12
lambda + 1 = 2
```

所以它不是 sum=A+B closure。

普通话说：

```text
它是“真镜像对”，
但不是这一条闭合线上的真镜像对。
```

---

## 5. reciprocal 闭合根的边界

在 sum=A+B 里，如果还要求：

```text
rs=lambda
```

那么：

```text
r+s=lambda+1
```

会给出：

```text
(r-1)(r-lambda)=0
```

也就是根是：

```text
r=1 或 r=lambda
```

普通话说：

```text
sum=A+B 的镜像闭合根其实就是 (1, lambda)。
```

但 `1` 不是 R_lambda 的真成员，因为：

```text
1^2 + 1 = 2
```

不是有理平方。

所以测试里：

```text
lambda = 7
roots = (1,7)
branch = false-reciprocal
```

---

## 6. 已知 residual

已知 residual：

```text
lambda = 535/161
r = 14/23
s = 26/7
```

满足：

```text
closes_sum_ab = True
reciprocal_pair = False
both_true_members = False
branch = false-residual
```

普通话说：

```text
它闭合，
但两个点不是真的 R_lambda 点；
所以不是反例。
```

---

## 7. 对主方向的意义

这轮没有证明主定理。

但它把目标改写成一个更精确的问题：

```text
能否证明 branch = true-nonreciprocal 永远不会出现？
```

并且还提醒：

```text
sum=A+B 的 reciprocal 根本身通常是 false-reciprocal，
真正的危险不在这个显然镜像分支，
而在非 reciprocal 的真闭合分支。
```

---

## 8. 可以说 / 不能说

可以说：

```text
现在有 helper 可以把 sum=A+B 闭合对按证明危险程度分类。
已知 residual 是 false-residual。
sum=A+B 的 reciprocal 根 (1,lambda) 是 false-reciprocal。
```

不能说：

```text
true-nonreciprocal 已被排除。
有理比例主定理已经证明。
所有 full-plane closure 都已分类完毕。
```

因为：

```text
这只是分类 ledger，
不是全空间证明。
```

---

## 9. 下一步

下一步可以走两条：

```text
1. 理论：从 r,s ∈ R_lambda 和 r+s=lambda+1 推导，尝试直接排除 true-nonreciprocal。
2. 实验：构造 bounded true-closure scanner，只监控 branch=true-nonreciprocal。
```

普通话总结：

```text
这轮把“要证明什么”压缩成一个更尖的问题：
别再泛泛说 residual，
就盯 true-nonreciprocal 这只鬼。
```

---

## 10. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_true_closure_relation_classifies_proof_branches -q
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
