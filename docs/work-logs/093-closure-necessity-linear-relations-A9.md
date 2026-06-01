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

## 四之二、大尺度实证：sum-closure 到 max_hyp=5,000,000

为把「sum 闭合 `N₁+N₂=A+B` 实证失败」的尺度从前述 max_hyp≤2000 推到百万级，复用
pivot-on-N 多-N **生成式**算法（对每个 `A` 因子分解 `A²` 直接还原全部 concordant `N`，
再按 `N` 分组；配合最小质因子线性筛 O(log A)/A，`iter_concordant_a_n`）。它只产**约化
互素**多-N pair，正是 §8.6 caveat 覆盖的那一类。

| max_hyp | multi-N pair | k 直方图 | closure | 时间 | 峰值 RSS |
|---|---|---|---|---|---|
| 1,000,000 | 111,090 | {2:109891, 3:1146, 4:50, **5:3**} | **0** | 40s | 0.88 GiB |
| 2,000,000 | 226,120 | {2:224219, 3:1814, 4:83, **5:4**} | **0** | 92s | 2.05 GiB |
| 5,000,000 | 580,828 | {2:577237, 3:3451, 4:134, **5:6**} | **0** | 270s | 5.92 GiB |
| 7,000,000 | 822,108 | {2:817591, 3:4348, 4:161, **5:8**} | **0** | 148s† | 5.56 GiB† |

（†7M 行用的是 §四之三 优化后扫描器，Cython + `--shards 8`；故时间/峰值不与上方基线行同条件，
仅作「纯内存封顶」实证。k=5 saturated pair 在 1M 就已出现；**到 7M 仍无 k=6**。
`closure_necessity_relations.py` 的小尺度结论一致：max_hyp≤2000 全平面四关系也 0 反例。）

**纯内存封顶 ≈ 7M（非先前估的 10–12M）**。10,000,000 在 8 GiB 机器上 **OOM 被杀**
（anon-rss 7.8 GB）。瓶颈是**关系排序阶段**而非 pair 缓冲：10M 时关系约 3 亿条，
`argsort(N)` 的索引数组（int64）+ 重排副本叠加峰值 ~8.7 GiB——`--shards` 只压下游 emit
缓冲、压不到这个 sort。故先前「~10–12M」高估了，没计排序翻倍。7M（5.56 GiB）能跑完、
是这台盒子的实际封顶；≥8M 需把关系排序也分块（外部排序）或换大内存机。

**内存：为何能上 5M**。原 `fast_multi_concordant_pairs`（`scripts/multi_n/fast_multi_concordant_scan.py`）
用 Python `dict` 存关系，max_hyp=2e6 时 `a_sets`+`pairs_with_n` 合计 >7.8 GiB，在 8 GiB
机器上 **OOM**（exit 137）——瓶颈是**内存不是时间**（dict 撑 5.3 GiB 实际只装 ~0.6 GB
原始 (N,A) 数据）。新增 `scripts/multi_n/fast_multi_concordant_scan_numpy.py`：把关系流存进
**numpy 数组**（int64 N + int32 A），两次排序代替两个 dict——
(1) 按 N 排序、走等值游程得到 concordant 桶；(2) 每对编码成 `key=ai·(H+1)+aj`，排序后
游程长度 ≥2 即「共享 k≥2 个 N 的 pair」。pair 写进**可增长 numpy 缓冲**（不建百万级小数组 /
大 Python list）。峰值 5M=5.92 GiB（vs dict 的 ~13 GiB 外推），1M/2M 与库函数**精确一致**
（111,090 / 226,120）。

**意义**：到 k=5、58 万个约化互素多-N pair（max_hyp=5e6），`N₁+N₂=A+B` 仍**全部失败**（0）。
把 §四（正方形内、sum 关系）的无反例实证从 max_hyp=2000 延伸到 **5,000,000**，与 wl046–052
「closure 失败是结构性、非 k 不够」一致（wl052 外推「k=5 要 500k–1M 量级」——1M 实锤 3 个）。
注意这是 **sum 关系**（正方形内）的扩尺度；全平面四关系 GEN-CLOSURE 的扩尺度仍只到
max_hyp=2000（§四），因 `closure_necessity_relations.py` 另需 safe-pass 过滤。

**RAM 墙与更大尺度**：numpy 版峰值 ~线性于关系数+pair 数，5M=5.92 GiB 已近 8 GiB 上限，
≥8–10M 需 disk（**外部排序**：定长记录顺序写盘、分片排序——非「磁盘当 swap 的随机访问」，
顺序 IO 可控，盘量小，5M 级仅 ~1–3 GB）。本仓库当前需求未到此规模，未实现。

## 四之三、扫描器三轴优化（省内存 + Cython + 并行，每步实测）

把 §四之二 的 numpy 扫描器沿三条**正交**轴优化，每步用 1M/2M 对拍（计数必须仍是
111,090 / 226,120）并实测时间/峰值 RSS。机器：8 GiB RAM、2 CPU。所有计数全程精确一致。

**相位剖析（Cython 前，5M）**：生成 `iter_concordant_a_n` ≈ 190s（~80%），numpy 排序 +
桶内出对 + 去重 ≈ 50s。Cython 化生成后瓶颈转移——**桶内「出对」嵌套循环**（gcd+奇偶+打包，
发 8650 万对）成了 5M 的 ~52s 大头，生成只剩 2.5s。故两段纯整数循环都 Cython 化。

| 版本 | 1M 时间 | 1M 峰值 | 2M 时间 | 2M 峰值 | 5M 时间 | 5M 峰值 |
|---|---|---|---|---|---|---|
| 基线 numpy（§四之二） | 40s | 0.88 | 90s | 2.00 | 270s | 5.92 |
| 步骤1 省内存（ai 分片 s4 + quicksort + numpy 边界） | 35s | 0.88 | 104s | **1.41** | 179s | **3.86** |
| 步骤2 Cython（生成+出对内核） s1 | **9.8s** | 0.87 | **25s** | 1.99 | **76s** | 5.89 |
| 步骤2 Cython s4（分片省内存） | — | — | 62s | **1.39** | 85s | **3.83** |
| 步骤3 并行 workers=2（含 Cython） | **7.2s** | 0.97† | **17.5s** | 2.17† | **56s** | 6.34† |

（†并行峰值为**最大子进程** RSS；共享内存把已排序关系映射进每个 worker，故子进程驻留更高。）

**步骤1 — 省内存（结构）**。`ai % K` 分片出对把 pair 缓冲降到 1/K；argsort 由稳定
mergesort 改 **quicksort**（introsort，省 O(n) scratch）；桶边界全程保持 **numpy 整型数组**
（不 `.tolist()` 出百万级 Python int）；末片前显式释放关系数组再做 pair 排序。
5M 峰值 5.92→3.86 GiB（−35%）。注意分片只压 **pair-emit 缓冲**，压不到上游关系排序，
故实测纯内存封顶约 **7M**（10M OOM，见 §四之二），而非先前估的 10–12M。
（N 秩压缩用 `np.unique` 试过但 `np.unique` 自身的 argsort+inverse 反而抬内存，已回退。）

**步骤2 — Cython（提速）**。`scripts/multi_n/_concordant_gen.pyx`：把 SPF 线性筛、每个 A
的 `A²` 除子枚举、(A,N) 发射，以及桶内出对（含 C 版 Euclid gcd + `qsort`）全部下沉到 C，
直接写进 numpy 数组（均 ≤ int64）。**两遍**设计（先计数、再按精确大小分配并填充），峰值仅
输出数组、无 malloc/realloc/memcpy 翻倍。实测：5M 生成 190s→**2.5s**（~75×）、出对
96s（Python）→52s（Cython 两遍）。总时间 270→76s（s1）。`.so` 平台相关、**不入库**，用
`uv run python scripts/multi_n/_build_gen.py build_ext --inplace` 现场编译；缺 `.so` 时
扫描器自动回退纯 Python 路径（已验证 100k 计数一致）。

**步骤3 — 并行（提速）**。`scan_numpy_parallel`：父进程**串行**生成+排序关系一次，经
`multiprocessing.shared_memory` 发布只读数组；K 个 spawn worker 各跑一个 ai-分片的
`emit_pairs`（Cython 已内建 shard/nshards 过滤）+ 局部排序去重，返回各自小结果 dict（分片
按 ai 划分、键不碰撞，父进程直接合并）。2 核实测 5M 76→56s（1.35×）；加速被 Amdahl
下界（串行 gen+sort ~15s 不可并行）+ 共享内存复制的内存开销限制。子进程峰值偏高（6.34 GiB）
使**并行=提速档、分片 s4=省内存档**；更多核 / 出对更重的区间并行收益更大。

**总结**：1M 40→7.2s（5.6×）、2M 90→17.5s（5.1×）、5M 270→56s（4.8×），计数精确不变；
省内存档 5M 5.92→3.83 GiB。三轴正交可叠加。实测本机纯内存封顶约 7M（822,108 pair、
closure 仍 0、仍无 k=6）；≥8M 因关系排序翻倍需外部排序（把 N-sort 也分块）或大内存机。

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
