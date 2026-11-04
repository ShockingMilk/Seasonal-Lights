"""Lighting controller management."""

from seasonal_lights.devices.base import LightingDevice


class ControllerManager:
    """Maintains registered lighting controllers."""

    def __init__(self) -> None:
        self._devices: dict[str, LightingDevice] = {}

    def register(
        self,
        device: LightingDevice,
    ) -> None:
        """Register a lighting device."""

        if device.device_id in self._devices:
            raise ValueError(
                f"Device already registered: {device.device_id}"
            )

        self._devices[device.device_id] = device

    def get(
        self,
        device_id: str,
    ) -> LightingDevice:
        """Retrieve a device by ID."""

        try:
            return self._devices[device_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown lighting device: {device_id}"
            ) from exc

    def close_all(self) -> None:
        """Close all registered devices."""

        for device in self._devices.values():
            device.close()