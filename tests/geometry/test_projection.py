import pytest

from anpr_simulator.geometry.camera_intrinsics import (
    CameraIntrinsics,
)

from anpr_simulator.geometry.projection import (
    Point2D,
    Point3D,
    project_point,
)


def test_project_center_point():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    point = Point3D(
        x=0.0,
        y=0.0,
        z=20.0,
    )

    result = project_point(
        point,
        intrinsics,
    )

    assert isinstance(result, Point2D)

    assert result.u == pytest.approx(968.0)
    assert result.v == pytest.approx(550.0)

def test_project_point_to_right():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    point = Point3D(
        x=2.0,
        y=0.0,
        z=20.0,
    )

    result = project_point(
        point,
        intrinsics,
    )

    expected_u = (
        973.4 * 2.0 / 20.0
        + 968.0
    )

    assert result.u == pytest.approx(expected_u)
    assert result.v == pytest.approx(550.0)

def test_project_point_up():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    point = Point3D(
        x=0.0,
        y=-2.0,
        z=20.0,
    )

    result = project_point(
        point,
        intrinsics,
    )

    expected_v = (
        983.4 * (-2.0) / 20.0
        + 550.0
    )

    assert result.u == pytest.approx(968.0)
    assert result.v == pytest.approx(expected_v)

def test_project_point_at_camera():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    point = Point3D(
        x=0.0,
        y=0.0,
        z=0.0,
    )

    with pytest.raises(ValueError):

        project_point(
            point,
            intrinsics,
        )

def test_project_point_behind_camera():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    point = Point3D(
        x=0.0,
        y=0.0,
        z=-10.0,
    )

    with pytest.raises(ValueError):

        project_point(
            point,
            intrinsics,
        )
