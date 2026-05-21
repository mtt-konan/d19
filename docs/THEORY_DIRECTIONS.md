# 理论方向与搜索空间缩减

本文档总结当前可以减少搜索空间的**短中期可落地**理论方向，按可落地难度排序。

> 想看可能直接撬动 Harborth 猜想本身的**长期数学突破**方向（Heegner 点、Chabauty、
> Brauer–Manin、K3 曲面等），请看 [THEORY_DIRECTIONS_ADVANCED.md](./THEORY_DIRECTIONS_ADVANCED.md)。
>
> 简单区分：
>
> - 本文 = "几周内能落到 `chain-fast` / `concordant` 里的安全前筛"
> - ADVANCED = "可能需要 SageMath / Magma 重型工具栈、但能把过滤器变成判定器"

---

## 方向一：(h3, h4) 因子分解攻击 ✅ 已实现

### 核心推导

从 C3 和 C4 的联立求解出发：

- C3: `h3² = A² + N²`
- C4: `h4² = N² + B²`

两式相减：
```
h4² - h3² = B² - A²
(h4 - h3)(h4 + h3) = (B - A)(B + A)
```

### 算法改进

**当前方式**：扫描 `N ∈ (A, B)`，对每个 N 检查 C3 和 C4。
- 复杂度：`O(B - A)`
- 问题：对大的 `(A, B)` 间隔，扫描成本高

**新方式**：枚举 `B² - A²` 的所有因子分解。

对 `B² - A² = d1 × d2`（其中 `d1 < d2`，同奇偶）：
1. 令 `h3 = (d2 - d1)/2`，`h4 = (d2 + d1)/2`
2. 检查 `N² = h3² - A²` 是否为非负完全平方数
3. 若是，验证 `N² + B² = h4²`（自动满足）

### 复杂度分析

- 因子对数：`O(τ(B² - A²))`，其中 `τ` 是除数函数
- 典型情况：`τ(n) ≈ O(n^ε)` 对任意 `ε > 0`
- 相比 `B - A`：通常快数个数量级

### 实现状态：已完成

- **模块**：`src/rational_distance/concordant/factor_search.py`
- **函数**：`find_concordant_by_factorization(A, B) -> list[int]`
- **CLI**：`concordant --method factor`（默认仍为 `ec`，完全兼容）
- **测试**：`tests/test_concordant.py::TestConcordantFactorSearch`（8 个测试）

```bash
# 单对验证（无需 PARI）
uv run python scripts/search.py concordant --pair 264,420 --method factor

# 批量分析（无需 PARI，无上界）
uv run python scripts/search.py concordant --max-hyp 500 --method factor --no-progress
```

这是把 C3+C4 从"两个独立条件"改写成"一个联立方程"，**从根本上绕过了 N 的线性扫描**。

---

## 方向二：Gaussian 整数表示结构

### 核心条件

`A² + N² = h3²` 成立，当且仅当 `A + Ni` 在 `Z[i]`（Gaussian 整数）中的分解满足：

**对每个素数 `p ≡ 3 (mod 4)`，`v_p(A² + N²)` 必须是偶数。**

其中 `v_p(n)` 是 n 的 p-adic 赋值（n 能被 p 整除的最高次数）。

### 联立条件

对 C3 + C4 同时成立：

- `v_p(A² + N²)` 是偶数
- `v_p(N² + B²)` 是偶数

给定素数 `p ≡ 3 (mod 4)`，这两个条件会限制 `N mod p²` 的可取值。

### 筛法构造

1. 对小素数 `p = 3, 7, 11, 19, 23, 31, ...` 分别计算禁止的 `N mod p²` 剩余类
2. 用中国剩余定理（CRT）合并这些条件
3. 得到一个关于 `N mod M`（M 是这些素数的积）的禁止集合

### 优势

- 比当前 `mod 8` 更细的可证明安全前筛
- 计算成本低（只需 `mod p²` 判断）
- 可以直接集成到 `chain-fast` 的 inner loop

### 与现有筛的关系

当前 `mod 8` 筛（来自 CHAIN_FAST_SAFE_FILTERS.md）实际上是 `p = 2` 的特例。这个方向是把它推广到所有 `p ≡ 3 (mod 4)` 的素数。

---

## 方向三：concordant 曲线的 2-descent 分层

### 现状

所有 chain-fast 产出的 `(A,B)` pair 的 concordant 曲线 rank ≥ 1（过滤率 0%）。

但 rank ≥ 1 只保证有理点存在，不保证整数 N 存在。

### 2-descent 方法

椭圆曲线 `Y² = X(X + A²)(X + B²)` 的 2-descent 给出 Selmer 群条件，可以限定：

**哪些 `(A, B)` pair 虽然有有理点但整数 N 不存在。**

### 实现路径

1. 对每个 `(A, B)` pair，用 PARI/GP 计算 Selmer 群（已有 `cypari2` 接口）
2. 分析 2-descent 障碍
3. 筛掉那些 Selmer 群表明不存在整数 N 的 pair

### 难度与收益

- **数学难度**：高（需要理解 2-descent 理论）
- **工程难度**：高（需要 PARI 深度集成）
- **预期收益**：高（理论上可以直接排除一大类 pair）

这个方向更像"长期研究"而不是"近期工程"。

---

## 方向四：对角符号筛的数学来源与加强

### 现有结果

从 MATH.md §7.2 的推导：

```
a + c = b + d ⟺ k1(p1 - q1) + k3(p3 - q3) = 0
∴ (p1 - q1) 与 (p3 - q3) 必须异号
```

这是硬必要条件，已实现为 `diagonal_sign_sieve`。

**效果**：从 `max_val=500` 的 10 个结果砍到 2 个（减少 80%）。

### 进一步加强

由 `k1/k3 = (q3 - p3)/(p1 - q1)`，因为 `k1, k3` 都是正有理数，还要求这个比值为正有理数。

结合 `k2 = k1 q1/p2` 的约束，可以导出对 `(T1, T2)` 具体腿值比的更细限制：

1. 对每对 `(T1, T2)`，计算 `(p1 - q1)` 和 `(p3 - q3)` 的比值范围
2. 结合 `k1, k2, k3` 的正性约束
3. 得到更严格的 pair 排除条件

### 难度与收益

- **数学难度**：低（纯数论）
- **工程难度**：低
- **预期收益**：中（已经有 80% 效果，再挤空间有限）

---

## 优先级建议

| 方向 | 数学难度 | 工程难度 | 预期收益 | 建议 |
|------|---------|---------|---------|------|
| **因子分解攻击** | 低 | 中 | **高** | ✅ 已实现 |
| **Gaussian 整数 mod 筛** | 中 | 低 | **中高** | **下一步立即动手** |
| **2-descent Selmer** | 高 | 高 | 高 | 中期 |
| **对角符号加强** | 低 | 低 | 中 | 可选 |

> 上述方向都还属于"工程范式内"——核心思想都是"减少搜索空间"。
> 如果想跳出这个范式，看是否有方法能**直接判定一个 `(A,B)` pair 永远无解**，
> 请看 [THEORY_DIRECTIONS_ADVANCED.md](./THEORY_DIRECTIONS_ADVANCED.md) 中的：
>
> - 方向五（Heegner 点直接构造）— 工程化最现实，**优先尝试**
> - 方向七（Chabauty / Quadratic Chabauty）— 长期攻关
> - 方向八（Brauer–Manin 障碍）— 可能直接证明 Harborth 猜想
> - 方向十（K3 曲面 / Mordell–Weil lattice）— 革命性视角

---

## 立即可做的第一步

### 因子分解攻击的快速验证

对 `chain-fast` 的现有结果集：

1. 对每个 near-miss `(A, B)` pair，计算 `B² - A²`
2. 枚举因子对，按新方式搜索 N
3. 对比现有结果，验证一致性
4. 测量加速比

这个验证可以用 Python 快速原型，不需要改动现有 `chain-fast` 代码。

---

## 参考文献

- MATH.md §7：Pythagorean 4-cycle 的代数化简
- MATH.md §8：Concordant 椭圆曲线分析
- CHAIN_FAST_SAFE_FILTERS.md：当前已实现的 mod 筛
- CHAIN_FAST_STRUCTURE_FINDINGS.md：`max_hyp=100000` 的结构统计

