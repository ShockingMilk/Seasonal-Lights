"""Simulator lighting device."""

from seasonal_lights.devices.base import LightingDevice
from seasonal_lights.models.color import Color


class SimulatorDevice(LightingDevice):
    """
    Simulates an LED controller.

    The simulator intentionally implements the same interface as a
    future physical controller.
    """

    def __init__(self, device_id: str) -> None:
        super().__init__(device_id)

        self.outputs: dict[int, list[Color]] = {}

    def set_pixels(
        self,
        output: int,
        pixels: list[Color],
    ) -> None:
        """Store a pixel buffer."""

        self.outputs[output] = list(pixels)

    def clear(self, output: int) -> None:
        """Clear an output."""

        self.outputs[output] = [
            Color(0, 0, 0)
            for _ in self.outputs.get(output, [])
        ]

    def show(self, output: int) -> None:
        """Display the current simulated output."""

        pixels = self.outputs.get(output, [])

        if not pixels:
            print(f"[{self.device_id}:output-{output}] OFF")
            return

        preview = "".join(
            self._color_to_character(pixel)
            for pixel in pixels
        )

        print(
            f"[{self.device_id}:output-{output}] "
            f"{preview}"
        )

    def close(self) -> None:
        """Close the simulated device."""

        self.outputs.clear()

    @staticmethod
    def _color_to_character(color: Color) -> str:
        """Convert an RGB color into a compact terminal representation."""

        if color.red == 0 and color.green == 0 and color.blue == 0:
            return "."

        if color.red >= color.green and color.red >= color.blue:
            return "R"

        if color.green >= color.red and color.green >= color.blue:
            return "G"

        return "B"