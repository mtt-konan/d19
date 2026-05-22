# Bremner & Guy 1989 — "The delta-lambda configurations in tiling the square"

**全名**：Bremner, A. & Guy, R. K. (1989). The delta-lambda configurations in tiling the square. *Journal of Number Theory* 32(3), 263–280.
**DOI**: 10.1016/0022-314X(89)90083-8
**MR**: MR1006593
**优先级**：⭐⭐⭐ 极可能是 Harborth 4-chain 真正奠基论文

---

## 状态：**待获取全文**

至今所有访问途径均受限：
- ScienceDirect：需机构订阅
- CORE Reader：HTTP timeout（多次重试失败）
- ASU Pure 页面：只有 metadata
- Elsevier 直链：404

**建议获取途径（按优先级）**：
1. 通过个人/学校的 ScienceDirect 订阅下载
2. 找 PostDoc / 在校研究生借资源（IDM / EBSCO）
3. 直接电邮 Andrew Bremner（ASU）询问
4. 跨馆借阅（OCLC ILL）

获取后将本笔记升级为完整阅读笔记。

---

## 为何认为是 Harborth 4-chain 奠基

间接证据 1：**作者** — Andrew Bremner 是协调形式 + rational distance + Diophantine 几何领域的核心人物（30+ 篇相关论文）；Richard Guy 编《Unsolved Problems in Number Theory》多次提到 Harborth 类问题。

间接证据 2：**标题** — "delta-lambda configurations in tiling the square" 直译为"在正方形铺砌中的 δ-λ 配置"。

- "tiling the square" = 正方形铺砌
- "delta-lambda" 极可能指**两类参数**（两种角度的直角三角形参数化），对应 Harborth 4-chain 里的两个 Pythagorean 单元
- "configurations" = 离散的几何配置

这跟 d19 项目 "正方形分成 4 个 Pythagorean 三角形 + chain 整数性" 的描述高度一致。

间接证据 3：**期刊** — *J. Number Theory* vol. 32（1989）；同卷有相关 Diophantine 论文。

间接证据 4：**Guy 1989 兄弟论文** — Guy 自己单独写过 "Tiling the square with rational triangles"（在 *Number Theory and Applications* NATO 会议集，Banff 1988），完全是同主题。

间接证据 5：**Campbell-Brady "Tiling the Unit Square with 5 Rational Triangles"** 文献提到 "14 distinct ways to tile the unit square with 5 triangles"——Harborth 4-chain 几乎肯定属于这 14 种之一。

---

## 拿到全文后必须确认的问题

1. 论文是否给出 d19 的 4-chain 条件 $\{A^2+B^2=h^2, A^2+N^2=h_3^2, N^2+B^2=h_4^2, ...\}$ 的早期表述？
2. 是否给出对应的椭圆曲线 / 代数簇？跟 $E_{A,B}: Y^2=X(X+A^2)(X+B^2)$ 是否同构？
3. 是否证明了任何非存在性 partial result？
4. 引用列表里有哪些上游文献？（追溯 1989 年之前是否有更早奠基）

---

## 引用建议

在 references.bib 已添加：

```bibtex
@article{bremner-guy-1989-deltalambda,
  author  = {Bremner, A. and Guy, R. K.},
  title   = {The delta-lambda configurations in tiling the square},
  journal = {Journal of Number Theory},
  volume  = {32},
  number  = {3},
  pages   = {263--280},
  year    = {1989},
  doi     = {10.1016/0022-314X(89)90083-8}
}
```

引用 key: `bremner-guy-1989-deltalambda`

---

## Action items

| 优先 | 任务 |
|---|---|
| ⭐⭐⭐ | 拿到全文 PDF，放到 `../pdfs/bremner-guy-1989-delta-lambda.pdf` |
| ⭐⭐⭐ | 精读 § 1-2，确认是否就是 4-chain 的原始表述 |
| ⭐⭐⭐ | 拿到全文后重写本笔记 |
