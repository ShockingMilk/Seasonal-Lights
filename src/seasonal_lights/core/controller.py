from seasonal_lights.models.color import Color
from seasonal_lights.models.zone import Zone

class LightingController:
    """Routes and combines zone frames into physical output frames."""

    def __init__(
        self,
        devices: dict,
        zones: dict[str, Zone],
    ) -> None:
        self.devices = devices
        self.zones = zones

        self._validate_configuration()

    def _validate_configuration(self) -> None:
        """Validate devices, zone capacities, and pixel ownership."""

        occupied_ranges: dict[
            tuple[str, int],
            list[tuple[int, int, str]],
        ] = {}

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

            if zone.pixel_end > device.pixels_per_output:
                raise ValueError(
                    f"Zone '{zone.zone_id}' exceeds output capacity. "
                    f"Range ends at {zone.pixel_end}, but the output "
                    f"supports only {device.pixels_per_output} pixels."
                )

            key = (zone.device_id, zone.output)

            occupied_ranges.setdefault(key, []).append(
                (
                    zone.pixel_start,
                    zone.pixel_end,
                    zone.zone_id,
                )
            )

        for output_key, ranges in occupied_ranges.items():
            ranges.sort(key=lambda item: item[0])

            for previous, current in zip(
                ranges,
                ranges[1:],
            ):
                previous_start, previous_end, previous_id = previous
                current_start, current_end, current_id = current

                if current_start < previous_end:
                    raise ValueError(
                        f"Zones '{previous_id}' and '{current_id}' "
                        f"overlap on device '{output_key[0]}', "
                        f"output {output_key[1]}."
                    )

    def render(
        self,
        zone_pixels: dict[str, list[Color]],
    ) -> None:
        """
        Combine all zone frames into complete physical output frames.

        Each output is written exactly once per render cycle.
        """

        unknown_zones = set(zone_pixels) - set(self.zones)

        if unknown_zones:
            raise ValueError(
                f"Unknown zones: {unknown_zones}"
            )

        # Create a complete black frame for every physical output.
        output_frames: dict[
            tuple[str, int],
            list[Color],
        ] = {}

        for device_id, device in self.devices.items():
            for output in range(device.outputs):
                output_frames[(device_id, output)] = [
                    Color.black()
                    for _ in range(device.pixels_per_output)
                ]

        # Insert each zone's pixels into its assigned range.
        for zone_id, pixels in zone_pixels.items():
            zone = self.zones[zone_id]

            if len(pixels) != zone.pixel_count:
                raise ValueError(
                    f"Incorrect pixel count for zone: {zone_id}. "
                    f"Expected {zone.pixel_count}, "
                    f"received {len(pixels)}."
                )

            frame = output_frames[
                (zone.device_id, zone.output)
            ]

            frame[
                zone.pixel_start:zone.pixel_end
            ] = pixels

        # Send one complete frame to each physical output.
        for (device_id, output), pixels in output_frames.items():
            self.devices[device_id].set_pixels(
                output=output,
                pixels=pixels,
            )

    def clear(self) -> None:
        """Clear every configured physical output once."""

        for device in self.devices.values():
            for output in range(device.outputs):
                device.clear(output)

    def shutdown(self) -> None:
        """Shut down all configured devices."""

        for device in self.devices.values():
            device.shutdown()