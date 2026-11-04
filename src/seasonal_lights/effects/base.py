"""Base lighting effect."""

from abc import ABC, abstractmethod

from seasonal_lights.models.color import Color


class LightEffect(ABC):
    """Base class for all lighting effects."""

    @abstractmethod
    def render(
        self,
        pixel_count: int,
        elapsed: float,
    ) -> list[Color]:
        """
        Generate the current pixel buffer.

        Args:
            pixel_count: Number of pixels to generate.
            elapsed: Seconds since the effect started.

        Returns:
            A list containing one Color for every pixel.
        """