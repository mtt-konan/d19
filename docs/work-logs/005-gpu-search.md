# [005] GPU 搜索后端

**日期**：2026-04-11  
**提交**：`1ae4419`

---

## 本次工作摘要

新增 GPU 加速搜索路径，支持三种后端（CuPy / PyTorch / NumPy）自动降级，通过 `_TorchXP` 封装屏蔽 PyTorch 与 NumPy 的 API 差异。针对 AMD Ryzen AI Max+ 392 / Windows ROCm 环境提供完整安装指南。

---

## 主要改动

- `src/rational_distance/search_gpu.py` — 新建：
  - `_detect_backend()`：按 CuPy → PyTorch CUDA → PyTorch CPU → NumPy 优先级自动选择
  - `_TorchXP`：封装类，将 `torch.Tensor` 的 `any()`/`where()`/`sqrt()` 等操作统一为 NumPy 风格接口
  - `parametric_search_gpu`：GPU 版主搜索函数，与 CPU 版逻辑一致，但全程使用 xp（后端 array 模块）
- `scripts/search_gpu.py` — 新建：GPU 搜索 CLI
  - `--backend [auto|cupy|torch|numpy]` 手动指定后端
  - 含 Windows ROCm 安装步骤（完整 docstring）
- `tests/test_search_gpu.py` — 新建：基本正确性测试（numpy 后端）

---

## 关键决策

**CuPy 优先于 PyTorch**：CuPy 的 API 与 NumPy 几乎一一对应，适配成本最低；PyTorch 需要额外的 `_TorchXP` 封装。在有 CuPy 的环境下优先使用。

**`_TorchXP` 封装而非完整适配层**：只封装搜索路径实际用到的约 10 个方法，而不是实现完整的 array protocol。减少代码量，降低维护负担。

**Windows ROCm 说明内嵌于脚本 docstring**：安装步骤较长（约 20 行），放在脚本文件顶部 docstring，比单独 markdown 文件更易被开发者发现。

**已知限制 — 无 int64 溢出保护**：GPU 张量无法使用 Python arbitrary-precision int；当 scale 较大时，大-r triple 在 GPU 路径可能产生静默错误。计划在后续版本为 GPU 路径添加 CPU 回退（见 006）。

---

## 注意点 / 后续

- `_TorchXP.where()` 的参数顺序与 `np.where()` 一致（condition, x, y），PyTorch 原生接口顺序相同，无需调整
- AMD ROCm on Windows：Python 版本必须为 3.11–3.13（ROCm wheels 不含 cp314）；使用 `uv python pin 3.12`
- CuPy ROCm on Windows：无预编译包，需从源码编译，实际不可行；Windows AMD 用户应使用 `--backend torch`
- GPU 路径的 int64 溢出修复留待 006
