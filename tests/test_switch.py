import pytest

from seasonal_lights.utils.switch import switch


def test_switch_selects_correct_case():
    result = switch(
        "red",
        {
            "red": lambda: "selected red",
            "blue": lambda: "selected blue",
        },
    )

    assert result == "selected red"


def test_switch_uses_default():
    result = switch(
        "green",
        {
            "red": lambda: "red",
        },
        default=lambda: "default",
    )

    assert result == "default"


def test_switch_raises_without_matching_case():
    with pytest.raises(ValueError):
        switch(
            "green",
            {
                "red": lambda: "red",
            },
        )