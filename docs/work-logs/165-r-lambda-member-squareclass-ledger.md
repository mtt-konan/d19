# wl165 — `R_lambda` member squareclass ledger

日期：2026-06-09

## 1. 本轮目标

wl164 已经把 `R_lambda` product ledger 分成三层：

```text
1. T,p 能不能拆回有理 r,s；
2. A_p,B_p 是否是平方；
3. r,s 是否真的在 R_lambda。
```

本轮继续补一层：

```text
四个真实单项分别属于哪个 squareclass？
```

普通话说：

```text
我们不只想知道它坏了，
还想知道它是怎么坏的。
```

---

## 2. 新字段

`closure_product_square_conditions(...)` 新增：

```text
member_squareclasses
```

对应四个单项：

```text
r^2+1
s^2+1
r^2+lambda^2
s^2+lambda^2
```

如果某一项是有理平方，它的 squareclass 是：

```text
1
```

如果不是平方，squareclass 记录它差哪个平方因子。

---

## 3. 关键样本

沿用 wl164 的假阳性：

```text
lambda = 535/161
r = 14/23
s = 26/7
T = lambda + 1
p = rs
```

它满足：

```text
r+s = T
D 是平方
A_p 是平方
B_p 是平方
```

但真实成员检查：

```text
member_square_flags = (False, False, False, False)
```

本轮新增观察：

```text
member_squareclasses = (29, 29, 29, 29)
```

普通话说：

```text
四个单项全都不是平方，
但它们全都坏在同一个平方类 29 上。
所以两两相乘时，29*29 被吃掉，
乘积层面就伪装成平方。
```

---

## 4. 这说明什么

可以说：

```text
A_p,B_p 平方的假阳性不是纯随机。
至少这个样本来自同 squareclass 伪装。
```

不能说：

```text
所有假阳性都一定是四项同 squareclass。
这个观察已经证明了 R_lambda theorem。
```

普通话说：

```text
这是一个很好的代数线索，
不是结论。
```

---

## 5. 下一步证明入口

现在 `R_lambda` 主线可以换一种问法：

```text
如果四个 member squareclasses 全部等于 1，
再加上 closure 条件，
是否强迫 p=lambda？
```

或者更细：

```text
如果 A_p,B_p 是平方，
它们是否只允许两种情况？

1. squareclass 全为 1，是真 R_lambda 点；
2. squareclass 全为同一个非 1，是假点。
```

如果第 2 种可以参数化，就可能继续找：

```text
局部模障碍
平方剩余障碍
递降结构
```

普通话总结：

```text
我们现在看到的坑不是“乘积条件太弱”这么笼统。
更具体地说：
乘积条件看不见共同 squareclass。
```

---

## 6. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_product_square_conditions_do_not_imply_membership -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q --ignore=tests/test_parallel.py
uv run pytest tests/test_parallel.py -q
uv run pytest -q
```

结果：

```text
1 passed
30 passed
378 passed
16 passed, 2 warnings
394 passed, 2 warnings
```

备注：

```text
第一次 full pytest 出现一次偶发卡住。
终止后分段测试通过，
重跑 full pytest 也通过。
```
