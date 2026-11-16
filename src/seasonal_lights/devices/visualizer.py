from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from seasonal_lights.devices.simulator import SimulatorDevice
    from seasonal_lights.models.zone import Zone


class SimulationDashboard:
    """Graphical dashboard for all simulated lighting devices."""

    def __init__(
        self,
        devices: dict[str, SimulatorDevice],
        zones: dict[str, Zone],
        title: str = "Seasonal Lights Simulator",
    ) -> None:
        try:
            import pygame
        except ImportError as exc:
            raise RuntimeError(
                "The graphical simulator requires Pygame. "
                'Install it with: pip install -e ".[dev,visual]"'
            ) from exc

        self.pygame = pygame
        self.devices = devices
        self.zones = zones
        self.title = title

        self.width = 1200
        self.height = 800

        self.background = (24, 27, 33)
        self.panel = (38, 43, 52)
        self.text_color = (235, 238, 242)
        self.muted_color = (160, 170, 182)

        self.zone_colors = [
            (90, 160, 255),
            (100, 210, 150),
            (245, 175, 80),
            (190, 130, 235),
            (240, 115, 140),
            (90, 205, 205),
            (210, 210, 100),
            (150, 160, 220),
        ]

        self.zone_color_map = {
            zone_id: self.zone_colors[index % len(self.zone_colors)]
            for index, zone_id in enumerate(sorted(zones))
        }

        self.scroll_offset = 0
        self.content_height = 0
        self.running = False

        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.RESIZABLE,
        )

        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "dejavusans",
            18,
        )

        self.small_font = pygame.font.SysFont(
            "dejavusans",
            14,
        )

        self.running = True

    @property
    def is_running(self) -> bool:
        return self.running

    def update(self) -> bool:
        """Process events and redraw the dashboard."""

        if not self.running:
            return False

        pygame = self.pygame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                self.width = max(700, event.w)
                self.height = max(500, event.h)

                self.screen = pygame.display.set_mode(
                    (self.width, self.height),
                    pygame.RESIZABLE,
                )

            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= event.y * 45

        if not self.running:
            return False

        self._draw()

        self.clock.tick(60)

        return True

    def _draw(self) -> None:
        pygame = self.pygame

        self.screen.fill(self.background)

        header_height = 72
        footer_height = 34

        self._draw_header(header_height)

        content_rect = pygame.Rect(
            0,
            header_height,
            self.width,
            self.height - header_height - footer_height,
        )

        self.screen.set_clip(content_rect)

        y = header_height + 16 - self.scroll_offset

        for device_id, device in self.devices.items():
            for output in range(device.outputs):
                y = self._draw_output(
                    device_id=device_id,
                    device=device,
                    output=output,
                    y=y,
                    content_rect=content_rect,
                )

        self.content_height = (
            y + self.scroll_offset - header_height
        )

        self.screen.set_clip(None)

        maximum_scroll = max(
            0,
            self.content_height - content_rect.height,
        )

        self.scroll_offset = max(
            0,
            min(self.scroll_offset, maximum_scroll),
        )

        self._draw_footer(footer_height)

        pygame.display.flip()

    def _draw_header(self, header_height: int) -> None:
        pygame = self.pygame

        pygame.draw.rect(
            self.screen,
            self.panel,
            (0, 0, self.width, header_height),
        )

        title = self.font.render(
            "SEASONAL LIGHTS",
            True,
            self.text_color,
        )

        subtitle = self.small_font.render(
            "Live output simulation",
            True,
            self.muted_color,
        )

        self.screen.blit(title, (22, 12))
        self.screen.blit(subtitle, (22, 42))

        device_count = len(self.devices)

        output_count = sum(
            device.outputs
            for device in self.devices.values()
        )

        pixel_capacity = sum(
            device.outputs * device.pixels_per_output
            for device in self.devices.values()
        )

        status = (
            f"Devices: {device_count}   "
            f"Outputs: {output_count}   "
            f"Pixel capacity: {pixel_capacity}"
        )

        status_surface = self.small_font.render(
            status,
            True,
            self.muted_color,
        )

        self.screen.blit(
            status_surface,
            (
                max(22, self.width - status_surface.get_width() - 22),
                27,
            ),
        )

    def _draw_output(
        self,
        device_id: str,
        device: SimulatorDevice,
        output: int,
        y: int,
        content_rect,
    ) -> int:
        pygame = self.pygame

        margin = 20
        card_x = margin
        card_width = self.width - margin * 2

        pixels = device.pixels[output]

        columns = max(
            1,
            min(80, (card_width - 40) // 14),
        )

        rows = (
            len(pixels) + columns - 1
        ) // columns

        tile_size = 10
        tile_spacing = 4
        grid_height = rows * (tile_size + tile_spacing)

        zones = [
            zone
            for zone in self.zones.values()
            if zone.device_id == device_id
            and zone.output == output
        ]

        zone_height = 24

        card_height = (
            48
            + zone_height
            + grid_height
            + 18
        )

        card_rect = pygame.Rect(
            card_x,
            y,
            card_width,
            card_height,
        )

        if card_rect.colliderect(content_rect):
            pygame.draw.rect(
                self.screen,
                self.panel,
                card_rect,
                border_radius=10,
            )

            label = self.font.render(
                f"{device.name}  |  Output {output}",
                True,
                self.text_color,
            )

            self.screen.blit(
                label,
                (card_x + 16, y + 10),
            )

            zone_text = self._zone_description(zones)

            zone_surface = self.small_font.render(
                zone_text,
                True,
                self.muted_color,
            )

            self.screen.blit(
                zone_surface,
                (card_x + 16, y + 34),
            )

            grid_x = card_x + 18
            grid_y = y + 48 + zone_height

            for pixel_index, color in enumerate(pixels):
                row = pixel_index // columns
                column = pixel_index % columns

                x = grid_x + column * (
                    tile_size + tile_spacing
                )

                pixel_y = grid_y + row * (
                    tile_size + tile_spacing
                )

                rect = pygame.Rect(
                    x,
                    pixel_y,
                    tile_size,
                    tile_size,
                )

                pygame.draw.rect(
                    self.screen,
                    color.as_tuple(),
                    rect,
                    border_radius=2,
                )

                zone = self._find_zone(
                    zones,
                    pixel_index,
                )

                if zone is not None:
                    pygame.draw.rect(
                        self.screen,
                        self.zone_color_map[zone.zone_id],
                        rect,
                        width=1,
                        border_radius=2,
                    )

        return y + card_height + 14

    def _zone_description(self, zones: list[Zone]) -> str:
        if not zones:
            return "No configured zones"

        descriptions = []

        for zone in sorted(
            zones,
            key=lambda item: item.pixel_start,
        ):
            end = zone.pixel_end - 1

            descriptions.append(
                f"{zone.name}: {zone.pixel_start}-{end}"
            )

        return "   |   ".join(descriptions)

    @staticmethod
    def _find_zone(
        zones: list[Zone],
        pixel_index: int,
    ) -> Zone | None:
        for zone in zones:
            if (
                zone.pixel_start
                <= pixel_index
                < zone.pixel_end
            ):
                return zone

        return None

    def _draw_footer(self, footer_height: int) -> None:
        pygame = self.pygame

        y = self.height - footer_height

        pygame.draw.rect(
            self.screen,
            self.panel,
            (0, y, self.width, footer_height),
        )

        message = self.small_font.render(
            "Scroll to view more outputs and LEDs  |  "
            "Close the window to stop the simulation",
            True,
            self.muted_color,
        )

        self.screen.blit(
            message,
            (18, y + 9),
        )

    def close(self) -> None:
        """Close the graphical dashboard."""

        if self.running:
            self.running = False

        self.pygame.quit()