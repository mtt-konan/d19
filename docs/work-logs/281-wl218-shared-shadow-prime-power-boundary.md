# wl281 — wl218 shared-shadow prime-power boundary

日期：2026-06-22

## 1. 本轮目标

接 wl280。

wl280 把 shared odd compensation 的第一层符号表拆成：

```text
q == 7 mod 16:
  only p-lambda shadow survives

q == 15 mod 16:
  p-lambda shadow and p+lambda shadow both survive
```

本轮检查一个自然希望：

```text
这些幸存符号会不会在 q^2 或 q^3 层自动死亡？
```

普通话说：

```text
第一层模 q 可能太粗。
如果升到 q^2、q^3 后幸存点自己消失，
原来的 valuation 证明就还有一条短路。
```

结论是：不会自动死亡。

---

## 2. 复用的局部模型

使用现有 helper：

```text
sum_ab_shared_odd_prime_power_lift_summary(q, k)
```

它在 `mod q^k` 中枚举：

```text
v_q(lambda^2-1) = 1
v_q(lambda^2-p^2) = 1
r+s = lambda+1
rs = p
```

并要求四个成员项在 `mod q^k` 中都是平方剩余：

```text
r^2+1,
s^2+1,
r^2+lambda^2,
s^2+lambda^2.
```

它统计两类 shadow：

```text
p-lambda shadow: v_q(p-lambda) >= 1
p+lambda shadow: v_q(p+lambda) >= 1
```

普通话说：

```text
这是局部模型，不是真有理点。
它回答的是：只靠 q-adic 成员平方条件，能不能把管道杀掉。
```

---

## 3. `q^2` 统计

可复跑结果：

```text
q=7   mod16=7   total=72     p-lambda=72     p+lambda=0
q=23  mod16=7   total=968    p-lambda=968    p+lambda=0
q=31  mod16=15  total=3600   p-lambda=1800   p+lambda=1800
q=47  mod16=15  total=8464   p-lambda=4232   p+lambda=4232
q=71  mod16=7   total=9800   p-lambda=9800   p+lambda=0
q=79  mod16=15  total=24336  p-lambda=12168  p+lambda=12168
q=103 mod16=7   total=20808  p-lambda=20808  p+lambda=0
q=127 mod16=15  total=63504  p-lambda=31752  p+lambda=31752
q=151 mod16=7   total=45000  p-lambda=45000  p+lambda=0
q=167 mod16=7   total=55112  p-lambda=55112  p+lambda=0
q=191 mod16=15  total=144400 p-lambda=72200  p+lambda=72200
q=199 mod16=7   total=78408  p-lambda=78408  p+lambda=0
```

普通话说：

```text
q==7 mod16 的确只有 p 接近 lambda。
q==15 mod16 时，p 接近 -lambda 的坏管道不但活着，
还和 p 接近 lambda 的管道一样多。
```

---

## 4. `q^3` 稳定性样例

对 `q=31`：

```text
k=2:
  total = 3600
  p-lambda shadow = 1800
  p+lambda shadow = 1800

k=3:
  total = 3459600
  p-lambda shadow = 1729800
  p+lambda shadow = 1729800
```

更细地看 `p+lambda` 管道，`mod 31` 的根只落在：

```text
(r,s) = (9,24)
(r,s) = (24,9)
```

其中：

```text
lambda ≡ 1
p      ≡ -1
```

升到 `31^3` 时，每个 `31^2` 的一阶 key 都有 `31^2` 个 lift。

普通话说：

```text
p+lambda 管道不是二阶假象。
它有稳定的 q-adic 厚度。
```

---

## 5. 对证明路线的影响

因此不能期待下面的短证明：

```text
shared odd compensation survives mod q,
but dies mod q^2.
```

这条路已经被局部 lift 否掉。

更准确地说：

```text
q-adic square conditions alone不够。
```

必须再加入至少一种全局信息：

```text
1. 所有素数的有理平方类，而不是单个 q-adic 平方；
2. 正有理域和 height/descent；
3. 另一枚素数的同时约束；
4. 或把 p+lambda shadow 接回四斜率/bridge 的全局曲线。
```

普通话说：

```text
这不是坏消息，而是把错误捷径堵住。
后面证明不能只靠单素数 Hensel 失败，
必须用“全局平方”或递降。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. shared odd compensation 的 q^2 lift 已按 q mod 16 分裂；
2. q==7 mod16 只有 p-lambda shadow；
3. q==15 mod16 同时有 p-lambda 和 p+lambda shadow；
4. q=31 的 q^3 诊断显示 p+lambda shadow 稳定存在；
5. sum=A+B 仍未证明。
```

不能说：

```text
p+lambda shadow 已关闭。
shared odd compensation 已关闭。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 7. 下一步

下一步应换成全局问题。

优先尝试：

```text
假设 p+lambda shadow 在某个 q==15 mod16 上发生。
把 r,s 的 mod q 根写成 1±sqrt(2)。
再要求 r^2+1、s^2+1、r^2+lambda^2、s^2+lambda^2
在 Q 中都是平方。
```

看这是否强迫：

```text
1. 一个伴随素数 q' == 3 or 11 mod16 出现，从而矛盾；
2. 或产生一个更小的 p+lambda shadow，形成递降；
3. 或落回已知 centerline / E=0 分支。
```

普通话说：

```text
现在的剩余问题已经不是“局部有没有解”。
局部有很多解。
要证明的是这些局部解不能拼成真正的有理四平方解。
```

---

## 8. 验证

可复跑：

```bash
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_shared_odd_prime_power_lift_summary,
)

for q in (7, 23, 31, 47, 71, 79, 103, 127, 151, 167, 191, 199):
    summary = sum_ab_shared_odd_prime_power_lift_summary(q, 2)
    print(
        q,
        "mod16", q % 16,
        "total", summary.total_lifts,
        "p-lambda", summary.p_minus_lambda_shadow_count,
        "p+lambda", summary.p_plus_lambda_shadow_count,
    )
PY
```

本轮输出见第 3 节。
