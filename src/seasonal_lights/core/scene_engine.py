from seasonal_lights.effects.base import LightEffect
from seasonal_lights.models.scene import Scene


class SceneEngine:
    """Generates pixel frames for active scenes."""

    def __init__(self) -> None:
        self.active_scene: Scene | None = None

        self.active_effects: dict[
            str,
            LightEffect
        ] = {}

    def activate(
        self,
        scene: Scene,
        effects: dict[str, LightEffect],
    ) -> None:
        """Activate a scene."""

        if not scene.zones:
            raise ValueError(
                "A scene must contain at least one zone."
            )

        missing = set(scene.zones) - set(effects)

        if missing:
            raise ValueError(
                f"Missing effects for zones: {missing}"
            )

        self.active_scene = scene
        self.active_effects = effects

    def update(
        self,
        elapsed: float,
        zone_pixel_counts: dict[str, int],
    ) -> dict[str, list]:
        """Generate frames for all active zones."""

        if self.active_scene is None:
            return {}

        frames = {}

        for zone_id in self.active_scene.zones:
            if zone_id not in zone_pixel_counts:
                raise ValueError(
                    f"Missing pixel configuration for {zone_id}."
                )

            effect = self.active_effects[zone_id]

            frames[zone_id] = effect.update(
                elapsed=elapsed,
                pixel_count=zone_pixel_counts[zone_id],
            )

        return frames