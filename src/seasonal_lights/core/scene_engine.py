"""Scene execution engine."""

from seasonal_lights.core.controller import ControllerManager
from seasonal_lights.effects import (
    LightEffect,
    PulseEffect,
    RainbowEffect,
    SolidEffect,
)
from seasonal_lights.enums import EffectType
from seasonal_lights.models import SceneConfig, ZoneConfig


class SceneEngine:
    """Coordinates scenes, zones, effects, and controllers."""

    def __init__(
        self,
        controllers: ControllerManager,
        zones: dict[str, ZoneConfig],
    ) -> None:
        self.controllers = controllers
        self.zones = zones

    def create_effect(
        self,
        scene: SceneConfig,
    ) -> LightEffect:
        """Create the appropriate effect for a scene."""

        config = scene.effect

        match config.effect_type:
            case EffectType.SOLID:
                return SolidEffect(
                    color=config.color,
                    brightness=config.brightness,
                )

            case EffectType.PULSE:
                return PulseEffect(
                    color=config.color,
                    brightness=config.brightness,
                    speed=config.speed,
                )

            case EffectType.RAINBOW:
                return RainbowEffect(
                    brightness=config.brightness,
                    speed=config.speed,
                )

            case _:
                raise ValueError(
                    f"Unsupported effect: {config.effect_type}"
                )

    def render_scene(
        self,
        scene: SceneConfig,
        elapsed: float,
    ) -> None:
        """Render a scene to all of its zones."""

        effect = self.create_effect(scene)

        for zone_id in scene.zones:
            zone = self._get_zone(zone_id)

            device = self.controllers.get(
                zone.controller_id
            )

            pixels = effect.render(
                pixel_count=zone.pixel_count,
                elapsed=elapsed,
            )

            device.set_pixels(
                output=zone.output,
                pixels=pixels,
            )

            device.show(zone.output)

    def _get_zone(
        self,
        zone_id: str,
    ) -> ZoneConfig:
        """Retrieve a zone by ID."""

        try:
            return self.zones[zone_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown lighting zone: {zone_id}"
            ) from exc