"""Top-level lighting system."""

import time

from seasonal_lights.config.loader import (
    load_devices,
    load_scenes,
    load_zones,
)
from seasonal_lights.core.controller import ControllerManager
from seasonal_lights.core.scene_engine import SceneEngine
from seasonal_lights.devices.simulator import SimulatorDevice
from seasonal_lights.enums import DeviceType
from seasonal_lights.models import DeviceConfig


class LightingSystem:
    """Top-level application coordinator."""

    def __init__(
        self,
        controllers: ControllerManager,
        scene_engine: SceneEngine,
        scenes: dict,
    ) -> None:
        self.controllers = controllers
        self.scene_engine = scene_engine
        self.scenes = scenes

    @classmethod
    def from_example_configuration(
        cls,
    ) -> "LightingSystem":
        """
        Create the POC system.

        POC #1 uses configuration objects directly so the project can
        be run immediately from the repository.
        """

        device_config = DeviceConfig(
            device_id="simulator_01",
            name="POC Simulator",
            device_type=DeviceType.SIMULATOR,
            outputs=1,
        )

        controller_manager = ControllerManager()

        controller_manager.register(
            SimulatorDevice(device_config.device_id)
        )

        from seasonal_lights.models import (
            Color,
            EffectConfig,
            SceneConfig,
            ZoneConfig,
        )
        from seasonal_lights.enums import EffectType

        zone = ZoneConfig(
            zone_id="test_strand",
            name="Test Strand",
            controller_id="simulator_01",
            output=0,
            pixel_count=30,
        )

        scene = SceneConfig(
            scene_id="demo",
            name="POC Demo",
            zones=["test_strand"],
            effect=EffectConfig(
                effect_type=EffectType.RAINBOW,
                color=Color(255, 255, 255),
                brightness=0.25,
                speed=1.0,
            ),
        )

        scene_engine = SceneEngine(
            controllers=controller_manager,
            zones={
                zone.zone_id: zone,
            },
        )

        return cls(
            controllers=controller_manager,
            scene_engine=scene_engine,
            scenes={
                scene.scene_id: scene,
            },
        )

    def run_demo(
        self,
        duration: float = 10.0,
        frame_rate: float = 10.0,
    ) -> None:
        """Run the POC demonstration."""

        scene = next(iter(self.scenes.values()))

        start_time = time.monotonic()
        frame_time = 1.0 / frame_rate

        try:
            while True:
                elapsed = time.monotonic() - start_time

                if elapsed >= duration:
                    break

                self.scene_engine.render_scene(
                    scene=scene,
                    elapsed=elapsed,
                )

                time.sleep(frame_time)

        except KeyboardInterrupt:
            print("\nDemo interrupted.")

        finally:
            self.controllers.close_all()