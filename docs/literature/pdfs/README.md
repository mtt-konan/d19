# PDF 存放约定

本目录用于存放文献全文 PDF。

## 命名规范

```
{第一作者姓氏小写}-{年份}-{短关键词}.pdf
```

示例：
- `bremner-guy-1989-delta-lambda.pdf`
- `peschmann-2026-quartic-reductions.pdf`
- `knaf-selder-spindler-2019-algorithm.pdf`
- `ono-1996-concordant-forms.pdf`

## Git 处理

本目录的 PDF **不入版本控制**（受 `.gitignore` 控制）。
原因：
1. PDF 文件体积大、二进制改不易 diff
2. 许多文献有版权限制，不应散播
3. 关键 metadata 已在 `../references.bib` 里

如果有需要团队共享但 GitHub 不便上传的 PDF：
- 用 Zenodo / Google Drive / OneDrive 等外部存储
- 在 `../notes/{paper}.md` 里写明本地路径 / 外部链接

## 当前应优先获取的 PDF

按优先级排序：

1. ⭐⭐⭐ **bremner-guy-1989-delta-lambda.pdf**
   - 全名：Bremner, A. & Guy, R. K. (1989). The delta-lambda configurations in tiling the square. J. Number Theory 32(3), 263-280.
   - 获取途径：
     - ScienceDirect (有机构订阅): https://www.sciencedirect.com/science/article/pii/0022314X89900838
     - CORE Reader (免费但慢): https://core.ac.uk/reader/82053950
     - ASU 作者主页: https://asu.elsevierpure.com/en/publications/the-delta-lambda-configurations-in-tiling-the-square

2. ⭐⭐⭐ **peschmann-2026-quartic-reductions.pdf**
   - 全名：Peschmann (2026). Quartic reductions and elliptic obstructions for perfect Euler bricks. arXiv:2604.09328
   - 获取途径：https://arxiv.org/pdf/2604.09328
   - HTML 版（已读完）：https://arxiv.org/html/2604.09328v1
   - 配套代码：https://github.com/renpe/euler-brick-obstructions
   - 数据：https://renepeschmann.de/research

3. ⭐⭐⭐ **ono-1996-concordant-forms.pdf**
   - 全名：Ono, K. (1996). Euler's concordant forms. Acta Arithmetica 78(2), 101-123.
   - 获取途径：
     - EUDML: https://eudml.org/doc/206936
     - ResearchGate: https://www.researchgate.net/publication/228792276
     - Academia: https://www.academia.edu/73654253

4. ⭐⭐ **knaf-selder-spindler-2019-algorithm.pdf**
   - 全名：Knaf, Selder, Spindler (2019). An Algorithm to Find Rational Points on Elliptic Curves Related to the Concordant Form Problem. arXiv:1907.02148
   - 获取途径：https://arxiv.org/pdf/1907.02148

5. ⭐⭐ **bremner-ulas-2016-rational-distances.pdf**
   - 全名：Bremner, Ulas (2016). Points at rational distances from the vertices of certain geometric objects. J. Number Theory 158, 104-133.
   - 获取途径：
     - arXiv: https://arxiv.org/pdf/1502.07312
     - ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0022314X15002243

6. ⭐⭐ **chang-2024-harborth-4regular.pdf**
   - 全名：Chang (2024). Harborth's Conjecture for 4-Regular Planar Graphs. LIPIcs GD 2024.
   - 获取途径：https://drops.dagstuhl.de/storage/00lipics/lipics-vol320-gd2024/LIPIcs.GD.2024.38/LIPIcs.GD.2024.38.pdf
