from seasonal_lights.core.controller import ControllerManager
from seasonal_lights.core.scene_engine import SceneEngine
from seasonal_lights.devices.simulator import SimulatorDevice
from seasonal_lights.enums import DeviceType, EffectType
from seasonal_lights.models import (
    Color,
    DeviceConfig,
    EffectConfig,
    SceneConfig,
    ZoneConfig,
)


def test_scene_renders_to_controller() -> None:
    device_config = DeviceConfig(
        device_id="test_device",
        name="Test Device",
        device_type=DeviceType.SIMULATOR,
        outputs=1,
    )

    controller = ControllerManager()

    controller.register(
        SimulatorDevice(device_config.device_id)
    )

    zone = ZoneConfig(
        zone_id="test_zone",
        name="Test Zone",
        controller_id="test_device",
        output=0,
        pixel_count=10,
    )

    scene = SceneConfig(
        scene_id="test_scene",
        name="Test Scene",
        zones=["test_zone"],
        effect=EffectConfig(
            effect_type=EffectType.SOLID,
            color=Color(255, 0, 0),
            brightness=1.0,
        ),
    )

    engine = SceneEngine(
        controllers=controller,
        zones={
            zone.zone_id: zone,
        },
    )

    engine.render_scene(
        scene=scene,
        elapsed=0,
    )

    device = controller.get("test_device")

    assert len(device.outputs[0]) == 10
    assert device.outputs[0][0] == Color(255, 0, 0)