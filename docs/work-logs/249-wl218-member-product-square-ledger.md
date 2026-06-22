# wl249 — wl218 member-product square ledger

日期：2026-06-22

## 1. 本轮目标

接 wl248。

wl248 说明 same-orientation 的局部 3-adic residue 账本还不能直接关门。
本轮切回用户最初指定的 product identity 路线：

```text
B_p - lambda^2 A_p = (lambda^2 - 1)(lambda^2 - p^2)
```

重点不是重新检查 `A_p,B_p` 是否为平方，而是把它们和真正的四个成员平方条件分开。

普通话说：

```text
A_p 和 B_p 是两个平方条件相乘后的影子。
影子是平方，不代表每个原始物件自己都是平方。
倒数定理要用的是原始四个平方条件，不能只用影子。
```

---

## 2. 账本公式

固定一个闭合分支：

```text
T = closure target
p = rs
epsilon = -1 for sum relations
epsilon = +1 for diff relations
```

已有 product terms 是：

```text
A_p = p^2 + epsilon*2p + T^2 + 1
B_p = p^2 + epsilon*2lambda^2*p + lambda^2*T^2 + lambda^4
```

对于 sum 分支 `r+s=T`：

```text
A_p = (r^2+1)(s^2+1)
B_p = (r^2+lambda^2)(s^2+lambda^2)
```

对于 diff 分支 `|r-s|=T`，同样成立，只是根恢复的判别式是：

```text
D = T^2 + 4p
```

所以统一账本应同时记录：

```text
r^2 + 1
s^2 + 1
r^2 + lambda^2
s^2 + lambda^2
A_p
B_p
B_p - lambda^2 A_p
```

普通话说：

```text
下一步做 prime valuation 时，不能只问 A_p 和 B_p 是不是平方。
要问让 A_p 成为平方的两个因子，各自是不是已经是平方；
B_p 那边也一样。
```

---

## 3. 关键假阳性 guard

仍用旧 guard：

```text
lambda = 535/161
r = 14/23
s = 26/7
p = rs = 364/161
T = lambda + 1 = 696/161
```

它满足：

```text
r+s = T
p != lambda
A_p square
B_p square
```

具体是：

```text
r^2+1 = 725/529
s^2+1 = 725/49

r^2+lambda^2 = 295829/25921
s^2+lambda^2 = 643829/25921
```

四个 squareclass 是：

```text
(29, 29, 29, 29)
```

因此：

```text
A_p = (r^2+1)(s^2+1) 是平方
B_p = (r^2+lambda^2)(s^2+lambda^2) 是平方
```

但四项本身都不是平方，所以它不是真 `R_lambda` 成员对。

普通话说：

```text
这是一个会骗过 product layer 的假点。
它告诉我们：证明不能停在 A_p,B_p 是平方。
必须把 squareclass 从 29 压到 1。
```

---

## 4. 代码入口

新增 helper：

```text
closure_member_product_square_ledger(lambda_ratio, target, product, relation)
```

它返回：

```text
roots
unit_values          # r^2+1, s^2+1
lambda_values        # r^2+lambda^2, s^2+lambda^2
unit_product         # A_p
lambda_product       # B_p
member_squareclasses
member_squareclass_pair
true_member_pair
identity_terms
```

新增测试：

```text
test_closure_member_product_square_ledger_separates_weak_and_true_squares
```

测试锁住两种情况：

```text
1. guard 假点：A_p,B_p 是平方，但四项 squareclass 都是 29；
2. lambda=1 的真点：四项 squareclass 都是 1。
```

普通话说：

```text
这个 helper 是后续 valuation 证明的桥。
一边接 product identity，
另一边接真正的 R_lambda 成员条件。
```

---

## 5. 对证明路线的影响

这一轮没有证明 `sum=A+B`。

它把下一步要证明的关键引理重新表述得更准确：

```text
r,s in R_lambda
closure relation with product p
=> A_p and B_p are square for the strong reason:
   each factor is already square.
```

而弱假点只有：

```text
squareclass(r^2+1) = squareclass(s^2+1)
squareclass(r^2+lambda^2) = squareclass(s^2+lambda^2)
```

下一步要排除的是：

```text
member_squareclass_pair = (d, e), with d,e != 1
```

在 `sum=A+B` 真成员分支里继续存在。

普通话说：

```text
现在证明目标更清楚了：
不是证明影子不能是平方；
而是证明影子若来自同一个闭合关系，
那两个 squareclass 不能停在非 1 的相同值。
```

---

## 6. 下一步

下一步应在这个账本上加 prime valuation 行：

```text
for q == 3 mod 4:
  v_q(r^2+1)
  v_q(s^2+1)
  v_q(r^2+lambda^2)
  v_q(s^2+lambda^2)
  v_q(lambda^2-p^2)
```

目标是证明：

```text
若四个成员值都是真平方，
则 identity 右侧 (lambda^2-1)(lambda^2-p^2)
不能有奇 valuation，
除非 p=lambda。
```

但必须小心两个边界：

```text
1. lambda^2-1 也会贡献 valuation；
2. A_p,B_p 是平方只给 pairwise squareclass 相等，不能替代四项全平方。
```

普通话说：

```text
接下来才是真正靠近用户原设想的地方：
看每个 3 mod 4 素数的次数怎么分布，
并且始终记住我们看的是四个原始平方，不只是两个乘积。
```

---

## 7. 当前边界

可以安全说：

```text
1. product identity 与四个成员平方条件已经有统一可复跑账本；
2. guard 假点被测试锁住，防止再把弱平方当真成员；
3. 这为下一步 prime valuation 引理做准备。
```

不能说：

```text
sum=A+B 已证明。
倒数定理已证明。
member-product ledger 本身给出矛盾。
```
