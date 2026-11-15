from typing import Any

from seasonal_lights.effects.base import LightEffect
from seasonal_lights.effects.pulse import PulseEffect
from seasonal_lights.effects.rainbow import RainbowEffect
from seasonal_lights.effects.solid import SolidEffect
from seasonal_lights.enums.lighting import EffectType
from seasonal_lights.models.color import Color
from seasonal_lights.utils.switch import switch


def create_effect(
    config: dict[str, Any],
) -> LightEffect:
    """Create an effect using its configuration."""

    effect_type = EffectType(config["type"])

    brightness = float(
        config.get("brightness", 1.0)
    )

    speed = float(
        config.get("speed", 1.0)
    )

    color_data = config.get("color")

    color = None

    if color_data is not None:
        color = Color(
            red=int(color_data["r"]),
            green=int(color_data["g"]),
            blue=int(color_data["b"]),
        )

    return switch(
        effect_type,
        {
            EffectType.SOLID: lambda: _create_solid(
                color,
                brightness,
            ),

            EffectType.PULSE: lambda: _create_pulse(
                color,
                brightness,
                speed,
            ),

            EffectType.RAINBOW: lambda: RainbowEffect(
                brightness=brightness,
                speed=speed,
            ),
        },
    )


def _create_solid(
    color: Color | None,
    brightness: float,
) -> SolidEffect:
    if color is None:
        raise ValueError(
            "Solid effect requires a color."
        )

    return SolidEffect(
        color=color,
        brightness=brightness,
    )


def _create_pulse(
    color: Color | None,
    brightness: float,
    speed: float,
) -> PulseEffect:
    if color is None:
        raise ValueError(
            "Pulse effect requires a color."
        )

    return PulseEffect(
        color=color,
        brightness=brightness,
        speed=speed,
    )