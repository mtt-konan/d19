# wl053 — Round-2 archive: src/ 顶层 chain-fast / EC / parametric 旧模块迁入 _legacy/

## 目的

接 wl043 的 Round-1（scripts/ 26 个旧脚本归档进 `scripts/archive/`）。这次把
`src/rational_distance/` 顶层里 chain-fast / EC / parametric 时代但**还有内容**
的 10 个 module 物理迁进 `_legacy/`，让顶层只保留当前主线在用的代码。

## 背景

Round-1 之前 `src/rational_distance/` 顶层有 ~14 个 .py 文件混杂着 4 个时代的代码：

```text
parametric  → search.py, search_gpu.py, parametric_core.py, square.py
chain       → search_chain.py
chain-fast  → search_chain_fast.py(stub), chain_db.py, chain_cache_db.py, chain_analysis.py
EC          → search_ec.py(stub), ec_search.py(canonical), ec_db.py, ec_analysis.py,
              concordant_ec.py(stub), pair_generator.py(stub)
现役       → __init__.py, math_utils.py, backend.py, parallel.py
新主线     → concordant/, proof_status/, chain_fast/, ec_search/, results/, literature/, cli/
```

Round-1 已经把 4 个 stub 化的 wrapper 迁了。剩下 10 个含真实代码的旧模块还在顶层，
新读者打开 `src/rational_distance/` 看到一长串文件名容易误判主线。

## 操作

10 个文件 `git mv` 进 `_legacy/`，原位置留 stub：

```text
src/rational_distance/
  chain_analysis.py        →  _legacy/chain_analysis.py        (189 → 13 lines stub)
  chain_cache_db.py        →  _legacy/chain_cache_db.py        (658 → 13)
  chain_db.py              →  _legacy/chain_db.py              (677 → 13)
  ec_analysis.py           →  _legacy/ec_analysis.py           (300 → 13)
  ec_db.py                 →  _legacy/ec_db.py                 (478 → 13)
  parametric_core.py       →  _legacy/parametric_core.py       (306 → 13)
  search.py                →  _legacy/search.py                (296 → 13)
  search_chain.py          →  _legacy/search_chain.py          (521 → 13)
  search_gpu.py            →  _legacy/search_gpu.py            (109 → 13)
  square.py                →  _legacy/square.py                (102 → 13)
```

3636 行物理迁出，顶层只剩 130 行 stub。

## Stub 模式

Round-1 的 `from X import *` + `__all__` 模式不能用，因为旧模块都没声明 `__all__`，
而且 tests 里还有 `from rational_distance.search import _parametric_search_fast_run`
这种 import 私有符号的用法。

改用 `sys.modules` 替换：

```python
"""Deprecated stub. Real implementation: rational_distance._legacy.<name>.

Round-2 archive (wl053) moved the chain-fast / EC / parametric era modules
into the _legacy package. This top-level file replaces itself with the
real module so historical imports (including private _underscore names)
keep working. New code should import from _legacy.<name> directly.
"""

import sys
from rational_distance._legacy import <name> as _impl
sys.modules[__name__] = _impl
```

效果：`rational_distance.X` 和 `rational_distance._legacy.X` 是**同一个** module
对象，所有公私符号、重新加载、isinstance 都一致。

## 内部 cross-reference

`_legacy/` 里 11 处 `from rational_distance.X import ...` 不需要改：stub 自动转
发到 `_legacy/X`，且无环（chain_db→search_chain，search_chain 不反向 import）。

## 验证

```bash
$ uv run pytest -q
234 passed, 2 warnings in 29.16s
```

包含 `tests/test_chain.py` (10 tests), `tests/test_chain_db.py` (10), 
`tests/test_chain_cache_db.py` (4), `tests/test_chain_cli.py` (12),
`tests/test_chain_fast.py` (16), `tests/test_chain_fast_cli.py` (10),
`tests/test_ec.py` (10), `tests/test_parametric.py` (31) 等。

## 顶层现状

```text
src/rational_distance/*.py
  __init__.py        11   active
  backend.py        136   active (PARI / numpy backend)
  math_utils.py      55   active (primitive Pythagorean / sqrt)
  parallel.py       221   active (multiprocessing helper)

  chain_analysis    13   stub  → _legacy
  chain_cache_db    13   stub  → _legacy
  chain_db          13   stub  → _legacy
  concordant_ec      9   stub  → _legacy (round-1)
  ec_analysis       13   stub  → _legacy
  ec_db             13   stub  → _legacy
  pair_generator     9   stub  → _legacy (round-1)
  parametric_core   13   stub  → _legacy
  search            13   stub  → _legacy
  search_chain      13   stub  → _legacy
  search_chain_fast  9   stub  → _legacy (round-1)
  search_ec          9   stub  → _legacy (round-1)
  search_gpu        13   stub  → _legacy
  square            13   stub  → _legacy

src/rational_distance/<package>/
  cli/             active
  concordant/      active  (主线 — pivot-on-N, half-points, 2-descent)
  chain_fast/      active  (baseline)
  ec_search/       active  (PARI ellrank wrapper)
  literature/      active
  proof_status/    active  (workflow)
  results/         active  (catalog)

  _legacy/         24 modules, 3636 lines  停滞探索代码
```

新读者扫一眼顶层就能看到主线只有 4 个独立 .py 文件 + 7 个活跃子包。

## 没改的东西

- `tests/` 里 8 个 chain/ec/parametric 时代的 test 文件没动。它们仍然过；这些 test
  覆盖了 `_legacy/` 里的实现，作为历史回归测试保留是有用的。如果将来确定整组
  代码彻底退役，再考虑把 tests 也搬进 `tests/archive/`。
- `chain_fast/`、`ec_search/` 这两个**子包**没动。它们是 chain-fast / EC 时代但
  还在被新代码间接调用（PARI rank 路径走 `ec_search.compute_rank`）。

## 文件

```text
src/rational_distance/_legacy/<10 modules>      新位置
src/rational_distance/<10 stubs>.py             顶层占位
docs/work-logs/053-round2-archive-src-legacy.md  本文件
```
