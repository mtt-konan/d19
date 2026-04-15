"""CLI output helpers for the search entrypoint."""

from __future__ import annotations

import heapq
import json
from math import gcd
from pathlib import Path


def _header() -> str:
    return (
        f"{'cnt':>3}  {'den':>7}  {'x':>14}  {'y':>14}  "
        f"{'d(A)':>10}  {'d(B)':>10}  {'d(C)':>10}  {'d(D)':>10}"
    )


def _row(pt) -> str:
    def fmt(d):
        return f"{d!s:>10}" if d is not None else f"{'?':>10}"

    dA, dB, dC, dD = pt.distances
    return (
        f"{pt.rational_count:>3}  {pt.denominator:>7}  "
        f"{pt.x!s:>14}  {pt.y!s:>14}  "
        f"{fmt(dA)}  {fmt(dB)}  {fmt(dC)}  {fmt(dD)}"
    )


def _size_estimate(max_m: int, max_k_num: int, max_k_den: int) -> str:
    n_triples = (
        sum(
            1
            for m in range(2, max_m + 1)
            for n in range(1, m)
            if (m - n) % 2 == 1 and gcd(m, n) == 1
        )
        * 2
    )
    n_pairs = sum(
        1 for b in range(1, max_k_den + 1) for a in range(1, max_k_num + 1) if gcd(a, b) == 1
    )
    total = n_triples * n_pairs
    if total >= 1_000_000_000:
        return f"{total / 1e9:.1f}B"
    if total >= 1_000_000:
        return f"{total / 1e6:.1f}M"
    return f"{total:,}"


def _print_summary(results, elapsed, deduped_from=None):
    count_by_n: dict[int, int] = {}
    for pt in results:
        count_by_n[pt.rational_count] = count_by_n.get(pt.rational_count, 0) + 1

    print(f"\n{'─' * 72}")
    if deduped_from is not None and deduped_from != len(results):
        print(
            f"Found {deduped_from} points → {len(results)} orbits after D4 dedup  ({elapsed:.2f}s)"
        )
    else:
        print(f"Found {len(results)} unique points in {elapsed:.2f}s")
    for n in sorted(count_by_n, reverse=True):
        marker = " ◄ 4-VERTEX SOLUTION!" if n == 4 else ""
        print(f"  {count_by_n[n]:6d}  points with {n}/4 rational distances{marker}")
    print(f"{'─' * 72}\n")
    return count_by_n


def _print_table(results, top):
    display = results if top == 0 else results[:top]
    print(_header())
    print("─" * 85)
    for pt in display:
        print(_row(pt))
    if top and len(results) > top:
        print(f"  … {len(results) - top} more rows omitted (use --top 0 to see all)")


def _print_four_vertex(results):
    four = [pt for pt in results if pt.rational_count == 4]
    if four:
        print(f"\n{'!' * 72}")
        print(f"  {len(four)} POINT(S) WITH ALL FOUR RATIONAL DISTANCES:")
        for pt in four:
            print(f"  {pt}")
        print(f"{'!' * 72}")
    else:
        print("\n(No 4-vertex solutions found in this search range.)")


def _save_json(
    path: str,
    method: str,
    params: dict,
    elapsed: float,
    results,
    count_by_n: dict,
    backend: str = "",
) -> None:
    payload = {
        "method": method,
        "backend": backend,
        "search_params": params,
        "elapsed_seconds": round(elapsed, 3),
        "total_found": len(results),
        "count_by_rational": {str(k): v for k, v in count_by_n.items()},
        "points": [pt.as_dict() for pt in results],
    }
    Path(path).write_text(json.dumps(payload, indent=2))
    print(f"\nResults written to {path}")


class _NearMissTopK:
    """Keep the best near-misses by smallest sq4_deficit then sq3_deficit."""

    def __init__(self, limit: int) -> None:
        self.limit = max(0, limit)
        self.seen = 0
        self._heap: list[tuple[tuple[int, ...], tuple[int, int, int, int]]] = []
        self._selected: dict[tuple[int, int, int, int], dict] = {}

    @staticmethod
    def _order(row: dict) -> tuple[int, int, int, int, int, int]:
        return (
            int(row["sq4_deficit"]),
            int(row["sq3_deficit"]),
            int(row["a"]),
            int(row["b_val"]),
            int(row["c"]),
            int(row["d"]),
        )

    @classmethod
    def _reverse_order(cls, row: dict) -> tuple[int, ...]:
        return tuple(-part for part in cls._order(row))

    def _current_worst(
        self,
    ) -> tuple[tuple[int, int, int, int, int, int], tuple[int, int, int, int]] | None:
        while self._heap:
            reverse_order, identity = self._heap[0]
            row = self._selected.get(identity)
            if row is None or reverse_order != self._reverse_order(row):
                heapq.heappop(self._heap)
                continue
            return (self._order(row), identity)
        return None

    def consider(
        self,
        a: int,
        b_val: int,
        c: int,
        d: int,
        c3_ok: bool,
        c4_ok: bool,
        sq3: int,
        sq4: int,
        h3: int,
        h4: int,
    ) -> None:
        self.seen += 1
        if self.limit <= 0:
            return

        row = {
            "a": int(a),
            "b_val": int(b_val),
            "c": int(c),
            "d": int(d),
            "c3_ok": bool(c3_ok),
            "c4_ok": bool(c4_ok),
            "sq3": int(sq3),
            "sq4": int(sq4),
            "h3": int(h3),
            "h4": int(h4),
            "sq3_deficit": int(sq3 - h3 * h3),
            "sq4_deficit": int(sq4 - h4 * h4),
        }
        identity = (row["a"], row["b_val"], row["c"], row["d"])
        existing = self._selected.get(identity)
        if existing is not None and self._order(existing) <= self._order(row):
            return
        if existing is not None:
            self._selected[identity] = row
            heapq.heappush(self._heap, (self._reverse_order(row), identity))
            return

        if len(self._selected) < self.limit:
            self._selected[identity] = row
            heapq.heappush(self._heap, (self._reverse_order(row), identity))
            return

        current_worst = self._current_worst()
        if current_worst is None:
            self._selected[identity] = row
            heapq.heappush(self._heap, (self._reverse_order(row), identity))
            return

        worst_order, worst_identity = current_worst
        if self._order(row) < worst_order:
            del self._selected[worst_identity]
            heapq.heappop(self._heap)
            self._selected[identity] = row
            heapq.heappush(self._heap, (self._reverse_order(row), identity))

    def rows(self) -> list[dict]:
        return sorted(self._selected.values(), key=self._order)

    @property
    def saved(self) -> int:
        return len(self._selected)

    @property
    def dropped(self) -> int:
        return self.seen - self.saved


def _print_chain_fast_profile(profile: dict) -> None:
    print("\nProfile:")
    print(
        f"  triples={profile['n_triples']}  pairs={profile['n_pairs_total']}  "
        f"after_safe_pair={profile['n_pairs_after_safe_pair_sieve']}  "
        f"after_filters={profile['n_pairs_after_basic_filters']}  "
        f"after_c3_mod={profile['n_pairs_after_c3_mod_sieve']}"
    )
    print(
        f"  c3_pass={profile['n_c3_pass']}  c4_pass={profile['n_c4_pass']}  "
        "solutions(before/after dedup)="
        f"{profile['n_solutions_before_dedup']}/{profile['n_solutions_after_dedup']}"
    )
    print(
        f"  near_miss seen/saved/dropped="
        f"{profile['near_miss_seen']}/{profile['near_miss_saved']}/{profile['near_miss_dropped']}"
    )
    print(
        f"  time_s: triples={profile['time_generate_triples_s']:.3f}  "
        f"outer={profile['time_outer_loop_s']:.3f}  "
        f"safe_pair={profile['time_safe_pair_sieve_s']:.3f}  "
        f"filter={profile['time_filter_s']:.3f}  "
        f"mod_c3={profile['time_mod_sieve_c3_s']:.3f}  c3={profile['time_c3_s']:.3f}  "
        f"c4={profile['time_c4_s']:.3f}  "
        f"dedup={profile['time_dedup_s']:.3f}  db={profile['time_db_write_s']:.3f}"
    )
    print(
        f"  safe_pair_sieve={profile['safe_pair_sieve_enabled']}  "
        f"mod_sieve={profile['mod_sieve_enabled']}  "
        f"moduli={profile['mod_sieve_moduli']}"
    )
    if profile.get("db_bytes_after_run", 0):
        print(
            f"  db_bytes_after_run={profile['db_bytes_after_run']}  "
            f"triples_source={profile['triples_source']}"
        )


def _print_concordant_profile(profile: dict) -> None:
    print("\nConcordant profile")
    print(
        f"  rank_enabled={profile['rank_enabled']}  deep={profile['deep']}  "
        f"safe_pair_sieve={profile['safe_pair_sieve_enabled']}"
    )
    print(
        "  pair sieve: "
        f"kept={profile['n_pairs_after_safe_pair_sieve']}  "
        f"rejected={profile['n_pairs_rejected_by_safe_pair_sieve']}  "
        f"(mixed_parity={profile['n_pairs_rejected_mixed_parity']}, "
        f"odd_odd_mod4={profile['n_pairs_rejected_mod4']})"
    )
    print(
        f"  pairs total/completed/failed="
        f"{profile['n_pairs_total']}/{profile['n_pairs_completed']}/{profile['n_pairs_failed']}"
    )
    print(
        f"  hits: concordant={profile['n_pairs_with_concordant']}  "
        f"chain={profile['n_pairs_with_chain_compatible']}  "
        f"mirror={profile['n_pairs_with_mirror_hit']}  "
        f"c1={profile['n_pairs_with_c1_hit']}  "
        f"c2={profile['n_pairs_with_c2_hit']}  "
        f"side={profile['n_pairs_with_side_hit']}"
    )
    print(
        f"  values: raw_square_x={profile['n_raw_square_x_total']}  "
        f"concordant_n={profile['n_concordant_n_total']}  "
        f"candidates={profile['n_candidates_total']}  "
        f"deep_extra={profile['n_deep_extra_total']}"
    )
    print(
        f"  time_s: pair_gen={profile['time_pair_generation_s']:.3f}  "
        f"safe_pair={profile['time_safe_pair_sieve_s']:.3f}  "
        f"pari_init={profile['time_pari_init_s']:.3f}  "
        f"rank={profile['time_rank_s']:.3f}  "
        f"find={profile['time_find_concordant_s']:.3f}  "
        f"chain={profile['time_chain_compat_s']:.3f}  "
        f"deep={profile['time_deep_search_s']:.3f}  "
        f"diagnostics={profile['time_candidate_diagnostics_s']:.3f}  "
        f"pair_total={profile['time_pair_analysis_s']:.3f}  "
        f"post={profile['time_postprocess_s']:.3f}  "
        f"json={profile['time_json_write_s']:.3f}"
    )
    if profile["n_pairs_completed"] > 0:
        print(
            f"  avg pair time="
            f"{profile['time_pair_analysis_s'] / profile['n_pairs_completed']:.6f}s"
        )


__all__ = [
    "_NearMissTopK",
    "_print_chain_fast_profile",
    "_print_concordant_profile",
    "_print_four_vertex",
    "_print_summary",
    "_print_table",
    "_save_json",
    "_size_estimate",
]
