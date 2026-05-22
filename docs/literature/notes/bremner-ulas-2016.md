# Bremner & Ulas 2016 — "Points at rational distances from the vertices of certain geometric objects"

**全名**: Bremner, A. & Ulas, M. (2016). Points at rational distances from the vertices of certain geometric objects. *Journal of Number Theory* 158, 104–133.
**arXiv preprint**: 1502.07312
**DOI**: 10.1016/j.jnt.2015.06.012
**优先级**：⭐⭐ 5 点 rational distance 通用框架（与 4-chain 几乎同构）
**状态**：abstract 读完

---

## 摘要要点（搜索片段拼出的）

> "We consider various problems related to finding points in $\mathbb{Q}^2$ and in $\mathbb{Q}^3$ which lie at rational distance from the vertices of some specified geometric object, for example, a square or rectangle in $\mathbb{Q}^2$, and a cube or tetrahedron in $\mathbb{Q}^3$."
>
> Keywords: "rational points, elliptic surfaces, rational distances set"
>
> "$\mathbb{Q}^3$ with rational distances to the six vertices of the unit cube"
>
> "Theorem 2.1. The set of $a \in \mathbb{Q}$ such that there are infinitely many rational points ... [from vertices of certain object]"

## 与 d19 的关系

**这是 d19 问题的"广义版"**：
- d19：5 点（1 个 inner + 4 个 corner）距离全有理 + 边长整数
- Bremner-Ulas：5/6 点（square, rectangle, tetrahedron, cube）vertices 距离全有理

**主要差别**：
- Bremner-Ulas 关心**任意有理距离**，不要求 chain 结构
- d19 关心 chain 结构（这是更强的约束）

但他们的 elliptic surface 工具 / parametric search 思路完全适用 d19。

## 应追踪的关键定理

1. **Theorem 2.1**：参数化哪些 $a \in \mathbb{Q}$ 使得有无穷多有理点（对某 geometric object）
2. **Cube case** 的 elliptic surface 分析（与 perfect cuboid 直接相关）
3. **Square case** 的具体结果（**d19 应该直接引用并对比**）

## Action items

| 优先 | 任务 |
|---|---|
| ⭐⭐⭐ | 从 arXiv 1502.07312 下载 PDF（无墙）放到 `../pdfs/` |
| ⭐⭐⭐ | 精读 § Square in Q² 部分，对比 d19 的 chain 条件 |
| ⭐⭐ | 找 Theorem 2.1 的精确陈述，可能可以直接用作 d19 反向论证 |
