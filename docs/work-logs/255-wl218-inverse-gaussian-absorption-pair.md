# wl255 — wl218 inverse Gaussian absorption pair

日期：2026-06-22

## 1. 本轮目标

接 wl254。

wl254 的有限摘要说明：

```text
bounded root-grid residual 的已知例子是 Gaussian centerline shadow。
```

本轮把这个 shadow 现象反过来写成生成公式。

普通话说：

```text
上一轮是：看到假根以后，把坏因子吸掉，得到同一个 z。
这一轮是反过来：从同一个 z 和同一个高斯因子出发，
能不能直接生成那两个假根？
```

---

## 2. 反向公式

正向 absorption 使用：

```text
z_plus  = (a*r + b) / (a - b*r)
z_minus = (a*r - b) / (a + b*r)
```

其中：

```text
d = a^2 + b^2
```

反解为：

```text
r_plus_inverse  = (a*z - b) / (b*z + a)
r_minus_inverse = (a*z + b) / (a - b*z)
```

普通话说：

```text
plus/minus 是两种高斯共轭分支。
给定吸收后的真斜率 z，
选择不同分支，就能生成原来的假斜率。
```

---

## 3. guard 复现

取：

```text
z = 4/3
d = 29 = 5^2 + 2^2
a = 5
b = 2
```

使用：

```text
r = plus_inverse(z)
s = minus_inverse(z)
```

得到：

```text
r = (5z-2)/(2z+5) = 14/23
s = (5z+2)/(5-2z) = 26/7
```

于是：

```text
lambda = r+s-1 = 535/161
p = rs = 52/23
```

并且 product ledger 仍分类为：

```text
product_square_bucket = residual
member_squareclass_pair = (29,29)
```

普通话说：

```text
guard 假点不是从空气里冒出来的。
它可以由一个中线斜率 z=4/3，
经过同一个高斯因子的两个相反分支生成。
```

---

## 4. 新 helper

新增 dataclass：

```text
InverseGaussianAbsorptionPair
```

新增 helper：

```text
inverse_gaussian_absorption_pair(
    absorbed=z,
    squareclass=d,
    r_branch="plus",
    s_branch="minus",
)
```

它返回：

```text
r
s
lambda_ratio = r+s-1
product = rs
condition = closure_product_square_conditions(lambda, lambda+1, product, sum=A+B)
```

新增测试：

```text
test_inverse_gaussian_absorption_pair_reconstructs_guard_residual
```

---

## 5. 对证明路线的影响

这仍不是完整证明。

但它把 only-1-mod-4 residual 的疑似结构变成了可计算参数：

```text
z, d=a^2+b^2, branch_r, branch_s
```

下一步可以直接推导：

```text
lambda(z,a,b)
p(z,a,b)
lambda^2 - p^2
A_p
B_p
```

普通话说：

```text
现在不用再猜 guard 的来源。
它就是“同一个 z + 同一个 d + 两个相反分支”的产物。
接下来要证明的是：
这种产物如果想变成真 R_lambda 成员，会被中线定理或倒数结构排掉。
```

---

## 6. 下一步

下一步应写符号账本：

```text
inverse_gaussian_absorption_symbolic_terms(z,a,b, branches)
```

优先处理：

```text
(plus, minus)
```

因为 guard 就是这个分支。

要看：

```text
lambda^2-p^2
```

是否含有中心线因子，或是否能直接约化到已有 centerline quartic / squareclass-ratio 条件。

普通话说：

```text
我们已经把假点变成参数化公式。
下一步就是把这个公式代回倒数定理的核心恒等式，
看它到底卡在哪里。
```

---

## 7. 当前边界

可以安全说：

```text
1. guard residual 可由 inverse Gaussian absorption 精确生成；
2. 生成公式已可复跑；
3. only-1-mod-4 分支现在有明确参数入口。
```

不能说：

```text
所有 only-1-mod-4 residual 都已参数化。
sum=A+B 已证明。
倒数定理已证明。
```
