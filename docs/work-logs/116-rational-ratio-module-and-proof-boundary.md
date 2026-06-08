# wl116 — 有理比例模块、测试和证明边界

日期：2026-06-09

本轮把 wl115 的判断落到代码里：

```text
整数固定比例 A=kB 不是终点。
真正该看的比例是 λ=A/B，其中 λ 是正有理数。
```

原因还是那个朴素版本：

```text
如果反例存在，点在归一化坐标系里会给出有理比例。
这个比例通常不是整数。
```

所以继续只证整数 `k`，最多是在证一些很窄的切片。要想接近全局证明，必须把工具升级成 `λ∈Q_{>0}` 版本。

---

## 1. 新增代码

新增：

```text
src/rational_distance/concordant/rational_ratio.py
tests/test_rational_ratio.py
```

这个模块不生成整数候选，也不声称证明无解。它只做一件事：

```text
把固定比例分支里的关键恒等式，改成精确 Fraction 版本。
```

也就是让后面推导时不会混淆：

```text
整数 k 的事实
有理 λ 的事实
有限搜索现象
真正证明
```

---

## 2. 现在的有理比例模型

归一化 `B=1` 后：

```text
λ = A/B
r = N/B
```

定义：

```text
R_λ = { r∈Q_{>0} :
        r^2 + 1   是有理平方，
        r^2 + λ^2 是有理平方 }
```

full-plane closure 仍是四类：

```text
r+s   = λ+1
r+s   = |λ-1|
|r-s| = λ+1
|r-s| = |λ-1|
```

这说明整数 `k` 模型确实可以升级成有理 `λ` 模型，形式没有坏。

---

## 3. 模块记录的几个安全事实

### 3.1 membership 必须同时检查两个平方

`r∈R_λ` 不是只看一个勾股条件，而是同时要求：

```text
r^2+1   是有理平方
r^2+λ^2 是有理平方
```

这点防止把任意 residue survivor 或任意二次方程根误当成真候选。

### 3.2 reciprocal 对称仍成立

如果：

```text
r∈R_λ
```

那么：

```text
λ/r ∈ R_λ
```

证明只用代数恒等式：

```text
(λ/r)^2 + 1   = (r^2+λ^2)/r^2
(λ/r)^2 + λ^2 = λ^2(r^2+1)/r^2
```

这条很重要。它说明有理比例里仍有自然的成对结构：

```text
r  <->  λ/r
```

### 3.3 closure hit 只按真实等式判断

`find_rational_ratio_hits` 检查的是有理数等式：

```text
r+s
|r-s|
```

不是模筛 survivor，也不是近似浮点。

这和之前理论审查的要求一致：不能把局部筛过关写成全局证明。

---

## 4. 已经暴露出的危险点

整数 `k` 下常用的一句话：

```text
k^2+1 不可能是有理平方
```

不能搬到有理 `λ`。

反例：

```text
λ = 3/4
λ^2 + 1 = 25/16 = (5/4)^2
```

所以整数证明如果用了这种“夹在两个整数平方之间”的理由，到有理比例里会失效。

不过这不代表同一个 reciprocal orbit 真的可以 closure。比如：

```text
r=λ=3/4
```

还要检查：

```text
r^2+λ^2 = 2λ^2
```

这里会要求 `sqrt(2)` 是有理数，仍然不行。

简短说：

```text
旧理由坏了。
结论可能还对。
证明必须换。
```

---

## 5. 同 orbit 的当前边界

如果 closure 点来自同一个 reciprocal orbit：

```text
s = λ/r
```

那么一些关系会给很简单的根。

例如：

```text
r + λ/r = λ + 1
=> (r-1)(r-λ)=0
```

根只有：

```text
r=1 或 r=λ
```

它们都不是真正的 `R_λ` 点：

```text
r=1 需要 2 是有理平方
r=λ 需要 2λ^2 是有理平方
```

但另外两类关系会出现“二次方程有有理根”的情况。

例子：

```text
λ=6,   r+λ/r=|λ-1| 的根是 r=2,3
λ=3/2, |r-λ/r|=λ+1 的正根是 r=3
```

这些根仍然不是 `R_λ` 成员。测试已经覆盖这类危险样本。

这提醒我们：

```text
判别式有理平方 != 产生真实候选
```

下一步证明必须同时使用两个平方条件。

---

## 6. 记录下来的恒等式

### 6.1 product identity

对 sum closure：

```text
r+s = T
p = rs
```

模块记录：

```text
A_p = p^2 - 2p + T^2 + 1
B_p = p^2 - 2λ^2p + λ^2T^2 + λ^4
```

恒等式：

```text
B_p - λ^2 A_p = (λ^2-1)(λ^2-p^2)
```

这条可能是后面逼出 `p=λ`，也就是 `s=λ/r` 的入口。

但现在还没有证明：

```text
closure => p=λ
```

不能提前写死。

### 6.2 square-rectangle model

统一四个平方候选：

```text
(M-T)^2 + 4
(M+T)^2 + 4
(M-T)^2 + 4λ^2
(M+T)^2 + 4λ^2
```

测试检查了它们的差分结构。

直觉上，这是“一个小矩形的四个角都要落在有理平方上”。这个条件很硬，值得继续攻。

---

## 7. 测试状态

新增测试覆盖：

```text
R_λ membership 同时检查两个平方
reciprocal mate λ/r
full-plane closure 四类等式
有理 λ 下同 orbit 旧证明失效的危险样本
product identity
square-rectangle 差分结构
```

目标测试已经通过：

```text
uv run pytest tests/test_rational_ratio.py -q
7 passed

uv run pytest tests/test_rational_ratio.py tests/test_fixed_ratio_exact.py tests/test_fixed_ratio_sieve.py tests/test_scan_fixed_ratio_exact.py -q
19 passed
```

全量测试需要在本 wl 后重新跑一次。

---

## 8. 下一步建议

下一步不要先继续硬证整数 `A=kB`。

更值得做的是证明或否定这条：

```text
Rational-Ratio Translation Theorem

对任意 λ∈Q_{>0}，
若 r,s∈R_λ 且满足一条 full-plane closure 关系，
那么 s 必须等于 λ/r。
```

如果这条成立，后续路线会变得很干净：

```text
closure
=> 只能来自 reciprocal orbit
=> 同 orbit closure 被排除
=> 有理比例 λ 全部关闭
```

如果这条不成立，也很有价值，因为它会暴露真正难点：

```text
不同 reciprocal orbit 之间也可能发生 closure。
```

那时整数 `k` 分支就不能再当主路，只能当样本库。

---

## 9. 普通话总结

现在我们没有证明 `A=λB` 全部不行。

我们已经做的是：

```text
把问题换成了正确的有理比例语言，
并把几个容易误判的坑钉住了。
```

最关键的坑是：

```text
二次方程有根，不代表点是真的。
模筛能过，也不代表点是真的。
整数 k 的证明理由，不一定能搬到有理 λ。
```

下一步真正要打的是：

```text
两个 R_λ 点如果刚好满足 closure，
它们是不是只能是一对 λ/r？
```

这比继续证明整数切片更接近原问题。
