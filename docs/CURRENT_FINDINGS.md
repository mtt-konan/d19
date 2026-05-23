# 当前关键结论

这份文档只记“现在已经基本确认的事情”，不展开长推导。

## 一、`concordant`（active）方向：已确认结论

### 1. “后两条成立”对应 concordant form / 椭圆曲线结构

对固定 `(A,B)`，找 `N` 使：
- `N² + A²` 是平方
- `N² + B²` 是平方

这件事本质上就是 concordant form 问题，也可以写成椭圆曲线。当前已经整理出的关键形式是：

```text
Y² = X(X + A²)(X + B²), 其中 X = N²
```

这说明：
- “后两条成立”不是随便试出来的巧合，背后有成熟的数论结构。
- 但目前还没有一条“已证明且可工程化”的路径，能把这件事直接推成完整四顶点解。

### 2. pair 级 `mod1680` 已经确认是空筛，不再作为正式方向

之前试过一版 `concordant` 的 pair 级 `mod1680` 前筛，想法是：

- 对固定 `(A,B)`
- 先看模 `16,3,5,7`
- 是否存在某个 `N` 的剩余类
- 能让 `N² + A²` 和 `N² + B²` 都“看起来可能是平方”

现在已经确认：

- 这不是实现 bug
- 而是这个条件本身太弱
- 因为 `N ≡ 0` 会让任何 `(A,B)` 都直接通过

**澄清一个常见误解**：`mod1680` 不是"被前面别的筛抢了功能"才没筛掉东西的。
实测在 `max_hyp=2000` 时 `99311` 个 pair 它砍 **0** 个——它跟谁都没有功能重叠，
它单独跑也是空筛。原因是数学条件本身就有 `N ≡ 0` 这个万能见证。

跟 `safe_sieve` (`(A,B)` 都奇 + `(A+B)%4==0`) 的真正区别：

- `mod1680` 只看后两条 concordant 条件，`N` 是自由的；`N ≡ 0` 总能见证
- `safe_sieve` 把完整 4-chain 的 4 个平方条件一起拉回来，`N` 和 `b = A+B-N`
  绑定，`N ≡ 0` 就破不动了
- 这是"维度"上的区别，不是"模数"上的区别

所以这条路已经被排除为有效前筛，只保留实验记录，不再继续作为运行时特性推进。

### 3. 当前最值得落地的安全前筛，是 reduced `(A,B)` 上的 2-adic 必要条件

对当前 `generate_ab_pairs()` 产出的 reduced `(A,B)`，完整 4-chain 的第一版安全必要条件已经固定为：

- `A` 必须是奇数
- `B` 必须是奇数
- `(A + B) % 4 == 0`

这条结论的重要性在于：

- 它是必要条件，不会误杀真完整候选
- 计算极便宜
- 可以在送进 PARI 之前先砍掉大量 pair

这条条件现在已经接成实验开关 `--safe-pair-sieve`，而且实测筛力很强：

- `max_hyp=1000`：`24197 -> 2120`，拒绝约 `91.2%`
- `max_hyp=2000`：`99311 -> 8220`，拒绝约 `91.7%`
- `time_find_concordant_s` 也跟着从 `23.8s -> 2.0s`、`96.4s -> 7.7s`

这说明它不仅数学上站得住，而且工程上也真的值钱。

### 4. “半解很多，完整正方形解极少”是稳定现象

像下面这些数：
- `(264,315,420)`
- `(264,352,420)`
- `(105,140,480)`
- `(105,360,480)`

都说明一件事：
- 找到 `N` 让 `N²+A²` 和 `N²+B²` 同时是平方，并不罕见。
- 但把它重新塞回完整四边闭环（满足 `a + c = b + d`）以后，通常还是会失败。

也就是说，半解不少，完整解极少。

## 二、`chain-fast`（baseline）方向：已确认结论

### 1. 当前统一入口

所有主要搜索都已经统一到：

```bash
uv run python scripts/search.py ...
```

目前主要子命令有：
- `parametric`
- `ec`
- `chain`
- `chain-fast`
- `concordant`

### 2. `chain-fast` 是最可信的 baseline 搜索器

原因很简单：
- 它直接瞄准正方形主问题
- 已经具备 `numpy` 加速和 SQLite 持久化

### 2.1 `mod` 预筛：能降 `C3` 候选，但在现有实验里不一定更快

最近一轮 `mod` 预筛实验说明：

- 它能明显减少进入 `C3` 精确判定的候选数
- 但总 wall time 在已测范围内并不一定更快

这件事用更谨慎的说法是：在当前实现与测试配置下，`mod` 预筛带来的候选减少，并没有稳定转化为 wall time 收益。对 `chain-fast` 来说，更值钱的仍然是：

- 更早的结构剪枝
- 更早的分桶 / 分组

### 2.2 `10w` 结构统计已经出现稳定信号

最新一轮 `max_hyp=100000` 的结构桶统计说明：

- `g = gcd(t1, s2)` 越大的桶，越容易活到 `C3`
- `mod 8` 模类也开始出现稳定偏向，不只是随机波动
- `delta = s-t` 这条线暂时有信号，但还不够干净

这说明后面如果要继续做新筛，最值得优先盯的是：

- `g_bucket`
- `residue_bucket`

而不是一上来就把 `delta` 写成硬剪枝。

### 2.3 原始 near-miss 明细在 `10w` 已经碰到 SQLite 上限

同一轮 `100000` 实测还暴露了一个很实际的问题：

- 搜索本身能跑完
- 但把超大的 near-miss 明细写进 SQLite 时，已经会撞到 `INTEGER` 上限

这说明以后大范围长跑更稳的方向会是：

- 存聚合统计
- 存代表样本
- 不再默认指望把所有超大整数明细都直接塞进 SQLite（SQLite `INTEGER` 是 64-bit 有符号整型）

### 3. `numpy` 快路径有安全上限

`chain-fast` 的 `numpy` 路径受 `int64` 限制，大约只能安全跑到：

- `max_hyp ≈ 36000`

超过这个范围后，程序会回退到 Python 精确整数逻辑。这不是程序坏了，而是为了避免静默溢出。

## 三、跨方向：已确认的数学结论

### 1. 长方形解很多，正方形解仍未找到

当前搜索很容易找到只满足前四条勾股条件的解，但还没有找到满足 `a + c = b + d` 的完整正方形解。

### 2. 交叉乘积族不可能给出正方形解

形如 `(a,b,c,d) = (pm, qm, qn, pn)` 的解会自动满足 `ac = bd`，并且可以证明：

`a + c - (b + d) = (p-q)(m-n) != 0`

所以这类结果不可能满足正方形条件，已经被排除。

## 四、为什么现在还难（高置信版本）

难点不是“搜索还不够快”这么简单，而是两层困难叠在一起：
- 数学上，缺少更强的必要条件去提前砍掉大量候选
- 工程上，主搜索复杂度仍然是 O(n²)

所以现在最值钱的进展通常不是“多跑一点”，而是：
- 找到新的筛选规律
- 证明某一大类结构根本不可能
- 或者把搜索问题改写成更硬的数论问题

## 五、2026-05 新增已确认结论（worklog 033–035）

针对 `archive/CHAIN_STRUCTURE_IDEAS.md`（已归档）的四个想法做了系统性实证：

### 1. dual EC 视角不提供 free obstruction（worklog 033）

在 150 个 D4-distinct chain near-miss 上算对偶椭圆曲线 $E_{b,d}: Y^2 = X(X+b^2)(X+d^2)$
的 rank：

- 默认 `ellrank` 报 4 个 dual rank=0 看似是 obstruction
- 用 `effort=2` 复核后 **0 个 certified rank=0**（全部升级到 rank=2）
- 这把已知的"chain pair rank 过滤率 0%"从 $E_{A,B}$ 主线推广到了对偶视角

### 2. chain candidate 在 dual EC 上必然是 trivial 2-descent class（worklog 035）

代数事实：把 Peschmann 2-descent map $\delta_i = \text{sf}(v^2(X - r_i))$ 用到
$E_{a,c}$ 上 $X = b^2$ 的有理点：

- $\delta_1 = \text{sf}(b^2) = 1$
- $\delta_2 = \text{sf}(b^2 + a^2) = \text{sf}(h_1^2) = 1$（因为 $a^2 + b^2$ 是平方）
- $\delta_3 = \text{sf}(b^2 + c^2) = \text{sf}(h_2^2) = 1$（因为 $b^2 + c^2$ 是平方）

所以 chain candidate 在 dual EC 上**自动**给出 trivial 2-descent class
$(1, 1, 1)$。这反向解释了为什么 worklog 033 必然是负面结果——Selmer 视角的
free obstruction 永远不可能命中 chain candidate。

### 3. 4-chain 的代数恒等式 A 和 C（worklog 034）

对任意 4-chain $(a, b, c, d)$（不要求正方形条件），4 个 hypotenuse
$h_1, h_2, h_3, h_4$ 满足：

- **恒等式 A**: $h_1^2 + h_3^2 = h_2^2 + h_4^2 = a^2+b^2+c^2+d^2$
- **恒等式 C**: $(h_1 h_3 - h_2 h_4)(h_1 h_3 + h_2 h_4) = (d-b)(a-c)(a+c)(b+d)$

1005 个长方形 4-chain (`max_val=5000`) 上 100% 数值验证通过。这是项目对 chain
结构发现的真实代数贡献，可以直接进 paper。

但基于这两个恒等式的 §2.4 "blocker prime" 论证**基础假设错误**（Fermat-Euler
对 hypotenuse 没有 mod 4 parity 约束），不提供 obstruction。

### 4. cypari2 性能 / 默认值教训（worklog 033/035）

实测确认两件需要注意的事：

- `pari.ellrank(E)` 默认 effort 太浅，会系统性给出虚假 `lower=0`。
  汇报 rank=0 之前必须 `effort=2` 复核。
- `pari.ellanalyticrank(E)` 在 conductor 中等大小时单条耗时 906s~6929s。
  任何脚本默认必须关闭，由 flag 显式开启。

### 5. 工具盘点：PARI 已含 2-descent 全部所需 API（worklog 035）

原 IDEAS §4 想法 3 估计装 Sage 要 1–2 天。实测发现 cypari2 已暴露：

- `pari.ellrank(E, effort)` 返回 **4 元组** `[rank_lo, rank_hi, sha2_lo, gens]`
- `pari.ell2cover(E)` 给出 Selmer 群的 quartic covers（= Sage `E.two_descent()` 核心）
- `pari.elltors(E)` 完整 torsion 结构

→ 该 bug 已在 worklog 036 修复，详见下面第 6 节。

### 6. compute_rank 4-tuple 修复 + 320 hard_case Selmer 实证（worklog 036）

`compute_rank` 现在返回 4 元组 `(rank, (lower, upper), sha2_lower, gens)`，
默认 `effort=1`（实测决定，比 effort=0 多 33% 时间换 7/7 certified vs 1/7）。
194/194 测试通过零 regression。

在 max_hyp=500 的 320 hard_case 上跑 `pari.ell2cover` + `pari.ellrank(E, 1)`
（共 3.6 秒）拿到 Selmer 数据，两个核心结果：

#### Selmer 维度公式实证

```
n_quartic_covers = rank_lower + 2 + sha2_lower
```

320/320 hard_case 全部满足。常数 "+2" 来自 $E_{A,B}$ 三根全有理给出的
$\dim_{\mathbb{F}_2} E[2](\mathbb{Q}) - 1$。

#### 项目首次追踪到非平凡 Sha[2]（2 个 hard_case）

| (A, B) | rank | sha2_lower | n_quartic_covers |
|---|---|---|---|
| (243, 1085) | 1 | 2 | 5 |
| (3969, 15895) | 1 | 2 | 5 |

两个 case 都 rank=1，但 Selmer 群比一般 rank=1 case 大（5 个 cover vs 3 个），
非平凡 Sha[2] 维度 = 2。这是项目第一次显式追踪到 Sha[2] 信息——是 worklog 036
4-tuple bug 修复的直接收益。后续可用 Cassels-Tate pairing（PARI 的
`elltatepairing`）做更细致的分析。

### 7. Finite-descent effective bound：N ≤ 10^8 上零 chain solution（worklog 037）

实现 Peschmann §7(2) 风格的两层 modular search：

- Layer 1 (per-prime universal blocker probe): **0 个 hard_case** 被任何
  prime $p < 200$ 简单阻挡。log_density 中位数 $\approx -58$，heuristic 上
  允许 N 残余比例 $\approx 10^{-25}$。
- Layer 2 (CRT mod 30030 + N 枚举到 $10^8$，58 秒): **0 chain-compatible N**
  在 320/320 hard_case 上。

**实证 lemma**: 对 max_hyp=500 的全部 320 hard_case $(A, B)$，不存在整数
$N \in [1, 10^8]$ 使两个平方条件 + 4-chain closure 同时成立。

把 d19 现有 ec_bound = $10^5$ 推到 $10^8$（×1000），$4.82 \times 10^8$ N
通过 mod-30030 sieve 后被精确平方判定 + chain closure 全部排除。完全可复现。

观察：concordant N 大量存在但几乎全部"几何 degenerate"（$A+B-N \leq 0$ 或
剩余两个平方条件不满足）—— chain 问题 vs cuboid 的 closure constraint 差异
在数据上明显。

---

## 六、补充阅读（更工程向的细节）

如果想看 `chain-fast` 侧的工程记录与实验结果，可以直接看：

- [docs/CHAIN_FAST_SAFE_FILTERS.md](./CHAIN_FAST_SAFE_FILTERS.md)
- [docs/archive/CHAIN_FAST_BUCKET_STATS.md](./archive/CHAIN_FAST_BUCKET_STATS.md)（已归档）
- [docs/archive/CHAIN_FAST_STRUCTURE_FINDINGS.md](./archive/CHAIN_FAST_STRUCTURE_FINDINGS.md)（已归档）
- [docs/archive/CHAIN_FAST_OPTIMIZATION.md](./archive/CHAIN_FAST_OPTIMIZATION.md)（已归档）

针对 2026-05 实证细节：

- [docs/work-logs/033-dual-ec-probe.md](./work-logs/033-dual-ec-probe.md) — dual EC 视角
- [docs/work-logs/034-hypotenuse-identity.md](./work-logs/034-hypotenuse-identity.md) — hypotenuse 恒等式
- [docs/work-logs/035-pari-selmer-api.md](./work-logs/035-pari-selmer-api.md) — PARI Selmer API + Peschmann §6/§7
- [docs/work-logs/036-compute-rank-fix-and-ell2cover-batch.md](./work-logs/036-compute-rank-fix-and-ell2cover-batch.md) — compute_rank 4-tuple 修复 + 320 hard_case Selmer 数据 + 2 个 sha2=2 case
- [docs/work-logs/037-finite-descent-on-hard-cases.md](./work-logs/037-finite-descent-on-hard-cases.md) — Peschmann §7(2) 风格两层 modular search，320 hard_case × N ≤ 10^8 零 chain-compatible N（effective lemma）
