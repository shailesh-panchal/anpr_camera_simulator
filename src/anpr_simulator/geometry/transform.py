import math

from anpr_simulator.geometry.camera_pose import CameraPose
from anpr_simulator.geometry.projection import Point3D
from anpr_simulator.geometry.world import WorldPoint


def world_to_camera(
    point: WorldPoint,
    camera: CameraPose,
) -> Point3D:

    # Translate world point relative to camera
    dx = point.x_m - camera.x_m
    dy = point.y_m - camera.y_m
    dz = point.z_m - camera.z_m

    pitch_rad = math.radians(camera.pitch_deg)

    cos_pitch = math.cos(pitch_rad)
    sin_pitch = math.sin(pitch_rad)

    # Rotation around X axis
    x_camera = dx

    y_camera = (
        cos_pitch * dy
        - sin_pitch * dz
    )

    z_camera = (
        sin_pitch * dy
        + cos_pitch * dz
    )

    return Point3D(
        x=x_camera,
        y=y_camera,
        z=z_camera,
    )