#!/usr/bin/env python3
"""
检验用户的几何推导：
从partner_full_bfs_edges.jsonl中，提取"同一个(A,B)的不同concordant值"，
检查是否满足：
1. N_i · N_j = A · B (倒数关系)
2. A² + B² = N_i² + N_j² (用户提出的等式)
3. A = B (对角线条件)
"""

import json
from pathlib import Path
from collections import defaultdict
from fractions import Fraction

def load_and_group_by_ab():
    """
    从partner_full_bfs_edges.jsonl加载数据

    edges格式：{"u": [A, B], "v": [C, D]}
    意味着(A,B)和(C,D)这两个multi-N pairs共享至少一个concordant值

    我们需要理解：对于同一个(A,B)，它可能通过不同的边连接到不同的pairs，
    这些连接可能对应不同的共享N值
    """
    edges_file = Path(__file__).resolve().parents[2] / "results" / "partner" / "partner_full_bfs_edges.jsonl"

    # 收集每个(A,B)的所有相邻节点
    neighbors = defaultdict(set)

    with open(edges_file) as f:
        for line in f:
            if not line.strip():
                continue
            edge = json.loads(line)
            u = tuple(edge["u"])
            v = tuple(edge["v"])

            neighbors[u].add(v)
            neighbors[v].add(u)

    return neighbors

def analyze_diagonal_hypothesis():
    """
    分析用户的假设：
    如果从partner graph的结构能推出 A² + B² = N₁² + N₂²，
    那么是否意味着 A = B（对角线）？
    """

    print("加载partner graph数据...")
    neighbors = load_and_group_by_ab()

    print(f"总共 {len(neighbors)} 个(A,B) pairs")

    # 统计
    total_pairs = 0
    diagonal_pairs = 0

    # 采样一些pairs检查
    sample_size = 1000
    examples = []

    import random
    sampled_pairs = random.sample(list(neighbors.keys()), min(sample_size, len(neighbors)))

    for ab in sampled_pairs:
        a, b = ab
        total_pairs += 1

        # 检查是否在对角线上
        is_diagonal = (a == b)
        if is_diagonal:
            diagonal_pairs += 1

        # 保存前20个例子
        if len(examples) < 20:
            examples.append({
                "ab": (a, b),
                "a_squared_plus_b_squared": a**2 + b**2,
                "is_diagonal": is_diagonal,
                "degree": len(neighbors[ab])
            })

    print(f"\n=== 统计结果（采样{sample_size}个pairs）===")
    print(f"总数: {total_pairs}")
    print(f"在对角线上 (A=B): {diagonal_pairs} ({100*diagonal_pairs/total_pairs:.2f}%)")

    print(f"\n前20个例子：")
    for i, ex in enumerate(examples, 1):
        print(f"{i}. (A,B)={ex['ab']}, A²+B²={ex['a_squared_plus_b_squared']}, 对角线={ex['is_diagonal']}, 度数={ex['degree']}")

    # 保存
    output_file = Path(__file__).resolve().parents[2] / "results" / "partner" / "diagonal_hypothesis_check.json"
    with open(output_file, 'w') as f:
        json.dump({
            "sample_size": sample_size,
            "total_pairs": total_pairs,
            "diagonal_pairs": diagonal_pairs,
            "diagonal_percentage": 100*diagonal_pairs/total_pairs if total_pairs > 0 else 0,
            "examples": examples
        }, f, indent=2)

    print(f"\n结果已保存：{output_file}")

    # 如果有对角线的例子，特别展示
    if diagonal_pairs > 0:
        print(f"\n=== 对角线例子 ===")
        diagonal_examples = [ex for ex in examples if ex['is_diagonal']]
        for ex in diagonal_examples[:10]:
            print(f"(A,B)={ex['ab']}, A²+B²={ex['a_squared_plus_b_squared']}, 度数={ex['degree']}")

def check_equation_directly():
    """
    直接验证：对于partner graph中的(A,B) pairs，
    检查是否存在某种模式使得 A² + B² 等于某个特殊值
    """
    print("\n=== 直接检查 A² + B² 的分布 ===")

    neighbors = load_and_group_by_ab()

    # 计算所有(A,B)的 A² + B²
    from collections import Counter
    sum_squares = Counter()

    for (a, b) in neighbors.keys():
        sum_sq = a**2 + b**2
        sum_squares[sum_sq] += 1

    # 找出最常见的值
    most_common = sum_squares.most_common(20)

    print(f"\nA² + B² 最常见的20个值：")
    for value, count in most_common:
        print(f"  {value}: {count}次")

    # 检查是否有 A² + B² = 2k² 的模式（对角线的变种）
    print(f"\n检查是否有 A² + B² = 2k² 的模式...")
    matches_2k_squared = 0

    for (a, b) in list(neighbors.keys())[:1000]:
        sum_sq = a**2 + b**2
        # 检查sum_sq/2是否是完全平方数
        if sum_sq % 2 == 0:
            half = sum_sq // 2
            sqrt_half = int(half ** 0.5)
            if sqrt_half * sqrt_half == half:
                matches_2k_squared += 1

    print(f"在前1000个pairs中，满足 A² + B² = 2k² 的有: {matches_2k_squared}")

if __name__ == "__main__":
    analyze_diagonal_hypothesis()
    check_equation_directly()
