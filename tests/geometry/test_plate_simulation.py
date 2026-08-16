import pytest

from anpr_simulator.geometry.camera_intrinsics import (
    CameraIntrinsics,
)

from anpr_simulator.geometry.camera_pose import (
    CameraPose,
)

from anpr_simulator.geometry.license_plate import (
    LicensePlateDimensions,
)

from anpr_simulator.geometry.plate_simulation import (
    ProjectedPlate,
    simulate_plate_at_time,
)

from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleDirection,
    VehicleTrajectory,
)


def test_simulate_plate_at_time():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    camera = CameraPose(
        x_m=0.0,
        y_m=0.0,
        z_m=0.0,
        pitch_deg=0.0,
    )

    trajectory = VehicleTrajectory(
        initial_z_m=50.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.0,
        direction=VehicleDirection.MOVING_AWAY,
    )

    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    result = simulate_plate_at_time(
        trajectory=trajectory,
        time_s=0.0,
        plate_center_y_m=0.0,
        plate_dimensions=plate,
        camera_pose=camera,
        intrinsics=intrinsics,
    )

    assert isinstance(
        result,
        ProjectedPlate,
    )

    assert result.width_pixels == pytest.approx(
        973.4 * 0.52 / 50.0
    )

    assert result.height_pixels == pytest.approx(
        983.4 * 0.11 / 50.0
    )

def test_plate_size_changes_with_vehicle_distance():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    camera = CameraPose(
        x_m=0.0,
        y_m=0.0,
        z_m=0.0,
        pitch_deg=0.0,
    )

    trajectory = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.0,
        direction=VehicleDirection.APPROACHING_CAMERA,
    )

    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    far_plate = simulate_plate_at_time(
        trajectory=trajectory,
        time_s=0.0,
        plate_center_y_m=0.0,
        plate_dimensions=plate,
        camera_pose=camera,
        intrinsics=intrinsics,
    )

    near_plate = simulate_plate_at_time(
        trajectory=trajectory,
        time_s=5.0,
        plate_center_y_m=0.0,
        plate_dimensions=plate,
        camera_pose=camera,
        intrinsics=intrinsics,
    )

    assert near_plate.width_pixels > far_plate.width_pixels
    assert near_plate.height_pixels > far_plate.height_pixels

