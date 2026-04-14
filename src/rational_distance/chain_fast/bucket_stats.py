"""Aggregated structural bucket statistics for chain-fast."""

from __future__ import annotations

import json
from dataclasses import dataclass
from math import gcd

BucketIdentity = tuple[str, tuple[object, ...]]

_G_BUCKET_RANGES: tuple[tuple[int, int, str], ...] = (
    (17, 32, "17-32"),
    (33, 64, "33-64"),
    (65, 128, "65-128"),
    (129, 256, "129-256"),
    (257, 512, "257-512"),
)
_DELTA_BINS: tuple[tuple[int, int, str], ...] = (
    (1, 3, "1-3"),
    (4, 7, "4-7"),
    (8, 15, "8-15"),
    (16, 31, "16-31"),
    (32, 63, "32-63"),
    (64, 127, "64-127"),
)


def _g_bucket_label(value: int) -> int | str:
    if value <= 16:
        return value
    for lower, upper, label in _G_BUCKET_RANGES:
        if lower <= value <= upper:
            return label
    return "513+"


def _delta_abs_bin(value: int) -> str:
    abs_value = abs(value)
    for lower, upper, label in _DELTA_BINS:
        if lower <= abs_value <= upper:
            return label
    return "128+"


def _delta_sign(value: int) -> str:
    return "neg" if value < 0 else "pos"


def build_bucket_identities(
    s1: int,
    t1: int,
    s2: int,
    t2: int,
    pair_gcd: int | None = None,
) -> tuple[BucketIdentity, BucketIdentity, BucketIdentity]:
    """Return the three fixed bucket identities for one ordered triple pair."""
    g_value = gcd(t1, s2) if pair_gcd is None else pair_gcd
    delta1 = s1 - t1
    delta2 = s2 - t2
    return (
        ("g_bucket", (_g_bucket_label(g_value),)),
        (
            "delta_bucket",
            (
                _delta_sign(delta1),
                _delta_abs_bin(delta1),
                abs(delta1) % 8,
                _delta_sign(delta2),
                _delta_abs_bin(delta2),
                abs(delta2) % 8,
            ),
        ),
        ("residue_bucket", (s1 % 8, t1 % 8, s2 % 8, t2 % 8)),
    )


def bucket_identity_to_json(bucket_type: str, raw_key: tuple[object, ...]) -> str:
    """Encode one bucket key as canonical JSON for stable DB storage."""
    if bucket_type == "g_bucket":
        payload = {"g_bucket": raw_key[0]}
    elif bucket_type == "delta_bucket":
        payload = {
            "delta1_sign": raw_key[0],
            "delta1_abs_bin": raw_key[1],
            "delta1_abs_mod8": raw_key[2],
            "delta2_sign": raw_key[3],
            "delta2_abs_bin": raw_key[4],
            "delta2_abs_mod8": raw_key[5],
        }
    elif bucket_type == "residue_bucket":
        payload = {
            "s1_mod8": raw_key[0],
            "t1_mod8": raw_key[1],
            "s2_mod8": raw_key[2],
            "t2_mod8": raw_key[3],
        }
    else:  # pragma: no cover - guarded by fixed callers
        raise ValueError(f"Unknown bucket_type: {bucket_type}")
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


@dataclass
class BucketStatRow:
    bucket_type: str
    bucket_key_json: str
    n_total: int = 0
    n_after_basic: int = 0
    n_c3_pass: int = 0
    n_c4_pass: int = 0
    n_near_miss: int = 0
    best_sq4_deficit: int | None = None
    best_sq3_deficit: int | None = None
    sample_a: int | None = None
    sample_b: int | None = None
    sample_c: int | None = None
    sample_d: int | None = None
    sample_sq3_deficit: int | None = None
    sample_sq4_deficit: int | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "bucket_type": self.bucket_type,
            "bucket_key_json": self.bucket_key_json,
            "n_total": self.n_total,
            "n_after_basic": self.n_after_basic,
            "n_c3_pass": self.n_c3_pass,
            "n_c4_pass": self.n_c4_pass,
            "n_near_miss": self.n_near_miss,
            "best_sq4_deficit": self.best_sq4_deficit,
            "best_sq3_deficit": self.best_sq3_deficit,
            "sample_a": self.sample_a,
            "sample_b": self.sample_b,
            "sample_c": self.sample_c,
            "sample_d": self.sample_d,
            "sample_sq3_deficit": self.sample_sq3_deficit,
            "sample_sq4_deficit": self.sample_sq4_deficit,
        }


class BucketStatsCollector:
    """In-memory aggregation of fixed structural bucket statistics."""

    def __init__(self) -> None:
        self._rows: dict[tuple[str, str], BucketStatRow] = {}

    def _row(self, bucket_type: str, raw_key: tuple[object, ...]) -> BucketStatRow:
        key_json = bucket_identity_to_json(bucket_type, raw_key)
        lookup_key = (bucket_type, key_json)
        row = self._rows.get(lookup_key)
        if row is None:
            row = BucketStatRow(bucket_type=bucket_type, bucket_key_json=key_json)
            self._rows[lookup_key] = row
        return row

    def note_total(self, bucket_identities: tuple[BucketIdentity, ...]) -> None:
        for bucket_type, raw_key in bucket_identities:
            self._row(bucket_type, raw_key).n_total += 1

    def note_after_basic(self, bucket_identities: tuple[BucketIdentity, ...]) -> None:
        for bucket_type, raw_key in bucket_identities:
            self._row(bucket_type, raw_key).n_after_basic += 1

    def note_c3_pass(self, bucket_identities: tuple[BucketIdentity, ...]) -> None:
        for bucket_type, raw_key in bucket_identities:
            self._row(bucket_type, raw_key).n_c3_pass += 1

    def note_c4_pass(self, bucket_identities: tuple[BucketIdentity, ...]) -> None:
        for bucket_type, raw_key in bucket_identities:
            self._row(bucket_type, raw_key).n_c4_pass += 1

    def note_near_miss(
        self,
        bucket_identities: tuple[BucketIdentity, ...],
        *,
        a: int,
        b: int,
        c: int,
        d: int,
        sq3: int,
        sq4: int,
        h3: int,
        h4: int,
    ) -> None:
        sq3_deficit = sq3 - h3 * h3
        sq4_deficit = sq4 - h4 * h4
        sample_order = (sq4_deficit, sq3_deficit, a, b, c, d)
        for bucket_type, raw_key in bucket_identities:
            row = self._row(bucket_type, raw_key)
            row.n_near_miss += 1
            current_order = None
            if row.best_sq4_deficit is not None and row.best_sq3_deficit is not None:
                current_order = (
                    row.best_sq4_deficit,
                    row.best_sq3_deficit,
                    row.sample_a,
                    row.sample_b,
                    row.sample_c,
                    row.sample_d,
                )
            if current_order is None or sample_order < current_order:
                row.best_sq4_deficit = sq4_deficit
                row.best_sq3_deficit = sq3_deficit
                row.sample_a = a
                row.sample_b = b
                row.sample_c = c
                row.sample_d = d
                row.sample_sq3_deficit = sq3_deficit
                row.sample_sq4_deficit = sq4_deficit

    def merge(self, other: BucketStatsCollector | None) -> None:
        if other is None:
            return
        for other_row in other._rows.values():
            lookup_key = (other_row.bucket_type, other_row.bucket_key_json)
            row = self._rows.get(lookup_key)
            if row is None:
                self._rows[lookup_key] = BucketStatRow(**other_row.as_dict())
                continue
            row.n_total += other_row.n_total
            row.n_after_basic += other_row.n_after_basic
            row.n_c3_pass += other_row.n_c3_pass
            row.n_c4_pass += other_row.n_c4_pass
            row.n_near_miss += other_row.n_near_miss

            current_order = None
            if row.best_sq4_deficit is not None and row.best_sq3_deficit is not None:
                current_order = (
                    row.best_sq4_deficit,
                    row.best_sq3_deficit,
                    row.sample_a,
                    row.sample_b,
                    row.sample_c,
                    row.sample_d,
                )
            other_order = None
            if other_row.best_sq4_deficit is not None and other_row.best_sq3_deficit is not None:
                other_order = (
                    other_row.best_sq4_deficit,
                    other_row.best_sq3_deficit,
                    other_row.sample_a,
                    other_row.sample_b,
                    other_row.sample_c,
                    other_row.sample_d,
                )
            if other_order is not None and (current_order is None or other_order < current_order):
                row.best_sq4_deficit = other_row.best_sq4_deficit
                row.best_sq3_deficit = other_row.best_sq3_deficit
                row.sample_a = other_row.sample_a
                row.sample_b = other_row.sample_b
                row.sample_c = other_row.sample_c
                row.sample_d = other_row.sample_d
                row.sample_sq3_deficit = other_row.sample_sq3_deficit
                row.sample_sq4_deficit = other_row.sample_sq4_deficit

    def rows(self) -> list[BucketStatRow]:
        return sorted(
            self._rows.values(),
            key=lambda row: (row.bucket_type, row.bucket_key_json),
        )

    def as_dict_rows(self) -> list[dict[str, object]]:
        return [row.as_dict() for row in self.rows()]
