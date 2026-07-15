# Berry C_1 Q3a Final Boundary

## Accepted Outcome

`precise_C1_etale_descent_blocker`

The selected curve remains

```text
C_1: v^2=g6(t),  K=Q(i),  t in P^1(Q).
```

No exclusion and no strict four-distance point are claimed. The exact
etale-descent blocker is the missing dyadic factor-field embedding certificate
at `K_varpi=Q_2(i)`.

## Established Object

The certified dyadic factor degrees are `[2,4]` over `K_varpi`. Writing

```text
A_varpi = E_2 x E_4,
[E_2:K_varpi]=2,
[E_4:K_varpi]=4,
```

the dyadic squareclass object has

```text
dim_F2(A_varpi^*/A_varpi^{*2}) = 6+10 = 16.
```

Hilbert norm-restriction duality gives the exact alternatives

```text
E_2 not contained in E_4:  (dim F_varpi, dim H_varpi) = (12,8),
E_2 contained in E_4:      (dim F_varpi, dim H_varpi) = (13,10),
```

where `F_varpi` is the quotient by diagonal `K_varpi` squareclasses and
`H_varpi` is its norm kernel. The source dimension `dim J(K_varpi)/2J(K_varpi)=5`
does not choose either alternative and does not compute the local fake image.

## Missing Theorem/Input

A proof-complete Q3a2 result requires one exact coefficient-level certificate
that decides whether the quadratic local factor field embeds in the quartic
local factor field. Equivalently, after exact completion and factorization,
the quadratic factor must be proved reducible or irreducible over `E_4`.
Without that bit there is no fixed coordinate presentation of `H_varpi`, hence
no certified 16-column ambient localization matrix and no valid Q3c local
image/kernel dimension.

The prepared exact Magma source `q3a2-embedding-bit.m` implements the
criterion with `Completion`, `Factorization`, `ext`, `Roots`, and
`IsIrreducible`. The permitted free-Magma submission was retried on
2026-07-16 and failed locally before receiving any calculator response with:

```text
status=transport_error
error=<urlopen error [Errno 1] Operation not permitted>
```

This raw failure is not treated as arithmetic evidence. The blocker is the
missing exact embedding certificate itself, not the service timeout.

## Independent Attempts

| route | result |
|---|---|
| exact local Sage/maximal-order probing | no certificate; repeated local API path terminated |
| free Magma local-field submission | exact 1,712-byte test prepared; local transport rejected before execution |
| pure SymPy exact number-field route | reached `round_two`/`prime_decomp`; no subfield certificate before termination |
| theorem-only local squareclass audit | proved `dim W_varpi=16` and the `(12,8)/(13,10)` alternatives, but cannot choose the bit |

The Q3a anchor records all known Worker session ids and `unknown` where the
wrapper did not expose one. Relevant commits are `f6070f3`, `5ce7b3f`,
`5c777d7`, `22eb3a8`, `fa0ae10`, and `6ef26ff`.

## Unclaimed Results

This outcome does not claim a fake Selmer group, true Selmer group, rank,
saturation, rational-`t` classification, Chabauty result, four-distance
reconstruction, family theorem, or conclusion about another Berry sextic.
The already certified facts `C_i(K_varpi)=empty` and trivial Jacobian torsion
remain valid but do not solve the selected `C_1` descent.

## Validation

The final focused regression suite passed (`9 passed`). `git diff --check`
passed and the final committed worktree is clean.
