# wl204 — D4 invariant coordinate summary

日期：2026-06-09

## 1. 本轮目标

wl106 画了 480 个 D4 代表点，但肉眼没有明显规律。

本轮把图换成不变量表：

```text
x(1-x)
y(1-y)
{x(1-x), y(1-y)}
sum/product
A+B, |A-B|, N1+N2, |N1-N2|
```

普通话说：

```text
不再盯着散点图看。
把每个点换成 D4 不变量，
看它们会不会自动合并成更少的家族。
```

---

## 2. 新脚本

新增：

```text
scripts/theory/summarize_closure_first_d4_invariants.py
```

输入：

```text
closure_first_three_square_search.py --include-d4-points
```

生成的 JSON，也就是包含：

```text
d4_point_records
```

的文件。

输出字段包括：

```text
record_count
raw_count_total
uv_pair_group_count
relation_counts
missing_edge_counts
uv_pair_groups_top
low_delta_records
top_invariant_records
```

其中：

```text
u = x(1-x)
v = y(1-y)
uv_pair = sorted(u, v)
```

这个 `uv_pair` 对 D4 旋转/翻转不变。

---

## 3. 本轮命令

已运行：

```text
uv run python scripts/theory/summarize_closure_first_d4_invariants.py \
  results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast_d4points.json \
  --out results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_d4_invariants.json
```

输出：

```text
records=480
uv_pair_groups=480
low_delta_records=9
```

注意：

```text
results/ 在本机 .git/info/exclude 中被忽略。
结果文件不提交，只记录命令和摘要。
```

---

## 4. 主要结论

第一，最自然的 D4 不变量没有进一步合并点：

```text
D4 point records = 480
uv_pair groups   = 480
```

这说明：

```text
480 个 D4 点在 {x(1-x), y(1-y)} 层面仍然全不同。
```

普通话说：

```text
这批点不是“同一个不变量家族被 D4 图没看出来”。
至少这个最便宜的不变量没有发现大合并。
```

第二，按 D4 点计数，关系分布是：

| relation | D4 points |
|---|---:|
| `diff=A+B` | 179 |
| `diff=|A-B|` | 152 |
| `sum=A+B` | 84 |
| `sum=|A-B|` | 65 |

外侧差关系仍然占大头。

第三，缺边分布是：

| missing edge | D4 points |
|---|---:|
| `A-N2` | 175 |
| `B-N1` | 116 |
| `B-N2` | 108 |
| `A-N1` | 81 |

这比 raw near-miss 分布更偏向 `A-N2`。

---

## 5. 低 delta D4 点

`delta <= 10` 的 D4 点只有 9 个：

| delta | x | y | relation | missing | side_n | sample |
|---:|---|---|---|---|---:|---|
| 1 | `-45/53` | `105/424` | `diff=A+B` | `B-N2` | 71656 | `(17745,53911,60840,132496)` |
| 6 | `-13/99` | `5/33` | `sum=|A-B|` | `A-N1` | 99 | `(13,112,15,84)` |
| 6 | `-13/15` | `-7/9` | `diff=|A-B|` | `A-N1` | 225 | `(175,400,195,420)` |
| 6 | `-27/1121` | `83/3363` | `sum=|A-B|` | `A-N1` | 3363 | `(81,3444,83,3280)` |
| 7 | `-252/299` | `-240/299` | `diff=|A-B|` | `B-N2` | 8671 | `(6960,15631,7308,15979)` |
| 8 | `7/52` | `6/13` | `sum=A+B` | `A-N2` | 52 | `(7,45,24,28)` |
| 8 | `-5/37` | `49/148` | `sum=|A-B|` | `A-N1` | 148 | `(20,168,49,99)` |
| 10 | `-4/17` | `16/51` | `sum=|A-B|` | `B-N2` | 51 | `(12,63,16,35)` |
| 10 | `-48/97` | `-17/291` | `diff=|A-B|` | `A-N2` | 873 | `(51,924,432,1305)` |

这些点有两个用途。

第一，`delta=1` 仍是唯一最尖样本。

第二，raw_count 最大的几个点也在这个表里：

```text
(7/52, 6/13)       raw_count=5793, delta=8
(-4/17, 16/51)     raw_count=4444, delta=10
(-13/15, -7/9)     raw_count=2440, delta=6
(-13/99, 5/33)     raw_count=2082, delta=6
(-5/37, 49/148)    raw_count=1605, delta=8
```

所以后续方程化不必只盯着 `delta=1`。高重复低 delta 点更像家族入口。

---

## 6. 对路线的影响

可以说：

```text
D4 图没有肉眼规律后，D4 不变量表也没有发现大规模合并。
但它筛出了 9 个低 delta D4 点和几个高 raw_count 家族入口。
```

不能说：

```text
D4 不变量路线已经失败。
480 点没有任何代数结构。
```

因为：

```text
本轮只试了 x(1-x), y(1-y) 这组最便宜的不变量。
还没试 squareclass、模类、分母因子、Pythagorean 参数。
```

普通话总结：

```text
这条路没有一刀砍出规律。
但它告诉我们：下一步该挑点方程化，而不是再整体聚类。
```

---

## 7. 建议下一步

优先方程化这三个点：

```text
1. delta=1:
   (A,B,N1,N2)=(17745,53911,60840,132496)

2. high raw_count + inside sum:
   (A,B,N1,N2)=(7,45,24,28)

3. high raw_count + outside sum:
   (A,B,N1,N2)=(12,63,16,35)
```

要写的不是“更多统计”，而是：

```text
三条已过勾股边的参数。
第四条失败边的平方差。
closure 关系怎样把参数绑住。
delta 为什么落到 1 / 8 / 10。
```

如果这些小点能写成同一类参数模板，再回头看 480 点表。

---

## 8. 验证

RED：

```text
uv run pytest tests/test_summarize_closure_first_d4_invariants.py -q
```

先失败于模块不存在。

GREEN：

```text
uv run pytest tests/test_summarize_closure_first_d4_invariants.py -q
```

结果：

```text
3 passed
```

相关测试：

```text
uv run pytest tests/test_plot_closure_first_d4_points.py tests/test_closure_first_three_square_search.py -q
```

结果：

```text
8 passed
```
