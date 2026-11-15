from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")
R = TypeVar("R")


def switch(
    value: T,
    cases: dict[T, Callable[[], R]],
    default: Callable[[], R] | None = None,
) -> R:
    """Execute the matching switch case."""

    if value in cases:
        return cases[value]()

    if default is not None:
        return default()

    raise ValueError(
        f"No switch case exists for value: {value!r}"
    )