# Architecture

## Purpose

The simulator creates synthetic ANPR sequences by combining a geometric motion model, a perspective camera model, and an OpenCV renderer.

## Layered design

### 1. Geometry layer

This layer describes the physical scene and camera math.

Responsibilities:

- vehicle motion over time
- plate size and placement on the vehicle
- camera pose and intrinsics
- world-to-camera transform
- projection into the image plane

Key files:

- [src/anpr_simulator/geometry/camera_pose.py](../src/anpr_simulator/geometry/camera_pose.py)
- [src/anpr_simulator/geometry/camera_intrinsics.py](../src/anpr_simulator/geometry/camera_intrinsics.py)
- [src/anpr_simulator/geometry/vehicle_trajectory.py](../src/anpr_simulator/geometry/vehicle_trajectory.py)
- [src/anpr_simulator/geometry/vehicle_state.py](../src/anpr_simulator/geometry/vehicle_state.py)
- [src/anpr_simulator/geometry/license_plate.py](../src/anpr_simulator/geometry/license_plate.py)
- [src/anpr_simulator/geometry/projection.py](../src/anpr_simulator/geometry/projection.py)
- [src/anpr_simulator/geometry/transform.py](../src/anpr_simulator/geometry/transform.py)
- [src/anpr_simulator/geometry/plate_projection.py](../src/anpr_simulator/geometry/plate_projection.py)

### 2. Simulation layer

This layer turns a scenario into a sequence of geometry states.

Responsibilities:

- hold scenario parameters
- compute a scene per timestamp
- generate frames at FPS intervals
- expose `SimulationFrame` objects

Key files:

- [src/anpr_simulator/simulation/scenario.py](../src/anpr_simulator/simulation/scenario.py)
- [src/anpr_simulator/simulation/frame_simulator.py](../src/anpr_simulator/simulation/frame_simulator.py)
- [src/anpr_simulator/simulation/frame_generator.py](../src/anpr_simulator/simulation/frame_generator.py)
- [src/anpr_simulator/simulation/simulation_frame.py](../src/anpr_simulator/simulation/simulation_frame.py)

### 3. Rendering layer

This layer converts projected plate geometry into an actual image.

Responsibilities:

- draw the vehicle body
- generate a base plate image with text
- warp the plate to the projected quadrilateral
- composite into a background frame

Key files:

- [src/anpr_simulator/renderer/opencv_renderer/renderer.py](../src/anpr_simulator/renderer/opencv_renderer/renderer.py)
- [src/anpr_simulator/renderer/opencv_renderer/vehicle_render.py](../src/anpr_simulator/renderer/opencv_renderer/vehicle_render.py)
- [src/anpr_simulator/renderer/opencv_renderer/license_plate_render.py](../src/anpr_simulator/renderer/opencv_renderer/license_plate_render.py)

### 4. Output layer

This layer exports generated results for downstream use.

Responsibilities:

- write MP4 videos
- write PNG frames
- write YUV420 raw frame files

Key file:

- [generate_anpr_sequence.py](../generate_anpr_sequence.py)

---

## Data flow

1. User configures a `SimulationScenario`
2. `FrameGenerator` steps through time using FPS
3. `simulate_frame(...)` computes the current vehicle state
4. plate corners are projected into image space
5. `render_projected_license_plate(...)` warps the plate texture
6. output is written as image files or video

---

## Design principles

- Geometry is independent from rendering
- Frame generation is time-driven and deterministic
- Renderers consume projected geometry rather than raw world state
- Each layer has a single responsibility
- Output generation is a thin wrapper around the simulation pipeline

---

## Why this structure works

This architecture keeps the system readable and testable:

- geometry bugs are isolated and easy to validate
- rendering bugs are isolated to the OpenCV layer
- motion and timing issues are isolated to the frame generator
- output generation is not embedded in the core simulation logic

This separation is critical when building realistic synthetic ANPR data.
