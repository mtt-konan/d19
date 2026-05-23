# 034 — 想法 1 实证：4 个 hypotenuse 的恒等式与 blocker prime

**日期**: 2026-05
**触发原因**: `docs/CHAIN_STRUCTURE_IDEAS.md` §2 (想法 1) 提出 4 个 hypotenuse
$h_1, h_2, h_3, h_4$ 之间存在三个代数恒等式（A, B, C），并基于"hypotenuse 的奇
素因子全部 ≡ 1 (mod 4)"导出 blocker prime 论证。本 worklog 实证验证这三个
恒等式 + 检验 blocker prime 论证是否成立。
**输出**: 两个分析脚本 + 一份 JSONL + 关键负面发现（§2.4 假设错误）。

---

## 数据来源

直接复用 d19 现成的 `src/rational_distance/search_chain.py`（worklog 014 / 015 /
016 时代构建），通过 `find_chains(max_val=N, require_square=False)` 获得"长方形
4-chain"（4 个 Pythagorean 边都闭合，但不要求 $a+c = b+d$）。该模块已经：

- D4 去重（4 旋 × 2 反射 = 8 个对称 image 取 lex-min）
- 排除 cross-product family（`a*c == b*d`，worklog 015）
- 排除 `len({a, b, c, d}) < 4` 的退化（如 (3,4,3,4)，矩形对角中心）

剩余的 "general family" chain 数量：

| `max_val` | chains | square_ok |
|---|---|---|
| 100  | 0   | 0 |
| 500  | 10  | 0 |
| 1000 | 51  | 0 |
| 2000 | 208 | 0 |
| 5000 | 1005 | 0 |

`square_ok = 0` 与 Harborth 猜想一致——`max_val ≤ 5000` 范围内**没有**正方形
4-chain。

---

## 恒等式数值验证

`scripts/analyze_hypotenuse_identity.py` 在 `max_val=5000` 的 1005 个 chain 上
逐个验证：

| 恒等式 | 验证条件 | 结果 |
|---|---|---|
| **A** | $h_1^2 + h_3^2 = h_2^2 + h_4^2 = a^2+b^2+c^2+d^2$ | **1005 / 1005** ✅ |
| **B** | $h_1^2 - h_2^2 = (a-c)(a+c)$（一般形式） | 退化恒等式，自动成立 |
| **C** | $(h_1 h_3 - h_2 h_4)(h_1 h_3 + h_2 h_4) = (d-b)(a-c)(a+c)(b+d)$ | **1005 / 1005** ✅ |

注：IDEAS §2.2 的 B 是 §2.1 A 的等价改写，且依赖正方形条件 $a+c=b+d=S$；这里
1005 个 chain 都 `square_ok=False`，所以 B 不可应用。一般形式
$h_1^2 - h_2^2 = (a-c)(a+c)$ 永远成立（直接展开）。

**结论**：恒等式 A, C 都是**正确的代数恒等式**。这部分 IDEAS §2 的代数推导
完整无误。

---

## §2.4 blocker prime 论证：基础假设错误

### IDEAS §2.4 的论证

> 每个 $h_i$ 是 hypotenuse → 它的奇素因子 $\equiv 1 \pmod 4$（Fermat 二平方定理）。
>
> 把恒等式 C 写成因子形式：
> $(h_1 h_3 - h_2 h_4)(h_1 h_3 + h_2 h_4) = (d-b)(a-c) S^2$
>
> 如果存在素数 $p \equiv 3 \pmod 4$ 整除右边但不能整除左边的某个因子（因为
> $p$ 不出现在 $h_i$ 的因子分解里），则**这个 $p$ 就是一个 blocker prime**。

### 关键 bug

Fermat 二平方定理实际上说的是：**正整数 $n$ 可表为 $n = u^2 + v^2$ ⟺ 在 $n$
的素因子分解里每个 $\equiv 3 \pmod 4$ 素因子出现偶数次**。

对 hypotenuse $h$，我们有 $h^2 = a^2 + b^2$。而 $h^2$ 的任意素因子分解里
每个素因子的指数都是 $h$ 中的指数 × 2，所以**自动是偶数**。换言之：

> Fermat-Euler 在 $h^2 = a^2 + b^2$ 上**没有给出任何对 $h$ 自身的约束**。
> $h$ 可以含任意素因子，包括 $\equiv 3 \pmod 4$ 的。

### 数值验证：错误的反例

`scripts/find_h_3mod4_counterexamples.py` 在 `max_val=2000` 的 208 个 chain
上扫描："是否存在某个 $h_i$ 含 $\equiv 3 \pmod 4$ 素因子"：

```
Total chains with at least one h_i containing a 3-mod-4 prime: 182 / 208 (87.5%)
```

**只有 12.5% 的 chain 满足 §2.4 的假设**。三个最小反例：

| 反例 chain | 违例的 hypotenuse | 来源 |
|---|---|---|
| (66, 88, 105, 360) | $h_1 = 110 = 2 \cdot 5 \cdot \mathbf{11}$ | scale=22 × primitive (3,4,5) |
| (56, 105, 208, 390) | $h_1 = 119 = \mathbf{7} \cdot 17$ | scale=7 × primitive (8,15,17) |
| (90, 216, 195, 400) | $h_1 = 234 = 2 \cdot \mathbf{3}^2 \cdot 13$ | scale=18 × primitive (5,12,13) |

**modus operandi**：non-primitive Pythagorean triple $(kp, kq, kh)$ 的 hypotenuse
$kh$ 继承 scale $k$ 的所有素因子。$k$ 可以是任意正整数，包括含 $\equiv 3$
mod 4 素因子的。

### 修正版假设可能成立但仍不直接 obstruct

可以尝试修正：**$h_i$ 的 primitive part $\tilde{h}_i$ 的奇素因子 $\equiv 1$
mod 4**。这是真的（来自 primitive Pythagorean triple 的标准结构定理）。

但 chain 里出现的 hypotenuse 是 primitive part × scale，scale 不受约束，
所以这个修正版假设**不能直接给出 blocker prime**。

---

## 二阶现象：mod-4 mass 守恒

恒等式 C $\Rightarrow$ 对任意素数 $p$，$v_p$ 在 LHS 和 RHS 守恒：

$$
v_p(h_1 h_3 - h_2 h_4) + v_p(h_1 h_3 + h_2 h_4)
= v_p(d-b) + v_p(a-c) + v_p(a+c) + v_p(b+d)
$$

特别地，所有 $\equiv 3 \pmod 4$ 素因子的总 multiplicity 在两边相等。`max_val=5000`
实证（1005 chains，sum-of-multiplicities）：

| 类别 | LHS | RHS |
|---|---|---|
| 素因子 = 2 | 8383 | 8383 |
| 素因子 ≡ 1 (mod 4) | 4059 | 4059 |
| 素因子 ≡ 3 (mod 4) | 7813 | 7813 |

完全守恒，但这是恒等式 C 的**直接推论**，不提供新信息。

注意 ≡ 3 (mod 4) 的总质量（7813）几乎是 ≡ 1 (mod 4) 的两倍。这反映了 chain
candidates 在 chain 边的差/和上"3 mod 4 素因子比 1 mod 4 多"的统计趋势，但这
本身不是 obstruction。

---

## 与 Peschmann 2026 §7(3) 的对比

Peschmann 在 perfect cuboid 上观察到 **88.4% of obstructed cases blockers
are $\equiv 1 \pmod 4$**，几乎没有 $\equiv 3$ 的 blocker。这跟本 worklog 在
chain 上的发现**截然相反**——chain candidates 的相关因子里 ≡ 3 mod 4 素因子
反而占多数。

可能的解释：cuboid 里的 quartic pair $f_1, f_2$ 是同质的，所以它们的素因子分
布受更强约束；chain 的 4 个 hypotenuse 完全独立，没有 cuboid 那种结构约束。

→ 这是 cuboid 与 chain 在算术结构上的实质差异，验证 IDEAS §5.4 的观察："对偶
EC / 4 个 hypotenuse 的对称性是 4-chain 特有的工具"，但**这个对称性并不会自
动给出 obstruction**。

---

## 主结论

| 项 | 结果 |
|---|---|
| 恒等式 A 数值验证 | 1005/1005 通过 ✅ |
| 恒等式 C 数值验证 | 1005/1005 通过 ✅ |
| §2.4 "h_i 奇素因子 ≡ 1 mod 4" 假设 | ❌ **错误**（来自对 Fermat 二平方定理的误用） |
| §2.4 blocker prime 论证 | ❌ **不成立**（基于错误假设） |
| 想法 1 提供 obstruction？ | ❌ 在 chain near-miss / 长方形 chain 上都不提供 |

---

## 后续路线

### 已废弃路线
- ~~"$h_i$ 都不含 ≡ 3 mod 4 素因子" → 矛盾 → blocker prime~~（基础假设错）

### 可能的 salvage 方向（低优先级）
1. **Primitive/scale 分解**：把每个 $h_i$ 写成 $k_i \tilde{h}_i$，研究 4 个
   primitive parts $\tilde{h}_1, \tilde{h}_2, \tilde{h}_3, \tilde{h}_4$ 之间
   是否有真正的算术约束。
2. **Mod p 同余**：对特定 $p$（特别是小 ≡ 3 mod 4 素数如 3, 7, 11），分析
   恒等式 C 在 mod $p^k$ 下的局部 obstruction。

### 高优先级转向（独立于想法 1）
3. **想法 3：Sage 2-descent**（IDEAS §4），从 dual EC probe 留下的 11 个候选
   的 Selmer group 结构入手。

---

## 输出物

### 脚本
- `scripts/analyze_hypotenuse_identity.py` — 主分析（恒等式数值验证 +
  mod-4 prime 分布统计）
- `scripts/find_h_3mod4_counterexamples.py` — 找出 §2.4 假设的最小反例

### 数据
- `results/hyp_identity_2000.jsonl` — 208 个 chain 的逐个分析
- `results/hyp_identity_5000.jsonl` — 1005 个 chain 的逐个分析

### 文档
- 本 worklog
- 待更新：`docs/CHAIN_STRUCTURE_IDEAS.md` §2.4 标记假设错误

---

## 复现命令

```bash
# 主分析（max_val=5000，约 1005 chains，几秒）
uv run python scripts/analyze_hypotenuse_identity.py \
    --max-val 5000 \
    --out results/hyp_identity_5000.jsonl

# 列出 §2.4 假设的最小反例
uv run python scripts/find_h_3mod4_counterexamples.py \
    results/hyp_identity_5000.jsonl --n 3
```
