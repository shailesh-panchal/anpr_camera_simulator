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
from anpr_simulator.geometry.camera_pose import (
    CameraPose,
)
from anpr_simulator.geometry.transform import (
    world_to_camera,
)

from anpr_simulator.geometry.vehicle_state import (
    VehicleState,
)

from anpr_simulator.geometry.world import (
    WorldPoint,
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

def project_vehicle_plate(
    vehicle_state: VehicleState,
    plate_dimensions: LicensePlateDimensions,
    camera_pose: CameraPose,
    intrinsics: CameraIntrinsics,
    vehicle_length_m: float = 0.0,
) -> ProjectedPlate:
    """
    Project the vehicle's license plate onto the camera image.
    
    The plate is positioned at the BACK of the vehicle (vehicle_z + vehicle_length/2)
    to ensure proper alignment with the rear panel visible from behind.
    """

    # Calculate the Z position of the vehicle's back panel
    plate_z_m = vehicle_state.z_m + (vehicle_length_m / 2.0) if vehicle_length_m > 0 else vehicle_state.z_m
    
    corners = license_plate_corners(
        center_x_m=vehicle_state.x_m,
        center_y_m=vehicle_state.y_m,
        distance_z_m=plate_z_m,
        dimensions=plate_dimensions,
    )

    image_points = []

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

        image_point = project_point(
            camera_point,
            intrinsics,
        )

        image_points.append(image_point)

    return ProjectedPlate(
        top_left=image_points[0],
        top_right=image_points[1],
        bottom_left=image_points[2],
        bottom_right=image_points[3],
    )