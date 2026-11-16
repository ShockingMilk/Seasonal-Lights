from dataclasses import dataclass

@dataclass(frozen=True)
class Zone:
    """Represents a logical group of lights on a physical output."""

    zone_id: str
    name: str
    device_id: str
    output: int
    pixel_count: int
    pixel_start: int = 0

    def __post_init__(self) -> None:
        if self.output < 0:
            raise ValueError("Output cannot be negative.")

        if self.pixel_start < 0:
            raise ValueError("Pixel start cannot be negative.")

        if self.pixel_count < 1:
            raise ValueError("A zone must contain at least one pixel.")

    @property
    def pixel_end(self) -> int:
        """Return the exclusive end of this zone's pixel range."""
        return self.pixel_start + self.pixel_count

    @property
    def pixel_range(self) -> range:
        """Return the pixel indices belonging to this zone."""
        return range(self.pixel_start, self.pixel_end)
