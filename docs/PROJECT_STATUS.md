# Project Status

这份文档是当前入口。旧的逐轮记录已经压缩到
[worklog index](./work-logs/README.md)。

## Current Mainline

项目现在的主线是：

```text
closure quotient
  -> lambda = A/B 射线账本
  -> AA/BB rank-zero certificates
  -> rank-zero Selmer family proof attempt
```

入口：

- [CLOSURE_QUOTIENT_MAINLINE.md](./CLOSURE_QUOTIENT_MAINLINE.md)
- [294-closure-quotient-foundation-consolidated.md](./work-logs/294-closure-quotient-foundation-consolidated.md)
- [363-lambda-mainline-consolidated.md](./work-logs/363-lambda-mainline-consolidated.md)
- [386-rank-zero-selmer-package-consolidated.md](./work-logs/386-rank-zero-selmer-package-consolidated.md)

普通话说：现在不是继续数更多 `(A,B)`，而是想证明一整批
`lambda=A/B` ratio family 的 `AA/BB` quotient rank 为 0。

## What Is Proved

Strictly proved or safely usable:

- GEN-CLOSURE 是正确的全平面闭合语言：
  `{N1+N2, |N1-N2|}` 必须和 `{A+B, |A-B|}` 相交。
- 旧 concordant 曲线会漏掉闭合腿 `M=A+B-N` 的信息。
- `AA/BB rank=0 + torsion pullback` 是严格有限证书。
- 已认证的 `AA/BB rank=0` 行只回拉到中点，没有完整闭合点。
- 中点分支由 Yang Ji 定理关闭。
- `AB/BA` 不是 rank-zero 击杀器。

## What Is Not Proved

还没有证明：

- Harborth 全局命题。
- 所有 `lambda` family 的 rank-zero 定理。
- residual two-cover / Sha[2] candidate 没有有理点。
- `required_count` 或 certificate count 增长本身不是数学进展。

## Current Bottleneck

当前瓶颈是 Selmer/rank-zero family proof：

```text
odd-prime local image
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank-zero conclusion
```

最近的 worklog 主要是在补这些 proof package 的可审阅段落。它们是证明链材料，
但每多一个 package 段落并不等于命题更接近完成；只有合成出 global Selmer
dimension bound 才算真正跨一步。

## Historical Routes

历史大路线已经压缩：

- `wl028-wl052`: proof-status / elliptic curve / Selmer 工具。
- `wl053-wl072`: partner graph / fast-core 工程。
- `wl073-wl104`: GEN-CLOSURE / modular filters / full-space scans。
- `wl105-wl161`: fixed-ratio / `sum=A+B` 探索。
- `wl162-wl202`: `R_lambda` / centerline。
- `wl203-wl293`: wl218 full-plane reciprocal route，未证明成功。

这些不是当前主线，只在需要追溯旧路线为什么关闭时阅读。

## Practical Next Step

继续主线时只看三件事：

1. `AA/BB/AA+BB` 的 remaining package 是否真的补成完整 local-image theorem。
2. dyadic local condition 是否能和 odd-prime 段落合并。
3. global Selmer dimension bound 是否能推出 rank zero。

如果第 3 步做不出来，这条 rank-zero Selmer 证明线就只是材料堆积，需要换方向。
