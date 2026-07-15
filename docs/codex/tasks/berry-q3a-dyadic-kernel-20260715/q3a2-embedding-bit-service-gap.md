# Q3a2 Final Embedding-Bit Check

## Outcome

`q3a2_embedding_bit_service_gap`

The embedding bit `E_2 subset E_4` remains undetermined. One and only one
free-Magma wrapper submission was prepared with a 1,712-byte Magma source and
a 60-second request timeout. The wrapper failed before receiving a
calculator response:

```text
input_bytes=1712
status=transport_error
error=<urlopen error [Errno 1] Operation not permitted>
```

This is a transport/sandbox failure, not a Magma intrinsic result and not an
arithmetic conclusion. No calculator XML, Magma version, elapsed time,
factorization, or embedding bit was returned.

## Exact Submission

The task-local source `q3a2-embedding-bit.m` constructs

```text
K = QuadraticField(-1)
P = ideal<RingOfIntegers(K) | 1+i>
K_varpi = Completion(K, P)
```

It maps the selected `g6` into the completion, factors it, selects the exact
degree-2 and degree-4 factors, and defines

```text
E_2 = ext<K_varpi | f_2>
E_4 = ext<K_varpi | f_4>.
```

The exact containment test is the documented polynomial criterion implemented
by `Roots` and `IsIrreducible`: `E_2` embeds in `E_4` exactly when `f_2` is
reducible over `E_4` (equivalently, has two roots there). The source does not
consume or print approximate factor coefficients.

Because the HTTP request was rejected locally, these Magma intrinsics were not
executed by the public service. No raw calculator JSON is preserved: there
was no exact proof-relevant calculator output to preserve.

## Boundary

This check makes no claim about `dim F_varpi`, `dim H_varpi`, localization
columns, `D_inf`, Q3b, Q4, or any later Berry/D19 route. The exact missing
input is a reachable free-Magma Calculator submission, or another exact
coefficient-level local-field certificate for the same containment bit.
