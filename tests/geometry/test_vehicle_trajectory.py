import pytest

from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleDirection,
    VehicleTrajectory,
)


def test_vehicle_approaching_camera():

    trajectory = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.5,
        direction=VehicleDirection.APPROACHING_CAMERA,
    )

    position = trajectory.position_at_time(5.0)

    assert position == pytest.approx(
        (0.0, 0.5, 50.0)
    )

def test_vehicle_moving_away():

    trajectory = VehicleTrajectory(
        initial_z_m=50.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.5,
        direction=VehicleDirection.MOVING_AWAY,
    )

    position = trajectory.position_at_time(5.0)

    assert position == pytest.approx(
        (0.0, 0.5, 100.0)
    )

def test_vehicle_position_at_time_zero():

    approaching = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.5,
        direction=VehicleDirection.APPROACHING_CAMERA,
    )

    moving_away = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.5,
        direction=VehicleDirection.MOVING_AWAY,
    )

    assert approaching.position_at_time(0.0) == pytest.approx(
        (0.0, 0.5, 100.0)
    )

    assert moving_away.position_at_time(0.0) == pytest.approx(
        (0.0, 0.5, 100.0)
    )