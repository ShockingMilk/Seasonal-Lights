import pytest

from seasonal_lights.models.color import Color


def test_color_creation():
    color = Color(255, 100, 50)

    assert color.as_tuple() == (255, 100, 50)


def test_color_rejects_invalid_values():
    with pytest.raises(ValueError):
        Color(256, 0, 0)


def test_color_scaling():
    color = Color(200, 100, 50)

    result = color.scale(0.5)

    assert result == Color(100, 50, 25)


def test_black_color():
    assert Color.black() == Color(0, 0, 0)