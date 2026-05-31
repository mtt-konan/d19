# wl090 — F.2：Stoll–Bruin / 开源 Chabauty 工具调研（能否替代 Magma）

## 问题

OPEN_DIRECTIONS **F.2**：B.1（closure-fiber Chabauty）被标 🛑 "要 Magma"。本调研问：
**Stoll / Bruin 一系的 Chabauty 工具（及其开源 / Sage 移植）能否在 d19 的用例下
替代 Magma**，从而复活 B.1（对 rank≥2 的主流 hard_case，~63%，给有限性判定）？

纯文献调研，无计算。

## d19 的目标曲线

对固定的 (A,B) hard_case，chain-closure 联立（`h3²=A²+N²`, `h4²=N²+B²`,
`a+c=b+d` 等，见 THEORY_DIRECTIONS_ADVANCED 方向七）定义一条亏格 g≥2 的曲线
`C_{A,B}`。Chabauty 定理：当 `rank Jac(C) < g` 时 `C(ℚ)` 有限且可 p-adic 枚举尽；
Quadratic Chabauty（Balakrishnan–Dogra–Müller–Tuitman–Vonk）把可处理范围扩到
`rank = g`。要把它变成 d19 的判定器，需要三步：(1) 把 closure 系统写成 Chabauty
可吃的模型（奇数次超椭圆 / 光滑平面四次）；(2) 算 `Jac` 的 Mordell–Weil rank；
(3) 跑 Chabauty + Mordell–Weil sieve 把有理点列尽，核验没有 X=N² 的解。

## 工具盘点（2020–2025）

| 工具 | 平台 | 能力 | 对 d19 的可用性 |
|------|------|------|----------------|
| Magma `Chabauty` + `MordellWeilSieve` (Stoll) | **Magma** | genus-2、`rank Jac ≤ 1`、需一个已知有理点；MW-sieve 多素数拼接，**结论性**（精确列尽 C(ℚ)） | 金标准，但商业许可（有学术免费版 / 在线 calculator） |
| Coleman 积分 (Balakrishnan–Bradshaw–Kedlaya) | **Sage** | 奇数次超椭圆上的 p-adic Coleman 积分 | 开源，是经典 CC 的核心算子 |
| de Frutos-Fernández–Hashimoto (arXiv 1909.04808) | **Sage** | rank-0 genus-3 奇数次超椭圆的经典 Chabauty–Coleman，跑过 5870 曲线库 | **开源且成体系**，但限 rank 0 / 奇数次 |
| `twocover-descent` (HastD, MIT) | **Sage** | genus-2 带有理 Weierstrass 点的 **two-cover descent**（即 Bruin–Stoll 思路的开源实现） | 开源；正是 "Bruin–Stoll" 这一支，可压 Sel 信息 / 找有理点 |
| `QCMod` (steffenmueller) | **Magma** | Quadratic Chabauty，`rank=genus`、real multiplication；含基于 Stoll 代码的 MW-sieve | Magma；rank=g 的主力 |
| `MWSieveForDatabase` (Bianchi–Padurariu) | Sage **+** Magma | rank-2 genus-2 bielliptic：Sage 做 QC，**MW-sieve 仍调 Magma**（QCMod 的代码） | 印证：QC 部分可开源，sieve 部分仍 Magma |

## 结论（verdict）

**Stoll–Bruin 一系工具在 d19 用例下"部分可替代、整体尚不可替代"Magma**：

1. **可开源的部分**：经典 Chabauty–Coleman 的核心算子（Coleman 积分）在 Sage 里
   成熟（BBK），且对 **奇数次超椭圆 + rank 0/1** 有成体系的 Sage 实现
   (1909.04808)。Bruin–Stoll 的 two-cover descent 也有 Sage 开源版
   (`twocover-descent`)。

2. **仍卡 Magma 的部分**：让 Chabauty **结论性**（排除多余 p-adic 点、处理
   `rank=g` 的剩余 residue class、跨素数拼接）的 **Mordell–Weil sieve** 至今主要是
   Stoll 的 Magma 代码（QCMod / Bianchi–Padurariu 都直接调它）。此外 `Jac` 的 MW
   rank / 2-Selmer 计算在 genus≥2 上通常也要 Magma 的 `RankBound` / `TwoSelmerGroup`。

3. **对 d19 的实际影响**：
   - B.1 维持 🛑，但可**降级措辞**：不是"全程要 Magma"，而是"MW-sieve 与高亏格
     rank 计算这两步要 Magma"。经典 CC 的积分部分可在 Sage 做。
   - rank=g 的主流 hard_case（~48% rank-2）走 **Quadratic Chabauty**，开源缺口
     最大（QCMod 是 Magma）。
   - **最低成本的开源 PoC**：挑 **一个** rank<g 的 hard_case fiber，手工写成奇数次
     超椭圆模型，用 Sage（CoCalc）跑经典 Chabauty–Coleman，看能否列尽有理点。这能
     验证"d19 的 closure 曲线适配 Chabauty"这一前提，**不需要 Magma**——但要先确认
     `C_{A,B}` 能写成奇数次超椭圆且 rank < g。

## 建议的后续动作（均非长跑）

- **F.2-a**（低成本，开源）：取一个 rank-1 hard_case（Heegner 已覆盖 ~37%，挑一个
  rank=2 之外的），把 `C_{A,B}` 显式写成超椭圆模型并报告其 genus 与 `Jac` 的近似
  rank（PARI/Sage）。只有 `rank < genus` 才进得了经典 Chabauty。
- **F.2-b**（决策点）：若 genus 与 rank 适配，用 CoCalc 上的 Sage（含 1909.04808
  风格代码）做单条曲线 PoC；若不适配或要 rank=g，则确认必须走 Magma（在线
  calculator / 学术许可）或等开源 QC 成熟。
- 把 B.1 的 🛑 注记更新为"MW-sieve + 高亏格 rank 两步需 Magma；经典 CC 积分部分
  Sage 可做"。

## 参考

- Magma handbook §Chabauty's Method（genus-2 `Chabauty` + MW-sieve，Stoll）。
- de Frutos-Fernández, Hashimoto, *Computing rational points on rank 0 genus 3
  hyperelliptic curves*, arXiv:1909.04808（Sage 实现）。
- Balakrishnan, Bradshaw, Kedlaya（2010）Coleman 积分算法（Sage）。
- steffenmueller/QCMod（Magma，Quadratic Chabauty + MW-sieve）。
- HastD/twocover-descent（Sage，Bruin–Stoll two-cover descent，MIT）。
- Bianchi, Padurariu, *Rational points on rank 2 genus 2 bielliptic curves in the
  LMFDB*（Sage QC + Magma MW-sieve）。
