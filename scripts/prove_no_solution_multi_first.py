#!/usr/bin/env python3
"""Multi-N-first driver: prove no Harborth counterexample using dual-closure sieve.

Pipeline (all sieves are unconditional 2-adic / mod p² necessary conditions):

    fast_multi_concordant_pairs(max_hyp)
        ↓ generates every reduced coprime (A, B) with k ≥ 2 concordant N
    chain_closure_mod_sieve on (A, B)
        ↓ kills (A, B) with empty T(A,B,M) ∩ ((A+B)−T)
    dual_chain_closure_mod_sieve on every (N_i, N_j) ∈ concordant_N(A, B)
        ↓ kills (A, B) when every reduced (N_i, N_j) is killed by some mod p²
    survivors → deeper analysis (PARI / Heegner / Selmer)

Rationale: Harborth counterexample requires k ≥ 2 (closure pair N_1+N_2=A+B).
So we skip the 30M-pair brute-force enumeration and start directly from the
multi-N candidate set, which is small (854 at max_hyp=10000, ~10k at 100k).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from rational_distance.concordant.chain_closure_sieve import (
    BALANCED_MODULI,
    EXTENDED_MODULI,
    MINIMAL_MODULI,
    STANDARD_MODULI,
    find_killer_modulus,
)
from rational_distance.concordant.dual_closure_sieve import find_surviving_n_pair
from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair
from rational_distance.parallel import parallel_map
from rational_distance.proof_status import multi_first_db

MODULI_PRESETS: dict[str, tuple[int, ...]] = {
    "minimal": MINIMAL_MODULI,
    "balanced": BALANCED_MODULI,
    "standard": STANDARD_MODULI,
    "extended": EXTENDED_MODULI,
}


@dataclass
class PairVerdict:
    A: int
    B: int
    ns: tuple[int, ...]
    primary_killer: int | None
    surviving_n_pair: tuple[int, int] | None
    elapsed_s: float

    @property
    def is_killed(self) -> bool:
        return self.surviving_n_pair is None


@dataclass
class Summary:
    max_hyp: int
    moduli_name: str
    moduli: tuple[int, ...]
    multi_n_pair_count: int
    safe_sieve_killed: int = 0
    primary_killed: int = 0
    dual_killed: int = 0
    survivors: list[PairVerdict] = field(default_factory=list)
    multi_n_elapsed_s: float = 0.0
    sieve_elapsed_s: float = 0.0
    # Populated only when run(collect_pairs=True), for compact SQLite output.
    safe_killed_pairs: list[tuple[int, int, int]] = field(default_factory=list)
    nonsafe_verdicts: list[PairVerdict] = field(default_factory=list)


def _evaluate_pair_with_moduli(
    packed: tuple[int, int, tuple[int, ...], tuple[int, ...]],
) -> PairVerdict:
    """Top-level (picklable) worker: ``(A, B, ns, moduli)`` → ``PairVerdict``."""
    a, b, ns, moduli = packed
    started = time.perf_counter()
    primary = find_killer_modulus(a, b, moduli)
    if primary is not None:
        elapsed = time.perf_counter() - started
        return PairVerdict(
            A=a,
            B=b,
            ns=ns,
            primary_killer=primary,
            surviving_n_pair=None,
            elapsed_s=elapsed,
        )
    survivor = find_surviving_n_pair(list(ns), moduli)
    elapsed = time.perf_counter() - started
    return PairVerdict(
        A=a,
        B=b,
        ns=ns,
        primary_killer=None,
        surviving_n_pair=survivor,
        elapsed_s=elapsed,
    )


def run(
    max_hyp: int,
    moduli_name: str,
    workers: int,
    collect_pairs: bool = False,
) -> Summary:
    moduli = MODULI_PRESETS[moduli_name]

    print(f"[phase] generating multi-N candidates for max_hyp={max_hyp}", flush=True)
    t0 = time.perf_counter()
    multi_n_pairs = fast_multi_concordant_pairs(max_hyp)
    multi_n_elapsed = time.perf_counter() - t0
    print(
        f"[phase] multi-N generation done: "
        f"{len(multi_n_pairs)} pairs in {multi_n_elapsed:.2f}s",
        flush=True,
    )

    items: list[tuple[int, int, tuple[int, ...]]] = []
    safe_killed = 0
    safe_killed_pairs: list[tuple[int, int, int]] = []
    for (a, b), ns in multi_n_pairs.items():
        if not allow_reduced_pair(a, b):
            safe_killed += 1
            if collect_pairs:
                safe_killed_pairs.append((a, b, len(ns)))
            continue
        items.append((a, b, tuple(ns)))

    summary = Summary(
        max_hyp=max_hyp,
        moduli_name=moduli_name,
        moduli=moduli,
        multi_n_pair_count=len(multi_n_pairs),
        safe_sieve_killed=safe_killed,
        multi_n_elapsed_s=multi_n_elapsed,
    )

    print(
        f"[phase] sieve running with workers={workers} moduli={moduli_name} "
        f"({len(moduli)} moduli)",
        flush=True,
    )
    t1 = time.perf_counter()
    if workers <= 1:
        verdicts: list[PairVerdict] = []
        for item in items:
            verdicts.append(
                _evaluate_pair_with_moduli((item[0], item[1], item[2], moduli))
            )
    else:
        # parallel_map with module-level worker init via spawn-safe globals
        verdicts = _run_parallel(items, moduli=moduli, workers=workers)
    summary.sieve_elapsed_s = time.perf_counter() - t1

    for verdict in verdicts:
        if verdict.is_killed:
            if verdict.primary_killer is not None:
                summary.primary_killed += 1
            else:
                summary.dual_killed += 1
        else:
            summary.survivors.append(verdict)

    if collect_pairs:
        summary.safe_killed_pairs = safe_killed_pairs
        summary.nonsafe_verdicts = verdicts

    return summary


def _run_parallel(
    items: list[tuple[int, int, tuple[int, ...]]],
    *,
    moduli: tuple[int, ...],
    workers: int,
) -> list[PairVerdict]:
    """Pack moduli into each item so workers don't rely on global state."""
    packed = [(a, b, ns, moduli) for (a, b, ns) in items]
    return parallel_map(
        _evaluate_pair_with_moduli,
        packed,
        workers=workers,
        chunksize=64,
        ordered=False,
    )


def _summary_to_dict(summary: Summary) -> dict[str, object]:
    return {
        "max_hyp": summary.max_hyp,
        "moduli_name": summary.moduli_name,
        "moduli": list(summary.moduli),
        "multi_n_pair_count": summary.multi_n_pair_count,
        "safe_sieve_killed": summary.safe_sieve_killed,
        "primary_killed": summary.primary_killed,
        "dual_killed": summary.dual_killed,
        "survivor_count": len(summary.survivors),
        "multi_n_elapsed_s": summary.multi_n_elapsed_s,
        "sieve_elapsed_s": summary.sieve_elapsed_s,
        "survivors": [
            {
                "A": v.A,
                "B": v.B,
                "ns": list(v.ns),
                "surviving_n_pair": list(v.surviving_n_pair) if v.surviving_n_pair else None,
            }
            for v in summary.survivors
        ],
    }


def _write_sqlite(summary: Summary, path: Path) -> None:
    """Persist a run + per-pair verdicts to the compact multi-first SQLite DB."""
    pair_rows: list[tuple[int, int, int, int, int | None]] = [
        (a, b, k, multi_first_db.VERDICT_SAFE_SIEVE, None)
        for (a, b, k) in summary.safe_killed_pairs
    ]
    survivor_n_rows: list[tuple[int, int, int]] = []
    for v in summary.nonsafe_verdicts:
        if v.is_killed:
            if v.primary_killer is not None:
                verdict = multi_first_db.VERDICT_CHAIN_CLOSURE
                killer: int | None = v.primary_killer
            else:
                verdict = multi_first_db.VERDICT_DUAL
                killer = None
        else:
            verdict = multi_first_db.VERDICT_SURVIVOR
            killer = None
            survivor_n_rows.extend((v.A, v.B, int(n)) for n in v.ns)
        pair_rows.append((v.A, v.B, len(v.ns), verdict, killer))

    conn = multi_first_db.connect_db(path)
    try:
        multi_first_db.init_schema(conn)
        multi_first_db.write_run(
            conn,
            max_hyp=summary.max_hyp,
            moduli_name=summary.moduli_name,
            moduli=summary.moduli,
            multi_n_pair_count=summary.multi_n_pair_count,
            safe_sieve_killed=summary.safe_sieve_killed,
            primary_killed=summary.primary_killed,
            dual_killed=summary.dual_killed,
            survivor_count=len(summary.survivors),
            multi_n_elapsed_s=summary.multi_n_elapsed_s,
            sieve_elapsed_s=summary.sieve_elapsed_s,
            pair_rows=pair_rows,
            survivor_n_rows=survivor_n_rows,
        )
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Multi-N-first Harborth no-solution prover using dual-closure sieve."
        )
    )
    parser.add_argument("--max-hyp", type=int, required=True)
    parser.add_argument(
        "--moduli",
        choices=tuple(MODULI_PRESETS),
        default="standard",
    )
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Write summary JSON here (includes survivors).",
    )
    parser.add_argument(
        "--sqlite-out",
        type=Path,
        default=None,
        help=(
            "Write a compact SQLite DB here (run_meta + per-pair verdict enum + "
            "survivor N lists). Much smaller than the legacy proof_status DB."
        ),
    )
    args = parser.parse_args()

    summary = run(
        args.max_hyp,
        args.moduli,
        args.workers,
        collect_pairs=args.sqlite_out is not None,
    )

    print("=" * 72)
    print(f"max_hyp:            {summary.max_hyp}")
    print(f"moduli:             {summary.moduli_name} ({len(summary.moduli)} moduli)")
    print(f"multi-N pairs:      {summary.multi_n_pair_count}")
    print(f"safe_sieve killed (mixed parity / mod 4): {summary.safe_sieve_killed}")
    print(
        f"primary killed (chain_closure on AB): {summary.primary_killed}"
    )
    print(
        f"dual killed    (chain_closure on N pairs): {summary.dual_killed}"
    )
    print(f"survivors:          {len(summary.survivors)}")
    print(
        f"multi-N gen elapsed: {summary.multi_n_elapsed_s:.2f}s; "
        f"sieve elapsed: {summary.sieve_elapsed_s:.2f}s"
    )
    if summary.survivors:
        print("survivor pairs (first 16):")
        for verdict in summary.survivors[:16]:
            print(
                f"  ({verdict.A}, {verdict.B}) ns={list(verdict.ns)} "
                f"surviving_n_pair={verdict.surviving_n_pair}"
            )

    if args.sqlite_out is not None:
        _write_sqlite(summary, args.sqlite_out)
        print(f"sqlite summary written to {args.sqlite_out}")

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(_summary_to_dict(summary), indent=2, sort_keys=True) + "\n"
        )
        print(f"summary written to {args.json_out}")


if __name__ == "__main__":
    main()
