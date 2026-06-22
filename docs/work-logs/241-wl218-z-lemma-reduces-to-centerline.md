# wl241 — wl218 z lemma reduces to centerline

日期：2026-06-22

## 1. 本轮目标

接 wl240，当前最短子引理是：

```text
z^2 + 4          是有理平方
5z^2 + 8z + 4   是有理平方
=> z = 0.
```

普通话说：

```text
如果这个 z 引理成立，那么 wl238 的新四次曲线只剩 t=±1 边界点。
这轮要看它是不是一个新问题，还是能转回已经关闭的中心线问题。
```

结论：

```text
z 引理可以归约到 centerline quartic。
如果允许引用 Yang Ji 中线定理，则 z 引理关闭。
如果要求仓库内完全自足代数证明，则它继承 centerline quartic 的
birational pullback 缺口。
```

---

## 2. 参数化第一条平方

从：

```text
z^2 + 4 = square
```

取基点：

```text
(z,w)=(0,2)
```

用斜率参数 `m` 参数化。

非退化分支为：

```text
z = -4m / ((m-1)(m+1)).
```

其中：

```text
m = 0  =>  z = 0.
```

`m=±1` 是参数化分母退化点，不给有限有理 `z`。

---

## 3. 第二条平方变成 centerline quartic

代入第二条：

```text
5z^2 + 8z + 4 = square.
```

得到：

```text
5z^2 + 8z + 4
= 4 R(m) / ((m-1)^2(m+1)^2)
```

其中：

```text
R(m) = m^4 - 8m^3 + 18m^2 + 8m + 1.
```

所以第二条平方等价于：

```text
R(m) 是有理平方.
```

而 centerline quartic 是：

```text
Q(t) = t^4 + 8t^3 + 18t^2 - 8t + 1.
```

直接代入：

```text
R(m) = Q(-m).
```

普通话说：

```text
z 引理不是新曲线。
它就是中心线 quartic 换了一个变量符号。
```

---

## 4. 如何得到 z=0

wl226 / wl202 已经把中心线分支接到 Yang Ji：

```text
Yang Ji Theorem 2 + Remark 1
```

在 d19 的 `R_lambda` 语言里，它排除 centerline 的非退化有理点。
本地 quartic 账本把这个中心线写成：

```text
Y^2 = Q(t).
```

可引用结论是：

```text
Q(t) 是有理平方
=> t = 0 这个退化点
```

在这里：

```text
R(m)=Q(-m)
```

所以：

```text
R(m) square
=> -m = 0
=> m = 0
=> z = 0.
```

普通话说：

```text
只要接受中线已由 Yang Ji 关闭，
那 z 引理也跟着关掉。
```

---

## 5. 和 wl218 第一分支的关系

这一步能关闭的是 wl238 里出现的“新曲线因子”：

```text
x^2+1 square
5x^2-4x+1 square
```

把：

```text
x = (1-t^2)/(2t)
```

代入后得到的新四次曲线，通过：

```text
z=t-1/t
```

再归约到 centerline quartic。

所以现在可以把这条支线标成：

```text
new-curve obstruction reduces to centerline/Yang Ji.
```

但这仍不等于：

```text
sum=A+B 第一分支已关闭。
```

原因是 wl238 的新曲线因子只是 `P=KQ` 外层判别式的一条入口。
真正剩余条件还有：

```text
K 是平方，
y 是有理数，
y^2+1 是平方，
P 和 Q 各自是平方。
```

普通话说：

```text
我们关掉了一条新冒出来的小支路。
主干的 same-orientation 非中线分支还没完全关掉。
```

---

## 6. 代码入口

新增 helper：

```text
sum_ab_z_lemma_centerline_bridge(m)
```

记录：

```text
z = -4m / ((m-1)(m+1))
R(m)
Q(-m)
5z^2+8z+4 = 4R(m)/((m-1)^2(m+1)^2)
```

新增测试：

```text
test_sum_ab_z_lemma_centerline_bridge_matches_quartic
```

---

## 7. 当前证明边界

可以安全说：

```text
1. z 引理归约到 centerline quartic；
2. 引用 Yang Ji 中线定理时，z 引理关闭；
3. 这关闭 wl238 的新曲线支路；
4. sum=A+B 的完整第一分支仍未关闭。
```

不能说：

```text
仓库已经有 centerline quartic 的完全自足代数证明。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 8. 下一步

回到主分支：

```text
x^2+1 square
y^2+1 square
P/Q square
=> x=y
```

现在可以记录一个新排除规则：

```text
若外层判别式进一步要求
5x^2-4x+1 square，
则这条路线归约到 centerline/Yang Ji，
不会给出非中线真解。
```

下一步应继续处理：

```text
P=KQ 的一般 K square 情形，
尤其是 K 不是通过该新曲线因子退化出来的情况。
```
