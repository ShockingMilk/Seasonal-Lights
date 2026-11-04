# Effects

Effects generate the current state of a lighting zone.

Every effect implements:

```python
render(pixel_count, elapsed)

and returns:

list[Color]
Current Effects
Solid

Every pixel receives the same color.

Pulse

Brightness changes smoothly over time.

Rainbow

A moving hue gradient is generated across the strand.

Adding an Effect

Create a new file under:

src/seasonal_lights/effects/

Subclass:

LightEffect

Implement:

render(
    pixel_count,
    elapsed,
)

The effect should not directly communicate with hardware.

This keeps effects reusable across:

simulator
Raspberry Pi
Pico
future controllers