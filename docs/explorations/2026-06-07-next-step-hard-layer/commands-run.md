# Commands Run

## Helper Tests

```bash
uv run pytest tests/test_gm_closure_delta.py -q
```

Result:

```text
6 passed in 0.01s
```

## Targeted Ruff

```bash
uv run ruff check \
  src/rational_distance/results/gm_closure_delta.py \
  tests/test_gm_closure_delta.py \
  scripts/partner/full_gm_full_plane_delta_stats.py
```

Result:

```text
All checks passed!
```

## Smoke Partner Scan

```bash
PYTHONPATH=src uv run python scripts/partner/full_gm_full_plane_delta_stats.py \
  --limit 200 --workers 1 \
  --summary-out results/partner/full_gm_full_plane_delta_summary_smoke.json \
  --top-out results/partner/full_gm_full_plane_delta_top_smoke.jsonl \
  --hits-out results/partner/full_gm_full_plane_closure_hits_smoke.jsonl \
  --top-n 20
```

Result:

```text
Total vertices scanned:     200
Total relation rows:        2018
Total full-plane hits:      0
Global min |delta|:         1
```

## Exhaustive Partner Full-Plane Scan

```bash
PYTHONPATH=src uv run python scripts/partner/full_gm_full_plane_delta_stats.py \
  --components results/partner/partner_full_bfs_components.jsonl \
  --summary-out results/partner/full_gm_full_plane_delta_summary.json \
  --top-out results/partner/full_gm_full_plane_delta_top.jsonl \
  --hits-out results/partner/full_gm_full_plane_closure_hits.jsonl \
  --workers 10 --chunksize 100 --top-n 100
```

Result:

```text
Total vertices scanned:     338225
Total relation rows:        5071562
Total full-plane hits:      0
Global min |delta|:         1
```

## Full Test Suite

```bash
uv run pytest -q
```

Result:

```text
338 passed, 2 warnings in 30.02s
```

The warnings are the existing unknown `pytest.mark.slow` warnings in `tests/test_parallel.py`.

## Closure-First 3/4 Smoke

```bash
PYTHONPATH=src uv run python scripts/theory/closure_first_three_square_search.py \
  --max-leg 100 --diff-tail 300 --top-k 30
```

Result:

```text
3/4 near misses: 16
three-edge candidates: 16
exact hits: 0
best: (A,B,N1,N2)=(15,84,13,112), relation diff=A+B, missing A-N1, delta=6
```

This smoke reproduces the remembered orientation:

```text
(A,B,N1,N2)=(7,45,24,28)
N1+N2=A+B=52
A-N1, B-N1, B-N2 are square checks
A-N2 fails with nearest-square delta 8
```

## Closure-First 3/4 Medium Run

```bash
PYTHONPATH=src uv run python scripts/theory/closure_first_three_square_search.py \
  --max-leg 500 --diff-tail 1500 --top-k 100
```

Result:

```text
3/4 near misses: 135
three-edge candidates: 135
exact hits: 0
best: (A,B,N1,N2)=(13,112,15,84), relation sum=|A-B|, missing A-N1, delta=6
```

## Closure-First 3/4 Main Run

```bash
PYTHONPATH=src uv run python scripts/theory/closure_first_three_square_search.py \
  --max-leg 2000 --diff-tail 5000 --top-k 200
```

Result:

```text
3/4 near misses: 682
three-edge candidates: 682
exact hits: 0
elapsed=0.034s
```

Key distribution:

```text
near_miss_3of4_by_relation:
  diff=A+B:     206
  diff=|A-B|:   202
  sum=A+B:      174
  sum=|A-B|:    100

missing_edge_counts:
  A-N1: 197
  B-N1: 184
  A-N2: 182
  B-N2: 119
```

## Closure-First Script Checks

```bash
uv run ruff check scripts/theory/closure_first_three_square_search.py
uv run ruff format --check scripts/theory/closure_first_three_square_search.py
uv run pytest tests/test_closure_first_three_square_search.py -q
PYTHONPATH=src uv run python scripts/theory/closure_first_three_square_search.py \
  --max-leg 100 --diff-tail 300 --top-k 30 \
  --out /tmp/closure_first_3of4_smoke.json
```

Result:

```text
All checks passed!
1 file already formatted
2 passed
3/4 near misses: 16
exact hits: 0
```

## Closure-First Speed Benchmark

```bash
PYTHONPATH=src uv run python - <<'PY'
import time
from scripts.theory.closure_first_three_square_search import scan_fast, scan_legacy
for max_leg, tail, top in [(100,300,30),(500,1500,100),(2000,5000,200)]:
    t=time.perf_counter(); legacy=scan_legacy(max_leg, tail, top); old=time.perf_counter()-t
    t=time.perf_counter(); fast=scan_fast(max_leg, tail, top); new=time.perf_counter()-t
    assert fast['near_miss_3of4_total']==legacy['near_miss_3of4_total']
    assert fast['near_miss_3of4_by_relation']==legacy['near_miss_3of4_by_relation']
    assert fast['missing_edge_counts']==legacy['missing_edge_counts']
    print(max_leg, old, new, old/new)
PY
```

Result:

```text
max_leg=100:  0.0322s -> 0.0008s  (40.9x)
max_leg=500:  1.0225s -> 0.0090s  (113.5x)
max_leg=2000: 19.1705s -> 0.0348s (550.9x)
```

Post micro-optimization benchmark:

```text
max_leg=2000, tail=5000:       0.0348s
max_leg=50000, tail=125000:    3.7332s
max_leg=100000, tail=250000:   8.4923s
```

## Closure-First Fast Large Runs

```bash
PYTHONPATH=src uv run python scripts/theory/closure_first_three_square_search.py \
  --max-leg 10000 --diff-tail 25000 --top-k 200 \
  --out results/counterexample_first/2026-06-07/closure_first_3of4_max10000_tail25000_fast.json

PYTHONPATH=src uv run python scripts/theory/closure_first_three_square_search.py \
  --max-leg 50000 --diff-tail 125000 --top-k 200 \
  --out results/counterexample_first/2026-06-07/closure_first_3of4_max50000_tail125000_fast.json

PYTHONPATH=src uv run python scripts/theory/closure_first_three_square_search.py \
  --max-leg 100000 --diff-tail 250000 --top-k 200 \
  --out results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast.json
```

Results:

```text
max_leg=10000:  3901 near misses, 0 exact hits, elapsed 0.687s
max_leg=50000:  20623 near misses, 0 exact hits, elapsed 5.993s
max_leg=100000: 41736 near misses, 0 exact hits, elapsed 15.988s in the CLI run
```

Best `max_leg=100000` sample:

```text
(A,B,N1,N2) = (17745,53911,60840,132496)
|N1-N2| = A+B = 71656
missing edge = B-N2
nearest-square delta = 1
```

## Closure-First Delta 1-10 Distribution

```bash
jq '{
  summary:{max_leg,diff_tail,elapsed_s,candidate_strategy,near_miss_3of4_total,exact_hits_by_relation},
  delta_1_to_10:.failed_delta_counts_1_to_10,
  signed_delta_1_to_10:.failed_signed_delta_counts_1_to_10,
  by_relation:.failed_delta_1_to_10_by_relation,
  by_missing_edge:.failed_delta_1_to_10_by_missing_edge,
  failed_delta_counts_top:.failed_delta_counts_top[:20]
}' \
  results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast.json
```

Result:

```text
delta_1_to_10:
  1: 1
  6: 6
  7: 6
  8: 4
  9: 2
  10: 6

signed_delta_1_to_10:
  -10: 4
  -9: 2
  -8: 4
  -7: 4
  -6: 4
  1: 1
  6: 2
  7: 2
  10: 2

by_relation totals:
  diff=A+B: 8
  diff=|A-B|: 8
  sum=|A-B|: 7
  sum=A+B: 2

by_missing_edge totals:
  A-N1: 16
  B-N2: 5
  A-N2: 2
  B-N1: 2
```

Horizontal bound comparison:

```bash
PYTHONPATH=src uv run python - <<'PY'
import json
from pathlib import Path
files=[
('2k','results/counterexample_first/2026-06-07/closure_first_3of4_max2000_tail5000.json'),
('10k','results/counterexample_first/2026-06-07/closure_first_3of4_max10000_tail25000_fast.json'),
('50k','results/counterexample_first/2026-06-07/closure_first_3of4_max50000_tail125000_fast.json'),
('100k','results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast.json'),
]
for label,path in files:
    r=json.loads(Path(path).read_text())
    d=r['failed_delta_counts_1_to_10']
    print(label, 'near', r['near_miss_3of4_total'], 'leq10', sum(d.values()), 'dist', d)
PY
```

Result:

```text
2k   near 682    leq10 13  dist {6:4, 8:4, 9:1, 10:4}
10k  near 3901   leq10 19  dist {6:6, 7:2, 8:4, 9:2, 10:5}
50k  near 20623  leq10 24  dist {6:6, 7:6, 8:4, 9:2, 10:6}
100k near 41736  leq10 25  dist {1:1, 6:6, 7:6, 8:4, 9:2, 10:6}
```

## Closure-First D4 Point Dedup

```bash
uv run python scripts/theory/closure_first_three_square_search.py \
  --max-leg 100000 \
  --diff-tail 250000 \
  --top-k 50 \
  --include-d4-points \
  --out results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast_d4points.json
```

Output:

```text
wrote results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast_d4points.json
3/4 near misses: 41736 three-edge candidates: 41736 exact hits: 0 elapsed=10.016s
best: {'A': 17745, 'B': 53911, 'N1': 60840, 'N2': 132496, 'relation': 'diff=A+B', 'missing': ['B-N2'], 'delta': 1}
```

Summary:

```text
raw records:                41,736
same coordinate points:        857
D4 point orbits:               480
raw - coordinate duplicates: 40,879
coordinate - D4 duplicates:    377
raw - D4 duplicates:        41,256
exact 4/4 hits:                  0
```

D4 point delta `1..10`:

```text
1: 1
6: 3
7: 3
8: 2
9: 1
10: 3
```

`2..5` still do not appear after coordinate/D4 deduplication.

Plot:

```bash
uv run --group viz python scripts/theory/plot_closure_first_d4_points.py \
  results/counterexample_first/2026-06-07/closure_first_3of4_max100000_tail250000_fast_d4points.json \
  --out results/counterexample_first/2026-06-07/closure_first_3of4_d4_points_max100000_tail250000.png
```

Output:

```text
wrote results/counterexample_first/2026-06-07/closure_first_3of4_d4_points_max100000_tail250000.png
records=480 inside_unit_square=84
```

The plot did not show a clean visual law. The useful follow-up is to split the `480`
orbits by high `raw_count` families and by small-delta failures.

## Notes

The full partner result uses exact `find_concordant_by_factorization` per vertex. There is no finite `N` bound inside that enumeration.

The closure-first sum relations are exhaustive for the stated `A,B` bound. The difference relations are bounded by `--diff-tail`, because `|N1-N2|=target` allows infinitely many positive shifts.

The optimized closure-first script keeps `scan_legacy` only as a correctness oracle in tests. The default `scan` path uses `scan_fast`.
