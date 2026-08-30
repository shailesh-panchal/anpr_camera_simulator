# Rendering Model

## Purpose

The rendering layer converts the projected plate geometry into an actual image sequence.

## Components

### Renderer base

The base renderer creates an empty image and background fill.

Key file:

- [src/anpr_simulator/renderer/opencv_renderer/renderer.py](../src/anpr_simulator/renderer/opencv_renderer/renderer.py)

### Vehicle rendering

The vehicle body is rendered as a filled rectangle in the image plane.

Key file:

- [src/anpr_simulator/renderer/opencv_renderer/vehicle_render.py](../src/anpr_simulator/renderer/opencv_renderer/vehicle_render.py)

### Plate rendering

The plate is generated as an image with centered text, then transformed to the projected quadrilateral.

Key file:

- [src/anpr_simulator/renderer/opencv_renderer/license_plate_render.py](../src/anpr_simulator/renderer/opencv_renderer/license_plate_render.py)

## Plate generation

The synthetic license plate is created with OpenCV text drawing. This produces a clean image suitable for ANPR-style rendering.

## Perspective warping

The projected polygon from the camera model is used as the destination quadrilateral for the plate texture.

The process is:

1. create source points from the plate image corners
2. create destination points from the projected plate polygon
3. compute a perspective transform
4. warp the plate image
5. mask and composite onto the final frame

This preserves the real perspective look of the plate in the image.

## Output

The rendered frame is a standard OpenCV BGR image.

This image can then be:

- saved as PNG
- saved as a video frame in MP4
- converted to YUV420 raw

## Limitation

The current renderer is intentionally simple. It does not include road textures, vehicle contours, shadows, or special lighting effects.
