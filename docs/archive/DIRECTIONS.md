# Directions

这份文档是路线入口。旧的五条 CLI 路线仍保留，但当前研究主线已经收束。

## Current Reading Order

1. [PROJECT_STATUS.md](../PROJECT_STATUS.md)
2. [CLOSURE_QUOTIENT_MAINLINE.md](../CLOSURE_QUOTIENT_MAINLINE.md)
3. [OPEN_DIRECTIONS.md](../OPEN_DIRECTIONS.md)
4. [EXPLORATION_MAP.md](./EXPLORATION_MAP.md)
5. [work-logs/README.md](../work-logs/README.md)

## Route Status

```text
concordant / closure quotient     active
chain-fast                        baseline / finite search reference
parametric, ec, chain              paused / historical
```

## Active Route

The active route is:

```text
fixed (A,B)
  -> concordant N
  -> closure leg M
  -> AA/BB quotient
  -> lambda=A/B family
  -> rank-zero Selmer proof attempt
```

Main code and docs:

- `src/rational_distance/concordant/`
- `scripts/theory/audit_closure_quotient_*`
- `tests/test_closure_quotient_*`
- [CLOSURE_QUOTIENT_MAINLINE.md](../CLOSURE_QUOTIENT_MAINLINE.md)

## Baseline Route

`chain-fast` remains the finite-search baseline. It is useful for:

- sanity checks;
- bounded no-counterexample scans;
- producing examples and residual datasets.

It is not the current proof engine, because scaling the search bound is still
finite evidence.

## Paused Routes

`parametric`, `ec`, and `chain` remain available through the CLI for historical
compatibility and reproduction. They are not current proof directions.

## Maintenance Rule

When a new result lands, classify it as one of:

- theorem / proof segment;
- strict certificate;
- candidate evidence;
- closed failed route;
- engineering support.

Do not treat larger counts or longer logs as proof progress.
