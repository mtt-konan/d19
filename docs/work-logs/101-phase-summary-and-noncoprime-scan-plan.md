# wl101 — 阶段性小结（wl097–wl100）+ 非互素大规模扫描规划

## A. 阶段性小结：从互素定理到非互素 sound 管线

这一段（wl097–wl100）解决的核心问题：**之前只筛过互素 $(A,B)$，而 coprime-$(A,B)$ 并非 WLOG**
（最小反例只保证 $\gcd(A,B,N_1,N_2)=1$，推不出 $\gcd(A,B)=1$）。于是把整套必要条件推广到非互素半空间。

| wl | 成果 | 性质 |
|---|---|---|
| **097** | **互素 mod-12 定理**：$\gcd(A,B)=1 \Rightarrow 12\mid N$（初等 mod 3 + mod 8） | 已证定理（必要条件） |
| | 框架纠正：coprime-$(A,B)$ 是搜索归一化、**非 WLOG**；safe_sieve 只对互素 sound | 文档修正 |
| **098** | **gcd-aware mod-12**：$3\mid N$ 除非 $3\mid g$；$4\mid N$ 除非 $4\mid g$（$g=\gcd(A,B)$） | 已证定理（推广 097） |
| **099** | **2-adic 精化**：$v_2(g)=1 \Rightarrow 8\mid N$；**保证除数** $D_g=P_2(g)P_3(g)$ | 已证定理 |
| | **sound 筛 `gcd_aware_kills`**：闭合需 $D_g\mid(A+B)$ 或 $D_g\mid|A-B|$，对**任意** $(A,B)$ 可靠 | sound 工具 |
| **100** | 残余 $84\to64$ 个**任何模数都杀不掉**（local-global gap）；GEN-CLOSURE 廉价完备判定（$0.05$ ms/对、$0$ 闭合） | 结构刻画 |

**净状态（诚实版）**：
- **已证（真定理）**：互素 mod-12、gcd-aware mod-12、$D_g$ 整除性（含 $8\mid N$ 精化）。它们是**部分必要条件**，**不是** Harborth 的证明。
- **sound 机器**：三段管线 `gcd_aware_kills → chain_closure 模 p² → GEN-CLOSURE`，对互素∪非互素全空间可靠。
- **经验**：全部非互素多-N 对（hyp≤2000，1,802 对）+ 海量互素范围（到 hyp 5M、>116 万个 N）→ **0 闭合**。
- **仍开放**：Harborth 本身（没有"闭合永不发生"的证明）；残余是 local-global，故只能靠**完备**判定器（GEN-CLOSURE）——而它廉价。

**一句话**：互素腿已有闭式模障碍（必要条件），非互素腿也补上了 sound 的 $D_g$ 障碍 + 廉价完备判定；
缺的仍是把"必要条件"升级为"不可能性"的证明（=Harborth 难题硬核）。可确定产出的是**覆盖全空间的经验声明**。

## B. 非互素大规模扫描规划

**目标**：第一次给出**同时覆盖互素 ∪ 非互素 $(A,B)$** 的"无反例到界 $B$"经验声明
（此前 7M 扫描的解析筛线只覆盖互素；非互素只有 hyp≤2000 这一窗）。

### B.1 唯一要改的地方：生成器去掉两行过滤

`src/rational_distance/concordant/fast_multi_n.py` 的 `fast_multi_concordant_pairs`（及 numpy 版
`scripts/multi_n/fast_multi_concordant_scan_numpy.py` 同构逻辑）现在硬删非互素：

```python
# fast_multi_n.py:214-218  —— 大规模非互素扫描时去掉这两段过滤
if not ai_is_odd and not (aj & 1):   # (1) 跳过 even-even
    continue
if gcd(ai, aj) != 1:                 # (2) 跳过非互素
    continue
```

改法：**删掉 (1)(2)，对每个 pair 打 `g=gcd(A,B)` 标签**（保留全部对）。判定器无需改——
`exact_concordant_pair` 对非互素已精确（wl098 验过 0 mismatch）。

### B.2 sound 三段管线（wl100 已验证为正确架构）

```
所有 multi-N 对 (含非互素)
   │
   ├─① gcd_aware_kills(A,B)        O(1)      —— D_g 整除性，kills ~63% (1138/1802)
   │
   ├─② chain_closure 模 p² (STANDARD/EXTENDED, full_plane)   O(素数)  —— 并联到 ~95% (1718/1802)
   │
   └─③ GEN-CLOSURE：exact_concordant_pair 完整集 + 四关系     完备 sound  —— 残余 ~84, 0.05 ms/对, 0 闭合
```

每对最终落 ①/②/③ 哪一档 + 是否闭合 + `g` 都记录；闭合数若 $>0$ 即**反例命中**（要立即报警）。

### B.3 分阶段界 + 预期

| 阶段 | max_hyp | 目的 | 估计 |
|---|---|---|---|
| 0 | 2,000 | sanity（已做：1,802 非互素多-N，0 闭合） | 秒级 |
| 1 | 10,000 | 验证去过滤后管线端到端正确、计数自洽 | 分钟级 |
| 2 | 100,000 | 第一个有分量的非互素覆盖声明 | 十分钟级 |
| 3 | 1,000,000 | 对齐已有互素 1M 扫描的范围 | 小时级（numpy 版） |
| 4 | 5,000,000 | 对齐 5M，给出完整空间最大经验界 | 需 numpy + 多进程 |

瓶颈是**枚举**（`iter_concordant_a_n` 对每个 $A\le$max_hyp 分解 $A^2$）与 **② chain_closure**（对每个 multi-N 对）；
③ GEN-CLOSURE 因残余集极小而廉价（B 阶段实测 0.05 ms/对）。numpy 版已为 3–4 阶段准备好向量化。

### B.4 产出物（确定能交付）

1. **覆盖互素∪非互素的"无反例到 max_hyp"声明** + 按 `g` 分层的存活/闭合计数（结果 JSON 存档）。
2. **非互素存活的 gcd 分布**（local-global 残余落在哪些 $g$，对照 wl100 的 $12\mid g$ 主导）。
3. 若任一阶段出现闭合 → 即 Harborth 反例候选，立即复核。

### B.5 立即可执行的第一步

阶段 1（max_hyp=10k）：复制 `fast_multi_concordant_pairs`、去掉 B.1 两行、按 B.2 三段管线跑、
输出计数表。确认无误后逐级推到 100k / 1M。这一步把 wl097–wl100 的全部理论变现成一个硬数据声明。
