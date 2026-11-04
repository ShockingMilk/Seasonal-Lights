"""Base interface for lighting devices."""

from abc import ABC, abstractmethod

from seasonal_lights.models.color import Color


class LightingDevice(ABC):
    """
    Abstract interface for a lighting controller.

    Physical devices such as Pico W controllers should implement this
    interface without requiring changes to the scene engine.
    """

    def __init__(self, device_id: str) -> None:
        self.device_id = device_id

    @abstractmethod
    def set_pixels(
        self,
        output: int,
        pixels: list[Color],
    ) -> None:
        """Set the complete pixel buffer for an output."""

    @abstractmethod
    def clear(self, output: int) -> None:
        """Turn all pixels on an output off."""

    @abstractmethod
    def show(self, output: int) -> None:
        """Commit the current pixel buffer to the physical device."""

    @abstractmethod
    def close(self) -> None:
        """Release resources used by the device."""