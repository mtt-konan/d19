# wl242 — wl218 K-discriminant completion

日期：2026-06-22

## 1. 本轮目标

回到 `sum=A+B` 第一分支的主硬点：

```text
x^2+1 square
y^2+1 square
P/Q square
=> x=y
```

其中：

```text
P = 2x^2 + 2xy - 2x + y^2 - 2y + 1
Q = x^2 + 2xy - 2x + 2y^2 - 2y + 1.
```

普通话说：

```text
上一轮把一个新曲线支路归约到 centerline/Yang Ji。
这轮回到一般的 K=P/Q 情形，看剩余判别式有没有更深结构。
```

---

## 2. 代入 x 的勾股参数

令：

```text
x = (1-a^2)/(2a).
```

写：

```text
P = k^2 Q
```

并把 `y` 也用勾股参数代入时，关于第二个参数的判别式除了平方因子外，剩下：

```text
R(a,K)
```

其中：

```text
K = k^2.
```

把 `R(a,K)` 看成关于 `K` 的二次式，有：

```text
R(a,K)
= A(a)K^2 + B(a)K + C(a)
```

其中：

```text
A(a) = a^4 + 8a^3 + 18a^2 - 8a + 1
B(a) = -4(a^2+2a-1)(a^2+4a-1)
C(a) = 4(a^2+2a-1)^2.
```

这里：

```text
A(a)
```

正是 centerline quartic：

```text
Q_center(a)=a^4+8a^3+18a^2-8a+1.
```

普通话说：

```text
一般 K 情形并没有离开中线四次式。
它的最高项系数就是 centerline quartic。
```

---

## 3. 配方恒等式

对 `R(a,K)` 完全平方，得到：

```text
4 A(a) R(a,K)
= [2A(a)K - 4(a^2+2a-1)(a^2+4a-1)]^2
  + [8a(a^2+2a-1)]^2.
```

也就是说：

```text
4 * centerline_quartic * remaining_quartic
```

被写成两个有理平方之和。

普通话说：

```text
如果 R(a,K) 也要成为平方，
它不是孤立发生的；
它会把 centerline quartic 一起拖进一个“两平方和”结构。
```

---

## 4. 当前意义

这个恒等式还没有直接证明：

```text
P/Q square => x=y.
```

但它给出一个新的主线入口：

```text
一般 K 的剩余判别式与 centerline quartic 强绑定。
```

特别是：

```text
disc_K R = -64 a^2(a^2+2a-1)^2.
```

所以只要：

```text
a != 0
a^2+2a-1 != 0
```

`R(a,K)` 作为实二次式没有两个实根，并且配方余项严格为正。

普通话说：

```text
这不是最终矛盾，
但说明非中线真解如果存在，必须穿过一个和中线 quartic 纠缠的窄门。
```

---

## 5. 代码入口

新增 helper：

```text
sum_ab_k_discriminant_quartic_completion(a, K)
```

记录：

```text
centerline_quartic = A(a)
remaining_quartic = R(a,K)
linear_square_term
positive_square_term
4*A*R = linear_square_term^2 + positive_square_term^2
```

新增测试：

```text
test_sum_ab_k_discriminant_quartic_completion_links_centerline
```

---

## 6. 当前证明边界

可以安全说：

```text
1. 一般 K 剩余判别式的最高项就是 centerline quartic；
2. R(a,K) 有一个严格的配方恒等式；
3. 这给出下一步 descent / norm obstruction 的入口。
```

不能说：

```text
一般 K square 情形已关闭。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 7. 下一步

下一步可以尝试：

```text
1. 假设 R(a,K)=square，把配方恒等式转成 norm equation；
2. 结合 A(a) 的 centerline/Yang Ji 排除；
3. 或对 4*A*R = S^2+T^2 做 prime 3 mod 4 的 valuation 分析。
```

普通话说：

```text
这一步把用户最初想走的 valuation 路线重新接回来了：
现在不是盲看 A_p,B_p，
而是看一个明确的“两平方和 + centerline quartic”结构里，
哪些 3 mod 4 素数必须成偶次。
```
