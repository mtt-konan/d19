# wl122 — `sum=A+B` 三项通过、一项失败的 near-miss 层

日期：2026-06-09

## 1. 本轮问题

wl121 已经能看出一个 `sum=A+B` 四斜率候选死在哪一项：

```text
x, y, λx, λy
```

其中 `x,y` 是先选的勾股斜率，closure 强制：

```text
λ = 1/(x+y-1)
```

本轮把里面最像 near-miss 的层单独拎出来：

```text
四项里有三项是勾股斜率，
只剩第四项不是。
```

普通话说：

```text
三条边已经对了，第四条差一点。
```

这比“两项过、两项不过”更接近 closure-first near-miss，也更可能被写成方程。

---

## 2. 新增代码

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

给 `SumAbSlopeObstruction` 增加：

```text
passed_terms
pass_count
failure_count
three_pass_near_miss
```

新增扫描函数：

```text
scan_sum_ab_slope_obstructions(slopes, pass_count=None)
```

用途：

```text
scan_sum_ab_slope_obstructions(slopes, pass_count=3)
```

只抓“三项通过、一项失败”的候选。

这仍然只是诊断层，不是证明器。

---

## 3. 固定样例

取：

```text
x = 15/8
y = 7/24
```

它们都是勾股斜率：

```text
(15/8)^2 + 1 = (17/8)^2
(7/24)^2 + 1 = (25/24)^2
```

closure 给出：

```text
λ = 1/(15/8 + 7/24 - 1) = 6/7
r = λx = 45/28
s = λy = 1/4
```

其中：

```text
r^2+1 = (45/28)^2 + 1 = (53/28)^2
s^2+1 = (1/4)^2 + 1 = 17/16
```

所以四项情况是：

```text
x: pass
y: pass
r: pass
s: fail, squareclass 17
```

这就是一个标准的三通过 near-miss。

注意：如果扫描器先排序斜率，它会写成 `x=7/24, y=15/8`，于是失败项名字变成 `r1`。这是命名差异，不是数学差异。

---

## 4. bounded scan

扫描方式：

```text
slopes = pythagorean_leg_ratios(max_m)
枚举 x<=y
令 λ=1/(x+y-1)
保留 pass_count=3 的 obstruction
```

结果：

| max_m | slopes | candidates | three-pass near-miss | fail r1 | fail r2 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 44 | 833 | 4 | 2 | 2 |
| 15 | 94 | 3,735 | 6 | 4 | 2 |
| 20 | 172 | 12,486 | 12 | 7 | 5 |
| 30 | 372 | 58,113 | 23 | 12 | 11 |
| 40 | 662 | 183,506 | 41 | 20 | 21 |

可以安全说：

```text
三通过 near-miss 在这个 bounded 池里很少；
左右失败数量大致平衡；
没有 true hit。
```

不能说：

```text
三通过 near-miss 全部都不可能升级为四通过；
sum=A+B 已证明无解。
```

---

## 5. 重复 squareclass 组

在 `max_m=40` 的 41 个三通过 near-miss 中，有些失败 squareclass 成对出现。

例如：

```text
sf = 17

x = 7/24, y = 15/8
λ = 6/7
fail r1

x = 8/15, y = 28/45
λ = 45/7
fail r2
```

```text
sf = 10193

x = 3/4, y = 403/396
λ = 99/76
fail r2

x = 304/297, y = 4/3
λ = 297/403
fail r1
```

```text
sf = 24634

x = 12/35, y = 21/20
λ = 28/11
fail r2

x = 55/48, y = 35/12
λ = 16/49
fail r1
```

```text
sf = 1517266

x = 129/920, y = 252/115
λ = 184/245
fail r1

x = 115/252, y = 175/288
λ = 672/43
fail r2
```

这看起来不像完全随机。

很多成对样例伴随：

```text
斜率取倒数
x,y 交换
r,s 交换
λ 变换
```

这和之前想做的 D4 对称变量是同一个味道：图上看不出规律，但 squareclass 层能看见“影子成对”。

---

## 6. 目前的解释

三通过 near-miss 可以被理解成一个中间曲线：

```text
x 是勾股斜率
y 是勾股斜率
λx 是勾股斜率
λ = 1/(x+y-1)
```

然后问：

```text
λy 为什么不是勾股斜率？
```

或者交换左右：

```text
x,y,λy 通过，λx 失败。
```

这比直接证明四项不可能更柔和。

普通话说：

```text
不要一口吃掉四条边。
先研究“已经有三条边对了”的点。
如果能证明第四条永远差一个非平方类，
那就是 closure-first near-miss 的理论版。
```

---

## 7. 下一步

### A. 参数化三项通过

先固定：

```text
x 是勾股斜率
y 是勾股斜率
r = λx 是勾股斜率
λ = 1/(x+y-1)
```

把它写成参数：

```text
x = (u^2-v^2)/(2uv)
y = (p^2-q^2)/(2pq)
r = (a^2-b^2)/(2ab)
```

再由：

```text
r = x/(x+y-1)
```

解出一个三项曲面/曲线。

真正要证明的是第四项：

```text
s = y/(x+y-1)
```

不可能也是勾股斜率。

### B. 做 D4/倒数归约

三通过样例里已经出现重复 squareclass 成对。

下一步可以把每个 obstruction 归一到某个 orbit：

```text
x <-> 1/x
y <-> 1/y
x <-> y
r <-> s
λ <-> 1/λ 或相关变换
```

先不要声称这就是完整 D4，只把经验 orbit 写清楚。

如果 41 个点能合并成更少的 orbit，说明这层确实适合用对称变量重写。

### C. 给 squareclass 加缓存

这轮统计 `max_m=40` 需要几十秒，因为每对都要 factorint。

如果后续还要扫三通过 near-miss，应该加缓存：

```text
leg_ratio_squareclass(z)
```

按 `z` 缓存结果，避免同一个斜率在许多 pair 里反复分解。

这属于工程加速，不影响数学结论。

---

## 8. 验证

新增测试：

```text
test_sum_ab_slope_obstruction_counts_three_pass_near_miss
test_scan_sum_ab_slope_obstructions_filters_three_pass_near_misses
```

运行：

```text
uv run pytest tests/test_rational_ratio.py -q
```

结果：

```text
16 passed
```

本轮只把 near-miss 中间层做成可复查对象，没有关闭任何全局分支。
