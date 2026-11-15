import time


def monotonic_seconds() -> float:
    """Return a monotonic timestamp."""

    return time.monotonic()


def sleep(seconds: float) -> None:
    """Sleep for a specified duration."""

    if seconds > 0:
        time.sleep(seconds)