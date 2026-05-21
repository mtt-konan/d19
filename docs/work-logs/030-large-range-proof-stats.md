# 030-large-range-proof-stats

## Summary

Ran `prove_no_solution.py --max-hyp 500` and analysed the resulting
`hard_case` distribution. The data forced **three corrections** to earlier
claims in `THEORY_DIRECTIONS_ADVANCED.md`:

1. Direction 5 (Heegner) max payoff is **~37%** of hard cases, not 80%+.
2. Direction 6 (L-function derivatives) is **fully redundant** — PARI gives
   exact rank for 100% of hard cases at this scale.
3. Direction 9 (second descent) is **also redundant** as a Selmer-bound
   tightener — PARI's `ellrank` already gives the precise rank.

No code was changed in this worklog. The output is data + doc updates only.

## Run

```bash
uv run python scripts/prove_no_solution.py --max-hyp 500 \
    --db .cache/proofs_500.sqlite3 --no-progress
```

Wall time: ~30 seconds.

## Headline Numbers

```
Total reduced pairs:        6172
├── no_solution (proven):   5852  (94.82%)
│   ├── safe_sieve:         5632
│   └── factor_concordant:   220
└── hard_case:               320  (5.18%)
```

Comparison with the earlier smoke test:

| `max_hyp` | total pairs | hard_case | hard_case ratio |
|---:|---:|---:|---:|
| 100 | 254 | 16 | 6.3% |
| 500 | 6172 | 320 | 5.2% |

The hard_case ratio is **stable around 5–6%**. Without adding new methods,
hard_case count grows roughly linearly with the input.

## Hard-case Rank Distribution (max_hyp=500)

```
rank=1  :  118  (36.9%)
rank=2  :  155  (48.4%)   ← most common
rank=3  :   43  (13.4%)
rank=4  :    4  ( 1.2%)
imprecise (lower != upper) :  0  (0%)
```

**Every single one of the 320 hard cases has `rank_lower == rank_upper`** —
PARI's `ellrank` proves the rank exactly in 100% of cases at this scale.

## Concordant N Distribution (hard_case)

- 313 / 320 hard cases have exactly 1 concordant integer N
- 7 / 320 have 2 concordant integer N

So hard cases are mostly *single-N-fails-to-close* situations, not
multi-witness cases.

## Implication 1 — Direction 5 payoff revised

Direction 5 (Heegner point construction) only applies when rank=1.

- Earlier estimate (max_hyp=100, n=16): rank=1 covers 62.5%
- New observation (max_hyp=500, n=320): rank=1 covers **36.9%**

So direction 5, even when fully implemented with canonical height bounds,
can only upgrade ~37% of current hard_case to `proven_no_solution`.

The remaining 63% (rank ≥ 2) is the territory of direction 7 (Chabauty /
Quadratic Chabauty) or direction 8 (Brauer–Manin obstruction).

## Implication 2 — Direction 6 fully redundant

Direction 6 was originally framed as "use L'(E,1), L''(E,1) to discriminate
rank=1 vs rank=2 vs higher, so direction 5 / 7 know which to apply".

But PARI's `ellrank` already returns exact rank for every hard case observed
so far. There is no rank-discrimination problem left for direction 6 to
solve. Its only remaining value is **canonical height estimation via
Gross–Zagier**, which is direction 5's prerequisite, not a stand-alone
deliverable.

`THEORY_DIRECTIONS_ADVANCED.md` priority table now lists direction 6 with
expected payoff `0`.

## Implication 3 — Direction 9 also redundant

Direction 9 (second descent) tightens the Selmer-group upper bound on rank.
But PARI is already giving us `lower == upper` for every hard case, meaning
its internal computation already proves rank exactly (whatever combination
of 2-descent and point search PARI uses).

Direction 9's only remaining theoretical value would be in cases where PARI
itself returns `lower < upper`. In max_hyp=500 there are zero such cases.

## What the doc was changed to say

`docs/THEORY_DIRECTIONS_ADVANCED.md` updates:

- `## 实现状态速查` block: max_hyp=500 numbers + rank distribution table +
  hard_case ratio trend
- Direction 6 "重要更新": now cites max_hyp=500 (320/320 exact rank)
- `## 优先级建议` table: directions 5 / 6 / 9 payoff columns updated
- `## 给学艺不精者的最实在建议`: replaced overoptimistic 1-2-day Heegner
  promise with the real 2-4-week height-theory cost; pointed at direction 2
  (Gaussian mod p²) and "run more data" as the actual short-term moves

## What This Means For Next Steps

The pipeline is in a healthy state:

- **Initial filter (safe_sieve + factor_concordant)** kills ~95% of pairs.
  Adding direction 2 (Gaussian mod p²) can incrementally improve this but
  cannot reduce hard_case count.
- **PARI ellrank** classifies every hard case by exact rank. We do not need
  any new "rank discrimination" tooling.
- **Hard cases** are the real bottleneck. Reducing them requires either
  height theory (direction 5, weeks) or higher-genus geometry (directions 7,
  8, 10, longer).

Concretely, the most honest near-term moves are:

1. Implement direction 2 (Gaussian mod p² sieve) for incremental kills
2. Run `max_hyp=1000+` to enlarge the hard_case sample (helps any future
   theoretical work)
3. Begin reading on canonical heights for direction 5

## Takeaway

Big-picture takeaway: the project's pipeline is now data-driven enough that
*the math itself tells us which directions are dead*. Directions 6 and 9 are
empirically dead at this scale; direction 5 is alive but smaller than
hoped; directions 7 / 8 / 10 are now the only paths that could reduce
hard_case count to zero.
