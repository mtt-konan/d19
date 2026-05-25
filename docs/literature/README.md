# 文献库 / Literature Archive

本目录收录 d19 项目（Harborth 4-chain / Euler 协调形式问题）相关的文献。

## 目录结构

```
literature/
├── README.md              # 本文件：总索引
├── timeline.md            # 按年份排序的文献时间轴
├── references.bib         # BibTeX 引用文件（写论文时直接用）
├── notes/                 # 阅读笔记，按"作者-年份"或 arXiv ID 命名
│   ├── peschmann-2604-09328.md   ⭐ 对标论文（最高优先级）
│   ├── knaf-selder-spindler.md   ⭐ 同曲线族算法
│   ├── ono-1996-concordant.md    ⭐ 协调形式奠基
│   ├── bremner-guy-1989.md       ⭐ 可能是 4-chain 真正奠基
│   ├── bremner-ulas-2016.md      （5 点 rational distance）
│   ├── chang-2024-4regular.md    （明确说 Harborth 4-regular open）
│   └── greenfeld-2024.md         （整数距离集密度）
└── pdfs/                  # PDF 全文（gitignore 不上传 GitHub）
    ├── README.md          # PDF 放置约定
    └── .gitignore
```

## 优先级与状态

| 论文 | 优先级 | 状态 | 笔记 |
|---|---|---|---|
| Peschmann 2026 (arXiv 2604.09328) | ⭐⭐⭐ | abstract+章节读完 | `notes/peschmann-2604-09328.md` |
| Bremner-Guy 1989 J. Number Theory 32 | ⭐⭐⭐ | **待获取全文** | `notes/bremner-guy-1989.md` |
| Ono 1996 Acta Arithmetica 78 | ⭐⭐⭐ | PDF/text 已获取，§1-3 关键结论已整理 | `notes/ono-1996-concordant.md` |
| KSS 2019/2020 系列 | ⭐⭐ | 核心算法论文 PDF/text 已获取，§2-4 已整理 | `notes/knaf-selder-spindler.md` |
| Bremner-Ulas 2016 J. Number Theory 158 | ⭐⭐ | abstract 读完 | `notes/bremner-ulas-2016.md` |
| Chang 2024 LIPIcs GD | ⭐⭐ | abstract 读完 | `notes/chang-2024-4regular.md` |
| Greenfeld-Iliopoulou-Peluse 2024 | ⭐ | abstract 读完 | `notes/greenfeld-2024.md` |
| Bremner-Silverman-Tzanakis 2000 | ⭐ | 待读 | （未创建笔记）|
| van Luijk 2000 (Utrecht thesis) | ⭐ | 待读 | （未创建笔记）|
| MacLeod 2016 arXiv:1610.03430 | 🔵 综述 | 待读 | （未创建笔记）|

## 阅读路线建议

**第一遍**（理解学术对标）：
1. `peschmann-2604-09328.md` — 看一个跟我们项目结构完全平行的最新工作如何 framing
2. `knaf-selder-spindler.md` — 看跟我们曲线族同构的算法工作如何 framing

**第二遍**（追溯奠基）：
3. `bremner-guy-1989.md`（拿到全文后）— 确认 4-chain 问题的真正起源
4. `ono-1996-concordant.md` — 协调形式问题的现代起点，PDF/text 已在 `pdfs/` 目录

**第三遍**（最新动态）：
5. `chang-2024-4regular.md` — Harborth 在图绘领域 2024 年的状态
6. `bremner-ulas-2016.md` — 5-vertex rational distance 框架

## 如何放置 PDF

见 [`pdfs/README.md`](./pdfs/README.md)。

简言之：
- 文件名格式：`{作者}-{年份}-{短标题}.pdf`，例如 `bremner-guy-1989-delta-lambda.pdf`
- PDF 不入 git（受 `.gitignore` 控制），但 `.txt` 抽取文本可以入 git 供 grep/review
- 抽取文本：`uv run python scripts/extract_pdf_text.py docs/literature/pdfs/*.pdf`
- 大于 100MB 的不要放，应放外部存储（Zenodo 等）

## 相关 worklog

- `docs/work-logs/032-literature-review.md` — 本次文献调研的工作日志
