# wl123 — `sum=A+B` 三通过 near-miss 的 ratio-shadow orbit

日期：2026-06-09

## 1. 本轮问题

wl122 发现 `sum=A+B` 的三通过 near-miss 里，有些失败 squareclass 成对出现。

这轮不直接做完整 D4。

先做一个更保守、更容易复查的小归约：

```text
把一个 obstruction 的四个 ratio：

x, y, r=λx, s=λy

看成无序集合；
再允许四个 ratio 同时取倒数；
取两者中字典序较小的作为 key。
```

我把这个叫：

```text
ratio-shadow key
```

普通话说：

```text
先不管 λ 怎么变。
只问：这四个斜率本身，是不是同一批数，或者同一批数的倒数？
```

这比完整 D4 弱很多，但安全：它不会宣称我们已经掌握所有正方形对称。

---

## 2. 新增代码

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增 dataclass：

```text
SumAbRatioShadowOrbit
```

新增 API：

```text
sum_ab_ratio_shadow_key(obstruction)
group_sum_ab_ratio_shadow_orbits(obstructions)
```

`sum_ab_ratio_shadow_key` 做的事：

```text
direct     = sorted([x,y,r,s])
reciprocal = sorted([1/x,1/y,1/r,1/s])
key        = min(direct, reciprocal)
```

`group_sum_ab_ratio_shadow_orbits` 按这个 key 分组，并记录：

```text
member_count
failed_squareclasses
members
```

注意：

```text
这不是完整 D4 orbit。
这只是一个 conservative shadow。
```

---

## 3. 最小合并样例

两个三通过 near-miss：

```text
x = 7/24
y = 15/8
λ = 6/7
r = 1/4
s = 45/28
fail r1, squareclass 17
```

和：

```text
x = 8/15
y = 28/45
λ = 45/7
r = 24/7
s = 4
fail r2, squareclass 17
```

第一组四个 ratio：

```text
7/24, 15/8, 1/4, 45/28
```

第二组四个 ratio：

```text
8/15, 28/45, 24/7, 4
```

第二组取倒数：

```text
15/8, 45/28, 7/24, 1/4
```

正好是第一组。

所以它们合并到同一个 ratio-shadow orbit。

这解释了为什么它们的失败 squareclass 都是 `17`。

---

## 4. bounded orbit 统计

数据来源：

```text
slopes = pythagorean_leg_ratios(max_m)
three = scan_sum_ab_slope_obstructions(slopes, pass_count=3)
orbits = group_sum_ab_ratio_shadow_orbits(three)
```

结果：

| max_m | three-pass near-miss | ratio-shadow orbits | orbit size 分布 |
| ---: | ---: | ---: | --- |
| 10 | 4 | 2 | `{2: 2}` |
| 20 | 12 | 9 | `{1: 6, 2: 3}` |
| 30 | 23 | 16 | `{1: 9, 2: 7}` |
| 40 | 41 | 29 | `{1: 17, 2: 12}` |

可以安全说：

```text
wl122 看到的“成对影子”不是偶然笔误；
这个保守 key 到 max_m=40 能合并 12 对 near-miss；
剩下 17 个 singleton 没被这个 key 解释。
```

不能说：

```text
所有 near-miss 都来自 D4 对称；
ratio-shadow key 就是完整 D4；
sum=A+B 分支因此被证明。
```

---

## 5. max_m=40 的合并 orbit

下面只列 size=2 的 orbit。

```text
sf = 17
key = {1/4, 7/24, 45/28, 15/8}

(x,y,λ) = (7/24, 15/8, 6/7), fail r1
(x,y,λ) = (8/15, 28/45, 45/7), fail r2
```

```text
sf = 730
key = {87/451, 87/416, 780/451, 15/8}

(x,y,λ) = (87/416, 15/8, 416/451), fail r1
(x,y,λ) = (8/15, 451/780, 260/29), fail r2
```

```text
sf = 5713
key = {231/520, 33/68, 153/104, 45/28}

(x,y,λ) = (231/520, 153/104, 130/119), fail r1
(x,y,λ) = (28/45, 104/153, 255/77), fail r1
```

```text
sf = 10193
key = {3/4, 297/304, 403/396, 403/304}

(x,y,λ) = (304/297, 4/3, 297/403), fail r1
(x,y,λ) = (3/4, 403/396, 99/76), fail r2
```

```text
sf = 11698
key = {71/2703, 7/24, 1184/1113, 2516/213}

(x,y,λ) = (7/24, 2516/213, 568/6307), fail r1
(x,y,λ) = (213/2516, 1113/1184, 20128/497), fail r2
```

```text
sf = 11986
key = {87/416, 1479/2303, 987/884, 24/7}

(x,y,λ) = (87/416, 987/884, 7072/2303), fail r1
(x,y,λ) = (7/24, 884/987, 2632/493), fail r1
```

```text
sf = 24634
key = {12/35, 48/55, 21/20, 147/55}

(x,y,λ) = (55/48, 35/12, 16/49), fail r1
(x,y,λ) = (12/35, 21/20, 28/11), fail r2
```

```text
sf = 235418
key = {84/187, 720/1519, 989/660, 16813/10633}

(x,y,λ) = (1519/720, 187/84, 5040/16813), fail r1
(x,y,λ) = (84/187, 989/660, 11220/10633), fail r2
```

```text
sf = 507809
key = {168/425, 8/15, 572/425, 572/315}

(x,y,λ) = (15/8, 425/168, 42/143), fail r2
(x,y,λ) = (8/15, 572/315, 63/85), fail r2
```

```text
sf = 51137
key = {451/780, 7667/9212, 987/884, 45/28}

(x,y,λ) = (451/780, 987/884, 3315/2303), fail r1
(x,y,λ) = (28/45, 884/987, 14805/7667), fail r1
```

```text
sf = 871690
key = {483/799, 3/4, 960/799, 240/161}

(x,y,λ) = (3/4, 240/161, 644/799), fail r1
(x,y,λ) = (161/240, 799/960, 320/161), fail r2
```

```text
sf = 1517266
key = {129/1225, 129/920, 288/175, 252/115}

(x,y,λ) = (129/920, 252/115, 184/245), fail r1
(x,y,λ) = (115/252, 175/288, 672/43), fail r2
```

---

## 6. 怎么理解

这个结果支持一个更具体的下一步：

```text
不要直接在坐标图里找规律。
先把三通过 near-miss 放到 ratio-shadow orbit 里。
再研究每个 orbit 的不变量。
```

可考虑的不变量：

```text
四个 ratio 的乘积
四个 ratio 的和
四个 ratio 的倒数和
failed squareclass
λ 和 1/λ 的关系
```

如果这些不变量能给出一个固定形式，就可以再往 D4 变量推进：

```text
x(1-x)
y(1-y)
A+B
|A-B|
```

目前只证明了一件很弱但有用的事：

```text
三通过 near-miss 的一部分重复，确实来自 ratio/reciprocal shadow。
```

---

## 7. 下一步

### A. 给 squareclass 诊断加缓存

本轮 `max_m=40` 统计仍要一分钟级别。

原因：

```text
同一个 z 在许多 pair 中重复出现；
leg_ratio_squareclass(z) 每次都 factorint。
```

后续若继续做 orbit scan，应先缓存：

```text
cached_leg_ratio_squareclass
```

或让扫描函数内部复用一个局部 cache。

### B. 把 singleton 单独列出来

`max_m=40` 仍有 17 个 singleton。

这些点可能有三种解释：

```text
1. bound 太小，它们的 shadow mate 还没出现；
2. ratio-shadow key 太弱，没覆盖真正 D4 变换；
3. 它们代表新的 near-miss 类型。
```

下一轮可以只研究 singleton。

### C. 从 ratio-shadow 升级到真正 D4

ratio-shadow 忘掉了很多结构，尤其是：

```text
λ 怎么变；
哪个点对应正方形哪条边；
failed r1/r2 怎么随变换移动。
```

真正 D4 需要把这些也放进去。

本轮的 key 只是一个安全的起点。

---

## 8. 验证

新增测试：

```text
test_sum_ab_ratio_shadow_key_identifies_reciprocal_near_misses
test_group_sum_ab_ratio_shadow_orbits_merges_reciprocal_pair
```

运行：

```text
uv run pytest tests/test_rational_ratio.py -q
```

结果：

```text
18 passed
```

本轮没有改变数学结论，只把 D4/倒数方向从“感觉像”推进到“有一个保守可测的 shadow orbit”。
