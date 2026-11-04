# Architecture

## Overview

Seasonal Lights separates the system into several layers.

```text
Configuration
     |
     v
Models
     |
     v
Scene Engine
     |
     +---- Effects
     |
     v
Controller Interface
     |
     +---- Simulator
     |
     +---- Raspberry Pi
     |
     +---- Pico W

Configuration

Configuration describes the deployment.

It should not contain application logic.

Examples:

device IDs
zone IDs
pixel counts
controller assignments
scene definitions
Models

Models represent system objects.

Examples:

Color
DeviceConfig
ZoneConfig
SceneConfig
Effects

Effects generate pixel states.

Examples:

Solid
Pulse
Rainbow

Effects should not know how pixels are physically transmitted.

Devices

Devices transmit pixel states.

The LightingDevice interface defines the contract.

A physical Pico controller can eventually implement the same interface.

Scene Engine

The scene engine connects:

Scene
  |
  +-- Zone
  |
  +-- Effect
  |
  +-- Controller

This allows scenes to remain independent of physical hardware.

Future Architecture

Eventually:

                    Scene Engine
                         |
                Experience Engine
                         |
          +--------------+--------------+
          |              |              |
        Lights         Audio        Projector
          |              |              |
       Pico W           Pi         HDMI/Network