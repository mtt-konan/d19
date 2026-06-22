# wl253 — wl218 Gaussian absorption centerline shadow

日期：2026-06-22

## 1. 本轮目标

接 wl252。

wl252 说明：

```text
单个 only-1-mod-4 坏 squareclass 可以被 Gaussian absorption 吸收到真勾股斜率。
```

本轮继续问：

```text
如果 product-layer residual 的两个根 r,s 共享同一个坏 squareclass d，
分别吸收以后，会不会落到同一个真勾股斜率？
```

普通话说：

```text
上一轮会修单个假根。
这一轮看一整对假根一起修，会不会露出它背后的真实形状。
```

---

## 2. 新 helper

新增：

```text
residual_gaussian_absorption_ledger(condition)
```

输入是一个 `ClosureProductSquareConditions` residual。

它要求：

```text
member_squareclass_pair = (d,d), d != 1
```

然后分别对两个根调用：

```text
squareclass_two_square_absorption(r, d)
squareclass_two_square_absorption(s, d)
```

最后记录：

```text
common_absorbed_members
centerline_shadow
```

普通话说：

```text
如果两个假根吸收以后有共同的真勾股斜率，
那这个 residual 很可能不是新结构，
而是某个中心线/同斜率结构被坏 squareclass 投下来的影子。
```

---

## 3. guard 结果

旧 guard：

```text
lambda = 535/161
r = 14/23
s = 26/7
d = 29 = 5^2 + 2^2
```

对 `r`：

```text
r_plus  = 4/3
r_minus = 24/143
```

对 `s`：

```text
s_plus  = -144/17
s_minus = 4/3
```

共同的正真勾股斜率是：

```text
common_absorbed_members = (4/3,)
```

所以：

```text
centerline_shadow = True
```

普通话说：

```text
这两个看起来不同的假根，
把 29 吸掉以后，都指向同一个真斜率 4/3。
所以 guard residual 更像“中心线的影子”，而不是一个真正的新闭合分支。
```

---

## 4. 对证明路线的影响

这仍然不是 `sum=A+B` 证明。

但它把 only-1-mod-4 分支推进成一个更具体的猜想：

```text
若 product-layer residual 的共同 squareclass d 只含 1 mod 4 素因子，
则 Gaussian absorption 后应落回 centerline 或 reciprocal shadow。
```

如果能证明这一点，再接上已有 centerline/Yang Ji 边界，就可能关闭 only-1-mod-4 假点路线。

普通话说：

```text
以前的问题是：1 mod 4 坏因子怎么办？
现在问题更具体：吸掉这个坏因子以后，是否一定回到我们已经认识的中线结构？
```

---

## 5. 代码与测试

新增 dataclass：

```text
ResidualGaussianAbsorptionLedger
```

新增 helper：

```text
residual_gaussian_absorption_ledger(...)
```

新增测试：

```text
test_residual_gaussian_absorption_ledger_detects_centerline_shadow
```

测试锁住：

```text
r=14/23 的 plus 分支吸收到 4/3；
s=26/7 的 minus 分支吸收到 4/3；
common_absorbed_members = (4/3,)；
centerline_shadow = True。
```

---

## 6. 下一步

下一步应从 guard 推向一般式。

具体可以尝试：

```text
1. 对 finite root-grid residuals 批量统计 centerline_shadow；
2. 推导 Gaussian absorption 对 sum=A+B 的变换公式；
3. 证明 common absorption slope 触发既有 centerline obstruction。
```

普通话说：

```text
现在最有希望的一刀不是继续扩大枚举，
而是把“共同吸收到同一个斜率”写成代数恒等式。
如果这个恒等式成立，only-1-mod-4 分支就可能被送回中线定理。
```

---

## 7. 当前边界

可以安全说：

```text
1. guard residual 是 centerline shadow；
2. pair-level Gaussian absorption 已可复跑；
3. only-1-mod-4 分支有了更明确的归约方向。
```

不能说：

```text
所有 only-1-mod-4 residual 都已证明是 centerline shadow。
sum=A+B 已证明。
倒数定理已证明。
```
