import pytest

from anpr_simulator.geometry.vehicle import (
    VehicleDimensions,
)

from anpr_simulator.geometry.vehicle_state import (
    VehicleState,
    vehicle_state_at_time,
)

from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleDirection,
    VehicleTrajectory,
)


def test_vehicle_state_at_time():

    vehicle = VehicleDimensions(
        length_m=4.5,
        width_m=1.8,
        height_m=1.5,
        license_plate_height_m=0.5,
    )

    trajectory = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.0,
        direction=VehicleDirection.APPROACHING_CAMERA,
    )

    result = vehicle_state_at_time(
        trajectory=trajectory,
        dimensions=vehicle,
        time_s=5.0,
    )

    assert isinstance(
        result,
        VehicleState,
    )

    assert result.x_m == pytest.approx(0.0)
    assert result.y_m == pytest.approx(0.5)
    assert result.z_m == pytest.approx(50.0)