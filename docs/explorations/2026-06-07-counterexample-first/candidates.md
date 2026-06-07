# Candidates

## Exact Hits

No verified GEN-CLOSURE hit was found in this pass.

| Bound | Hits | Verification status |
|---:|---:|---|
| 10,000 | 0 | exact full-plane scan completed |
| 100,000 | 0 | exact full-plane scan completed |
| 1,000,000 | 0 | exact full-plane scan completed |

## What A Hit Would Need

A candidate must provide positive integers `(A,B,N1,N2)` such that:

```text
N_i^2 + A^2 = square
N_i^2 + B^2 = square
```

for both `i=1,2`, and:

```text
{N1 + N2, |N1 - N2|} intersects {A + B, |A - B|}
```

The scans here used exactly that predicate. They did not use the old inside-square-only condition `N1+N2=A+B` as a full-plane test.

## Closest Main-Scan Candidate-Like Object

The closest stage-3 survivor is:

| Field | Value |
|---|---|
| `(A,B)` | `(15960, 61776)` |
| `gcd(A,B)` | `24` |
| `D_g` | `1` |
| exact concordant `N` | `[4950, 10368, 20007, 49280, 95095]` |
| closest relation | `|N1-N2| = |A-B|` |
| witness pair | `N1=49280`, `N2=95095` |
| left side | `45815` |
| right side | `45816` |
| delta | `1` |

Plain-language status: this is not a counterexample. It is one integer away from the full-plane difference closure relation.

## Closest Constructive Candidate-Like Object

The constructive subagent found examples where all four square checks are already true, but the final closure misses by `1`.

| Field | Value |
|---|---|
| `(A,B,N1,N2)` | `(60,84,63,80)` |
| square checks | `63^2+60^2=87^2`, `63^2+84^2=105^2`, `80^2+60^2=100^2`, `80^2+84^2=116^2` |
| closest relation | `N1+N2=A+B` |
| left side | `143` |
| right side | `144` |
| delta | `1` |

Plain-language status: this is also not a counterexample, but it is an excellent construction seed because the four distance equations are already perfect.
