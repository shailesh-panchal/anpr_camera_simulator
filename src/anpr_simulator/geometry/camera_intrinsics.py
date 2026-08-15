from dataclasses import dataclass

from anpr_simulator.geometry.camera_model import (
    focal_length_pixels,
)


@dataclass(frozen=True)
class CameraIntrinsics:
    """
    Pinhole camera intrinsic parameters.

    Attributes:
        fx: Focal length in pixels along X axis.
        fy: Focal length in pixels along Y axis.
        cx: Principal point X coordinate.
        cy: Principal point Y coordinate.
    """

    fx: float
    fy: float
    cx: float
    cy: float


def create_camera_intrinsics(
    focal_length_mm: float,
    active_pixel_width: int,
    active_pixel_height: int,
    active_area_width_mm: float,
    active_area_height_mm: float,
) -> CameraIntrinsics:

    if focal_length_mm <= 0:
        raise ValueError(
            "Focal length must be greater than 0"
        )

    if active_pixel_width <= 0:
        raise ValueError(
            "Active pixel width must be greater than 0"
        )

    if active_pixel_height <= 0:
        raise ValueError(
            "Active pixel height must be greater than 0"
        )

    if active_area_width_mm <= 0:
        raise ValueError(
            "Active sensor width must be greater than 0"
        )

    if active_area_height_mm <= 0:
        raise ValueError(
            "Active sensor height must be greater than 0"
        )

    fx = focal_length_pixels(
        focal_length_mm=focal_length_mm,
        active_pixels=active_pixel_width,
        active_area_mm=active_area_width_mm,
    )

    fy = focal_length_pixels(
        focal_length_mm=focal_length_mm,
        active_pixels=active_pixel_height,
        active_area_mm=active_area_height_mm,
    )

    cx = active_pixel_width / 2.0
    cy = active_pixel_height / 2.0

    return CameraIntrinsics(
        fx=fx,
        fy=fy,
        cx=cx,
        cy=cy,
    )