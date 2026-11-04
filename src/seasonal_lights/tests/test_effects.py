from seasonal_lights.effects import (
    PulseEffect,
    RainbowEffect,
    SolidEffect,
)
from seasonal_lights.models.color import Color


def test_solid_effect() -> None:
    effect = SolidEffect(
        color=Color(255, 0, 0),
        brightness=0.5,
    )

    pixels = effect.render(
        pixel_count=5,
        elapsed=0,
    )

    assert len(pixels) == 5
    assert all(
        pixel == Color(128, 0, 0)
        for pixel in pixels
    )


def test_pulse_effect_returns_correct_pixel_count() -> None:
    effect = PulseEffect(
        color=Color(255, 0, 0),
        brightness=1.0,
        speed=1.0,
    )

    pixels = effect.render(
        pixel_count=10,
        elapsed=0,
    )

    assert len(pixels) == 10


def test_rainbow_effect_returns_correct_pixel_count() -> None:
    effect = RainbowEffect(
        brightness=0.5,
        speed=1.0,
    )

    pixels = effect.render(
        pixel_count=20,
        elapsed=0,
    )

    assert len(pixels) == 20