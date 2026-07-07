# Rank-Zero Selmer Coprime Supports

## Question

Can the symbolic local supports be split into independent odd-prime cases for
future rank-zero Selmer transcripts?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_coprime_supports.py \
  --local-supports results/closure_quotient_rank_zero_selmer_local_supports.json \
  --out results/closure_quotient_rank_zero_selmer_coprime_supports.json \
  --strict
```

## Output

```text
status=ok
package_count=9
coprime_support_entry_count=9
local_condition_proved_count=0
```

## Symbolic Facts

For primitive `A:B`, with `T=A+B` and `L=A` for `AA` or `L=B` for `BB`:

```text
gcd(L, T) = 1
gcd(L, T^2 + 4*L^2) = 1
gcd(T, T^2 + 4*L^2) divides 4
```

So the odd-prime local support separates into:

```text
odd primes dividing L
odd primes dividing T
odd primes dividing T^2 + 4*L^2
```

The prime `2` remains a separate 2-adic case.

## Interpretation

普通话说：这一步把未来局部 Selmer 检查拆成更小的盒子。奇素数不会同时落进多个盒子；
真正还会互相缠在一起的是 `2`。这让后续 transcript 可以分别处理三个奇素数场景，再单独处理
2-adic 场景。

## Boundary

This is a symbolic coprime-support partition. It does not compute local Selmer
images, prove local conditions, prove a Selmer rank bound, or exclude any
lambda family.
