from seasonal_lights.effects.factory import create_effect
from seasonal_lights.effects.pulse import PulseEffect
from seasonal_lights.effects.rainbow import RainbowEffect
from seasonal_lights.effects.solid import SolidEffect
from seasonal_lights.models.color import Color


def test_solid_effect():
    effect = SolidEffect(
        color=Color(255, 0, 0),
        brightness=0.5,
    )

    pixels = effect.update(0, 10)

    assert len(pixels) == 10
    assert pixels[0] == Color(128, 0, 0)


def test_pulse_effect():
    effect = PulseEffect(
        color=Color(255, 0, 0),
        brightness=1.0,
        speed=1.0,
    )

    pixels = effect.update(0, 10)

    assert len(pixels) == 10
    assert pixels[0] == Color(128, 0, 0)


def test_rainbow_effect():
    effect = RainbowEffect(
        brightness=0.5,
        speed=1.0,
    )

    pixels = effect.update(0, 30)

    assert len(pixels) == 30
    assert len(set(pixels)) > 1


def test_effect_factory():
    effect = create_effect(
        {
            "type": "solid",
            "color": {
                "r": 255,
                "g": 0,
                "b": 0,
            },
            "brightness": 1.0,
        }
    )

    assert isinstance(effect, SolidEffect)


def test_effect_factory_rejects_unknown_effect():
    import pytest

    with pytest.raises(ValueError):
        create_effect(
            {
                "type": "unknown",
            }
        )