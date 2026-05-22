# 032 — 文献调研：Harborth 4-chain / Euler 协调形式问题

**日期**: 2026-05
**触发原因**: 用户要求做文献调研，澄清 d19 项目的学术对接位置和真实贡献空间。
**输出**: 建立 `docs/literature/` 文献库（详见 [`../literature/README.md`](../literature/README.md)）。

---

## 调研覆盖范围

通过 7+ 轮 web search + arXiv abstract/HTML 拉取 + GitHub 仓库检查，覆盖了：

- 1980s 奠基期（Bremner-Cassels 1984、Bremner-Guy 1988/1989、Guy 1989）
- 1990s 协调形式现代化（Ono 1996 ×2）
- 2000s descent 与 K3（Bremner-Silverman-Tzanakis 2000、van Luijk 2000、Sharipov 2011/2013）
- 2010s 框架完善（Bremner-Ulas 2016、MacLeod 2016、KSS 三部曲 2019-2020）
- 2024-2026 当代（Greenfeld 2024、Chang 2024、Hosseini 2025、Asiryan 2025、Peschmann 2026 三部曲）

完整时间轴见 `docs/literature/timeline.md`。

## 三大关键发现

### 1. ⭐⭐⭐ Peschmann 2026 (arXiv 2604.09328) 是 d19 的"完美双胞胎"

这篇 2026-04 发表的 perfect Euler brick 论文，结构和 d19 项目几乎完全平行：

- 同样不声称证明无解，只声明 "reduction framework + unconditional obstructions"
- 同样用 PARI/GP + SageMath
- 同样跑到 parameter ≤ 1000
- 同样诚实承认 "remaining gap"
- 同样把 Faltings + Chabauty + Brauer-Manin 列为 future work
- 同样开源 GitHub repo（renpe/euler-brick-obstructions）+ 数据库 dump

**意义**：彻底证明 d19 的 framing 是学术合法的。这种工作 2026 年还能投 arxiv 配套三部曲。

详细对照见 `docs/literature/notes/peschmann-2604-09328.md`。

### 2. ⭐⭐⭐ Bremner-Guy 1989 极可能是 4-chain 真正奠基

> Bremner, A. & Guy, R. K. (1989). The delta-lambda configurations in tiling the square. *J. Number Theory* 32(3), 263-280.

间接证据强烈指向 d19 项目的"原始论文"应该是这篇 1989 的，而不是 Harborth 自己关于 unit circle rational distance 的论文（后者 Eppstein 2023 已指出有误）。

**待办**：拿到全文确认。所有公开访问途径（ScienceDirect、CORE、Elsevier）至今均受限。

详见 `docs/literature/notes/bremner-guy-1989.md`。

### 3. ⭐⭐⭐ Ono 1996 "Euler's concordant forms" 是 EC family 的现代奠基

d19 的 $E_{A,B}: Y^2 = X(X+A^2)(X+B^2)$ 是 Ono 1996 框架的 $E_{M,N}: y^2 = x(x+M)(x+N)$ 在 $M = A^2, N = B^2$ 时的特殊子族。

意味着 d19 在做的是 Ono 协调形式问题在"$M, N$ 都是平方"约束下的有限性分析。这给 d19 一个明确的母领域 / 历史源头。

详见 `docs/literature/notes/ono-1996-concordant.md`。

## 重新评估 d19 的学术贡献空间

**之前两次定位都需要修正**：

| 阶段 | 评估 |
|---|---|
| Round 1 | "不算原创"（过度悲观） |
| Round 2 | "KSS 反向应用"（被单点牵引） |
| **Round 3（当前）** | **"Peschmann 风格的实验性反向研究"** |

**可发表性评估**：

| 形态 | venue | 实际可行性 |
|---|---|---|
| arXiv preprint + GitHub | math.NT | ✅ 高 |
| *Experimental Mathematics* | EXM | 🟡 中-高（需补 1-2 个不平凡定理） |
| *J. Number Theory* short paper | JNT | 🟡 中 |
| ANTS conference proceedings | ANTS | 🟡 中 |

**与 Peschmann 工作的对比劣势**：
- 缺少 2-descent + Kummer character 这类结构性定理
- 计算规模（24k pairs at max_hyp=1000）显著小于他们（~$10^{11}$ tuples）
- 还没有正式的 reduction lemma

**优势**：
- proof_status pipeline 完整、增量、可重现
- safe_sieve + rank=0 + Heegner 组合是 novel
- 0 反例发现 + 116 个 rank=1 hard_case 数据已是 publishable

## 文献库结构

```
docs/literature/
├── README.md              总索引
├── timeline.md            按年份排序的文献时间轴
├── references.bib         BibTeX 格式所有 reference（写论文用）
├── notes/
│   ├── peschmann-2604-09328.md   ⭐⭐⭐
│   ├── knaf-selder-spindler.md   ⭐⭐⭐
│   ├── ono-1996-concordant.md    ⭐⭐⭐
│   ├── bremner-guy-1989.md       ⭐⭐⭐（待获取全文）
│   ├── bremner-ulas-2016.md      ⭐⭐
│   ├── chang-2024-4regular.md    ⭐⭐
│   └── greenfeld-2024.md         ⭐
└── pdfs/
    ├── README.md          PDF 获取与命名规范
    └── .gitignore         默认忽略所有 PDF
```

## 后续推荐 action items（按优先级）

### Tier 1（必做，1-2 周）

1. **拿到 Bremner-Guy 1989 全文**，更新 `notes/bremner-guy-1989.md`
2. **clone renpe/euler-brick-obstructions** 学习代码组织和 reproduction 结构
3. **下载并精读 KSS 1907.02148** 的 § 2-3 reduction setup

### Tier 2（中期，2-4 周）

4. **起草 Lemma**: "任何 Harborth 4-chain 给出 $E_{A,B}(\mathbb{Q})$ 非平凡有理点"
   - 类比 Peschmann Lemma 3.1
   - 写到 `docs/lemma_chain_to_ec.md`

5. **试 Sage 2-descent** on hard_case 的 (A,B)
   - 对应 Peschmann § 6 方法
   - 看能否排除整个 descent class

6. **重新统计 safe_sieve 数据看是否有 "blocker prime" 现象**（对应 Peschmann § 7 (3)）

### Tier 3（长期，1-3 月）

7. **重组 d19 为 paper 形态**（参照 renpe layout）
8. **联系 Bremner / Cremona / Ulas 学界**（电邮 1-2 段 + GitHub link）

## 与现有文档的关系

- `docs/THEORY_DIRECTIONS_ADVANCED.md`：方向 7-10 的描述基本对，但应该新增"对标 Peschmann 2026 方法"段
- `docs/CURRENT_FINDINGS.md`：实证内容不变，但 framing 段可以引用 Peschmann 来证明这种工作的学术合法性
- `docs/PROJECT_STATUS.md`：long-term plan 段应该指向 literature/ 文件夹
