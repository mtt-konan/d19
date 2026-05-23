# 035 — PARI 内置 Selmer / 2-descent API 探明

**日期**: 2026-05
**触发原因**: 想法 3（IDEAS §4，2-descent on $E_{A,B}$）原本预期需要装 SageMath，
工作量 1-2 天。本 worklog 探查 cypari2 直接暴露的 PARI 命令，发现项目**已经
拥有**做 2-descent obstruction 所需的全部计算工具，无需装 Sage。
**输出**: 一份探查脚本 + API 盘点 + 后续路线图（写 worklog 036 时直接实证）。

---

## 起因

worklog 033 在 dual EC probe 中调用 `rational_distance.concordant.compute_rank`，
该函数是 d19 的 PARI 封装，签名为：

```python
def compute_rank(A, B, pari=None, *, profile=None) -> tuple[int, tuple[int, int], list]:
    # returns (rank, (lower, upper), generators)
```

只用了 PARI `ellrank(E, effort)` 返回值的**前 3 项**（理解为 lower/upper/gens）。
但 worklog 033 暴露出"default ellrank 给虚假 rank=0"的现象，提示 PARI 的返回
值结构可能比 3 元组更丰富，值得深挖。

## 探查方法

`scripts/probe_pari_selmer_api.py` 在 chain near-miss `(7, 24, 45, 28)` 上对
$E_{7,45}: Y^2 = X(X+49)(X+2025)$ 调用了所有可能相关的 PARI 命令：

| 命令 | 返回内容 | 是否实测可用 |
|---|---|---|
| `ellrank(E, 2)` | `[rank_lo, rank_hi, sha2_lo, gens]` (**4 元组**) | ✅ |
| `elltors(E)` | `[order, [structure], [gen_X, gen_Y]]` 完整 torsion | ✅ |
| `ell2cover(E)` | quartic 4 次多项式列表 = Selmer 群非平凡元素的显式形式 | ✅ |
| `ellratpoints(E, h)` | height ≤ h 的有理点列表（实测 h=20 太小，只返回 torsion） | ✅ |
| `ellrankinit(E, e)` | 报错 "too many parameters" — cypari2 暴露方式有问题 | ❌ |

具体输出（已 trim）：

```
ellrank(E, 2)  → [1, 1, 0, [[-1323, 34398]]]
                  ↑  ↑  ↑   ↑
                rank rank Sha[2] generator (X, Y)
                lower upper lower

elltors(E)     → [8, [4, 2], [[-315, 11970], [-49, 0]]]
                  ↑   ↑       ↑                 ↑
                order 结构    Z/4 gen           Z/2 gen

ell2cover(E)   → 3 个 quartic covers:
                 [49x⁴ - 630x³ + 2473x² - 1170x + 169, ...]
                 [x⁴ - 3854x² + 4100625, ...]
                 [x⁴ + 300x³ + 7552x² - 7800x + 676, ...]
```

## 关键发现

### 1. `ellrank` 返回 4 元组而非 3 元组

PARI 文档实际定义（核对 `?ellrank` in GP）：

```
ellrank(E, {effort=0}, {points})
returns [rlo, rhi, sha, vec]
  rlo:  rank lower bound (certified by finding points)
  rhi:  rank upper bound (certified by 2-descent)
  sha:  lower bound on F_2-dimension of Sha(E)[2] / E[2](Q)
  vec:  list of independent rational points
```

> **`sha` 是免费的 Sha[2] 信息**：之前 worklog 033 完全没用到。

d19 的 `compute_rank` **丢失了 `sha` 字段**——这是个项目级 bug。

### 2. `ell2cover(E)` 直接给出 Selmer covers

Sage 的 `E.two_descent()` 内部本质是调用 mwrank 拿 quartic covers，再做局部
solubility 检查得到 Selmer 群结构。PARI 的 `ell2cover` 是**同一个底层算法**
的直接出口（PARI 2.16+）。

输出的每个 quartic $g(x) \in \mathbb{Q}[x]$ 满足：在 $E$ 的 2-isogeny descent
下，$g(x) = z^2$ 的有理解对应 $E(\mathbb{Q})$ 的一个非平凡 2-descent class。

> **这就是想法 3 (Sage 2-descent) 的核心输出**，已经免费拿到。

### 3. 实测：`(7, 24, 45, 28)` 在 E_{7,45} 上的对应有理点

数值验证：$X = b^2 = 24^2 = 576$ 在 $E_{7, 45}$ 上确实给出有理点，
$Y^2 = 576 \cdot 625 \cdot 2601 = 936\,360\,000 = 30\,600^2$。

但 generator 是 $(-1323, 34398)$，跟 $(576, 30600)$ 不直接相等 —— 后者必然是
generator + torsion 的某个组合（因为 rank=1，torsion = $\mathbb{Z}/4 \times
\mathbb{Z}/2$）。

这印证了 chain near-miss 在 dual EC 视角下**总是产生有理点**——和 worklog 033
的负面结论一致：dual EC 不能 obstruct 这些 candidate。

## 修正项目级 bug

`src/rational_distance/concordant/analysis.py` 中的 `compute_rank` 当前签名：

```python
def compute_rank(A, B, pari=None, *, profile=None) -> tuple[int, tuple[int, int], list]:
```

应当扩展为：

```python
def compute_rank(
    A, B, pari=None, *, profile=None, effort=2,
) -> tuple[int, tuple[int, int], int, list]:
    # returns (rank, (lower, upper), sha2_lower, generators)
```

或者引入更丰富的 return type（dataclass）。这个改动会影响所有调用点，需要
单独的 worklog 处理（参见后续 routes）。

> 现行 `compute_rank` 默认 `effort=0`（隐式），实测证明默认 effort 在大量 chain
> candidate 上给虚假 `lower=0`，应该统一改为 `effort=2`。

## 暗藏的能力盘点

PARI 通过 cypari2 还暴露：

| 命令 | 用途 | 想法对应 |
|---|---|---|
| `ellisoncurve(E, P)` | 验证点是否在曲线上 | 数值 sanity |
| `ellisogenyapply` | 同源映射 | 2-isogeny descent 的细化 |
| `ellpadicregulator` | $p$-adic regulator | BSD 验证 |
| `elltatepairing` | Tate pairing | Cassels-Tate pairing 实现 |
| `ellL1` | $L(E, 1)$ 数值 | 替代 `ellanalyticrank`，无 conductor 限制 |
| `ellpadicL` | $p$-adic L | Heegner-style obstruction |

**这一组工具足以对应 Peschmann 2026 §6 的 2-descent technique 实现**，无需
SageMath 安装。

## 与 Peschmann 2026 §6 的对接

读 [arXiv HTML](https://arxiv.org/html/2604.09328v1) §6 后澄清的关键点：

### Peschmann 的 2-descent map (Theorem 6.2)

设 $E_A: y^2 = (x+A)(x-2)(x+2)$，三根 $r_1 = -A, r_2 = 2, r_3 = -2$。
对非 torsion $P = (x, y)$ with $x = u/v^2$（gcd=1），定义
$\delta_i := \text{sf}(v^2(x - r_i))$，则 $\delta_1 \delta_2 \delta_3 \equiv 1 \pmod{\mathbb{Q}^{*2}}$。

**Theorem 6.2(a)**: $\delta_3 = 1 \Rightarrow f(P) \equiv 2 \pmod{\mathbb{Q}^{*2}}$（不是平方）。

**Remark 6.5 (Gaussian arithmetic)**: 每个 $f_i$ 是 $\mathbb{Z}[i]$ 中的 norm，
所以 $p \equiv 3 \pmod 4$ 自动偶次出现；**只有 $p \equiv 1 \pmod 4$ 的分裂
素数能 obstruct**——这正是 §7(3) 报告的"88.4% blockers $\equiv 1 \pmod 4$"
现象的来源。

### d19 的对应

把 $E_{A,B}: Y^2 = X(X+A^2)(X+B^2)$ 套进同样结构，三根 $0, -A^2, -B^2$。
对 $X = u/v^2$:

- $\delta_1 = \text{sf}(u)$
- $\delta_2 = \text{sf}(u + A^2 v^2)$
- $\delta_3 = \text{sf}(u + B^2 v^2)$

**chain solution 等价于**：存在整数 $N$ 使 $X = N^2$ 给出有理点 $(N^2, Y)$ 同时
$N^2 + A^2$ 和 $N^2 + B^2$ 都是完全平方。这等价于 $u = N^2, v = 1$ 时
$(\delta_1, \delta_2, \delta_3) = (1, 1, 1)$ —— **trivial 2-descent class**。

### 关键实证含义

> chain solution 必须落在 $E_{A,B}(\mathbb{Q})$ 的 trivial 2-descent class，
> 即 $2 E(\mathbb{Q}) + E[2]$。

后向解释 worklog 033 的 negative：chain near-miss $(a, b, c, d)$ 在 dual EC
$E_{a,c}$ 上给出 $X = b^2$，自动 trivial class（因为 $b^2 + a^2 = h_1^2$ 是
平方）。所以 dual EC probe 一开始就不可能给 free obstruction——chain
candidate 永远在 trivial class 里。

### Peschmann §6 的 obstruction 不直接适用

Theorem 6.2(a) 的 $\delta_3 = 1$ obstruction 是对 *non-torsion non-chain*
点的限制。chain candidate 自动满足 $\delta_3 = 1$，所以这条 obstruction 反而
是 chain solution 的**必要条件**而非排除条件。

**真正可能用的 d19 版 obstruction**：

1. 对 hard_case $(A, B)$ 算 $E_{A,B}(\mathbb{Q})$ 的 Mordell-Weil generators
2. 枚举高度 ≤ $H$ 的所有 $\mathbb{Z}$-线性组合 $Q = n_1 P_1 + \cdots + t$
3. 检查是否存在 $Q$ 使 $X(Q) = N^2$（perfect square）AND $N^2 + A^2, N^2 + B^2$ 都是平方
4. 如果没有 → **finite-descent obstruction**（非平凡的 effective bound）

这就是 Peschmann §7 在 perfect cuboid 上跑的 "5 hard specialisations × 175,418
lattice points" 的对应物。在 d19 的 116 个 hard_case 上跑这个，是 worklog 036
的目标。

### Peschmann §7 实测细节（读完 chunk 12 后）

§7 的三层验证（[arxiv chunk 12](https://arxiv.org/html/2604.09328v1)）：

**(1) Brute force**: $(a, b, m, n) \in [1, 1000]^4$ + coprime + parity → 约
$10^{11}$ tuples，$f_1 f_2$ 从未是平方。

**(2) Finite-descent / modular search**: 对 5 个 hard $s$ values
$(18/41, 18/47, 23/59, 23/64, 29/65)$（即 Mordell-Weil generators 全部
$\delta_3 | \delta_1$ 的 case），在某 lattice 上枚举 **175,418 candidates**，
对每个用 **45 primes $p < 200$ 做 mod-$p$ 同余检查**。结果：0 candidate 让
$f(P) \in \mathbb{Q}^{*2}$。

**(3) Per-tuple blocker prime 分布**: 223,729 tuples ($a, b, m, n \leq 40$)，
最小 blocker prime $p$ 的 mod 4 分布：
- 88.4% 是 $p \equiv 1 \pmod 4$
- 11.6% 是 $p = 2$
- **0% 是 $p \equiv 3 \pmod 4$** ← 完美验证 Remark 6.5

### Level 2 不是枚举 Mordell-Weil 点

关键细节：Peschmann §7(2) **不是 enumerate height ≤ H 的所有 rational points**，
而是 **modular search on a lattice**——在某个有限格点集上对 45 个小素数做
mod-$p$ 同余检查。这跟 d19 现有的 safe_sieve (mod 1680, ~5 primes) 思路完全
一致，只是 prime 集合更大。

### d19 vs cuboid 的 mod 4 反差

| | Peschmann (cuboid) | d19 (chain, worklog 034) |
|---|---|---|
| 主导素因子 mod 4 | 88.4% $\equiv 1$, 0% $\equiv 3$ | 大多数因子里 $\equiv 3$ 占多数 |
| 算术结构 | $f_i$ 是 $\mathbb{Z}[i]$ 范数 | hypotenuse 含 scale × primitive，不是单一范数 |
| Selmer trivial class | 主要 obstruction 来源 | chain candidate 自动落入，无 obstruction |

这定量验证了"chain ≠ cuboid"。Peschmann 风格的 Selmer/blocker prime obstruction
**不直接适用**于 d19 chain candidate。d19 的 obstruction 必须找别的来源。

### worklog 036 的明确目标

把 d19 现有 safe_sieve（mod 1680）**升级到 Peschmann §7(2) 规模**：
- 把 prime 集合从 ~5 扩到 45 (所有 $p < 200$)
- 对 d19 的 116 hard_case 做 finite-descent
- 看是否能复制"0 candidate"结果

如果有 hard_case 在扩展后过了 sieve（即 sieve 找不到 obstruction），它就是
**真正难的 case**，需要更精细的方法（Heegner / explicit point search / Brauer-Manin）。

## 后续路线（worklog 036+）

### 短期（本 session 之外）

1. **修 `compute_rank` 拿全 4 元组**，包括 `sha2` 和 `effort=2` 默认。
2. **重跑 worklog 033 的 dual EC probe**，把 sha2 加入 JSONL 输出。
3. **批量在 d19 hard_case 列表（116 个 (A, B)）上跑 ell2cover**，统计 quartic 数量
   分布。这跟 Peschmann §7 的 42/54 rank-0 验证是同一种实证。

### 中期

4. **逐章对照 Peschmann §6**：用 PARI 实现他用 Sage 做的所有步骤。`docs/literature/notes/peschmann-2604-09328.md`
   已经摘录了主要定理（5.4, 6.2）+ 关键 references，可以直接对接。
5. **实现 Kummer character $\chi_f$ 在 d19 EC 上**（IDEAS 没列出，是从 Peschmann
   学来的新方向）。

### 长期

6. **完整 d19 paper draft 的 §6"Selmer-style obstructions"**，复用 PARI 工具，
   不依赖 Sage。

---

## 输出物

### 脚本
- `scripts/probe_pari_selmer_api.py` — PARI Selmer API 探查（一次性，不进 batch
  pipeline）

### 文档
- 本 worklog
- 待更新：`src/rational_distance/concordant/analysis.py` `compute_rank` 签名
- 待更新：`docs/CHAIN_STRUCTURE_IDEAS.md` 想法 3 加注"无需装 Sage"

### 复现命令

```bash
# 一次性 API 探查（< 1 秒）
uv run python scripts/probe_pari_selmer_api.py
```
