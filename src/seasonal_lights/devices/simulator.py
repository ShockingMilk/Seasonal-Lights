from seasonal_lights.models.color import Color
from seasonal_lights.devices.base import LightingDevice

class SimulatorDevice(LightingDevice):
    """In-memory simulation of an addressable LED controller."""

    def __init__(
        self,
        name: str,
        outputs: int,
        pixels_per_output: int,
    ) -> None:
        if outputs < 1:
            raise ValueError("Outputs must be positive.")

        if pixels_per_output < 1:
            raise ValueError("Pixel count must be positive.")

        self.name = name
        self.outputs = outputs
        self.pixels_per_output = pixels_per_output

        self.pixels: dict[int, list[Color]] = {
            output: [
                Color.black()
                for _ in range(pixels_per_output)
            ]
            for output in range(outputs)
        }

        self.initialized = False

    def initialize(self) -> None:
        """Initialize the simulated device."""
        self.initialized = True

        print(
            f"[SIMULATOR] Initialized: {self.name} "
            f"({self.outputs} outputs, "
            f"{self.pixels_per_output} pixels per output)"
        )

    def set_pixels(
        self,
        output: int,
        pixels: list[Color],
    ) -> None:
        """Replace the complete pixel frame for one output."""

        self._validate_output(output)

        if not self.initialized:
            raise RuntimeError(
                "Simulator has not been initialized."
            )

        if len(pixels) != self.pixels_per_output:
            raise ValueError(
                f"Expected {self.pixels_per_output} pixels; "
                f"received {len(pixels)}."
            )

        self.pixels[output] = list(pixels)

    def clear(self, output: int) -> None:
        """Clear one output."""

        self._validate_output(output)

        self.pixels[output] = [
            Color.black()
            for _ in range(self.pixels_per_output)
        ]

    def shutdown(self) -> None:
        """Clear all outputs and shut down the simulator."""

        for output in self.pixels:
            self.clear(output)

        self.initialized = False

        print(f"[SIMULATOR] Shutdown: {self.name}")

    def _validate_output(self, output: int) -> None:
        if output not in self.pixels:
            raise ValueError(
                f"Invalid simulator output: {output}"
            )