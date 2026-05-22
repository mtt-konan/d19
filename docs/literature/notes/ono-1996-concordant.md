# Ono 1996 — "Euler's concordant forms"

**全名**: Ono, K. (1996). Euler's concordant forms. *Acta Arithmetica* 78(2), 101–123.
**优先级**：⭐⭐⭐ 现代协调形式问题的奠基论文
**状态**：仅 abstract 读完，**待获取全文**

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

## Action items

| 优先 | 任务 |
|---|---|
| ⭐⭐⭐ | 下载全文 PDF（EUDML/ResearchGate）放到 `../pdfs/ono-1996-concordant-forms.pdf` |
| ⭐⭐⭐ | 精读 § 1-3，确认 $E_{M,N}$ 的定义和我们的 $E_{A,B}$ 一致 |
| ⭐⭐ | 读 § 4 看是否有 "$M = A^2, N = B^2$" 时的特殊结构 |
| ⭐ | 配套读 Ono 1996b "Rank zero quadratic twists" Compositio Math. 104 |
