# wl168 — `R_lambda` squareclass-pair abstraction

日期：2026-06-09

## 1. 本轮目标

wl167 说：

```text
A_p,B_p 是平方
```

可以翻成：

```text
r^2+1        与 s^2+1        同 squareclass
r^2+lambda^2 与 s^2+lambda^2 同 squareclass
```

本轮把这两对 squareclass 压成一个摘要：

```text
(u, v)
```

普通话说：

```text
u 表示“到 1 这边坏在哪”。
v 表示“到 lambda 这边坏在哪”。
真正的 R_lambda 成员要求 u=v=1。
```

---

## 2. 新字段

`closure_product_square_conditions(...)` 新增：

```text
member_squareclass_pair
```

当：

```text
member_squareclasses = (u, u, v, v)
```

时：

```text
member_squareclass_pair = (u, v)
```

如果四项没有成对相等，则返回空 tuple：

```text
()
```

---

## 3. 三个样本

### 四项全同假点

```text
lambda = 535/161
r = 14/23
s = 26/7
member_squareclasses = (29, 29, 29, 29)
member_squareclass_pair = (29, 29)
```

### 两对同类假点

```text
lambda = 2
r = s = 3/2
member_squareclasses = (13, 13, 1, 1)
member_squareclass_pair = (13, 1)
```

### 真点

```text
lambda = 1
r = 3/4
s = 4/3
member_squareclasses = (1, 1, 1, 1)
member_squareclass_pair = (1, 1)
```

---

## 4. 小扫描

有限诊断：

```text
lambda = 1..15
relation = sum=A+B
target = lambda + 1
r = small rational with denominator <= 20
s = target - r
只保留 D square 且 A_p,B_p square 的点
```

`member_squareclass_pair` 出现频次前几项：

```text
(2, 2)    60
(5, 13)   20
(10, 34)  20
(17, 65)  20
(26, 106) 20
(37, 157) 20
(2, 218)  20
(65, 1)   20
(13, 1)   10
```

典型样本：

```text
lambda=3,  r=s=2, pair=(5,13)
lambda=5,  r=s=3, pair=(10,34)
lambda=7,  r=s=4, pair=(17,65)
lambda=15, r=s=8, pair=(65,1)
```

普通话说：

```text
很多非平凡 (u,v) 来自 r=s 的中心线样本。
这不是原问题真解，
但它提示 fixed-line / centerline proof note
可能能解释一大类 product-square 假象。
```

---

## 5. 这和主线的关系

原目标是：

```text
若 r,s in R_lambda 且满足 closure，
是否必须 rs=lambda？
```

现在中间多了一层语言：

```text
closure + product-square
=> squareclass pair (u,v)
```

真成员要求：

```text
(u,v) = (1,1)
```

所以可证明的问题变成：

```text
哪些 closure 分支允许非平凡 (u,v)？
这些非平凡 (u,v) 是否都来自特殊线，比如 r=s？
如果不来自特殊线，能不能递降或模排除？
```

普通话说：

```text
我们现在不是直接抓整个平面。
先抓住“坏法”的名字。
坏法有名字以后，才可能分类。
```

---

## 6. 下一步

下一步比较自然的是：

```text
把 r=s 中心线样本单独做 proof note。
```

因为扫描里很多 `(u,v)` 都来自：

```text
r = s = (lambda + 1)/2
```

对于奇数整数 lambda：

```text
lambda = 2n - 1
r = s = n
```

于是：

```text
u = squareclass(n^2 + 1)
v = squareclass(n^2 + lambda^2)
```

这条线很可能能整理成一个可读证明样板：

```text
中心线 product-square 假象为什么多；
但为什么不是真 R_lambda member。
```

普通话总结：

```text
R_lambda 主线和特殊线方向开始接上了。
中心线不是全局证明，
但它可能解释一批最显眼的非平凡 squareclass pair。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_product_square_conditions_do_not_imply_membership -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
30 passed
394 passed, 2 warnings
```
