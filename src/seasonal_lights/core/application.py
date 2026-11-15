from pathlib import Path
from typing import Any

from seasonal_lights.core.controller import LightingController
from seasonal_lights.core.scene_engine import SceneEngine
from seasonal_lights.core.scheduler import Scheduler
from seasonal_lights.devices.simulator import SimulatorDevice
from seasonal_lights.effects.factory import create_effect
from seasonal_lights.enums.device import DeviceType
from seasonal_lights.models.device import Device
from seasonal_lights.models.scene import Scene
from seasonal_lights.models.zone import Zone
from seasonal_lights.utils.config import load_yaml
from seasonal_lights.utils.switch import switch


class SeasonalLightsApplication:
    """Builds and runs the Seasonal Lights application."""

    def __init__(
        self,
        config_dir: Path,
    ) -> None:
        self.config_dir = config_dir

        self.devices = {}
        self.zones = {}

        self.controller = None
        self.scheduler = None

    def _load_config(
        self,
        filename: str,
    ) -> dict[str, Any]:
        """Load local configuration or fall back to examples."""

        local = self.config_dir / filename

        if local.exists():
            return load_yaml(local)

        example = self.config_dir / filename.replace(
            ".yaml",
            ".example.yaml",
        )

        return load_yaml(example)

    def _create_device(
        self,
        device_id: str,
        data: dict[str, Any],
    ) -> tuple[Device, Any]:
        """Create a device model and implementation."""

        device_type = DeviceType(data["type"])

        device = Device(
            device_id=device_id,
            name=data["name"],
            device_type=device_type,
            outputs=int(data["outputs"]),
            pixels_per_output=int(data["pixels_per_output"]),
        )

        implementation = switch(
            device_type,
            {
                DeviceType.SIMULATOR: lambda: SimulatorDevice(
                    name=device.name,
                    outputs=device.outputs,
                    pixels_per_output=device.pixels_per_output,
                )
            },
            default=lambda: self._unsupported_device(device_type),
        )

        return device, implementation

    @staticmethod
    def _unsupported_device(device_type: DeviceType):
        raise NotImplementedError(
            f"Device type '{device_type}' is not implemented yet."
        )

    def load_devices(self) -> None:
        """Load all configured devices."""

        config = self._load_config(
            "devices.yaml"
        )

        for device_id, data in config["devices"].items():
            _, implementation = self._create_device(
                device_id,
                data,
            )

            self.devices[device_id] = implementation

    def load_zones(self) -> None:
        """Load all configured zones."""

        config = self._load_config(
            "zones.yaml"
        )

        for zone_id, data in config["zones"].items():
            self.zones[zone_id] = Zone(
                zone_id=zone_id,
                name=data["name"],
                device_id=data["device"],
                output=int(data["output"]),
                pixel_count=int(data["pixel_count"]),
            )

    def build_scene(
        self,
        scene_id: str,
        config: dict[str, Any],
    ) -> tuple[Scene, dict]:
        """Build a scene and its independent zone effects."""

        scene = Scene(
            name=config["name"],
            zones=list(config["zones"]),
            effect_config=dict(config["effect"]),
        )

        effects = {
            zone_id: create_effect(scene.effect_config)
            for zone_id in scene.zones
        }

        unknown_zones = set(scene.zones) - set(self.zones)

        if unknown_zones:
            raise ValueError(
                f"Scene '{scene_id}' references unknown zones: "
                f"{unknown_zones}"
            )

        return scene, effects

    def prepare(self, scene_id: str) -> None:
        """Prepare devices and the selected scene."""

        runtime = self._load_config(
            "config.yaml"
        )

        scene_path = (
            self.config_dir
            / "scenes"
            / f"{scene_id}.yaml"
        )

        scene_config = load_yaml(scene_path)

        self.load_devices()
        self.load_zones()

        scene, effects = self.build_scene(
            scene_id,
            scene_config,
        )

        self.controller = LightingController(
            devices=self.devices,
            zones=self.zones,
        )

        engine = SceneEngine()

        engine.activate(
            scene=scene,
            effects=effects,
        )

        safety = runtime.get("safety", {})

        maximum_brightness = float(
            safety.get("maximum_brightness", 1.0)
        )

        if not 0.0 <= maximum_brightness <= 1.0:
            raise ValueError(
                "Maximum brightness must be between 0.0 and 1.0."
            )

        for effect in effects.values():
            if effect.brightness > maximum_brightness:
                effect.brightness = maximum_brightness

        zone_pixel_counts = {
            zone_id: zone.pixel_count
            for zone_id, zone in self.zones.items()
        }

        interval = float(
            runtime.get("runtime", {}).get(
                "update_interval",
                0.10,
            )
        )

        self.scheduler = Scheduler(
            engine=engine,
            controller=self.controller,
            zone_pixel_counts=zone_pixel_counts,
            update_interval=interval,
        )

        for device in self.devices.values():
            device.initialize()

        self.scene = scene

    def run(
        self,
        duration: float | None = 10.0,
    ) -> None:
        """Run the prepared application."""

        if self.scheduler is None:
            raise RuntimeError(
                "Application has not been prepared."
            )

        print()
        print("================================")
        print("       SEASONAL LIGHTS")
        print("================================")
        print(f"Scene: {self.scene.name}")
        print(f"Duration: {duration}")
        print()

        try:
            self.scheduler.run(duration)

        finally:
            for device in self.devices.values():
                device.shutdown()