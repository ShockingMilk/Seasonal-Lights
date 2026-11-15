import argparse


def create_parser() -> argparse.ArgumentParser:
    """Create application command-line arguments."""

    parser = argparse.ArgumentParser(
        prog="seasonal-lights",
        description="Seasonal Lights control system.",
    )

    parser.add_argument(
        "--scene",
        default=None,
        help="Scene to run.",
    )

    parser.add_argument(
        "--duration",
        type=float,
        default=10.0,
        help="Runtime in seconds. Use 0 for continuous operation.",
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=None,
        help="Override the configured update interval.",
    )

    parser.add_argument(
        "--config-dir",
        type=str,
        default=None,
        help="Path to the configuration directory.",
    )

    return parser