"""CLI run orchestration for the search entrypoint."""

from __future__ import annotations

import argparse
import json
import time

from .chain_fast_runner import _run_chain_fast
from .chain_runner import _run_chain
from .ec_runner import _run_ec
from .output import _print_concordant_profile
from .parametric_runner import _resolve_parametric_limits, _run_parametric


def _run_concordant_factor(
    args: argparse.Namespace,
    *,
    safe_pair_sieve_enabled: bool = False,
) -> None:
    """Run concordant analysis using the pure-Python factor-decomposition method."""
    from rational_distance.concordant import (
        check_chain_compatibility,
        generate_ab_pairs,
    )
    from rational_distance.concordant.factor_search import find_concordant_by_factorization
    from rational_distance.concordant.safe_pair_sieve import classify_reduced_pair

    if args.pair:
        if safe_pair_sieve_enabled:
            raise SystemExit(
                "--safe-pair-sieve currently supports only batch concordant runs, not --pair."
            )
        parts = args.pair.split(",")
        if len(parts) != 2:
            print("Error: --pair must be A,B (e.g. --pair 264,420)")
            return
        pair_a, pair_b = int(parts[0].strip()), int(parts[1].strip())
        print(f"  pair=({pair_a}, {pair_b})  method=factor")
        print("=" * 72)
        t0 = time.perf_counter()
        concordant_n = find_concordant_by_factorization(pair_a, pair_b)
        chain_compatible = [n for n in concordant_n if check_chain_compatibility(pair_a, pair_b, n)]
        elapsed = time.perf_counter() - t0
        print(f"\n(A={pair_a}, B={pair_b}): concordant_n={concordant_n}")
        print(f"  chain_compatible={chain_compatible}")
        if concordant_n:
            print("\nChain compatibility diagnostics")
            for n in concordant_n:
                b = pair_a + pair_b - n
                chain_ok = check_chain_compatibility(pair_a, pair_b, n)
                print(
                    f"  N={n}  b={b}  b_positive={b > 0}  "
                    f"chain_ok={chain_ok}"
                )
        print(f"\nCompleted in {elapsed:.3f}s")
        if chain_compatible:
            print("\n*** CHAIN SOLUTION FOUND! ***")

    else:
        print(f"  max_hyp={args.max_hyp}  method=factor")
        print("=" * 72)
        t0 = time.perf_counter()
        pairs = generate_ab_pairs(args.max_hyp)
        print(f"Generated {len(pairs)} primitive (A,B) pairs")

        pairs_to_analyze = pairs
        if safe_pair_sieve_enabled:
            filtered_pairs: list[tuple[int, int]] = []
            for ab_a, ab_b in pairs:
                classification = classify_reduced_pair(ab_a, ab_b)
                if classification == "pass":
                    filtered_pairs.append((ab_a, ab_b))
            pairs_to_analyze = filtered_pairs
            print(f"Safe pair sieve: kept {len(pairs_to_analyze)}/{len(pairs)} pairs")

        iterator = enumerate(pairs_to_analyze)
        if not args.no_progress:
            from tqdm import tqdm
            iterator = tqdm(list(iterator), desc="Factor search", leave=False)

        n_with_concordant = 0
        n_with_chain = 0
        results_summary: list[tuple[int, int, list[int], list[int]]] = []

        for _idx, (ab_a, ab_b) in iterator:
            concordant_n = find_concordant_by_factorization(ab_a, ab_b)
            chain_compatible = [
                n for n in concordant_n if check_chain_compatibility(ab_a, ab_b, n)
            ]
            if concordant_n:
                n_with_concordant += 1
                results_summary.append((ab_a, ab_b, concordant_n, chain_compatible))
            if chain_compatible:
                n_with_chain += 1
                print(f"\n*** CHAIN SOLUTION: (A={ab_a}, B={ab_b}) concordant_n={concordant_n} ***")

        elapsed = time.perf_counter() - t0

        analyzed = len(pairs_to_analyze)
        print(f"\n{'─' * 72}")
        print(f"Analysed {analyzed} pairs in {elapsed:.1f}s")
        print(f"Pairs with concordant N: {n_with_concordant}/{analyzed}")
        print(f"Pairs with chain-compatible N: {n_with_chain}/{analyzed}")

        if n_with_chain > 0:
            print("\n*** HARBORTH SOLUTIONS EXIST! ***")

        top = args.top if args.top > 0 else len(results_summary)
        if results_summary:
            print(f"\nPairs with concordant N (showing up to {top}):")
            for ab_a, ab_b, concordant_n, chain_compatible in results_summary[:top]:
                print(
                    f"  (A={ab_a}, B={ab_b}): "
                    f"concordant_n={concordant_n}  chain_compatible={chain_compatible or 'none'}"
                )

        if args.out:
            report = {
                "method": "factor",
                "max_hyp": args.max_hyp,
                "n_pairs": len(pairs),
                "n_pairs_analyzed": analyzed,
                "safe_pair_sieve_enabled": safe_pair_sieve_enabled,
                "elapsed_s": round(elapsed, 2),
                "n_with_concordant": n_with_concordant,
                "n_with_chain_compatible": n_with_chain,
                "pairs": [
                    {
                        "A": ab_a,
                        "B": ab_b,
                        "concordant_n": concordant_n,
                        "chain_compatible": chain_compatible,
                    }
                    for ab_a, ab_b, concordant_n, chain_compatible in results_summary
                ],
            }
            with open(args.out, "w") as handle:
                json.dump(report, handle, indent=2)
            print(f"\nReport saved to {args.out}")


def _run_concordant(args: argparse.Namespace) -> None:
    from rational_distance.concordant import (
        ConcordantProfile,
        diagnose_pair,
        generate_ab_pairs,
    )
    from rational_distance.concordant.safe_pair_sieve import classify_reduced_pair

    include_rank = False
    safe_pair_sieve_enabled = bool(getattr(args, "safe_pair_sieve", False))

    def _candidate_payload(candidate) -> dict[str, object]:
        return {
            "n": candidate.n,
            "source": candidate.source,
            "b": candidate.b,
            "b_positive": candidate.b_positive,
            "b_in_concordant_set": candidate.b_in_concordant_set,
            "b_source": candidate.b_source,
            "c1_ok": candidate.c1_ok,
            "c2_ok": candidate.c2_ok,
            "side_hit": candidate.side_hit,
            "chain_ok": candidate.chain_ok,
            "c1_nearest_square_delta": candidate.c1_nearest_square_delta,
            "c2_nearest_square_delta": candidate.c2_nearest_square_delta,
            "combined_delta": candidate.combined_delta,
        }

    def _pair_report(diagnostics, *, deep: int) -> dict[str, object]:
        result = diagnostics.result
        return {
            "mode": "pair",
            "A": result.A,
            "B": result.B,
            "ec_bound": result.ec_bound,
            "deep": deep,
            "rank": result.rank,
            "rank_bounds": list(result.rank_bounds) if result.rank_bounds is not None else None,
            "generators": [list(generator) for generator in result.generators],
            "raw_square_x": result.raw_square_x,
            "concordant_n": result.concordant_n,
            "deep_extra_n": diagnostics.deep_extra_n,
            "all_concordant_n": diagnostics.all_concordant_n,
            "mirror_hit_n": diagnostics.mirror_hit_n,
            "c1_hit_n": diagnostics.c1_hit_n,
            "c2_hit_n": diagnostics.c2_hit_n,
            "side_hit_n": diagnostics.side_hit_n,
            "chain_compatible": diagnostics.chain_compatible,
            "best_candidate": (
                _candidate_payload(diagnostics.best_candidate)
                if diagnostics.best_candidate is not None
                else None
            ),
            "candidates": [_candidate_payload(candidate) for candidate in diagnostics.candidates],
        }

    def _batch_pair_summary(diagnostics) -> dict[str, object]:
        result = diagnostics.result
        best_candidate = diagnostics.best_candidate
        return {
            "A": result.A,
            "B": result.B,
            "rank": result.rank,
            "rank_bounds": list(result.rank_bounds) if result.rank_bounds is not None else None,
            "concordant_n": result.concordant_n,
            "all_concordant_n": diagnostics.all_concordant_n,
            "chain_compatible": diagnostics.chain_compatible,
            "raw_square_x": result.raw_square_x,
            "mirror_hit_n": diagnostics.mirror_hit_n,
            "mirror_hit_count": len(diagnostics.mirror_hit_n),
            "c1_hit_n": diagnostics.c1_hit_n,
            "c2_hit_n": diagnostics.c2_hit_n,
            "side_hit_n": diagnostics.side_hit_n,
            "best_candidate": (
                _candidate_payload(best_candidate) if best_candidate is not None else None
            ),
            "best_side_hit": best_candidate.side_hit if best_candidate is not None else "none",
            "best_b_positive": best_candidate.b_positive if best_candidate is not None else None,
            "min_combined_delta": (
                best_candidate.combined_delta if best_candidate is not None else None
            ),
            "best_b": best_candidate.b if best_candidate is not None else None,
        }

    def _best_candidate_sort_key(diagnostics) -> tuple[float, float, float, float, int, int]:
        candidate = diagnostics.best_candidate
        if candidate is None:
            return (1.0, 1.0, 1.0, float("inf"), diagnostics.result.A, diagnostics.result.B)
        if candidate.side_hit == "both":
            side_rank = 0.0
        elif candidate.side_hit != "none":
            side_rank = 1.0
        else:
            side_rank = 2.0
        return (
            0.0 if candidate.chain_ok else 1.0,
            0.0 if candidate.b_positive else 1.0,
            side_rank,
            float(candidate.combined_delta),
            diagnostics.result.A,
            diagnostics.result.B,
        )

    use_factor = getattr(args, "concordant_method", "ec") == "factor"

    print("=" * 72)
    print(
        "Concordant-form analysis"
        f"  method={'factor-decomposition' if use_factor else 'PARI-ellratpoints'}"
    )
    profile = ConcordantProfile(
        enabled=bool(getattr(args, "profile", False)),
        deep=args.deep,
        rank_enabled=include_rank,
        safe_pair_sieve_enabled=safe_pair_sieve_enabled,
    )
    active_profile = profile if profile.enabled else None

    if use_factor:
        _run_concordant_factor(args, safe_pair_sieve_enabled=safe_pair_sieve_enabled)
        return

    if args.pair:
        if safe_pair_sieve_enabled:
            raise SystemExit(
                "--safe-pair-sieve currently supports only batch concordant runs, not --pair."
            )
        from rational_distance.concordant.analysis import _ensure_pari

        parts = args.pair.split(",")
        if len(parts) != 2:
            print("Error: --pair must be A,B (e.g. --pair 264,420)")
            return
        A, B = int(parts[0].strip()), int(parts[1].strip())
        print(f"  pair=({A}, {B})  ec_bound={args.ec_bound}  deep={args.deep}")
        print("=" * 72)

        t0 = time.perf_counter()
        profile.n_pairs_total = 1
        profile.n_pairs_after_safe_pair_sieve = 1
        profile.n_pairs_rejected_by_safe_pair_sieve = 0
        pari_started = time.perf_counter()
        pari = _ensure_pari()
        profile.time_pari_init_s += time.perf_counter() - pari_started
        diagnostics = diagnose_pair(
            A,
            B,
            ec_bound=args.ec_bound,
            pari=pari,
            deep=args.deep,
            profile=active_profile,
            include_rank=include_rank,
        )
        profile.n_pairs_completed = 1
        if diagnostics.result.has_concordant:
            profile.n_pairs_with_concordant = 1
        if diagnostics.result.has_chain_solution:
            profile.n_pairs_with_chain_compatible = 1
        if diagnostics.mirror_hit_n:
            profile.n_pairs_with_mirror_hit = 1
        if diagnostics.c1_hit_n:
            profile.n_pairs_with_c1_hit = 1
        if diagnostics.c2_hit_n:
            profile.n_pairs_with_c2_hit = 1
        if diagnostics.side_hit_n:
            profile.n_pairs_with_side_hit = 1
        result = diagnostics.result
        print(f"\n{result.summary()}")
        if args.deep > 0:
            print(f"\nDeep search (depth={args.deep})...")
        print("\nChain compatibility diagnostics")
        print(f"  deep_extra_n: {diagnostics.deep_extra_n if diagnostics.deep_extra_n else 'none'}")
        print(f"  all_concordant_n: {diagnostics.all_concordant_n}")
        print(f"  mirror_hit_n: {diagnostics.mirror_hit_n if diagnostics.mirror_hit_n else 'none'}")
        print(f"  c1_hit_n: {diagnostics.c1_hit_n if diagnostics.c1_hit_n else 'none'}")
        print(f"  c2_hit_n: {diagnostics.c2_hit_n if diagnostics.c2_hit_n else 'none'}")
        print(f"  side_hit_n: {diagnostics.side_hit_n if diagnostics.side_hit_n else 'none'}")
        if diagnostics.best_candidate is None:
            print("  best_candidate: none")
        else:
            candidate = diagnostics.best_candidate
            print(
                "  best_candidate: "
                f"N={candidate.n} source={candidate.source} b={candidate.b} "
                f"b_positive={candidate.b_positive} side_hit={candidate.side_hit} "
                f"chain_ok={candidate.chain_ok} combined_delta={candidate.combined_delta}"
            )
        if diagnostics.candidates:
            print("  candidates:")
            for candidate in diagnostics.candidates:
                print(
                    "    "
                    f"N={candidate.n} source={candidate.source} b={candidate.b} "
                    f"b_positive={candidate.b_positive} side_hit={candidate.side_hit} "
                    f"b_in_concordant_set={candidate.b_in_concordant_set} "
                    f"C1={candidate.c1_ok}(delta={candidate.c1_nearest_square_delta}) "
                    f"C2={candidate.c2_ok}(delta={candidate.c2_nearest_square_delta}) "
                    f"combined_delta={candidate.combined_delta}"
                )
        else:
            print("  candidates: none")

        elapsed = time.perf_counter() - t0
        if args.out:
            json_started = time.perf_counter()
            report = _pair_report(diagnostics, deep=args.deep)
            if profile.enabled:
                report["profile"] = profile.as_dict()
            with open(args.out, "w") as handle:
                json.dump(report, handle, indent=2)
            profile.time_json_write_s += time.perf_counter() - json_started
            print(f"\nReport saved to {args.out}")
        if profile.enabled:
            _print_concordant_profile(profile.as_dict())
        print(f"\nCompleted in {elapsed:.1f}s")

    else:
        print(f"  max_hyp={args.max_hyp}  ec_bound={args.ec_bound}  method=ec")
        print("=" * 72)

        t0 = time.perf_counter()
        pair_gen_started = time.perf_counter()
        pairs = generate_ab_pairs(args.max_hyp)
        profile.time_pair_generation_s += time.perf_counter() - pair_gen_started
        profile.n_pairs_total = len(pairs)
        print(f"Generated {len(pairs)} primitive (A,B) pairs")

        pairs_to_analyze = pairs
        if safe_pair_sieve_enabled:
            sieve_started = time.perf_counter()
            filtered_pairs: list[tuple[int, int]] = []
            for A, B in pairs:
                classification = classify_reduced_pair(A, B)
                if classification == "pass":
                    filtered_pairs.append((A, B))
                elif classification == "mixed_parity":
                    profile.n_pairs_rejected_mixed_parity += 1
                elif classification == "odd_odd_wrong_mod4":
                    profile.n_pairs_rejected_mod4 += 1
                else:  # pragma: no cover - defensive guard
                    raise RuntimeError(f"unexpected safe-pair classification: {classification}")
            pairs_to_analyze = filtered_pairs
            profile.time_safe_pair_sieve_s += time.perf_counter() - sieve_started
            profile.n_pairs_after_safe_pair_sieve = len(pairs_to_analyze)
            profile.n_pairs_rejected_by_safe_pair_sieve = len(pairs) - len(pairs_to_analyze)
            print(
                "Safe pair sieve: "
                f"kept {profile.n_pairs_after_safe_pair_sieve}/{profile.n_pairs_total} pairs, "
                f"rejected {profile.n_pairs_rejected_by_safe_pair_sieve} "
                f"(mixed parity {profile.n_pairs_rejected_mixed_parity}, "
                f"odd+odd but A+B mod 4 wrong {profile.n_pairs_rejected_mod4}), "
                f"time {profile.time_safe_pair_sieve_s:.3f}s"
            )
        else:
            profile.n_pairs_after_safe_pair_sieve = len(pairs)
            profile.n_pairs_rejected_by_safe_pair_sieve = 0

        results = []
        rank_counts: dict[int, int] = {}
        n_with_concordant = 0
        n_with_chain = 0
        n_with_mirror_hit = 0
        n_with_c1_hit = 0
        n_with_c2_hit = 0
        n_with_side_hit = 0

        iterator = enumerate(pairs_to_analyze)
        if not args.no_progress:
            from tqdm import tqdm

            iterator = tqdm(list(iterator), desc="EC analysis", leave=False)

        from rational_distance.concordant.analysis import _ensure_pari

        pari = None
        if pairs_to_analyze:
            pari_started = time.perf_counter()
            pari = _ensure_pari()
            profile.time_pari_init_s += time.perf_counter() - pari_started

        for _idx, (A, B) in iterator:
            try:
                diagnostics = diagnose_pair(
                    A,
                    B,
                    ec_bound=args.ec_bound,
                    pari=pari,
                    profile=active_profile,
                    include_rank=include_rank,
                )
                results.append(diagnostics)
                profile.n_pairs_completed += 1

                result = diagnostics.result
                if result.rank is not None:
                    rank_counts[result.rank] = rank_counts.get(result.rank, 0) + 1
                if result.has_concordant:
                    n_with_concordant += 1
                if result.has_chain_solution:
                    n_with_chain += 1
                    print(f"\n*** CHAIN SOLUTION: {result.summary()} ***")
                if diagnostics.mirror_hit_n:
                    n_with_mirror_hit += 1
                if diagnostics.c1_hit_n:
                    n_with_c1_hit += 1
                if diagnostics.c2_hit_n:
                    n_with_c2_hit += 1
                if diagnostics.side_hit_n:
                    n_with_side_hit += 1
            except Exception as exc:
                profile.n_pairs_failed += 1
                print(f"\n  Error on ({A},{B}): {exc}")

        elapsed = time.perf_counter() - t0

        print(f"\n{'─' * 72}")
        print(f"Analysed {len(results)} pairs in {elapsed:.1f}s")
        if include_rank:
            print("\nRank distribution:")
            for rank in sorted(rank_counts):
                print(f"  rank={rank}: {rank_counts[rank]} pairs")
        else:
            print("\nRank distribution: skipped")
        analyzed_pairs = len(results)
        print(f"Pairs analyzed after safe pair sieve: {analyzed_pairs}/{len(pairs)}")
        print(f"\nPairs with concordant N: {n_with_concordant}/{analyzed_pairs}")
        print(f"Pairs with chain-compatible N: {n_with_chain}/{analyzed_pairs}")
        print(f"Pairs with mirror hits: {n_with_mirror_hit}/{analyzed_pairs}")
        print(f"Pairs with C1 hits: {n_with_c1_hit}/{analyzed_pairs}")
        print(f"Pairs with C2 hits: {n_with_c2_hit}/{analyzed_pairs}")
        print(f"Pairs with side hits: {n_with_side_hit}/{analyzed_pairs}")

        if n_with_chain > 0:
            print("\n*** HARBORTH SOLUTIONS EXIST! ***")

        top = args.top if args.top > 0 else len(results)
        post_started = time.perf_counter()
        conc_results = [diagnostics for diagnostics in results if diagnostics.result.has_concordant]
        profile.n_pairs_with_concordant = n_with_concordant
        profile.n_pairs_with_chain_compatible = n_with_chain
        profile.n_pairs_with_mirror_hit = n_with_mirror_hit
        profile.n_pairs_with_c1_hit = n_with_c1_hit
        profile.n_pairs_with_c2_hit = n_with_c2_hit
        profile.n_pairs_with_side_hit = n_with_side_hit
        if conc_results:
            print(f"\nPairs with concordant N (showing up to {top}):")
            conc_results.sort(key=_best_candidate_sort_key)
            for diagnostics in conc_results[:top]:
                result = diagnostics.result
                best = diagnostics.best_candidate
                rank_label = result.rank if result.rank is not None else "skipped"
                print(
                    f"  (A={result.A}, B={result.B}): rank={rank_label} "
                    f"concordant_n={result.concordant_n} "
                    f"mirror_hit_n={diagnostics.mirror_hit_n or 'none'} "
                    f"side_hit_n={diagnostics.side_hit_n or 'none'} "
                    f"best_side_hit={best.side_hit if best is not None else 'none'} "
                    f"best_b={best.b if best is not None else 'none'} "
                    f"best_b_positive={best.b_positive if best is not None else 'none'} "
                    f"min_combined_delta={best.combined_delta if best is not None else 'none'}"
                )
                print()
        profile.time_postprocess_s += time.perf_counter() - post_started

        if profile.enabled:
            _print_concordant_profile(profile.as_dict())

        if args.out:
            json_started = time.perf_counter()
            report = {
                "max_hyp": args.max_hyp,
                "ec_bound": args.ec_bound,
                "n_pairs": len(pairs),
                "n_pairs_analyzed": analyzed_pairs,
                "safe_pair_sieve_enabled": safe_pair_sieve_enabled,
                "elapsed_s": round(elapsed, 2),
                "rank_distribution": rank_counts,
                "n_with_concordant": n_with_concordant,
                "n_with_chain_compatible": n_with_chain,
                "n_with_mirror_hit": n_with_mirror_hit,
                "n_with_c1_hit": n_with_c1_hit,
                "n_with_c2_hit": n_with_c2_hit,
                "n_with_side_hit": n_with_side_hit,
                "pairs": [_batch_pair_summary(diagnostics) for diagnostics in results],
            }
            if profile.enabled:
                report["profile"] = profile.as_dict()
            with open(args.out, "w") as handle:
                json.dump(report, handle, indent=2)
            profile.time_json_write_s += time.perf_counter() - json_started
            print(f"\nReport saved to {args.out}")


RUNNERS = {
    "chain": _run_chain,
    "chain-fast": _run_chain_fast,
    "concordant": _run_concordant,
    "ec": _run_ec,
    "parametric": _run_parametric,
}


__all__ = [
    "RUNNERS",
    "_resolve_parametric_limits",
    "_run_chain",
    "_run_chain_fast",
    "_run_concordant",
    "_run_ec",
    "_run_parametric",
]
