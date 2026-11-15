from seasonal_lights.devices.base import LightingDevice
from seasonal_lights.models.color import Color
from seasonal_lights.models.zone import Zone


class LightingController:
    """Routes pixel frames to configured lighting devices."""

    def __init__(
        self,
        devices: dict[str, LightingDevice],
        zones: dict[str, Zone],
    ) -> None:
        self.devices = devices
        self.zones = zones

        self._validate_configuration()

    def _validate_configuration(self) -> None:
        """Validate zone and device relationships."""

        for zone in self.zones.values():
            if zone.device_id not in self.devices:
                raise ValueError(
                    f"Unknown device: {zone.device_id}"
                )

            device = self.devices[zone.device_id]

            if zone.output >= device.outputs:
                raise ValueError(
                    f"Invalid output for zone: {zone.zone_id}"
                )

            if zone.pixel_count > device.pixels_per_output:
                raise ValueError(
                    f"Zone exceeds output capacity: {zone.zone_id}"
                )

    def render(
        self,
        zone_pixels: dict[str, list[Color]],
    ) -> None:
        """Send pixel frames to their configured outputs."""

        for zone_id, pixels in zone_pixels.items():
            if zone_id not in self.zones:
                raise ValueError(
                    f"Unknown zone: {zone_id}"
                )

            zone = self.zones[zone_id]
            device = self.devices[zone.device_id]

            if len(pixels) != zone.pixel_count:
                raise ValueError(
                    f"Incorrect pixel count for zone: {zone_id}"
                )

            device_pixels = (
                list(pixels)
                + [
                    Color.black()
                    for _ in range(
                        device.pixels_per_output - zone.pixel_count
                    )
                ]
            )

            device.set_pixels(
                output=zone.output,
                pixels=device_pixels,
            )

    def clear(self) -> None:
        """Clear every configured output once."""

        cleared = set()

        for zone in self.zones.values():
            key = (zone.device_id, zone.output)

            if key in cleared:
                continue

            self.devices[zone.device_id].clear(zone.output)

            cleared.add(key)

    def shutdown(self) -> None:
        """Shut down all devices."""

        for device in self.devices.values():
            device.shutdown()