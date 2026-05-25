# 022 - chain-fast profile / cache / bounded near-miss

## 本轮完成

- `chain-fast` 新增 `--profile`
- 输出和 JSON 里增加 profile 字段
- SQLite 增加 run profile 字段、triple 缓存表、run-triple 记录表
- `chain-fast` 支持优先复用缓存 triples
- `near-miss` 改成 bounded top-K 持久化，新增 `--near-miss-limit`

## 关键工程变化

- 保留 `find_chains_fast()` 兼容行为，同时新增 `run_chain_fast()` 返回结果加 profile
- `chain_db.py` 从“结果库”扩成“结果 + 画像 + triple 缓存索引”
- CLI 现在能在不写数据库时直接看纯计算 profile

## 已验证

- `uv run pytest -q` -> `115 passed`
- `uv run ruff check scripts/search.py src/rational_distance/search_chain_fast.py src/rational_distance/chain_db.py tests/test_all.py`

## 首轮性能观察

纯计算 profile（不写数据库）显示：

- triple 生成几乎不占时间
- 当前最大头是前置 filter
- `python` 路径多进程有效，`8 workers` 在当前机器上接近甜点
- `numpy` 在安全范围内非常强，但仍受 `max_hyp ≈ 36000` 限制

## 下一步建议

- 继续找更强的过滤 / 剪枝
- 保留 triple 缓存用于分析，但不要把它当成主加速点
- 后面如需继续扩展范围，优先考虑 `python + 多进程`
