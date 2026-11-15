from pathlib import Path

import pytest
import yaml

from seasonal_lights.utils.config import load_yaml


def test_load_yaml(tmp_path: Path):
    config_file = tmp_path / "test.yaml"

    config_file.write_text(
        "name: Seasonal Lights\n",
        encoding="utf-8",
    )

    result = load_yaml(config_file)

    assert result["name"] == "Seasonal Lights"


def test_load_yaml_missing_file():
    with pytest.raises(FileNotFoundError):
        load_yaml(Path("missing.yaml"))


def test_load_yaml_invalid_mapping(tmp_path: Path):
    config_file = tmp_path / "invalid.yaml"

    config_file.write_text(
        "- item1\n- item2\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_yaml(config_file)