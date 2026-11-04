"""Pulsing lighting effect."""

import math

from seasonal_lights.effects.base import LightEffect
from seasonal_lights.models.color import Color


class PulseEffect(LightEffect):
    """Smoothly pulses a color between off and full brightness."""

    def __init__(
        self,
        color: Color,
        brightness: float = 1.0,
        speed: float = 1.0,
    ) -> None:
        self.color = color
        self.brightness = brightness
        self.speed = speed

    def render(
        self,
        pixel_count: int,
        elapsed: float,
    ) -> list[Color]:
        """Render the current pulse state."""

        wave = (
            math.sin(elapsed * self.speed * 2.0 * math.pi)
            + 1.0
        ) / 2.0

        brightness = wave * self.brightness

        pixel = self.color.scaled(brightness)

        return [pixel for _ in range(pixel_count)]