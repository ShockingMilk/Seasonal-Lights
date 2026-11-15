from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Scene:
    """Represents a lighting scene."""

    name: str
    zones: list[str]
    effect_config: dict[str, Any]