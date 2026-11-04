"""YAML configuration loading."""

from pathlib import Path
from typing import Any

import yaml

from seasonal_lights.enums import DeviceType, EffectType
from seasonal_lights.models import (
    Color,
    DeviceConfig,
    EffectConfig,
    SceneConfig,
    ZoneConfig,
)


def _load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file."""

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data or {}


def load_devices(path: Path) -> dict[str, DeviceConfig]:
    """Load device configurations."""

    data = _load_yaml(path)

    devices: dict[str, DeviceConfig] = {}

    for device_id, config in data.get("devices", {}).items():
        devices[device_id] = DeviceConfig(
            device_id=device_id,
            name=config["name"],
            device_type=DeviceType(config["type"]),
            outputs=int(config["outputs"]),
        )

    return devices


def load_zones(path: Path) -> dict[str, ZoneConfig]:
    """Load zone configurations."""

    data = _load_yaml(path)

    zones: dict[str, ZoneConfig] = {}

    for zone_id, config in data.get("zones", {}).items():
        zones[zone_id] = ZoneConfig(
            zone_id=zone_id,
            name=config["name"],
            controller_id=config["controller"],
            output=int(config["output"]),
            pixel_count=int(config["pixel_count"]),
        )

    return zones


def load_scenes(path: Path) -> dict[str, SceneConfig]:
    """Load scene configurations."""

    data = _load_yaml(path)

    scenes: dict[str, SceneConfig] = {}

    for scene_id, config in data.get("scenes", {}).items():

        effect_data = config["effect"]

        color_data = effect_data.get(
            "color",
            {"red": 255, "green": 255, "blue": 255},
        )

        color = Color(
            red=int(color_data["red"]),
            green=int(color_data["green"]),
            blue=int(color_data["blue"]),
        )

        effect = EffectConfig(
            effect_type=EffectType(effect_data["type"]),
            color=color,
            brightness=float(
                effect_data.get("brightness", 1.0)
            ),
            speed=float(
                effect_data.get("speed", 1.0)
            ),
        )

        scenes[scene_id] = SceneConfig(
            scene_id=scene_id,
            name=config["name"],
            zones=list(config["zones"]),
            effect=effect,
        )

    return scenes