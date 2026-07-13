from __future__ import annotations

from pathlib import Path

from scripts.theory.json_io import load_json, load_jsonl, write_json


def test_json_helpers_round_trip_and_merge_jsonl(tmp_path: Path) -> None:
    payload_path = tmp_path / "nested" / "payload.json"
    write_json(payload_path, {"status": "ok", "value": 3})
    assert load_json(payload_path) == {"status": "ok", "value": 3}

    first = tmp_path / "first.jsonl"
    second = tmp_path / "second.jsonl"
    first.write_text('{"value": 1}\n', encoding="utf-8")
    second.write_text('{"value": 2}\n\n', encoding="utf-8")

    assert load_jsonl(first) == [{"value": 1}]
    assert load_jsonl([first, second]) == [{"value": 1}, {"value": 2}]
