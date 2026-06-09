# wl209 — D4 shared-variable pattern summary

日期：2026-06-09

## 1. 本轮目标

wl208 只看了一个小样本 `(7,45,24,28)`，发现 near-miss 可以看成共享变量网络。

本轮把这个结构接到 D4 invariant summary 上，批量问：

```text
480 个 D4 代表点里，
共享变量角色模式是否集中？
```

普通话说：

```text
不要只看一个点里 B 和 N1 被重复生成。
看看所有 near-miss 点是不是也都有类似“公共接口”。
```

---

## 2. 代码变化

修改：

```text
scripts/theory/summarize_closure_first_d4_invariants.py
tests/test_summarize_closure_first_d4_invariants.py
```

每个 invariant record 现在新增：

```text
shared_variable_roles
shared_role_pattern
```

总 summary 现在新增：

```text
shared_role_pattern_counts
```

含义：

```text
shared_variable_roles:
  B:  [odd_leg, odd_leg]
  N1: [even_leg, even_leg]

shared_role_pattern:
  B:odd_leg+odd_leg|N1:even_leg+even_leg
```

注意：

```text
这是角色模式，不是完整参数。
它只看共享变量分别是 odd leg 还是 even leg。
```

---

## 3. CLI 入口修复

本轮还修了一个入口问题。

之前：

```text
uv run pytest tests/test_summarize_closure_first_d4_invariants.py
```

可以通过，因为测试文件把 repo root 加进了 `sys.path`。

但直接运行：

```text
uv run python scripts/theory/summarize_closure_first_d4_invariants.py ...
```

会失败：

```text
ModuleNotFoundError: No module named 'scripts'
```

原因：

```text
直接执行脚本时，Python 默认把 scripts/theory 当作入口目录，
不会自动把 repo root 加进 import path。
```

已补一个 subprocess 测试覆盖真实 CLI 入口，并在脚本中显式加入 repo root。

---

## 4. 真实数据运行

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

结果文件在 `results/` 下，仍按仓库规则不提交。

---

## 5. 共享角色模式分布

480 个 D4 点里没有 `none`。

普通话说：

```text
每个 3/4 near-miss D4 代表点，
都至少有两个变量被多条已通过边共享。
```

但模式不是单一的，共有 16 类。出现最多的几类：

| count | shared_role_pattern |
|---:|---|
| 49 | `B:even_leg+even_leg|N1:odd_leg+odd_leg` |
| 45 | `B:even_leg+even_leg|N1:even_leg+odd_leg` |
| 43 | `B:odd_leg+even_leg|N1:even_leg+even_leg` |
| 39 | `A:odd_leg+odd_leg|N1:even_leg+even_leg` |
| 39 | `A:odd_leg+odd_leg|N2:even_leg+even_leg` |
| 38 | `B:odd_leg+odd_leg|N1:even_leg+even_leg` |

所以：

```text
共享变量结构是普遍现象。
但不是一个模式吃掉全部 near-miss。
```

---

## 6. 低 delta 点

`delta <= 10` 的 9 个 D4 点：

| delta | raw_count | pattern | relation | missing | sample |
|---:|---:|---|---|---|---|
| 1 | 440 | `A:odd_leg+odd_leg|N1:even_leg+even_leg` | `diff=A+B` | `B-N2` | `(17745,53911,60840,132496)` |
| 6 | 2082 | `B:even_leg+even_leg|N2:odd_leg+even_leg` | `sum=|A-B|` | `A-N1` | `(13,112,15,84)` |
| 6 | 2440 | `B:even_leg+even_leg|N2:odd_leg+even_leg` | `diff=|A-B|` | `A-N1` | `(175,400,195,420)` |
| 6 | 59 | `B:even_leg+odd_leg|N2:even_leg+even_leg` | `sum=|A-B|` | `A-N1` | `(81,3444,83,3280)` |
| 7 | 366 | `A:even_leg+even_leg|N1:odd_leg+even_leg` | `diff=|A-B|` | `B-N2` | `(6960,15631,7308,15979)` |
| 8 | 5793 | `B:odd_leg+odd_leg|N1:even_leg+even_leg` | `sum=A+B` | `A-N2` | `(7,45,24,28)` |
| 8 | 1605 | `B:even_leg+even_leg|N2:odd_leg+odd_leg` | `sum=|A-B|` | `A-N1` | `(20,168,49,99)` |
| 10 | 4444 | `A:odd_leg+even_leg|N1:even_leg+even_leg` | `sum=|A-B|` | `B-N2` | `(12,63,16,35)` |
| 10 | 553 | `B:odd_leg+even_leg|N1:even_leg+even_leg` | `diff=|A-B|` | `A-N2` | `(51,924,432,1305)` |

观察：

```text
低 delta 点也分散在多个角色模式里。
但高 raw_count 的入口点仍然都能被 shared-variable network 表达。
```

---

## 7. 对下一步的意义

可以说：

```text
D4 视觉图没看出规律，
但 shared-variable 视角确认了一个更代数的共同结构：
3/4 near-miss 普遍是两个共享变量接口组成的小网络。
```

不能说：

```text
某一个 shared_role_pattern 已经足以覆盖所有 near-miss。
```

下一步更合理的路线：

```text
按 shared_role_pattern 分桶，
每次只方程化一个桶。
```

优先桶可以选：

```text
B:odd_leg+odd_leg|N1:even_leg+even_leg
```

原因：

```text
它包含高 raw_count 小样本 (7,45,24,28)，
方程最容易手算，
并且模式清楚：一个变量两次 odd_leg，另一个变量两次 even_leg。
```

---

## 8. 验证

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
