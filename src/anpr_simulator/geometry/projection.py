from dataclasses import dataclass

from anpr_simulator.geometry.camera_intrinsics import CameraIntrinsics


@dataclass(frozen=True)
class Point3D:
    """
    A point in the camera coordinate system.

    x: horizontal position
    y: vertical position
    z: distance from camera
    """

    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Point2D:
    """
    A point in the image plane.

    u: horizontal pixel coordinate
    v: vertical pixel coordinate

    Compatibility aliases:
        x == u
        y == v
    """

    u: float
    v: float

    @property
    def x(self) -> float:
        return self.u

    @property
    def y(self) -> float:
        return self.v


def project_point(
    point: Point3D,
    intrinsics: CameraIntrinsics,
) -> Point2D:
    """
    Project a 3D camera-coordinate point onto the image plane.

    Equations:

        u = fx * X / Z + cx
        v = fy * Y / Z + cy

    Args:
        point:
            3D point expressed in camera coordinates.

        intrinsics:
            Camera intrinsic parameters.

    Returns:
        Projected 2D image coordinate.

    Raises:
        ValueError:
            If the point is on or behind the camera.
    """

    if point.z <= 0:
        raise ValueError(
            "Point must be in front of the camera (z > 0)"
        )

    u = (
        intrinsics.fx
        * point.x
        / point.z
        + intrinsics.cx
    )

    v = (
        intrinsics.cy
        - intrinsics.fy
        * point.y
        / point.z
    )

    return Point2D(
        u=u,
        v=v,
    )