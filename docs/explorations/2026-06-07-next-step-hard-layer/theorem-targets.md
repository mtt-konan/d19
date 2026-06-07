# Theorem Targets

## Target 1: Hard-Layer Residue Obstruction

Try to prove:

```text
If 12 | gcd(A,B), then exact full-plane closure cannot occur.
```

That statement is probably too strong as written, but it is the right starting shape. The data says this layer dominates the residual, and the gap-1 rows suggest the final linear target may be forced into a nonzero residue class.

More realistic version:

```text
Let g = gcd(A,B) = 12h. For all concordant N_i,N_j, the four values
N_i+N_j and |N_i-N_j| avoid A+B and |A-B| modulo a modulus depending on h
or the reduced pair (A/g, B/g).
```

## Target 2: Gap-1 Template

The `(60,84,63,80)` row should be treated as a small Diophantine template, not a curiosity.

Useful question:

```text
Can the construction that gives N1+N2=A+B-1 ever be deformed to equality?
```

If no, it may become a proof seed. If yes, it may become a counterexample generator.

## Target 3: Partner-Transpose Near-Miss Symmetry

The full-plane partner scan shows many near-misses where `(A,B)` and the closest `N` row swap roles.

Example:

```text
(A,B)=(92,440), closest N=(525,1056), diff=A+B misses by 1.
(A,B)=(525,1056), closest N=(92,440), sum=|A-B| misses by 1.
```

This suggests checking whether partner graph edges preserve a signed delta invariant, or at least turn one gap-1 relation into another gap-1 relation.

## Target 4: Island Full-Plane Pass

The full `G_M` pass is now complete, but the island reports still have old wording. The cheap cleanup is:

```text
Rerun island-level reports with full-plane delta fields.
```

This is not mathematically deeper than the full graph scan, but it prevents future readers from confusing graph-island closure with Harborth full-plane closure.

## Closed Side Target: Center-Line Branch

The `A=B` center-vertical branch is equivalent by axis swap to the `N1=N2=n`
center-horizontal branch. In current closure language, that branch asks for one
shared Pythagorean `n` and one of:

```text
a + b = 2n
|a - b| = 2n
```

Yang Ji's Theorem 2 in "Several special cases of a square problem"
(`arXiv:2105.05250`) proves that no point on a square midline has four rational
distances to the vertices, and the paper states that this special case extends
to the whole plane. Treat this branch as closed, pending a local proof note that
rewrites the infinite descent in our variables.

## Deprioritized

Do not spend the next round only extending finite bounds. Wider scans are useful after the hard-layer structure is better understood, but the current best return is from explaining why delta reaches `1` and then stops.
