from abc import ABC, abstractmethod

from seasonal_lights.models.color import Color


class LightingDevice(ABC):
    """Common interface for all lighting devices."""

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the device."""

    @abstractmethod
    def set_pixels(
        self,
        output: int,
        pixels: list[Color],
    ) -> None:
        """Send pixel data to an output."""

    @abstractmethod
    def clear(self, output: int) -> None:
        """Turn off an output."""

    @abstractmethod
    def shutdown(self) -> None:
        """Safely shut down the device."""