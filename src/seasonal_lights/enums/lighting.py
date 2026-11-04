"""Lighting-related enumerations."""

from enum import StrEnum


class ColorMode(StrEnum):
    """Supported color modes."""

    RGB = "rgb"
    RGBW = "rgbw"
    WHITE = "white"


class EffectType(StrEnum):
    """Available lighting effects."""

    SOLID = "solid"
    PULSE = "pulse"
    RAINBOW = "rainbow"


class PixelProtocol(StrEnum):
    """Supported addressable LED protocols."""

    SIMULATED = "simulated"
    WS2812 = "ws2812"
    SK6812 = "sk6812"