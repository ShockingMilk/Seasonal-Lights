from pathlib import Path

from seasonal_lights import __version__
from seasonal_lights.cli.commands import create_parser
from seasonal_lights.core.application import SeasonalLightsApplication
from seasonal_lights.utils.config import load_yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_DIR = PROJECT_ROOT / "config"


def main() -> None:
    """Application entry point."""

    parser = create_parser()
    args = parser.parse_args()

    config_dir = (
        Path(args.config_dir)
        if args.config_dir
        else DEFAULT_CONFIG_DIR
    )

    config_path = config_dir / "config.yaml"

    if not config_path.exists():
        config_path = config_dir / "config.example.yaml"

    runtime = load_yaml(config_path)

    scene_id = (
        args.scene
        or runtime.get("runtime", {}).get(
            "default_scene",
            "solid_warm",
        )
    )

    duration = (
        None
        if args.duration == 0
        else args.duration
    )

    if args.interval is not None and args.interval <= 0:
        parser.error("--interval must be greater than zero.")

    print(f"Seasonal Lights v{__version__}")

    application = SeasonalLightsApplication(
        config_dir=config_dir,
    )

    application.prepare(
        scene_id=scene_id,
        visual=args.visual,
    )

    if args.interval is not None:
        application.scheduler.update_interval = args.interval

    application.run(duration)


if __name__ == "__main__":
    main()