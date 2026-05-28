# wl071 - PARI `nbthreads` 显式单线程修复

日期：2026-05-27

## 背景

wl070 里已经确认过一类 PARI 卡住：多个 Python worker（单任务子进程）同时跑 `ellrank`（秩计算）时，PARI 内部又启用多线程，最后停在：

```text
ellrank
ell2selmer
mt_queue_reset
pthread_join
```

当时的修复是让 `scripts/prove_no_solution.py` 默认设置：

```text
PARI_MT_ENGINE=single
```

这保证 worker 能继承这个环境变量。

## 新复现

后续 20k fast-core run 使用：

```text
--fast-core
--moduli minimal
```

核心筛已经结束，summary 显示：

```text
checked        = 10090806
no_solution    = 10080387
survivor_count = 10419
```

然后进入 survivor（幸存疑难对）审计。SQLite DB 显示：

```text
pair_proof_status rows = 10000
status hard_case       = 10000
max(updated_at)        = 2026-05-27T14:03:10+00:00
```

也就是说，审计已经完成 10000 个幸存疑难对，还剩 419 个时不再写 DB。

## 现场证据

主进程和 worker 都确实带着环境变量：

```text
PARI_MT_ENGINE=single
```

但是卡住 worker 的 `sample` 仍然看到：

```text
ellrank
ell2selmer
mt_queue_reset
pthread_join
__ulock_wait
```

同时 worker 内部还有 PARI 的：

```text
mt_queue_run
pthread_cond_wait
```

这说明问题仍在 PARI 内部多线程队列，而不是 SQLite 写锁，也不是 Python 主进程没有把环境变量传给 worker。

## 关键反证

独立探针：

```bash
uv run python - <<'PY'
import os
os.environ.setdefault('PARI_MT_ENGINE','single')
from cypari2 import Pari
pari = Pari()
print('env', os.environ.get('PARI_MT_ENGINE'))
print('default(nbthreads)', pari('default(nbthreads)'))
PY
```

输出：

```text
env single
default(nbthreads) 10
```

所以在当前 macOS + cypari2 + PARI 2.17.2 组合里，`PARI_MT_ENGINE=single` 不会自动把 PARI 的 `nbthreads` 改成 1。

这解释了为什么 wl070 的修复仍然不够：环境变量在，但 PARI 内部线程数还是 10。

## 修复

在 `rational_distance.concordant.analysis._ensure_pari()` 里创建 `Pari()` 后显式执行：

```python
pari = cypari2.Pari()
if os.environ.get("PARI_MT_ENGINE", "").strip().lower() == "single":
    pari("default(nbthreads,1)")
pari.allocatemem(64 * 1024 * 1024)
```

这样外层约定仍是：

```text
PARI_MT_ENGINE=single
```

但真正生效点变成 PARI 自己的运行时配置：

```text
default(nbthreads,1)
```

## 测试

新增回归测试：

```text
tests/test_concordant.py::TestConcordantEC::test_ensure_pari_forces_single_thread_when_requested
```

测试用 fake `cypari2.Pari` 验证 `_ensure_pari()` 在 `PARI_MT_ENGINE=single` 时会调用：

```text
default(nbthreads,1)
```

先看过红灯：旧代码只调用 `allocatemem`，测试失败。

修复后测试通过。

## 真实探针验证

修复后运行：

```bash
PYTHONPATH=src uv run python - <<'PY'
import os
os.environ['PARI_MT_ENGINE'] = 'single'
from rational_distance.concordant.analysis import _ensure_pari
pari = _ensure_pari()
print('env', os.environ.get('PARI_MT_ENGINE'))
print('nbthreads', pari('default(nbthreads)'))
PY
```

输出：

```text
PARI stack size set to 67108864 bytes, maximum size set to 67108864
env single
nbthreads 1
```

## 对当前卡住进程的影响

这个修复只影响新启动的 Python 进程。已经卡住的 worker 里 PARI 已经初始化成 `nbthreads=10`，不会被新代码自动改变。

所以旧 run 需要停止后重跑。

## 后续建议

- 继续保留命令行里的 `PARI_MT_ENGINE=single`，表达运行意图。
- 但判断是否真的关闭 PARI 内部多线程，要看 `default(nbthreads)`，不能只看环境变量。
- 大范围 benchmark 先用 `--fast-core-only`，特别是 `--moduli minimal` 会留下很多幸存疑难对，不适合直接接完整 PARI 审计。
- 如果需要完整审计，后续还应做 per-pair timeout（每个 pair 的超时）和当前 pair 日志，方便定位单个卡住输入。
