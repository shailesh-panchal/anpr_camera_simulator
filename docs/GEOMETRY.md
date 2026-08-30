# Geometry Model

## Overview

The geometry model represents the physical world, camera, and projected image plane used to create synthetic license plate frames.

## Coordinate system

The project uses a right-handed world coordinate model:

- X: lateral direction
- Y: vertical direction
- Z: forward along the road axis

The camera sits in the world and looks along the positive Z direction from the camera origin toward the scene.

## Camera pose

The camera pose is represented by:

- x_m
- y_m
- z_m
- pitch_deg

This gives the camera world position and downward pitch relative to the road plane.

## Camera intrinsics

The camera intrinsics are:

- fx
- fy
- cx
- cy

These allow the conversion from 3D camera coordinates to 2D image coordinates using the pinhole camera model.

## Plate geometry

The plate is represented by a rectangle of dimensions:

- width_m
- height_m

The project builds the plate corners around its center and then projects them to the image plane.

## Projection equation

The image coordinates are computed using:

$$

u = fx \cdot \frac{X}{Z} + cx

$$

$$

v = fy \cdot \frac{Y}{Z} + cy

$$

This assumes a simple pinhole camera without lens distortion.

## World-to-camera transform

Before projection, the world point is transformed into camera coordinates using the camera pose and pitch.

This includes:

- translation relative to the camera origin
- pitch rotation around the X axis

The result is a camera-space point with X, Y, Z values that can be projected into the image plane.

## Vehicle state

The vehicle state holds the current world-space position of the vehicle plate center:

- x_m
- y_m
- z_m

The vehicle vertical position is defined by the plate mount height, so the plate remains attached to the vehicle body.

## Important modeling assumptions

- the vehicle moves primarily along the road axis
- the camera is fixed in the world
- the plate is planar and rigid
- no lens distortion is modeled yet
- no multiple lights or shadows are modeled yet

These assumptions keep the system computationally simple and highly explainable.
