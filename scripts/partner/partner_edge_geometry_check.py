#!/usr/bin/env python3
"""
检验partner edges的几何性质：
用户猜想：a²+b² = n₁²+n₂² 对应对角线及其延长线

在partner graph中：
- 边连接两个(A,B) pairs，因为它们共享concordant值N
- 检查：A₁² + B₁² 与 A₂² + B₂² 的关系
- 检查：是否与共享的N有关系
"""

import json
from pathlib import Path
from fractions import Fraction
from collections import defaultdict, Counter

def load_partner_edges():
    """加载partner edges数据

    格式：{"u": [A, B], "v": [N_i, N_j]}
    u是multi-N pair (A,B)
    v是另一个multi-N pair (N_i, N_j)
    它们之间有边，意味着共享某个concordant值
    """
    edges_file = Path(__file__).resolve().parents[2] / "results" / "partner" / "partner_full_bfs_edges.jsonl"

    edges = []
    with open(edges_file) as f:
        for line in f:
            if not line.strip():
                continue
            edge_data = json.loads(line)

            # u和v都是(A,B)形式的multi-N pairs
            a1, b1 = edge_data["u"]
            a2, b2 = edge_data["v"]

            edges.append({
                "a1": a1,
                "b1": b1,
                "a2": a2,
                "b2": b2
            })

    return edges

def check_geometric_property(edges, sample_size=1000):
    """检查几何性质"""

    # 统计数据
    total = 0
    sum_squares_equal = 0  # A₁² + B₁² = A₂² + B₂²

    # 采样检查
    import random
    sample = random.sample(edges, min(sample_size, len(edges)))

    detailed_examples = []

    for edge in sample:
        a1, b1 = edge["a1"], edge["b1"]
        a2, b2 = edge["a2"], edge["b2"]

        # 计算 A² + B²
        sum_sq_1 = a1**2 + b1**2
        sum_sq_2 = a2**2 + b2**2

        total += 1

        # 检查 A₁² + B₁² = A₂² + B₂²
        if sum_sq_1 == sum_sq_2:
            sum_squares_equal += 1

        # 保存前几个例子
        if len(detailed_examples) < 10:
            detailed_examples.append({
                "pair1": (a1, b1),
                "pair2": (a2, b2),
                "sum_sq_1": sum_sq_1,
                "sum_sq_2": sum_sq_2,
                "sum_sq_equal": sum_sq_1 == sum_sq_2
            })

    return {
        "total_checked": total,
        "sum_squares_equal": sum_squares_equal,
        "detailed_examples": detailed_examples
    }

def analyze_diagonal_condition(edges, sample_size=1000):
    """
    检查对角线条件：A = B
    如果partner edges满足对角线性质，应该有 A₁ = B₁ 或 A₂ = B₂
    """
    import random
    sample = random.sample(edges, min(sample_size, len(edges)))

    diagonal_count = 0
    both_diagonal = 0

    for edge in sample:
        a1, b1 = edge["a1"], edge["b1"]
        a2, b2 = edge["a2"], edge["b2"]

        is_diag_1 = (a1 == b1)
        is_diag_2 = (a2 == b2)

        if is_diag_1 or is_diag_2:
            diagonal_count += 1

        if is_diag_1 and is_diag_2:
            both_diagonal += 1

    return {
        "total_checked": len(sample),
        "at_least_one_diagonal": diagonal_count,
        "both_diagonal": both_diagonal
    }

def main():
    print("加载partner edges数据...")
    edges = load_partner_edges()
    print(f"总共 {len(edges)} 条边")

    print("\n=== 检查几何性质：A² + B² ===")
    geom_result = check_geometric_property(edges, sample_size=5000)

    print(f"\n采样检查：{geom_result['total_checked']} 条边")
    print(f"  A₁² + B₁² = A₂² + B₂²: {geom_result['sum_squares_equal']} ({100*geom_result['sum_squares_equal']/geom_result['total_checked']:.1f}%)")

    print("\n前10个例子：")
    for i, ex in enumerate(geom_result['detailed_examples'][:10], 1):
        print(f"\n例子 {i}:")
        print(f"  Pair1: {ex['pair1']}, A₁²+B₁² = {ex['sum_sq_1']}")
        print(f"  Pair2: {ex['pair2']}, A₂²+B₂² = {ex['sum_sq_2']}")
        print(f"  相等: {ex['sum_sq_equal']}")

    print("\n=== 检查对角线条件：A = B ===")
    diag_result = analyze_diagonal_condition(edges, sample_size=5000)
    print(f"\n采样检查：{diag_result['total_checked']} 条边")
    print(f"  至少一个pair在对角线上 (A=B): {diag_result['at_least_one_diagonal']} ({100*diag_result['at_least_one_diagonal']/diag_result['total_checked']:.1f}%)")
    print(f"  两个pair都在对角线上: {diag_result['both_diagonal']} ({100*diag_result['both_diagonal']/diag_result['total_checked']:.2f}%)")

    # 保存结果
    output_file = Path(__file__).resolve().parents[2] / "results" / "partner" / "partner_edge_geometry_check.json"
    with open(output_file, 'w') as f:
        json.dump({
            "geometric_property": geom_result,
            "diagonal_condition": diag_result
        }, f, indent=2)

    print(f"\n完整结果已保存：{output_file}")

if __name__ == "__main__":
    main()
