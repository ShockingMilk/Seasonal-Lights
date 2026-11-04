"""Scene configuration models."""

from dataclasses import dataclass, field

from seasonal_lights.enums import EffectType
from seasonal_lights.models.color import Color


@dataclass(frozen=True)
class EffectConfig:
    """Configuration for an individual effect."""

    effect_type: EffectType
    color: Color = field(
        default_factory=lambda: Color(255, 255, 255)
    )
    brightness: float = 1.0
    speed: float = 1.0

    def __post_init__(self) -> None:
        """Validate effect configuration."""

        if not 0.0 <= self.brightness <= 1.0:
            raise ValueError("brightness must be between 0 and 1")

        if self.speed < 0:
            raise ValueError("speed cannot be negative")


@dataclass(frozen=True)
class SceneConfig:
    """Configuration describing a lighting scene."""

    scene_id: str
    name: str
    zones: list[str]
    effect: EffectConfig

    def __post_init__(self) -> None:
        """Validate scene configuration."""

        if not self.scene_id:
            raise ValueError("scene_id cannot be empty")

        if not self.zones:
            raise ValueError("scene must contain at least one zone")