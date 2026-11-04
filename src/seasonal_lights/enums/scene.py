"""Scene-related enumerations."""

from enum import StrEnum


class SceneState(StrEnum):
    """Current state of a scene."""

    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"