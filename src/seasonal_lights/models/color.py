from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    """Represents an RGB color."""

    red: int
    green: int
    blue: int

    def __post_init__(self) -> None:
        for value in self.as_tuple():
            if not 0 <= value <= 255:
                raise ValueError(
                    "RGB values must be between 0 and 255."
                )

    def scale(self, brightness: float) -> "Color":
        """Return a brightness-adjusted color."""

        if not 0.0 <= brightness <= 1.0:
            raise ValueError(
                "Brightness must be between 0.0 and 1.0."
            )

        return Color(
            red=round(self.red * brightness),
            green=round(self.green * brightness),
            blue=round(self.blue * brightness),
        )

    def as_tuple(self) -> tuple[int, int, int]:
        """Return the RGB values."""

        return self.red, self.green, self.blue

    @classmethod
    def black(cls) -> "Color":
        """Return an off color."""

        return cls(0, 0, 0)