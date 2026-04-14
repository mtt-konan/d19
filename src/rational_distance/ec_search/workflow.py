"""Main EC search workflow."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

import numpy as np

from rational_distance.math_utils import primitive_pythagorean_triples
from rational_distance.square import RationalPoint, canonical_xy, make_point

from .curve import QuarticEC
from .models import ECCandidateRecord, ECSeedBranch, ECSeedRecord, ECTripleTrace
from .seeds import (
    _INT64_SAFE_HALF,
    _build_coprime_arrays,
    _find_seeds_gpu,
    _seeds_raw_to_fractions,
    find_seeds_for_triple,
)


def _make_ec_point(p: int, q: int, r: int, k: Fraction, inside_only: bool) -> RationalPoint | None:
    """Construct a RationalPoint from triple (p, q, r) and scale k."""
    x = k * Fraction(p, r)
    y = k * Fraction(q, r)

    if x == 0 or y == 0:
        return None
    if x == 1 or y == 1:
        return None
    if inside_only and (x >= 1 or y >= 1):
        return None

    return make_point(x, y)


def _point_xy_from_k(p: int, q: int, r: int, k: Fraction) -> tuple[Fraction, Fraction]:
    return k * Fraction(p, r), k * Fraction(q, r)


def _evaluate_candidate(
    p: int,
    q: int,
    r: int,
    k: Fraction | None,
    inside_only: bool,
    min_rational: int,
) -> tuple[
    str,
    Fraction | None,
    Fraction | None,
    RationalPoint | None,
    tuple[Fraction, Fraction] | None,
]:
    if k is None:
        return "infinite_k", None, None, None, None
    if k <= 0:
        return "non_positive_k", None, None, None, None

    x, y = _point_xy_from_k(p, q, r, k)
    if x == 0 or y == 0 or x == 1 or y == 1:
        return "side_filtered", x, y, None, None
    if inside_only and (x >= 1 or y >= 1):
        return "inside_filtered", x, y, None, None

    point = make_point(x, y)
    canonical = canonical_xy(point.x, point.y)
    if point.rational_count < min_rational:
        return "insufficient_rational", x, y, point, canonical
    return "candidate_ok", x, y, point, canonical


def _build_triple_trace(
    p: int,
    q: int,
    r: int,
    seeds_raw: list[tuple[Fraction, Fraction, Fraction]],
    max_steps: int,
    min_rational: int,
    inside_only: bool,
    seen_canonical: set[tuple[Fraction, Fraction]],
) -> ECTripleTrace:
    seed_records = [
        ECSeedRecord(
            seed_index=index,
            a=seed_k.numerator,
            b=seed_k.denominator,
            k=seed_k,
            dB=dB,
            dD=dD,
        )
        for index, (seed_k, dB, dD) in enumerate(seeds_raw)
    ]

    ec = QuarticEC(p, q, r)
    seed_branches: list[ECSeedBranch] = []
    for seed in seed_records:
        for t in ec.t_from_k_dB(seed.k, seed.dB):
            E = ec.E_from_t_dD(t, seed.dD)
            if ec.on_curve(t, E):
                seed_branches.append(ECSeedBranch(seed.seed_index, t, E))
                if E != 0:
                    seed_branches.append(ECSeedBranch(seed.seed_index, t, -E))

    if not seed_branches:
        return ECTripleTrace(p=p, q=q, r=r, seeds=seed_records, nodes=[], edges=[], candidates=[])

    orbit_trace = ec.expand_orbit_trace(seed_branches, max_steps=max_steps)

    seen_k: set[Fraction | None] = set()
    candidates: list[ECCandidateRecord] = []

    def add_candidate(
        source_kind: str,
        source_seed_index: int | None,
        source_node_index: int | None,
        k_value: Fraction | None,
    ) -> None:
        base_status, x, y, point, canonical = _evaluate_candidate(
            p, q, r, k_value, inside_only, min_rational
        )
        status = base_status
        if k_value in seen_k:
            status = "k_duplicate"
        else:
            seen_k.add(k_value)
            if base_status == "candidate_ok" and canonical is not None:
                if canonical in seen_canonical:
                    status = "d4_duplicate"
                else:
                    status = "accepted"
                    seen_canonical.add(canonical)

        candidates.append(
            ECCandidateRecord(
                candidate_index=len(candidates),
                source_kind=source_kind,
                source_seed_index=source_seed_index,
                source_node_index=source_node_index,
                k=k_value,
                status=status,
                x=x,
                y=y,
                point=point,
                canonical_xy=canonical,
            )
        )

    for seed in seed_records:
        add_candidate(
            source_kind="seed",
            source_seed_index=seed.seed_index,
            source_node_index=orbit_trace.seed_primary_nodes.get(seed.seed_index),
            k_value=seed.k,
        )

    for node_index in orbit_trace.active_node_indices:
        node = orbit_trace.nodes[node_index]
        add_candidate(
            source_kind="orbit",
            source_seed_index=None,
            source_node_index=node.node_index,
            k_value=ec.k_from_t(node.t),
        )

    return ECTripleTrace(
        p=p,
        q=q,
        r=r,
        seeds=seed_records,
        nodes=orbit_trace.nodes,
        edges=orbit_trace.edges,
        candidates=candidates,
    )


def ec_search(
    max_m: int = 30,
    max_k_num: int = 200,
    max_k_den: int = 100,
    max_steps: int = 20,
    min_rational: int = 3,
    inside_only: bool = False,
    progress: bool = True,
    xp=None,
    store: Any | None = None,
) -> list[RationalPoint]:
    """Search for rational-distance points using the elliptic-curve method."""
    try:
        from tqdm import tqdm

        _tqdm = tqdm
    except ImportError:

        def _tqdm(it, **kw):
            return it

    triples = primitive_pythagorean_triples(max_m)

    _use_gpu = xp is not None and xp is not np
    a_cpu, b_cpu = _build_coprime_arrays(max_k_num, max_k_den)
    if _use_gpu:
        a_dev = xp.array(a_cpu.tolist(), dtype=xp.int64)
        b_dev = xp.array(b_cpu.tolist(), dtype=xp.int64)
    else:
        a_dev = b_dev = None

    coeff = max_k_num + max_k_den
    safe_r_max = _INT64_SAFE_HALF // coeff if coeff > 0 else 10**18

    results = store.existing_points() if store is not None else []
    seen_canonical: set[tuple[Fraction, Fraction]] = {
        canonical_xy(point.x, point.y) for point in results
    }

    iterator = _tqdm(triples, desc="EC search", unit="triple", disable=not progress)
    for triple_index, (p, q, r) in enumerate(iterator):
        if store is not None and (p, q, r) in store.processed_triples:
            continue

        if _use_gpu and r <= safe_r_max:
            raw = _find_seeds_gpu(xp, p, q, r, a_dev, b_dev, inside_only)
            seeds_raw = _seeds_raw_to_fractions(raw, r)
        else:
            seeds_raw = find_seeds_for_triple(
                p,
                q,
                r,
                max_k_num,
                max_k_den,
                inside_only,
                _a_arr=a_cpu,
                _b_arr=b_cpu,
            )

        if not seeds_raw:
            if store is not None:
                store.record_triple(
                    triple_index,
                    ECTripleTrace(p=p, q=q, r=r, seeds=[], nodes=[], edges=[], candidates=[]),
                )
            continue

        if store is not None:
            trace = _build_triple_trace(
                p=p,
                q=q,
                r=r,
                seeds_raw=seeds_raw,
                max_steps=max_steps,
                min_rational=min_rational,
                inside_only=inside_only,
                seen_canonical=seen_canonical,
            )
            store.record_triple(triple_index, trace)
            results.extend(trace.accepted_points())
            continue

        ec = QuarticEC(p, q, r)

        curve_seeds: list[tuple[Fraction, Fraction]] = []
        for k_value, dB, dD in seeds_raw:
            for t in ec.t_from_k_dB(k_value, dB):
                E = ec.E_from_t_dD(t, dD)
                if ec.on_curve(t, E):
                    curve_seeds.append((t, E))
                    if E != 0:
                        curve_seeds.append((t, -E))

        if not curve_seeds:
            continue

        k_values_from_orbit = ec.expand_orbit(curve_seeds, max_steps=max_steps)
        seed_k_values = [k_value for k_value, _, _ in seeds_raw]
        all_k_values = list(dict.fromkeys(seed_k_values + k_values_from_orbit))

        for k_value in all_k_values:
            point = _make_ec_point(p, q, r, k_value, inside_only)
            if point is None:
                continue
            if point.rational_count < min_rational:
                continue

            cx, cy = canonical_xy(point.x, point.y)
            if (cx, cy) in seen_canonical:
                continue
            seen_canonical.add((cx, cy))
            results.append(point)

    results.sort(key=lambda point: point.denominator)
    return results


__all__ = [
    "_build_triple_trace",
    "_evaluate_candidate",
    "_make_ec_point",
    "_point_xy_from_k",
    "ec_search",
]
