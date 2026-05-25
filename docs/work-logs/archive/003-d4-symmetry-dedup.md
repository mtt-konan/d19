# [003] D4 对称去重

**日期**：2026-04-11  
**提交**：`e9ca51a`

---

## 本次工作摘要

单位正方形具有 D4 对称群（8 个等距变换），导致搜索结果中同一等价类的点重复出现。本次实现了基于规范代表元（canonical form）的去重，并引入 `denominator` 属性和结果排序规则。

---

## 主要改动

- `src/rational_distance/square.py`
  - `RationalPoint.denominator`：返回 x、y 分母的最小公倍数，作为"解的尺度"度量
  - `RationalPoint.canonical()`：对点 (x,y) 计算 D4 轨道中字典序最小的代表元
  - `RationalPoint.orbit()`：枚举 8 个 D4 像
- `src/rational_distance/search.py`
  - `parametric_search_fast` 结果集改用 `set[RationalPoint]`，插入前调用 `canonical()`
  - 保证同一等价类只保留一个代表元
- `scripts/search_3vertex.py`
  - 增加 `--sort-by` 参数（`rational_count`、`denominator`、`distance_a`）
  - 表格新增 `den` 列

---

## 关键决策

**规范代表元定义**：对 D4 的 8 个像 {(x,y),(y,x),(1-x,y),(1-x,1-y),(x,1-y),(y,1-x),(1-y,x),(1-y,1-x)} 取字典序（先比 x 再比 y）最小者作为代表元。此选择保证唯一性，且易于计算。

**为何 D4 轨道不总是大小 8**：若点落在对称轴上（如 x=y、x=1-y 等），部分变换结果相同，轨道可能更小（4 或 2）。在结果输出中观察到"size 2"轨道，是因为对称像的坐标超出搜索范围（负坐标或超出 k 枚举上限），并非数学错误。

**`denominator` 作为排序键**：按 denominator 升序排列，使"结构最简单"的解排在前面，便于人工分析。

---

## 注意点 / 后续

- 去重发生在 worker 结果汇总阶段（主进程），不影响并行效率
- 若搜索参数范围不对称（max_k_num ≠ max_k_den × 2），D4 覆盖可能不完整——当前比例已验证覆盖性
- `canonical()` 使用 Fraction 运算，汇总阶段点数一般较少，性能可接受
