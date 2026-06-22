# wl278 — wl218 shared odd prime residue split

日期：2026-06-22

## 1. 本轮目标

接 wl277。

wl277 说明：

```text
q == 3 mod 4
v_q(lambda^2-1) odd
v_q(lambda^2-p^2) odd
```

这种 shared odd compensation 不会被闭合判别式自动排除。

本轮把它先降到最小的有限域问题：

```text
lambda ≡ ±1 mod q
p      ≡ ±1 mod q
r+s    = lambda+1
rs     = p
```

并同时要求四个成员项在 mod `q` 上都是平方剩余：

```text
r^2+1,
s^2+1,
r^2+lambda^2,
s^2+lambda^2.
```

普通话说：

```text
如果 q 同时帮 lambda^2-1 和 lambda^2-p^2 配平，
那 lambda 和 p 在 mod q 里都只剩正负号。
先问这四种正负号里，哪些连第一层平方剩余都过不了。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbSharedOddPrimeResidueCase
SumAbSharedOddPrimeResidueSummary
```

新增 helper：

```text
sum_ab_shared_odd_prime_residue_summary(q)
```

它只处理第一分支：

```text
sum=A+B:
r+s = lambda+1.
```

对 `q == 3 mod 4` 素数，它枚举四个符号组合：

```text
(lambda mod q, p mod q) ∈ {(1,1), (1,-1), (-1,1), (-1,-1)}
```

并记录哪些组合存在 roots `(r,s)`，且成员平方剩余同时通过。

---

## 3. residue 表

可复跑输出：

```text
q=3:
  cases = ()

q=7:
  cases = ((1,1), (-1,-1))

q=23:
  cases = ((1,1), (-1,-1))

q=31:
  cases = ((1,1), (1,-1), (-1,-1))

q=19471:
  cases = ((1,1), (1,-1), (-1,-1))
```

可复跑模式：

```text
q ≡ 3 mod 8:
  all four sign cases die.

q ≡ 7 mod 16:
  surviving cases:
    (lambda,p) ≡ (1,1)
    (lambda,p) ≡ (-1,-1)

q ≡ 15 mod 16:
  surviving cases:
    (lambda,p) ≡ (1,1)
    (lambda,p) ≡ (1,-1)
    (lambda,p) ≡ (-1,-1)
```

另外：

```text
(lambda,p) ≡ (-1,1)
```

在这些 `q == 3 mod 4` 里都死。

普通话说：

```text
shared odd compensation 不是完全自由的。
第一层 residue 已经直接杀掉 q ≡ 3 mod 8；
q ≡ 7 mod 8 还会留下少量正负号清单。
```

---

## 4. 对证明路线的影响

这轮给出一个可用于后续证明的局部引理雏形：

```text
在 sum=A+B 分支中，
若 q == 3 mod 4 是 shared odd compensation prime，
且四项成员平方在 q 上都通过，
则 q != 3 mod 8。
```

这部分有直接短证明：

```text
lambda ≡ 1,  p ≡ 1:
  r+s=2, rs=1 -> r=s=1, so r^2+1=2 must be square.

lambda ≡ -1, p ≡ -1:
  r+s=0, rs=-1 -> r=±1, so r^2+1=2 must be square.

lambda ≡ -1, p ≡ 1:
  r+s=0, rs=1 -> -r^2=1, impossible because -1 is nonsquare.
```

因此若 `q ≡ 3 mod 8`，`2` 不是平方，上面三个可能全部死。
剩余 `lambda ≡ 1, p ≡ -1` 还需要 `2` 先是平方，所以也不可能在
`q ≡ 3 mod 8` 出现。

更细的 `q ≡ 7 mod 16` / `q ≡ 15 mod 16` 分裂目前由 helper 对给定
素数完整枚举；可作为下一步纸面引理候选，但本 wl 不把它当成已证明的
全素数定理。

保守结论是：

```text
q == 7 mod 8
```

是 shared case 的必要条件。

这还没有关闭 sum 分支，因为：

```text
q == 7 mod 8
```

仍然有 surviving local patterns。

普通话说：

```text
我们已经把一大片 shared prime 杀掉了，
但还没杀掉 q=7 mod 8 的幸存管道。
下一步要对这些幸存管道做更高阶 valuation 或递降。
```

---

## 5. 当前证明状态

可以安全说：

```text
1. shared odd compensation 不再是黑箱；
2. q == 3 mod 8 的 shared case 已被第一层 residue 排除；
3. q == 7 mod 8 仍有局部幸存；
4. sum=A+B 仍未证明。
```

不能说：

```text
shared odd compensation 已关闭。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 6. 验证

新增测试：

```text
test_sum_ab_shared_odd_prime_residue_summary_splits_sign_cases
```

已按 TDD 跑过：

```text
先失败：
ImportError: cannot import name 'sum_ab_shared_odd_prime_residue_summary'

实现后：
1 passed
```
