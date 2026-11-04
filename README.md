# Seasonal Lights

A modular, hardware-independent lighting control platform designed for
seasonal lighting, events, synchronized shows, and future multimedia
experiences.

The project is designed to grow from a single strand of addressable LEDs
into a distributed lighting system capable of controlling multiple zones,
controllers, projectors, and other devices.

## Project Goals

- Start with a single strand of lights.
- Support multiple strands and zones.
- Support multiple lighting controllers.
- Keep hardware-specific code separate from the lighting engine.
- Support different occasions and themes.
- Minimize unnecessary power consumption.
- Eventually support synchronized projectors and multimedia.
- Remain suitable for Raspberry Pi and Pico-class hardware.
- Keep deployment-specific configuration outside the source code.

## Current Status

POC #1.

POC #1 provides:

- A simulated lighting controller.
- A virtual LED strand.
- Configurable zones.
- Configurable scenes.
- Solid color effects.
- Pulse effects.
- Rainbow effects.
- A hardware-independent controller interface.
- Basic automated tests.

No physical lighting hardware is required.

## Architecture

```text
                    Seasonal Lights
                          |
                    Scene Engine
                          |
                   Effect Generator
                          |
                   Controller API
                          |
                +---------+---------+
                |                   |
             Simulator           Pico W
                |                 Future
                |
             LED Strand

The simulator implements the same controller interface that future physical
controllers will implement.

Requirements
Python 3.11+
pip
Linux, macOS, or Windows

Raspberry Pi OS is supported.

Installation

Clone the repository:

git clone <your-repository-url>
cd seasonal-lights

Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Install the project in editable mode:

pip install -e .
Running POC #1
python -m seasonal_lights.main

Or:

./scripts/run.sh

The simulator will display the current virtual LED state in the terminal.

Configuration

Example configuration files are located in:

config/

The example files are safe to commit to GitHub.

Machine-specific configuration should not be committed.

Future Development

Planned progression:

Single simulated strand
Single physical strand
Multiple strands
Multiple zones
Pico W controllers
Distributed synchronization
Whole-house lighting
Scheduling
Audio synchronization
Projector synchronization
Multimedia experiences
Design Principle

Scenes describe what should happen.

Controllers describe where the lights physically exist.

Effects describe how the lights behave.

Hardware drivers describe how commands reach the hardware.

These concerns should remain separate.