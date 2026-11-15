import math

from seasonal_lights.effects.base import LightEffect
from seasonal_lights.models.color import Color


class PulseEffect(LightEffect):
    """Pulses a color between off and configured brightness."""

    def __init__(
        self,
        color: Color,
        brightness: float = 1.0,
        speed: float = 1.0,
    ) -> None:
        super().__init__(
            brightness=brightness,
            speed=speed,
        )

        self.color = color

    def update(
        self,
        elapsed: float,
        pixel_count: int,
    ) -> list[Color]:
        wave = (
            math.sin(elapsed * self.speed * math.tau) + 1
        ) / 2

        intensity = wave * self.brightness

        color = self.color.scale(intensity)

        return [
            color
            for _ in range(pixel_count)
        ]