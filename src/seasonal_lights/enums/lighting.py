from enum import StrEnum


class EffectType(StrEnum):
    """Supported lighting effect types."""

    SOLID = "solid"
    PULSE = "pulse"
    RAINBOW = "rainbow"