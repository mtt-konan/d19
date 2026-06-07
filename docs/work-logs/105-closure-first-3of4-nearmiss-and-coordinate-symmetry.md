# wl105 — closure-first 3/4 near-miss：速度、delta 分布、坐标还原与对称性

日期：2026-06-07

本 wl 冻结一条新复活的路线：**先强制 full-plane 闭合，再检查四条勾股边**。它来自用户提醒：

> 不走筛，先假定 `A,B,N1,N2` 已经满足正方形/全平面闭合条件；四条边里可能 `A-N1`、`N1-B`、`B-N2` 都是勾股数，只剩 `N2-A` 不是。点也可以在正方形外面。

这里的重点不是证明 Harborth，而是把这条路线变成可复跑、可分析、可接回坐标系的实验工具。

---

## 1. 口径

给定正整数 `A,B,N1,N2`，检查四条边：

```text
A^2 + N1^2
B^2 + N1^2
B^2 + N2^2
A^2 + N2^2
```

全平面闭合使用 wl093 的 GEN-CLOSURE 四关系：

```text
N1 + N2   = A + B
N1 + N2   = |A - B|
|N1 - N2| = A + B
|N1 - N2| = |A - B|
```

本轮专门收集：

```text
闭合精确成立 + 四条边恰好 3 条是平方
```

也记录 `4/4`。目前所有 bounded run 都是 `0` 个 `4/4`。

---

## 2. 实现与速度

脚本：

```text
scripts/theory/closure_first_three_square_search.py
```

测试：

```text
tests/test_closure_first_three_square_search.py
```

关键优化：

1. 生成每条腿的 Pythagorean partner 集合：`leg -> {N}`。
2. 反向建共同 `N`：`N -> [legs]`。
3. 同一个 `N` 下任意两条腿 `(A,B)` 至少共享一个共同 `N`。
4. 一个 `3/4` 候选必然让 `(A,B)` 共享至少一个共同 `N`，所以不用扫所有 `(A,B)`。
5. 不要求 `gcd(A,B)=1`。这条路线覆盖非互素层。

这不是旧 multi-N 的 `>=2` 共同 N 口径。旧 multi-N 找完整四边结构，通常需要两个共同 `N`。本路线只找 `3/4`，一个共同 `N` 就够。

速度对比：

| Bound | 旧版 | 快版 | 提速 |
|---:|---:|---:|---:|
| `max_leg=100`, `tail=300` | `0.0322s` | `0.0008s` | `40.9x` |
| `max_leg=500`, `tail=1500` | `1.0225s` | `0.0090s` | `113.5x` |
| `max_leg=2000`, `tail=5000` | `19.1705s` | `0.0348s` | `550.9x` |

大边界：

| Bound | `3/4` near-miss | `4/4` hit | time |
|---:|---:|---:|---:|
| `max_leg=10000`, `tail=25000` | `3,901` | `0` | `0.44s` |
| `max_leg=50000`, `tail=125000` | `20,623` | `0` | `3.66s` |
| `max_leg=100000`, `tail=250000` | `41,736` | `0` | `9.03s` |

测试状态：

```text
uv run pytest tests/test_closure_first_three_square_search.py -q
3 passed

uv run pytest -q
346 passed, 2 warnings
```

两个 warning 是旧的 `pytest.mark.slow` 未注册。

---

## 3. delta 1-10 分布

`max_leg=100000`, `diff_tail=250000`：

```text
3/4 near-miss: 41,736
4/4 hit: 0
```

失败边到最近平方的绝对 delta：

| delta | count |
|---:|---:|
| `1` | `1` |
| `2` | `0` |
| `3` | `0` |
| `4` | `0` |
| `5` | `0` |
| `6` | `6` |
| `7` | `6` |
| `8` | `4` |
| `9` | `2` |
| `10` | `6` |

低 delta 不连续。`2..5` 在此窗口完全不出现；`6..10` 出现小簇；`1` 只有一个样本。

按闭合关系：

| relation | delta `1..10` count |
|---|---:|
| `diff=A+B` | `8` |
| `diff=|A-B|` | `8` |
| `sum=|A-B|` | `7` |
| `sum=A+B` | `2` |

低 delta 主要来自外部 full-plane 关系，不是旧的内部关系 `N1+N2=A+B`。

按坏边：

| missing edge | delta `1..10` count |
|---|---:|
| `A-N1` | `16` |
| `B-N2` | `5` |
| `A-N2` | `2` |
| `B-N1` | `2` |

signed delta（`失败值 - 最近平方`）：

| signed delta | count |
|---:|---:|
| `-10` | `4` |
| `-9` | `2` |
| `-8` | `4` |
| `-7` | `4` |
| `-6` | `4` |
| `1` | `1` |
| `6` | `2` |
| `7` | `2` |
| `10` | `2` |

大部分低 delta 在平方下面。唯一 delta-1 在平方上面。

最强样本：

```text
(A,B,N1,N2) = (17745, 53911, 60840, 132496)
relation    = |N1-N2| = A+B = 71656
missing     = B-N2

17745^2 + 60840^2  = 63375^2
17745^2 + 132496^2 = 133679^2
53911^2 + 60840^2  = 81289^2
53911^2 + 132496^2 = 143044^2 + 1
```

这个样本的 gcd：

```text
gcd(A,B)     = 169
gcd(N1,N2)   = 1352
```

---

## 4. 如果找到 `4/4`，怎么还原到单位正方形坐标

从几何定义取整数 `u,v,n`：

```text
x = u/n
y = v/n

A  = |u|
B  = |u - n|
N1 = |v|
N2 = |v - n|
```

四个角距离为：

```text
sqrt(A^2  + N1^2) / n      corner (0,0)
sqrt(B^2  + N1^2) / n      corner (1,0)
sqrt(B^2  + N2^2) / n      corner (1,1)
sqrt(A^2  + N2^2) / n      corner (0,1)
```

`n` 由闭合关系给出，是两个集合的公共值：

```text
n in {A+B, |A-B|} ∩ {N1+N2, |N1-N2|}
```

还原 `u`：

```text
若 A+B = n:
    u = A                   # 0 <= x <= 1

若 |A-B| = n 且 A > B:
    u = A                   # x > 1

若 |A-B| = n 且 A < B:
    u = -A                  # x < 0
```

还原 `v` 同理：

```text
若 N1+N2 = n:
    v = N1                  # 0 <= y <= 1

若 |N1-N2| = n 且 N1 > N2:
    v = N1                  # y > 1

若 |N1-N2| = n 且 N1 < N2:
    v = -N1                 # y < 0
```

本脚本默认用 `A < B`、`N1 <= N2` 的 canonical 方向。因此：

| relation | coordinates under current orientation |
|---|---|
| `sum=A+B` | `x=A/(A+B)`, `y=N1/(A+B)` |
| `sum=|A-B|` | `x=-A/(B-A)`, `y=N1/(B-A)` |
| `diff=A+B` | `x=A/(A+B)`, `y=-N1/(A+B)` |
| `diff=|A-B|` | `x=-A/(B-A)`, `y=-N1/(B-A)` |

如果一个真实 `4/4` hit 出现，按上表即可得到单位正方形坐标系里的有理点。然后再约分 `x,y`。

边界备注：当前 closure-first 探针没有覆盖 `A=B` 的中心竖线情形，因为共同 `N` pair 生成时只取两条不同腿 `(A,B)`。这不是速度优化导致的漏判，而是当前实验口径。若要把 closure-first 探针改成完整坐标系枚举，需要另加便宜的一维分支：

```text
A = B
N1 + N2 = 2A
A^2 + N1^2, A^2 + N2^2 为平方
```

`N1=N2` 的中心横线情形可以由现有 sum relation 生成，但 D4-canonical 去重时也要保留等号情况。

---

## 5. 对称性怎么砍

单位正方形的 D4 对称群会作用在 `(A,B,N1,N2)` 上：

| square symmetry | effect on legs |
|---|---|
| reflect left-right | swap `A,B` |
| reflect up-down | swap `N1,N2` |
| swap axes (`x,y`) | swap pair `(A,B)` with `(N1,N2)` |

当前脚本已经用了两层弱 canonical：

```text
A < B
N1 <= N2
```

这等价于先用左右反射、上下反射，把点放进一个固定半平面方向。它没有用 axis-swap。因此数据里还会出现转置对：

```text
(A,B,N1,N2) = (7,45,24,28)
(A,B,N1,N2) = (24,28,7,45)
```

这两个样本通过 `x,y` 对调互相对应。它们不该在结构统计里算作完全独立模板。

下一步可以加一个 D4 canonical key：

```text
take all transforms:
  (A,B,N1,N2)
  (B,A,N1,N2)
  (A,B,N2,N1)
  (B,A,N2,N1)
  (N1,N2,A,B)
  (N2,N1,A,B)
  (N1,N2,B,A)
  (N2,N1,B,A)

for each transform, reorient so first pair is increasing and second pair is increasing;
choose lexicographically smallest tuple.
```

这会把 41,736 个 `3/4` near-miss 缩成 D4-orbit 模板集。更重要的是，delta `1..10` 的那些小样本里已经能看到明显转置：

```text
(13,112,15,84)  <->  (15,84,13,112)
(7,45,24,28)    <->  (24,28,7,45)
(260,2240,300,1680) <-> (300,1680,260,2240)
```

所以后续统计应该同时保留两套数：

```text
raw near-miss count
D4-canonical template count
```

raw count 看搜索密度，canonical count 看真正结构族。

### 5.1 D4 point 去重结果

已在 `closure_first_three_square_search.py` 增加坐标系层面的去重统计：

```text
max_leg=100000
diff_tail=250000

raw 3/4 near-miss records:          41,736
same coordinate points:                857
D4-distinct coordinate point orbits:   480
exact 4/4 hits:                          0
```

这里分三层：

```text
raw records
  = 搜索枚举到的整数包装；同一个点的整数倍会重复出现。

same coordinate points
  = 先还原到单位正方形坐标 (x,y)，所以整体倍数重复被合并。

D4-distinct coordinate point orbits
  = 再把正方形旋转/翻转得到的点合并。
```

所以这批 `41,736` 个 near-miss 在正方形坐标系里实际只有 `857` 个不同点；如果把正方形的 D4 对称也视为同一个结构，则只剩 `480` 个轨道。

delta `1..10` 在 D4 point 层面的分布：

```text
delta=1:   1
delta=6:   3
delta=7:   3
delta=8:   2
delta=9:   1
delta=10:  3
```

空缺仍然存在：`delta=2..5` 没有出现。

---

## 6. 下一步

优先顺序：

1. 对 signed delta 做模小素数/素数平方统计，先看 `square+1` 与 `square-d` 是否分属不同 residue class。
2. 对 delta-1 样本 `(17745,53911,60840,132496)` 单独建 mini note，分解四条边、gcd、primitive triples。
3. `A=B` 中心竖线分支已在 wl106 里接到已知 midline theorem；后续只需写本地 proof note，不必先扩实验。
4. 如果出现 `4/4`，立即按 §4 坐标公式还原 `(x,y)` 并生成 D4 orbit，确认它不是同一个点的反射/旋转重复。

---

## 7. 涉及文件

```text
scripts/theory/closure_first_three_square_search.py
scripts/theory/plot_closure_first_d4_points.py
tests/test_closure_first_three_square_search.py
tests/test_plot_closure_first_d4_points.py
docs/explorations/2026-06-07-next-step-hard-layer/closure-first-3of4.md
docs/explorations/2026-06-07-next-step-hard-layer/commands-run.md
docs/explorations/2026-06-07-next-step-hard-layer/README.md
results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast.json
results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast_d4points.json
results/counterexample_first/2026-06-07/closure_first_3of4_d4_points_max100000_tail250000.png
```
