from seasonal_lights.core.controller import LightingController
from seasonal_lights.core.scene_engine import SceneEngine
from seasonal_lights.utils.timing import monotonic_seconds, sleep


class Scheduler:
    """Runs the active lighting scene."""

    def __init__(
        self,
        engine: SceneEngine,
        controller: LightingController,
        zone_pixel_counts: dict[str, int],
        update_interval: float = 0.10,
    ) -> None:
        if update_interval <= 0:
            raise ValueError(
                "Update interval must be positive."
            )

        self.engine = engine
        self.controller = controller
        self.zone_pixel_counts = zone_pixel_counts
        self.update_interval = update_interval

        self.running = False

    def run(
        self,
        duration: float | None = None,
    ) -> None:
        """Run the lighting engine."""

        if duration is not None and duration < 0:
            raise ValueError(
                "Duration cannot be negative."
            )

        self.running = True
        start = monotonic_seconds()

        try:
            while self.running:
                elapsed = monotonic_seconds() - start

                if duration is not None and elapsed >= duration:
                    break

                frames = self.engine.update(
                    elapsed=elapsed,
                    zone_pixel_counts=self.zone_pixel_counts,
                )

                self.controller.render(frames)

                sleep(self.update_interval)

        except KeyboardInterrupt:
            print("\nStopping lighting engine...")

        finally:
            self.running = False
            self.controller.clear()

    def stop(self) -> None:
        """Request the scheduler to stop."""

        self.running = False