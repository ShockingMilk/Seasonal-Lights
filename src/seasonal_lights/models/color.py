"""Color model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    """Represents an RGB color."""

    red: int
    green: int
    blue: int

    def __post_init__(self) -> None:
        """Validate RGB values."""

        for name, value in (
            ("red", self.red),
            ("green", self.green),
            ("blue", self.blue),
        ):
            if not 0 <= value <= 255:
                raise ValueError(
                    f"{name} must be between 0 and 255, got {value}"
                )

    def scaled(self, brightness: float) -> "Color":
        """Return the color scaled by a brightness value."""

        brightness = max(0.0, min(1.0, brightness))

        return Color(
            red=round(self.red * brightness),
            green=round(self.green * brightness),
            blue=round(self.blue * brightness),
        )

    def as_tuple(self) -> tuple[int, int, int]:
        """Return the color as an RGB tuple."""

        return self.red, self.green, self.blue