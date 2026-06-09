# wl163 — `R_lambda` true-member boundary and next directions

日期：2026-06-09

## 1. 本轮意思

上一轮看到：

```text
closure hit 可能满足乘积 rs=lambda，
甚至看起来像 reciprocal pair。
```

但这还不够。

本轮补上的边界是：

```text
true_member_pair =
  r in R_lambda 且 s in R_lambda
```

普通话说：

```text
两个数能把 closure 拼上，
不等于两个数真的能同时配上正方形两边的距离。
```

这一步是为了防止后续把“闭包层面的假点”误当成“真正候选点”。

---

## 2. 新字段

`rational_ratio_hit_product_diagnostics(...)` 现在对每个 hit 记录：

```text
product = r1*r2
product_equals_lambda
reciprocal_pair
true_member_pair
```

关键测试样本：

```text
lambda = 6
r = 2
s = 3
```

它满足：

```text
r+s = 5 = |lambda-1|
rs = 6 = lambda
s = lambda/r
```

所以它是 closure 层面的 reciprocal pair。

但它不是：

```text
true_member_pair
```

普通话说：

```text
它长得像镜像闭合点，
但没有真的住进 R_lambda。
```

---

## 3. 小扫描记录

有限 ratio pool：

```text
pythagorean_leg_ratios(18)
lambda = 2..15
```

输出摘要：

```text
lambda=5: hits=1 product=lambda=0 reciprocal=0 true_member_pair=0 bad_true=0
  sum=A+B: r1=21/20, r2=99/20, p=2079/400, p=lambda=False, true=False

lambda=7: hits=2 product=lambda=0 reciprocal=0 true_member_pair=0 bad_true=0
  sum=A+B: r1=8/15, r2=112/15, p=896/225, p=lambda=False, true=False
  sum=|A-B|: r1=21/20, r2=99/20, p=2079/400, p=lambda=False, true=False

lambda=9: hits=1 product=lambda=0 reciprocal=0 true_member_pair=0 bad_true=0
  sum=|A-B|: r1=8/15, r2=112/15, p=896/225, p=lambda=False, true=False
```

可以说：

```text
有限 pool 里会出现 closure 假象。
这些假象目前都不是真 R_lambda 成员对。
```

不能说：

```text
有限扫描证明了 R_lambda translation theorem。
没有扫到 true hit 就说明全局没有 true hit。
```

---

## 4. 后续还有什么方向

我现在会把方向分成三类。

### A. 主线：攻 `R_lambda`

目标还是：

```text
若 r,s in R_lambda 且满足 full-plane closure，
是否必须 rs=lambda？
```

普通话说：

```text
两个真正候选点如果闭合，
是不是只能是一对 reciprocal 镜像点？
```

下一步不要扩大搜索，而是写代数 worksheet：

```text
设 r+s=T, p=rs。
把 r,s in R_lambda 翻译成只含 T,p,lambda 的平方条件。
然后尝试证明这些条件强迫 p=lambda。
```

这是最像主证明的方向。

### B. 固定线：当 proof laboratory

`A=B`、`A=kB` 这类线值得继续做，但不要把它当全局终点。

它的价值是：

```text
先在低维分支里看清楚失败机制。
如果失败机制不依赖 k，
才有机会推广到有理比例 lambda。
```

普通话说：

```text
固定线像小风洞。
它不能替代天空，
但能帮我们看气流怎么坏掉。
```

优先顺序可以是：

```text
A=B proof note
A=2B / A=3B 小素数样本
A=kB 的模条件或平方剩余障碍
```

### C. near-miss / D4：找结构，不当证明

`3/4 near-miss` 和 D4 坐标变量仍然值得做。

但重点要变成：

```text
把 near-miss 写成方程，
把 D4 对称写成不变量。
```

例如：

```text
x(1-x), y(1-y), A+B, |A-B|
```

视觉图看不出规律，不代表代数变量没有规律。

---

## 5. 当前建议

下一步最稳的是：

```text
1. 继续 R_lambda product worksheet。
2. 固定 closure target T。
3. 用 p=rs 消掉 r,s。
4. 看 membership 四个平方条件是否能推出 p=lambda。
```

如果这个方向卡住，再回到：

```text
A=kB proof note
near-miss equationization
D4 invariant rewrite
```

普通话总结：

```text
现在不是没有方向。
而是方向要分清：
R_lambda 是主攻；
固定线是样板；
near-miss 和 D4 是找结构的显微镜。
```

---

## 6. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_rational_ratio_hit_product_diagnostics_identify_reciprocal_pair -q
uv run pytest tests/test_rational_ratio.py -q
```

结果：

```text
1 passed
30 passed
```
