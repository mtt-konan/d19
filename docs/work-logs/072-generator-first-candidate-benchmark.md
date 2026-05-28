# Worklog 072: Generator-first candidate benchmark

## 目标

本记录对应实验线 B：比较直接整数域上的候选生成器。

直接整数域定义为：

```text
1 <= A < B <= max_hyp
gcd(A, B) = 1
```

这不是当前 `proof_status --max-hyp` 使用的三元组斜边域。当前 `proof_status` 的 `max_hyp` 约束的是本原勾股三元组的斜边，不是直接约束 `A` 和 `B` 都小于等于 `max_hyp`。

## 对比对象

```text
all_coprime   直接枚举所有互素整数 pair
safe_coprime  all_coprime 经过 safe_sieve（安全前筛）后的 survivor（剩余候选）
multi_n       pivot-on-N（以 N 为枢轴）直接生成 multi-N（多 N）pair
```

`multi_n` 使用已有的 `fast_multi_concordant_pairs(max_hyp)`。它生成时已经携带每个 pair 的 concordant_N 列表，因此后续不需要再对这些 pair 跑 `concordant_search` 或 `multi_n_sieve`。

## 命令

```bash
uv run python scripts/benchmark_candidate_generators.py --max-hyp 200 --json-out results/candidate_generators_max200.json
uv run python scripts/benchmark_candidate_generators.py --max-hyp 2000 --json-out results/candidate_generators_max2000.json
uv run python scripts/benchmark_candidate_generators.py --max-hyp 10000 --json-out results/candidate_generators_max10000.json
uv run python scripts/benchmark_candidate_generators.py --max-hyp 20000 --json-out results/candidate_generators_max20000.json
uv run python scripts/benchmark_candidate_generators.py --max-hyp 50000 --only multi_n --json-out results/candidate_generators_max50000_multi_n.json
uv run python scripts/benchmark_candidate_generators.py --max-hyp 100000 --only multi_n --json-out results/candidate_generators_max100000_multi_n.json
```

## 结果：max_hyp=200

```text
name          max_hyp      pairs  elapsed_s  carries_N  min_k  max_k
------------  -------  ---------  ---------  ---------  -----  -----
all_coprime       200      12231      0.001      False      -      -
safe_coprime      200       2040      0.002      False      -      -
multi_n           200          7      0.001       True      2      2
```

## 结果：max_hyp=2000

```text
name          max_hyp      pairs  elapsed_s  carries_N  min_k  max_k
------------  -------  ---------  ---------  ---------  -----  -----
all_coprime      2000    1216587      0.123      False      -      -
safe_coprime     2000     202713      0.190      False      -      -
multi_n          2000        133      0.047       True      2      3
```

## 结果：max_hyp=10000

```text
name          max_hyp      pairs  elapsed_s  carries_N  min_k  max_k
------------  -------  ---------  ---------  ---------  -----  -----
all_coprime     10000   30397485      3.417      False      -      -
safe_coprime    10000    5065838      4.970      False      -      -
multi_n         10000        854      1.038       True      2      3
```

## 结果：max_hyp=20000

```text
name          max_hyp      pairs  elapsed_s  carries_N  min_k  max_k
------------  -------  ---------  ---------  ---------  -----  -----
all_coprime     20000  121590395     13.998      False      -      -
safe_coprime    20000   20264681     21.552      False      -      -
multi_n         20000       1848      4.113       True      2      4
```

## 更大规模 multi_n-only

50k 以上没有继续跑 `all_coprime` / `safe_coprime` 全量计数，因为它们当前实现是直接双层枚举加 gcd，复杂度是 O(H²)。例如 50k 的直接整数域互素 pair 量级约为 7.6 亿，作为确认趋势没有必要硬扫。

```text
name          max_hyp      pairs  elapsed_s  carries_N  min_k  max_k
------------  -------  ---------  ---------  ---------  -----  -----
multi_n         50000       4968     26.327       True      2      4
multi_n        100000      10333    106.732       True      2      4
```

## 关键观察

1. `all_coprime` 在 `max_hyp=10000` 的数量是 30,397,485，和 wl046 的直接整数域慢扫总 pair 数一致。
2. `safe_coprime` 把 10k 的候选从 30,397,485 压到 5,065,838，剩余比例约 16.7%。这个比例不同于当前三元组域里的安全前筛比例，说明两个域不能混用统计结论。
3. `multi_n` 直接生成 854 个 pair，和 wl046 / wl048 的 10k 多 N catalog 一致。
4. `multi_n` 的 10k 运行时间约 1 秒，并且输出自带 concordant_N 列表；在这个直接整数域 benchmark 中，它可以直接替代后筛式的 `concordant_search` + `multi_n_sieve` 组合。
5. `multi_n` 在 50k 和 100k 仍然只生成 4,968 / 10,333 个 pair，说明直接多 N 生成器的候选规模增长很慢，适合作为大范围候选入口。

## 解释

实验线 B 的目的不是替换当前 `proof_status --max-hyp` 语义，而是回答另一个问题：如果搜索域定义成 `A,B <= H` 的互素整数 pair，哪种方法最适合作为候选生成器。

在这个口径下，结论很明确：

```text
all_coprime  ->  safe_coprime  ->  multi_n
30,397,485   ->  5,065,838     ->  854      at max_hyp=10000
```

安全前筛很便宜，但只利用 2-adic（2 进）必要条件；多 N 直接生成器利用 concordant_N 结构，生成结果已经是强候选集合。

## 文件

```text
src/rational_distance/concordant/candidate_generators.py
scripts/benchmark_candidate_generators.py
tests/test_candidate_generators.py
results/candidate_generators_max200.json
results/candidate_generators_max2000.json
results/candidate_generators_max10000.json
results/candidate_generators_max20000.json
results/candidate_generators_max50000_multi_n.json
results/candidate_generators_max100000_multi_n.json
```

## 后续优化：safe 直接生成 + multi_n 因子枚举

原始 `safe_coprime` 是：

```text
all_coprime -> safe_sieve
```

优化后改成直接生成安全前筛可通过的互素 pair：

```text
A odd
B odd
A + B ≡ 0 mod 4
gcd(A, B) = 1
```

原始 `multi_n` 对每个 `A` 扫描 `p = 1..A-1`，再测试 `p | A²`。优化后先分解 `A`，生成 `A²` 的真实 divisor（因子），只遍历真实因子恢复 `N = (q-p)/2`。

### 优化后结果

```text
name          max_hyp      pairs  elapsed_s  carries_N  min_k  max_k
------------  -------  ---------  ---------  ---------  -----  -----
all_coprime     10000   30397485      3.366      False      -      -
safe_coprime    10000    5065838      0.821      False      -      -
multi_n         10000        854      0.103       True      2      3

all_coprime     20000  121590395     14.051      False      -      -
safe_coprime    20000   20264681      3.333      False      -      -
multi_n         20000       1848      0.258       True      2      4

safe_coprime    50000  126652918     23.473      False      -      -
multi_n         50000       4968      0.990       True      2      4
multi_n        100000      10333      2.489       True      2      4
```

### 优化收益

```text
safe_coprime 10k:  4.970s -> 0.821s
safe_coprime 20k: 21.552s -> 3.333s

multi_n 10k:       1.038s -> 0.103s
multi_n 20k:       4.113s -> 0.258s
multi_n 50k:      26.327s -> 0.990s
multi_n 100k:    106.732s -> 2.489s
```

### 新增结果文件

```text
results/candidate_generators_max10000_optimized.json
results/candidate_generators_max20000_optimized.json
results/candidate_generators_max50000_safe_coprime_optimized.json
results/candidate_generators_max50000_multi_n_optimized.json
results/candidate_generators_max100000_multi_n_optimized.json
```
