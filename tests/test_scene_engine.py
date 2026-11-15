from seasonal_lights.core.scene_engine import SceneEngine
from seasonal_lights.effects.solid import SolidEffect
from seasonal_lights.models.color import Color
from seasonal_lights.models.scene import Scene


def test_scene_engine_generates_zone_frames():
    scene = Scene(
        name="Test Scene",
        zones=["zone_a"],
        effect_config={"type": "solid"},
    )

    effect = SolidEffect(
        color=Color(255, 0, 0),
        brightness=1.0,
    )

    engine = SceneEngine()

    engine.activate(
        scene,
        {
            "zone_a": effect,
        },
    )

    result = engine.update(
        elapsed=0,
        zone_pixel_counts={
            "zone_a": 5,
        },
    )

    assert len(result["zone_a"]) == 5
    assert result["zone_a"][0] == Color(255, 0, 0)


def test_scene_engine_rejects_missing_effect():
    import pytest

    scene = Scene(
        name="Test Scene",
        zones=["zone_a"],
        effect_config={},
    )

    engine = SceneEngine()

    with pytest.raises(ValueError):
        engine.activate(scene, {})