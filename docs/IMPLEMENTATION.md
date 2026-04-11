# 实现参考文档

本文档覆盖代码架构、搜索策略、关键优化细节和已知限制。数学推导见 [MATH.md](MATH.md)。

---

## 一、模块结构

```
src/rational_distance/
├── __init__.py          — 包入口，导出主要公共 API
├── math_utils.py        — 数学工具：有理平方根、本原勾股数生成
├── square.py            — 数据结构：RationalPoint、D4 对称、距离计算
├── backend.py           — 后端检测：CuPy / PyTorch / NumPy 自动切换
├── search.py            — 搜索引擎：三种模式 + 向量化 + 多进程
└── search_gpu.py        — GPU 加速路径（依赖 backend.py）

scripts/
├── search_gpu.py        — 唯一 CLI 入口（支持 --backend numpy/cupy/torch/auto）
└── visualize.py         — 可视化工具：从 JSON 生成 Plotly HTML 报告

tests/
└── test_all.py          — 统一测试套件（27 个用例）
```

### 各模块依赖关系

```
search.py / search_gpu.py
    └── square.py (RationalPoint, d4_images, canonical_xy)
    └── math_utils.py (primitive_pythagorean_triples)
```

---

## 二、搜索参数比例

`--scale N` 按以下比例设置三个参数：
```
max_m     = N          # 本原勾股数生成参数上限
max_k_den = 4 * N      # 比例因子 k=a/b 的分母上限
max_k_num = 8 * N      # 比例因子 k=a/b 的分子上限
```

**比例来源**：经验上，k 的最优分母大致与 max_m 同阶（4×），分子约为分母的 2 倍（因为解通常出现在 k>1 的范围）。三个参数可在 `--scale` 后面单独覆盖做非均匀搜索。

**搜索空间大小**：triple 数约 O(max_m²)，k-pair 数约 O(max_k_num × max_k_den / ln)，总组合数约 O(max_m² × max_k_num × max_k_den)，即 O(N⁴)。scale 翻倍则搜索量增加 16 倍。

---

## 三、三种搜索模式

| 模式 | 函数 | 特点 | 适用场景 |
|------|------|------|---------|
| 快速整数法 | `parametric_search_fast` | numpy 向量化 + 多进程 + 自动溢出回退 | 正式搜索（推荐） |
| Fraction 生成器 | `parametric_search` | 逐点生成，无多进程 | 小范围调试、兼容性 |
| 暴力枚举 | `brute_force_search` | 枚举所有分母 ≤ max_den 的有理点 | 小范围验证结果正确性 |

### 3.1 快速整数法数据流

```
primitive_pythagorean_triples(max_m)
    → triples list [(p, q, r), ...]
    → ProcessPoolExecutor (N workers)
        → _init_worker: 预建 (a,b) 互素对、numpy 数组
        → _worker(p, q, r):
            if r <= safe_r_max:
                _search_triple_numpy(...)   ← 主路径
            else:
                _search_triple_int(...)     ← 回退路径
    → 汇总 all_raw → 去重 → 排序 → RationalPoint 列表
```

---

## 四、Numpy 向量化

### 4.1 向量化结构

`_search_triple_numpy` 将一个三元组 (p,q,r) 对应的所有 (a,b) 对**一次性**处理：

```python
# 输入：a_arr, b_arr 均为 shape (N,) 的 int64 数组（预建，含全部互素对）
ar = a_arr * r         # shape (N,)
bp = b_arr * p
bq = b_arr * q

tB = (ar - bp)**2 + bq**2
okB, sB = _isqrt_vec(tB)   # 向量化完全平方判断

rational_count = 1 + okB + okD + okC   # d(A) 恒为 1
mask = rational_count >= min_rational
# 仅对命中点进行 Python 循环（极少数），提取结果
```

收益来源：SIMD 指令（AVX2/AVX-512）同时处理 8~16 个元素，大幅减少 Python 循环开销。

### 4.2 `_isqrt_vec` 精度处理

```python
def _isqrt_vec(t):
    s  = np.floor(np.sqrt(t.astype(np.float64))).astype(np.int64)
    ok = s * s == t
    # float64 对大整数的 sqrt 可能向下舍入 1，加 s+1 修正
    s1 = s + 1
    fix = ~ok & (s1 * s1 == t)
    ok |= fix
    s[fix] = s1[fix]
    return ok, s
```

**精度边界**：float64 的有效位数为 53 bits（约 9×10¹⁵）。对 t > 9×10¹⁵，float64 的 sqrt 结果可能有 ±1 误差，但 `s+1` 修正足以覆盖这一误差范围。对更大的 t 值，int64 本身会先溢出（见下节）。

---

## 五、int64 溢出检测与自动回退

### 5.1 溢出位置分析

溢出发生在**计算 tC 的中间步骤**：
```
tC = (ar - b(p+q))² + (b(p-q))²
```

最坏情况下 `ar - b(p+q)` 的绝对值 ≤ (max_a + 2·max_b)·r。

若此值超过 `√(INT64_MAX/2) = 2¹⁵ - 1 = 2147483647`（约 2.1×10⁹），则平方后相加可能超过 INT64_MAX，导致 numpy int64 静默溢出返回错误结果。

### 5.2 安全阈值推导

```
_INT64_SAFE_HALF = (1 << 31) - 1 = 2147483647

# 由此得到每个 triple 的安全 r 上限：
# 要求 (max_k_num + 2*max_k_den) * r ≤ _INT64_SAFE_HALF
_WORKER_SAFE_R_MAX = _INT64_SAFE_HALF // (max_k_num + 2 * max_k_den)
```

**与 scale 的关系**：

| scale | safe_r_max | r_max (≈ 2·scale²) | numpy 覆盖率 |
|-------|-----------|---------------------|-------------|
| 100   | 1,342,177 | 20,000              | 100% |
| 200   | 671,088   | 80,000              | 100% |
| 400   | 335,544   | 320,000             | ~100%（勉强覆盖）|
| 600   | 223,696   | 720,000             | ~31%（大 r 走回退）|
| 1000  | 134,217   | 2,000,000           | ~7%（大多数走回退）|

### 5.3 回退路径

`_search_triple_int` 使用 Python 的**任意精度整数**（无溢出上限），代价是丧失向量化加速（约慢 5-10 倍）。对于 scale ≤ 400，几乎不触发回退。

---

## 六、多进程模式

### 6.1 Initializer 模式

```python
ProcessPoolExecutor(
    max_workers=n_workers,
    initializer=_init_worker,    # 每个子进程启动时执行一次
    initargs=(max_k_num, max_k_den),
)
```

`_init_worker` 在子进程中预建 `_WORKER_PAIRS`（Python list）、`_WORKER_A`/`_WORKER_B`（numpy 数组）和 `_WORKER_SAFE_R_MAX`，后续每次任务（一个 triple）都复用这些数据，无需重复计算或传输。

### 6.2 macOS spawn 限制

macOS 默认使用 `spawn` 模式启动子进程（而非 Linux 的 `fork`）。这要求 `_worker` 必须是**模块级函数**（可被 pickle），不能使用 lambda 或嵌套函数。

### 6.3 任务粒度

每个 triple 作为一个任务单元。triple 数约为 O(max_m²)，worker 数为 CPU 核数。任务粒度不均（大 r 的 triple 更慢），但总体上 triple 数远大于 worker 数，负载均衡自然。

---

## 七、D4 去重算法

### 7.1 canonical_xy

```python
def canonical_xy(x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    return min(d4_images(x, y))   # min 按元组字典序比较
```

对同一 D4 轨道中的任意点，`canonical_xy` 返回相同的代表元，用作去重键。

### 7.2 dedup_by_symmetry

```python
for pt in sorted_points:
    key = canonical_xy(pt.x, pt.y)
    if key not in best or pt.rational_count > best[key].rational_count:
        best[key] = pt
    elif pt.rational_count == best[key].rational_count:
        if pt.denominator < best[key].denominator:
            best[key] = pt
```

保留每个轨道中：① `rational_count` 最高的；② 相等时取 `denominator` 最小的（最简单的代表）。

---

## 八、GPU 路径

### 8.1 Backend 优先级

Backend 检测逻辑已拆分到独立模块 `backend.py`，`search_gpu.py` 从中导入：

```
detect_backend():
    1. 尝试 CuPy（import cupy）→ 最快，原生 numpy-like API
    2. 尝试 PyTorch CUDA/ROCm（torch.cuda.is_available()）→ 稍慢，API 需适配
    3. 回退 NumPy（CPU）→ 与 CPU 搜索相同，用于验证
```

### 8.2 `_TorchXP` 封装

由于 PyTorch 的数组 API 与 numpy/cupy 不完全兼容，`backend.py` 中的 `_TorchXP` 是一个薄包装器，实现了 `_search_triple_gpu` 所需的接口（`zeros_like`、`floor`、`sqrt` 等）。dtype 转换统一使用 `_xp_cast(arr, dtype)` 辅助函数（numpy 用 `.astype()`，torch 用 `.to(dtype)`）。

### 8.3 GPU 路径的 int64 限制

GPU 路径目前未实现 int64 溢出自动回退（GPU 不支持 Python 任意精度整数）。大 scale 时（> ~400）会打印警告但继续运行，溢出 triple 的结果可能不正确。

修复方向：在 GPU 路径中，对溢出 triple 降级到 CPU 的 `_search_triple_int`。

---

## 九、结果排序

默认排序键：`(-rational_count, denominator, x, y)`

| 优先级 | 字段 | 方向 | 含义 |
|--------|------|------|------|
| 1 | rational_count | 降序 | 四顶点解排最前（如有） |
| 2 | denominator | 升序 | lcm(x.den, y.den)，小的排前（"最简单"的解） |
| 3 | (x, y) | 升序 | 同等复杂度下字典序，结果可复现 |

`denominator` = lcm(x.denominator, y.denominator)，反映点坐标的"复杂度"，与解的数论性质相关。
