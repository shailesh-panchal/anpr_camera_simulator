from dataclasses import dataclass

from anpr_simulator.geometry.camera_intrinsics import CameraIntrinsics
from anpr_simulator.geometry.license_plate import (
    LicensePlateDimensions,
    license_plate_corners,
)
from anpr_simulator.geometry.projection import (
    Point2D,
    project_point,
)
from anpr_simulator.geometry.transform import (
    world_to_camera,
)
from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleTrajectory,
)
from anpr_simulator.geometry.world import WorldPoint


@dataclass(frozen=True)
class ProjectedPlate:
    """
    License plate projected onto the camera image.
    """

    top_left: Point2D
    top_right: Point2D
    bottom_left: Point2D
    bottom_right: Point2D

    @property
    def width_pixels(self) -> float:
        return abs(
            self.top_right.u - self.top_left.u
        )

    @property
    def height_pixels(self) -> float:
        return abs(
            self.bottom_left.v - self.top_left.v
        )


def simulate_plate_at_time(
    trajectory: VehicleTrajectory,
    time_s: float,
    plate_center_y_m: float,
    plate_dimensions: LicensePlateDimensions,
    camera_pose,
    intrinsics: CameraIntrinsics,
) -> ProjectedPlate:

    # 1. Get vehicle position at this time.
    x_m, _, z_m = trajectory.position_at_time(time_s)

    # 2. Generate license plate corners in world coordinates.
    corners = license_plate_corners(
        center_x_m=x_m,
        center_y_m=plate_center_y_m,
        distance_z_m=z_m,
        dimensions=plate_dimensions,
    )

    # 3. Convert each corner from world coordinates
    #    to camera coordinates.
    camera_points = []

    for corner in corners:

        world_point = WorldPoint(
            x_m=corner.x,
            y_m=corner.y,
            z_m=corner.z,
        )

        camera_point = world_to_camera(
            world_point,
            camera_pose,
        )

        camera_points.append(camera_point)

    # 4. Project camera coordinates onto image.
    image_points = [
        project_point(
            point,
            intrinsics,
        )
        for point in camera_points
    ]

    return ProjectedPlate(
        top_left=image_points[0],
        top_right=image_points[1],
        bottom_left=image_points[2],
        bottom_right=image_points[3],
    )