# wl239 — wl218 new curve local and cubic diagnostics

日期：2026-06-22

## 1. 本轮目标

接 wl238 的新曲线入口：

```text
Y^2 = 5t^4 + 8t^3 - 6t^2 - 8t + 5.
```

普通话说：

```text
上一轮发现：如果固定一个合格的 x，
外层判别式会冒出 5x^2-4x+1。
把 x 参数化以后，它变成这条四次曲线。
这轮目标是看它能不能直接升级成一个可引用的小证明。
```

结论先说：

```text
还没有升级成证明。
但得到了两个可复查的证据：
1. 一个从四次曲线到三次曲线的显式中间模型；
2. 一个 mod 3 局部筛：平方 residue 只允许 t ≡ ±1。
```

---

## 2. 四次曲线到三次曲线的显式中间模型

四次曲线：

```text
Y^2 = 5t^4 + 8t^3 - 6t^2 - 8t + 5
```

有有理点：

```text
(t,Y) = (1,2).
```

以这个点为基点，作代换：

```text
t = 1 + 1/u
Y = 2 + v/u^2.
```

直接代入并乘以 `u^4`，得到：

```text
v^2 + 4u^2 v - 24u^3 - 48u^2 - 28u - 5 = 0.
```

也就是：

```text
v^2 + 4u^2v = 24u^3 + 48u^2 + 28u + 5.
```

普通话说：

```text
四次曲线确实已经被压成一条三次曲线。
接下来只差把这条三次曲线规范化成 Weierstrass 形，
并把 torsion 点显式拉回原来的 t。
```

---

## 3. PARI 诊断复核

PARI 对原四次曲线给出的雅可比模型仍是：

```text
ellfromeqn model = [0, -6, 0, -164, 1240]
```

对应椭圆曲线：

```text
Y^2 = X^3 - 6X^2 - 164X + 1240.
```

诊断：

```text
ellrank = [0, 0, 0, []]
elltors = [4, [4], [[6, 16]]]
```

torsion 点循环：

```text
O
(6, 16)
(10, 0)
(6, -16)
O
```

`ellratpoints` 小高度复核：

```text
[[6, 16], [6, -16], [10, 0]]
```

普通话说：

```text
椭圆曲线这一侧看起来非常干净：
rank 0，只有 4 阶 torsion。
但我们还没有把这 4 个点完整拉回四次曲线。
```

因此仍不能写成正式证明。

---

## 4. mod 3 局部筛

把 `t=a/b` 齐次化：

```text
Y^2 = 5a^4 + 8a^3b - 6a^2b^2 - 8ab^3 + 5b^4.
```

在 `mod 3` 下枚举 primitive residue classes：

```text
primitive classes = 8
square classes    = 4
```

所有 square classes 都满足：

```text
a ≡ b mod 3
```

或：

```text
a ≡ -b mod 3.
```

也就是：

```text
t ≡ 1 或 -1 mod 3.
```

普通话说：

```text
如果这条四次曲线有有理点，
它在 mod 3 上必须贴着两个边界点 t=±1。
```

但这个筛还不是证明。

原因是：

```text
在这些活 residue class 里，曲线值通常仍是 1 mod 3，
不会强迫 a,b,Y 继续被 3 整除。
```

所以它不像一个直接的 3-adic 递降。

---

## 5. 代码入口

新增 helper：

```text
sum_ab_new_curve_residue_summary(modulus)
```

对新四次曲线的齐次式：

```text
5a^4 + 8a^3b - 6a^2b^2 - 8ab^3 + 5b^4
```

统计：

```text
primitive_classes
square_classes
boundary_square_classes
nonboundary_square_classes
boundary_examples
nonboundary_examples
```

新增测试：

```text
test_sum_ab_new_curve_mod3_residue_summary_only_leaves_boundary_classes
```

它固定了：

```text
modulus = 3
primitive_classes = 8
square_classes = 4
boundary_square_classes = 4
nonboundary_square_classes = 0
```

---

## 6. 当前证明边界

可以安全说：

```text
1. 新四次曲线有一个显式三次模型；
2. PARI 继续显示它的雅可比 rank 0、torsion order 4；
3. mod 3 局部筛只留下 t ≡ ±1 的 residue classes；
4. 这些都支持“只有边界点”的方向。
```

不能说：

```text
新四次曲线已证明只有 t=±1。
sum=A+B 第一分支已关闭。
倒数定理已证明。
```

---

## 7. 下一步

下一步应集中在：

```text
1. 把三次曲线
   v^2 + 4u^2v = 24u^3 + 48u^2 + 28u + 5
   规范化到 PARI 的 Weierstrass 模型；

2. 写出从 Weierstrass torsion 点回到 (t,Y) 的显式公式；

3. 验证 4 个 torsion 点只拉回：
   t = 1, Y = ±2
   t = -1, Y = ±2
   以及无穷远/基点边界。
```

普通话说：

```text
我们现在离“这条新曲线只有边界点”更近了，
但还差最后一段显式曲线字典。
```
