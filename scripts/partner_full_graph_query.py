#!/usr/bin/env python3
"""查询 partner_full_graph 结果。

用法: PYTHONPATH=src uv run python scripts/partner_full_graph_query.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def find_component_of(pair: tuple[int, int], source: str = "bfs") -> dict | None:
    target = list(pair)
    fname = "partner_full_bfs_components.jsonl" if source == "bfs" else "partner_full_graph_components.jsonl"
    with (ROOT / "results" / fname).open() as f:
        for line in f:
            c = json.loads(line)
            if target in c["vertices"]:
                return c
    return None


def main() -> int:
    interesting = [
        (153, 560),       # wl058 BFS 起点 (71 nodes @ max_value=100k)
        (264, 420),       # wl058 另一根 (28 nodes @ 100k tree)
        (1344, 3900),     # K_5 hub on (153,560) 6-cycle
        (7105, 9360),     # comp 16 size=71 候选 (跟 wl058 (153,560) 同 size?)
        (55440, 445536),  # K_8
        (58800, 98280),   # K_8
        (40950, 99470),   # 巨型 super-hub
        (412800, 434214), # comp 2 size=473
        (75465, 146965),  # comp 3 size=471
        (439725, 537264), # comp 4 size=393
        (5985, 59584),    # 之前不闭合脚本里的最大 (392 nodes)
    ]
    for ab in interesting:
        c = find_component_of(ab)
        if c is None:
            print(f"({ab[0]:>6}, {ab[1]:>6})  NOT in any component (out of range?)")
            continue
        print(f"({ab[0]:>6}, {ab[1]:>6})  "
              f"comp={c['component_id']:<5} size={c['size']:<5} "
              f"edges={c['edges']:<5} circuit_rank={c['circuit_rank']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
