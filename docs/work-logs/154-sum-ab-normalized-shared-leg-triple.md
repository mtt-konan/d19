# wl154 — `sum=A+B` normalized shared-leg triple

日期：2026-06-09

## 1. 本轮问题

wl153 说明：

```text
normalized pair = (P/gcd(P,Q), Q/gcd(P,Q))
```

有漂亮样例：

```text
(6,7)
```

但这只看了 `P,Q`，没有看共享腿：

```text
N
```

如果想做递降，真正对象应该更像：

```text
(N,P,Q)
```

普通话说：

```text
只看两条边，会漏掉同一个三角形最关键的那条共享腿。
递降不能只把 P,Q 变小，还要让 N 一起落下来。
```

---

## 2. 新增字段

扩展：

```text
SumAbNormalizedNearMissExample
```

新增：

```text
gcd_n_p_q = gcd(N,P,Q)
normalized_shared_leg_triple = (N/gcd_n_p_q, P/gcd_n_p_q, Q/gcd_n_p_q)
```

注意它和 wl153 的 pair 用的 gcd 不同：

```text
pair 用 gcd(P,Q)
triple 用 gcd(N,P,Q)
```

普通话说：

```text
pair 是“只剥 P,Q 的共同皮”；
triple 是“把 N,P,Q 的共同皮一起剥掉”。
后者更接近递降候选。
```

---

## 3. 关键样例

原始 near-miss：

```text
N = 105
P = 360
Q = 420
```

只看 `P,Q`：

```text
gcd(P,Q) = 60
(P/g,Q/g) = (6,7)
```

但看完整三元组：

```text
gcd(N,P,Q) = 15
(N/h,P/h,Q/h) = (7,24,28)
```

交换方向：

```text
(N,h-normalized P,h-normalized Q) = (7,28,24)
```

普通话说：

```text
漂亮的 (6,7) 不是完整对象。
真正约掉共同因子后，留下的是 (7,24,28)。
```

这很重要，因为：

```text
7^2 + 24^2 = 25^2
7^2 + 28^2 不是平方
```

也就是说，三通过 near-miss 的性质在 triple normalization 后仍然可见。

---

## 4. max_m<=20 观察

取每个 bucket 的首个样例：

```text
abs=1:
  pair=(6,7)
  triple=(7,24,28)

abs=11:
  pair=(119,130)
  triple=(231,476,520)

abs=17:
  pair=(28,11)
  triple=(147,140,55)

abs=38:
  pair=(45,7)
  triple=(28,45,7)

abs=231:
  pair=(260,29)
  triple=(451,780,87)
```

普通话说：

```text
pair 有时看起来很小；
但 triple 会把 N 重新带回来。
如果 N/h 仍然不小，递降就没那么直接。
```

---

## 5. 当前判断

可以说：

```text
normalized pair 不是完整递降对象。
后续若做递降，应优先研究 normalized shared-leg triple。
```

不能说：

```text
normalized triple 已经给出递降。
near-miss 都能约成更小 near-miss 族。
same orientation 已关闭。
```

普通话说：

```text
我们把钥匙又擦干净了一层。
但现在看到的是：齿形没有那么简单。
```

---

## 6. 下一步

下一步可以做一个非常具体的检查：

```text
对 normalized_shared_leg_triple=(N',P',Q')，
检查 N'^2+P'^2 和 N'^2+Q'^2 的 squareclass。
```

如果所有 near-miss 都保留：

```text
一边 squareclass=1
另一边有稳定 p≡3 mod 4 奇次因子
```

那会比 `delta` 或 `pair` 更接近证明。

如果 squareclass 分布很散：

```text
normalized triple 更像诊断坐标，不像直接 obstruction。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_normalized_near_miss_summary_counts_patterns -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
29 passed
393 passed, 2 warnings
```
