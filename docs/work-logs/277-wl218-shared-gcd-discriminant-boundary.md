# wl277 — wl218 shared-gcd discriminant boundary

日期：2026-06-22

## 1. 本轮目标

接 wl276。

wl276 暴露了一个补偿现象：

```text
q == 3 mod 4
v_q(lambda^2-p^2) odd
```

不一定立刻矛盾，因为同一个 `q` 可能也满足：

```text
v_q(lambda^2-1) odd.
```

本轮继续追踪这种共享奇赋值会不会被：

```text
p^2-1
```

或闭合二次方程判别式杀掉。

普通话说：

```text
如果同一个素数同时帮 lambda^2-1 和 lambda^2-p^2 配平，
那它一定也和 p^2-1 有关系。
问题是：这个关系是否已经足够推出矛盾？
```

---

## 2. 新 helper

新增 dataclass：

```text
ClosureIdentitySharedGcdRow
ClosureIdentitySharedGcdLedger
```

新增 helper：

```text
closure_identity_shared_gcd_ledger(lambda, target, product, relation)
```

它基于 wl276 的 helper，额外记录：

```text
v_q(p^2-1)
v_q(discriminant)
```

其中 `sum` 分支的判别式是：

```text
Delta = target^2 - 4p.
```

---

## 3. t+u near-miss 的共享补偿

继续看：

```text
lambda = 487/129
p = 2432/1075
target = 616/129
```

在 `q=7`：

```text
v_7(lambda^2-1)   = 1
v_7(lambda^2-p^2) = 1
v_7(p^2-1)        = 1
v_7(Delta)        = 0
```

普通话说：

```text
7 确实是共享奇补偿素数。
它也进入 p^2-1，这符合
(lambda^2-p^2) - (lambda^2-1) = 1-p^2。
```

但：

```text
v_7(Delta)=0
```

所以 `r,s` 是有理根这一点本身没有排除它。

---

## 4. 未共享奇素数

同一个 near-miss 里还有：

```text
q = 19471
```

它满足：

```text
v_q(lambda^2-1)   = 0
v_q(lambda^2-p^2) = 1
v_q(p^2-1)        = 0
v_q(Delta)        = 0
```

普通话说：

```text
这是未被 lambda^2-1 补偿的奇素数。
但这个点不是真成员，所以它只是一个边界样例；
真正证明还要问四项全平方时这种未补偿奇数能不能存在。
```

---

## 5. 对证明路线的影响

这轮说明：

```text
shared odd compensation => q divides p^2-1
```

但这还不够，因为：

```text
Delta = (lambda+1)^2 - 4p
```

可以在同一个 `q` 上保持偶赋值。

普通话说：

```text
共享补偿不会被“有理根判别式是平方”自动消灭。
下一步必须利用四项成员平方，而不是只用闭合二次方程。
```

用户原关键引理现在可以更精确地写成：

```text
在 r,s in R_lambda 且 r+s=lambda+1 的真成员假设下，
q == 3 mod 4 的 shared odd compensation 不可能发生，
除非 p=lambda 或落回已关闭边界。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. 共享奇补偿已经被追踪到 p^2-1；
2. 闭合判别式本身不排除共享奇补偿；
3. 下一步必须把四项成员平方重新纳入；
4. sum=A+B 仍未证明。
```

不能说：

```text
shared odd compensation 已关闭。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 7. 下一步

下一步应专门分析 shared odd prime `q`：

```text
q | lambda^2-1
q | lambda^2-p^2
q | p^2-1
q == 3 mod 4
```

在四项成员平方：

```text
r^2+1,
s^2+1,
r^2+lambda^2,
s^2+lambda^2
```

同时为平方时，是否强迫：

```text
r,s,lambda,p
```

落入某个符号组合：

```text
lambda ≡ ±1,
p ≡ ±1,
r,s roots of z^2-(lambda+1)z+p.
```

普通话说：

```text
接下来不是再加一个模筛，而是把 q 同时看见的四个平方项写成局部方程。
如果 q==3 mod 4，很多 “-1 是平方” 类型的可能性会被关掉。
```

---

## 8. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_closure_identity_shared_gcd_ledger_tracks_discriminant_boundary -q
```

结果：

```text
1 passed
```
