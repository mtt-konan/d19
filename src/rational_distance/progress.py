"""Optional progress-bar helper."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, TypeVar

T = TypeVar("T")


class _NullProgress(Iterator[T]):
    def __init__(self, iterable: Iterable[T] | None = None, **_kwargs: Any) -> None:
        self._iterator = iter(iterable) if iterable is not None else iter(())

    def __iter__(self) -> _NullProgress[T]:
        return self

    def __next__(self) -> T:
        return next(self._iterator)

    def update(self, _n: int = 1) -> None:
        return None

    def close(self) -> None:
        return None


def optional_tqdm[T](iterable: Iterable[T] | None = None, **kwargs: Any) -> Any:
    """Return ``tqdm`` when installed, otherwise a no-op progress wrapper."""
    try:
        from tqdm import tqdm
    except ImportError:
        return _NullProgress(iterable, **kwargs)
    return tqdm(iterable, **kwargs)
