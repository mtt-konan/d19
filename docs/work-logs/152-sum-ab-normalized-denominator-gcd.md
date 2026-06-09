# wl152 — `sum=A+B` normalized denominator gcd

日期：2026-06-09

## 1. 本轮问题

wl151 已经把 same-orientation 的交叉乘来源写成 gcd 账本：

```text
P = bc
Q = ad
g = gcd(P,Q)
```

这轮继续往前一小步：

```text
把 P-Q、P+Q、P、Q 都除以 g 看。
```

普通话说：

```text
先把 P 和 Q 共有的部分剥掉，
再看剩下的差和和。
这样更接近“如果有解，能不能变小”的递降问题。
```

---

## 2. 新增诊断字段

扩展：

```text
sum_ab_same_orientation_cross_gcd_terms(...)
```

新增字段 / 属性：

```text
denominator_sum = P+Q
denominator_difference_over_gcd = (P-Q)/g
denominator_sum_over_gcd = (P+Q)/g
normalized_denominator_pair = (P/g, Q/g)
difference_factorization_over_gcd
sum_factorization_over_gcd
```

其中原始因式分解仍是：

```text
P-Q = ±2(mu+nv)(nu-mv)
P+Q = 2(mu-nv)(mv+nu)
```

除以 `g=gcd(P,Q)` 后，代码把系数写成 `Fraction`。

普通话说：

```text
现在不仅知道 P 和 Q 的共同因子从哪里来，
还可以直接看剥掉共同因子后的 P-Q 和 P+Q。
```

---

## 3. 样例

还是 near-miss：

```text
(m,n) = (4,1), odd
(u,v) = (7,2), odd

P = 360
Q = 420
g = 60
```

归一化后：

```text
P/g = 6
Q/g = 7

(P-Q)/g = -1
(P+Q)/g = 13
```

对应因式分解：

```text
P-Q = 2*30*(-1)
P+Q = 2*26*15

(P-Q)/g = (1/30)*30*(-1) = -1
(P+Q)/g = (1/30)*26*15 = 13
```

换成 even/even：

```text
P/g = 7
Q/g = 6
(P-Q)/g = 1
(P+Q)/g = 13
```

普通话说：

```text
这个样例剥掉共同因子后，只剩一对相邻数 6 和 7。
这很像递降会喜欢的形状，
但目前它只是样例，不是一般规律。
```

---

## 4. 能说什么，不能说什么

可以说：

```text
同向分支已有工具直接查看 (P/g,Q/g)、(P-Q)/g、(P+Q)/g。
near-miss 样例中归一化后是 (6,7)，差为 ±1。
```

不能说：

```text
所有 near-miss 归一化后都是相邻数。
same orientation 已关闭。
nu-mv != 0 已矛盾。
```

普通话说：

```text
我们只是把“共同因子剥掉后剩什么”变成可复查的量。
它像线索，不像结论。
```

---

## 5. 下一步

下一步建议写一个小扫描，不是为了证明，而是为了找递降形状：

```text
same orientation
primitive parity
other/pass 或 both-pass residue
统计 normalized_denominator_pair = (P/g,Q/g)
统计 |(P-Q)/g|
统计 (P+Q)/g 的因子分解
```

最想确认的问题：

```text
1. near-miss 中 |(P-Q)/g|=1 是否常见，还是只是样例？
2. 如果 both-pass 真存在，normalized pair 是否必须也是一组共享腿参数？
3. nu-mv 的因子是否经常被 g 吃掉，还是会留在 (P-Q)/g 里？
```

如果第 2 点能转成：

```text
从 (P,Q,N) 生成更小的 (P',Q',N')
```

才可能成为真正的递降证明。

---

## 6. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_cross_gcd_terms_expose_denominator_source -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
28 passed
392 passed, 2 warnings
```
