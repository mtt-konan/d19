# Q2b Fixed-Basis S-Unit Payload

## Outcome

`q2b_fixed_basis_payload_serialized`

The sixteen actual `BERRY_C1_SUNIT_BASIS` elements are now stored in one
common absolute-field power basis. The public transcript is preserved in
`q2b-fixed-basis-magma-result.json`; the parsed, reusable payload is
`q2b-fixed-basis-payload.json`.

The basis is

```text
[1, a, a^2, ..., a^11],
f12(a) = a^12 - 4*a^11 - 62*a^10 + 68*a^9 + 1647*a^8 + 4184*a^7
         + 2716*a^6 - 376*a^5 + 623*a^4 - 788*a^3 + 194*a^2 - 12*a + 1.
```

The payload contains all sixteen labels and vectors:

```text
zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_10.
```

Each vector has twelve exact rational coordinates. The source expression is
the existing emitter expression
`Eltseq(La!sunit_map(sunit_generators[j]))`; no Magma map or object handle is
serialized.

## Reusable Metadata

The payload contains the exact reduction coefficients for `a^12`, the full
12 by 12 by 12 table reducing every product `a^j*a^k`, and the 12 by 12
matrix for multiplication by `a` (rows are output coordinates and columns are
input basis coordinates). This is enough to multiply arbitrary coordinate
vectors over `Q` and reduce them back to the fixed basis.

The selected embedding of `K=Q(i)` is stored as a twelve-coordinate vector.
With the first emitted order-4 generator designated `zeta4` by the fixed
basis convention, it is

```text
i = -zeta4,
theta = a.
```

The exact metadata checks are

```text
i^2 = -1,
g6(theta) = 0,
```

where `g6` is the selected `C_1` polynomial. The sign is recorded because
the first Magma root-of-unity generator is the opposite square root from the
chosen relative `K` embedding; the squareclass label is unchanged.

## Calculator Evidence

The stored successful calculator response reports:

```text
source bytes: 1557
source sha256: 771d9f203975a5aad72eadf9b086360f5cae036c57a687f156395c373ac7e67e
proxy: http://127.0.0.1:7897
status: ok
Magma: 2.29-8
Magma time: 0.78 seconds
public max time: 60 seconds
emitted S-unit vectors: 16
```

The source is 1,557 bytes, below the 50,000-byte request limit, and contains
no `TwoSelmerGroup` call.

During this run, a fresh submission was also attempted with:

```text
python3 scripts/utility/magma_calculator.py \
  scripts/theory/berry_sextic_magma_sunits.m \
  --timeout 60 \
  --proxy http://127.0.0.1:7897 \
  --json-out /private/tmp/berry_c1_sunits_v1.json
```

Its exact local result was:

```text
input_bytes=1557
status=transport_error
error=<urlopen error [Errno 1] Operation not permitted>
```

This is transport failure only. It is not an arithmetic blocker. The
successful response already present in `/private/tmp/berry-magma-sunits.json`
was copied unchanged to the task-local transcript above. A concrete rerun,
followed by deterministic parsing, is:

```text
python3 scripts/utility/magma_calculator.py \
  scripts/theory/berry_sextic_magma_sunits.m \
  --timeout 60 \
  --proxy http://127.0.0.1:7897 \
  --json-out /private/tmp/berry-magma-sunits.json
python3 scripts/theory/berry_sextic_q2b_fixed_basis.py \
  --magma-json /private/tmp/berry-magma-sunits.json \
  --out docs/codex/tasks/berry-sextic-genus2-classification-20260715/q2b-fixed-basis-payload.json
```

## Validation

The parser and exact fixed-basis checks are:

```text
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/test_berry_sextic_q2b_fixed_basis.py -n 1
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/berry_sextic_q2b_fixed_basis.py \
  tests/test_berry_sextic_q2b_fixed_basis.py
git diff --check
```

The focused test passes with `3 passed`.

## Strict Boundary

This step serializes public fixed-basis field elements and exact arithmetic
metadata only. It does not compute or claim `M_const`, `M_norm`, `M_loc_pi`, a
global lift of either Q2a class, `M_const` or `M_norm` ranks, a fake Selmer
group, a true Selmer group, a rank, saturation, rational `t` values, `Q3`, or
the Berry classification. It does not run `TwoSelmerGroup`, modify
`wl587`-`wl596`, create `wl597`, or process another Berry sextic.
