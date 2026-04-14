"""Seed-finding helpers for EC search."""

from __future__ import annotations

from fractions import Fraction
from math import gcd, isqrt

import numpy as np


def _build_coprime_arrays(max_k_num: int, max_k_den: int) -> tuple[np.ndarray, np.ndarray]:
    """Return int64 arrays (a_arr, b_arr) of all coprime pairs a<=max_k_num, b<=max_k_den."""
    pairs = [
        (a, b) for b in range(1, max_k_den + 1) for a in range(1, max_k_num + 1) if gcd(a, b) == 1
    ]
    if not pairs:
        return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.int64)
    a_arr = np.array([a for a, b in pairs], dtype=np.int64)
    b_arr = np.array([b for a, b in pairs], dtype=np.int64)
    return a_arr, b_arr


def _isqrt_arr(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized perfect-square check. Returns (ok, s) where s = isqrt(t)."""
    s = np.floor(np.sqrt(t.astype(np.float64))).astype(np.int64)
    ok = s * s == t
    s1 = s + 1
    fix = ~ok & (s1 * s1 == t)
    ok |= fix
    s[fix] = s1[fix]
    return ok, s


def _find_seeds_numpy(
    p: int,
    q: int,
    r: int,
    a_arr: np.ndarray,
    b_arr: np.ndarray,
    inside_only: bool = False,
) -> list[tuple[int, int, int, int]]:
    """Vectorized seed finder (numpy)."""
    mask = ~((a_arr * p == b_arr * r) | (a_arr * q == b_arr * r))
    if inside_only:
        mask &= (a_arr * p < b_arr * r) & (a_arr * q < b_arr * r)
    a = a_arr[mask]
    b = b_arr[mask]
    if len(a) == 0:
        return []

    ar = a * r
    bp = b * p
    bq = b * q

    tB = (ar - bp) ** 2 + bq**2
    okB, sB = _isqrt_arr(tB)
    if not okB.any():
        return []

    a2, b2, sB2 = a[okB], b[okB], sB[okB]
    tD = (a2 * r - b2 * q) ** 2 + (b2 * p) ** 2
    okD, sD = _isqrt_arr(tD)

    results: list[tuple[int, int, int, int]] = []
    for index in okD.nonzero()[0]:
        results.append((int(a2[index]), int(b2[index]), int(sB2[index]), int(sD[index])))
    return results


def _find_seeds_gpu(
    xp,
    p: int,
    q: int,
    r: int,
    a_dev,
    b_dev,
    inside_only: bool = False,
) -> list[tuple[int, int, int, int]]:
    """Vectorized seed finder for GPU (cupy / torch wrapper)."""
    from rational_distance.backend import _xp_cast

    mask = ~((a_dev * p == b_dev * r) | (a_dev * q == b_dev * r))
    if inside_only:
        mask = mask & (a_dev * p < b_dev * r) & (a_dev * q < b_dev * r)
    a = a_dev[mask]
    b = b_dev[mask]
    if len(a) == 0:
        return []

    ar = a * r
    bp = b * p
    bq = b * q

    tB = (ar - bp) ** 2 + bq**2
    tD = (ar - bq) ** 2 + bp**2

    sB_f = _xp_cast(xp.floor(xp.sqrt(_xp_cast(tB, xp.float64))), xp.int64)
    sD_f = _xp_cast(xp.floor(xp.sqrt(_xp_cast(tD, xp.float64))), xp.int64)
    okB = (sB_f * sB_f == tB) | ((sB_f + 1) * (sB_f + 1) == tB)
    okD = (sD_f * sD_f == tD) | ((sD_f + 1) * (sD_f + 1) == tD)

    mask2 = okB & okD
    if not xp.any(mask2):
        return []

    idx = xp.where(mask2)[0]

    def _to_cpu(arr):
        sliced = arr[idx]
        if hasattr(sliced, "get"):
            return sliced.get()
        if hasattr(sliced, "cpu"):
            return sliced.cpu().numpy()
        return np.asarray(sliced)

    a_hit = _to_cpu(a)
    b_hit = _to_cpu(b)

    results: list[tuple[int, int, int, int]] = []
    for index in range(len(a_hit)):
        a_i, b_i = int(a_hit[index]), int(b_hit[index])
        tB_i = (a_i * r - b_i * p) ** 2 + (b_i * q) ** 2
        sB_i = isqrt(tB_i)
        if sB_i * sB_i != tB_i:
            sB_i += 1
            if sB_i * sB_i != tB_i:
                continue
        tD_i = (a_i * r - b_i * q) ** 2 + (b_i * p) ** 2
        sD_i = isqrt(tD_i)
        if sD_i * sD_i != tD_i:
            sD_i += 1
            if sD_i * sD_i != tD_i:
                continue
        results.append((a_i, b_i, sB_i, sD_i))
    return results


_INT64_SAFE_HALF: int = (1 << 31) - 1


def _seeds_raw_to_fractions(
    raw: list[tuple[int, int, int, int]], r: int
) -> list[tuple[Fraction, Fraction, Fraction]]:
    """Convert (a, b, sB, sD) integer tuples to (k, dB, dD) Fraction triples."""
    seeds = []
    for a, b, sB, sD in raw:
        br = b * r
        seeds.append((Fraction(a, b), Fraction(sB, br), Fraction(sD, br)))
    return seeds


def find_seeds_for_triple(
    p: int,
    q: int,
    r: int,
    max_k_num: int,
    max_k_den: int,
    inside_only: bool = False,
    _a_arr: np.ndarray | None = None,
    _b_arr: np.ndarray | None = None,
) -> list[tuple[Fraction, Fraction, Fraction]]:
    """Find all rational k = a/b such that dB and dD are both rational."""
    coeff = max_k_num + max_k_den
    safe_r_max = _INT64_SAFE_HALF // coeff if coeff > 0 else 10**18

    if r <= safe_r_max:
        if _a_arr is None:
            _a_arr, _b_arr = _build_coprime_arrays(max_k_num, max_k_den)
        raw = _find_seeds_numpy(p, q, r, _a_arr, _b_arr, inside_only)
        return _seeds_raw_to_fractions(raw, r)

    seeds: list[tuple[Fraction, Fraction, Fraction]] = []
    for b in range(1, max_k_den + 1):
        for a in range(1, max_k_num + 1):
            if gcd(a, b) != 1:
                continue
            if a * p == b * r or a * q == b * r:
                continue
            if inside_only and (a * p > b * r or a * q > b * r):
                continue
            ar, bp, bq, br = a * r, b * p, b * q, b * r
            tB = (ar - bp) ** 2 + bq * bq
            sB = isqrt(tB)
            if sB * sB != tB:
                s1 = sB + 1
                if s1 * s1 != tB:
                    continue
                sB = s1
            tD = (ar - bq) ** 2 + bp * bp
            sD = isqrt(tD)
            if sD * sD != tD:
                s1 = sD + 1
                if s1 * s1 != tD:
                    continue
                sD = s1
            seeds.append((Fraction(a, b), Fraction(sB, br), Fraction(sD, br)))
    return seeds


__all__ = [
    "_INT64_SAFE_HALF",
    "_build_coprime_arrays",
    "_find_seeds_gpu",
    "_find_seeds_numpy",
    "_isqrt_arr",
    "_seeds_raw_to_fractions",
    "find_seeds_for_triple",
]
