# wl118 — `R_λ` translation theorem 的 `p=rs` worksheet

日期：2026-06-09

承接 wl117 的 P0 主线：

```text
若 r,s∈R_λ 且满足 full-plane closure，
是否必须有 s = λ/r？
```

本轮不声称证明这条命题。只做第一步：

```text
把 r+s=T 或 |r-s|=T 的两个 R_λ 条件，
压成 p=rs 语言，
看 p=λ 目标到底卡在哪里。
```

---

## 1. 模型

归一化：

```text
λ = A/B ∈ Q_{>0}
r = N_1/B
s = N_2/B
```

定义：

```text
R_λ = { r∈Q_{>0} :
        r^2 + 1   是有理平方，
        r^2 + λ^2 是有理平方 }
```

full-plane closure 有四类：

```text
r+s   = λ+1
r+s   = |λ-1|
|r-s| = λ+1
|r-s| = |λ-1|
```

统一记：

```text
T = closure target
p = rs
```

目标是看这些条件是否能逼出：

```text
p = λ
```

因为：

```text
rs = λ
=> s = λ/r
```

这正是 reciprocal orbit。

---

## 2. Sum closure：`r+s=T`

若：

```text
r+s = T
p = rs
```

则：

```text
r^2+s^2 = T^2 - 2p
```

因为 `r,s∈R_λ`，四个数都必须是有理平方：

```text
r^2+1
s^2+1
r^2+λ^2
s^2+λ^2
```

把成对乘积写成 `T,p,λ`：

```text
(r^2+1)(s^2+1)
= p^2 + (r^2+s^2) + 1
= p^2 - 2p + T^2 + 1
```

记：

```text
A_p = p^2 - 2p + T^2 + 1
```

同理：

```text
(r^2+λ^2)(s^2+λ^2)
= p^2 + λ^2(r^2+s^2) + λ^4
= p^2 - 2λ^2p + λ^2T^2 + λ^4
```

记：

```text
B_p = p^2 - 2λ^2p + λ^2T^2 + λ^4
```

于是有恒等式：

```text
B_p - λ^2 A_p = (λ^2 - 1)(λ^2 - p^2)
```

这条式子很漂亮，但还不是证明。

普通话说：

```text
如果四个单项都是平方，
那 A_p 和 B_p 的确是平方。
但 A_p、B_p 是平方，
不反过来保证四个单项分别是平方。
```

所以现在的必要条件是：

```text
A_p 是有理平方
B_p 是有理平方
```

但真实条件更强：

```text
r^2+1, s^2+1, r^2+λ^2, s^2+λ^2
各自都是有理平方。
```

---

## 3. Difference closure：`|r-s|=T`

若先取有序版本：

```text
s-r = T
p = rs
```

则：

```text
r^2+s^2 = T^2 + 2p
```

于是：

```text
A_p = p^2 + 2p + T^2 + 1
B_p = p^2 + 2λ^2p + λ^2T^2 + λ^4
```

同样有：

```text
B_p - λ^2 A_p = (λ^2 - 1)(λ^2 - p^2)
```

所以 sum 和 difference 的统一形式是：

```text
A_p = p^2 + ε·2p + T^2 + 1
B_p = p^2 + ε·2λ^2p + λ^2T^2 + λ^4
```

其中：

```text
ε = -1  对应 r+s=T
ε = +1  对应 |r-s|=T
```

本轮把这个统一公式加入代码：

```text
closure_product_identity_terms(lambda_ratio, target, product, relation)
```

它不会证明无解，只保证 worksheet 里的 `+2p / -2p` 不会手算错。

---

## 4. 为什么 `p=λ` 是自然目标

若：

```text
p = rs = λ
```

则：

```text
s = λ/r
```

这表示 `r,s` 在同一个 reciprocal orbit。

wl115-wl116 已经把 same-orbit closure 的危险点拆开：

```text
有些 closure 二次方程确实有有理根；
但这些根未必是真 R_λ 成员。
```

所以整体路线是：

```text
Step 1: closure + R_λ 条件 => p=λ
Step 2: p=λ => reciprocal orbit
Step 3: reciprocal orbit closure 被排除
```

Step 1 还没证明。

---

## 5. 当前卡点

从 `A_p,B_p` 只能得到两个乘积是平方：

```text
(r^2+1)(s^2+1) 是平方
(r^2+λ^2)(s^2+λ^2) 是平方
```

但这不等于：

```text
r^2+1 是平方
s^2+1 是平方
r^2+λ^2 是平方
s^2+λ^2 是平方
```

举个普通例子：

```text
2 × 8 = 16 是平方，
但 2 和 8 都不是平方。
```

因此不能这样证明：

```text
A_p、B_p 是平方
=> p=λ
=> 完成
```

这会把必要条件当充分条件。

真正需要的是把 `r,s` 是同一个二次方程的两个根也用上：

```text
X^2 - T X + p = 0       sum closure, roots are r,s
X^2 + T X - p = 0       difference closure, roots are r,-s if s-r=T
```

更具体地说：

```text
r,s 必须是有理数
=> 判别式必须是有理平方。
```

sum closure:

```text
D = T^2 - 4p
```

difference closure:

```text
D = T^2 + 4p
```

所以下一步应同时使用三类条件：

```text
1. A_p 是平方
2. B_p 是平方
3. T^2 ± 4p 是平方
```

再加上真实 membership 的分裂条件。

---

## 6. 下一步最值得攻的子命题

先不要处理四个 closure target。

优先处理最自然的一支：

```text
sum=A+B:
T = λ + 1
r+s = λ + 1
```

目标子命题：

```text
若 λ∈Q_{>0}, r,s∈R_λ, r+s=λ+1，
则 rs=λ。
```

把它翻译成 `p`：

```text
T = λ+1
A_p = p^2 - 2p + (λ+1)^2 + 1
B_p = p^2 - 2λ^2p + λ^2(λ+1)^2 + λ^4
D   = (λ+1)^2 - 4p
```

已知：

```text
A_p, B_p, D 都是有理平方。
```

想证：

```text
p=λ。
```

如果 `p=λ`，则：

```text
D = (λ+1)^2 - 4λ = (λ-1)^2
```

这正好对应根：

```text
r,s = 1, λ
```

但这两个根通常不是真 `R_λ` 点，因为会碰到 `2` 或 `2λ^2` 的平方问题。

这说明一个更强的可能结论是：

```text
sum=A+B 分支根本没有真 R_λ 解。
```

而不是只得到 `p=λ`。

---

## 7. 本轮代码变更

新增：

```text
src/rational_distance/concordant/rational_ratio.py
  closure_product_identity_terms(...)
```

新增测试：

```text
tests/test_rational_ratio.py
  test_closure_product_identity_uses_difference_sign
```

测试固定两件事：

```text
sum closure 使用 -2p；
difference closure 使用 +2p；
两者都有同一个差值恒等式：
B_p - λ^2 A_p = (λ^2 - 1)(λ^2 - p^2)
```

---

## 8. 下一步

建议下一轮做一个更小的 proof note：

```text
docs/proofs/rational-ratio-sum-ab-p-target.md
```

只攻：

```text
T = λ+1
A_p, B_p, D 是平方
```

看能不能推出：

```text
p=λ
```

如果推不出，就尝试找反例：

```text
λ,p∈Q
A_p, B_p, D 都是平方
p≠λ
```

注意：就算找到这样的 `λ,p`，也不一定是原问题反例，因为还要把 `r,s` 拆回真实 `R_λ` 成员。

这正好能测出 `p` 模型到底强到哪一步。
