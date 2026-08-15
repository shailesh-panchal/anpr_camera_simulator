from dataclasses import dataclass

from anpr_simulator.geometry.projection import Point3D

@dataclass(frozen=True)
class LicensePlateDimensions:
    width_m: float
    height_m: float


def license_plate_corners(
    center_x_m: float,
    center_y_m: float,
    distance_z_m: float,
    dimensions: LicensePlateDimensions,
) -> tuple[Point3D, Point3D, Point3D, Point3D]:

    half_width = dimensions.width_m / 2.0
    half_height = dimensions.height_m / 2.0

    top_left = Point3D(
        x=center_x_m - half_width,
        y=center_y_m - half_height,
        z=distance_z_m,
    )

    top_right = Point3D(
        x=center_x_m + half_width,
        y=center_y_m - half_height,
        z=distance_z_m,
    )

    bottom_left = Point3D(
        x=center_x_m - half_width,
        y=center_y_m + half_height,
        z=distance_z_m,
    )

    bottom_right = Point3D(
        x=center_x_m + half_width,
        y=center_y_m + half_height,
        z=distance_z_m,
    )

    return (
        top_left,
        top_right,
        bottom_left,
        bottom_right,
    )
