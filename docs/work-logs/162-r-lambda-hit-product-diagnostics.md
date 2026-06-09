# wl162 — `R_lambda` hit product diagnostics

日期：2026-06-09

## 1. 本轮问题

wl161 把 `sum=A+B` near-miss family 支线暂时收束：

```text
有结构，
但暂时不像直接递降主路。
```

这轮回到 P0 主线：

```text
R_lambda translation theorem
```

目标仍是：

```text
若 r,s in R_lambda 且满足 full-plane closure，
是否必须 rs=lambda？
```

普通话说：

```text
如果两个点真的都能配上左右两边，
又刚好闭合，
那它们是不是只能是一对 reciprocal 镜像？
```

---

## 2. 新 helper

新增：

```text
rational_ratio_hit_product_diagnostics(lambda_ratio, ratios)
```

它复用：

```text
find_rational_ratio_hits(...)
```

并给每个 closure hit 增加：

```text
product = r1*r2
product_equals_lambda
reciprocal_pair
```

普通话说：

```text
先不证明所有情况。
先让工具直接告诉我们：
这个 closure hit 的乘积是不是 lambda。
```

---

## 3. 一个边界例子

例子：

```text
lambda = 6
r = 2
s = 3
```

它满足：

```text
r+s = 5 = |lambda-1|
rs = 6 = lambda
```

所以 helper 标记：

```text
relation = sum=|A-B|
product_equals_lambda = True
reciprocal_pair = True
```

但注意：

```text
这只是 closure-level reciprocal 例子。
它不自动说明 r,s 是真的 R_lambda 成员。
```

普通话说：

```text
闭合和 reciprocal 是一回事；
真正在 R_lambda 里面，是另一回事。
```

---

## 4. 小范围扫描

用：

```text
pythagorean_leg_ratios(18)
lambda = 2..15
```

扫 closure hits。

观察到：

```text
lambda=5:
  hits=1
  product_equals_lambda=0
  true_R_lambda_hits=0

lambda=7:
  hits=2
  product_equals_lambda=0
  true_R_lambda_hits=0

lambda=9:
  hits=1
  product_equals_lambda=0
  true_R_lambda_hits=0
```

典型假 hit：

```text
lambda=7
r=8/15
s=112/15
r+s=8=lambda+1
rs=896/225 != 7
```

但它不是真 `R_lambda` hit。

普通话说：

```text
普通 Pythagorean leg pool 里会出现 closure 假象。
它们乘积不等于 lambda。
但因为它们还没通过 R_lambda 两边条件，
不能拿来反驳 P0。
```

---

## 5. 当前判断

可以说：

```text
product diagnostics 能把 closure hit 分成 p=lambda 和 p!=lambda。
有限 slope pool 中的 p!=lambda closure hits 目前都是 false members。
```

不能说：

```text
已经证明 R_lambda closure => p=lambda。
有限扫描支持 theorem 就等于 theorem。
普通 closure hit 反驳了 P0。
```

普通话说：

```text
这轮只是把 P0 的验算入口补上。
真正要打的还是 R_lambda membership 条件。
```

---

## 6. 下一步

更合理的下一步：

```text
1. 对 product diagnostics 增加 true_member_pair 字段。
2. 扫描有限 pool 时直接分出 true hits 和 false hits。
3. 如果发现 true hit 且 p!=lambda，那 P0 猜想错。
4. 如果只发现 false hits，就回到代数证明 membership => p=lambda。
```

普通话说：

```text
我们要找的不是普通闭合点，
而是真正活在 R_lambda 里的闭合点。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_rational_ratio_hit_product_diagnostics_identify_reciprocal_pair -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
30 passed
394 passed, 2 warnings
```
