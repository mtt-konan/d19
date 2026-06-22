# wl233 — wl218 `z` parameterization self-similarity

日期：2026-06-22

## 1. 本轮目标

继续推进 `sum=A+B` 分支的 squareclass-ratio 引理。

上一轮 wl232 得到：

```text
z = u - 1/u
```

把：

```text
A/B 是有理平方
```

降成：

```text
Phi(t,z) 是有理平方
```

但 `z` 不是任意有理数；它必须来自有理 `u`，也就是：

```text
z^2 + 4 是有理平方。
```

本轮检查：

```text
把 z^2+4 参数化后，Phi(t,z) 是否继续降维？
```

普通话说：

```text
我们想知道 z 这条路是不是继续往下走。
答案是：它会绕回原问题。
这不是坏事，但说明不能靠这一步直接证明。
```

---

## 2. 参数化 `z^2+4`

所有有理解可写成：

```text
z = a - 1/a
```

因为：

```text
z^2 + 4 = (a + 1/a)^2.
```

在本问题里：

```text
0<u<1
```

所以：

```text
z = u - 1/u < 0.
```

同一个 `z` 对应两根：

```text
a = u
a = -1/u.
```

若保持正参数，则取：

```text
a = u.
```

---

## 3. 自相似恒等式

wl232 中：

```text
Phi(t,z) = N(t,z) / D(t,z).
```

把：

```text
z = a - 1/a
```

代入后，得到：

```text
N(t,a-1/a) = A(t,a)
D(t,a-1/a) = B(t,a)
```

也就是说：

```text
Phi(t, a-1/a) = A(t,a) / B(t,a).
```

普通话说：

```text
z 参数化没有产生一个新问题。
它只是把变量 u 换名为 a，然后回到同一个 A/B。
```

这解释了为什么继续参数化 `z^2+4` 不会自动证明候选引理。

---

## 4. 中心线因子再次出现

代入 `a` 后仍有：

```text
A(t,a) - B(t,a)
  = (t-a)(t+a)(ta-1)(ta+1).
```

在正范围：

```text
0<t,a<1
```

只有：

```text
t=a
```

能让 `A=B`。

这就是中心线：

```text
u=t
=> x=y.
```

普通话说：

```text
完全相等时仍然马上落到中线。
但我们需要的是“相差一个平方倍数”，所以还差一层。
```

---

## 5. 有限反例搜索

本轮做了两个小搜索：

```text
1. 直接枚举 0<t,u<1, denominator <= 90:
   A/B square 且 t!=u
   结果：none

2. 直接枚举 t,h 后检查 A-h^2B 的小有理根:
   denominator(t), denominator(h) <= 20
   结果：none
```

这不是证明。

它只说明：

```text
候选引理仍然没有小反例。
```

---

## 6. 代码入口

新增 helper：

```text
sum_ab_squareclass_ratio_z_parameterization(t, parameter)
```

它记录：

```text
z = parameter - 1/parameter
reduced_ratio = Phi(t,z)
self_similar_ratio = A(t,parameter)/B(t,parameter)
centerline_factor = (t-a)(t+a)(ta-1)(ta+1)
```

测试：

```text
test_sum_ab_squareclass_ratio_z_parameterization_is_self_similar
```

这个测试的作用是防止后续误判：

```text
z 参数化不是新的独立降维；
它是原方程的自相似复现。
```

---

## 7. 当前证明边界

可以安全说：

```text
1. A/B square 的 z 降维有效；
2. 但 z^2+4 参数化后，问题回到同一形状；
3. 中心线因子一直是 (t-a)(t+a)(ta-1)(ta+1)；
4. 非中线平方比值仍未证明不可能。
```

不能说：

```text
sum=A+B 已证明。
squareclass-ratio 引理已证明。
z 参数化关闭了非中线分支。
```

---

## 8. 下一步

现在最合理的两条路线是：

```text
1. Descent:
   利用自相似结构，寻找一个规范量 M(t,u)，
   使得任何非中线 A/B square 解都会产生更小解。

2. Local symbol:
   回到 Gaussian integer / Hilbert-symbol 分配，
   证明非中线 squareclass equality 在 2 或 1 mod 4 素数处矛盾。
```

普通话说：

```text
变量替换已经把门摸清了。
下一步不是继续换变量，而是要找到“如果有反例，就能变成更小反例”的机制，
或者找到一个真正杀死非中线的局部符号。
```
