# wl064 — 公共并行层复用进程池与流式回调

## 触发

用户提出一个很具体的工程问题：`src/rational_distance/parallel.py` 已经成了公共并行层，很多脚本都在调用它，但在 mac 上感觉并行并没有想象中快，希望判断瓶颈到底在不在这个公共层本身，以及能不能在**尽量少改调用方**的前提下提速。

专项检查后，先确认了两个明显问题：

1. `parallel_map(...)` 无论调用方是否真的需要，都会把结果完整攒回主进程。
2. `partner_full_bfs.py` 这类脚本在循环里每轮都 `cfg.map(...)` 一次，会反复创建 / 销毁 `spawn` 单任务子进程池；在 mac 上这笔固定成本很贵。

## 本次改动

### 1. 公共并行层新增两条低风险优化

`src/rational_distance/parallel.py` 现在新增：

- `collect_results=False`
  - 适合只靠 `on_result` 回调做进度汇报、写文件、累积统计的脚本
  - 这样主进程不再额外保留一整份结果列表
- `ParallelExecutor`
  - 通过 `ParallelConfig.executor()` 暴露
  - 适合“循环里反复并行一小批任务”的脚本
  - 效果是复用同一个 `spawn` 单任务子进程池，而不是每轮重新建池

另外，`parallel_map(...)` 也去掉了原来一上来就 `list(items)` 的做法，避免在公共层提前把输入整体物化。

### 2. 调用方接入

#### `scripts/partner_full_bfs.py`

从：

- 每轮 `cfg.map(_compute_ns, batch)`

改为：

- `with cfg.executor() as executor:`
- 每轮 `executor.map(_compute_ns, batch)`

这是本次最关键的调用点，因为它正好符合“多轮、小批、循环反复 map”的高开销模式。

#### `scripts/full_gm_closure_scan.py`

原脚本只通过 `on_result`：

- 更新计数
- 累积命中
- 打进度

并不需要完整返回列表，所以改成：

- `cfg.map(..., on_result=on_result, collect_results=False)`

#### `scripts/k10_extract_and_ellrank.py`

同样只靠 `on_result` 收集高 `k` 顶点，也改成：

- `cfg.map(..., on_result=on_result, collect_results=False)`

### 3. 基准脚本

新增：

- `scripts/benchmark_parallel_executor.py`

用途：比较两种真实写法的成本差：

1. 每批都重新 `cfg.map(...)`
2. 外层先拿 `executor`，批次之间复用进程池

它直接复用 `partner_full_bfs.py` 的 `_compute_ns` 负载，所以结论对 BFS 场景比较有代表性。

## 基准结果

### 小样本：`max2000`，133 对，9 批

```text
cfg.map mean:   0.373s
executor mean:  0.063s
speedup mean:   x5.90
```

### 中样本：`max20000`，640 对，40 批

```text
cfg.map mean:   1.735s
executor mean:  0.190s
speedup mean:   x9.13
```

### 更大样本：`max20000`，1280 对，80 批

```text
cfg.map mean:   3.541s
executor mean:  0.384s
speedup mean:   x9.21
```

## 结论

### 1. 主瓶颈不是单个任务计算，而是“每批固定建池成本”

从三组数据看，`cfg.map` 和 `executor` 的差值基本按批次数近似线性增长：

- 9 批：差 `0.310s`
- 40 批：差 `1.545s`
- 80 批：差 `3.157s`

折算下来，约等于**每批固定多付 39ms 左右**，这正是反复 `spawn` / 进程初始化 / 回收的代价。

### 2. `partner_full_bfs.py` 是本次优化的最大受益者

因为它正好是：

- 多轮
- 小批
- 每轮都并行

这类脚本最适合复用进程池。

### 3. `collect_results=False` 更像“降内存 + 降主进程汇总开销”

对 `full_gm_closure_scan.py`、`k10_extract_and_ellrank.py` 这类一次性大扫描脚本，这条改动的主要价值是：

- 少一份无意义的大列表
- 减轻主进程内存与汇总压力

它们不一定像 BFS 那样拿到接近 `x9` 的加速，但这是零风险的正确默认写法。

## 验证

```bash
uv run pytest tests/test_parallel.py -q
uv run python -m py_compile \
    src/rational_distance/parallel.py \
    scripts/partner_full_bfs.py \
    scripts/full_gm_closure_scan.py \
    scripts/k10_extract_and_ellrank.py \
    scripts/benchmark_parallel_executor.py

uv run python scripts/benchmark_parallel_executor.py
uv run python scripts/benchmark_parallel_executor.py \
    --data results/multi_concordant_N_max20000_fast.jsonl --pairs 640
uv run python scripts/benchmark_parallel_executor.py \
    --data results/multi_concordant_N_max20000_fast.jsonl --pairs 1280
```

结果：

- `tests/test_parallel.py`：16 passed
- `py_compile`：通过
- 基准结果稳定复现：BFS 风格负载下复用进程池约 `x6` 到 `x9` 加速

## 文件变更

| 文件 | 变更 |
|------|------|
| `src/rational_distance/parallel.py` | 新增 `ParallelExecutor`、`collect_results=False`、流式输入路径 |
| `tests/test_parallel.py` | 新增“复用进程池”“不收集结果”测试 |
| `scripts/partner_full_bfs.py` | 改为复用同一个进程池 |
| `scripts/full_gm_closure_scan.py` | 改为 `collect_results=False` |
| `scripts/k10_extract_and_ellrank.py` | 改为 `collect_results=False` |
| `scripts/benchmark_parallel_executor.py` | 新增并行层基准脚本 |
| `docs/IMPLEMENTATION.md` | 补充公共并行层的推荐用法 |
| `docs/CURRENT_FINDINGS.md` | 记录“循环式 map 主瓶颈是反复建池”的工程结论 |

## 后续

如果以后继续做并行优化，优先顺序建议是：

1. 先找“循环里反复 `cfg.map(...)`”的调用点，优先改成 `executor`
2. 再找“只靠 `on_result` 汇总”的脚本，统一加 `collect_results=False`
3. 最后才考虑更重的方向，比如把热点计算挪到原生代码或 JIT
