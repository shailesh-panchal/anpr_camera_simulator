# Frame Generation

## Purpose

The simulation produces a sequence of frames over time, aligned with the requested FPS and vehicle motion model.

## Time stepping

The generator advances time using:

$$

\Delta t = \frac{1}{fps}

$$

This creates a regular sample sequence for the simulated camera.

## Generator behavior

The frame generator:

- starts at $t = 0$
- computes the vehicle state at each timestamp
- projects the plate into the image plane
- yields a `SimulationFrame`

Main file:

- [src/anpr_simulator/simulation/frame_generator.py](../src/anpr_simulator/simulation/frame_generator.py)

## Simulation frame

Each frame stores:

- frame number
- timestamp in seconds
- vehicle state
- projected plate geometry

Main file:

- [src/anpr_simulator/simulation/simulation_frame.py](../src/anpr_simulator/simulation/simulation_frame.py)

## Real frame rendering

The generator also includes a rendered-frame path that creates actual OpenCV images for each simulated frame.

This is useful for generating:

- output video
- per-frame PNGs
- raw YUV420 exports

## Important property

The physical distance movement during the sequence is determined by vehicle speed, independent of FPS sampling density. The pixel projection changes as the vehicle approaches or moves away, while the underlying physical motion remains consistent.

## Example behavior

For a vehicle moving at 10 m/s and an FPS of 30, each frame advances the vehicle by approximately:

$$

\frac{10}{30} = 0.333\dots \text{ meters per frame}

$$

This is the correct simulation of temporal motion at the configured sample rate.
