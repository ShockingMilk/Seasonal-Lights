"""Application entry point."""

from seasonal_lights.core.system import LightingSystem


def main() -> None:
    """Start the Seasonal Lights application."""

    system = LightingSystem.from_example_configuration()

    print("Seasonal Lights")
    print("================")
    print("POC #1 - Simulator")
    print()

    system.run_demo()


if __name__ == "__main__":
    main()