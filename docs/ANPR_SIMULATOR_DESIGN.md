# ANPR Simulator Design

## 1. Overview

This project builds a synthetic ANPR (Automatic Number Plate Recognition) data generator. It models a vehicle moving toward or away from a camera, computes the plate geometry in 3D, projects that plate into the camera image plane, and renders a sequence of frames over time.

The design keeps the system modular:

- geometry models the real-world scene
- projection converts the scene into camera coordinates
- rendering composites the visual output
- frame generation advances time according to FPS and vehicle speed

The result is a synthetic video stream suitable for ANPR testing, benchmarking, and dataset generation.

---

## 2. Goals

The simulator is designed to:

- model a vehicle driving along a road in front of a camera
- position a license plate on the vehicle at a fixed physical offset
- project the plate into the camera image using perspective geometry
- generate a sequence of frames at a configurable FPS
- render the visual output into OpenCV images and video files
- support synthetic plate strings, motion directions, and camera setups

---

## 3. High-Level Architecture

The system has four major layers:

### 3.1 Geometry layer

Responsible for all physical placement and projection math.

Main components:

- [src/anpr_simulator/geometry/camera_pose.py](../src/anpr_simulator/geometry/camera_pose.py) — camera position and pitch
- [src/anpr_simulator/geometry/camera_intrinsics.py](../src/anpr_simulator/geometry/camera_intrinsics.py) — pinhole intrinsics
- [src/anpr_simulator/geometry/vehicle_trajectory.py](../src/anpr_simulator/geometry/vehicle_trajectory.py) — motion path over time
- [src/anpr_simulator/geometry/vehicle_state.py](../src/anpr_simulator/geometry/vehicle_state.py) — vehicle state at a timestamp
- [src/anpr_simulator/geometry/license_plate.py](../src/anpr_simulator/geometry/license_plate.py) — plate corners in 3D
- [src/anpr_simulator/geometry/projection.py](../src/anpr_simulator/geometry/projection.py) — point projection math
- [src/anpr_simulator/geometry/transform.py](../src/anpr_simulator/geometry/transform.py) — world-to-camera transform
- [src/anpr_simulator/geometry/plate_projection.py](../src/anpr_simulator/geometry/plate_projection.py) — projected plate geometry

### 3.2 Simulation layer

Responsible for turning time and motion into a sequence of scene states.

Main components:

- [src/anpr_simulator/simulation/scenario.py](../src/anpr_simulator/simulation/scenario.py) — scenario configuration object
- [src/anpr_simulator/simulation/frame_simulator.py](../src/anpr_simulator/simulation/frame_simulator.py) — one-frame simulation
- [src/anpr_simulator/simulation/frame_generator.py](../src/anpr_simulator/simulation/frame_generator.py) — time-based frame generation
- [src/anpr_simulator/simulation/simulation_frame.py](../src/anpr_simulator/simulation/simulation_frame.py) — per-frame result container

### 3.3 Rendering layer

Responsible for turning the projected plate geometry into actual OpenCV images.

Main components:

- [src/anpr_simulator/renderer/opencv_renderer/renderer.py](../src/anpr_simulator/renderer/opencv_renderer/renderer.py) — basic frame creation and background fill
- [src/anpr_simulator/renderer/opencv_renderer/vehicle_render.py](../src/anpr_simulator/renderer/opencv_renderer/vehicle_render.py) — vehicle rectangle rendering
- [src/anpr_simulator/renderer/opencv_renderer/license_plate_render.py](../src/anpr_simulator/renderer/opencv_renderer/license_plate_render.py) — synthetic plate generation and perspective plate rendering

### 3.4 Output layer

Responsible for exporting the generated results as video or frame files.

Main reference:

- [generate_anpr_sequence.py](../generate_anpr_sequence.py)

This script wraps the simulation and rendering pipelines and can export:

- MP4 video
- PNG frames
- YUV420 raw frames

---

## 4. Geometry Model

### 4.1 Camera model

The camera is modeled as a simple pinhole camera with:

- focal length in x and y: fx, fy
- principal point: cx, cy

This is the standard intrinsics model used by OpenCV and projective geometry.

The projection equation is:

$$

u = fx \cdot \frac{X}{Z} + cx

$$

$$

v = fy \cdot \frac{Y}{Z} + cy

$$

where $(X, Y, Z)$ is the point in camera coordinates and $(u, v)$ is the image-plane coordinate.

### 4.2 Camera pose

The camera is mounted at a world-space position:

- x_m = lateral offset
- y_m = height above road
- z_m = longitudinal position along road axis

It also has a pitch angle in degrees.

The transformation from world coordinates to camera coordinates is performed by rotating around the X axis to account for the camera pitch, then projecting with the intrinsics.

### 4.3 Vehicle motion model

The vehicle is treated as moving along the road axis. Its motion is defined by:

- initial distance from camera
- speed in meters per second
- direction: approaching or moving away

At time $t$, the traveled distance is:

$$

d = speed \cdot t

$$

The vehicle position along the camera axis then changes based on its direction.

---

## 5. Plate Modeling

The plate is represented as a planar rectangle with:

- width_m
- height_m

The plate corners are generated in local 3D world coordinates around the vehicle’s plate center.

The plate is mounted on the vehicle at a fixed vertical offset from the road, represented by `license_plate_height_m` in the vehicle dimensions.

This means the plate is effectively attached to the vehicle body, not independently positioned in the frame.

---

## 6. Projection Pipeline

The per-frame projective flow is:

1. Compute vehicle state at the current time
2. Build plate corners in 3D
3. Convert world points to camera coordinates via world-to-camera transform
4. Project camera-space points into image coordinates using the camera intrinsics
5. Produce a `ProjectedPlate` object containing the four projected corners

This is implemented in [src/anpr_simulator/geometry/plate_projection.py](../src/anpr_simulator/geometry/plate_projection.py).

The important result is a 2D quadrilateral that describes the image-space plate boundary.

---

## 7. Rendering Pipeline

The visual pipeline uses the projected plate polygon as the ground truth position of the plate in the frame.

### 7.1 Plate generation

A synthetic plate image is generated in [src/anpr_simulator/renderer/opencv_renderer/license_plate_render.py](../src/anpr_simulator/renderer/opencv_renderer/license_plate_render.py) using OpenCV text rendering.

This creates a flat image with:

- background color
- plate text centered on the canvas

### 7.2 Perspective warp

The flat plate image is warped into the quadrilateral defined by the projected plate corners using OpenCV perspective transforms.

The key operations are:

- `cv2.getPerspectiveTransform(...)`
- `cv2.warpPerspective(...)`
- masking with `cv2.fillConvexPoly(...)`
- `cv2.copyTo(...)`

This makes the plate appear as a real planar object in the camera view, with perspective distortion matching the vehicle pose.

### 7.3 Vehicle rendering

A simple rectangle is rendered for the vehicle body in [src/anpr_simulator/renderer/opencv_renderer/vehicle_render.py](../src/anpr_simulator/renderer/opencv_renderer/vehicle_render.py).

This is intentionally simple but sufficient for a synthetic ANPR front-end test case.

---

## 8. Frame Generation

The frame generator advances time based on the scenario FPS:

$$

t_i = i \cdot \frac{1}{fps}

$$

This is implemented in [src/anpr_simulator/simulation/frame_generator.py](../src/anpr_simulator/simulation/frame_generator.py).

Each generated frame contains:

- frame number
- timestamp
- vehicle state
- projected plate geometry

The generator yields one `SimulationFrame` per timestamp until the configured duration expires.

This keeps the simulation deterministic and easy to test.

---

## 9. Output Formats

The simulator can produce several output forms:

### 9.1 Geometry-only output

SimulationFrame objects are used for analysis and validation without any visual output.

### 9.2 OpenCV image output

A rendered RGB frame is produced by combining:

- background
- vehicle rectangle
- projected plate image

### 9.3 MP4 output

The script [generate_anpr_sequence.py](../generate_anpr_sequence.py) writes the rendered sequence to MP4 using OpenCV `VideoWriter`.

### 9.4 PNG frames

The same script can export each frame as a PNG file.

### 9.5 YUV420 raw frames

The script also supports export of raw YUV420 planar frames in a format that is useful for downstream camera or image-pipeline testing.

---

## 10. Data Flow

The complete execution flow is:

1. User supplies a scenario configuration
2. `FrameGenerator` advances time over the configured duration
3. `simulate_frame(...)` computes the current vehicle state
4. `project_vehicle_plate(...)` computes projected plate corners
5. `render_projected_license_plate(...)` warps the plate into the scene
6. Optional output pipeline writes MP4, PNG, or YUV420 files

This yields a video sequence where the plate scales, shifts, and distorts according to the real camera geometry.

---

## 11. Design Strengths

- clean separation of geometry and rendering
- straightforward implementation of camera projection
- deterministic frame sequence generation
- easy to test with unit tests
- extensible to richer scenes and output pipelines

---

## 12. Limitations and Realism Gaps

This version is intentionally simplified and does not yet include:

- full vehicle 3D mesh
- road lane markings and background scene
- radial distortion and lens calibration
- realistic lighting, occlusion, shadows
- dynamic speed variations
- more complex trajectory models
- environment noise and motion blur

These can be added later without redesigning the overall pipeline.

---

## 13. Recommended Next Upgrades

Ordered by value:

1. road background with lane geometry
2. more realistic vehicle body rendering
3. camera distortion modeling
4. variable vehicle paths and lateral movement
5. frame-level noise, exposure, and motion blur
6. multiple vehicle / plate scenarios in one sequence
7. dataset metadata export alongside generated frames

---

## 14. Summary

The simulator is a well-structured synthetic ANPR generator built around the right projective camera model. It separates physical motion, projection math, and rendering, which makes it easy to reason about and extend.

The most important idea is that the geometry defines where the plate should appear in the camera, and the renderer simply draws that projected plate into the image. This is the correct architectural pattern for a synthetic ANPR video generator.
