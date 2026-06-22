# wl275 — wl218 trivial-tube member squareclass boundary

日期：2026-06-22

## 1. 本轮目标

接 wl274。

wl274 只看 dual-slope recovery 层：

```text
x^2+1,
y^2+1.
```

本轮把同一批 positive trivial-tube local witness 还原回原始 `sum=A+B`
变量：

```text
lambda = 1/L
r = x/L
s = y/L
```

然后记录完整成员四项：

```text
r^2+1,
s^2+1,
r^2+lambda^2,
s^2+lambda^2.
```

普通话说：

```text
这次不只看 x,y。
我们直接看它离真正 R_lambda 成员还差在哪一项。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopePositiveTrivialTubeMemberLedger
```

新增 helper：

```text
sum_ab_dual_slope_positive_trivial_tube_member_ledgers()
```

它对 wl273 的两个 witness 记录：

```text
lambda,
r,s,
product,
四个 member values,
四个 squareclasses,
squareclass primes by term.
```

---

## 3. t+u 管道 witness

对：

```text
t=1/4, u=19/24
```

还原得到：

```text
lambda = 487/129
r = 8/15
s = 912/215
r+s = lambda+1
rs = 2432/1075 != lambda
```

成员四项：

```text
r^2+1              squareclass 1
s^2+1              squareclass 1
r^2+lambda^2       squareclass 6047561
s^2+lambda^2       squareclass 13414921
```

分解：

```text
6047561  = 13 * 173 * 2689
13414921 = 13 * 17 * 101 * 601
```

全部坏素数都是：

```text
1 mod 4.
```

普通话说：

```text
这个点已经过了 r^2+1 和 s^2+1。
它不是 R_lambda 成员，只是因为 lambda 那两项没过。
但失败仍然藏在 1 mod 4 素数里。
```

---

## 4. tu-1 管道 witness

对：

```text
t=1/4, u=7/8
```

还原得到：

```text
lambda = 7
r = 8/15
s = 112/15
r+s = lambda+1
rs = 896/225 != lambda
```

成员四项：

```text
r^2+1              squareclass 1
s^2+1              squareclass 1
r^2+lambda^2       squareclass 11089
s^2+lambda^2       squareclass 481
```

分解：

```text
11089 = 13 * 853
481   = 13 * 37
```

全部坏素数也都是：

```text
1 mod 4.
```

---

## 5. 对原始 q==3 mod 4 路线的影响

这轮比 wl274 更接近原始命题。

可以看到：

```text
r+s=lambda+1
r^2+1 square
s^2+1 square
```

仍然不够推出 `rs=lambda`。

而且这些 near-miss 的失败：

```text
r^2+lambda^2 not square
s^2+lambda^2 not square
```

不一定暴露任何 `q == 3 mod 4` 的奇 valuation。

普通话说：

```text
如果要用 3 mod 4 素数做矛盾，
不能只从“哪一项不是平方”粗暴抽一个坏素数。
因为坏素数可能全是 1 mod 4。
```

所以用户目标里的关键引理需要更精细：

```text
不是证明 near-miss 的某个失败项含 q==3 mod 4；
而是要在假设四项全是平方时，
通过 B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)
强制 lambda^2-p^2 的 valuation 冲突。
```

普通话说：

```text
3 mod 4 矛盾应该来自“全都已经是平方”的强约束，
不是来自这些半成员样例的失败因子。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. positive trivial-tube near-miss 可同时满足 closure 和两条 unit 成员平方；
2. 它们失败在 lambda 成员平方；
3. lambda 成员平方失败可完全由 1 mod 4 素数承载；
4. 因此 q==3 mod 4 引理必须使用四项全平方的假设，而不是 near-miss 失败素数。
```

不能说：

```text
q==3 mod 4 路线失败。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 7. 下一步

下一步应切回用户原始恒等式路线：

```text
p = rs
target = lambda+1
A_p = p^2 - 2p + target^2 + 1
B_p = p^2 - 2lambda^2*p + lambda^2*target^2 + lambda^4
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)
```

对真实成员假设：

```text
r^2+1, s^2+1, r^2+lambda^2, s^2+lambda^2 all squares
```

建立 valuation ledger，重点不要再只记录失败项的 squareclass，而要记录：

```text
在四项都为平方时，
identity 两边的 q==3 mod 4 valuation 如何被迫为偶/奇。
```

---

## 8. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_positive_trivial_tube_member_ledgers_fail_only_lambda_terms -q
```

结果：

```text
1 passed
```
