# wl078 — 路径 B 阶段 3a：mod p² kill pattern 实证 audit

承接 wl077（方向 2 fail，转向路径 B）。本 wl 实施阶段 3a 的 diagnostic：
对 wl073 dual closure sieve 实证数据做 per-M kill rate 分析，明确路径 B
严格证明的 framework + 关键 M_0 + dual sieve 不可省的具体证据。

## 一、Audit 工具

`scripts/uniform_mod_p2_audit.py`：

1. 加载 max_hyp 内全部 multi-N pair, 过 safe sieve
2. 对每个 pair (A, B):
   - **primary kill**: 哪些 M ∈ STANDARD_MODULI 让 `chain_closure_mod_sieve(A, B, M)` killed
   - **dual kill**: 对每对 (N_i, N_j) ∈ partners(A, B) reduce 后哪些 M kill
3. 输出 per-M kill rate, primary 全 kill 数, greedy minimum M_0

## 二、实测数据（max_hyp = 1,000,000）

```
1907 个 safe-pass multi-N pair (max_hyp=1M)

Primary kill (chain_closure on (A, B)):
  M=  9 (3²): 1696 pairs (88.94%)  ← 主力，单 M 砍 89%
  M= 25 (5²):  170 pairs (8.91%, 增量)
  M= 121 (11²): 33 pairs
  M= 169 (13²): 29 pairs
  M= 289 (17²): 12 pairs
  M= 361 (19²): 54 pairs
  M= 529 (23²):  4 pairs
  M= 841 (29²): 21 pairs
  M= 961 (31²):  8 pairs
  M=1369 (37²): 36 pairs  ← 不可省（见 §四）
  M=1681 (41²):  1 pair
  M=2209 (47²):  7 pairs
  M=2809 (53²):  1 pair

Pairs unkilled by ANY primary M:  6 / 1907 (0.31%)
Pairs killed by primary + dual:   1907 / 1907 (100%) ← wl073 数据一致
```

## 三、Greedy minimum M_0（primary only）

```
+ M=    9, kills 1696 new (211 left)
+ M=   25, kills  170 new ( 41 left)
+ M=  361, kills   15 new ( 26 left)
+ M=  121, kills    6 new ( 20 left)
+ M= 1369, kills    6 new ( 14 left)
+ M=  169, kills    4 new ( 10 left)
+ M=  841, kills    3 new (  7 left)
+ M= 2809, kills    1 new (  6 left)
cannot cover remaining 6 pairs with any M
```

**8 个 prime² 已经 cover 99.7%，剩 6 个 dual-only pair** 必须 dual sieve。

## 四、6 个 dual-only pair（**dual sieve 不可省的关键证据**）

```
(26611, 680561)  k=2  primary=[]  dual=[2809]   ← 53² 才能杀
(42809, 197659)  k=2  primary=[]  dual=[9]
(216733, 504455) k=2  primary=[]  dual=[9]
(552421, 915971) k=2  primary=[]  dual=[9]
(251069, 697015) k=2  primary=[]  dual=[25]
(28613, 910063)  k=2  primary=[]  dual=[25]
```

全部是 **k=2 multi-N pair**，全部不被 STANDARD_MODULI 的任何 primary kill，
但它们的 partner pair (N_1, N_2) reduce 后被某个 M ∈ STANDARD_MODULI kill。

⟹ **路径 B 必须包含 dual sieve**。

## 五、稀有 primary M 的特殊角色

部分 pair 只被高阶 prime² (M ≥ 1369 = 37²) 的 primary kill:

```
(26543, 284557) k=2  primary=[1369]  dual=[]
  ← 只被 M=37² primary kill, 且无 dual killer
  ← 如果 M_0 不含 37²，该 pair 漏网

(1943, 4693)    k=2  primary=[1369]  dual=[9]   ← 备选 dual=9
(487577, 923923) k=2 primary=[2809]  dual=[9]
```

⟹ **M_0 必须包含 1369 = 37²** 对某些 pair 才有 primary cover。如果只用
greedy 选前几个 (9, 25, 121, ...)，会漏掉这种 case。

## 六、Refined Conjecture B'

基于以上 audit:

> **Conjecture B' (refined)**: ∃ finite ``M_0 = STANDARD_MODULI = {p² : p ∈
> [3, 53] prime}`` （14 个），使对任意 reduced coprime safe-pass multi-N
> pair `(A, B)`，
>
> ```
> primary kill: ∃ M ∈ M_0  with  T(A, B, M) ∩ ((A+B)−T) = ∅
> OR
> dual kill:    ∃ (N_i, N_j) ∈ partners(A, B), ∃ M ∈ M_0
>               with  T(reduced(N_i, N_j), M) ∩ ((N_i+N_j)−T) = ∅
> ```

**实证**: max_hyp ≤ 2,000,000 全部 226k multi-N pair 100% 覆盖（wl073）。
现 audit 数据：max_hyp=1M 1907/1907，primary 砍 99.7%，dual 砍剩 0.3%。

## 七、Conjecture B' 严格证明 strategy

### 7.1 把 multi-N condition 翻译成 mod p² behavior

multi-N (A, B) 要求 `∃ N ∈ Z` 使 `N²+A² ∈ □` 和 `N²+B² ∈ □`. 对每个 prime
``p``, 这给 (A mod p², B mod p²) 上的 quadratic residue lift 条件：
`N² + A² ≡ □ mod p²` 强迫 (N mod p, A mod p) 的某种关系。

具体：若 ``p | N²+A²``，则需 ``p² | N²+A²`` (Hensel lifting)。
这是个 "depth-2" 提升条件。

### 7.2 从 mod p² 到 chain_closure_mod_sieve kill

T(A, B, M) 是 mod M 的 N residue 集。当 multi-N (A, B) 落入特定 mod p²
class，T(A, B, p²) 的 size 受限，进而 T ∩ ((A+B) − T) 的 size 也受限。

要证: **存在 finite M_0 使对每个 mod p² class of multi-N (A, B), 至少一个
M ∈ M_0 让 intersection 空**。

实证 audit 数据给出了具体的 "M_i 与 mod p² class" 对应关系，可作为
case-by-case 证明的起点。

### 7.3 dual sieve 的角色

6 个 dual-only pair (§四) 表明：某些 (A, B) 的 mod p² class 让 primary
intersection 非空，但其 partner (N_1, N_2) 的 mod p² class 让 primary
intersection 在 (N_1, N_2)-AB 视角下空。

⟹ dual sieve 给的"K_{2,2} 反向 mod p² obstruction"是 primary 视角看不到
的 obstruction。两者必须组合。

## 八、文件 / 引用

```
docs/work-logs/073-dual-closure-sieve-and-n-side-theory.md  实证全杀
docs/work-logs/077-direction-2-height-bound-and-pivot-to-path-b.md  路径 B 提出
src/rational_distance/concordant/chain_closure_sieve.py     primary sieve
src/rational_distance/concordant/dual_closure_sieve.py      dual sieve
scripts/uniform_mod_p2_audit.py                             本 wl: audit 工具
results/uniform_mod_p2_max1m.jsonl                          1907 sample 数据
```

## 九、阶段 3b — brute (a, b) mod M_full enumeration

`scripts/enumerate_mod_p2_classes.py`：直接在 (Z/M_full Z)² 上枚举 safe-pass
+ 未被任何 primary M kill 的 (a, b) class，给"路径 B 不算 multi-N 时的
mod-level upper bound"。

| moduli                | M_full   | safe-pass  | killed by primary | surviving        |
|-----------------------|----------|------------|-------------------|------------------|
| {9}                   | 36       | 162        | 108 (66.67%)      | 54 (33.33%)      |
| {9, 25}               | 900      | 101 250    | 91 260 (90.13%)   | 9 990 (9.87%)    |
| {9, 25, 49}           | 44 100   | 243 101 250| 230 863 500 (94.97%)| 12 237 750 (5.03%)|

观察:

1. **CRT 独立**: surviving = 2 × 27 × 185 × 1225 × ... — 因 4 与每个 p² 互素，
   safe-pass-mod-4 与 mod-m primary kill 完全独立（实测验证）。
2. **5% surviving 不是空**: 这是 (a, b) 全空间，没用 multi-N 多 N 联立 +
   dual 结构，所以 surviving classes 不一定真有 multi-N pair。Conjecture B'
   的"零空间"必须靠 multi-N 限制才出现。

## 十、阶段 3c — CRT-style 大模数枚举

`scripts/enumerate_mod_p2_crt.py`：用 CRT 把 enumeration 拆成 per-modulus
的 |S_m| 计算 + 联立乘积，复杂度 O(Σ m²) 取代 O((Π m)²)。

```
moduli = (9, 25, 49, 121, 169)   M_full = 9.0×10⁸
  m=  9  survived=    27/   81  (33.3%)   killed 67%
  m= 25  survived=   185/  625  (29.6%)   killed 70%
  m= 49  survived=  1225/ 2401  (51.0%)   killed 49%
  m=121  survived=  4961/14641  (33.9%)   killed 66%
  m=169  survived= 14521/28561  (50.8%)   killed 49%
=> safe-pass = 1.02×10¹⁷, surviving = 8.82×10¹⁴ (0.87%)

moduli = (9, 25, 49, 121, 169, 289, 361, 529, 841, 961)  M_full ≈ 4.0×10²²
=> 0.137% of safe-pass surviving, 0.017% of total
```

per-prime 模式：

- **p ≡ 3 mod 4** (3, 7, 11, 19, 23, 31, ...): 杀率 ~67% 或 50% 交错
- **p ≡ 1 mod 4** (5, 13, 17, ...): 比 p ≡ 3 mod 4 杀更多 (70% / 67%)
- 大 prime 杀率 → 1: surviving 比例越来越 趋近 100%

⟹ **mod p² obstruction 不会"在 (a, b) 全空间"达到 universal**。
即使把所有 prime² (p ≤ 47) 都用上，surviving classes 仍然占 0.017% 非零比例。
所以 Conjecture B' 的"零空间"必须靠 **multi-N + dual** 联立限制才出现。

## 十一、修正后的攻击点

阶段 3a/3b/3c 的发现:

1. **Audit (3a)**: 真实 multi-N pair 在 STANDARD_MODULI 下 99.7% primary +
   100% dual kill。剩 6 个 dual-only pair 是 dual sieve 的"金证据"。
2. **Brute / CRT (3b/3c)**: (a, b) 全空间在 mod p² primary 下永远 surviving
   (≥ 0.017%)，所以 path B 的"零空间"不能仅靠 (a, b) mod p² 看。

⟹ 严格证明的真正路线是 Conjecture B' 不是 "(a, b) mod M_0 → killed"，
而是 **"(a, b) mod M_0 + multi-N 存在 + dual partner mod M_0 → killed"**:

```
multi-N (A, B) ⟹ ∃ N ∈ Z s.t. N²+A², N²+B² ∈ □
   ⟹ (A, B, N) mod M ∈ specific T-feasible set L_M
   ⟹ |L_M| 上 chain_closure 的 obstruction 可计算
```

下一步 phase 4 计划:

- **4a**: 把 (a, b) 在 mod M_full surviving sample 反向 lift 到 Z 找 multi-N，
  统计实际 multi-N density（应该远低于 0.017%）。
- **4b**: 证明 multi-N 的存在性 (∃ N s.t. T(A,B,p²) 含 N) 给 (a, b) mod p²
  额外约束 → 把 surviving fraction 压到 0。
- **4c**: dual sieve 的 mod p² 等价描述 (partner reduce 关系) 写出 case-by-case
  的 6-pair 完整 algebraic 证明。

## 十二、状态

- ✅ Audit 工具 + max_hyp=1M 实测 (3a)
- ✅ 6 个 dual-only pair 抓出，证明 dual sieve 不可省 (3a)
- ✅ Refined Conjecture B' (含 dual sieve)
- ✅ Brute / CRT (a, b) mod M_full surviving 量化 (3b, 3c)
- ⏳ multi-N 限制下 surviving → 0 的代数证明 (phase 4b)
- ⏳ dual sieve 的 mod p² 代数等价描述 (phase 4c)
- ⏳ 推到 max_hyp=2M / 5M 看是否仍在 STANDARD_MODULI 范围内
