# Seasonal Lights Architecture

## Overview

Seasonal Lights uses a modular architecture.

The application separates configuration, scene management, effects, devices, and hardware implementation.

## Architecture Flow

```text
                  Configuration
                        |
                        v
                     Models
                        |
                        v
                   Scene Engine
                        |
                        v
                     Effects
                        |
                        v
                Lighting Controller
                        |
                        v
                 Device Interface
                        |
             +----------+----------+
             |                     |
         Simulator             Hardware
                               Adapters
```

## Configuration

Configuration defines:

- Application settings.
- Devices.
- Zones.
- Scenes.
- Brightness limits.
- Runtime behavior.

Configuration should not contain implementation logic.

## Models

Models describe application objects.

Examples:

- Color
- Device
- Zone
- Scene

## Core

The core package coordinates the application.

It is responsible for:

- Preparing devices.
- Loading scenes.
- Activating effects.
- Rendering frames.
- Scheduling updates.

## Effects

Effects generate pixel frames.

They do not communicate with hardware.

An effect should not know which controller or physical lighting system will display its output.

## Devices

Devices implement the common LightingDevice interface.

Examples:

- Simulator.
- Raspberry Pi local output.
- Raspberry Pi Pico.
- ESP32.

## Zones

A zone represents a logical group of lights.

Examples:

- Front roof.
- Garage.
- Porch.
- Windows.
- Trees.
- Walkway.

Zones reference device outputs.

## Scenes

Scenes define which zones participate and which effects are applied.

Scenes should remain independent of hardware.

## Future Distributed Architecture

```text
                   Raspberry Pi 5
                         |
                   Scene Engine
                         |
                   Network Layer
                         |
             +-----------+-----------+
             |           |           |
           Pico W      Pico W      Pico W
             |           |           |
           Roof        Porch      Garage
```

The Pi handles orchestration.

Each microcontroller handles its own local hardware timing.
