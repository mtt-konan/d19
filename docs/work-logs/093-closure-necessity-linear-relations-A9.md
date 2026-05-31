# wl093 — A.9 closure-necessity：闭合 (N₁+N₂=A+B) 只是「正方形内」情形，全平面充要条件是 4 个线性关系

## 任务

承接 wl092 指认的真正开放杠杆 **closure-necessity**：

> 对一个 Harborth 反例，闭合 4-chain（`b = A+B−N` 也 concordant，即 `N₁+N₂=A+B`）
> 是否**必要**？若必要，则「concordant N 全部不闭合 ⇒ `no_solution`」对所有 rank
> 立即成立（factor_search 已穷尽所有整数 N），无需 Magma / canonical height。

本 wl 用初等几何把这个问题彻底厘清，结论分**纠错**与**强化**两部分。

## 结论先行

1. **纠错**：pipeline 的闭合判据（`analysis.check_chain_compatibility` 用
   `b=A+B−N`、`chain_closure_sieve.killed_at_modulus` 把 `T` 按 `A+B` 反射）只检验
   **和关系 `N₁+N₂=A+B`**。这条关系恰好对应反例点 **落在单位正方形内部**
   `0≤x≤1, 0≤y≤1`。项目此前的归约（MATH §7 要求 `a,b,c,d>0` 且 `a+c=b+d`）
   **默认了反例在正方形内**——这个前提之前从未明说，也没被论证。

2. **强化**：一个落在正方形**外部**的反例，满足的是另外**三个**线性关系之一，
   现判据一概不查。把四条关系合写，反例的**充要必要条件**是

   $$\{\,N_1+N_2,\ |N_1-N_2|\,\}\ \cap\ \{\,A+B,\ |A-B|\,\}\ \neq\ \varnothing.\qquad(\text{GEN-CLOSURE})$$

   它仍然只依赖 factor_search 穷尽出的**有限** concordant 集合，对**所有 rank**
   成立、毫秒级、无 Magma / height。实测把判据从「正方形内」升级到「全平面」后，
   `max_hyp≤2000` 的 8220 个 safe-pass pair（含 67 个 multi-N）**0 个**满足任一
   关系——把 wl092 的「无反例」证据从正方形内扩到全平面。

3. **诚实残留**：把「无 GEN-CLOSURE ⇒ `no_solution`」做成对**所有 (A,B)** 严格的
   判定器，还需处理 §8.6 的 **gcd-scaling 覆盖**问题（`generate_ab_pairs` 只产
   reduced 互素对，非互素腿的反例在约化对上不可见）。这一 gap 对**原有**和**升级后**
   判据同样适用，是另一条独立未解项，本 wl 不解决，只明确标注。

## 一、几何推导：四个角距离 → 两腿的和/差

Harborth 反例 = 平面内有理点 `P=(x,y)`，到单位正方形四角 `(0,0),(1,0),(1,1),(0,1)`
距离全有理（由任意三距离有理推出 `x,y∈ℚ`，MATH §1）。取公分母写
`x=u/n, y=v/n`（`u,v∈ℤ`，`n>0`）。四个角距离平方乘以 `n²` 得

```
u²       + v²       = □     角 (0,0)
(u−n)²   + v²       = □     角 (1,0)
(u−n)²   + (v−n)²   = □     角 (1,1)
u²       + (v−n)²   = □     角 (0,1)
```

把**水平两腿**记 `(A,B):=(|u|, |u−n|)`，**竖直两腿**记 `(N₁,N₂):=(|v|, |v−n|)`。
上面四式正好说明 `N₁,N₂` 都是 `(A,B)` 的 concordant 值（每个组合都是平方）：

```
N₁²+A² = v²+u²       = □
N₁²+B² = v²+(u−n)²   = □
N₂²+A² = (v−n)²+u²   = □
N₂²+B² = (v−n)²+(u−n)² = □
```

**关键引理（腿的和/差恒含 n）**：对任意整数 `u` 与 `n>0`，

```
|u| + |u−n| = n          当 0 ≤ u ≤ n
| |u| − |u−n| | = n      当 u < 0 或 u > n
```

证：`0≤u≤n` 时 `|u|+|u−n| = u+(n−u)=n`；`u>n` 时 `|u|−|u−n|=u−(u−n)=n`；
`u<0` 时 `|u−n|−|u| = (n−u)−(−u)=n`。∎

所以**恰好一个** `{A+B, |A−B|}` 等于 `n`，也**恰好一个** `{N₁+N₂, |N₁−N₂|}` 等于 `n`。
公共值 `n` 同时落在两个二元集里，立得 (GEN-CLOSURE)。区域对照：

| 反例点位置 | 水平 (u) | 竖直 (v) | 满足的关系 |
|---|---|---|---|
| 正方形**内** | `A+B=n` | `N₁+N₂=n` | **`N₁+N₂ = A+B`**（现判据） |
| 左右外 | `\|A−B\|=n` | `N₁+N₂=n` | `N₁+N₂ = \|A−B\|` |
| 上下外 | `A+B=n` | `\|N₁−N₂\|=n` | `\|N₁−N₂\| = A+B` |
| 四角外 | `\|A−B\|=n` | `\|N₁−N₂\|=n` | `\|N₁−N₂\| = \|A−B\|` |

（交换「水平当 (A,B)」与「竖直当 (A,B)」的角色，上下外↔左右外互换，仍非「和=和」。）

**充分性**：反过来给定 reduced `(A,B)` 与两个 concordant `N₁,N₂`，若存在公共值
`m∈{A+B,|A−B|}∩{N₁+N₂,|N₁−N₂|}`，令 `n=m` 可还原出 `u,v` 与一个有理点 `P`，其四个
角距离全有理（边排除定理 MATH §4 保证不退化到延伸边）。故 (GEN-CLOSURE) 是
**充要**条件（模 §8.6 的 gcd-scaling，见 §三）。

## 二、为什么现判据只覆盖「正方形内」

`check_chain_compatibility(A,B,N)`：

```python
b = A + B - N            # 隐含 N₁=N, N₂=b, 且 N₁+N₂=A+B
if b <= 0: return False   # 要求 b>0  →  0<N<A+B  →  正方形内
return is_sq(B*B+b*b) and is_sq(b*b+A*A)
```

`chain_closure_sieve.killed_at_modulus`：把 `T` 仅按 `A+B` 反射，
`T ∩ ((A+B)−T)`。两者都只编码 `N₁+N₂=A+B`，即上表第一行。`b>0` 这个看似无害的
正性约束，几何上正是「反例在正方形内」。**项目从未论证反例可 WLOG 取在正方形内**：

- 单位正方形的等距对称群只有 `D4`（8 阶），它把正方形映成自身，**外部点仍映到外部**，
  无法把外部反例搬进内部。
- 「到四角有理距离」未发现比 `D4` 更大的保距/保有理结构，故 WLOG-inside **不是免费的**。

因此严格地说，「所有 concordant N 不满足 `N₁+N₂=A+B` ⇒ 无反例」此前只排除了
**正方形内**反例，外部反例从未被这条判据触及。

## 三、诚实残留：gcd-scaling 覆盖（§8.6）

`generate_ab_pairs` 把 `(A,B)` 除掉 `g=gcd(A,B)` 后只产**互素**对。若反例的水平腿
`(A,B)=g·(A',B')` 非互素，竖直腿 `N₁,N₂` 与同一个 `n` 绑定，约化对 `(A',B')` 的
concordant 值**不是** `N_i` 的简单缩放（§8.6：`E_{kA,kB}≅E_{A,B}` 保 rank，但整数
concordant N 不随 k 缩放）。所以「reduced 对上 factor_search 穷尽 ⇒ 全平面判定」对
**非互素腿反例**有覆盖缺口。

要点：这个 gap 对**原有 sum-only 判据**和**本 wl 的 GEN-CLOSURE 升级**完全相同——
升级没有引入新缺口，只是把「正方形内」补成「全平面（互素腿）」。彻底封闭还需单独处理
§8.6（或依赖 chain_fast 的直接 O(n²) 整数枚举，它不经约化、在搜索界内已穷尽）。

## 四、实测（`scripts/theory/closure_necessity_relations.py`）

```
(1) 区域/腿关系 sanity：5 个采样点（内/右外/上外/四角外/竖直中线）全部
    与「内⟺和、外⟺差」一致。
(2) GEN-CLOSURE 扫描：
    max_hyp= 500 : 540 pair (7 multi-N)   25 ms  — sum 闭合 0，非 sum 关系 0
    max_hyp=1000 : 2120 pair (19 multi-N) 118 ms — 0 / 0
    max_hyp=2000 : 8220 pair (67 multi-N) 599 ms — 0 / 0
(3) 7 个残余 hard_case（≥2 concordant N、sum 闭合失败）对四关系制表：
    无一在 {N_i+N_j,|N_i−N_j|} ∩ {A+B,|A−B|} 命中 → 全平面下仍 0 反例。
```

`(25,91)` 例：`A+B=116, |A−B|=66`；concordant `N=[60,312]`；
sums `=[120,372,624]`、diffs `=[252]`——与 `{116,66}` 不交。其余 6 个同理。

## 五、结论 / 建议

- **A.9 部分解决**：closure-necessity 的几何内容已厘清。`N₁+N₂=A+B` 是**正方形内**的
  必要条件；全平面的充要必要条件是 **GEN-CLOSURE**（四个线性关系）。这纠正了项目
  归约「默认反例在正方形内」的隐含前提。
- **可立即落地的升级（建议，未在本 PR 改生产判据）**：把 `check_chain_compatibility`
  / `killed_at_modulus` 从「只查 `A+B` 反射」扩成「查 `{N₁+N₂,|N₁−N₂|}∩{A+B,|A−B|}`」。
  代价极小、全 rank、无 Magma；可把残余 inconclusive hard_case 在**全平面（互素腿）**
  下判成 `no_solution`。因会改变 `no_solution` 语义并牵动既有结果/测试，留待单独 PR +
  用户确认。
- **仍开放**：(a) §8.6 gcd-scaling 覆盖——非互素腿反例的约化对可见性；(b) rank≥2
  的结论性工具 Chabauty（需 Magma，wl090 F.2）/ Brauer–Manin（A.4）。GEN-CLOSURE
  不依赖这些，但「彻底证明 Harborth」仍需 (a)(b) 之一收尾。

## 复现

```bash
PYTHONPATH=src uv run python scripts/theory/closure_necessity_relations.py --max-hyp 500
PYTHONPATH=src uv run python scripts/theory/closure_necessity_relations.py --max-hyp 2000
```

## 参考

- `src/rational_distance/concordant/analysis.py::check_chain_compatibility`（`b=A+B−N`）
- `src/rational_distance/concordant/chain_closure_sieve.py`（按 `A+B` 反射的 mod 筛）
- `src/rational_distance/concordant/factor_search.py`（穷尽 concordant N，自证完整）
- `src/rational_distance/concordant/pairs.py`（`generate_ab_pairs` 只产互素对 → §8.6 caveat）
- MATH.md §1（三距离有理 ⇒ x,y 有理）、§3（角距离公式）、§4（边排除）、§7（4-chain
  归约，隐含 `a,b,c,d>0` ⇒ 正方形内）、§8.6（gcd 归约下 concordant N 不缩放）
- wl092（closure-necessity 提出）、wl077 / B.6（height-bound 已关闭）、OPEN_DIRECTIONS A.9
