from seasonal_lights.effects.base import LightEffect
from seasonal_lights.models.color import Color


class SolidEffect(LightEffect):
    """Displays a single solid color."""

    def __init__(
        self,
        color: Color,
        brightness: float = 1.0,
    ) -> None:
        super().__init__(brightness=brightness)
        self.color = color

    def update(
        self,
        elapsed: float,
        pixel_count: int,
    ) -> list[Color]:
        color = self.color.scale(self.brightness)

        return [
            color
            for _ in range(pixel_count)
        ]