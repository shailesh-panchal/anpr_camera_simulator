import pytest

from anpr_simulator.geometry.camera_pose import CameraPose
from anpr_simulator.geometry.transform import world_to_camera
from anpr_simulator.geometry.world import WorldPoint


def test_world_point_in_front_of_camera():

    camera = CameraPose(
        x_m=0.0,
        y_m=5.0,
        z_m=0.0,
        pitch_deg=0.0,
    )

    point = WorldPoint(
        x_m=0.0,
        y_m=5.0,
        z_m=50.0,
    )

    result = world_to_camera(
        point,
        camera,
    )

    assert result.x == pytest.approx(0.0)
    assert result.y == pytest.approx(0.0)
    assert result.z == pytest.approx(50.0)

def test_camera_height_difference():

    camera = CameraPose(
        x_m=0.0,
        y_m=5.0,
        z_m=0.0,
        pitch_deg=0.0,
    )

    point = WorldPoint(
        x_m=0.0,
        y_m=0.5,
        z_m=50.0,
    )

    result = world_to_camera(
        point,
        camera,
    )

    assert result.x == pytest.approx(0.0)
    assert result.y == pytest.approx(-4.5)
    assert result.z == pytest.approx(50.0)

def test_world_to_camera_with_pitch():

    camera = CameraPose(
        x_m=0.0,
        y_m=5.0,
        z_m=0.0,
        pitch_deg=10.0,
    )

    point = WorldPoint(
        x_m=0.0,
        y_m=0.5,
        z_m=50.0,
    )

    result = world_to_camera(
        point,
        camera,
    )

    assert result.x == pytest.approx(0.0)

    assert result.y == pytest.approx(
        -13.11,
        abs=0.01,
    )

    assert result.z == pytest.approx(
        48.45,
        abs=0.01,
    )