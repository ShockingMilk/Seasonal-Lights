from dataclasses import dataclass

from seasonal_lights.enums.device import DeviceType


@dataclass(frozen=True)
class Device:
    """Represents a configured lighting controller."""

    device_id: str
    name: str
    device_type: DeviceType
    outputs: int
    pixels_per_output: int

    def __post_init__(self) -> None:
        if self.outputs < 1:
            raise ValueError("A device must have at least one output.")

        if self.pixels_per_output < 1:
            raise ValueError(
                "A device must support at least one pixel per output."
            )