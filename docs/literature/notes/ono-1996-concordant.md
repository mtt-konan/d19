# Ono 1996 — "Euler's concordant forms"

**全名**: Ono, K. (1996). Euler's concordant forms. *Acta Arithmetica* 78(2), 101–123.
**优先级**：⭐⭐⭐ 现代协调形式问题的奠基论文
**状态**：PDF 已获取；§1-3 关键段已抽取
**本地 PDF**：`../pdfs/ono-1996-eulers-concordant-forms.pdf`
**抽取文本**：`../pdfs/ono-1996-eulers-concordant-forms.txt`

---

## 一句话总结

Ono 把 Euler 1700s 提的协调形式问题（$x^2 + My^2 = t^2$ 和 $x^2 + Ny^2 = z^2$ 同解）系统翻译成椭圆曲线 $E_{M,N}: y^2 = x(x+M)(x+N)$ 上找有理点的现代框架，用模形式 + L-函数技术处理 rank-0 family。

## 与 d19 的关系

**这是 d19 椭圆曲线族的 namesake**：
- Ono 写法：$y^2 = x(x+M)(x+N)$，参数 $M, N$
- d19 写法：$Y^2 = X(X+A^2)(X+B^2)$，参数 $A^2, B^2$

它们的关系：d19 的 $E_{A,B}$ 是 Ono 框架的 $E_{M,N}$ 在 $M = A^2, N = B^2$ 时的**特殊子族**。

**意义**：d19 项目的整个 EC 计算栈，本质上是在做"Ono 协调形式问题"的一个特殊参数化（约束 $M, N$ 都是平方数）下的有限性分析。

## 应追踪的关键结果

1. **rank-0 family 的结构定理**（Ono 1996b: "Rank zero quadratic twists" Compositio Math.）
2. **模形式 → BSD 部分进展**：Ono 用 Waldspurger 类型公式处理 rank 偶数情况
3. **协调形式存在/不存在的部分判据**

## 已确认关键结论

### 1. 正秩意味着无限多 primitive solutions

Ono 的模型：

```text
E_Q(M,N): y^2 = x^3 + (M+N)x^2 + MNx = x(x+M)(x+N)
```

论文开头直接给出：

```text
If E_Q(M,N) has positive rank, then there are infinitely many primitive
integer solutions to x^2 + M y^2 = t^2, x^2 + N y^2 = z^2.
```

d19 的曲线是 `M=A^2, N=B^2` 的特殊子族。因此 `(153,560)` rank=3 与多个
concordant `N` 是同一个背景下的现象。

### 2. 但 d19 的 multi-N 比 Ono primitive solution 更强

Ono 的 primitive solution 允许一般 `(x,y,t,z)` 且 `gcd(x,y)=1`。
d19 的 concordant `N` 固定为：

```text
y = 1
x = N
N^2 + A^2 = square
N^2 + B^2 = square
```

椭圆曲线坐标则是：

```text
X = N^2
Y = N * sqrt(N^2+A^2) * sqrt(N^2+B^2)
```

所以 `rank > 0` 是“有无限多 primitive 解”的机制，但不是“有多个整数 N”的充分条件。
multi-N 是正秩曲线上的 square-x / `y=1` 特殊截面问题。

### 3. torsion 分类对 d19 子族的启发

Ono Main Theorem 1 分类了 `E_Q(M,N)` 的 torsion：

- `Z2 × Z4`：当 `M,N` 都是平方，或 `-M,N-M` 都是平方，或 `-N,M-N` 都是平方。
- `Z2 × Z8`：来自 Pythagorean triple 的四次幂 family。
- `Z2 × Z6`：来自 `M=a^4+2a^3b, N=2ab^3+b^4` 的 family。
- 其他情况下只有 `Z2 × Z2`。

对 d19 子族 `M=A^2,N=B^2`，自动落入 `Z2 × Z4` 条件。但 Ono 的 Main Corollary 1
说明非平凡 primitive 解由 `Z2 × Z8` 或 `Z2 × Z6` torsion 给出；`Z2 × Z4`
本身不提供非平凡 primitive 解。因此 d19 中真正有价值的 multi-N 样本仍应主要来自正秩。

### 4. rank-zero / twist families 是排除工具

Ono Main Theorem 2/3 用 ternary quadratic forms 和 lacunary modular forms 描述
部分 quadratic twists 的 rank 0 / positive-rank 条件。这对 d19 的用途是：

```text
给定某些比例 family 的 (M,N)，可用表示数差异判定 rank 0，从而排除 primitive solution。
```

但这些 family 未直接覆盖一般 `M=A^2,N=B^2`，更适合作为理论背景和未来批量 family 分析的模板。

## Action items

| 优先 | 任务 |
|---|---|
| ✅ | 下载全文 PDF，已放到 `../pdfs/ono-1996-eulers-concordant-forms.pdf` |
| ✅ | 抽取文本：`uv run python scripts/utility/extract_pdf_text.py docs/literature/pdfs/ono-1996-eulers-concordant-forms.pdf` |
| ✅ | 精读 § 1-3，确认 $E_{M,N}$ 的定义和我们的 $E_{A,B}$ 一致 |
| ⭐⭐ | 读 § 4 看是否有 "$M = A^2, N = B^2$" 时的特殊结构 |
| ⭐ | 配套读 Ono 1996b "Rank zero quadratic twists" Compositio Math. 104 |
