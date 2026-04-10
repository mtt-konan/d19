# 实现设计文档

本文档记录搜索算法的关键设计决策和技术细节，供后续开发参考。

---

## 参数化与距离公式推导

单位正方形顶点：A(0,0)、B(1,0)、C(1,1)、D(0,1)。

取本原勾股数三元组 (p,q,r)（p²+q²=r²），令

```
P = (x, y) = (ap/(br),  aq/(br))，其中 gcd(a,b)=1，a,b>0
```

则 d(A) = k = a/b 自动为有理数。其余距离化简后：

```
d(B)² = (x-1)² + y²  →  分子 = (ar-bp)² + (bq)²  = tB
d(D)² = x² + (y-1)²  →  分子 = (ar-bq)² + (bp)²  = tD
d(C)² = (x-1)²+(y-1)²→  分子 = (ar-b(p+q))²+(b(p-q))² = tC
        公分母均为 (br)²
```

所以 d(B) 有理 ⟺ tB 是完全平方数。其余同理。**全部化为整数完全平方判断，无需 Fraction 运算。**

两种方向 (p,q,r) 和 (q,p,r) 均生成，覆盖 x↔y 对称情况。

---

## 搜索参数比例

三个参数之间有经验比例关系：
```
max_k_den ≈ 4 × max_m
max_k_num ≈ 8 × max_m
```

`--scale N` 即按此比例设置：`max_m=N, max_k_den=4N, max_k_num=8N`。
仍可在 `--scale` 后面单独覆盖任意参数。

---

## Numpy 向量化

`_search_triple_numpy()` 对每个三元组的所有 (a,b) 对一次性用数组运算处理：

```python
ar = a_arr * r          # shape (N,)
bp = b_arr * p
...
tB = (ar - bp)**2 + bq**2
okB, sB = _isqrt_vec(tB)
```

`_isqrt_vec(t)` 用 float64 sqrt 做初始估计，再用 `s*(s+1)` fallback 修正 float 舍入误差：

```python
s = np.floor(np.sqrt(t.astype(np.float64))).astype(np.int64)
ok = (s * s == t) | ((s + 1) * (s + 1) == t)
```

**精度边界**：int64 安全上限约 scale=600（tB_max ≈ 4×10¹⁸ < int64 最大值 9.2×10¹⁸）。

---

## 多进程模式

使用 `ProcessPoolExecutor` + `initializer` 模式：

```python
executor = ProcessPoolExecutor(
    max_workers=workers,
    initializer=_init_worker,
    initargs=(pairs_list, a_arr, b_arr),
)
```

- `_init_worker` 在每个子进程中设置模块级全局 `_WORKER_PAIRS`、`_WORKER_A`、`_WORKER_B`
- `_worker(args)` 必须是模块级函数（macOS `spawn` 限制，不能用 lambda 或闭包）
- numpy 数组通过 `initargs` 传入（不需要 pickle 每次任务）

---

## 侧边排除

**定理**（椭圆曲线方法证明）：满足到单位正方形任意三个顶点距离均为有理数的点，不能落在四条延伸边（x=0, x=1, y=0, y=1）上。

在参数化中：
- `x = ap/(br) = 1` ⟺ `a*p == b*r`
- `y = aq/(br) = 1` ⟺ `a*q == b*r`
- `x=0` 和 `y=0` 由正参数保证不可能出现

此过滤**对所有搜索无条件生效**（不区分 `min_rational=3` 或 `4`）。

虽然被过滤的候选仅占总量的约 0.0001%（加速可忽略），但显著提升结果纯净度：scale=80 时从 402 个结果降至 118 个，均为真正的非侧边解。

---

## D4 对称去重

单位正方形具有 D4 对称群（8 个变换）：

| 变换 | 公式 |
|------|------|
| 恒等 | (x, y) |
| 沿 x=½ 翻转 | (1-x, y) |
| 沿 y=½ 翻转 | (x, 1-y) |
| 180° 旋转 | (1-x, 1-y) |
| 沿主对角线翻转 | (y, x) |
| 沿副对角线翻转 | (1-y, 1-x) |
| 90° 顺时针 | (y, 1-x) |
| 90° 逆时针 | (1-y, x) |

`d4_images(x,y)` 返回去重后的 D4 轨道（用 `set` 自动合并对称轴上的重合像）。  
`canonical_xy(x,y)` 取字典序最小的像作为轨道代表元，用于去重键。

**轨道大小**：理论上为 1、2、4 或 8（整除 8）。搜索结果中出现"大小 2"是因为其余对称像落在负坐标区域或超出参数 k 的搜索范围，不在结果集内——这是搜索范围限制，不是数学错误。

**`dedup_by_symmetry(points)`** 逻辑：
1. 以 `canonical_xy(x,y)` 为键
2. 保留 `rational_count` 最高的代表；相等则取分母（`denominator`）最小的

---

## 结果排序

默认排序：`(-rational_count, denominator, x, y)`

- `rational_count` 降序：四顶点解排最前（如有），其次三顶点
- `denominator` 升序：`lcm(x.denominator, y.denominator)` 小的排前，即"最简单"的解排前
- `(x, y)` 升序：同等复杂度下字典序

---

## 已知限制与后续方向

1. **参数化仅覆盖 d(A) 有理的解**：以 A 为锚点。理论上可以 B/C/D 为锚，但 D4 对称保证了大部分覆盖。
2. **椭圆曲线方法**：对固定三元组，将"第四距离也有理"化为椭圆曲线上的有理点问题，可能得到无穷参数族，但尚未整合进搜索流程。
3. **大内存机器**：64GB RAM 允许更大 scale（如 300+）不受内存压力，直接加大 `--scale` 参数即可。
4. **int64 溢出边界**：scale ≈ 600 时接近 int64 上限，超过需切换 Python 原生 int 或 int128。
