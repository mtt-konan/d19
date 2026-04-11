# [006] int64 溢出自动回退

**日期**：2026-04-11  
**提交**：`aedccea`

---

## 本次工作摘要

分析并修复了大参数下 NumPy int64 运算的溢出问题，实现"超阈值的 triple 自动回退到 Python 任意精度整数"机制，同时完善了 Windows ROCm 文档（Python 版本固定方法）。

---

## 主要改动

- `src/rational_distance/search.py`
  - 新增常量 `_INT64_SAFE_HALF = (1 << 31) - 1`（= 2,147,483,647）
  - 新增全局 `_WORKER_SAFE_R_MAX`，在 `_init_worker` 中按公式计算：
    ```
    safe_r_max = _INT64_SAFE_HALF // (max_k_num + 2 * max_k_den)
    ```
  - `_worker`：若 triple 的 r > `_WORKER_SAFE_R_MAX`，调用 `_search_triple_int`（Python int）而非 `_search_triple_vec`（NumPy）
  - `parametric_search_fast`：当 scale > 400 时打印警告，说明大-r triple 将走回退路径
- `scripts/search_gpu.py` — 更新 docstring：完整 Windows ROCm 安装步骤（AMD Adrenalin 驱动、`uv python pin 3.12`、gfx1151 wheels URL、验证命令）

---

## 关键决策

**为什么 tC 是约束最紧的**：三个距离平方表达式中，tC = (ar - b(p+q))² + (b(p-q))² 中的 `p+q` 最大可达 `2r`，导致 `(ar - b·2r)` 项最大，易溢出。而 tB 中 `p < r`，tD 中 `q < r`，均更小。

**`_INT64_SAFE_HALF` 的推导**：要求每个平方项 < INT64_MAX/2，即各项 < 2^63/2 = 2^62。取 `sqrt(2^62) ≈ 2.147×10^9 = 2^31 - 1`（恰好是一个整洁的幂次减一）作为各乘积的上界阈值。

**不修复 GPU 路径**：GPU 张量的整数类型固定，无法动态切换到 Python int。修复方案（CPU 回退大-r triple）代码量较大，留作后续工作。当前 GPU 路径在 scale ≤ 400 时安全（safe_r_max 约 335,544，大于 r_max ≈ 320,000）。

**scale 与溢出关系**：
| scale | r_max (≈2×scale²) | safe_r_max | 是否全 numpy |
|-------|-------------------|------------|-------------|
| 400   | 320,000           | 335,544    | ✅ 全部       |
| 600   | 720,000           | 223,696    | ❌ 部分回退   |
| 1000  | 2,000,000         | 134,217    | ❌ 大量回退   |

---

## 注意点 / 后续

- `_search_triple_int`（Python int 回退）与 `_search_triple_vec` 逻辑一致，均含侧边过滤
- GPU 路径的 int64 溢出保护仍未实现，scale > 400 时 GPU 结果可能有误；待后续版本修复
- Windows ROCm：`uv python pin 3.12` 会在项目根目录生成 `.python-version` 文件，版本固定为项目级别，不影响系统 Python
