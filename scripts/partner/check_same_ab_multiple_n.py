#!/usr/bin/env python3
"""
检验用户的几何推导：
对同一个(A,B)，如果有两个concordant值N_i, N_j满足倒数定理（N_i·N_j = A·B），
那么是否有 A² + B² = N_i² + N_j²，
进而推出点在对角线上（A = B）？
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from fractions import Fraction

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))

from rational_distance.concordant.multi_n_pairs import load_multi_n_pairs

def analyze_same_ab_pairs():
    """分析同一个(A,B)有多个N的情况"""

    print("加载multi-N pairs数据...")
    pairs_data = load_multi_n_pairs()

    # 按(A,B)分组，收集所有对应的N值
    ab_to_ns = defaultdict(list)

    for pair_key, n_values in pairs_data.items():
        a, b = pair_key
        for n in n_values:
            ab_to_ns[(a, b)].append(Fraction(n))

    print(f"总共 {len(ab_to_ns)} 个不同的(A,B) pairs")

    # 找出有多个N值的(A,B)
    multi_n_pairs = {ab: ns for ab, ns in ab_to_ns.items() if len(ns) >= 2}

    print(f"其中有 {len(multi_n_pairs)} 个(A,B)有多个concordant值")

    if len(multi_n_pairs) == 0:
        print("\n没有找到同一个(A,B)有多个N值的情况")
        print("这意味着每个(A,B)只对应一个唯一的N值")
        return

    # 分析这些multi-N pairs
    print("\n=== 分析同一(A,B)的多个N值 ===")

    reciprocal_count = 0
    diagonal_count = 0
    sum_squares_match = 0

    examples = []

    for (a, b), ns in list(multi_n_pairs.items())[:100]:  # 检查前100个
        lam = Fraction(a, b)

        # 检查所有N值对
        for i in range(len(ns)):
            for j in range(i+1, len(ns)):
                n_i, n_j = ns[i], ns[j]

                r_i = n_i / b
                r_j = n_j / b

                # 检查倒数关系
                product = n_i * n_j
                target_product = a * b
                is_reciprocal = (product == target_product)

                # 检查 A² + B² = N_i² + N_j²
                sum_sq_ab = a**2 + b**2
                sum_sq_nn = n_i**2 + n_j**2
                sum_squares_equal = (sum_sq_ab == sum_sq_nn)

                # 检查对角线
                is_diagonal = (a == b)

                if is_reciprocal:
                    reciprocal_count += 1

                if is_diagonal:
                    diagonal_count += 1

                if sum_squares_equal:
                    sum_squares_match += 1

                if len(examples) < 20:
                    examples.append({
                        "ab": (int(a), int(b)),
                        "n_i": float(n_i),
                        "n_j": float(n_j),
                        "lambda": float(lam),
                        "n_i_times_n_j": float(product),
                        "a_times_b": float(target_product),
                        "is_reciprocal": is_reciprocal,
                        "a_sq_plus_b_sq": int(sum_sq_ab) if sum_sq_ab.denominator == 1 else float(sum_sq_ab),
                        "n_i_sq_plus_n_j_sq": int(sum_sq_nn) if sum_sq_nn.denominator == 1 else float(sum_sq_nn),
                        "sum_squares_equal": sum_squares_equal,
                        "is_diagonal": is_diagonal
                    })

    print(f"\n统计结果：")
    print(f"  满足倒数关系 (N_i·N_j = A·B): {reciprocal_count}")
    print(f"  满足 A² + B² = N_i² + N_j²: {sum_squares_match}")
    print(f"  在对角线上 (A = B): {diagonal_count}")

    print(f"\n前20个例子：")
    for i, ex in enumerate(examples, 1):
        print(f"\n例子 {i}:")
        print(f"  (A,B) = {ex['ab']}, λ = {ex['lambda']:.6f}")
        print(f"  N_i = {ex['n_i']:.6f}, N_j = {ex['n_j']:.6f}")
        print(f"  N_i·N_j = {ex['n_i_times_n_j']:.6f}, A·B = {ex['a_times_b']:.6f}, 倒数: {ex['is_reciprocal']}")
        print(f"  A²+B² = {ex['a_sq_plus_b_sq']}, N_i²+N_j² = {ex['n_i_sq_plus_n_j_sq']}, 相等: {ex['sum_squares_equal']}")
        print(f"  对角线: {ex['is_diagonal']}")

    # 保存结果
    output = {
        "total_ab_pairs": len(ab_to_ns),
        "multi_n_pairs": len(multi_n_pairs),
        "reciprocal_pairs": reciprocal_count,
        "sum_squares_match": sum_squares_match,
        "diagonal_pairs": diagonal_count,
        "examples": examples
    }

    output_file = _ROOT / "results" / "partner" / "same_ab_multiple_n_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n完整结果已保存：{output_file}")

if __name__ == "__main__":
    analyze_same_ab_pairs()
