# wl279 — wl218 shared prime-power shadow split

日期：2026-06-22

## 1. 本轮目标

接 wl278。

wl278 把 shared odd compensation 的第一层 residue 缩成：

```text
q == 7 mod 8
```

仍有局部幸存。

本轮继续看这些幸存类在 `mod q^k` 下更像哪一种阴影：

```text
p ≈ lambda
```

还是：

```text
p ≈ -lambda.
```

普通话说：

```text
用户目标想最后逼出 p=rs=lambda。
但 shared prime 幸存时，局部上可能只是说明 p 接近 lambda，
也可能说明 p 接近 -lambda。
这两种后续要用不同办法杀。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbSharedOddPrimePowerLiftSummary
```

新增 helper：

```text
sum_ab_shared_odd_prime_power_lift_summary(q, k)
```

它枚举 `mod q^k` 下：

```text
v_q(lambda^2-1) = 1
v_q(lambda^2-p^2) = 1
r+s = lambda+1
rs = p
```

并要求四个成员项在 `mod q^k` 上都是平方：

```text
r^2+1,
s^2+1,
r^2+lambda^2,
s^2+lambda^2.
```

每个 surviving lift 记录：

```text
lambda mod q
p mod q
v_q(p-lambda)
v_q(p+lambda)
四个成员项的截断 valuation
```

---

## 3. q=7, k=2

输出：

```text
modulus = 49
total_lifts = 72

pattern_counts =
{
  (-1, -1, 1, 0, (0, 0, 0, 0)): 72
}
```

解释：

```text
lambda ≡ -1 mod 7
p      ≡ -1 mod 7
v_7(p-lambda) = 1
v_7(p+lambda) = 0
```

普通话说：

```text
q=7 这条幸存管道只像 p≈lambda，
不是 p≈-lambda。
```

---

## 4. q=31, k=2

输出：

```text
modulus = 961
total_lifts = 3600

pattern_counts =
{
  (-1, -1, 1, 0, (0, 0, 0, 0)): 1800,
  ( 1, -1, 0, 1, (0, 0, 0, 0)): 1800,
}
```

解释：

第一类：

```text
lambda ≡ -1 mod 31
p      ≡ -1 mod 31
v_31(p-lambda) = 1
v_31(p+lambda) = 0
```

第二类：

```text
lambda ≡ 1 mod 31
p      ≡ -1 mod 31
v_31(p-lambda) = 0
v_31(p+lambda) = 1
```

普通话说：

```text
q=31 已经出现 p≈-lambda 的局部幸存。
所以 shared-prime 路线不能只说“局部上 p 接近 lambda”。
还必须单独处理 p+lambda 管道。
```

---

## 5. 对证明路线的影响

这轮没有关闭 sum 分支，但把剩余问题分成两条：

```text
1. p-lambda shadow:
   shared odd prime 只说明 p 与 lambda 在 q 上贴近。
   这条可能适合做递降或证明最终 p=lambda。

2. p+lambda shadow:
   shared odd prime 说明 p 与 -lambda 在 q 上贴近。
   这条不能直接推出 p=lambda，
   必须用正性、闭合判别式、或四个成员平方的更高阶信息另杀。
```

普通话说：

```text
原来的关键引理要再拆一次。
不是所有 shared odd compensation 都朝 p=lambda 靠。
有一部分朝 p=-lambda 靠，这正是下一步最危险的管道。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. q == 3 mod 8 的 shared case 已被 wl278 第一层排除；
2. q == 7 mod 8 的 surviving lifts 可分成 p-lambda shadow 和 p+lambda shadow；
3. q=31 已显示 p+lambda shadow 在 mod q^2 层面真实存在；
4. sum=A+B 仍未证明。
```

不能说：

```text
shared odd compensation 已关闭。
q == 7 mod 8 管道只会逼 p=lambda。
sum=A+B 已证明。
倒数定理已证明。
```

---

## 7. 验证

新增测试：

```text
test_sum_ab_shared_odd_prime_power_lift_summary_tracks_p_shadow
```

TDD 记录：

```text
先失败：
ImportError: cannot import name 'sum_ab_shared_odd_prime_power_lift_summary'

实现后：
1 passed
```
