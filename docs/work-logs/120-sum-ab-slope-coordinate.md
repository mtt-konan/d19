# wl120 — `sum=A+B` 四单项平方的斜率坐标

日期：2026-06-09

承接 wl119。

wl119 说明：

```text
A_p, B_p, D 都是平方
```

这个弱 `p` 模型不够强。它会产生假解，因为两个乘积是平方，不代表四个单项分别是平方。

本轮换一个坐标，保留四单项平方条件。

---

## 1. 起点

sum closure：

```text
r+s = λ+1
```

真实 membership：

```text
r^2+1   是有理平方
s^2+1   是有理平方
r^2+λ^2 是有理平方
s^2+λ^2 是有理平方
```

`r^2+1` 是平方，说明 `r` 是一个勾股斜率。

`r^2+λ^2` 是平方，除以 `λ^2`：

```text
(r/λ)^2 + 1 是有理平方
```

所以：

```text
r∈R_λ
<=> r 和 r/λ 都是勾股斜率。
```

这是本轮的核心坐标变化。

---

## 2. 新变量

令：

```text
x = r/λ
y = s/λ
```

于是：

```text
r = λx
s = λy
```

sum closure：

```text
λx + λy = λ + 1
```

移项：

```text
λ(x+y-1)=1
```

所以：

```text
λ = 1/(x+y-1)
```

要求 `λ>0`，所以：

```text
x+y>1
```

真实 membership 变成四个勾股斜率条件：

```text
x 是勾股斜率
y 是勾股斜率
λx 是勾股斜率
λy 是勾股斜率
```

普通话说：

```text
先选两个“相对 λ 的斜率” x,y。
它们自己要能成勾股。
按 closure 算出 λ。
再要求 λx, λy 也能成勾股。
```

这比 `p=rs` 模型更接近真实问题，因为它没有把两个平方乘在一起。

---

## 3. reciprocal orbit 在这个坐标里是什么

若：

```text
rs = λ
```

代入 `r=λx, s=λy`：

```text
λ^2xy = λ
```

因为 `λ>0`：

```text
λxy = 1
```

而 closure 给：

```text
λ(x+y-1)=1
```

所以：

```text
xy = x+y-1
```

即：

```text
(x-1)(y-1)=0
```

也就是说：

```text
reciprocal orbit 对应 x=1 或 y=1。
```

但：

```text
1^2+1 = 2
```

不是有理平方。

所以在 `sum=A+B` 分支里，如果 `x,y` 都必须是勾股斜率，那么 reciprocal orbit 也不会给真解。

这和 wl115-wl116 的 same-orbit 排除一致。

---

## 4. 新的 theorem target

旧目标：

```text
r,s∈R_λ, r+s=λ+1
=> rs=λ
```

换成 `x,y` 后，等价于：

```text
x,y, λx, λy 都是勾股斜率
λ = 1/(x+y-1)
=> x=1 或 y=1
```

但 `x=1` 或 `y=1` 不是勾股斜率。

所以更强、更直接的目标是：

```text
不存在正有理 x,y，使得：

x+y>1,
x 是勾股斜率,
y 是勾股斜率,
x/(x+y-1) 是勾股斜率,
y/(x+y-1) 是勾股斜率。
```

这是 `sum=A+B` 分支的四单项平方版本。

---

## 5. 小范围探针

用勾股参数生成斜率：

```text
z = (m^2-n^2)/(2mn)
或
z = (2mn)/(m^2-n^2)
```

在 `m≤50` 的斜率池里，扫描：

```text
x,y
λ = 1/(x+y-1)
λx
λy
```

结果：

```text
max_m 10: 0 true hits
max_m 15: 0 true hits
max_m 20: 0 true hits
max_m 25: 0 true hits
max_m 30: 0 true hits
max_m 40: 0 true hits
max_m 50: 0 true hits
```

这不是证明，只说明：

```text
这个坐标没有马上暴露小反例。
```

它比 wl119 的弱 `p` 模型更可信，因为它直接检查四个单项平方。

---

## 6. 本轮代码变更

新增：

```text
src/rational_distance/concordant/rational_ratio.py
```

API：

```text
is_pythagorean_leg_ratio(z)
sum_ab_point_from_slopes(x, y)
scan_sum_ab_slope_pairs(slopes, include_false_members=False)
```

新增 dataclass：

```text
SumAbSlopePoint
```

新增测试：

```text
test_sum_ab_slope_pair_translates_to_rational_ratio_membership
test_scan_sum_ab_slope_pairs_finds_no_small_true_hits
```

测试固定：

```text
1. x,y 坐标能重建 λ,r,s；
2. closure `r+s=λ+1` 自动成立；
3. 只有四单项 membership 通过时才算 true hit；
4. 小斜率池没有 true hit。
```

---

## 7. 下一步

这条路线现在有一个更清楚的证明对象。

可以从勾股斜率参数开始：

```text
x = (a^2-b^2)/(2ab)
y = (c^2-d^2)/(2cd)
```

然后要求：

```text
x/(x+y-1)
y/(x+y-1)
```

也都是勾股斜率。

这可能落到一个递降命题：

```text
两个勾股斜率做 closure 归一化后，
不可能同时仍是勾股斜率。
```

也可能落到一个模障碍：

```text
x+y-1 的分母/分子带来某个 p≡3 mod 4 奇次因子。
```

下一轮建议：

```text
1. 写脚本输出 false member 的 squareclass obstruction；
2. 查 true-hit 条件在模 p 下是否已经空；
3. 如果模 p 不空，再尝试递降。
```

这就把 `sum=A+B` 分支从 `p` 单变量模型，推进到了真实四平方坐标。
