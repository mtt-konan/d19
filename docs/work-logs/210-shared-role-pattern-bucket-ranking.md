# wl210 — shared-role pattern bucket ranking

日期：2026-06-09

## 1. 本轮目标

wl209 已经确认：

```text
480 个 D4 near-miss 点全部有 shared-variable interface。
```

但 wl209 只有 pattern count，不够直接指导下一步。

本轮给每个 `shared_role_pattern` 分桶，统计：

```text
d4_points
raw_count
relation_counts
missing_edge_counts
best_failed_nearest_delta
example
```

普通话说：

```text
不要只问“哪类点最多”。
还要问“哪类点重复次数最多、缺哪条边、最好样本是谁”。
```

这样下一步挑桶做方程化时，不再靠感觉。

---

## 2. 代码变化

修改：

```text
scripts/theory/summarize_closure_first_d4_invariants.py
tests/test_summarize_closure_first_d4_invariants.py
```

summary 新增：

```text
shared_role_pattern_groups_top
```

排序规则：

```text
raw_count desc
d4_points desc
best_failed_nearest_delta asc
shared_role_pattern asc
```

普通话说：

```text
优先看“重复最多”的桶；
如果重复差不多，再看点数；
再看离真正命中最近的代表样本。
```

---

## 3. 真实数据运行

已运行：

```text
uv run python scripts/theory/summarize_closure_first_d4_invariants.py \
  results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast_d4points.json \
  --out results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_d4_invariants.json
```

输出仍为：

```text
records=480
uv_pair_groups=480
low_delta_records=9
```

结果文件在 `results/` 下，不提交。

---

## 4. Top buckets

按 `raw_count` 排名前几的桶：

| raw_count | D4 points | best delta | pattern | missing |
|---:|---:|---:|---|---|
| 7240 | 38 | 8 | `B:odd_leg+odd_leg|N1:even_leg+even_leg` | `A-N2` |
| 6500 | 16 | 6 | `B:even_leg+even_leg|N2:odd_leg+even_leg` | `A-N1` |
| 4541 | 18 | 10 | `A:odd_leg+even_leg|N1:even_leg+even_leg` | `B-N2` |
| 4345 | 43 | 10 | `B:odd_leg+even_leg|N1:even_leg+even_leg` | `A-N2` |
| 4210 | 39 | 13 | `A:odd_leg+odd_leg|N2:even_leg+even_leg` | `B-N1` |

第一名桶：

```text
B:odd_leg+odd_leg|N1:even_leg+even_leg
```

代表样本：

```text
(A,B,N1,N2) = (7,45,24,28)
relation = sum=A+B
missing = A-N2
delta = 8
```

这个桶的额外好处：

```text
38 个 D4 点全部 missing A-N2。
```

普通话说：

```text
这不是“某个小样本看着好玩”。
它所在的桶，是 raw_count 总量最高的桶；
而且缺边非常统一。
```

---

## 5. 下一步建议

优先方程化第一名桶：

```text
pattern:
  B:odd_leg+odd_leg
  N1:even_leg+even_leg

missing:
  A-N2
```

可以写成模板：

```text
A  = u*(p^2-q^2)
N1 = u*(2pq)

B  = v*(r^2-s^2)
N1 = v*(2rs)

B  = w*(x^2-y^2)
N2 = w*(2xy)

closure relation varies by record:
  sum=A+B / sum=|A-B| / diff=A+B / diff=|A-B|

missing test:
  A^2 + N2^2
```

更窄的第一步：

```text
只先做 relation=sum=A+B 的子桶，
也就是小样本 (7,45,24,28) 所在的最手算形状。
```

原因：

```text
closure 直接是 N1+N2=A+B。
三条过边和缺边方向都最直观。
```

---

## 6. 边界

可以说：

```text
shared-role 分桶给出了下一步理论攻击顺序。
第一桶既重复多，又缺边统一，适合方程化。
```

不能说：

```text
第一桶代表所有 near-miss。
```

原因：

```text
一共有 16 个 shared-role pattern。
第一桶只是 raw_count 最高，不是全覆盖。
```

---

## 7. 验证

已运行：

```text
uv run pytest \
  tests/test_equationize_closure_first_near_miss.py \
  tests/test_summarize_closure_first_d4_invariants.py \
  tests/test_closure_first_three_square_search.py -q
```

结果：

```text
13 passed
```

已运行：

```text
uv run ruff check \
  scripts/theory/summarize_closure_first_d4_invariants.py \
  tests/test_summarize_closure_first_d4_invariants.py
```

结果：

```text
All checks passed
```
