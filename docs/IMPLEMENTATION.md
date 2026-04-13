# 实现参考文档

本文档描述当前代码结构、`parametric` 主线的执行方式，以及 CPU 开发机和 AMD APU 主力机如何共用同一套判定逻辑。数学推导见 [MATH.md](MATH.md)。

---

## 一、模块结构

```text
src/rational_distance/
├── __init__.py           — 包入口
├── math_utils.py         — 有理平方根、本原勾股数生成
├── square.py             — RationalPoint、D4 对称、距离计算
├── backend.py            — numpy / torch / cupy 后端检测与薄封装
├── parametric_core.py    — parametric 共享判定核心（唯一真理源）
├── search.py             — CPU 编排层：多进程、汇总、兼容旧接口
├── search_gpu.py         — APU/GPU 编排层：设备数组执行 + 自动精确回退
└── search_ec.py          — 椭圆曲线引导搜索（本轮未重构）

scripts/
├── search.py             — 统一 CLI 入口
├── compare_parametric.py — CPU vs 加速后端对照工具
└── visualize.py          — Plotly HTML 可视化

tests/
└── test_all.py           — 统一测试套件（当前 51 个用例）
```

---

## 二、参数与命令习惯

### 2.1 `--scale` 仍然是主入口

主搜索命令仍推荐用：

```bash
uv run python scripts/search.py parametric --scale 200
```

含义仍然是：

```text
max_m     = N
max_k_den = 4 * N
max_k_num = 8 * N
```

如果同时传了显式参数，则显式参数优先，没写的部分继续沿用 `--scale` 推导出的默认值。

### 2.2 CPU 和 APU 共用一套命令心智

- 开发机 CPU：默认 `auto` 会回落到 `numpy`
- 主力机 AMD APU：默认 `auto` 会优先尝试 `torch`

也就是说，大多数情况下你可以先记这一条：

```bash
uv run python scripts/search.py parametric --scale 200
```

只有在你想强制指定后端时，才补：

```bash
--backend numpy   # 强制 CPU
--backend torch   # 强制 AMD APU / ROCm
```

### 2.3 对照工具也支持 `--scale`

为了避免再记一套参数，`compare_parametric.py` 也支持：

```bash
uv run python scripts/compare_parametric.py --scale 20 --backend torch
```

它默认会：

1. 用 CPU 基线跑一遍
2. 用指定加速后端再跑一遍
3. 对比点集、D4 去重数量、耗时和 exact fallback 统计

---

## 三、`parametric` 主线现在怎么工作

### 3.1 只维护一套判定逻辑

本轮重构后，`parametric_core.py` 是唯一真理源，里面统一定义了：

- 候选过滤：side-exclusion、`inside_only`
- 三个判定式：`tB` / `tC` / `tD`
- 完全平方预筛：统一保留 `s+1` 修正
- `int64` 安全边界：`safe_r_max(...)`
- Python 大整数精确判定：作为所有后端的最终参考答案
- 命中结果的归一化、去重键、排序规则

这意味着以后再加剪枝或改判定规则，不需要同时维护 CPU 一份、APU 一份。

### 3.2 CPU 路径只负责编排

`search.py` 现在主要负责：

- 生成本原勾股数
- 预建 `(a, b)` 互素对
- 通过 `ProcessPoolExecutor` 把 triple 分发到多个 CPU worker
- 收集原始命中并统一去重

真正的数学判断已经下沉到 `parametric_core.py`。

### 3.3 APU/GPU 路径只负责加速执行

`search_gpu.py` 现在主要负责：

- 把 `(a, b)` 数组搬到 `torch` / `cupy` / `numpy`
- 在安全范围内调用共享向量化判定
- 超过 `safe_r_max` 时自动切回共享的 Python 精确判定

这点和旧实现最大的区别是：

- 以前：高规模时可能“报警但继续算”
- 现在：高规模时会自动精确回退，结果优先保证正确

### 3.4 共享运行统计

`ParametricRunStats` 会同时记录：

- triple 总数
- 每个 triple 的候选 `(a, b)` 对数量
- `safe_r_max`
- 触发 exact fallback 的 triple 数量

CPU 基线、APU 加速、对照脚本都复用这套统计结构。

### 3.5 架构护栏：避免再次分叉实现

`parametric` 这一层现在有一个明确约束：

- 任何新的筛选条件、判定式、overflow 规则、exact fallback 规则，只能改 `parametric_core.py`
- `search.py` 只管 CPU 编排
- `search_gpu.py` 只管后端执行

如果以后在 `search.py` 或 `search_gpu.py` 里重新长出一套 `tB / tC / tD` 判定逻辑，等于把这轮重构推翻了。后续开发应把这种改动视为架构回退，而不是普通重构。

---

## 四、为什么这样更适合开发

这个项目的难点不在“代码很多”，而在“公式和筛选条件很严谨，一旦分叉就容易漏改”。

现在的开发流程推荐是：

1. 先在开发机 CPU 上改逻辑
2. 跑 `pytest`
3. 跑 `compare_parametric.py`
4. 再去主力机上用 `--backend torch` 跑更大范围

这样 CPU 负责“确认没改错”，APU 负责“用同一套规则跑得更快”。

---

## 五、exact fallback 规则

### 5.1 安全边界

共享安全边界使用：

```python
safe_r_max = (2**31 - 1) // (max_k_num + 2 * max_k_den)
```

这个界限是按 `tC = (ar - b(p+q))² + (b(p-q))²` 的最坏情况推出来的，用来保证 `int64` 路径不会静默溢出。

### 5.2 回退策略

对于每个 triple：

- 如果 `r <= safe_r_max`：走向量化快路径
- 如果 `r > safe_r_max`：走 Python 任意精度整数精确路径

CPU 和 APU 都遵守这个规则，只是前者在 CPU 上做快路径，后者在设备数组上做快路径。

---

## 六、测试与验算

当前测试除了原有功能覆盖，还新增了三类护栏：

### 6.1 共享核心测试

- `safe_r_max(...)` 是否符合统一公式
- 完全平方预筛在边界值附近是否与精确 `isqrt` 一致

### 6.2 CPU / 加速后端一致性测试

- `parametric_search_gpu(xp=np)` 与 CPU 基线点集一致
- 强制 exact fallback 时，CPU 和加速包装层仍然一致

### 6.3 对照脚本 smoke test

- `compare_parametric.py` 能运行
- 小范围下对称差应为 0

---

## 七、Ruff 工具链

当前代码质量工具统一使用 `ruff`：

```bash
uv run ruff check .
uv run ruff format .
```

默认启用的规则族：

- `E`, `F`, `W`, `I`, `UP`, `B`, `SIM`, `C4`, `PIE`, `RET`, `RUF`

为了避免数学符号文案带来过多噪音，当前忽略：

- `RUF001`
- `RUF002`

另外对少数文件做了局部豁免：

- `scripts/visualize.py`：忽略 `E501`
- `tests/test_all.py`：忽略 `E402`

这套配置的目标不是“把所有风格都卡死”，而是让重构和后续优化时，能尽早发现真实代码问题。

---

## 八、`EC` 路径当前状态

这轮只重构了 `parametric` 主线。

`search_ec.py` 仍然保持现有结构，包括：

- seed-finding 的 numpy / GPU 分支
- `QuarticEC` 的弦切法轨道展开
- Fraction 精确运算的四顶点检验

也就是说，`EC` 目前还没有像 `parametric` 那样完全收成“单一逻辑源 + 多后端执行壳”。如果以后要继续做结构统一，建议优先复用 `parametric_core.py` 中那些低风险公共小工具，而不是一次性重写整个 `EC` 层。
