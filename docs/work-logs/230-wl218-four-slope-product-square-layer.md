# wl230 — wl218 four-slope product-square layer

日期：2026-06-22

## 1. 本轮目标

继续推进 `sum=A+B` 分支：

```text
r,s in R_lambda
r+s=lambda+1
=> rs=lambda
```

用户原始路线希望使用 product identity：

```text
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)
```

并把真成员平方条件翻译到 `A_p,B_p` 和单项平方上。

这轮专门看一个更贴近四斜率模型的弱层：

```text
x = r/lambda
y = s/lambda
lambda = 1/(x+y-1)

x,y 是勾股斜率
r=lambda*x
s=lambda*y
```

在这个模型里：

```text
A_p square
```

等价于：

```text
r^2+1 和 s^2+1 的 squareclass 相同
```

普通话说：

```text
先把 lambda-side 两只鞋确认是合脚的。
再问 unit-side 两只鞋是不是“坏得一样”。
如果坏得一样，而且又不是中线，那才是 product identity 路线真正危险的地方。
```

---

## 2. 新诊断 helper

新增：

```text
SumAbFourSlopeSquareclassSummary
sum_ab_four_slope_squareclass_summary(max_m=...)
```

它枚举 bounded Euclid 斜率池：

```text
x,y 是勾股斜率
x+y>1
lambda=1/(x+y-1)
r=lambda*x
s=lambda*y
```

然后统计：

```text
equal_unit_squareclass_pairs:
  r^2+1 和 s^2+1 squareclass 相等

centerline_equal_unit_squareclass_pairs:
  上述弱命中里 x=y 的数量

noncenter_equal_unit_squareclass_pairs:
  上述弱命中里 x!=y 的数量

true_four_pass_pairs:
  r^2+1 与 s^2+1 都真平方的数量
```

这只是诊断 helper，不是证明。

---

## 3. 小范围结果

运行：

```text
sum_ab_four_slope_squareclass_summary(max_m=8)
sum_ab_four_slope_squareclass_summary(max_m=20)
sum_ab_four_slope_squareclass_summary(max_m=24)
sum_ab_four_slope_squareclass_summary(max_m=28)
```

结果摘要：

| max_m | slopes | equal unit squareclass | centerline | noncenter | true four-pass |
|---:|---:|---:|---:|---:|---:|
| 8  | 30  | 21  | 21  | 0 | 0 |
| 20 | 172 | 119 | 119 | 0 | 0 |
| 24 | 242 | 167 | 167 | 0 | 0 |
| 28 | 328 | 227 | 227 | 0 | 0 |

普通话说：

```text
小范围里，弱 product-square 命中全是 x=y 中线。
非中线没有留下“坏得一样”的 unit-side 假点。
真四通过当然也没有出现。
```

---

## 4. 和旧 guard 例子的关系

wl224 的 guard 例子：

```text
lambda = 535/161
r = 14/23
s = 26/7
```

有：

```text
unit squareclasses   = (29,29)
lambda squareclasses = (29,29)
```

所以它通过了 product-square 弱层。

但在四斜率坐标里：

```text
x = r/lambda = 98/535
y = s/lambda = 598/535
```

并且：

```text
x^2+1 和 y^2+1 的 squareclass 也是 29
```

也就是说：

```text
x,y 不是勾股斜率。
```

普通话说：

```text
这个 guard 例子确实提醒我们 A_p,B_p 太弱。
但它不是四斜率模型里的危险残留，因为 lambda-side 已经不是真通过。
```

因此后续 valuation 路线应区分两件事：

```text
1. 纯 product ledger 的假阳性。
2. 已保留 x,y 两个 lambda-side 真平方后的假阳性。
```

第二类才是 `sum=A+B` 真证明要打的弱层。

---

## 5. 新的候选引理

小范围结果建议把用户的第 3 步改成更强、更准确的引理：

```text
Let x,y be positive Pythagorean leg ratios with x+y>1.
Set lambda=1/(x+y-1), r=lambda*x, s=lambda*y.

If r^2+1 and s^2+1 have the same rational squareclass,
then x=y.
```

然后：

```text
x=y
```

就是 centerline，已由 Yang Ji 关闭。

如果这个引理成立，则更强于只证明真四通过不存在：

```text
true four-pass
=> equal unit squareclass
=> x=y
=> centerline contradiction
```

普通话说：

```text
我们可以不直接追四个都平方。
先证明只要 unit-side 两个坏得一样，就已经被迫站到中线上。
中线已经关掉，所以真闭合也关掉。
```

---

## 6. 这和 `P!=Q` 的关系

在 same-orientation 语言里：

```text
x=y
```

对应：

```text
P=Q
```

wl229 已经说明 `P=Q` 分支归到 centerline。

所以新引理等价于把剩余分支写成：

```text
P!=Q
=> unit-side squareclasses cannot be equal
```

这正好贴合用户想要的 valuation 路线：

```text
证明非退化分支里，某个 squareclass / valuation 必须不匹配。
```

---

## 7. 当前不能说什么

不能说：

```text
四斜率 product-square 引理已证明。
sum=A+B 已证明。
倒数定理已证明。
```

因为目前只有有界诊断。

可以安全说：

```text
四斜率模型下，小范围 weak product-square 命中全是 centerline。
旧 guard 例子不属于四斜率真 lambda-side 层。
下一步应尝试证明 noncenter equal-squareclass 不可能。
```

---

## 8. 验证

新增测试：

```text
test_sum_ab_four_slope_squareclass_summary_separates_centerline_artifacts
```

已跑：

```text
uv run pytest tests/test_rational_ratio.py -q
```

结果：

```text
54 passed
```
