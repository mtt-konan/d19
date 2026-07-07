# Rank-Zero Selmer Odd-Prime Cases

## Question

Can the coprime support partition be turned into a per-package local-case
checklist for future rank-zero Selmer transcripts?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_odd_prime_cases.py \
  --coprime-supports results/closure_quotient_rank_zero_selmer_coprime_supports.json \
  --out results/closure_quotient_rank_zero_selmer_odd_prime_cases.json \
  --strict
```

## Output

```text
status=ok
package_count=9
odd_prime_case_count=27
two_adic_case_count=9
local_condition_proved_count=0
```

## Interpretation

普通话说：每个 rank-zero Selmer package 现在有 4 个局部检查小盒子：

```text
ell odd and ell | L
ell odd and ell | T
ell odd and ell | T^2 + 4*L^2
ell = 2
```

9 个 package 合起来就是 27 个奇素数 case 和 9 个 2-adic case。
这让未来 transcript 可以逐盒子写局部 squareclass 条件。

## Boundary

All cases are still `open`. This is a checklist, not a local Selmer image
computation, local condition proof, Selmer rank bound, or family exclusion.
