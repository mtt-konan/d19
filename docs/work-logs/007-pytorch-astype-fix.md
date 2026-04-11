# [007] 修复 PyTorch 后端 .astype() 兼容性

**日期**：2026-04-11  
**提交**：（本次）

---

## 本次工作摘要

修复 `--backend torch` 路径在 Windows ROCm 环境下崩溃的问题。根本原因：PyTorch `Tensor` 对象不支持 `.astype(dtype)` 方法（应使用 `.to(dtype)`），但 GPU 搜索代码对所有后端统一调用了 `.astype()`。同时修复了 `_to_cpu` 辅助函数无法将 PyTorch GPU 张量正确拷贝回 CPU 的问题。

错误信息：`AttributeError: 'Tensor' object has no attribute 'astype'`

---

## 主要改动

- `src/rational_distance/search_gpu.py`
  - 新增模块级辅助函数 `_xp_cast(t, dtype)`：
    - NumPy 数组：调用 `t.astype(dtype)`
    - PyTorch 张量（有 `.to()`，无 `.astype()`）：调用 `t.to(dtype)`
    - CuPy 数组（同时有两者）：调用 `t.astype(dtype)`
  - `_isqrt_gpu`：将 `t.astype(xp.float64)` 和 `.astype(xp.int64)` 替换为 `_xp_cast(...)`
  - `_search_triple_gpu`：将 `okB/okD/okC.astype(xp.int64)` 替换为 `_xp_cast(...)`
  - `_to_cpu`（`_search_triple_gpu` 内部）：增加 PyTorch 分支 `sliced.cpu().numpy()`，原先仅处理 CuPy（`.get()`）和 NumPy（`np.asarray()`），PyTorch GPU 张量会在 `np.asarray()` 处崩溃

---

## 关键决策

**用 `_xp_cast` 而非修改 `_TorchXP`**：另一方案是让 `xp.array()` 返回 `_TorchArrayWrapper`，使所有算术结果自动带 `.astype()`。但这需要重写 `__getitem__` 索引逻辑（需要解包 wrapper 作为索引），以及让 `_TorchXP.sqrt/floor` 接受 wrapper 输入，改动面更大。`_xp_cast` 是精准最小改动，且对三种后端均正确。

**类型判断顺序**：NumPy 数组检查放首位（`isinstance(t, np.ndarray)`），因为 NumPy 数组也有 `.to()` 方法（新版 numpy 中）。CuPy 数组同时有 `.to()` 和 `.astype()`，走最后的 `.astype()` 分支。

**`_to_cpu` 顺序**：先检查 `.get()`（CuPy），再检查 `.cpu()`（PyTorch），最后 `np.asarray()`（NumPy）。顺序不可颠倒——CuPy 数组没有 `.cpu()`，PyTorch 张量没有 `.get()`，NumPy 数组没有任何一个。

---

## 注意点 / 后续

- 修复后在 Windows ROCm（gfx1151）`--backend torch` 可正常运行
- GPU 路径仍无 int64 溢出保护，scale > 400 时结果可能有误（已知，待后续修复）
- 8 项单元测试全部通过
