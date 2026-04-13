# 工作日志 013 — Parametric 单一逻辑源、APU 自动回退与 Ruff 接管

**日期**：2026-04  
**对应提交**：本次提交

---

## 摘要

本次改动只处理 `parametric` 主线，不动 `EC` 主体逻辑。目标是把 CPU 开发机和 AMD APU 主力机的“判定规则”收成一套，让两边只在执行方式上不同，不再分别维护两份核心实现。

同时补上了：

- CPU vs 加速后端的对照脚本
- `ruff` 代码质量工具链
- 对应的测试和文档

---

## 问题

重构前，`parametric` 的 CPU 路径和 GPU/APU 路径虽然数学目标一致，但代码上各自维护了一套判定流程：

- CPU 路径有自己的向量化判定和 Python 精确回退
- GPU/APU 路径也有自己的数组判定
- 高规模下 GPU/APU 只会打印警告，不会自动回退到精确路径

这会带来两个实际问题：

1. 后续如果继续做剪枝或提速，需要同时改两份核心逻辑，容易漏改。
2. 主力机跑得快，但当参数增大时结果可靠性不够硬。

---

## 改动

### 1. 新增 `parametric_core.py`

新增 `src/rational_distance/parametric_core.py`，作为 `parametric` 的唯一真理源，集中承载：

- side-exclusion 和 `inside_only` 过滤
- `tB / tC / tD` 的统一定义
- 完全平方预筛与 `s+1` 修正
- `safe_r_max(...)` 安全边界
- Python 大整数精确判定
- 原始命中结果归一化、去重键和排序
- 统一运行统计 `ParametricRunStats`

### 2. CPU 路径改为编排层

`src/rational_distance/search.py` 不再维护独立的核心判定实现，只负责：

- 多进程调度
- worker 初始化
- 汇总与去重
- 兼容现有公开接口

真正的判定已全部下沉到共享核心。

### 3. APU/GPU 路径改为执行层

`src/rational_distance/search_gpu.py` 现在只负责：

- 把 `(a, b)` 数组放到 `torch` / `cupy` / `numpy`
- 在安全范围内执行共享向量化逻辑
- 在不安全范围内自动切回共享的 Python 精确判定

也就是说，旧行为“报警但继续算”已经改成“自动精确回退后继续算”。

### 4. 新增对照脚本

新增 `scripts/compare_parametric.py`，用于在同一组参数下比较：

- CPU 基线
- 指定加速后端

输出内容包括：

- 耗时
- 点数
- D4 去重后的轨道数
- 对称差数量
- exact fallback 是否触发

并且也支持 `--scale`，避免再记一套参数。

### 5. 接入 `ruff`

`pyproject.toml` 中新增 `ruff` 配置与开发依赖，统一使用：

- `uv run ruff check .`
- `uv run ruff format .`

本次也顺手做了一轮全仓格式整理和低风险修正。

---

## 验证

本次完成后，验证项包括：

- `uv run pytest`：通过（当前 51 个用例）
- `uv run ruff check .`：通过
- `uv run python scripts/compare_parametric.py --scale 10 --max-k-num 20 --max-k-den 10 --backend numpy`
  - 输出 `symmetric difference: 0`
- `uv run python scripts/search.py parametric --max-m 10 --max-k-num 20 --max-k-den 10 --backend numpy --no-progress --top 5`
  - 正常执行

---

## 结果

这次提交的重点不是“已经更快很多”，而是把结构收顺：

- `parametric` 主线现在只维护一套判定逻辑
- CPU 开发机可以作为稳定基线
- AMD APU 主力机可以复用同一套规则并利用 `torch/ROCm`
- 以后继续做剪枝和提速时，不需要同时修改两份核心实现

下一步如果继续优化，推荐优先做：

1. 新的数学筛选条件 / 剪枝
2. 主力机上的 `torch` 实测基准
3. 视需要再把 `EC` 路径也逐步收成同样的结构
