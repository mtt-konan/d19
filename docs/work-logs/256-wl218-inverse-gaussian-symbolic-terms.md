# wl256 — wl218 inverse Gaussian symbolic terms

日期：2026-06-22

## 1. 本轮目标

接 wl255。

wl255 已经说明 guard residual 可以由：

```text
z = 4/3
d = 29 = 5^2 + 2^2
r_branch = plus
s_branch = minus
```

反向生成。

本轮把这个例子提升成 `(plus, minus)` 分支的通式账本。

普通话说：

```text
上一轮知道 guard 从哪里来。
这一轮把“从哪里来”写成公式，
让 lambda、p=rs、A_p、B_p 都能直接从 z,a,b 算出来。
```

---

## 2. 通式

设：

```text
d = a^2 + b^2
Delta = a^2 - b^2 z^2
```

对 inverse Gaussian 的 `(plus, minus)` 分支：

```text
r = (a z - b) / (a + b z)
s = (a z + b) / (a - b z)
```

在 `sum=A+B` 分支中：

```text
lambda = r + s - 1
p = rs
```

展开得到：

```text
lambda = (2a^2 z - a^2 + b^2 z^2 + 2b^2 z) / Delta
p      = (a^2 z^2 - b^2) / Delta
```

普通话说：

```text
只要给一个吸收后的斜率 z 和一个高斯因子 a+bi，
这两条分支就自动给出一个候选闭合对。
```

---

## 3. 核心差因子

最关键的是：

```text
lambda - p =
  ((a+b) - z(a-b)) (z(a+b) - (a-b)) / Delta

lambda + p =
  d (z^2 + 2z - 1) / Delta
```

所以：

```text
lambda^2 - p^2 =
  d (z^2 + 2z - 1)
    ((a+b) - z(a-b))
    (z(a+b) - (a-b))
  / Delta^2
```

另外：

```text
lambda^2 - 1 =
  4 z d (a^2 z - a^2 + b^2 z^2 + b^2 z) / Delta^2
```

普通话说：

```text
倒数结论要排除 p != lambda。
这里 p != lambda 被拆成了两条很具体的线性因子。
如果未来能证明真成员平方条件强迫其中一条因子消失，
就能回到 p=lambda。
```

---

## 4. Product identity 项

对 `sum=A+B`，product ledger 使用：

```text
A_p = p^2 - 2p + (lambda+1)^2 + 1
B_p = p^2 - 2lambda^2 p + lambda^2(lambda+1)^2 + lambda^4
```

通式给出：

```text
A_p = d^2 (z^2 + 1)^2 / Delta^2
```

并且：

```text
B_p = d^2 F_- F_+ / Delta^4
```

其中：

```text
F_- =
  5a^2z^2 - 4a^2z + a^2
  - 2abz^3 - 2abz
  + b^2z^4 + 4b^2z^3 + 5b^2z^2

F_+ =
  5a^2z^2 - 4a^2z + a^2
  + 2abz^3 + 2abz
  + b^2z^4 + 4b^2z^3 + 5b^2z^2
```

核心恒等式仍逐项成立：

```text
B_p - lambda^2 A_p = (lambda^2 - 1)(lambda^2 - p^2)
```

普通话说：

```text
A_p 在这个模型里几乎自动变成平方影子。
真正要吃掉的约束更可能藏在 B_p，
或者藏在 r、s 各自的四个真实成员平方条件里。
```

---

## 5. guard 数值复核

取：

```text
z = 4/3
a = 5
b = 2
d = 29
Delta = 161/9
```

得到：

```text
lambda = 535/161
p = 52/23
```

差因子为：

```text
lambda - p = 171/161
lambda + p = 899/161
lambda^2 - p^2 = 153729/25921
lambda^2 - 1 = 260304/25921
```

product identity 项为：

```text
A_p = 525625/25921 = (725/161)^2
F_- = 10201/81
F_+ = 22201/81
B_p = 190463289241/671898241 = (436421/25921)^2
```

普通话说：

```text
guard 之所以能通过 product-square 层，
不是偶然撞上平方。
它正好落在这套 Gaussian 通式的平方影子里。
```

---

## 6. 四个成员项

这次还把四个真正的 `R_lambda` 成员项分开写入账本：

```text
r^2 + 1 =
  d (z^2 + 1) / (a + bz)^2

s^2 + 1 =
  d (z^2 + 1) / (a - bz)^2

r^2 + lambda^2 =
  d F_- / Delta^2

s^2 + lambda^2 =
  d F_+ / Delta^2
```

因此：

```text
(r^2+1)(s^2+1) = A_p
(r^2+lambda^2)(s^2+lambda^2) = B_p
```

普通话说：

```text
product 层只看到两个乘积 A_p、B_p。
真成员条件要每一项自己都是平方。
现在这四项也被拆开了：
两个 unit 项共享 d(z^2+1)，
两个 lambda 项分别对应 B_p 的两个共轭因子。
```

guard 中这四项为：

```text
r^2 + 1        = 725/529
s^2 + 1        = 725/49
r^2 + lambda^2 = 295829/25921
s^2 + lambda^2 = 643829/25921
```

它们都带着同一个非平凡 squareclass：

```text
29
```

所以 guard 只是 product-square shadow，不是真成员。

一个立即可用的子结论是：

```text
如果 z^2+1 已经是平方，
且 d 不是平方，
那么这个 `(plus, minus)` inverse Gaussian pair 不可能是真成员。
```

原因很简单：

```text
r^2+1 = d * square / square
s^2+1 = d * square / square
```

普通话说：

```text
只要 shadow 吸回去的 z 真的是勾股斜率，
再乘回一个非平凡高斯平方类 d，
就会把 r 和 s 的 unit 项都染上同一个 d。
它们能骗过乘积层，却骗不过单项平方层。
```

---

## 7. 新 helper

新增 dataclass：

```text
InverseGaussianAbsorptionPairTerms
```

新增 helper：

```text
inverse_gaussian_absorption_pair_terms(
    absorbed=z,
    squareclass=d,
    r_branch="plus",
    s_branch="minus",
)
```

当前只实现 `(plus, minus)` 分支。

新增测试：

```text
test_inverse_gaussian_absorption_pair_terms_factor_guard_identity
```

这个测试锁住：

```text
lambda(z,a,b)
p(z,a,b)
lambda-p
lambda+p
lambda^2-p^2
lambda^2-1
A_p
B_p
B_p - lambda^2 A_p
```

新增测试：

```text
test_inverse_gaussian_absorption_pair_terms_factor_member_squares
```

这个测试锁住四个单独成员项，并确认它们的乘积回到 `A_p,B_p`。

---

## 8. 对证明路线的影响

这仍不是 `sum=A+B` 证明，更不是全平面倒数定理证明。

但现在 only-1-mod-4 residual 的 guard 结构已经有更明确的代数入口：

```text
z
d = a^2 + b^2
Delta = a^2 - b^2z^2
two linear factors in lambda-p
one z-factor in lambda+p
```

下一步应检查：

```text
真成员四平方条件
```

能否强迫：

```text
((a+b) - z(a-b)) (z(a+b) - (a-b)) = 0
```

或强迫 `B_p` 的两个共轭因子落回中线障碍。

普通话说：

```text
现在敌人更具体了：
不是“某个神秘 residual”，
而是一个由 z,a,b 生成的平方影子。
要证明倒数定理，就要证明这个影子不能同时变成真的 R_lambda 成员。
```

---

## 9. 当前边界

可以安全说：

```text
1. guard residual 的 `(plus, minus)` 通式已写成可复跑账本；
2. 核心恒等式的两侧因子完全对齐；
3. A_p 的平方影子来源明确；
4. B_p 有共轭因子分解；
5. 四个单独成员项已经拆开，下一步可直接研究真平方约束。
```

不能说：

```text
所有 residual 都已被参数化。
真成员平方条件已经推出 p=lambda。
sum=A+B 已证明。
全平面倒数定理已证明。
```
