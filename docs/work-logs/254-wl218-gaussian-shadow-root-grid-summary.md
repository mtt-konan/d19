# wl254 — wl218 Gaussian shadow root-grid summary

日期：2026-06-22

## 1. 本轮目标

接 wl253。

wl253 说明旧 guard residual 是：

```text
centerline_shadow = True
```

也就是两个假根经过 Gaussian absorption 后落到同一个真勾股斜率。

本轮把这个现象提升成 root-grid 摘要：

```text
bounded root-grid residuals 中，有多少是 centerline shadow？
```

普通话说：

```text
上一轮看一个例子。
这一轮让工具在小范围里统一统计：
所有 product-layer residual 是不是都像这个例子一样，
只是中线结构的影子？
```

---

## 2. 新 helper

新增：

```text
sum_ab_root_grid_gaussian_shadow_summary(
    max_numerator=...,
    max_denominator=...,
)
```

它枚举：

```text
sum_ab_product_square_residuals_from_root_grid(...)
```

并对每个 residual 调用：

```text
residual_gaussian_absorption_ledger(...)
```

统计：

```text
total_residuals
centerline_shadow_count
nonshadow_count
common_absorbed_member_counts
examples_by_bucket
```

普通话说：

```text
这张表不是证明。
它只是告诉我们：在有限范围里，product-layer 假点是不是都能吸回中线。
```

---

## 3. 小范围结果

测试锁住范围：

```text
max_numerator = 26
max_denominator = 23
```

结果：

```text
total_residuals = 1
centerline_shadow_count = 1
nonshadow_count = 0
common_absorbed_member_counts = {
  (4/3,): 1
}
```

唯一例子仍是：

```text
lambda = 535/161
r = 14/23
s = 26/7
member_squareclass_pair = (29,29)
```

普通话说：

```text
这个小范围里唯一的假点，
确实完全吸回了同一个斜率 4/3。
目前没有看到非 shadow residual。
```

---

## 4. 对证明路线的影响

这继续支持一个更具体的归约猜想：

```text
product-layer residual
+ common only-1-mod-4 squareclass
=> Gaussian absorption centerline shadow
```

如果这个猜想能被证明，则 only-1-mod-4 假点路线可以接回：

```text
centerline obstruction / Yang Ji
```

普通话说：

```text
1 mod 4 坏因子现在不是“额外敌人”，
而像是把中线斜率乘上高斯因子后产生的假象。
证明要做的是把这个“像”写成恒等式。
```

---

## 5. 代码与测试

新增 dataclass：

```text
GaussianShadowSummary
```

新增 helper：

```text
sum_ab_root_grid_gaussian_shadow_summary(...)
```

新增测试：

```text
test_sum_ab_root_grid_gaussian_shadow_summary_counts_centerline_shadows
```

测试锁住：

```text
bounded root-grid residual 总数为 1；
centerline shadow 数为 1；
共同吸收斜率是 4/3。
```

---

## 6. 下一步

下一步应从统计转向代数公式。

要推导：

```text
r = inverse_absorb(z, d, sign_r)
s = inverse_absorb(z, d, sign_s)
r+s = lambda+1
```

时：

```text
lambda, p=rs, A_p, B_p
```

如何用：

```text
z, d=a^2+b^2, sign_r, sign_s
```

表示。

普通话说：

```text
现在要把“两个根都吸到 z”反过来写：
从同一个 z 和同一个高斯因子出发，
能生成哪些 residual？
如果全都只是 centerline shadow，
就能把这个分支接回已知中线排除。
```

---

## 7. 当前边界

可以安全说：

```text
1. bounded root-grid 的已知 residual 是 Gaussian centerline shadow；
2. 这个结论有可复跑摘要；
3. 下一步应推导 absorption 的反向参数公式。
```

不能说：

```text
所有 residual 都已证明是 shadow。
sum=A+B 已证明。
倒数定理已证明。
```
