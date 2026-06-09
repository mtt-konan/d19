# wl166 — `R_lambda` pairwise squareclass pattern

日期：2026-06-09

## 1. 本轮修正

wl165 看到一个假阳性样本：

```text
member_squareclasses = (29, 29, 29, 29)
```

这说明：

```text
四个单项全都坏在同一个 squareclass 上，
所以 A_p,B_p 会伪装成平方。
```

但这不是最一般的说法。

本轮小扫描发现，更稳的结构是：

```text
(r^2+1) 和 (s^2+1) 同 squareclass；
(r^2+lambda^2) 和 (s^2+lambda^2) 同 squareclass。
```

普通话说：

```text
不是四个都必须穿同一件外衣；
而是前一对穿同一件，后一对穿同一件。
这样两对相乘都会变成平方。
```

---

## 2. 新字段

`closure_product_square_conditions(...)` 新增：

```text
member_squareclasses_pairwise_equal
```

它检查：

```text
member_squareclasses[0] == member_squareclasses[1]
member_squareclasses[2] == member_squareclasses[3]
```

也就是：

```text
r^2+1        与 s^2+1        同 squareclass
r^2+lambda^2 与 s^2+lambda^2 同 squareclass
```

保留旧字段：

```text
member_squareclasses_all_equal
member_squareclasses_all_trivial
```

它们分别表示：

```text
四项全同 squareclass
四项全是 squareclass 1
```

---

## 3. 两种假阳性模式

### 模式 A：四项全同

样本：

```text
lambda = 535/161
r = 14/23
s = 26/7
```

结果：

```text
member_squareclasses = (29, 29, 29, 29)
member_squareclasses_pairwise_equal = True
member_squareclasses_all_equal = True
member_squareclasses_all_trivial = False
```

普通话说：

```text
四项都差同一个 29。
所以 A_p 和 B_p 都看起来是平方。
但没有一个单项真是平方。
```

### 模式 B：两对同类

样本：

```text
lambda = 2
T = 3
p = 9/4
r = s = 3/2
```

结果：

```text
member_squareclasses = (13, 13, 1, 1)
member_squareclasses_pairwise_equal = True
member_squareclasses_all_equal = False
member_squareclasses_all_trivial = False
```

普通话说：

```text
第一对不是平方，但同类；
第二对是真的平方。
所以 A_p,B_p 也都能过。
但这仍然不是真 R_lambda member pair。
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

结果：

```text
(true_member_pair, pairwise_equal, all_equal, all_trivial)

(False, True, False, False) 210
(False, True, True,  False) 60
```

可以说：

```text
这个有限池里的 product-square 假点全部满足 pairwise squareclass equal。
```

不能说：

```text
已经证明所有假点都满足这个模式。
有限扫描等于定理。
```

---

## 5. 为什么这更接近证明

`A_p` 是：

```text
(r^2+1)(s^2+1)
```

`B_p` 是：

```text
(r^2+lambda^2)(s^2+lambda^2)
```

所以：

```text
A_p 是平方
```

真正看到的是：

```text
r^2+1 与 s^2+1 的 squareclass 相乘为 1
```

对正有理数来说，这等价于：

```text
r^2+1 与 s^2+1 同 squareclass
```

同理：

```text
B_p 是平方
```

看到的是：

```text
r^2+lambda^2 与 s^2+lambda^2 同 squareclass
```

普通话说：

```text
乘积平方不是在告诉我们“两个都平方”。
它只告诉我们“两边坏得一样”。
```

---

## 6. 下一步

后面证明可以换成这个问题：

```text
在 closure 条件下，
如果两对 squareclass 都相等，
什么时候能进一步推出它们都等于 1？
```

或者：

```text
如果它们不等于 1，
能不能参数化这些共同 squareclass 假点，
再用模条件或递降排掉？
```

这比直接盯着 `A_p,B_p` 更有用。

普通话总结：

```text
R_lambda 主线往前挪了一小步：
我们把“乘积平方”翻译成了“成对 squareclass 相同”。
真正要证明的是：
成对相同什么时候会被迫变成成对都是 1。
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
