# M2 Pure v_ell Direct Residue Method Classification

## Question

Do the direct good-reduction residue arguments used in `wl536`-`wl538`
continue indefinitely, or can that method itself be classified exactly?

This work proves a finite classification of that method. It also records the
last additional class found by it, at auxiliary prime `23`.

## Method Being Classified

Fix an auxiliary prime `p ≡ 3 (mod 4)` and a nonzero residue `e mod p`.
The equation `a^2+q^2=ell`, with `ell ≡ e (mod p)`, makes rational `a,q`
`p`-adically integral. Put `R=q^2 mod p` and define

```text
f1(R)=R,
f2(R)=e-R,
f3(R)=eR+4,
f4(R)=G_e(R).
```

The direct method excludes `e` exactly when there is no `R in F_p` for which
all four values are quadratic residues, with zero included as a square
residue. In the large-prime proof, zeros are separated only to show the
existence of the stronger kind of survivor having all four values nonzero.
Any such survivor proves that this direct residue test cannot exclude the
class. It need not lift to a rational `wl535` point.

## Large-prime bound

Let `chi` be the quadratic character with `chi(0)=0`, and set

```text
W = (1/16) * sum_R product_i (1+chi(fi(R))).
```

For any nonempty subset `S` of the four factors, the corresponding character
sum has degree at most `sum_{i in S} deg(fi)`, where the degrees are
`1,1,1,4`. The three linear factors are pairwise coprime for nonzero `e`:
the only nontrivial possible collision would require `e^2=-4`, impossible
because `-1` is a nonsquare.

They are also coprime to `G_e`. At their roots,

```text
G_e(0)=16,
G_e(e)=(5e^2-8e+4)^2,
e^4 G_e(-4/e)=16(5e^2-8e+4)^2.
```

The common expression cannot vanish because its discriminant is `-16`.
Finally,

```text
disc_R(G_e)=2^26 (e-2)^2 (e-1)^4 (e^2-2e+2).
```

The last factor has discriminant `-4`, so over these fields `G_e` is
squarefree unless `e=1` or `e=2`. In those two cases

```text
G_1(R)=(R^2+4R-4)^2,
G_2(R)=(R^2+4)^2,
```

and its character-sum contribution is nonnegative. Every other nonempty
subset product is not a constant times a square, so the quadratic Weil bound
applies. Summing the worst-case errors gives

```text
sum_{empty != S} (deg(product_S)-1)
  = 8*(1+1+1+4)-15
  = 41.
```

Hence

```text
W >= (p-41*sqrt(p))/16.
```

At most seven residues are roots of one of the four factors. Their total
weighted contribution to `W` is at most seven. Therefore `W>7` forces a
survivor with every factor nonzero. For primes `p ≡ 3 (mod 4)`, this holds
from `p=1907` onward.

## Exact finite certificate

It remains to enumerate primes `p ≡ 3 (mod 4)` below `1907`, every nonzero
`e mod p`, and every square residue `R`. The executable certificate finds
exactly four excluding pairs:

```text
(p,e) = (7,5), (11,10), (19,15), (23,5).
```

The first three are `wl536`-`wl538`. The fourth proves the new direct
obstruction

```text
ell ≡ 5 (mod 23).
```

Together with `ell ≡ 1 (mod 4)`, this is exactly

```text
ell ≡ 5 (mod 92),
```

an infinite prime subfamily by Dirichlet.

## Exact Failure Proposition

The direct single-prime, good-reduction, four-square-residue elimination
method is exhausted. No auxiliary prime `p ≡ 3 (mod 4)` other than
`7,11,19,23` eliminates any nonzero parameter residue, and the four displayed
pairs are the complete list.

This does not prove that the complementary `wl535` classes have rational
points. It proves only that further work cannot consist of repeating the same
single-prime residue table. A next proof gate must use valuations/bad
reduction, more than one local condition in a genuinely coupled way, a
descent, or a strict rational counterexample.

No complete Selmer upper bound, rank-zero theorem, `Sha[2]=0`, general family
exclusion, or M3 statement is proved here.
