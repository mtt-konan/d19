#!/usr/bin/env python3
"""
验证用户的几何推导：

根据wl223，partner edge的含义是：
  {"u": [A, B], "v": [N_i, N_j]}
  表示(A,B)有两个concordant值N_i和N_j，
  因此生成边 (A,B) -> (N_i, N_j)

用户的推导：
  对同一个(A,B)，如果两个concordant值N_i, N_j满足：
  1. 转成 r_i = N_i/B, r_j = N_j/B 后满足closure
  2. 倒数定理：r_i · r_j = λ = A/B
  那么可以推出：A² + B² = N_i² + N_j²
  进而得到：点在对角线上（A = B）
"""

import json
from pathlib import Path
from fractions import Fraction
from collections import Counter

def analyze_partner_edges_geometry():
    """分析partner edges的几何性质"""

    edges_file = Path(__file__).resolve().parents[2] / "results" / "partner" / "partner_full_bfs_edges.jsonl"

    print("加载partner edges数据...")

    # 统计
    total_edges = 0
    reciprocal_pairs = 0
    sum_squares_equal = 0
    diagonal_u = 0
    diagonal_v = 0

    examples = []

    with open(edges_file) as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue

            edge = json.loads(line)
            a, b = edge["u"]
            n_i, n_j = edge["v"]

            total_edges += 1

            # 计算关键量
            lam = Fraction(a, b)
            product_n = n_i * n_j
            product_ab = a * b

            # 检查倒数关系：N_i · N_j = A · B
            is_reciprocal = (product_n == product_ab)
            if is_reciprocal:
                reciprocal_pairs += 1

            # 检查 A² + B² = N_i² + N_j²
            sum_sq_ab = a**2 + b**2
            sum_sq_nn = n_i**2 + n_j**2
            sum_squares_match = (sum_sq_ab == sum_sq_nn)
            if sum_squares_match:
                sum_squares_equal += 1

            # 检查对角线
            is_diag_u = (a == b)
            is_diag_v = (n_i == n_j)
            if is_diag_u:
                diagonal_u += 1
            if is_diag_v:
                diagonal_v += 1

            # 保存前50个例子
            if len(examples) < 50:
                examples.append({
                    "u": (a, b),
                    "v": (n_i, n_j),
                    "lambda": float(lam),
                    "n_i_times_n_j": product_n,
                    "a_times_b": product_ab,
                    "is_reciprocal": is_reciprocal,
                    "a_sq_plus_b_sq": sum_sq_ab,
                    "n_i_sq_plus_n_j_sq": sum_sq_nn,
                    "sum_squares_equal": sum_squares_match,
                    "u_diagonal": is_diag_u,
                    "v_diagonal": is_diag_v
                })

            # 只处理前10000条以加速
            if line_num >= 10000:
                break

    print(f"\n=== 统计结果（前{total_edges}条边）===")
    print(f"总边数: {total_edges}")
    print(f"满足倒数关系 (N_i·N_j = A·B): {reciprocal_pairs} ({100*reciprocal_pairs/total_edges:.2f}%)")
    print(f"满足 A²+B² = N_i²+N_j²: {sum_squares_equal} ({100*sum_squares_equal/total_edges:.2f}%)")
    print(f"u在对角线上 (A=B): {diagonal_u} ({100*diagonal_u/total_edges:.2f}%)")
    print(f"v在对角线上 (N_i=N_j): {diagonal_v} ({100*diagonal_v/total_edges:.2f}%)")

    print(f"\n=== 前20个例子 ===")
    for i, ex in enumerate(examples[:20], 1):
        print(f"\n例子 {i}:")
        print(f"  u=(A,B)={ex['u']}, v=(N_i,N_j)={ex['v']}")
        print(f"  N_i·N_j={ex['n_i_times_n_j']}, A·B={ex['a_times_b']}, 倒数={ex['is_reciprocal']}")
        print(f"  A²+B²={ex['a_sq_plus_b_sq']}, N_i²+N_j²={ex['n_i_sq_plus_n_j_sq']}, 相等={ex['sum_squares_equal']}")
        print(f"  u对角线={ex['u_diagonal']}, v对角线={ex['v_diagonal']}")

    # 找出满足倒数关系的例子
    reciprocal_examples = [ex for ex in examples if ex['is_reciprocal']]
    if reciprocal_examples:
        print(f"\n=== 满足倒数关系的例子（共{len(reciprocal_examples)}个）===")
        for i, ex in enumerate(reciprocal_examples[:10], 1):
            print(f"\n倒数例子 {i}:")
            print(f"  u=(A,B)={ex['u']}, v=(N_i,N_j)={ex['v']}")
            print(f"  A²+B²={ex['a_sq_plus_b_sq']}, N_i²+N_j²={ex['n_i_sq_plus_n_j_sq']}, 相等={ex['sum_squares_equal']}")
            print(f"  u对角线={ex['u_diagonal']}, v对角线={ex['v_diagonal']}")

    # 找出满足等式的例子
    sum_sq_examples = [ex for ex in examples if ex['sum_squares_equal']]
    if sum_sq_examples:
        print(f"\n=== 满足A²+B²=N_i²+N_j²的例子（共{len(sum_sq_examples)}个）===")
        for i, ex in enumerate(sum_sq_examples[:10], 1):
            print(f"\n等式例子 {i}:")
            print(f"  u=(A,B)={ex['u']}, v=(N_i,N_j)={ex['v']}")
            print(f"  倒数={ex['is_reciprocal']}")
            print(f"  u对角线={ex['u_diagonal']}, v对角线={ex['v_diagonal']}")

    # 保存
    output_file = Path(__file__).resolve().parents[2] / "results" / "partner" / "partner_edge_geometry_analysis.json"
    with open(output_file, 'w') as f:
        json.dump({
            "total_edges": total_edges,
            "reciprocal_pairs": reciprocal_pairs,
            "sum_squares_equal": sum_squares_equal,
            "diagonal_u": diagonal_u,
            "diagonal_v": diagonal_v,
            "examples": examples[:100]
        }, f, indent=2)

    print(f"\n结果已保存：{output_file}")

if __name__ == "__main__":
    analyze_partner_edges_geometry()
