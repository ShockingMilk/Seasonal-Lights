from seasonal_lights.devices.base import LightingDevice
from seasonal_lights.models.color import Color


class SimulatorDevice(LightingDevice):
    """Simulates an addressable LED controller."""

    def __init__(
        self,
        name: str,
        outputs: int,
        pixels_per_output: int,
    ) -> None:
        if outputs < 1 or pixels_per_output < 1:
            raise ValueError(
                "Outputs and pixel count must be positive."
            )

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
        self.initialized = True

        print(
            f"[SIMULATOR] Initialized: {self.name}"
        )

    def set_pixels(
        self,
        output: int,
        pixels: list[Color],
    ) -> None:
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

        self._display(output)

    def clear(self, output: int) -> None:
        self._validate_output(output)

        self.pixels[output] = [
            Color.black()
            for _ in range(self.pixels_per_output)
        ]

        self._display(output)

    def shutdown(self) -> None:
        for output in self.pixels:
            self.clear(output)

        self.initialized = False

        print("[SIMULATOR] Shutdown.")

    def _validate_output(self, output: int) -> None:
        if output not in self.pixels:
            raise ValueError(
                f"Invalid simulator output: {output}"
            )

    def _display(self, output: int) -> None:
        pixels = self.pixels[output]

        average = self._average_color(pixels)

        print(
            f"[SIMULATOR] Output {output} | "
            f"Pixels: {len(pixels)} | "
            f"Average RGB: {average.as_tuple()}"
        )

    @staticmethod
    def _average_color(
        pixels: list[Color],
    ) -> Color:
        if not pixels:
            return Color.black()

        count = len(pixels)

        return Color(
            red=sum(pixel.red for pixel in pixels) // count,
            green=sum(pixel.green for pixel in pixels) // count,
            blue=sum(pixel.blue for pixel in pixels) // count,
        )