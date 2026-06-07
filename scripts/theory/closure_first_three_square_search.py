#!/usr/bin/env python3
"""Closure-first search for full-plane 3-of-4 square near misses.

This script tests the route:

1. force one exact full-plane GEN-CLOSURE relation for ``(A, B, N1, N2)``;
2. check the four Pythagorean square conditions;
3. save candidates where exactly three conditions pass and one edge fails.

It is intentionally an exploration probe, not a proof.  The difference
relations ``|N1-N2| = target`` need a finite ``--diff-tail`` bound because
``N1`` can be shifted outward forever.
"""

from __future__ import annotations

import argparse
import heapq
import json
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.concordant.fast_multi_n import (  # noqa: E402
    _build_smallest_prime_factor,
    _factor_with_spf,
    concordant_n_for_leg,
)

CHECKS: tuple[tuple[str, str, str], ...] = (
    ("A-N1", "A", "N1"),
    ("B-N1", "B", "N1"),
    ("B-N2", "B", "N2"),
    ("A-N2", "A", "N2"),
)

RELATIONS = ("sum=A+B", "sum=|A-B|", "diff=A+B", "diff=|A-B|")


@dataclass(frozen=True)
class SquareCheck:
    is_square: bool
    value: int
    root: int | None
    nearest_root: int
    nearest_delta: int


def is_square_check(x: int) -> SquareCheck:
    root = isqrt(x)
    if root * root == x:
        return SquareCheck(True, x, root, root, 0)
    lower_delta = x - root * root
    upper_root = root + 1
    upper_delta = upper_root * upper_root - x
    if lower_delta <= upper_delta:
        return SquareCheck(False, x, None, root, lower_delta)
    return SquareCheck(False, x, None, upper_root, upper_delta)


def build_partner_sets(max_leg: int, max_n: int) -> list[set[int]]:
    """Return ``partners[x] = {N <= max_n: x^2 + N^2 is a square}``."""
    spf = _build_smallest_prime_factor(max_leg)
    partners: list[set[int]] = [set() for _ in range(max_leg + 1)]
    for leg in range(2, max_leg + 1):
        factors = _factor_with_spf(leg, spf)
        ns = concordant_n_for_leg(leg, tuple(factors.items()))
        partners[leg] = {n for n in ns if n <= max_n}
    return partners


def relation_target(a: int, b: int, relation: str) -> int:
    if relation.endswith("A+B"):
        return a + b
    return abs(a - b)


def forced_domain_size(a: int, b: int, relation: str, diff_tail: int) -> int:
    target = relation_target(a, b, relation)
    if target <= 0:
        return 0
    if relation.startswith("sum="):
        return target // 2
    return diff_tail


def potential_n1_values(
    union_partners: set[int],
    *,
    relation: str,
    target: int,
    diff_tail: int,
) -> list[int]:
    """Enumerate only N1 values that can possibly have >=3 square checks.

    For exactly 3/4 or 4/4 checks, both N1 and N2 must each be Pythagorean
    with at least one of A or B.  The union partner set captures that condition.
    """
    if target <= 0:
        return []
    out: set[int] = set()
    if relation.startswith("sum="):
        for n in union_partners:
            other = target - n
            if 1 <= n <= other and other in union_partners:
                out.add(n)
            if 1 <= other <= n and n in union_partners:
                out.add(other)
        return sorted(out)

    for n in union_partners:
        other = n + target
        if n <= diff_tail and other in union_partners:
            out.add(n)
    return sorted(out)


def square_checks_for(a: int, b: int, n1: int, n2: int) -> dict[str, SquareCheck]:
    values = {
        "A-N1": a * a + n1 * n1,
        "B-N1": b * b + n1 * n1,
        "B-N2": b * b + n2 * n2,
        "A-N2": a * a + n2 * n2,
    }
    return {name: is_square_check(value) for name, value in values.items()}


def check_to_json(check: SquareCheck) -> dict[str, Any]:
    out: dict[str, Any] = {
        "is_square": check.is_square,
        "value": check.value,
        "nearest_delta": check.nearest_delta,
        "nearest_root": check.nearest_root,
    }
    if check.root is not None:
        out["root"] = check.root
    return out


def closure_values(a: int, b: int, n1: int, n2: int) -> dict[str, int]:
    return {
        "A+B": a + b,
        "|A-B|": abs(a - b),
        "N1+N2": n1 + n2,
        "|N1-N2|": abs(n1 - n2),
    }


def square_coordinate_for(
    a: int, b: int, n1: int, n2: int, relation: str
) -> tuple[Fraction, Fraction, int]:
    """Return the unit-square coordinate represented by a closure relation.

    The integer square side length is the common closure target.  With the
    script's ``A < B`` and ``N1 <= N2`` orientation, sum means the coordinate is
    between the two parallel square sides, while difference means it is outside
    on the negative side.
    """
    del n2
    target = relation_target(a, b, relation)
    if target <= 0:
        raise ValueError(f"relation {relation!r} has non-positive target")
    x = Fraction(a, target) if relation.endswith("A+B") else Fraction(-a, target)
    y = Fraction(n1, target) if relation.startswith("sum=") else Fraction(-n1, target)
    return x, y, target


def d4_point_images(x: Fraction, y: Fraction) -> set[tuple[Fraction, Fraction]]:
    one = Fraction(1)
    return {
        (x, y),
        (one - x, y),
        (x, one - y),
        (one - x, one - y),
        (y, x),
        (one - y, one - x),
        (y, one - x),
        (one - y, x),
    }


def square_point_key_for(
    a: int, b: int, n1: int, n2: int, relation: str
) -> tuple[Fraction, Fraction]:
    x, y, _side = square_coordinate_for(a, b, n1, n2, relation)
    return x, y


def d4_point_key_for(a: int, b: int, n1: int, n2: int, relation: str) -> tuple[Fraction, Fraction]:
    x, y, _side = square_coordinate_for(a, b, n1, n2, relation)
    return min(d4_point_images(x, y))


def square_coordinate_to_json(x: Fraction, y: Fraction, side: int) -> dict[str, Any]:
    return {"x": str(x), "y": str(y), "side_n": side}


def d4_point_key_to_json(key: tuple[Fraction, Fraction]) -> list[str]:
    return [str(key[0]), str(key[1])]


def _record_sort_key(record: dict[str, Any]) -> tuple[int, int, int, int, int, int]:
    return (
        int(record["failed_nearest_delta"]),
        int(record["max_entry"]),
        int(record["A"]),
        int(record["B"]),
        int(record["N1"]),
        int(record["N2"]),
    )


def update_d4_point_records(
    best_records: dict[tuple[Fraction, Fraction], dict[str, Any]],
    raw_counts: Counter[tuple[Fraction, Fraction]],
    d4_key: tuple[Fraction, Fraction],
    record: dict[str, Any],
) -> None:
    raw_counts[d4_key] += 1
    current = best_records.get(d4_key)
    if current is None or _record_sort_key(record) < _record_sort_key(current):
        best_records[d4_key] = record


def slim_sample_for_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "A": record["A"],
        "B": record["B"],
        "N1": record["N1"],
        "N2": record["N2"],
        "relation": record["relation"],
        "missing_edges": record["missing_edges"],
        "failed_nearest_delta": record["failed_nearest_delta"],
        "square_coordinate": record["square_coordinate"],
    }


def sorted_d4_point_records(
    best_records: dict[tuple[Fraction, Fraction], dict[str, Any]],
    raw_counts: Counter[tuple[Fraction, Fraction]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for key, record in best_records.items():
        x, y = key
        records.append(
            {
                "x": str(x),
                "y": str(y),
                "x_float": float(x),
                "y_float": float(y),
                "raw_count": raw_counts[key],
                "best_failed_nearest_delta": int(record["failed_nearest_delta"]),
                "best_missing_edges": record["missing_edges"],
                "best_relation": record["relation"],
                "best_sample": slim_sample_for_record(record),
            }
        )
    return sorted(records, key=lambda item: (item["x_float"], item["y_float"]))


def record_for(
    a: int,
    b: int,
    n1: int,
    n2: int,
    relation: str,
    checks: dict[str, SquareCheck],
) -> dict[str, Any]:
    missing = [name for name, check in checks.items() if not check.is_square]
    failed_delta = sum(checks[name].nearest_delta for name in missing)
    x, y, side = square_coordinate_for(a, b, n1, n2, relation)
    d4_key = d4_point_key_for(a, b, n1, n2, relation)
    return {
        "A": a,
        "B": b,
        "N1": n1,
        "N2": n2,
        "relation": relation,
        "square_count": 4 - len(missing),
        "missing_edges": missing,
        "failed_nearest_delta": failed_delta,
        "max_entry": max(a, b, n1, n2),
        "gcd_AB": gcd(a, b),
        "gcd_N1N2": gcd(n1, n2),
        "closure_values": closure_values(a, b, n1, n2),
        "square_coordinate": square_coordinate_to_json(x, y, side),
        "d4_point_key": d4_point_key_to_json(d4_key),
        "square_checks": {name: check_to_json(check) for name, check in checks.items()},
    }


def push_top(
    heap: list[tuple[tuple[int, int, int, int, int, int], int, dict[str, Any]]],
    record: dict[str, Any],
    *,
    top_k: int,
    sequence: int,
) -> None:
    key = (
        int(record["failed_nearest_delta"]),
        int(record["max_entry"]),
        int(record["A"]),
        int(record["B"]),
        int(record["N1"]),
        int(record["N2"]),
    )
    # heapq is a min-heap; store negated key so the worst saved record is on top.
    heap_item = (tuple(-x for x in key), sequence, record)
    if len(heap) < top_k:
        heapq.heappush(heap, heap_item)
    elif heap_item > heap[0]:
        heapq.heapreplace(heap, heap_item)


def sorted_top(
    heap: list[tuple[tuple[int, int, int, int, int, int], int, dict[str, Any]]],
) -> list[dict[str, Any]]:
    return [
        item[2]
        for item in sorted(
            heap,
            key=lambda item: (
                item[2]["failed_nearest_delta"],
                item[2]["max_entry"],
                item[2]["A"],
                item[2]["B"],
                item[2]["N1"],
                item[2]["N2"],
            ),
        )
    ]


def sorted_counter_top(counter: Counter[int], limit: int) -> list[tuple[int, int]]:
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit]


def counter_range(counter: Counter[int], start: int, end: int) -> dict[str, int]:
    return {str(i): counter[i] for i in range(start, end + 1) if counter[i]}


def signed_counter_abs_range(counter: Counter[int], start: int, end: int) -> dict[str, int]:
    return {str(i): counter[i] for i in sorted(counter) if start <= abs(i) <= end and counter[i]}


def set_counter_range(
    counter: dict[int, set[tuple[Fraction, Fraction]]], start: int, end: int
) -> dict[str, int]:
    return {str(i): len(counter[i]) for i in range(start, end + 1) if counter[i]}


def signed_set_counter_abs_range(
    counter: dict[int, set[tuple[Fraction, Fraction]]], start: int, end: int
) -> dict[str, int]:
    return {
        str(i): len(counter[i]) for i in sorted(counter) if start <= abs(i) <= end and counter[i]
    }


def nested_counter_range(
    counters: dict[str, Counter[int]], start: int, end: int
) -> dict[str, dict[str, int]]:
    return {
        key: values
        for key, counter in sorted(counters.items())
        if (values := counter_range(counter, start, end))
    }


def nested_set_counter_range(
    counters: dict[str, dict[int, set[tuple[Fraction, Fraction]]]], start: int, end: int
) -> dict[str, dict[str, int]]:
    return {
        key: values
        for key, counter in sorted(counters.items())
        if (values := set_counter_range(counter, start, end))
    }


def scan_legacy(
    max_leg: int, diff_tail: int, top_k: int, *, include_d4_points: bool = False
) -> dict[str, Any]:
    max_n = 2 * max_leg + diff_tail
    partners = build_partner_sets(max_leg, max_n)

    relation_domain: Counter[str] = Counter()
    relation_potential: Counter[str] = Counter()
    square_count_hist: Counter[int] = Counter()
    exact_hits_by_relation: Counter[str] = Counter()
    near_miss_by_relation: Counter[str] = Counter()
    missing_edge_counts: Counter[str] = Counter()
    gcd_ab_counts: Counter[int] = Counter()
    gcd_n_counts: Counter[int] = Counter()
    failed_delta_counts: Counter[int] = Counter()
    failed_signed_delta_counts: Counter[int] = Counter()
    failed_delta_by_relation: dict[str, Counter[int]] = defaultdict(Counter)
    failed_delta_by_missing_edge: dict[str, Counter[int]] = defaultdict(Counter)
    near_miss_point_keys: set[tuple[Fraction, Fraction]] = set()
    near_miss_d4_point_keys: set[tuple[Fraction, Fraction]] = set()
    d4_point_best_records: dict[tuple[Fraction, Fraction], dict[str, Any]] = {}
    d4_point_raw_counts: Counter[tuple[Fraction, Fraction]] = Counter()
    failed_delta_d4_point_keys: dict[int, set[tuple[Fraction, Fraction]]] = defaultdict(set)
    failed_signed_delta_d4_point_keys: dict[int, set[tuple[Fraction, Fraction]]] = defaultdict(set)
    failed_delta_d4_point_keys_by_relation: dict[str, dict[int, set[tuple[Fraction, Fraction]]]] = (
        defaultdict(lambda: defaultdict(set))
    )
    failed_delta_d4_point_keys_by_missing_edge: dict[
        str, dict[int, set[tuple[Fraction, Fraction]]]
    ] = defaultdict(lambda: defaultdict(set))
    top_heap: list[tuple[tuple[int, int, int, int, int, int], int, dict[str, Any]]] = []
    exact_hits: list[dict[str, Any]] = []
    sequence = 0

    for a in range(1, max_leg + 1):
        pa = partners[a]
        for b in range(a + 1, max_leg + 1):
            pb = partners[b]
            union = pa | pb
            if not union:
                continue
            for relation in RELATIONS:
                target = relation_target(a, b, relation)
                relation_domain[relation] += forced_domain_size(a, b, relation, diff_tail)
                n1_values = potential_n1_values(
                    union,
                    relation=relation,
                    target=target,
                    diff_tail=diff_tail,
                )
                relation_potential[relation] += len(n1_values)
                for n1 in n1_values:
                    n2 = target - n1 if relation.startswith("sum=") else n1 + target
                    if n2 <= 0 or n1 > n2:
                        continue
                    checks = square_checks_for(a, b, n1, n2)
                    square_count = sum(1 for check in checks.values() if check.is_square)
                    square_count_hist[square_count] += 1
                    if square_count == 4:
                        exact_hits_by_relation[relation] += 1
                        if len(exact_hits) < top_k:
                            exact_hits.append(record_for(a, b, n1, n2, relation, checks))
                    elif square_count == 3:
                        record = record_for(a, b, n1, n2, relation, checks)
                        near_miss_by_relation[relation] += 1
                        missing = str(record["missing_edges"][0])
                        failed_delta = int(record["failed_nearest_delta"])
                        failed_check = checks[missing]
                        signed_delta = failed_check.value - failed_check.nearest_root**2
                        point_key = square_point_key_for(a, b, n1, n2, relation)
                        d4_key = d4_point_key_for(a, b, n1, n2, relation)
                        near_miss_point_keys.add(point_key)
                        near_miss_d4_point_keys.add(d4_key)
                        update_d4_point_records(
                            d4_point_best_records, d4_point_raw_counts, d4_key, record
                        )
                        failed_delta_counts[failed_delta] += 1
                        failed_signed_delta_counts[signed_delta] += 1
                        failed_delta_by_relation[relation][failed_delta] += 1
                        failed_delta_by_missing_edge[missing][failed_delta] += 1
                        failed_delta_d4_point_keys[failed_delta].add(d4_key)
                        failed_signed_delta_d4_point_keys[signed_delta].add(d4_key)
                        failed_delta_d4_point_keys_by_relation[relation][failed_delta].add(d4_key)
                        failed_delta_d4_point_keys_by_missing_edge[missing][failed_delta].add(
                            d4_key
                        )
                        missing_edge_counts[missing] += 1
                        gcd_ab_counts[int(record["gcd_AB"])] += 1
                        gcd_n_counts[int(record["gcd_N1N2"])] += 1
                        push_top(top_heap, record, top_k=top_k, sequence=sequence)
                        sequence += 1

    result = {
        "max_leg": max_leg,
        "diff_tail": diff_tail,
        "max_n_precomputed": max_n,
        "candidate_strategy": "legacy_union_scan",
        "relations": list(RELATIONS),
        "forced_domain_size_by_relation": dict(relation_domain),
        "forced_domain_size_total": sum(relation_domain.values()),
        "potential_candidates_by_relation": dict(relation_potential),
        "potential_candidates_total": sum(relation_potential.values()),
        "square_count_histogram_on_potential": {
            str(k): square_count_hist[k] for k in sorted(square_count_hist)
        },
        "exact_hits_by_relation": dict(exact_hits_by_relation),
        "exact_hits_sample": exact_hits,
        "near_miss_3of4_by_relation": dict(near_miss_by_relation),
        "near_miss_3of4_total": sum(near_miss_by_relation.values()),
        "near_miss_3of4_coordinate_point_total": len(near_miss_point_keys),
        "near_miss_3of4_raw_minus_coordinate_point_total": (
            sum(near_miss_by_relation.values()) - len(near_miss_point_keys)
        ),
        "near_miss_3of4_d4_point_total": len(near_miss_d4_point_keys),
        "near_miss_3of4_raw_minus_d4_point_total": (
            sum(near_miss_by_relation.values()) - len(near_miss_d4_point_keys)
        ),
        "near_miss_3of4_coordinate_point_minus_d4_point_total": (
            len(near_miss_point_keys) - len(near_miss_d4_point_keys)
        ),
        "missing_edge_counts": dict(missing_edge_counts),
        "failed_delta_counts_1_to_10": counter_range(failed_delta_counts, 1, 10),
        "failed_signed_delta_counts_1_to_10": signed_counter_abs_range(
            failed_signed_delta_counts, 1, 10
        ),
        "failed_delta_d4_point_counts_1_to_10": set_counter_range(
            failed_delta_d4_point_keys, 1, 10
        ),
        "failed_signed_delta_d4_point_counts_1_to_10": signed_set_counter_abs_range(
            failed_signed_delta_d4_point_keys, 1, 10
        ),
        "failed_delta_1_to_10_by_relation": nested_counter_range(failed_delta_by_relation, 1, 10),
        "failed_delta_1_to_10_by_missing_edge": nested_counter_range(
            failed_delta_by_missing_edge, 1, 10
        ),
        "failed_delta_d4_point_1_to_10_by_relation": nested_set_counter_range(
            failed_delta_d4_point_keys_by_relation, 1, 10
        ),
        "failed_delta_d4_point_1_to_10_by_missing_edge": nested_set_counter_range(
            failed_delta_d4_point_keys_by_missing_edge, 1, 10
        ),
        "failed_delta_counts_top": sorted_counter_top(failed_delta_counts, 20),
        "gcd_AB_counts_top": sorted_counter_top(gcd_ab_counts, 20),
        "gcd_N1N2_counts_top": sorted_counter_top(gcd_n_counts, 20),
        "top_near_misses": sorted_top(top_heap),
    }
    if include_d4_points:
        result["d4_point_records"] = sorted_d4_point_records(
            d4_point_best_records, d4_point_raw_counts
        )
    return result


def build_common_partner_map(partners: list[set[int]]) -> dict[tuple[int, int], list[int]]:
    """Return pairs ``(A, B)`` together with their shared Pythagorean ``N`` values.

    Any 3-of-4 square candidate must have one of ``N1`` or ``N2`` connected to
    both ``A`` and ``B``. Therefore ``A`` and ``B`` must share at least one
    common partner. This map is the main speed-up over scanning every pair.
    """
    legs_by_n: dict[int, list[int]] = defaultdict(list)
    for leg, ns in enumerate(partners):
        for n in ns:
            legs_by_n[n].append(leg)

    common: dict[tuple[int, int], list[int]] = defaultdict(list)
    for n, legs in legs_by_n.items():
        legs.sort()
        for i, a in enumerate(legs):
            for b in legs[i + 1 :]:
                common[(a, b)].append(n)

    return {pair: sorted(ns) for pair, ns in common.items()}


def _three_edge_candidates_for_relation(
    pa: set[int],
    pb: set[int],
    common_ns: list[int],
    *,
    relation: str,
    target: int,
    diff_tail: int,
) -> set[tuple[int, int]]:
    """Generate only candidates where at least three edges are forced square."""
    if target <= 0:
        return set()

    candidates: set[tuple[int, int]] = set()
    if relation.startswith("sum="):
        for n2 in common_ns:
            n1 = target - n2
            if 1 <= n1 <= n2 and (n1 in pa or n1 in pb):
                candidates.add((n1, n2))
        for n1 in common_ns:
            n2 = target - n1
            if n1 <= n2 and (n2 in pa or n2 in pb):
                candidates.add((n1, n2))
        return candidates

    for n2 in common_ns:
        n1 = n2 - target
        if 1 <= n1 <= diff_tail and (n1 in pa or n1 in pb):
            candidates.add((n1, n2))
    for n1 in common_ns:
        n2 = n1 + target
        if n1 <= diff_tail and (n2 in pa or n2 in pb):
            candidates.add((n1, n2))
    return candidates


def _square_count_from_partners(
    pa: set[int], pb: set[int], n1: int, n2: int
) -> tuple[int, list[str]]:
    checks = {
        "A-N1": n1 in pa,
        "B-N1": n1 in pb,
        "B-N2": n2 in pb,
        "A-N2": n2 in pa,
    }
    missing = [name for name, ok in checks.items() if not ok]
    return 4 - len(missing), missing


def scan_fast(
    max_leg: int, diff_tail: int, top_k: int, *, include_d4_points: bool = False
) -> dict[str, Any]:
    max_n = 2 * max_leg + diff_tail
    partners = build_partner_sets(max_leg, max_n)
    common_partner_map = build_common_partner_map(partners)

    relation_domain: Counter[str] = Counter()
    relation_potential: Counter[str] = Counter()
    square_count_hist: Counter[int] = Counter()
    exact_hits_by_relation: Counter[str] = Counter()
    near_miss_by_relation: Counter[str] = Counter()
    missing_edge_counts: Counter[str] = Counter()
    gcd_ab_counts: Counter[int] = Counter()
    gcd_n_counts: Counter[int] = Counter()
    failed_delta_counts: Counter[int] = Counter()
    failed_signed_delta_counts: Counter[int] = Counter()
    failed_delta_by_relation: dict[str, Counter[int]] = defaultdict(Counter)
    failed_delta_by_missing_edge: dict[str, Counter[int]] = defaultdict(Counter)
    near_miss_point_keys: set[tuple[Fraction, Fraction]] = set()
    near_miss_d4_point_keys: set[tuple[Fraction, Fraction]] = set()
    d4_point_best_records: dict[tuple[Fraction, Fraction], dict[str, Any]] = {}
    d4_point_raw_counts: Counter[tuple[Fraction, Fraction]] = Counter()
    failed_delta_d4_point_keys: dict[int, set[tuple[Fraction, Fraction]]] = defaultdict(set)
    failed_signed_delta_d4_point_keys: dict[int, set[tuple[Fraction, Fraction]]] = defaultdict(set)
    failed_delta_d4_point_keys_by_relation: dict[str, dict[int, set[tuple[Fraction, Fraction]]]] = (
        defaultdict(lambda: defaultdict(set))
    )
    failed_delta_d4_point_keys_by_missing_edge: dict[
        str, dict[int, set[tuple[Fraction, Fraction]]]
    ] = defaultdict(lambda: defaultdict(set))
    top_heap: list[tuple[tuple[int, int, int, int, int, int], int, dict[str, Any]]] = []
    exact_hits: list[dict[str, Any]] = []
    sequence = 0

    def process_candidate(
        a: int,
        b: int,
        pa: set[int],
        pb: set[int],
        relation: str,
        n1: int,
        n2: int,
    ) -> None:
        nonlocal sequence
        square_count, missing_edges = _square_count_from_partners(pa, pb, n1, n2)
        square_count_hist[square_count] += 1
        if square_count == 4:
            exact_hits_by_relation[relation] += 1
            if len(exact_hits) < top_k:
                checks = square_checks_for(a, b, n1, n2)
                exact_hits.append(record_for(a, b, n1, n2, relation, checks))
        elif square_count == 3:
            checks = square_checks_for(a, b, n1, n2)
            record = record_for(a, b, n1, n2, relation, checks)
            near_miss_by_relation[relation] += 1
            missing_edge_counts[missing_edges[0]] += 1
            failed_delta = int(record["failed_nearest_delta"])
            failed_check = checks[missing_edges[0]]
            signed_delta = failed_check.value - failed_check.nearest_root**2
            point_key = square_point_key_for(a, b, n1, n2, relation)
            d4_key = d4_point_key_for(a, b, n1, n2, relation)
            near_miss_point_keys.add(point_key)
            near_miss_d4_point_keys.add(d4_key)
            update_d4_point_records(d4_point_best_records, d4_point_raw_counts, d4_key, record)
            failed_delta_counts[failed_delta] += 1
            failed_signed_delta_counts[signed_delta] += 1
            failed_delta_by_relation[relation][failed_delta] += 1
            failed_delta_by_missing_edge[missing_edges[0]][failed_delta] += 1
            failed_delta_d4_point_keys[failed_delta].add(d4_key)
            failed_signed_delta_d4_point_keys[signed_delta].add(d4_key)
            failed_delta_d4_point_keys_by_relation[relation][failed_delta].add(d4_key)
            failed_delta_d4_point_keys_by_missing_edge[missing_edges[0]][failed_delta].add(d4_key)
            gcd_ab_counts[int(record["gcd_AB"])] += 1
            gcd_n_counts[int(record["gcd_N1N2"])] += 1
            push_top(top_heap, record, top_k=top_k, sequence=sequence)
            sequence += 1

    for (a, b), common_ns in common_partner_map.items():
        pa = partners[a]
        pb = partners[b]
        ab_sum = a + b
        ab_diff = b - a
        relation_domain["sum=A+B"] += ab_sum // 2
        relation_domain["sum=|A-B|"] += ab_diff // 2
        relation_domain["diff=A+B"] += diff_tail
        relation_domain["diff=|A-B|"] += diff_tail

        for relation, is_sum, target in (
            ("sum=A+B", True, ab_sum),
            ("sum=|A-B|", True, ab_diff),
            ("diff=A+B", False, ab_sum),
            ("diff=|A-B|", False, ab_diff),
        ):
            seen_candidates: set[tuple[int, int]] | None = None
            if is_sum:
                for n2 in common_ns:
                    n1 = target - n2
                    if 1 <= n1 <= n2 and (n1 in pa or n1 in pb):
                        candidate = (n1, n2)
                        if seen_candidates is None:
                            seen_candidates = {candidate}
                        elif candidate in seen_candidates:
                            continue
                        else:
                            seen_candidates.add(candidate)
                        relation_potential[relation] += 1
                        process_candidate(a, b, pa, pb, relation, n1, n2)
                for n1 in common_ns:
                    n2 = target - n1
                    if n1 <= n2 and (n2 in pa or n2 in pb):
                        candidate = (n1, n2)
                        if seen_candidates is None:
                            seen_candidates = {candidate}
                        elif candidate in seen_candidates:
                            continue
                        else:
                            seen_candidates.add(candidate)
                        relation_potential[relation] += 1
                        process_candidate(a, b, pa, pb, relation, n1, n2)
            else:
                for n2 in common_ns:
                    n1 = n2 - target
                    if 1 <= n1 <= diff_tail and (n1 in pa or n1 in pb):
                        candidate = (n1, n2)
                        if seen_candidates is None:
                            seen_candidates = {candidate}
                        elif candidate in seen_candidates:
                            continue
                        else:
                            seen_candidates.add(candidate)
                        relation_potential[relation] += 1
                        process_candidate(a, b, pa, pb, relation, n1, n2)
                for n1 in common_ns:
                    n2 = n1 + target
                    if n1 <= diff_tail and (n2 in pa or n2 in pb):
                        candidate = (n1, n2)
                        if seen_candidates is None:
                            seen_candidates = {candidate}
                        elif candidate in seen_candidates:
                            continue
                        else:
                            seen_candidates.add(candidate)
                        relation_potential[relation] += 1
                        process_candidate(a, b, pa, pb, relation, n1, n2)

    result = {
        "max_leg": max_leg,
        "diff_tail": diff_tail,
        "max_n_precomputed": max_n,
        "candidate_strategy": "three_edge_common_n",
        "relations": list(RELATIONS),
        "common_partner_pairs": len(common_partner_map),
        "forced_domain_size_by_relation": dict(relation_domain),
        "forced_domain_size_total": sum(relation_domain.values()),
        "potential_candidates_by_relation": dict(relation_potential),
        "potential_candidates_total": sum(relation_potential.values()),
        "square_count_histogram_on_potential": {
            str(k): square_count_hist[k] for k in sorted(square_count_hist)
        },
        "exact_hits_by_relation": dict(exact_hits_by_relation),
        "exact_hits_sample": exact_hits,
        "near_miss_3of4_by_relation": dict(near_miss_by_relation),
        "near_miss_3of4_total": sum(near_miss_by_relation.values()),
        "near_miss_3of4_coordinate_point_total": len(near_miss_point_keys),
        "near_miss_3of4_raw_minus_coordinate_point_total": (
            sum(near_miss_by_relation.values()) - len(near_miss_point_keys)
        ),
        "near_miss_3of4_d4_point_total": len(near_miss_d4_point_keys),
        "near_miss_3of4_raw_minus_d4_point_total": (
            sum(near_miss_by_relation.values()) - len(near_miss_d4_point_keys)
        ),
        "near_miss_3of4_coordinate_point_minus_d4_point_total": (
            len(near_miss_point_keys) - len(near_miss_d4_point_keys)
        ),
        "missing_edge_counts": dict(missing_edge_counts),
        "failed_delta_counts_1_to_10": counter_range(failed_delta_counts, 1, 10),
        "failed_signed_delta_counts_1_to_10": signed_counter_abs_range(
            failed_signed_delta_counts, 1, 10
        ),
        "failed_delta_d4_point_counts_1_to_10": set_counter_range(
            failed_delta_d4_point_keys, 1, 10
        ),
        "failed_signed_delta_d4_point_counts_1_to_10": signed_set_counter_abs_range(
            failed_signed_delta_d4_point_keys, 1, 10
        ),
        "failed_delta_1_to_10_by_relation": nested_counter_range(failed_delta_by_relation, 1, 10),
        "failed_delta_1_to_10_by_missing_edge": nested_counter_range(
            failed_delta_by_missing_edge, 1, 10
        ),
        "failed_delta_d4_point_1_to_10_by_relation": nested_set_counter_range(
            failed_delta_d4_point_keys_by_relation, 1, 10
        ),
        "failed_delta_d4_point_1_to_10_by_missing_edge": nested_set_counter_range(
            failed_delta_d4_point_keys_by_missing_edge, 1, 10
        ),
        "failed_delta_counts_top": sorted_counter_top(failed_delta_counts, 20),
        "gcd_AB_counts_top": sorted_counter_top(gcd_ab_counts, 20),
        "gcd_N1N2_counts_top": sorted_counter_top(gcd_n_counts, 20),
        "top_near_misses": sorted_top(top_heap),
    }
    if include_d4_points:
        result["d4_point_records"] = sorted_d4_point_records(
            d4_point_best_records, d4_point_raw_counts
        )
    return result


def scan(
    max_leg: int, diff_tail: int, top_k: int, *, include_d4_points: bool = False
) -> dict[str, Any]:
    return scan_fast(max_leg, diff_tail, top_k, include_d4_points=include_d4_points)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-leg", type=int, default=100)
    parser.add_argument(
        "--diff-tail",
        type=int,
        default=300,
        help="For difference relations, scan 1 <= min(N1,N2) <= diff_tail.",
    )
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument(
        "--include-d4-points",
        action="store_true",
        help="Include one serializable representative for each D4-distinct near-miss point.",
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    if args.max_leg < 2:
        raise SystemExit("--max-leg must be >= 2")
    if args.diff_tail < 1:
        raise SystemExit("--diff-tail must be >= 1")
    if args.top_k < 1:
        raise SystemExit("--top-k must be >= 1")

    out = args.out
    if out is None:
        out = Path(
            "results/counterexample_first/2026-06-07/"
            f"closure_first_3of4_max{args.max_leg}_tail{args.diff_tail}.json"
        )

    started = time.perf_counter()
    result = scan(
        args.max_leg, args.diff_tail, args.top_k, include_d4_points=args.include_d4_points
    )
    result.update(
        {
            "generated_at": datetime.now(UTC).isoformat(),
            "elapsed_s": round(time.perf_counter() - started, 3),
            "command": " ".join(sys.argv),
            "predicate": (
                "force one exact full-plane GEN-CLOSURE relation, then keep "
                "exact 3-of-4 Pythagorean square near misses"
            ),
            "boundedness_note": (
                "Sum relations are exhaustive for A<B<=max_leg. Difference relations are "
                "bounded by --diff-tail because translating both N values outward keeps "
                "the same difference relation."
            ),
        }
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"wrote {out}")
    print(
        "3/4 near misses:",
        result["near_miss_3of4_total"],
        "three-edge candidates:",
        result["potential_candidates_total"],
        "exact hits:",
        sum(result["exact_hits_by_relation"].values()),
        f"elapsed={result['elapsed_s']}s",
    )
    if result["top_near_misses"]:
        best = result["top_near_misses"][0]
        print(
            "best:",
            {
                "A": best["A"],
                "B": best["B"],
                "N1": best["N1"],
                "N2": best["N2"],
                "relation": best["relation"],
                "missing": best["missing_edges"],
                "delta": best["failed_nearest_delta"],
            },
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
