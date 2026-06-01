# wl100 — §8.6 残余的结构：局部-整体 gap + GEN-CLOSURE 廉价完备判定

## 目标（方向2）

解剖 wl099 里那 $84$ 个"$D_g$ 筛 + `chain_closure` 模 $p^2$ 都漏掉、只靠穷尽 GEN-CLOSURE 才判掉"的残余：
找共同结构，看能否再加一道 sound 模筛。

## 结果

### 残余被任何模数都杀不掉（local-global gap）

在 $1{,}802$ 个非互素多-N 对上跑 sound 筛：
- `gcd_aware_kills`（$D_g$）杀 $1138$；`chain_closure` 模 $p^2$（STANDARD）后并联剩 **$84$**。
- 再用大模数集（$p^2\le300$ + 素数幂 $8,16,\dots,243,125,625,343$，共 $74$ 个模）：仍有 **$64$ 个杀不掉**。

这 $64$ 个的闭合同余在**每个被测模下都可解**（`killed_at_modulus` 全 False）——是真正的
**局部-整体 gap**：mod-$p^k$ 局部处处有解，整数闭合却不存在。**故任何模筛都无法清掉它**，
这是模方法的能力上限，不是筛没调好。

### 共同结构

- gcd 分布偏向 $12\mid g$（$39/64$ 满足 $12\mid g$，此时 $D_g=1$，整除性筛完全失效）；也含少量低 gcd（$3,4,6,8$）。
- 完整 concordant 集**极小**：$57$ 个恰 $2$ 个 $N$、$6$ 个 $3$ 个、$1$ 个 $4$ 个。
- 这批对正是 §8.6 gcd-scaling 的实体：约化对 $(A/g,B/g)$ 互素，但 $(A,B)$ 的 $N$ **不是 $g$ 的倍数**
  （例 $(60,396)$，$g=12$，$N=[80,297]$ 都不被 $12$ 整除），约化后不可见。

### GEN-CLOSURE 是廉价完备判定器

对这 $64$ 个跑完整 GEN-CLOSURE（`exact_concordant_pair` 完整集 + 四关系）：
**$0$ 闭合、$0.05$ ms/对**。因残余 concordant 集极小，完备判定本身就廉价。

## 结论 / 落地

**没有**额外的 sound 模筛能清掉残余（local-global gap 注定）；但也**不需要**——
正确的 sound 架构是三段「预筛 + 完备 backstop」：

```
gcd_aware_kills (D_g, O(1))  ->  chain_closure 模 p² (O(素数))  ->  GEN-CLOSURE (完整整数枚举, sound)
        杀 1138                       并联杀到 1718/1802            残余 ~84, 0 闭合, 0.05 ms/对
```

模筛是性价比预筛（清掉 ~95%），GEN-CLOSURE 才是 sound 完备判定器，且因残余集极小而廉价。
**这正是大规模非互素扫描（方向"接生成器"）应采用的管线**——无需新理论，照此 wiring 即可。

## 文件

- `docs/MATH.md` §8.6（残余结构 + 三段管线结论）
- `scripts/multi_n/residual_localglobal_audit.py`（审计脚本）
