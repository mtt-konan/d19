# wl243 — wl218 K-square layer boundary

日期：2026-06-22

## 1. 本轮目标

接 wl242 的恒等式：

```text
4 A(a) R(a,K) = S(a,K)^2 + T(a)^2.
```

普通话说：

```text
上一轮发现一般 K 的剩余判别式 R(a,K)
和 centerline quartic A(a) 绑在一起。
这轮检查：这个恒等式本身够不够杀掉非中线？
```

结论：

```text
不够。
```

原因是：

```text
R(a,K) 是平方
K 是平方
```

这两件事可以同时发生；真正会继续卡住的是下一层：

```text
P=KQ 作为 y 二次式的判别式是否为平方。
```

---

## 2. 一个边界样本

取：

```text
a = 1/2
x = (1-a^2)/(2a) = 3/4
K = 36/25 = (6/5)^2.
```

此时 wl242 的剩余 quartic 为：

```text
R(a,K) = 9409/2500 = (97/50)^2.
```

也就是说：

```text
K 是平方；
R(a,K) 也是平方。
```

但回到真正的 `P=KQ`，把它看成关于 `y` 的二次方程，
判别式是：

```text
D_y = 10179/2500.
```

这不是有理平方。

普通话说：

```text
R 和 K 都过关，还不代表能解出有理 y。
所以 wl242 的 R 层只是中间门，不是原问题的门。
```

---

## 3. 层级关系

现在需要区分三层：

```text
Layer 1: K = P/Q 是平方。
Layer 2: 代入 x 参数后，R(a,K) 是平方。
Layer 3: P=KQ 作为 y 二次式，判别式 D_y 是平方。
Layer 4: 解出的 y 还要满足 y^2+1 是平方。
```

wl242 的恒等式控制的是：

```text
Layer 2
```

但 sum=A+B 主目标需要至少到：

```text
Layer 4.
```

普通话说：

```text
不能在第二层宣布胜利。
真正的敌人还在第三、第四层。
```

---

## 4. 对 valuation 路线的影响

用户最初希望用：

```text
p ≡ 3 mod 4 的 valuation
```

逼出矛盾。

现在更精确地说，valuation 应该优先作用在：

```text
D_y
```

或：

```text
D_y 与 y^2+1 square 的组合
```

而不是只作用在：

```text
R(a,K)
```

因为 `R(a,K)` 可以是平方，同时仍然没有有理 `y`。

---

## 5. 代码入口

新增 helper：

```text
sum_ab_k_square_candidate_y_discriminant(a, K)
```

记录：

```text
x = (1-a^2)/(2a)
K 是否平方
R(a,K) 是否平方
P=KQ 的 y 判别式 D_y
D_y 是否平方
```

新增测试：

```text
test_sum_ab_k_square_candidate_y_discriminant_separates_layers
```

---

## 6. 当前证明边界

可以安全说：

```text
1. R(a,K) square + K square 不足以推出 y 有理；
2. wl242 的恒等式是 Layer 2 工具；
3. 后续必须打 Layer 3/4。
```

不能说：

```text
R(a,K) 的两平方和恒等式已经关闭一般 K。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 7. 下一步

下一步应直接分析：

```text
D_y = -4*(K^2x^2 - 2K^2x + K^2
          -3Kx^2 + 2Kx - K + x^2)
```

并加入：

```text
x^2+1 square
y^2+1 square.
```

普通话说：

```text
下一刀要切在真正让 y 出现的判别式上。
```
