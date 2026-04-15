"""Timing and count profile for concordant analysis."""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class ConcordantProfile:
    """Aggregate timings and counts for concordant CLI runs."""

    enabled: bool = False
    deep: int = 0
    rank_enabled: bool = True
    n_pairs_total: int = 0
    n_pairs_completed: int = 0
    n_pairs_failed: int = 0
    n_pairs_with_concordant: int = 0
    n_pairs_with_chain_compatible: int = 0
    n_pairs_with_mirror_hit: int = 0
    n_pairs_with_c1_hit: int = 0
    n_pairs_with_c2_hit: int = 0
    n_pairs_with_side_hit: int = 0
    n_raw_square_x_total: int = 0
    n_concordant_n_total: int = 0
    n_candidates_total: int = 0
    n_deep_extra_total: int = 0
    time_pair_generation_s: float = 0.0
    time_pari_init_s: float = 0.0
    time_rank_s: float = 0.0
    time_find_concordant_s: float = 0.0
    time_chain_compat_s: float = 0.0
    time_deep_search_s: float = 0.0
    time_candidate_diagnostics_s: float = 0.0
    time_pair_analysis_s: float = 0.0
    time_postprocess_s: float = 0.0
    time_json_write_s: float = 0.0

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-safe profile payload."""
        return asdict(self)


__all__ = ["ConcordantProfile"]
