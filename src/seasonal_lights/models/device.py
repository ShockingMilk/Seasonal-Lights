"""Device configuration model."""

from dataclasses import dataclass

from seasonal_lights.enums import DeviceType


@dataclass(frozen=True)
class DeviceConfig:
    """Configuration describing a lighting controller."""

    device_id: str
    name: str
    device_type: DeviceType
    outputs: int

    def __post_init__(self) -> None:
        """Validate configuration."""

        if not self.device_id:
            raise ValueError("device_id cannot be empty")

        if self.outputs < 1:
            raise ValueError("outputs must be at least 1")