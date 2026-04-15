"""Pure chain-fast scanning kernels."""

from __future__ import annotations

import time
from dataclasses import dataclass
from math import gcd, isqrt

from rational_distance.search_chain import ChainResult

from .bucket_stats import BucketStatsCollector, build_bucket_identities
from .mod_sieve import DEFAULT_C3_MOD_SIEVE
from .safe_pair_sieve import decide_safe_pair_sieve, passes_n_mod4_requirement

try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised only when numpy is missing
    np = None  # type: ignore[assignment]

NearMissRecord = tuple[int, int, int, int, bool, bool, int, int, int, int]


@dataclass
class ScanProfile:
    n_pairs_total: int = 0
    n_pairs_after_safe_pair_sieve: int = 0
    n_pairs_after_basic_filters: int = 0
    n_pairs_after_c3_mod_sieve: int = 0
    n_c3_pass: int = 0
    n_c4_pass: int = 0
    n_solutions_before_dedup: int = 0
    n_near_miss: int = 0
    time_safe_pair_sieve_s: float = 0.0
    time_filter_s: float = 0.0
    time_mod_sieve_c3_s: float = 0.0
    time_c3_s: float = 0.0
    time_c4_s: float = 0.0

    def merge(self, other: ScanProfile) -> None:
        self.n_pairs_total += other.n_pairs_total
        self.n_pairs_after_safe_pair_sieve += other.n_pairs_after_safe_pair_sieve
        self.n_pairs_after_basic_filters += other.n_pairs_after_basic_filters
        self.n_pairs_after_c3_mod_sieve += other.n_pairs_after_c3_mod_sieve
        self.n_c3_pass += other.n_c3_pass
        self.n_c4_pass += other.n_c4_pass
        self.n_solutions_before_dedup += other.n_solutions_before_dedup
        self.n_near_miss += other.n_near_miss
        self.time_safe_pair_sieve_s += other.time_safe_pair_sieve_s
        self.time_filter_s += other.time_filter_s
        self.time_mod_sieve_c3_s += other.time_mod_sieve_c3_s
        self.time_c3_s += other.time_c3_s
        self.time_c4_s += other.time_c4_s


def _append_solution_if_valid(
    solutions: list[ChainResult],
    a: int,
    b: int,
    c: int,
    d: int,
    x1: int,
    x2: int,
    x3: int,
    x4: int,
) -> None:
    solutions.append(
        ChainResult(a=a, b=b, c=c, d=d, x1=x1, x2=x2, x3=x3, x4=x4, square_ok=True)
    )


def _numpy_scan_t1(
    i: int,
    triples: list[tuple[int, int, int]],
    s_arr,
    t_arr,
    collect_profile: bool = False,
    safe_pair_sieve_enabled: bool = False,
    mod_sieve_enabled: bool = False,
    collect_bucket_stats: bool = False,
) -> tuple[list[ChainResult], list[NearMissRecord], ScanProfile, BucketStatsCollector | None]:
    """Vectorised inner T2 loop for one outer T1 iteration."""
    if np is None:  # pragma: no cover - guarded by backend selection
        raise RuntimeError("numpy backend requested but numpy is not installed")
    if safe_pair_sieve_enabled:  # pragma: no cover - guarded by API/CLI validation
        raise RuntimeError("safe-pair-sieve currently supports only the python backend")

    s1, t1, h1 = triples[i]
    solutions: list[ChainResult] = []
    near_misses: list[NearMissRecord] = []
    scan_profile = ScanProfile(
        n_pairs_total=len(triples),
        n_pairs_after_safe_pair_sieve=len(triples),
    )
    bucket_stats = BucketStatsCollector() if collect_bucket_stats else None

    filter_started = time.perf_counter() if collect_profile else 0.0
    cg = np.gcd(np.int64(t1), s_arr)
    s2r = s_arr // cg
    t1r = np.int64(t1) // cg

    A = t1r * t_arr
    B = np.int64(s1) * s2r
    N = s2r * np.int64(s1 - t1) + A
    b_all = s2r * np.int64(t1)

    mask = N > 0
    mask &= A % 2 == B % 2  # P1
    even = A % 2 == 0
    mask &= ((even & (A % 4 == 0) & (B % 4 == 0)) | (~even & (b_all % 4 == 0) & (N % 4 == 0)))
    mask &= (b_all != B) & (B != A) & (B != N) & (b_all != A) & (b_all != N) & (A != N)
    scan_profile.n_pairs_after_basic_filters = int(np.count_nonzero(mask))
    if collect_profile:
        scan_profile.time_filter_s = time.perf_counter() - filter_started

    if not np.any(mask):
        if bucket_stats is not None:
            for j, (s2, t2, _) in enumerate(triples):
                bucket_ids = build_bucket_identities(s1, t1, s2, t2, int(cg[j]))
                bucket_stats.note_total(bucket_ids)
        return solutions, near_misses, scan_profile, bucket_stats

    j_idx = np.where(mask)[0]
    A_m = A[mask]
    B_m = B[mask]
    N_m = N[mask]
    b_m = b_all[mask]

    if mod_sieve_enabled:
        mod_started = time.perf_counter() if collect_profile else 0.0
        mod_mask = DEFAULT_C3_MOD_SIEVE.filter_numpy(A_m, N_m)
        scan_profile.n_pairs_after_c3_mod_sieve = int(np.count_nonzero(mod_mask))
        if collect_profile:
            scan_profile.time_mod_sieve_c3_s = time.perf_counter() - mod_started
        if not np.any(mod_mask):
            if bucket_stats is not None:
                for j, (s2, t2, _) in enumerate(triples):
                    bucket_ids = build_bucket_identities(s1, t1, s2, t2, int(cg[j]))
                    bucket_stats.note_total(bucket_ids)
                    if bool(mask[j]):
                        bucket_stats.note_after_basic(bucket_ids)
            return solutions, near_misses, scan_profile, bucket_stats
        j_idx = j_idx[mod_mask]
        A_m = A_m[mod_mask]
        B_m = B_m[mod_mask]
        N_m = N_m[mod_mask]
        b_m = b_m[mod_mask]
    else:
        scan_profile.n_pairs_after_c3_mod_sieve = len(A_m)

    c3_started = time.perf_counter() if collect_profile else 0.0
    sq3 = A_m * A_m + N_m * N_m
    h3f = np.round(np.sqrt(sq3.astype(np.float64))).astype(np.int64)
    c3e = h3f * h3f == sq3
    c3p1 = (h3f + 1) * (h3f + 1) == sq3
    c3m1 = (h3f - 1) * (h3f - 1) == sq3
    c3 = c3e | c3p1 | c3m1
    h3c = np.where(c3e, h3f, np.where(c3p1, h3f + 1, h3f - 1))
    scan_profile.n_c3_pass = int(np.count_nonzero(c3))
    if collect_profile:
        scan_profile.time_c3_s = time.perf_counter() - c3_started

    if not np.any(c3):
        if bucket_stats is not None:
            for j, (s2, t2, _) in enumerate(triples):
                bucket_ids = build_bucket_identities(s1, t1, s2, t2, int(cg[j]))
                bucket_stats.note_total(bucket_ids)
                if bool(mask[j]):
                    bucket_stats.note_after_basic(bucket_ids)
        return solutions, near_misses, scan_profile, bucket_stats

    j_c3 = j_idx[c3]
    A3 = A_m[c3]
    B3 = B_m[c3]
    N3 = N_m[c3]
    b3 = b_m[c3]
    h3v = h3c[c3]
    sq3_c = sq3[c3]

    c4_started = time.perf_counter() if collect_profile else 0.0
    sq4 = N3 * N3 + B3 * B3
    h4f = np.round(np.sqrt(sq4.astype(np.float64))).astype(np.int64)
    c4e = h4f * h4f == sq4
    c4p1 = (h4f + 1) * (h4f + 1) == sq4
    c4m1 = (h4f - 1) * (h4f - 1) == sq4
    c4 = c4e | c4p1 | c4m1
    h4c = np.where(c4e, h4f, np.where(c4p1, h4f + 1, h4f - 1))
    scan_profile.n_c4_pass = int(np.count_nonzero(c4))

    nm_mask = ~c4
    if np.any(nm_mask):
        for ki in np.where(nm_mask)[0]:
            near_misses.append(
                (
                    int(B3[ki]),
                    int(b3[ki]),
                    int(A3[ki]),
                    int(N3[ki]),
                    True,
                    False,
                    int(sq3_c[ki]),
                    int(sq4[ki]),
                    int(h3v[ki]),
                    int(h4c[ki]),
                )
            )
    scan_profile.n_near_miss = len(near_misses)
    if collect_profile:
        scan_profile.time_c4_s = time.perf_counter() - c4_started

    if not np.any(c4):
        if bucket_stats is not None:
            c3_pass_full = np.zeros(len(triples), dtype=bool)
            c3_pass_full[j_c3] = True
            near_miss_payloads = {
                int(j_c3[idx]): (
                    int(B3[idx]),
                    int(b3[idx]),
                    int(A3[idx]),
                    int(N3[idx]),
                    int(sq3_c[idx]),
                    int(sq4[idx]),
                    int(h3v[idx]),
                    int(h4c[idx]),
                )
                for idx in np.where(nm_mask)[0]
            }
            for j, (s2, t2, _) in enumerate(triples):
                bucket_ids = build_bucket_identities(s1, t1, s2, t2, int(cg[j]))
                bucket_stats.note_total(bucket_ids)
                if not bool(mask[j]):
                    continue
                bucket_stats.note_after_basic(bucket_ids)
                if not bool(c3_pass_full[j]):
                    continue
                bucket_stats.note_c3_pass(bucket_ids)
                payload = near_miss_payloads.get(j)
                if payload is not None:
                    bucket_stats.note_near_miss(
                        bucket_ids,
                        a=payload[0],
                        b=payload[1],
                        c=payload[2],
                        d=payload[3],
                        sq3=payload[4],
                        sq4=payload[5],
                        h3=payload[6],
                        h4=payload[7],
                    )
        return solutions, near_misses, scan_profile, bucket_stats

    j_c34 = j_c3[c4]
    A_hit = A3[c4]
    B_hit = B3[c4]
    N_hit = N3[c4]
    b_hit = b3[c4]

    for ki in range(len(A_hit)):
        a_v = int(B_hit[ki])
        b_v = int(b_hit[ki])
        c_v = int(A_hit[ki])
        d_v = int(N_hit[ki])

        sq3_e = c_v * c_v + d_v * d_v
        h3_e = isqrt(sq3_e)
        if h3_e * h3_e != sq3_e:
            continue
        sq4_e = d_v * d_v + a_v * a_v
        h4_e = isqrt(sq4_e)
        if h4_e * h4_e != sq4_e:
            continue

        j = int(j_c34[ki])
        s2j, _, h2j = triples[j]
        cgj = gcd(t1, s2j)
        x1 = (s2j // cgj) * h1
        x2 = (t1 // cgj) * h2j
        _append_solution_if_valid(solutions, a_v, b_v, c_v, d_v, x1, x2, h3_e, h4_e)

    scan_profile.n_solutions_before_dedup = len(solutions)
    if bucket_stats is not None:
        c3_pass_full = np.zeros(len(triples), dtype=bool)
        c4_pass_full = np.zeros(len(triples), dtype=bool)
        c3_pass_full[j_c3] = True
        c4_pass_full[j_c34] = True
        near_miss_payloads = {
            int(j_c3[idx]): (
                int(B3[idx]),
                int(b3[idx]),
                int(A3[idx]),
                int(N3[idx]),
                int(sq3_c[idx]),
                int(sq4[idx]),
                int(h3v[idx]),
                int(h4c[idx]),
            )
            for idx in np.where(nm_mask)[0]
        }
        for j, (s2, t2, _) in enumerate(triples):
            bucket_ids = build_bucket_identities(s1, t1, s2, t2, int(cg[j]))
            bucket_stats.note_total(bucket_ids)
            if not bool(mask[j]):
                continue
            bucket_stats.note_after_basic(bucket_ids)
            if not bool(c3_pass_full[j]):
                continue
            bucket_stats.note_c3_pass(bucket_ids)
            if bool(c4_pass_full[j]):
                bucket_stats.note_c4_pass(bucket_ids)
                continue
            payload = near_miss_payloads.get(j)
            if payload is not None:
                bucket_stats.note_near_miss(
                    bucket_ids,
                    a=payload[0],
                    b=payload[1],
                    c=payload[2],
                    d=payload[3],
                    sq3=payload[4],
                    sq4=payload[5],
                    h3=payload[6],
                    h4=payload[7],
                )
    return solutions, near_misses, scan_profile, bucket_stats


def _python_scan_t1(
    i: int,
    triples: list[tuple[int, int, int]],
    collect_profile: bool = False,
    safe_pair_sieve_enabled: bool = False,
    mod_sieve_enabled: bool = False,
    collect_bucket_stats: bool = False,
) -> tuple[list[ChainResult], list[NearMissRecord], ScanProfile, BucketStatsCollector | None]:
    """Pure-Python inner T2 loop for one outer T1 iteration."""
    solutions: list[ChainResult] = []
    near_misses: list[NearMissRecord] = []
    scan_profile = ScanProfile(n_pairs_total=len(triples))
    s1, t1, h1 = triples[i]
    n = len(triples)
    bucket_stats = BucketStatsCollector() if collect_bucket_stats else None

    for j in range(n):
        s2, t2, h2 = triples[j]
        bucket_ids = None
        if bucket_stats is not None:
            bucket_ids = build_bucket_identities(s1, t1, s2, t2)
            bucket_stats.note_total(bucket_ids)

        decision = None
        if safe_pair_sieve_enabled:
            sieve_started = time.perf_counter() if collect_profile else 0.0
            decision = decide_safe_pair_sieve(s1, t1, s2, t2)
            if collect_profile:
                scan_profile.time_safe_pair_sieve_s += time.perf_counter() - sieve_started
            if not decision.allow_pair:
                continue

        filter_started = time.perf_counter() if collect_profile else 0.0
        if not safe_pair_sieve_enabled:
            scan_profile.n_pairs_after_safe_pair_sieve += 1
        cg = gcd(t1, s2)
        s2r = s2 // cg
        t1r = t1 // cg

        A = t1r * t2
        B = s1 * s2r
        N = s2r * (s1 - t1) + A

        if safe_pair_sieve_enabled:
            sieve_started = time.perf_counter() if collect_profile else 0.0
            passes_safe_sieve = passes_n_mod4_requirement(decision, N)
            if collect_profile:
                scan_profile.time_safe_pair_sieve_s += time.perf_counter() - sieve_started
            if not passes_safe_sieve:
                if collect_profile:
                    scan_profile.time_filter_s += time.perf_counter() - filter_started
                continue
            scan_profile.n_pairs_after_safe_pair_sieve += 1

        if N <= 0:
            if collect_profile:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue
        if A % 2 != B % 2:
            if collect_profile:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue
        if A % 2 == 0 and (A % 4 != 0 or B % 4 != 0):
            if collect_profile:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue

        b = s2r * t1
        a, c, d = B, A, N

        if A % 2 == 1 and (b % 4 != 0 or N % 4 != 0):
            if collect_profile:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue
        if len({a, b, c, d}) < 4:
            if collect_profile:
                scan_profile.time_filter_s += time.perf_counter() - filter_started
            continue
        scan_profile.n_pairs_after_basic_filters += 1
        if bucket_ids is not None:
            bucket_stats.note_after_basic(bucket_ids)
        if collect_profile:
            scan_profile.time_filter_s += time.perf_counter() - filter_started

        if mod_sieve_enabled:
            mod_started = time.perf_counter() if collect_profile else 0.0
            if not DEFAULT_C3_MOD_SIEVE.allow_pair(A, N):
                if collect_profile:
                    scan_profile.time_mod_sieve_c3_s += time.perf_counter() - mod_started
                continue
            scan_profile.n_pairs_after_c3_mod_sieve += 1
            if collect_profile:
                scan_profile.time_mod_sieve_c3_s += time.perf_counter() - mod_started
        else:
            scan_profile.n_pairs_after_c3_mod_sieve += 1

        c3_started = time.perf_counter() if collect_profile else 0.0
        sq3 = A * A + N * N
        h3 = isqrt(sq3)
        if collect_profile:
            scan_profile.time_c3_s += time.perf_counter() - c3_started
        if h3 * h3 != sq3:
            continue
        scan_profile.n_c3_pass += 1
        if bucket_ids is not None:
            bucket_stats.note_c3_pass(bucket_ids)

        c4_started = time.perf_counter() if collect_profile else 0.0
        sq4 = N * N + B * B
        h4 = isqrt(sq4)
        if collect_profile:
            scan_profile.time_c4_s += time.perf_counter() - c4_started
        if h4 * h4 != sq4:
            near_misses.append((a, b, c, d, True, False, sq3, sq4, h3, h4))
            if bucket_ids is not None:
                bucket_stats.note_near_miss(
                    bucket_ids,
                    a=a,
                    b=b,
                    c=c,
                    d=d,
                    sq3=sq3,
                    sq4=sq4,
                    h3=h3,
                    h4=h4,
                )
            continue
        scan_profile.n_c4_pass += 1
        if bucket_ids is not None:
            bucket_stats.note_c4_pass(bucket_ids)

        x1 = s2r * h1
        x2 = t1r * h2
        _append_solution_if_valid(solutions, a, b, c, d, x1, x2, h3, h4)

    scan_profile.n_solutions_before_dedup = len(solutions)
    scan_profile.n_near_miss = len(near_misses)
    return solutions, near_misses, scan_profile, bucket_stats
