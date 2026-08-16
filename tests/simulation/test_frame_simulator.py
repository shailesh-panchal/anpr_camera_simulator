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

from anpr_simulator.geometry.plate_projection import (
    ProjectedPlate,
    project_vehicle_plate
)

from anpr_simulator.geometry.vehicle import (
    VehicleDimensions,
)

from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleDirection,
    VehicleTrajectory,
)

from anpr_simulator.simulation.frame_simulator import (
    simulate_frame,
)
from anpr_simulator.simulation.simulation_frame import (
    SimulationFrame,
)

def test_simulate_frame():

    # Camera intrinsic parameters
    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    # Camera mounted at 5 m height.
    # No pitch initially so that we can
    # verify the basic pipeline first.
    camera_pose = CameraPose(
        x_m=0.0,
        y_m=5.0,
        z_m=0.0,
        pitch_deg=0.0,
    )

    # Vehicle physical dimensions
    vehicle = VehicleDimensions(
        length_m=4.5,
        width_m=1.8,
        height_m=1.5,
        license_plate_height_m=0.5,
    )

    # License plate physical dimensions
    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    # Vehicle starts at 100 m and approaches
    # the camera at 10 m/s.
    trajectory = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.0,
        direction=VehicleDirection.APPROACHING_CAMERA,
    )

    # Simulate frame at t = 5 seconds.
    #
    # Vehicle position:
    #
    # Z = 100 - (10 * 5)
    #   = 50 m
    #
    result = simulate_frame(
        trajectory=trajectory,
        vehicle_dimensions=vehicle,
        plate_dimensions=plate,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
        frame_number=1,
        time_s=5.0,
    )

    # Verify returned object
    assert isinstance(
        result,
        SimulationFrame,
    )

    # Plate must have a positive projected size
    assert result.frame_number == 1
    assert result.timestamp_s == pytest.approx(5.0)

    assert result.vehicle_state.z_m == pytest.approx(
        50.0
    )

    assert result.projected_plate.width_pixels > 0
    assert result.projected_plate.height_pixels > 0

def test_simulate_frame_vehicle_approaching():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    camera_pose = CameraPose(
        x_m=0.0,
        y_m=5.0,
        z_m=0.0,
        pitch_deg=0.0,
    )

    vehicle = VehicleDimensions(
        length_m=4.5,
        width_m=1.8,
        height_m=1.5,
        license_plate_height_m=0.5,
    )

    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    trajectory = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.0,
        direction=VehicleDirection.APPROACHING_CAMERA,
    )

    far_result = simulate_frame(
        trajectory=trajectory,
        vehicle_dimensions=vehicle,
        plate_dimensions=plate,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
        frame_number=1,
        time_s=0.0,
    )

    near_result = simulate_frame(
        trajectory=trajectory,
        vehicle_dimensions=vehicle,
        plate_dimensions=plate,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
        frame_number=1,
        time_s=5.0,
    )

    assert near_result.projected_plate.width_pixels > far_result.projected_plate.width_pixels
    assert near_result.projected_plate.height_pixels > far_result.projected_plate.height_pixels

def test_simulate_frame_vehicle_moving_away():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    camera_pose = CameraPose(
        x_m=0.0,
        y_m=5.0,
        z_m=0.0,
        pitch_deg=0.0,
    )

    vehicle = VehicleDimensions(
        length_m=4.5,
        width_m=1.8,
        height_m=1.5,
        license_plate_height_m=0.5,
    )

    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    trajectory = VehicleTrajectory(
        initial_z_m=50.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.0,
        direction=VehicleDirection.MOVING_AWAY,
    )

    near_result = simulate_frame(
        trajectory=trajectory,
        vehicle_dimensions=vehicle,
        plate_dimensions=plate,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
        frame_number=1,
        time_s=0.0,
    )

    far_result = simulate_frame(
        trajectory=trajectory,
        vehicle_dimensions=vehicle,
        plate_dimensions=plate,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
        frame_number=1,
        time_s=5.0,
    )

    assert near_result.projected_plate.width_pixels > far_result.projected_plate.width_pixels
    assert near_result.projected_plate.height_pixels > far_result.projected_plate.height_pixels

