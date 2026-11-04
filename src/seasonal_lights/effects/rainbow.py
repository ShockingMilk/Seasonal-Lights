"""Rainbow lighting effect."""

import colorsys

from seasonal_lights.effects.base import LightEffect
from seasonal_lights.models.color import Color


class RainbowEffect(LightEffect):
    """Displays a moving rainbow across the strand."""

    def __init__(
        self,
        brightness: float = 1.0,
        speed: float = 1.0,
    ) -> None:
        self.brightness = brightness
        self.speed = speed

    def render(
        self,
        pixel_count: int,
        elapsed: float,
    ) -> list[Color]:
        """Render the current rainbow frame."""

        pixels: list[Color] = []

        for index in range(pixel_count):
            position = index / max(pixel_count, 1)

            hue = (
                position
                + elapsed * self.speed * 0.1
            ) % 1.0

            red, green, blue = colorsys.hsv_to_rgb(
                hue,
                1.0,
                self.brightness,
            )

            pixels.append(
                Color(
                    round(red * 255),
                    round(green * 255),
                    round(blue * 255),
                )
            )

        return pixels