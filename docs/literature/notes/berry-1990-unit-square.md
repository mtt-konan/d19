# Berry 1990 — "Points at rational distance from the corners of a unit square"

**全名**: Berry, T.G. (1990). Points at rational distance from the corners of a unit square. *Annali della Scuola Normale Superiore di Pisa, Classe di Scienze* (4) 17, no. 4, 505–529.
**免费全文**: <http://www.numdam.org/item?id=ASNSP_1990_4_17_4_505_0>（Numdam，无墙）
**优先级**：⭐⭐⭐ 唯一直接对 d19 四距离问题做 surface-level 代数几何分析的论文
**状态**：全文精读完成（2026-07-14）
**本地 PDF**：`../pdfs/berry-1990-rational-distance-unit-square.pdf`
**抽取文本**：`../pdfs/berry-1990-rational-distance-unit-square.txt`
**注意**：抽取文本丢失了大部分 displayed 公式和附录 Table 1–5；精确方程需回看 PDF 原图或重推。

---

## 一句话总结

把三距离条件 (1) 看成 P³ 中的 **Kummer 曲面 S**（16 个 node），完整算出
Néron–Severi 群并分类低次可参数化曲线；四距离问题对应 S 的二重覆盖
**R ⊂ P⁴，一般型正则曲面（p_g=5，K_R ample，典范嵌入 P⁵）**，并证明
Hunter–Leech 等低次三距离族中**不含**四距离解。未解决四距离问题。

## 主要结果

### 三距离曲面 S（Kummer）

- 方程 (1)（三距离的齐次必要充分条件）定义 P³(X,Y,Z,T) 中恰有 16 个
  node 的四次曲面 ⇒ Kummer 曲面，带 16₆ 配置（Table 1–3）。
- `ρ(S̄)=19, d(S̄)=64`；经由 Abelian 二重覆盖 A ≅ 同源 E×E（E 无 CM，
  j=2⁷…，文中给出）算出。`NS(S̄,Q)`（Q 上有理部分）秩 13，显式基与
  相交矩阵（Fig. 6）。
- 椭圆纤维化：过 node 1、2 的平面束切出的 binodal 四次曲线束；
  截面群 torsion = Z/2×Z/2（C1,C6,C9,C13），自由部分秩 2，由 P 与 C2
  生成（Cox 判据）。
- **Theorem 3.1**：2 次与 4 次可参数化曲线分类完备（2 次 = tropes，
  4 次 = 三 node 平面四次曲线；4 次族即 Hunter–Leech–Conway–Guy 族）。
- **Theorem 3.2**：从 node 2、node 1 相继投影 = 截面群中平移 C2
  （无限阶）⇒ 无穷多条一参数三距离解族。
- 6 次时算法找到投影生成之外的 **24 条新 sextic**（均过 4 个有理 node，
  故可参数化）；8 次更多。⇒ 三距离解"异常丰富"，且超出 Hunter–Leech
  迭代生成范围。
- S 上所有曲线次数为偶（Cor. 2.8）。

### 四距离曲面 R

- (1)+(2) 定义 P⁴(X,Y,Z,T,U) 中的曲面 R，经 U=0 投影为 S 的二重覆盖 π，
  分歧于 B = S ∩ {二次曲面}。
- **Prop 4.1**：B = B₁+B₂，两条 Q(i) 上共轭椭圆四次曲线，交于 8 点
  (±1, ±√2, ±1, ±1)。
- **Cor 4.2**：R 是正则一般型曲面，几何亏格 5，仅 ordinary node 奇点，
  K_R ample，典范嵌入 P⁵。⇒ "一般型曲面没有 Diophantine 理论"——
  Berry 认为这解释了四距离问题之难。
- **Prop 4.3**：对 Thm 3.2 程序生成的任何有理曲线 C，π*C 在 R 上不是
  有理曲线（分歧点计数 + C·B=2degC + B 只有 8 个 node ⇒ degC≤8，再逐一
  显式验证 2/6/8 次曲线不过 B 的 node、4 次至多过 2 个）。
- **Prop 4.4**：2 次（trope C7）与 4 次（Hunter–Leech）三距离族中
  **无四距离解**。4 次情形代入参数化后是一条初等 **2-adic** 论证
  （t=2^a·p/q 清分母后两侧 2 幂不可能匹配）。
- 6 次族代入 (2) 得 **亏格 5 曲线**，RHS mod 3 无平方因子；小规模搜索
  只见平凡点 t=0,U=±1，**未证明**。8 次类似。
- Berry 结论：S 上有理曲线横截地、避开 node 地交 B ⇒ 拉回是高亏格曲线
  ⇒ 支持"无解"猜想，但"本文的代数几何技术不太可能给出证明"。

## 与 d19 的关系

- **这是 wl596 之后 route table 里 higher-genus 行所要的 family-level
  外部几何数据的最直接来源**：仓库现有工作（wl594 的 genus-3/5 covers、
  λ-族逐纤维分析）是 fiber-wise 的；Berry 给出的是**总曲面** R 的整体
  几何（NS 格、分歧曲线、一般型性质）。这个 object layer 仓库里没有。
- 但 Berry **不**提供统一 obstruction（一般型曲面无可用理论，1990 与今天
  同样成立，Bombieri–Lang 只是猜想）。route audit 的
  `no_current_route_without_new_external_input` 结论不因本文而推翻；
  本文提供的是**新的有限可执行任务**与新对象层，不是家族定理。
- 全平面性质：Berry 通过符号对称（变量变号 + X↔Z、Y↔T）处理所有象限，
  与 d19 的全平面 closure 约定兼容。
- **可执行缺口（1990 年工具止步处）**：24+ 条 6 次族与 8 次族的四距离
  排除。每条的 π 拉回是显式亏格 5 曲线，Berry 只做了"小搜索"。现代
  工具（two-cover descent / elliptic Chabauty / Mordell–Weil sieve）
  有现实机会逐条证死。若全部证死，得到定理：
  "所有已知三距离一参数族（次数 ≤8）不含四距离解"——这是 Berry
  Prop 4.4 的严格推广，属于新的 partial result。
- 需要 scoped 对比：Berry 的 2-adic 论证（Prop 4.4 degree-4 情形）与
  wl162（Yang Ji centerline）、wl203–293（reciprocal/q-adic 路线）是否
  同构或互相蕴含；Berry 的 genus-5 sextic 拉回与 wl594 的 genus-5
  individual lift 是不同对象（前者在 Kummer 曲面上，后者在 λ-线上），
  勿混同。
- Bremner–Ulas 2016 对平面正方形情形只引用本文并声明 open（其正文是
  矩形与 Q³ 变体），所以本文就是平面四距离问题 surface 方法的终点文献。

## 上游文献

- [5] = Bremner–Guy 1989 delta-lambda（仓库已建 note，仍待全文）。
- [9] = Guy, "Tiling the square with rational triangles"（Acta Arith.，
  当时 to appear）——三距离问题历史综述。
- [16] Swinnerton-Dyer、[2–4] Bremner：K3/四次曲面 Diophantine 技术源头。

## Action items

| 优先 | 任务 |
|---|---|
| ⭐⭐⭐ | 从 PDF 原图恢复 Table 4/5（低次族的显式参数化）与 6 次拉回曲线方程 |
| ⭐⭐⭐ | scoped task：用现代 descent/Chabauty 逐条攻击 6 次族的亏格 5 拉回（Berry 未证明的部分） |
| ⭐⭐ | 对比 Berry Prop 4.4 的 2-adic 论证与 wl162/wl203–293 现有排除，确认是否已被仓库结果蕴含 |
| ⭐⭐ | 把 R（一般型，p_g=5）这一对象层写进 route table 的 higher-genus 行作为已获取的外部数据 |
| ⭐ | 追 Berry 1992 三角形论文（Acta Arith. 62(4)）与 Guy Acta Arith. 综述 |
