from dataclasses import dataclass

from anpr_simulator.geometry.projection import(
    Point2D,
    Point3D,
    project_point,
)
from anpr_simulator.geometry.camera_intrinsics import CameraIntrinsics
from anpr_simulator.geometry.license_plate import (
    LicensePlateDimensions,
    license_plate_corners,
)

@dataclass(frozen=True)
class ProjectedPlate:
    top_left: Point2D
    top_right: Point2D
    bottom_left: Point2D
    bottom_right: Point2D

    @property
    def width_pixels(self) -> float:
        return abs(self.top_right.u - self.top_left.u)

    @property
    def height_pixels(self) -> float:
        return abs(self.bottom_left.v - self.top_left.v)


def project_plate(
    center_x_m: float,
    center_y_m: float,
    distance_z_m: float,
    dimensions: LicensePlateDimensions,
    intrinsics: CameraIntrinsics,
) -> ProjectedPlate:

    corners_3d = license_plate_corners(
        center_x_m=center_x_m,
        center_y_m=center_y_m,
        distance_z_m=distance_z_m,
        dimensions=dimensions,
    )

    projected_corners = [
        project_point(point, intrinsics)
        for point in corners_3d
    ]

    return ProjectedPlate(
        top_left=projected_corners[0],
        top_right=projected_corners[1],
        bottom_left=projected_corners[2],
        bottom_right=projected_corners[3],
    )
