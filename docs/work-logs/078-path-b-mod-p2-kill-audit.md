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

## 九、状态

- ✅ Audit 工具 + max_hyp=1M 实测
- ✅ 6 个 dual-only pair 抓出，证明 dual sieve 不可省
- ✅ Refined Conjecture B' (含 dual sieve)
- ⏳ Conjecture B' 严格证明 (multi-N → mod p² → kill 的代数推导)
- ⏳ 推到 max_hyp=2M / 5M 看是否仍在 STANDARD_MODULI 范围内
