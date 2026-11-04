"""Solid color lighting effect."""

from seasonal_lights.effects.base import LightEffect
from seasonal_lights.models.color import Color


class SolidEffect(LightEffect):
    """Displays one solid color."""

    def __init__(
        self,
        color: Color,
        brightness: float = 1.0,
    ) -> None:
        self.color = color
        self.brightness = brightness

    def render(
        self,
        pixel_count: int,
        elapsed: float,
    ) -> list[Color]:
        """Render the solid color."""

        pixel = self.color.scaled(self.brightness)

        return [pixel for _ in range(pixel_count)]