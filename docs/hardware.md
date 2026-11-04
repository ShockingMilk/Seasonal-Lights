# Hardware

## POC #1

POC #1 does not require physical hardware.

A simulated controller is used.

## Planned Hardware

The initial physical implementation is expected to use:

- Raspberry Pi
- Pico W
- Addressable LED pixels

## Controller Responsibilities

The Raspberry Pi should eventually handle:

- scene selection
- scheduling
- configuration
- synchronization
- user interface
- projector coordination

Pico-class controllers should handle:

- LED timing
- GPIO
- local output
- sensors
- physical interfaces

## Power

Lighting power should be supplied independently from the Raspberry Pi
or Pico controller.

Do not power a large LED installation directly from GPIO.

Actual power supplies, wiring, fusing, injection points, and connectors
must be selected based on the specific LED hardware and installation.

## Future

Potential controller architecture:

```text
Raspberry Pi
     |
     +---- Pico W
     |       |
     |       +---- Zone
     |
     +---- Pico W
     |       |
     |       +---- Zone
     |
     +---- Pico W
             |
             +---- Zone