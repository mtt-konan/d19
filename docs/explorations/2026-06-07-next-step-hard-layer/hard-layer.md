# Hard Layer: `D_g=1`

## Definition

The code computes the guaranteed divisor with:

```text
D_g = P2(v2(gcd(A,B))) * P3(v3(gcd(A,B)))
```

In ordinary terms: `D_g` is the number that every valid concordant `N` is forced to be divisible by. If `D_g` is large, it gives a cheap way to rule out closure. If `D_g=1`, that cheap divisibility argument has no force.

The implemented rule is:

| gcd condition | guaranteed part |
|---|---:|
| `v2(g)=0` | `4` |
| `v2(g)=1` | `8` |
| `v2(g)>=2` | `1` |
| `v3(g)=0` | `3` |
| `v3(g)>=1` | `1` |

So for positive `(A,B)`:

```text
D_g=1  iff  v2(g)>=2 and v3(g)>=1  iff  12 | gcd(A,B)
```

There is no normal positive-pair exception in the current search domain.

## Why It Matters

The exact residual increasingly concentrates in this layer:

| Bound | exact GEN survivors | `D_g=1` survivors | Share |
|---:|---:|---:|---:|
| `10,000` | `866` | `585` | `67.55%` |
| `100,000` | `19,219` | `13,988` | `72.78%` |
| `1,000,000` | `332,373` | `256,774` | `77.25%` |

Plain-language version: the easy sieve removes many cases, but the remaining pile is mostly where that easy sieve has no teeth.

## What This Rules Out

It rules out treating reduced/coprime analysis as enough for the global problem. The hard layer is overwhelmingly non-coprime.

It also rules out relying on a “more gcd divisibility” version of the same argument. In the dominant layer, `D_g=1`, so divisibility alone cannot separate the final closure values.

## Best Next Lemma Shape

A useful theorem would look like this:

```text
Assume 12 | gcd(A,B), A < B, and there are at least two concordant N values.
Then all four full-plane closure relations miss by a nonzero residue.
```

The residue may depend on the reduced pair `(A/12h, B/12h)`, on `h=gcd(A,B)/12`, or on the Pythagorean factorizations that produce the concordant `N` values.
