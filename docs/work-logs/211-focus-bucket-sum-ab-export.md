# wl211 — focus export for first shared-role bucket

日期：2026-06-09

## 1. 本轮目标

wl210 选出了 raw_count 第一的 shared-role 桶：

```text
B:odd_leg+odd_leg|N1:even_leg+even_leg
```

这个桶总计：

```text
raw_count = 7240
D4 points = 38
missing = A-N2 for all 38 points
```

本轮继续收窄：

```text
只看 relation=sum=A+B 的子桶。
```

普通话说：

```text
先别把四种 closure 关系混在一起。
先拿最直观的一种：

N1 + N2 = A + B

它就是小样本 (7,45,24,28) 所在形状。
```

---

## 2. 代码变化

修改：

```text
scripts/theory/summarize_closure_first_d4_invariants.py
tests/test_summarize_closure_first_d4_invariants.py
```

新增参数：

```text
--focus-pattern
--focus-relation
```

summary 新增：

```text
focus
focus_records
```

`focus_records` 会按：

```text
best_failed_nearest_delta asc
raw_count desc
side_n asc
x,y
```

排序。

普通话说：

```text
这就是“把要下手的桶捞出来”，不用每次手动翻 JSON。
```

---

## 3. 真实数据运行

已运行：

```text
uv run python scripts/theory/summarize_closure_first_d4_invariants.py \
  results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast_d4points.json \
  --out results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_d4_invariants_focus_bucket.json \
  --focus-pattern 'B:odd_leg+odd_leg|N1:even_leg+even_leg' \
  --focus-relation 'sum=A+B'
```

输出：

```text
records=480
uv_pair_groups=480
low_delta_records=9
```

focus 摘要：

```text
pattern = B:odd_leg+odd_leg|N1:even_leg+even_leg
relation = sum=A+B
record_count = 4
raw_count = 5820
```

结果文件在 `results/` 下，不提交。

---

## 4. Focus records

| delta | raw_count | x | y | sample | missing |
|---:|---:|---|---|---|---|
| 8 | 5793 | `7/52` | `6/13` | `(7,45,24,28)` | `A-N2` |
| 1056 | 22 | `49/348` | `910/2871` | `(1617,9867,3640,7844)` | `A-N2` |
| 13689 | 4 | `13/5500` | `1711/12375` | `(117,49383,6844,42656)` | `A-N2` |
| 26325 | 1 | `1771/10750` | `29939/129000` | `(29939,99061,21252,107748)` | `A-N2` |

观察：

```text
这个子桶非常集中。
4 个 D4 点里，小样本 (7,45,24,28) 一点占 raw_count=5793。
整个子桶 raw_count=5820。
```

普通话说：

```text
如果先做 relation=sum=A+B，
其实就是先研究小样本所在的强重复家族。
```

---

## 5. 下一步方程模板

这个 focus 子桶固定：

```text
pattern:
  B: odd_leg + odd_leg
  N1: even_leg + even_leg

relation:
  N1 + N2 = A + B

missing:
  A-N2
```

模板：

```text
A  = u*(p^2-q^2)
N1 = u*(2pq)

B  = v*(r^2-s^2)
N1 = v*(2rs)

B  = w*(x^2-y^2)
N2 = w*(2xy)

N1 + N2 = A + B

question:
  can A^2 + N2^2 be a square?
```

小样本对应：

```text
A  = 1*(4^2-3^2)
N1 = 1*(2*4*3)

B  = 3*(4^2-1^2)
N1 = 3*(2*4*1)

B  = 1*(7^2-2^2)
N2 = 1*(2*7*2)
```

失败边：

```text
A^2 + N2^2 = 7^2 + 28^2 = 833
29^2 = 841
delta = -8
```

---

## 6. 边界

可以说：

```text
第一 shared-role 桶的 sum=A+B 子桶已经被明确导出。
它是一个非常集中的理论入口。
```

不能说：

```text
研究这个子桶就能覆盖全部第一 shared-role 桶。
```

原因：

```text
第一 shared-role 桶有 38 个 D4 点。
sum=A+B 子桶只有 4 个 D4 点。
其他 relation 仍需分别处理。
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
14 passed
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
