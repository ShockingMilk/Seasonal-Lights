"""Timing utilities."""

import time


def monotonic_seconds() -> float:
    """Return a monotonic timestamp in seconds."""

    return time.monotonic()