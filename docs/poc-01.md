# POC #1 - Simulated Lighting

## Objective

Demonstrate the complete lighting-control pipeline without requiring physical lighting hardware.

## Supported Features

- RGB color model.
- Configurable brightness.
- Lighting zones.
- Device definitions.
- Scene definitions.
- Solid color effect.
- Pulse effect.
- Rainbow effect.
- Simulated pixel output.
- Command-line execution.
- Automated tests.

## Pipeline

```text
YAML Configuration
        |
        v
      Scene
        |
        v
     Effects
        |
        v
   Scene Engine
        |
        v
 Lighting Controller
        |
        v
 Simulator Device
```

## Excluded Features

POC #1 intentionally excludes:

- GPIO.
- WS2812 hardware.
- Pico W firmware.
- Network communication.
- Web interface.
- Date-based scheduling.
- Audio synchronization.
- Projector control.

## Success Criteria

POC #1 is complete when:

1. The application installs on Linux.
2. The application runs without physical hardware.
3. Automated tests pass.
4. Scenes can be selected through the CLI.
5. Effects generate pixel frames.
6. Device outputs receive pixel frames.
7. Brightness limits are enforced.
8. Device-specific code remains isolated.
9. Additional effects can be introduced independently.
10. Configuration can be changed without modifying application code.

## Next Phase

POC #2 will introduce a physical addressable LED strand.

The existing device interface will be extended to support physical LED hardware.

The scene engine and effects should not need to be rewritten.
