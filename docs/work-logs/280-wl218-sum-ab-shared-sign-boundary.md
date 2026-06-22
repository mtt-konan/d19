# wl280 — wl218 sum=A+B shared-prime sign boundary

日期：2026-06-22

## 1. 本轮目标

接 wl275。

用户原路线是：

```text
r,s in R_lambda
r+s = lambda+1
p = rs
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)
```

然后用 `q == 3 mod 4` 的 valuation 逼：

```text
p = lambda.
```

普通话说：

```text
我们想证明：如果四个原始平方项都是真的平方，
那么 identity 右边不应该留下奇数次的 3 mod 4 素数。
```

本轮先把 shared odd compensation 的第一层符号完全写清楚。

---

## 2. 先修正公式

在 `sum=A+B` 分支：

```text
T = lambda+1
p = rs
r+s = T
```

正确的 product terms 是：

```text
A_p = p^2 - 2p + T^2 + 1
B_p = p^2 - 2lambda^2 p + lambda^2 T^2 + lambda^4
```

也就是：

```text
A_p = (r^2+1)(s^2+1)
B_p = (r^2+lambda^2)(s^2+lambda^2)
```

并且：

```text
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2).
```

不能写成：

```text
A_p = p^2 - T^2 + 1
B_p = p^2 - T^2 + lambda^2
```

普通话说：

```text
平方影子来自两个因子的乘积；
中间项是 -2p，不是 -T^2。
这个号如果写错，后面的 valuation 会走偏。
```

---

## 3. shared odd prime 的第一层归约

设 `q == 3 mod 4`，并假设它是 shared odd compensation prime：

```text
v_q(lambda^2-1) odd
v_q(lambda^2-p^2) odd
```

那么在 mod `q` 上：

```text
lambda ≡ ±1
p      ≡ ±1
```

因为 `lambda^2 ≡ 1`，四个成员平方条件在第一层都化成：

```text
r^2+1 square
s^2+1 square
```

同时：

```text
r+s = lambda+1
rs  = p.
```

普通话说：

```text
shared prime 一出现，lambda 和 p 在这个素数眼里只剩正负号。
问题变成四个符号组合里，哪些连最基本的平方剩余都过得去。
```

---

## 4. 四个符号组合

### Case `(lambda,p) = (1,1)`

```text
r+s = 2
rs  = 1
```

所以：

```text
r = s = 1
```

成员平方要求：

```text
r^2+1 = 2
```

是 mod `q` 的平方。

因此这一类要求：

```text
2 is square mod q
```

在 `q == 3 mod 4` 下等价于：

```text
q == 7 mod 8.
```

### Case `(lambda,p) = (-1,-1)`

```text
r+s = 0
rs  = -1
```

所以：

```text
r = ±1,  s = -r.
```

同样要求：

```text
r^2+1 = 2
```

是平方，因此也只在：

```text
q == 7 mod 8
```

可能幸存。

### Case `(lambda,p) = (-1,1)`

```text
r+s = 0
rs  = 1
```

所以：

```text
r^2 = -1.
```

但 `q == 3 mod 4` 时 `-1` 不是平方。

因此这类永远死。

### Case `(lambda,p) = (1,-1)`

```text
r+s = 2
rs  = -1
```

判别式是：

```text
Delta = 8.
```

所以首先也要求：

```text
2 is square mod q.
```

令 `alpha^2=2`，根为：

```text
r = 1 + alpha
s = 1 - alpha.
```

成员平方进一步要求：

```text
r^2+1 = 2(2+alpha)
s^2+1 = 2(2-alpha)
```

都是平方。因为 `2` 已经是平方，这等价于：

```text
2+alpha is square.
```

也就是 quartic：

```text
z^4 - 4z^2 + 2 = 0
```

在 `F_q` 中有根。

这个 quartic 是 `Q(zeta_16)^+` 的最小多项式之一；对奇素数 `q`，
它在 `F_q` 中有根当且仅当：

```text
q ≡ ±1 mod 16.
```

限制在：

```text
q == 3 mod 4
```

只剩：

```text
q == 15 mod 16.
```

普通话说：

```text
p ≈ -lambda 这条最危险的管道不是所有 q==7 mod 8 都能走。
它只在更窄的 q==15 mod 16 里第一层活着。
```

---

## 5. 第一层符号表

因此对 `q == 3 mod 4`：

```text
q mod 16 = 3:
  no sign case survives

q mod 16 = 7:
  (lambda,p) = ( 1,  1)
  (lambda,p) = (-1, -1)

q mod 16 = 11:
  no sign case survives

q mod 16 = 15:
  (lambda,p) = ( 1,  1)
  (lambda,p) = ( 1, -1)
  (lambda,p) = (-1, -1)
```

这和 `sum_ab_shared_odd_prime_residue_summary(q)` 的枚举一致。

---

## 6. 对关键引理的影响

原关键引理不能直接写成：

```text
shared odd compensation impossible.
```

因为第一层已经显示：

```text
q == 7 mod 16:
  p ≡ lambda 的同号管道仍活着；

q == 15 mod 16:
  p ≡ lambda 的同号管道活着，
  p ≡ -lambda 的异号管道也活着。
```

更准确的下一版关键引理应拆成：

```text
1. q == 3 or 11 mod 16 的 shared odd prime 直接矛盾；
2. q == 7 mod 16 只能落在 p-lambda shadow；
3. q == 15 mod 16 还要额外处理 p+lambda shadow。
```

普通话说：

```text
3 mod 4 赋值路线没有死，
但它不能“一刀切”。
它先把 shared prime 缩到两个窄管道，
然后还需要一个全局步骤把这些管道关掉。
```

---

## 7. 当前证明状态

可以安全说：

```text
1. sum=A+B 的 product formula 已校正；
2. shared odd prime 的第一层符号表已证明；
3. q == 3,11 mod 16 的 shared case 已被成员平方剩余排除；
4. q == 7,15 mod 16 仍有局部幸存；
5. p+lambda shadow 只可能从 q == 15 mod 16 出现。
```

不能说：

```text
sum=A+B 已证明。
shared odd compensation 已关闭。
倒数定理已证明。
```

---

## 8. 下一步

下一步要处理两个幸存管道：

```text
A. p-lambda shadow:
   shared prime 强迫 p 接近 lambda；
   需要证明这种接近要么无限提升到 p=lambda，
   要么和其他成员平方项冲突。

B. p+lambda shadow:
   只在 q == 15 mod 16 第一层出现；
   需要用正性、判别式、或更高阶成员平方条件排除。
```

普通话说：

```text
现在目标不再是“找一个 3 mod 4 素数就完事”。
真正要证明的是：所有能帮忙配平的 3 mod 4 素数，
最后都会把 p 推回 lambda，而不是允许 p != lambda。
```

---

## 9. 验证

可复跑：

```bash
PYTHONPATH=src uv run python - <<'PY'
from sympy import primerange
from rational_distance.concordant.rational_ratio import (
    sum_ab_shared_odd_prime_residue_summary,
)

for q in primerange(3, 200):
    if q % 4 != 3:
        continue
    summary = sum_ab_shared_odd_prime_residue_summary(q)
    print(q, "mod16", q % 16, "cases", summary.case_keys)
PY
```

本轮输出符合上表。
