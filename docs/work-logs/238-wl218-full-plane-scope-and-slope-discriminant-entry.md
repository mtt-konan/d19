# wl238 — wl218 full-plane scope and slope discriminant entry

日期：2026-06-22

## 1. 本轮修正

用户修正要求：

```text
可以在全平面，不一定是只在正方形里。
```

普通话说：

```text
最终要证明的不是“正方形里面那条闭合线”。
最终要证明的是：在整个平面里，只要 r,s 是真 R_lambda 成员，
并且满足任意一种闭合关系，就只能是倒数对 rs=lambda。
```

因此全平面闭合条件必须写成：

```text
{r+s, |r-s|} intersect {lambda+1, |lambda-1|} nonempty.
```

也就是四个分支：

```text
1. r+s   = lambda+1
2. r+s   = |lambda-1|
3. |r-s| = lambda+1
4. |r-s| = |lambda-1|
```

当前 `sum=A+B`：

```text
r+s = lambda+1
```

只是第一分支，不是整个倒数定理。

---

## 2. 第一分支的当前最短模型

继续只看第一分支。

令：

```text
x = r/lambda
y = s/lambda
D = x+y-1
lambda = 1/D
```

则：

```text
r = x/D
s = y/D
```

真成员条件可写成四个平方：

```text
x^2+1 square
y^2+1 square
x^2+D^2 square
y^2+D^2 square
```

普通话说：

```text
这是一个小矩形问题：
横向长度取 x 或 y，纵向长度取 1 或 D。
四条斜边都必须是有理数。
```

因为：

```text
D = x+y-1,
```

所以这个矩形不是任意矩形；高度被两条横向长度绑定住。

---

## 3. 二次型版本

已有：

```text
r^2+1 = P / (x+y-1)^2
s^2+1 = Q / (x+y-1)^2
```

其中：

```text
P = 2x^2 + 2xy - 2x + y^2 - 2y + 1
Q = x^2 + 2xy - 2x + 2y^2 - 2y + 1.
```

也就是：

```text
P = x^2 + D^2
Q = y^2 + D^2.
```

所以一个足够强、但仍未证明的候选引理是：

```text
x^2+1 square
y^2+1 square
P/Q square
=> x=y.
```

这里 `P/Q square` 只是弱化条件；真正成员还要求 `P` 和 `Q` 各自都是平方。

普通话说：

```text
如果连“P 和 Q 只差一个平方倍数”都只能发生在 x=y，
那真正的四平方条件当然也只能发生在 x=y。
```

---

## 4. 新判别式入口

把：

```text
P = K Q
```

看成关于 `y` 的二次方程，其中 `K` 表示 `P/Q`。

得到：

```text
(1-2K)y^2 + (-2Kx+2K+2x-2)y
  + (-Kx^2+2Kx-K+2x^2-2x+1) = 0.
```

它关于 `y` 的判别式是：

```text
-4 * I(x,K)
```

其中：

```text
I(x,K)
= K^2x^2 - 2K^2x + K^2
  - 3Kx^2 + 2Kx - K
  + x^2.
```

再把 `I(x,K)` 看成关于 `K` 的二次式，它的判别式为：

```text
(x^2+1)(5x^2-4x+1).
```

由于第一项 `x^2+1` 已经是平方，新的曲线入口是：

```text
5x^2 - 4x + 1.
```

普通话说：

```text
固定一个合格的 x 后，非中线的 y 若要从 P=KQ 里冒出来，
判别式会把我们带到一个新的二次因子 5x^2-4x+1。
这不是最终证明，但它是下一条很小的曲线入口。
```

---

## 5. 不能过度解读

这个入口不能直接说：

```text
5x^2-4x+1 必须是平方。
```

原因是：

```text
K=1
```

本身就是一个特殊点，对应 `P=Q` / centerline。

更准确地说：

```text
(x^2+1)(5x^2-4x+1)
```

控制的是 `I(x,K)` 这条外层二次曲线关于 `K` 的可参数化形状。
真正的第一分支仍然还要同时吃掉：

```text
K 是有理平方，
y 是有理数，
y^2+1 是有理平方，
P 和 Q 各自是有理平方。
```

普通话说：

```text
它像是一张地图上新出现的窄桥，
但还不是已经走完了桥。
```

---

## 6. PARI 诊断

参数化：

```text
x = (1-t^2)/(2t)
```

后：

```text
5x^2-4x+1
= (5t^4+8t^3-6t^2-8t+5)/(4t^2).
```

于是新入口对应四次曲线：

```text
Y^2 = 5t^4+8t^3-6t^2-8t+5.
```

本轮 PARI 诊断：

```text
ellfromeqn model = [0, -6, 0, -164, 1240]
ellrank         = [0, 0, 0, []]
elltors         = [4, [4], [[6, 16]]]
hyperellratpoints height<=100:
  [[-1, 2], [-1, -2], [1, 2], [1, -2]]
```

这说明：

```text
雅可比椭圆曲线 rank 0；
小高度有理点只看到 t=±1 的边界点。
```

但这仍不是正式证明。

缺的步骤是：

```text
把椭圆曲线 torsion 点显式拉回四次曲线，
证明四次曲线的有理点只有这些边界点。
```

---

## 7. 代码入口

新增 helper：

```text
sum_ab_slope_ratio_y_discriminant_ledger(x, K)
```

它记录：

```text
1. P=KQ 作为 y 二次式的三个系数；
2. y 判别式；
3. I(x,K)；
4. I 作为 K 二次式的判别式；
5. x^2+1；
6. 新因子 5x^2-4x+1。
```

新增测试：

```text
test_sum_ab_slope_ratio_y_discriminant_ledger_records_new_curve_factor
```

---

## 8. 当前证明状态

可以安全说：

```text
1. 全平面目标已修正为四分支；
2. sum=A+B 只是第一分支；
3. 第一分支的剩余硬点仍是 x,y 二次型引理；
4. 本轮新增了一个可复查的判别式入口；
5. PARI 强烈提示新四次曲线是 rank 0 / 只有边界点。
```

不能说：

```text
sum=A+B 已证明。
四个全平面分支已证明。
倒数定理已证明。
有限扫描或 PARI 诊断已经替代了证明。
```

---

## 9. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py -q
PYTHONPATH=src uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
git diff --check
```

结果：

```text
60 passed
All checks passed
git diff --check passed
```

---

## 10. 下一步

最具体的下一步：

```text
1. 对 Y^2 = 5t^4+8t^3-6t^2-8t+5 做显式 birational pullback；
2. 确认 torsion 点只拉回 t=±1；
3. 若成立，抽成引理：
   x^2+1 square 且 5x^2-4x+1 square
   => x=0 或边界/退化；
4. 再检查这个引理是否足够接回 K square 和 y recovery 条件。
```

普通话说：

```text
下一步不是继续大扫。
下一步是把这条 rank 0 曲线从“诊断”升级成“可引用的小引理”。
```
