# Development

## Python Version

Python 3.11 or newer.

## Virtual Environment

Create:

```bash
python3 -m venv .venv

Activate:

source .venv/bin/activate

Install:

pip install -r requirements.txt
pip install -e .
Run
python -m seasonal_lights.main
Tests
pytest
Design Rules
Do
Keep hardware-specific code in devices.
Keep effects independent of hardware.
Keep deployment configuration outside source code.
Add new device types through the device abstraction.
Add new effects through the effect abstraction.
Keep enums centralized.
Avoid

Do not place hardware-specific logic in the scene engine.

Avoid:

if device == "pico":

inside scene or effect code.

Prefer:

Scene Engine
    |
LightingDevice
    |
PicoDevice

This allows hardware to change without changing scenes.

Git

Do not commit:

private configuration
credentials
local IP addresses
generated logs
runtime data