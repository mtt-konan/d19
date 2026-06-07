# Partner Graph Full-Plane Scan

## What Was Upgraded

Old partner graph results answered the inside-square question:

```text
N1 + N2 = A + B
```

The current full-plane GEN-CLOSURE question is broader:

```text
{N1+N2, |N1-N2|} intersects {A+B, |A-B|}
```

So this follow-up added a full-plane delta helper and a full `G_M @ max_value=1M` scanner.

## New Full-Graph Result

Command:

```bash
PYTHONPATH=src uv run python scripts/partner/full_gm_full_plane_delta_stats.py \
  --components results/partner/partner_full_bfs_components.jsonl \
  --summary-out results/partner/full_gm_full_plane_delta_summary.json \
  --top-out results/partner/full_gm_full_plane_delta_top.jsonl \
  --hits-out results/partner/full_gm_full_plane_closure_hits.jsonl \
  --workers 10 --chunksize 100 --top-n 100
```

Result:

| Item | Value |
|---|---:|
| vertices scanned | `338,225` |
| candidate full-plane relation rows | `5,071,562` |
| full-plane closure hits | `0` |
| vertices with full-plane hits | `0` |
| global min delta | `1` |
| vertices with delta `1` | `31` |
| elapsed | `8.4s` |

The closure-hit file is empty:

```text
results/partner/full_gm_full_plane_closure_hits.jsonl
```

## Relation Coverage

All four relation families have minimum delta `1` somewhere in the graph:

| Relation | Min delta |
|---|---:|
| `sum=A+B` | `1` |
| `sum=|A-B|` | `1` |
| `diff=A+B` | `1` |
| `diff=|A-B|` | `1` |

This matters because any proof that handles only `N1+N2=A+B` is still proving the old inside-square statement, not the full-plane target.

## First Delta-1 Rows

| `(A,B)` | Relation | `N` row | Value | Target | Delta |
|---|---|---|---:|---:|---:|
| `(92,440)` | `diff=A+B` | `(525,1056)` | `531` | `532` | `1` |
| `(525,1056)` | `sum=|A-B|` | `(92,440)` | `532` | `531` | `-1` |
| `(1260,5440)` | `sum=A+B` | `(3024,3675)` | `6699` | `6700` | `1` |
| `(990,1575)` | `diff=|A-B|` | `(1320,1904)` | `584` | `585` | `1` |
| `(1440,3575)` | `sum=A+B` | `(2508,2508)` | `5016` | `5015` | `-1` |

Some sum near-misses use the same `N` twice, such as `(2508,2508)`. The new scanner allows this for sum relations and forbids it for difference relations, matching `analysis.gen_closure_hit`.

## What This Does And Does Not Prove

This proves the stored `G_M @ max_value=1M` vertex set has no full-plane GEN-CLOSURE hit.

It does not prove the infinite partner graph has no hit, and it does not prove global Harborth. It is strong finite evidence plus a cleaned-up semantic boundary.
