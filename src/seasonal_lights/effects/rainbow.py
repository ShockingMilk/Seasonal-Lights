import colorsys

from seasonal_lights.effects.base import LightEffect
from seasonal_lights.models.color import Color


class RainbowEffect(LightEffect):
    """Generates an animated rainbow across the pixels."""

    def update(
        self,
        elapsed: float,
        pixel_count: int,
    ) -> list[Color]:
        pixels = []

        if pixel_count <= 0:
            return pixels

        movement = elapsed * self.speed

        for index in range(pixel_count):
            position = index / pixel_count

            hue = (position + movement) % 1.0

            red, green, blue = colorsys.hsv_to_rgb(
                hue,
                1.0,
                self.brightness,
            )

            pixels.append(
                Color(
                    red=round(red * 255),
                    green=round(green * 255),
                    blue=round(blue * 255),
                )
            )

        return pixels