# Development Guide

## Requirements

- Python 3.11+
- Git
- Linux recommended

## Initial Setup

Clone the repository:

```bash
git clone <repository-url>
cd seasonal-lights
```

Create the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install:

```bash
pip install -e ".[dev]"
```

## Run

```bash
seasonal-lights
```

## Run Tests

```bash
pytest
```

## Development Principles

### Hardware isolation

Do not place GPIO or LED-library implementation inside:

- Core.
- Effects.
- Models.
- Configuration utilities.

Hardware-specific code belongs in devices.

### Configuration first

If a setting can reasonably be changed without modifying Python code, prefer configuration.

### Independent effects

Effects should not know:

- Which holiday is being celebrated.
- Which house is being controlled.
- Which controller is being used.
- Which GPIO pin is connected.

### Lightweight dependencies

Avoid unnecessary dependencies.

The core application should remain lightweight enough to run comfortably on a Raspberry Pi.

### Hardware-independent testing

Use the simulator for development and testing.

Physical hardware should not be required to contribute to the core application.
