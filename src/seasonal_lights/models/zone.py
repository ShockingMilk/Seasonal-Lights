from dataclasses import dataclass


@dataclass(frozen=True)
class Zone:
    """Represents a logical group of lights."""

    zone_id: str
    name: str
    device_id: str
    output: int
    pixel_count: int

    def __post_init__(self) -> None:
        if self.output < 0:
            raise ValueError("Output cannot be negative.")

        if self.pixel_count < 1:
            raise ValueError("A zone must contain at least one pixel.")