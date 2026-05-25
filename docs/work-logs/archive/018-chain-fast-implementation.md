# 018 — chain-fast: O(n²) 原始三元组对搜索

## 背景

在 017 中，推导了将四顶点问题化简为二元组枚举的数学框架。
本工作日志记录该算法的实现。

## 实现

新增模块 `src/rational_distance/search_chain_fast.py`，函数 `find_chains_fast(max_hyp, progress)`。

### 算法核心

给定两个原始勾股三元组 T1=(s1,t1,h1)、T2=(s2,t2,h2)（斜边 ≤ max_hyp）：

1. 计算耦合约数 g = gcd(t1, s2)，令 s2r = s2/g，t1r = t1/g
2. 计算候选四元组：
   - a = s1·s2r，b = s2r·t1，c = t1r·t2，d = N = s2r·(s1-t1) + t1r·t2
   - 由构造，a+c = b+d 自动成立
3. 验证 C3：(t1r·t2)² + N² 是完全平方数
4. 验证 C4：N² + (s1·s2r)² 是完全平方数
5. 通过二面体群（8 元素）去重

### 关键性质

- g 的引入使 gcd(s2r, t1r) = 1，输出为原始代表元（最小正整数倍数代表）
- 单位正方形点 P = (a/k, b/k) 对同族的任意倍数保持不变
- 交叉积族（ac=bd）自动排除（需要 s2=t2，但原始三元组两腿不等）

### 性能

| max_hyp | 三元组数 | 检验对数 | 耗时 |
|---------|---------|---------|------|
| 500 | 160 | 25,600 | 0.01s |
| 5,000 | 1,584 | 2,509,056 | 0.9s |
| 20,000 | 6,372 | 40,602,384 | 14.8s |

相比原始 chain 搜索（O(n⁴)），在相当参数范围内快约 4 个数量级。

## CLI 入口

```bash
uv run python scripts/search.py chain-fast --max-hyp 1000
uv run python scripts/search.py chain-fast --max-hyp 5000 --out fast.json
```

## 测试

在 `tests/test_all.py` 中新增 `TestChainFast` 类（7 个测试）：全部通过（共 72 个测试）。

## 当前搜索结果

所有已测试范围（max_hyp ≤ 20000）均未找到解，与 Harborth 猜想一致。
