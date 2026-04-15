# 024 - chain-fast 100k structure findings

## Summary

Recorded the first large-range `chain-fast --bucket-stats` findings.

This round was not about adding a new pruning rule yet. It was about checking
whether the new structure buckets actually reveal anything useful at a range
large enough to matter.

## Runs

Key runs used for the write-up:

- `max_hyp=5000`, `backend=python`, `workers=8`, `--bucket-stats --near-miss --profile`
- `max_hyp=10000`, `backend=python`, `workers=8`, `--bucket-stats --near-miss --profile`
- `max_hyp=100000`, `backend=python`, `workers=8`, `--bucket-stats --profile`

Important note:

- the first `max_hyp=100000` run with `--near-miss` completed the search itself
- but failed when persisting near-miss rows to SQLite
- the failure was `OverflowError: Python int too large to convert to SQLite INTEGER`

So the final large-range analysis used the successful run without raw near-miss
row persistence.

## Result

The `100000` run produced:

- `31,838` primitive triples
- `1,013,658,244` ordered triple pairs
- `250,042,288` pairs after the basic filters
- `318` pairs passing `C3`
- `0` pairs passing `C4`
- wall time about `1192s`

Two strong structural signals were visible:

- larger `g = gcd(t1, s2)` buckets outperform the small `g` buckets by a clear margin
- the top `residue_bucket` families repeatedly satisfy `t1 ≡ 0 (mod 8)`, `s2 ≡ 0 (mod 8)`, with `s1` and `t2` often in `{1,7} (mod 8)`

A weaker signal also appeared:

- large `|s-t|` buckets show up often near the top
- but the `delta_bucket` story is still less clean than `g_bucket` and `residue_bucket`

## Conclusion

This round makes two things much clearer.

First:

- future pruning work should probably start from `g_bucket` and `mod 8` structure
- not from deeper `C3/C4` arithmetic

Second:

- the current `--bucket-stats` implementation is analysis-grade, not production-grade
- it is useful for focused evidence runs
- but it is too expensive to leave on by default for very large long runs

It also established a practical storage boundary:

- raw giant near-miss integers cannot be assumed to fit in SQLite `INTEGER`
- aggregate stats and representative samples are safer persistence targets for `10w+`
