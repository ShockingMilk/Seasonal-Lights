"""Lighting zone configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ZoneConfig:
    """Describes a physical or logical lighting zone."""

    zone_id: str
    name: str
    controller_id: str
    output: int
    pixel_count: int

    def __post_init__(self) -> None:
        """Validate zone configuration."""

        if not self.zone_id:
            raise ValueError("zone_id cannot be empty")

        if self.output < 0:
            raise ValueError("output cannot be negative")

        if self.pixel_count < 1:
            raise ValueError("pixel_count must be at least 1")