# Near Misses

The table below ranks exact stage-3 survivors at `max_hyp=100000`. These pairs survived:

```text
gcd_aware_kills
full-plane chain_closure_mod_sieve
```

and were then checked by exact GEN-CLOSURE.

## Top Stage-3 Near-Misses

| Rank | `(A,B)` | `g` | `D_g` | `k` | Closest relation | Delta | Witness |
|---:|---|---:|---:|---:|---|---:|---|
| 1 | `(15960,61776)` | 24 | 1 | 5 | `|N1-N2|=|A-B|` | 1 | `49280,95095` |
| 2 | `(1080,1428)` | 12 | 1 | 2 | `N1+N2=A+B` | 3 | `1071,1440` |
| 3 | `(3780,16320)` | 60 | 1 | 3 | `N1+N2=A+B` | 3 | `9072,11025` |
| 4 | `(8364,11136)` | 12 | 1 | 2 | `N1+N2=A+B` | 4 | `8352,11152` |
| 5 | `(25344,51660)` | 36 | 1 | 3 | `|N1-N2|=|A-B|` | 4 | `22880,49200` |
| 6 | `(3960,6300)` | 180 | 1 | 5 | `|N1-N2|=|A-B|` | 4 | `5280,7616` |
| 7 | `(460,2200)` | 20 | 3 | 2 | `|N1-N2|=A+B` | 5 | `2625,5280` |
| 8 | `(2160,2856)` | 24 | 1 | 2 | `N1+N2=A+B` | 6 | `2142,2880` |
| 9 | `(7560,32640)` | 120 | 1 | 3 | `N1+N2=A+B` | 6 | `18144,22050` |
| 10 | `(5940,6384)` | 12 | 1 | 2 | `N1+N2=A+B` | 7 | `6080,6237` |

## Survivor Strata

The hard samples are mostly in the `D_g=1` layer:

| `D_g` | Stage-3 survivor count |
|---:|---:|
| 1 | 13,988 |
| 3 | 2,480 |
| 4 | 1,814 |
| 8 | 785 |
| 12 | 104 |
| 24 | 48 |

Since `D_g=1` means the gcd-aware divisibility argument has no force, this layer is the best target for a new theorem.

Top gcd values among stage-3 survivors:

| gcd | Count |
|---:|---:|
| 12 | 1,831 |
| 60 | 1,256 |
| 24 | 1,115 |
| 120 | 674 |
| 36 | 646 |
| 48 | 564 |
| 180 | 374 |
| 84 | 347 |
| 72 | 347 |
| 240 | 306 |

## Closest Relation Distribution

Among stage-3 survivors at `max_hyp=100000`:

| Closest relation | Count |
|---|---:|
| `|N1-N2|=A+B` | 6,998 |
| `N1+N2=A+B` | 6,770 |
| `N1+N2=|A-B|` | 3,071 |
| `|N1-N2|=|A-B|` | 2,380 |

This matters because the closest misses are not all inside-square sums. The full-plane difference relations are genuinely active in the data.

## High-k Observations

High `k` helps produce more chances to close, but it did not produce a hit in this pass.

At `max_hyp=100000`, the highest observed `k` in the ranked data was `8`; the top `k=8` rows were killed before exact survivor status, usually by full-plane modular obstruction. The best high-k residual in the smaller gcd-strata pass was `(3960,6300)`, with `k=5` and delta `4`.

Plain-language takeaway: having many `N` values is useful, but not sufficient. The `N` values still land one or more units away from the four allowed closure targets.

## Constructive Gap-1 Families

The `constructive-families` slice searched in the reverse direction: first force or nearly force closure, then test exact square conditions. Its strongest rows have all four square checks true and closure gap `1`.

Top examples:

| `(A,B)` | `(N1,N2)` | Nearest relation | Gap | gcd profile |
|---|---|---|---:|---|
| `(60,84)` | `(63,80)` | `N1+N2=A+B` | 1 | `gcd(A,B)=12`, `gcd(N1,N2)=1` |
| `(63,80)` | `(60,84)` | `N1+N2=A+B` | 1 | `gcd(A,B)=1`, `gcd(N1,N2)=12` |
| `(84,780)` | `(112,585)` | `N1+N2=|A-B|` | 1 | `gcd(A,B)=12`, `gcd(N1,N2)=1` |
| `(112,585)` | `(84,780)` | `|N1-N2|=A+B` | 1 | `gcd(A,B)=1`, `gcd(N1,N2)=12` |

These transposed pairs suggest a possible structural symmetry: the four-square condition can be easy while the final closure equality is shifted by one.
