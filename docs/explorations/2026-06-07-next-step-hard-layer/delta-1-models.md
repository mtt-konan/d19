# Delta-1 Models

These examples are not counterexamples. They are useful because all four square checks pass exactly, and only the final full-plane closure misses by `1`.

## Stage-3 Survivor: `(15960,61776)`

```text
A  = 15960 = 2^3 * 3 * 5 * 7 * 19
B  = 61776 = 2^4 * 3^3 * 11 * 13
N1 = 49280 = 2^7 * 5 * 7 * 11
N2 = 95095 = 5 * 7 * 11 * 13 * 19

gcd(A,B) = 24
D_g = 1
gcd(N1,N2) = 385
```

Exact square checks:

```text
15960^2 + 49280^2 = 51800^2
15960^2 + 95095^2 = 96425^2
61776^2 + 49280^2 = 79024^2
61776^2 + 95095^2 = 113399^2
```

Full-plane closure deltas:

| Relation | Value | Target | Delta |
|---|---:|---:|---:|
| `N1+N2 = A+B` | `144375` | `77736` | `66639` |
| `N1+N2 = |A-B|` | `144375` | `45816` | `98559` |
| `|N1-N2| = A+B` | `45815` | `77736` | `-31921` |
| `|N1-N2| = |A-B|` | `45815` | `45816` | `-1` |

This row survives the sound prefilters and is decided only by exact GEN-CLOSURE. It is the strongest local model for the hard layer.

## Constructive Gap-1: `(60,84,63,80)`

```text
A  = 60 = 2^2 * 3 * 5
B  = 84 = 2^2 * 3 * 7
N1 = 63 = 3^2 * 7
N2 = 80 = 2^4 * 5

gcd(A,B) = 12
D_g = 1
gcd(N1,N2) = 1
```

Exact square checks:

```text
60^2 + 63^2 = 87^2
60^2 + 80^2 = 100^2
84^2 + 63^2 = 105^2
84^2 + 80^2 = 116^2
```

Full-plane closure deltas:

| Relation | Value | Target | Delta |
|---|---:|---:|---:|
| `N1+N2 = A+B` | `143` | `144` | `-1` |
| `N1+N2 = |A-B|` | `143` | `24` | `119` |
| `|N1-N2| = A+B` | `17` | `144` | `-127` |
| `|N1-N2| = |A-B|` | `17` | `24` | `-7` |

## Shared Pattern

Both models have:

```text
A+B ≡ 0 mod 24
|A-B| ≡ 0 mod 24
nearest closure value ≡ -1 mod 24
```

This is only a clue, not a proof. But it says the square constraints can line up perfectly while the final linear placement lands one unit away from the target.
