# wl276 — wl218 identity three-mod-four balance

日期：2026-06-22

## 1. 本轮目标

接 wl275。

wl275 告诉我们：

```text
near-miss 的失败项可以完全坏在 1 mod 4 素数里。
```

所以本轮不再只看失败项 squareclass，而是回到用户原始恒等式：

```text
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2).
```

本轮只追踪：

```text
q == 3 mod 4
```

在右侧两个因子之间的奇偶配平。

普通话说：

```text
如果 lambda^2-p^2 有一个 3 mod 4 的奇次数素数，
它不一定马上矛盾；
同一个素数也可能出现在 lambda^2-1 里，把右侧乘积配成偶数。
```

---

## 2. 新 helper

新增 dataclass：

```text
ClosureIdentityThreeModFourBalanceRow
ClosureIdentityThreeModFourBalanceLedger
```

新增 helper：

```text
closure_identity_three_mod_four_balance_ledger(lambda, target, product, relation)
```

它基于已有：

```text
closure_member_prime_valuation_ledger(...)
```

只提取 `q == 3 mod 4` 的几类素数：

```text
odd_identity_difference_primes
odd_lambda_squared_minus_product_squared_primes
shared_odd_lambda_squared_minus_one_primes
unshared_odd_lambda_squared_minus_product_squared_primes
```

---

## 3. t+u near-miss 的新信息

沿用 wl275 的：

```text
lambda = 487/129
p = rs = 2432/1075
target = lambda+1 = 616/129
```

它不是 `R_lambda` 真成员，但它适合暴露 valuation 边界。

在 `q == 3 mod 4` 里：

```text
odd_lambda_squared_minus_product_squared_primes = (7, 19471)
```

其中 `q=7` 的 row 是：

```text
identity_valuations =
  v(A_p)                 = 0
  v(B_p)                 = 0
  v(B_p-lambda^2 A_p)    = 2
  v(lambda^2-1)          = 1
  v(lambda^2-p^2)        = 1
```

普通话说：

```text
7 确实在 lambda^2-p^2 里出现奇数次，
但它也在 lambda^2-1 里出现奇数次，
所以右侧乘积的 7 次数变成 2，并没有立刻矛盾。
```

而 `q=19471` 的 row 是：

```text
identity_valuations =
  v(A_p)                 = 0
  v(B_p)                 = 0
  v(B_p-lambda^2 A_p)    = 1
  v(lambda^2-1)          = 0
  v(lambda^2-p^2)        = 1
```

普通话说：

```text
19471 是没有被 lambda^2-1 补偿的奇素数。
但这个点本来就不是真成员，所以它只是提示下一步要分析这种未补偿奇数
在四项全平方假设下能不能存在。
```

---

## 4. tu-1 near-miss 的新信息

沿用：

```text
lambda = 7
p = rs = 896/225
target = 8
```

这里：

```text
odd_lambda_squared_minus_product_squared_primes = ()
```

但仍有：

```text
odd_identity_difference_primes = (3,)
```

对应 `q=3`：

```text
v(B_p-lambda^2 A_p) = -3
v(lambda^2-1)       = 1
v(lambda^2-p^2)     = -4
```

普通话说：

```text
这一例里 lambda^2-p^2 在 3-adic 上是偶数次，
但 lambda^2-1 自己带奇数次，所以差项仍有奇数赋值。
```

---

## 5. 对关键引理的修正

用户目标里的第 4 点可以更精确地拆成两个子问题：

```text
1. 如果 lambda^2-p^2 出现 q==3 mod 4 的奇 valuation，
   必须排除它被 lambda^2-1 同素数奇 valuation 补偿；

2. 如果没有这种 q==3 mod 4 奇 valuation，
   必须解释为什么所有坏现象藏在 1 mod 4 仍不可能形成真成员。
```

普通话说：

```text
不是看到 lambda^2-p^2 有奇数次 3 mod 4 素数就赢了。
还要看 lambda^2-1 有没有同一个素数在帮它配平。
```

这轮还没有证明 `sum=A+B`。
它只是把 valuation 战场再缩小一层：

```text
真正要控的是 lambda^2-1 与 lambda^2-p^2 的 gcd/共享奇赋值。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. 原始 identity 的 3 mod 4 parity ledger 已可复跑；
2. lambda^2-p^2 的奇赋值可能被 lambda^2-1 共享补偿；
3. 关键引理必须处理 shared odd compensation；
4. sum=A+B 仍未证明。
```

不能说：

```text
3 mod 4 valuation 路线失败。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 7. 下一步

下一步应分析：

```text
gcd(lambda^2-1, lambda^2-p^2)
```

在 `sum=A+B` 且四项全平方假设下会被怎样限制。

因为：

```text
gcd(lambda^2-1, lambda^2-p^2)
  divides something controlled by p^2-1
```

但在有理数赋值层，需要逐素数写清楚。

普通话说：

```text
下一块桥板是 gcd 控制：
同一个 3 mod 4 素数什么时候能同时帮 lambda^2-1 和 lambda^2-p^2 配平？
如果这种配平只能发生在 p=lambda 或中心线边界，第一分支就会更接近关闭。
```

---

## 8. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_closure_identity_three_mod_four_balance_tracks_shared_compensation -q
```

结果：

```text
1 passed
```
