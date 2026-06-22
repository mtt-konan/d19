# wl250 — wl218 prime valuation ledger boundary

日期：2026-06-22

## 1. 本轮目标

接 wl249。

wl249 已经把 product identity 和真正的四个成员平方条件接起来：

```text
A_p = (r^2+1)(s^2+1)
B_p = (r^2+lambda^2)(s^2+lambda^2)
```

本轮继续加 prime valuation 账本，靠近用户原设想：

```text
对 q ≡ 3 mod 4 的素数比较赋值，
看是否能强制 lambda^2-p^2 出现矛盾，除非 p=lambda。
```

普通话说：

```text
上一轮把“影子平方”和“真平方”分开。
这一轮开始数每个素数出现了几次，看奇偶次数能不能把假点排掉。
```

---

## 2. 新 helper

新增：

```text
closure_member_prime_valuation_ledger(lambda_ratio, target, product, relation)
```

它基于 `closure_member_product_square_ledger`，记录每个相关素数 `q` 的：

```text
member_valuations:
  v_q(r^2+1)
  v_q(s^2+1)
  v_q(r^2+lambda^2)
  v_q(s^2+lambda^2)

identity_valuations:
  v_q(A_p)
  v_q(B_p)
  v_q(B_p - lambda^2 A_p)
  v_q(lambda^2 - 1)
  v_q(lambda^2 - p^2)
```

其中如果某个 identity 项为 `0`，赋值记为 `None`，避免把边界零项伪装成有限赋值。

普通话说：

```text
这个 helper 是显微镜。
它不会自动证明定理，但会告诉我们每个素数在哪些项里出现了奇数次。
```

---

## 3. guard 假点的新信息

仍看旧 guard：

```text
lambda = 535/161
r = 14/23
s = 26/7
p = 364/161
T = 696/161
```

它的四个成员值是：

```text
r^2+1            = 725/529
s^2+1            = 725/49
r^2+lambda^2     = 295829/25921
s^2+lambda^2     = 643829/25921
```

四项共同的坏 squareclass 是：

```text
29
```

而：

```text
29 ≡ 1 (mod 4)
```

所以：

```text
three_mod_four_member_squareclass_primes = ()
```

普通话说：

```text
这个假点不会被“只看 3 mod 4 的成员项奇赋值”抓住。
它的坏因子是 29，而 29 是 1 mod 4。
```

更细地看 `q=29`：

```text
member_valuations  = (1, 1, 1, 1)
identity_valuations = (2, 2, 2, 1, 1)
```

也就是说：

```text
A_p 和 B_p 的 29-赋值都是偶数；
四个原始成员项的 29-赋值都是奇数；
lambda^2-1 和 lambda^2-p^2 各自也带一个 29。
```

普通话说：

```text
29 在四个原始项里都只出现一次，所以它证明这些项不是真平方。
但相乘以后次数变成 2，于是 A_p、B_p 看起来仍然是平方。
同时 identity 右侧也把这个 29 配平了。
```

---

## 4. 对原关键引理的修正

这轮暴露一个必须修正的点。

不能直接写：

```text
只看 q ≡ 3 mod 4 的赋值，就能排除所有 product-layer 假点。
```

因为 guard 假点的坏 squareclass 是：

```text
29 ≡ 1 mod 4.
```

更准确的关键引理必须是下面二选一之一：

```text
版本 A:
  先证明在 sum=A+B 真闭合候选里，
  非平凡共同 squareclass 必须含有某个 q ≡ 3 mod 4；
  然后再用 q ≡ 3 mod 4 valuation 矛盾。

版本 B:
  不只看 q ≡ 3 mod 4，
  而是对所有共同 squareclass prime 做 valuation/gcd 控制，
  再额外利用 q ≡ 1 mod 4 的结构。
```

普通话说：

```text
如果想只用 3 mod 4 素数，那必须先证明坏东西一定会漏到 3 mod 4。
目前 guard 告诉我们：弱层假点完全可以只坏在 1 mod 4。
```

---

## 5. 真点 sanity check

用：

```text
lambda = 1
r = 3/4
s = 4/3
p = 1
T = 25/12
```

作为 sanity check。

这里：

```text
member_squareclass_primes = ()
```

唯一相关的 `3 mod 4` 素数是 `3`，但成员赋值为：

```text
v_3(r^2+1)        = 0
v_3(s^2+1)        = -2
v_3(r^2+lambda^2) = 0
v_3(s^2+lambda^2) = -2
```

全是偶数。

边界项：

```text
lambda^2 - 1 = 0
lambda^2 - p^2 = 0
```

所以对应赋值记为：

```text
None
```

普通话说：

```text
真平方时，每个素数的成员项赋值都应为偶数。
但 p=lambda 或 lambda=1 这类边界会让 identity 右侧某些因子变成 0，
这里必须单独处理，不能强行说它有某个有限赋值。
```

---

## 6. 对证明路线的影响

这一轮没有证明 `sum=A+B`。

它把用户原第 4 点推进成一个更精确的任务：

```text
原想法:
  用 q ≡ 3 mod 4 的 valuation 强制 lambda^2-p^2 矛盾。

现在必须补的前置:
  为什么任何非倒数真闭合候选的坏共同 squareclass
  必须被某个 q ≡ 3 mod 4 看见？
```

如果这个前置不成立，就要改成：

```text
同时处理 q ≡ 1 mod 4 的共同 squareclass prime。
```

普通话说：

```text
3 mod 4 估值路线还没死，
但它少了一块桥板：
要先把坏因子从 1 mod 4 世界赶出来，
或者干脆把 1 mod 4 也纳入证明。
```

---

## 7. 代码与测试

新增 dataclass：

```text
ClosureMemberPrimeValuationRow
ClosureMemberPrimeValuationLedger
```

新增 helper：

```text
closure_member_prime_valuation_ledger(...)
```

新增测试：

```text
test_closure_member_prime_valuation_ledger_tracks_squareclass_escape
```

测试锁住：

```text
1. guard 假点的坏 squareclass prime 是 29；
2. 29 不是 3 mod 4；
3. q=29 的四个成员赋值都是奇数；
4. A_p,B_p 的 q=29 赋值仍是偶数；
5. lambda=1 真点的成员赋值全是偶数，零 identity 项记为 None。
```

---

## 8. 下一步

下一步不要直接宣称 valuation 矛盾。

更具体的两个方向是：

```text
1. 在 bounded true-member 候选扫描里统计 member_squareclass_primes，
   看是否所有弱假点都可能只坏在 1 mod 4；

2. 对 sum=A+B 的斜率/Euclid 模型证明：
   如果共同 squareclass prime 全是 1 mod 4，
   那么它是否可以通过 Gaussian norm / Pythagorean 参数结构被吸收，
   最后逼回中心线或倒数线。
```

普通话说：

```text
下一步要回答：
坏因子如果全是 1 mod 4，是不是还能真闭合？
如果能，3 mod 4 路线不够；
如果不能，就要把“不能”的原因写成引理。
```

---

## 9. 当前边界

可以安全说：

```text
1. prime valuation 账本已经可复跑；
2. guard 假点说明 q≡3 mod4 成员赋值检查不是充分条件；
3. 原关键引理需要补前置，或扩大到所有 squareclass prime。
```

不能说：

```text
sum=A+B 已证明。
倒数定理已证明。
q≡3 mod4 valuation 已经排除所有非倒数候选。
```
