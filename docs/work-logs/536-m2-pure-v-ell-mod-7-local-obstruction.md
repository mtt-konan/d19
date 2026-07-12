# M2 Pure v_ell mod-7 Local Obstruction

## Question

Starting from the exact `wl535` q-root-coordinate square/quartic proposition
for

```text
support=v_ell|L=1|T=ell|d=(ell,1,ell),
```

can one prove any genuine arithmetic obstruction that removes an infinite
subfamily without reviving a birational rewrite?

Accepted outcomes for this step were:

- a proved local / congruence / valuation obstruction;
- a strict counterexample;
- or one genuinely smaller exact lemma.

This work reaches only the first outcome. It proves one direct local
obstruction and stops. It does not solve the complementary residue classes,
does not produce a counterexample, and does not enter M3.

## Input

Immediate checked input:

```text
wl535  exact q-root-coordinate square/quartic obstruction
```

The touched object layer is still only:

```text
pure-v_ell M2 exact missing proposition
-> direct local analysis inside the wl535 rational system
-> 7-adic integrality from p^2+q^2 = ell
-> mod-7 elimination of one prime residue class
```

not theorem-level Selmer, not a new support family, not shell 11, not a
counterexample search, and not the old package-`x` / `S~` bridge.

## Statement Proved Here

If `ell` is an odd prime with

```text
ell ≡ 1 (mod 4),
ell ≡ 5 (mod 7),
```

then there is no rational pair `(q,V)` such that

```text
ell - q^2 is a rational square,
ell*q^2 + 4 is a rational square,
ell*q^4 + 4*q^2 - 4*ell > 0,
V^2 = G_ell(q^2).
```

Equivalently: the exact `wl535` obstruction has no rational solution in the
prime class `ell ≡ 5 (mod 28)`.

This is an infinite prime subfamily: `gcd(5,28)=1`, so Dirichlet's theorem on
primes in arithmetic progress gives infinitely many primes `ell ≡ 5 (mod 28)`.

## Proof

Assume for contradiction that such a rational solution exists. Choose rational
`p,c` with

```text
p^2 = ell - q^2,
c^2 = ell*q^2 + 4.
```

### Step 1: 7-adic integrality

Write

```text
p = P/D,
q = Q/D
```

in lowest terms, so

```text
P^2 + Q^2 = ell*D^2
```

with `gcd(P,Q,D)=1`.

Because `ell ≡ 5 (mod 7)`, we have `7 ∤ ell`. If `7 | D`, then

```text
P^2 + Q^2 ≡ 0 (mod 7).
```

The square residues mod `7` are

```text
{0,1,2,4},
```

and `-1` is a nonsquare mod `7`. So the only way `P^2+Q^2 ≡ 0 (mod 7)` can
hold is `P ≡ Q ≡ 0 (mod 7)`, contradicting `gcd(P,Q,D)=1`.

Therefore `7 ∤ D`. So `q` and `p` are `7`-adic integers, hence

```text
q^2,
ell-q^2,
ell*q^2+4,
G_ell(q^2)
```

all reduce mod `7` as honest square classes. Since

```text
c^2 = ell*q^2 + 4,
V^2 = G_ell(q^2),
```

both `ell*q^2+4` and `G_ell(q^2)` must reduce to square residues mod `7` too.

### Step 2: residue check for `ell ≡ 5 (mod 7)`

Reduce everything mod `7`. Let

```text
R = q^2 mod 7.
```

Then `R` must lie in

```text
{0,1,2,4}.
```

Also `ell ≡ 5 (mod 7)`, so the four exact square conditions force:

```text
R square mod 7,
5-R square mod 7,
5R+4 square mod 7,
G_5(R) square mod 7.
```

Here

```text
G_5(R) ≡ R^4 + 4*R^3 + 5*R + 2 (mod 7),
```

because the `R^2` coefficient is

```text
32*5^2 - 96*5 + 72 = 392 ≡ 0 (mod 7).
```

Now check the four possible square residues:

1. `R = 0`:

   ```text
   5-R = 5,
   ```

   and `5` is a nonsquare mod `7`.

2. `R = 1`:

   ```text
   5-R = 4,
   5R+4 = 9 ≡ 2,
   ```

   both squares mod `7`, but

   ```text
   G_5(1) ≡ 1 + 4 + 5 + 2 = 12 ≡ 5,
   ```

   and `5` is a nonsquare mod `7`.

3. `R = 2`:

   ```text
   5-R = 3,
   ```

   and `3` is a nonsquare mod `7`.

4. `R = 4`:

   ```text
   5R+4 = 24 ≡ 3,
   ```

   and `3` is a nonsquare mod `7`.

Every square residue class for `q^2 mod 7` is eliminated. Contradiction.

So the exact `wl535` rational system has no solution for primes

```text
ell ≡ 5 (mod 7).
```

## What Is Proved And What Is Not

Proved here:

- one direct local obstruction inside the exact `wl535` proposition;
- the entire prime class `ell ≡ 5 (mod 28)` is removed from the remaining
  pure-`v_ell` M2 search, hence an infinite prime subfamily is closed at M2.

Not proved here:

- the full `wl535` obstruction for all odd primes `ell ≡ 1 (mod 4)`;
- a strict rational counterexample;
- any theorem-level Selmer, rank-zero, or family-exclusion claim;
- anything in M3.

## Next Gate

The exact `wl535` proposition remains open on the complementary odd-prime
classes. Any next step must still be one of:

- another proved local / valuation obstruction;
- a strict counterexample with the full original lift;
- or one genuinely smaller exact arithmetic lemma that is not an invertible
  coordinate rewrite.

This work enters none of those next branches here.
