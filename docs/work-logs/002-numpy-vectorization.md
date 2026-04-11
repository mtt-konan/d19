# [002] NumPy 向量化与多进程加速

**日期**：2026-04-10  
**提交**：`271c833`

---

## 本次工作摘要

将搜索内层循环从逐元素 Python 整数运算改为 NumPy 向量化批量运算，同时引入 `--scale` 参数统一控制搜索规模。整体搜索速度提升约 20-50 倍（取决于 scale），并添加进度条和预估时间。

---

## 主要改动

- `src/rational_distance/search.py`
  - 新增 `_isqrt_vec(arr)`：批量整数平方根 + 完全平方判断，纯 NumPy，无 Python 循环
  - 新增 `_search_triple_vec(triple, coprimes, ...)`：对给定 (p,q,r)，向量化枚举所有 (a,b)，一次 NumPy 操作计算 tB/tD/tC
  - `_init_worker` 保存向量化所需的 max_k_num/max_k_den 等全局变量
  - `parametric_search_fast` 改用 `_search_triple_vec`；`--scale N` 自动推导三个参数（`max_m=N`，`max_k_num=8N`，`max_k_den=4N`）
- `scripts/search_3vertex.py` — 增加 `--scale` 参数；进度条改用 tqdm，附预估剩余时间
- `pyproject.toml` — 添加 tqdm 依赖

---

## 关键决策

**`_isqrt_vec` 的 float64 边界问题**：NumPy 的 `sqrt` 是 float64，对大整数（≥ 2^53）存在精度误差，可能导致 floor 结果偏低 1。修正方法：计算 `s = np.floor(sqrt(arr)).astype(int64)`，再检验 `(s+1)²`，满足时采用 `s+1`。这样可以覆盖 float 截断误差，代价是两次乘法。

**`--scale` 比例设计**：p,q,r 来自本原勾股数，r ≤ 2·scale²；a/b 的分子上限 8·scale、分母上限 4·scale，确保 d(A)=a/b 的分母（即整个坐标的公分母）可达 4·scale，覆盖足够密的有理网格。具体比例是经过实验（与 brute_force 对比）验证的。

**向量化内存考量**：每个 triple 的 (a,b) 对不超过 32N² 个，单次 NumPy 分配约数十 MB，可接受。若后续 scale 增大，可改为分块处理。

---

## 注意点 / 后续

- `_isqrt_vec` 的 s+1 修正与 int64 溢出共用同一阈值（见 006）
- 多进程 `spawn` 模式在 macOS 需要模块级 worker，不能用 lambda 或嵌套函数
- 速度瓶颈此时已转移到 `primitive_pythagorean_triples` 枚举 + 进程初始化，而非 isqrt 本身
