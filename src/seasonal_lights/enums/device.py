from enum import StrEnum


class DeviceType(StrEnum):
    """Supported lighting device types."""

    SIMULATOR = "simulator"
    LOCAL = "local"
    PICO = "pico"