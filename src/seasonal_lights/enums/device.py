"""Device-related enumerations."""

from enum import StrEnum


class DeviceType(StrEnum):
    """Types of lighting controllers."""

    SIMULATOR = "simulator"
    RASPBERRY_PI = "raspberry_pi"
    PICO_W = "pico_w"