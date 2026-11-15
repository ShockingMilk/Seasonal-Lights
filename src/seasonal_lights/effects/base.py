from abc import ABC, abstractmethod

from seasonal_lights.models.color import Color


class LightEffect(ABC):
    """Base class for lighting effects."""

    def __init__(
        self,
        brightness: float = 1.0,
        speed: float = 1.0,
    ) -> None:
        if not 0.0 <= brightness <= 1.0:
            raise ValueError(
                "Brightness must be between 0.0 and 1.0."
            )

        if speed < 0:
            raise ValueError(
                "Speed cannot be negative."
            )

        self.brightness = brightness
        self.speed = speed

    @abstractmethod
    def update(
        self,
        elapsed: float,
        pixel_count: int,
    ) -> list[Color]:
        """Generate the current pixel frame."""