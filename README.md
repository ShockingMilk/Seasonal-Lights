# Seasonal Lights

A modular, extensible lighting control platform designed for Raspberry Pi and distributed microcontrollers.

Seasonal Lights is intended to support more than holiday decorations. It provides a flexible system for controlling lighting installations, creating animated scenes, scheduling experiences, and eventually synchronizing lights with audio and projection.

## Project Vision

The project will grow through several stages:

1. POC #1 - Simulated single-zone lighting.
2. POC #2 - Physical single-strand lighting.
3. POC #3 - Multiple strands and lighting zones.
4. POC #4 - Distributed Raspberry Pi Pico controllers.
5. POC #5 - Whole-house lighting.
6. Future - Audio, projector, and synchronized experiences.

## Architecture

The Raspberry Pi acts as the primary application controller.

```text
                  Raspberry Pi 5
                        |
                 Seasonal Lights
                        |
              +---------+---------+
              |                   |
          Scene Engine        Scheduler
              |
          Zone Manager
              |
       Lighting Controller
              |
        Device Interface
              |
        +-----+-----+
        |           |
    Simulator   Hardware
                Adapters
```

The core application does not directly communicate with LED hardware.

Instead, hardware implementations use a common device interface.

## POC #1 Features

- YAML configuration.
- Device definitions.
- Lighting zones.
- Scene definitions.
- RGB color support.
- Brightness control.
- Solid color effect.
- Pulse effect.
- Rainbow effect.
- Simulated LED output.
- Command-line scene selection.
- Automated tests.

No physical lighting hardware is required.

## Requirements

- Python 3.11 or newer.
- Linux recommended.
- Raspberry Pi OS supported.
- Git.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd seasonal-lights
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
pip install -e ".[dev]"
```

## Configuration

Copy the example configurations:

```bash
cp config/config.example.yaml config/config.yaml
cp config/devices.example.yaml config/devices.yaml
cp config/zones.example.yaml config/zones.yaml
```

Example scene files are already available in `config/scenes/`.

The application uses the example configurations when local configuration files are absent.

## Running

Run the default scene:

```bash
seasonal-lights
```

Select a scene:

```bash
seasonal-lights --scene solid_warm
```

Run a rainbow effect for 30 seconds:

```bash
seasonal-lights --scene rainbow --duration 30
```

Run continuously:

```bash
seasonal-lights --scene pulse --duration 0
```

Stop with Ctrl+C.

## Testing

Run:

```bash
pytest
```

## Development

The project is designed around several principles:

- Hardware-independent core.
- Configuration-driven behavior.
- Modular effects.
- Reusable device interfaces.
- Centralized enums.
- Independent lighting zones.
- Testable application components.

## Future Hardware

Potential hardware includes:

- Raspberry Pi 5.
- Raspberry Pi Pico W.
- ESP32.
- WS2812B LED strips.
- SK6812 LED strips.
- Other compatible addressable lighting systems.

## Electrical Safety

The project is intended to control appropriately designed low-voltage lighting systems.

Never connect LED power supplies directly to Raspberry Pi GPIO pins.

Use appropriate power supplies, current protection, wiring, level shifting, and enclosures.

Mains-powered equipment requires suitable isolation and appropriately rated components.

## License

MIT License. See LICENSE.
