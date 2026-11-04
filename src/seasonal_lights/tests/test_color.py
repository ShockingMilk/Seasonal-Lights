import pytest

from seasonal_lights.models.color import Color


def test_color_creation() -> None:
    color = Color(255, 128, 0)

    assert color.red == 255
    assert color.green == 128
    assert color.blue == 0


def test_color_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        Color(256, 0, 0)


def test_color_scaling() -> None:
    color = Color(200, 100, 50)

    scaled = color.scaled(0.5)

    assert scaled == Color(100, 50, 25)