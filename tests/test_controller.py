import pytest

from seasonal_lights.core.controller import LightingController
from seasonal_lights.devices.simulator import SimulatorDevice
from seasonal_lights.models.color import Color
from seasonal_lights.models.zone import Zone


@pytest.fixture
def device():
    result = SimulatorDevice(
        name="Test Simulator",
        outputs=2,
        pixels_per_output=20,
    )

    result.initialize()

    return result


def test_multiple_zones_share_one_output(device):
    zones = {
        "porch": Zone(
            zone_id="porch",
            name="Porch",
            device_id="simulator",
            output=0,
            pixel_start=0,
            pixel_count=3,
        ),
        "window": Zone(
            zone_id="window",
            name="Window",
            device_id="simulator",
            output=0,
            pixel_start=3,
            pixel_count=4,
        ),
    }

    controller = LightingController(
        devices={"simulator": device},
        zones=zones,
    )

    red = Color(255, 0, 0)
    blue = Color(0, 0, 255)

    controller.render(
        {
            "porch": [red] * 3,
            "window": [blue] * 4,
        }
    )

    frame = device.pixels[0]

    assert frame[0:3] == [red] * 3
    assert frame[3:7] == [blue] * 4
    assert frame[7:] == [Color.black()] * 13


def test_unused_output_is_cleared(device):
    zone = Zone(
        zone_id="porch",
        name="Porch",
        device_id="simulator",
        output=0,
        pixel_count=3,
    )

    controller = LightingController(
        devices={"simulator": device},
        zones={"porch": zone},
    )

    red = Color(255, 0, 0)

    controller.render(
        {"porch": [red] * 3}
    )

    assert device.pixels[1] == [
        Color.black()
    ] * 20


def test_overlapping_zones_are_rejected(device):
    zones = {
        "porch": Zone(
            zone_id="porch",
            name="Porch",
            device_id="simulator",
            output=0,
            pixel_start=0,
            pixel_count=5,
        ),
        "window": Zone(
            zone_id="window",
            name="Window",
            device_id="simulator",
            output=0,
            pixel_start=4,
            pixel_count=5,
        ),
    }

    with pytest.raises(ValueError, match="overlap"):
        LightingController(
            devices={"simulator": device},
            zones=zones,
        )


def test_zone_cannot_exceed_output_capacity(device):
    zone = Zone(
        zone_id="porch",
        name="Porch",
        device_id="simulator",
        output=0,
        pixel_start=18,
        pixel_count=5,
    )

    with pytest.raises(ValueError, match="exceeds output capacity"):
        LightingController(
            devices={"simulator": device},
            zones={"porch": zone},
        )


def test_zone_cannot_reference_unknown_device():
    zone = Zone(
        zone_id="porch",
        name="Porch",
        device_id="missing",
        output=0,
        pixel_count=5,
    )

    with pytest.raises(ValueError, match="Unknown device"):
        LightingController(
            devices={},
            zones={"porch": zone},
        )


def test_unknown_zone_frame_is_rejected(device):
    zone = Zone(
        zone_id="porch",
        name="Porch",
        device_id="simulator",
        output=0,
        pixel_count=3,
    )

    controller = LightingController(
        devices={"simulator": device},
        zones={"porch": zone},
    )

    with pytest.raises(ValueError, match="Unknown zones"):
        controller.render(
            {"missing": [Color.black()] * 3}
        )